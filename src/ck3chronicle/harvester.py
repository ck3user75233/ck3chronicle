"""Discover, stage, verify, and atomically preserve CK3 evidence bundles."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

LOG_NAMES = (
    "error.log",
    "game.log",
    "debug.log",
    "database_conflicts.log",
    "setup.log",
    "text.log",
)
PRINCIPAL_LOG_NAMES = ("error.log", "debug.log", "game.log")
MANIFEST_NAME = "manifest.json"
MANIFEST_VERSION = 1
BUNDLE_HASH_ALGORITHM = "ck3chronicle.bundle.v1"


class CaptureError(RuntimeError):
    """Base class for evidence-capture failures."""


class InvalidCaptureInput(CaptureError):
    """The source cannot represent a CK3 session."""


class UnstableCapture(CaptureError):
    """The live evidence changed while it was being captured."""


class ArchiveIntegrityError(CaptureError):
    """A finalized archive does not match its content identity."""


@dataclass(frozen=True)
class FileIdentity:
    bytes: int
    mtime_ns: int
    sha256: str


@dataclass(frozen=True)
class EvidenceSource:
    source_path: Path
    kind: str
    identity_path: str
    retained_path: str


@dataclass(frozen=True)
class CapturedFile:
    kind: str
    identity_path: str
    rel_path: str
    sha256: str
    bytes: int
    source_mtime_ns: int

    def manifest_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "identity_path": self.identity_path,
            "rel_path": self.rel_path,
            "sha256": self.sha256,
            "bytes": self.bytes,
            "source_mtime_ns": self.source_mtime_ns,
        }


@dataclass
class EvidenceBundle:
    logs_root: Path
    log_files: list[Path] = field(default_factory=list)
    crash_folder: Path | None = None
    crash_files: list[Path] = field(default_factory=list)
    evidence_bundle_hash: str = ""
    identities: dict[str, FileIdentity] = field(default_factory=dict)


@dataclass(frozen=True)
class SnapshotResult:
    evidence_bundle_hash: str
    dest_dir: Path
    files_copied: int
    was_existing: bool
    captured_at: str
    files: tuple[CapturedFile, ...]
    missing_principal_logs: tuple[str, ...]
    manifest_sha256: str


def discover_logs(root: Path) -> list[Path]:
    """Return regular, non-symlink approved log files in canonical order."""
    found: list[Path] = []
    for name in LOG_NAMES:
        candidate = root / name
        if candidate.exists():
            if candidate.is_symlink() or not candidate.is_file():
                raise InvalidCaptureInput(f"evidence source is not a regular file: {name}")
            found.append(candidate)
    return found


def discover_crash_folder(root: Path) -> Path | None:
    """Return only an explicitly colocated/fixture crash folder.

    Real CK3 crashes live beside ``logs``. They are deliberately not selected
    here because "newest crash" does not establish that it belongs to this run.
    A run-window-aware crash collector can pass an explicit folder in a later
    checkpoint without poisoning ordinary session capture with stale evidence.
    """
    crashes_dir = root / "crashes"
    if crashes_dir.is_dir():
        candidates = [d for d in crashes_dir.iterdir() if d.is_dir()]
        if candidates:
            return max(candidates, key=lambda d: d.stat().st_mtime_ns)
    crash_dir = root / "crash"
    if crash_dir.is_dir():
        return crash_dir
    return None


def hash_file(path: Path) -> str:
    """Return the lowercase SHA-256 digest of exact file bytes."""
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _source_entries(bundle: EvidenceBundle) -> tuple[EvidenceSource, ...]:
    entries: list[EvidenceSource] = [
        EvidenceSource(
            source_path=path,
            kind="log",
            identity_path=path.relative_to(bundle.logs_root).as_posix(),
            retained_path=path.relative_to(bundle.logs_root).as_posix(),
        )
        for path in bundle.log_files
    ]
    if bundle.crash_folder is not None:
        entries.extend(
            EvidenceSource(
                source_path=path,
                kind="crash",
                identity_path=path.relative_to(bundle.crash_folder).as_posix(),
                retained_path=(
                    Path("crash") / path.relative_to(bundle.crash_folder)
                ).as_posix(),
            )
            for path in bundle.crash_files
        )
    return tuple(entries)


def _identity_key(entry: EvidenceSource) -> str:
    return f"{entry.kind}:{entry.identity_path}"


def _stable_identity(path: Path) -> FileIdentity:
    before = path.stat()
    digest = hash_file(path)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise UnstableCapture(f"source changed while hashing: {path.name}")
    return FileIdentity(
        bytes=after.st_size,
        mtime_ns=after.st_mtime_ns,
        sha256=digest,
    )


def _bundle_hash(records: Iterable[tuple[str, str, str]]) -> str:
    canonical = "\n".join(
        sorted(f"{kind}:{rel_path}:{digest}" for kind, rel_path, digest in records)
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _compute_bundle_hash(bundle: EvidenceBundle) -> str:
    """Compute the v1 bundle identity from the bundle's frozen identities."""
    return _bundle_hash(
        (
            entry.kind,
            entry.identity_path,
            bundle.identities[_identity_key(entry)].sha256,
        )
        for entry in _source_entries(bundle)
    )


def build_bundle(logs_root: Path) -> EvidenceBundle:
    """Inventory and hash a stable set of approved live evidence files."""
    logs_root = Path(logs_root)
    if not logs_root.is_dir():
        raise InvalidCaptureInput(f"logs directory does not exist: {logs_root}")
    log_files = discover_logs(logs_root)
    if not any(path.name.casefold() == "error.log" for path in log_files):
        raise InvalidCaptureInput("mandatory error.log is missing")

    crash_folder = discover_crash_folder(logs_root)
    crash_files: list[Path] = []
    if crash_folder:
        crash_files = sorted(
            path
            for path in crash_folder.rglob("*")
            if path.is_file() and not path.is_symlink()
        )

    bundle = EvidenceBundle(
        logs_root=logs_root,
        log_files=log_files,
        crash_folder=crash_folder,
        crash_files=crash_files,
    )
    for entry in _source_entries(bundle):
        bundle.identities[_identity_key(entry)] = _stable_identity(entry.source_path)
    bundle.evidence_bundle_hash = _compute_bundle_hash(bundle)
    return bundle


def _copy_exact(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with src.open("rb") as source, dst.open("xb") as target:
        shutil.copyfileobj(source, target, length=1024 * 1024)
        target.flush()
        os.fsync(target.fileno())
    shutil.copystat(src, dst, follow_symlinks=False)


def _manifest_payload(
    *,
    bundle_hash: str,
    captured_at: str,
    files: tuple[CapturedFile, ...],
) -> dict[str, Any]:
    present_logs = {item.identity_path for item in files if item.kind == "log"}
    missing = [name for name in PRINCIPAL_LOG_NAMES if name not in present_logs]
    return {
        "manifest_version": MANIFEST_VERSION,
        "hash_algorithm": BUNDLE_HASH_ALGORITHM,
        "capture_status": "finalized",
        "evidence_bundle_hash": bundle_hash,
        "captured_at": captured_at,
        "evidence_completeness": "complete" if not missing else "partial",
        "principal_logs": {
            name: "present" if name in present_logs else "missing"
            for name in PRINCIPAL_LOG_NAMES
        },
        "files": [item.manifest_dict() for item in files],
    }


def _write_manifest(directory: Path, payload: dict[str, Any]) -> str:
    encoded = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path = directory / MANIFEST_NAME
    with path.open("xb") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    return hashlib.sha256(encoded).hexdigest()


def _publish_manifest_atomic(directory: Path, payload: dict[str, Any]) -> str:
    """Publish a manifest to a legacy archive without overwrite races."""
    encoded = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    staging_root = directory.parent / ".staging"
    staging_root.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        prefix="legacy-manifest-", suffix=".tmp", dir=staging_root
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            # Hard-link publication is atomic and fails if another adopter won.
            os.link(temp_path, directory / MANIFEST_NAME)
        except FileExistsError:
            pass
        raw = (directory / MANIFEST_NAME).read_bytes()
        return hashlib.sha256(raw).hexdigest()
    finally:
        temp_path.unlink(missing_ok=True)


def _load_manifest(directory: Path) -> tuple[dict[str, Any], str]:
    path = directory / MANIFEST_NAME
    try:
        raw = path.read_bytes()
        payload = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ArchiveIntegrityError(f"invalid capture manifest: {path}") from exc
    if not isinstance(payload, dict):
        raise ArchiveIntegrityError(f"capture manifest is not an object: {path}")
    return payload, hashlib.sha256(raw).hexdigest()


def _files_from_manifest(payload: dict[str, Any]) -> tuple[CapturedFile, ...]:
    if payload.get("manifest_version") != MANIFEST_VERSION:
        raise ArchiveIntegrityError("unsupported capture manifest version")
    if payload.get("hash_algorithm") != BUNDLE_HASH_ALGORITHM:
        raise ArchiveIntegrityError("unsupported bundle hash algorithm")
    try:
        files = tuple(
            CapturedFile(
                kind=item["kind"],
                identity_path=item["identity_path"],
                rel_path=item["rel_path"],
                sha256=item["sha256"],
                bytes=int(item["bytes"]),
                source_mtime_ns=int(item["source_mtime_ns"]),
            )
            for item in payload["files"]
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ArchiveIntegrityError("malformed capture manifest file entry") from exc
    for item in files:
        rel = Path(item.rel_path)
        identity = Path(item.identity_path)
        if (
            rel.is_absolute()
            or ".." in rel.parts
            or identity.is_absolute()
            or ".." in identity.parts
        ):
            raise ArchiveIntegrityError("capture manifest contains an unsafe path")
        if item.kind not in {"log", "crash"}:
            raise ArchiveIntegrityError("capture manifest contains an unknown kind")
    return files


def validate_snapshot(
    directory: Path,
    *,
    expected_hash: str | None = None,
) -> tuple[tuple[CapturedFile, ...], str]:
    """Verify a finalized directory, its manifest, and every retained byte."""
    payload, manifest_sha256 = _load_manifest(directory)
    bundle_hash = payload.get("evidence_bundle_hash")
    if not isinstance(bundle_hash, str) or len(bundle_hash) != 64:
        raise ArchiveIntegrityError("capture manifest has an invalid bundle hash")
    if directory.name != bundle_hash:
        raise ArchiveIntegrityError("archive directory name disagrees with manifest")
    if expected_hash is not None and bundle_hash != expected_hash:
        raise ArchiveIntegrityError("archive identity disagrees with expected hash")
    if payload.get("capture_status") != "finalized":
        raise ArchiveIntegrityError("capture manifest is not finalized")

    files = _files_from_manifest(payload)
    actual_records: list[tuple[str, str, str]] = []
    seen_paths: set[str] = set()
    for item in files:
        if item.rel_path in seen_paths:
            raise ArchiveIntegrityError("capture manifest repeats a retained path")
        seen_paths.add(item.rel_path)
        retained = directory / Path(item.rel_path)
        if retained.is_symlink() or not retained.is_file():
            raise ArchiveIntegrityError(f"archived evidence is missing: {item.rel_path}")
        if retained.stat().st_size != item.bytes or hash_file(retained) != item.sha256:
            raise ArchiveIntegrityError(f"archived evidence hash mismatch: {item.rel_path}")
        actual_records.append((item.kind, item.identity_path, item.sha256))
    actual_paths = {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if path.is_file()
        and path.relative_to(directory).as_posix() != MANIFEST_NAME
    }
    if actual_paths != seen_paths:
        raise ArchiveIntegrityError("archive contains unlisted or missing evidence files")
    if _bundle_hash(actual_records) != bundle_hash:
        raise ArchiveIntegrityError("manifest files do not derive the bundle identity")
    present_logs = {item.identity_path for item in files if item.kind == "log"}
    expected_principal = {
        name: "present" if name in present_logs else "missing"
        for name in PRINCIPAL_LOG_NAMES
    }
    if payload.get("principal_logs") != expected_principal:
        raise ArchiveIntegrityError("principal-log status disagrees with manifest files")
    expected_completeness = (
        "complete"
        if all(state == "present" for state in expected_principal.values())
        else "partial"
    )
    if payload.get("evidence_completeness") != expected_completeness:
        raise ArchiveIntegrityError("evidence completeness is inconsistent")
    return files, manifest_sha256


def _evidence_descriptor(files: Iterable[CapturedFile]) -> tuple[tuple[Any, ...], ...]:
    """Compare immutable evidence fields while ignoring source mtimes."""
    return tuple(
        sorted(
            (item.kind, item.identity_path, item.rel_path, item.sha256, item.bytes)
            for item in files
        )
    )


def _existing_snapshot_result(
    directory: Path,
    *,
    expected_hash: str,
    staged_files: tuple[CapturedFile, ...],
) -> SnapshotResult:
    existing_files, manifest_sha256 = validate_snapshot(
        directory, expected_hash=expected_hash
    )
    if _evidence_descriptor(existing_files) != _evidence_descriptor(staged_files):
        raise ArchiveIntegrityError(
            "existing archive manifest disagrees with staged evidence"
        )
    payload, _ = _load_manifest(directory)
    principal = payload.get("principal_logs", {})
    captured_at = payload.get("captured_at")
    if not isinstance(captured_at, str) or not captured_at:
        raise ArchiveIntegrityError("capture manifest has no capture timestamp")
    return SnapshotResult(
        evidence_bundle_hash=expected_hash,
        dest_dir=directory,
        files_copied=0,
        was_existing=True,
        captured_at=captured_at,
        files=existing_files,
        missing_principal_logs=tuple(
            name
            for name in PRINCIPAL_LOG_NAMES
            if principal.get(name) == "missing"
        ),
        manifest_sha256=manifest_sha256,
    )


def read_snapshot(directory: Path) -> SnapshotResult:
    """Load and fully verify one manifest-backed finalized archive."""
    directory = Path(directory)
    files, manifest_sha256 = validate_snapshot(
        directory, expected_hash=directory.name
    )
    payload, _ = _load_manifest(directory)
    captured_at = payload.get("captured_at")
    if not isinstance(captured_at, str) or not captured_at:
        raise ArchiveIntegrityError("capture manifest has no capture timestamp")
    principal = payload["principal_logs"]
    return SnapshotResult(
        evidence_bundle_hash=directory.name,
        dest_dir=directory,
        files_copied=0,
        was_existing=True,
        captured_at=captured_at,
        files=files,
        missing_principal_logs=tuple(
            name
            for name in PRINCIPAL_LOG_NAMES
            if principal[name] == "missing"
        ),
        manifest_sha256=manifest_sha256,
    )


def adopt_legacy_archive(directory: Path) -> SnapshotResult:
    """Verify a pre-P1 content-addressed directory and add its manifest."""
    directory = Path(directory)
    if (directory / MANIFEST_NAME).exists():
        return read_snapshot(directory)
    if not directory.is_dir() or len(directory.name) != 64:
        raise ArchiveIntegrityError("legacy archive has an invalid directory identity")

    files: list[CapturedFile] = []
    allowed_paths: set[str] = set()
    for name in LOG_NAMES:
        path = directory / name
        if path.exists():
            if path.is_symlink() or not path.is_file():
                raise ArchiveIntegrityError(f"legacy evidence is not regular: {name}")
            stat = path.stat()
            files.append(
                CapturedFile(
                    kind="log",
                    identity_path=name,
                    rel_path=name,
                    sha256=hash_file(path),
                    bytes=stat.st_size,
                    source_mtime_ns=stat.st_mtime_ns,
                )
            )
            allowed_paths.add(name)
    crash_root = directory / "crash"
    if crash_root.is_dir():
        for path in sorted(crash_root.rglob("*")):
            if path.is_symlink():
                raise ArchiveIntegrityError("legacy crash evidence contains a symlink")
            if path.is_file():
                identity_path = path.relative_to(crash_root).as_posix()
                retained_path = path.relative_to(directory).as_posix()
                stat = path.stat()
                files.append(
                    CapturedFile(
                        kind="crash",
                        identity_path=identity_path,
                        rel_path=retained_path,
                        sha256=hash_file(path),
                        bytes=stat.st_size,
                        source_mtime_ns=stat.st_mtime_ns,
                    )
                )
                allowed_paths.add(retained_path)
    actual_paths = {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if path.is_file()
    }
    if actual_paths != allowed_paths:
        raise ArchiveIntegrityError("legacy archive contains unsupported evidence files")
    if not any(item.identity_path == "error.log" for item in files if item.kind == "log"):
        raise ArchiveIntegrityError("legacy archive is missing mandatory error.log")

    captured_files = tuple(sorted(files, key=lambda item: (item.rel_path, item.kind)))
    derived_hash = _bundle_hash(
        (item.kind, item.identity_path, item.sha256) for item in captured_files
    )
    if derived_hash != directory.name:
        raise ArchiveIntegrityError("legacy archive bytes disagree with directory identity")
    captured_at = datetime.fromtimestamp(
        directory.stat().st_mtime, timezone.utc
    ).isoformat()
    payload = _manifest_payload(
        bundle_hash=derived_hash,
        captured_at=captured_at,
        files=captured_files,
    )
    _publish_manifest_atomic(directory, payload)
    return read_snapshot(directory)


def _adopt_legacy_snapshot(
    directory: Path,
    payload: dict[str, Any],
    expected_files: tuple[CapturedFile, ...],
) -> str:
    """Add a manifest to a byte-identical pre-P1 archive without recopying it."""
    expected_paths = {item.rel_path for item in expected_files}
    actual_paths = {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if path.is_file()
        and path.relative_to(directory).as_posix() != MANIFEST_NAME
    }
    if actual_paths != expected_paths:
        raise ArchiveIntegrityError("legacy archive file set is incomplete or unexpected")
    for item in expected_files:
        path = directory / Path(item.rel_path)
        if path.stat().st_size != item.bytes or hash_file(path) != item.sha256:
            raise ArchiveIntegrityError(f"legacy archive mismatch: {item.rel_path}")

    return _publish_manifest_atomic(directory, payload)


def snapshot(bundle: EvidenceBundle, dest_root: Path) -> SnapshotResult:
    """Stage, verify, and atomically promote one content-addressed bundle."""
    if not any(path.name.casefold() == "error.log" for path in bundle.log_files):
        raise InvalidCaptureInput("mandatory error.log is missing")

    sessions_root = Path(dest_root) / "sessions"
    staging_root = sessions_root / ".staging"
    staging_root.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="capture-", dir=staging_root))
    captured_at = datetime.now(timezone.utc).isoformat()
    copied: list[CapturedFile] = []
    promoted = False
    try:
        for entry in _source_entries(bundle):
            identity = bundle.identities[_identity_key(entry)]
            before = entry.source_path.stat()
            if (before.st_size, before.st_mtime_ns) != (
                identity.bytes,
                identity.mtime_ns,
            ):
                raise UnstableCapture(f"source changed before copy: {entry.identity_path}")
            retained = stage / Path(entry.retained_path)
            _copy_exact(entry.source_path, retained)
            after = entry.source_path.stat()
            staged_hash = hash_file(retained)
            if (
                (after.st_size, after.st_mtime_ns)
                != (identity.bytes, identity.mtime_ns)
                or retained.stat().st_size != identity.bytes
                or staged_hash != identity.sha256
            ):
                raise UnstableCapture(f"source changed during copy: {entry.identity_path}")
            copied.append(
                CapturedFile(
                    kind=entry.kind,
                    identity_path=entry.identity_path,
                    rel_path=entry.retained_path,
                    sha256=staged_hash,
                    bytes=identity.bytes,
                    source_mtime_ns=identity.mtime_ns,
                )
            )

        # Re-inventory after every copy catches files appearing/disappearing and
        # changes that occur after an individual file's post-copy stat.
        post_bundle = build_bundle(bundle.logs_root)
        if post_bundle.evidence_bundle_hash != bundle.evidence_bundle_hash:
            raise UnstableCapture("evidence set changed during capture")

        files = tuple(sorted(copied, key=lambda item: (item.rel_path, item.kind)))
        staged_hash = _bundle_hash(
            (item.kind, item.identity_path, item.sha256) for item in files
        )
        if staged_hash != bundle.evidence_bundle_hash:
            raise UnstableCapture("staged bytes disagree with the source identity")

        payload = _manifest_payload(
            bundle_hash=staged_hash,
            captured_at=captured_at,
            files=files,
        )
        manifest_sha256 = _write_manifest(stage, payload)
        final = sessions_root / staged_hash
        if final.exists():
            if not final.is_dir():
                raise ArchiveIntegrityError("bundle destination is not a directory")
            if (final / MANIFEST_NAME).exists():
                return _existing_snapshot_result(
                    final,
                    expected_hash=staged_hash,
                    staged_files=files,
                )
            else:
                _adopt_legacy_snapshot(final, payload, files)
            return _existing_snapshot_result(
                final,
                expected_hash=staged_hash,
                staged_files=files,
            )

        try:
            os.rename(stage, final)
            promoted = True
        except FileExistsError:
            # A concurrent capture won the race. It is a duplicate only after
            # full validation, never because the destination merely exists.
            return _existing_snapshot_result(
                final,
                expected_hash=staged_hash,
                staged_files=files,
            )

        try:
            validate_snapshot(final, expected_hash=staged_hash)
        except Exception:
            # This process alone promoted ``final``. A failed post-promotion
            # verification must not expose an accepted-looking partial bundle.
            shutil.rmtree(final)
            promoted = False
            raise
        return SnapshotResult(
            evidence_bundle_hash=staged_hash,
            dest_dir=final,
            files_copied=len(files),
            was_existing=False,
            captured_at=captured_at,
            files=files,
            missing_principal_logs=tuple(
                name
                for name, state in payload["principal_logs"].items()
                if state == "missing"
            ),
            manifest_sha256=manifest_sha256,
        )
    finally:
        if not promoted and stage.exists():
            shutil.rmtree(stage)
