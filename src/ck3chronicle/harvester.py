"""Discover, stage, verify, and atomically preserve CK3 evidence bundles."""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

LEGACY_LOG_NAMES = (
    "error.log",
    "debug.log",
    "game.log",
    "database_conflicts.log",
    "setup.log",
    "text.log",
)
LOG_NAMES = ("error.log",)
LEGACY_PRINCIPAL_LOG_NAMES = ("error.log", "debug.log", "game.log")
PRINCIPAL_LOG_NAMES = ("error.log",)
MANIFEST_NAME = "manifest.json"
CAPTURE_METADATA_NAME = "capture-metadata.json"
LEGACY_MANIFEST_VERSION = 1
PREVIOUS_LIVE_MANIFEST_VERSION = 2
MANIFEST_VERSION = 3
SUPPORTED_MANIFEST_VERSIONS = frozenset(
    {LEGACY_MANIFEST_VERSION, PREVIOUS_LIVE_MANIFEST_VERSION, MANIFEST_VERSION}
)
BUNDLE_HASH_ALGORITHM = "ck3chronicle.bundle.v1"
LIVE_SESSION_HASH_ALGORITHM = "ck3chronicle.live-session.v1"


class CaptureError(RuntimeError):
    """Base class for evidence-capture failures."""


class InvalidCaptureInput(CaptureError):
    """The source cannot represent a CK3 session."""


class UnstableCapture(CaptureError):
    """The live evidence changed while it was being captured."""


class ArchiveIntegrityError(CaptureError):
    """A finalized archive does not match its manifest identity."""


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
    manifest_version: int
    source_pending_name: str | None = None


@dataclass(frozen=True)
class PendingFileStat:
    """Metadata captured from a protected copy without reading its contents."""

    name: str
    bytes: int
    source_mtime_ns: int


@dataclass(frozen=True)
class PendingCapture:
    """A complete unpublished copy awaiting hashes, manifest, and registration."""

    dest_dir: Path
    captured_at: str
    files_copied: int
    file_names: tuple[str, ...]
    file_stats: tuple[PendingFileStat, ...]


@dataclass(frozen=True)
class PendingInspection:
    """Read-only identity and manifest projection for one protected capture."""

    source_pending_name: str
    source_dir: Path
    captured_at: str
    files: tuple[CapturedFile, ...]
    missing_principal_logs: tuple[str, ...]
    evidence_bundle_hash: str
    manifest_sha256: str
    manifest_version: int
    manifest_present: bool
    metadata_present: bool


def _make_inheriting_staging_directory(parent: Path, prefix: str) -> Path:
    """Create a collision-resistant staging directory with its parent's ACL.

    ``tempfile.mkdtemp`` deliberately applies an owner-only security descriptor
    on Windows. Renaming such a directory preserves that descriptor, which can
    make a published capture unreadable to a later ck3chronicle process. The
    runtime parent is the access-control authority, so staging children must
    inherit it.
    """
    for _attempt in range(100):
        candidate = parent / f"{prefix}{secrets.token_urlsafe(6)}"
        try:
            candidate.mkdir(mode=0o770)
        except FileExistsError:
            continue
        return candidate
    raise FileExistsError(f"could not allocate staging directory below {parent}")


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


def spool_logs(
    logs_root: Path,
    dest_root: Path,
    *,
    abort_if: Callable[[], bool] | None = None,
    capture_metadata: dict[str, Any] | None = None,
    crash_folder: Path | None = None,
) -> PendingCapture:
    """Immediately protect a completed CK3 session without hashing or SQLite.

    Files are copied in priority order into an unpublished ``.copying-*`` directory.
    Only a complete copy set is renamed into the durable pending queue.  An
    interrupted directory remains visibly incomplete and is never treated as a
    finalized archive.
    """
    root = Path(logs_root)
    if not root.is_dir():
        raise InvalidCaptureInput(f"logs directory does not exist: {root}")
    if abort_if is not None and abort_if():
        raise UnstableCapture("CK3 is running; refusing to copy live logs")

    log_files = discover_logs(root)
    if not any(path.name.casefold() == "error.log" for path in log_files):
        raise InvalidCaptureInput("mandatory error.log is missing")
    if (root / "error.log").stat().st_size == 0:
        raise InvalidCaptureInput("mandatory error.log is empty")

    pending_root = Path(dest_root) / "pending"
    pending_root.mkdir(parents=True, exist_ok=True)
    copying = _make_inheriting_staging_directory(pending_root, ".copying-")
    captured_at_dt = datetime.now(timezone.utc)
    copied_names: list[str] = []
    copied_stats: list[PendingFileStat] = []

    for source in log_files:
        target = copying / source.name
        try:
            target_stat = _copy_stable_without_hash(source, target)
        except Exception as exc:
            setattr(
                exc,
                "capture_context",
                {
                    "logs_root": str(root.resolve()),
                    "pending_root": str(pending_root.resolve()),
                    "staging_dir": str(copying.resolve()),
                    "source_file": str(source.resolve()),
                    "staging_file": str(target.resolve()),
                },
            )
            setattr(exc, "capture_stage", "copy_live_log_file")
            raise
        copied_names.append(source.name)
        copied_stats.append(
            PendingFileStat(
                name=source.name,
                bytes=target_stat.st_size,
                source_mtime_ns=target_stat.st_mtime_ns,
            )
        )

    metadata = dict(capture_metadata or {})
    crash_exception = {
        "status": "not_applicable",
        "source_rel_path": None,
        "retained_path": None,
    }
    if crash_folder is not None:
        exception_source = Path(crash_folder) / "exception.txt"
        crash_exception["status"] = "absent"
        crash_exception["source_rel_path"] = "exception.txt"
        if exception_source.exists():
            exception_target = copying / "crash" / "exception.txt"
            try:
                if exception_source.is_symlink() or not exception_source.is_file():
                    raise InvalidCaptureInput(
                        "associated crash exception is not a regular file"
                    )
                _copy_exact(exception_source, exception_target)
            except Exception as exc:
                # The crash attachment is secondary evidence. Its failure must
                # not discard the already protected mandatory error.log.
                exception_target.unlink(missing_ok=True)
                try:
                    exception_target.parent.rmdir()
                except OSError:
                    pass
                crash_exception.update(
                    status="unavailable",
                    retained_path=None,
                    error_type=type(exc).__name__,
                    error=str(exc),
                )
            else:
                exception_stat = exception_target.stat()
                copied_names.append("crash/exception.txt")
                copied_stats.append(
                    PendingFileStat(
                        name="crash/exception.txt",
                        bytes=exception_stat.st_size,
                        source_mtime_ns=exception_stat.st_mtime_ns,
                    )
                )
                crash_exception.update(
                    status="captured",
                    retained_path="crash/exception.txt",
                )

    if abort_if is not None and abort_if():
        exc = UnstableCapture(
            f"CK3 restarted while copying logs; incomplete copy retained at {copying}"
        )
        setattr(
            exc,
            "capture_context",
            {
                "logs_root": str(root.resolve()),
                "pending_root": str(pending_root.resolve()),
                "staging_dir": str(copying.resolve()),
            },
        )
        setattr(exc, "capture_stage", "validate_completed_copy")
        raise exc

    ready_name = (
        captured_at_dt.strftime("%Y%m%dT%H%M%S.%fZ")
        + "-"
        + copying.name.removeprefix(".copying-")
    )
    metadata.update(
        {
            "schema_version": 1,
            "capture_id": ready_name,
            "captured_at": captured_at_dt.isoformat(),
            "crash_exception": crash_exception,
        }
    )
    (copying / CAPTURE_METADATA_NAME).write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    ready = pending_root / ready_name
    try:
        os.rename(copying, ready)
    except Exception as exc:
        setattr(
            exc,
            "capture_context",
            {
                "logs_root": str(root.resolve()),
                "pending_root": str(pending_root.resolve()),
                "staging_dir": str(copying.resolve()),
                "intended_pending_dir": str(ready.resolve()),
            },
        )
        setattr(exc, "capture_stage", "publish_pending_copy")
        raise
    return PendingCapture(
        dest_dir=ready,
        captured_at=captured_at_dt.isoformat(),
        files_copied=len(copied_names),
        file_names=tuple(copied_names),
        file_stats=tuple(copied_stats),
    )


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


def _live_session_hash(
    capture_id: str, records: Iterable[tuple[str, str, str]]
) -> str:
    """Return a stable identity for one live capture, not a content dedup key."""
    content_hash = _bundle_hash(records)
    identity = f"{LIVE_SESSION_HASH_ALGORITHM}\n{capture_id}\n{content_hash}"
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


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
    if (logs_root / "error.log").stat().st_size == 0:
        raise InvalidCaptureInput("mandatory error.log is empty")

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


def _copy_stable_without_hash(src: Path, dst: Path) -> os.stat_result:
    """Fsync one copy and reject a source that changed across the copy."""
    before = src.stat()
    _copy_exact(src, dst)
    after = src.stat()
    copied = dst.stat()
    if (
        (before.st_size, before.st_mtime_ns)
        != (after.st_size, after.st_mtime_ns)
        or copied.st_size != after.st_size
    ):
        raise UnstableCapture(f"source changed while copying: {src.name}")
    return copied


def _manifest_payload(
    *,
    bundle_hash: str,
    captured_at: str,
    files: tuple[CapturedFile, ...],
    capture_id: str | None = None,
    capture_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    present_logs = {item.identity_path for item in files if item.kind == "log"}
    missing = [name for name in PRINCIPAL_LOG_NAMES if name not in present_logs]
    content_hash = _bundle_hash(
        (item.kind, item.identity_path, item.sha256) for item in files
    )
    payload = {
        "manifest_version": (
            MANIFEST_VERSION if capture_id is not None else LEGACY_MANIFEST_VERSION
        ),
        "hash_algorithm": (
            LIVE_SESSION_HASH_ALGORITHM
            if capture_id is not None
            else BUNDLE_HASH_ALGORITHM
        ),
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
    if capture_id is not None:
        payload["capture_id"] = capture_id
        error_file = next(
            item
            for item in files
            if item.kind == "log" and item.identity_path == "error.log"
        )
        payload["error_log_sha256"] = error_file.sha256
    else:
        payload["content_bundle_hash"] = content_hash
    if capture_metadata is not None:
        payload["capture_metadata"] = capture_metadata
    return payload


def _principal_names(payload: dict[str, Any]) -> tuple[str, ...]:
    if payload.get("manifest_version") == MANIFEST_VERSION:
        return PRINCIPAL_LOG_NAMES
    return LEGACY_PRINCIPAL_LOG_NAMES


def read_capture_metadata(directory: Path) -> dict[str, Any] | None:
    """Return session metadata embedded in a current archive manifest."""
    payload, _ = _load_manifest(Path(directory))
    metadata = payload.get("capture_metadata")
    return dict(metadata) if isinstance(metadata, dict) else None


def _write_manifest(directory: Path, payload: dict[str, Any]) -> str:
    encoded = _manifest_bytes(payload)
    path = directory / MANIFEST_NAME
    with path.open("xb") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    return hashlib.sha256(encoded).hexdigest()


def _manifest_bytes(payload: dict[str, Any]) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


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
    version = payload.get("manifest_version")
    if version not in SUPPORTED_MANIFEST_VERSIONS:
        raise ArchiveIntegrityError("unsupported capture manifest version")
    expected_algorithm = (
        LIVE_SESSION_HASH_ALGORITHM
        if version in {PREVIOUS_LIVE_MANIFEST_VERSION, MANIFEST_VERSION}
        else BUNDLE_HASH_ALGORITHM
    )
    if payload.get("hash_algorithm") != expected_algorithm:
        raise ArchiveIntegrityError("unsupported bundle hash algorithm")
    if version in {PREVIOUS_LIVE_MANIFEST_VERSION, MANIFEST_VERSION}:
        capture_id = payload.get("capture_id")
        if (
            not isinstance(capture_id, str)
            or not capture_id
            or capture_id in {".", ".."}
            or Path(capture_id).name != capture_id
        ):
            raise ArchiveIntegrityError("capture manifest has an invalid capture id")
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


def _manifest_identity(
    payload: dict[str, Any], records: Iterable[tuple[str, str, str]]
) -> tuple[str, str]:
    """Return the archive identity and exact retained-content hash."""
    frozen_records = tuple(records)
    content_hash = _bundle_hash(frozen_records)
    if payload.get("manifest_version") in {
        PREVIOUS_LIVE_MANIFEST_VERSION,
        MANIFEST_VERSION,
    }:
        identity_hash = _live_session_hash(str(payload["capture_id"]), frozen_records)
    else:
        identity_hash = content_hash
    return identity_hash, content_hash


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
    derived_identity, content_hash = _manifest_identity(payload, actual_records)
    if derived_identity != bundle_hash:
        raise ArchiveIntegrityError("manifest files do not derive the bundle identity")
    if payload.get("manifest_version") == MANIFEST_VERSION:
        error_hashes = [
            item.sha256
            for item in files
            if item.kind == "log" and item.identity_path == "error.log"
        ]
        if error_hashes != [payload.get("error_log_sha256")]:
            raise ArchiveIntegrityError("manifest error.log hash disagrees")
    elif payload.get("content_bundle_hash", content_hash) != content_hash:
        raise ArchiveIntegrityError("manifest content hash disagrees with its files")
    present_logs = {item.identity_path for item in files if item.kind == "log"}
    expected_principal = {
        name: "present" if name in present_logs else "missing"
        for name in _principal_names(payload)
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


def snapshot_file_metadata_matches_manifest(
    directory: Path, *, files: tuple[CapturedFile, ...] | None = None
) -> bool:
    """Return whether retained file metadata still matches a known manifest.

    This is the inexpensive steady-state guard used before accepting a
    previously verified archive from the registry.  It reads the small
    manifest and stats the retained files, but does not re-read evidence bytes.
    Any metadata drift sends the caller through full SHA-256 verification.
    """
    directory = Path(directory)
    if files is None:
        payload, _manifest_sha256 = _load_manifest(directory)
        files = _files_from_manifest(payload)
    expected_paths = {item.rel_path for item in files}
    if len(expected_paths) != len(files):
        return False
    for item in files:
        retained = directory / Path(item.rel_path)
        if retained.is_symlink() or not retained.is_file():
            return False
        stat = retained.stat()
        if (
            stat.st_size != item.bytes
            or stat.st_mtime_ns != item.source_mtime_ns
        ):
            return False
    actual_paths = {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if path.is_file()
        and path.relative_to(directory).as_posix() != MANIFEST_NAME
    }
    return actual_paths == expected_paths


def snapshot_manifest_projection(
    directory: Path,
) -> tuple[tuple[CapturedFile, ...], str, str, int]:
    """Read the immutable manifest projection without hashing evidence files.

    The archive registry uses this only after the manifest itself and retained
    file metadata agree with a previously verified archive.  It supplies the
    exact manifest rows needed to validate the rebuildable SQLite projection.
    """
    directory = Path(directory)
    payload, manifest_sha256 = _load_manifest(directory)
    bundle_hash = payload.get("evidence_bundle_hash")
    if not isinstance(bundle_hash, str) or len(bundle_hash) != 64:
        raise ArchiveIntegrityError("capture manifest has an invalid bundle hash")
    if directory.name != bundle_hash:
        raise ArchiveIntegrityError("archive directory name disagrees with manifest")
    if payload.get("capture_status") != "finalized":
        raise ArchiveIntegrityError("capture manifest is not finalized")
    files = _files_from_manifest(payload)
    if len({item.rel_path for item in files}) != len(files):
        raise ArchiveIntegrityError("capture manifest repeats a retained path")
    records = [(item.kind, item.identity_path, item.sha256) for item in files]
    derived_identity, content_hash = _manifest_identity(payload, records)
    if derived_identity != bundle_hash:
        raise ArchiveIntegrityError("manifest files do not derive the bundle identity")
    if payload.get("manifest_version") == MANIFEST_VERSION:
        error_hashes = [
            item.sha256
            for item in files
            if item.kind == "log" and item.identity_path == "error.log"
        ]
        if error_hashes != [payload.get("error_log_sha256")]:
            raise ArchiveIntegrityError("manifest error.log hash disagrees")
    elif payload.get("content_bundle_hash", content_hash) != content_hash:
        raise ArchiveIntegrityError("manifest content hash disagrees with its files")
    present_logs = {item.identity_path for item in files if item.kind == "log"}
    expected_principal = {
        name: "present" if name in present_logs else "missing"
        for name in _principal_names(payload)
    }
    if payload.get("principal_logs") != expected_principal:
        raise ArchiveIntegrityError("principal-log status disagrees with manifest files")
    completeness = payload.get("evidence_completeness")
    expected_completeness = (
        "complete"
        if all(state == "present" for state in expected_principal.values())
        else "partial"
    )
    if completeness != expected_completeness:
        raise ArchiveIntegrityError("evidence completeness is inconsistent")
    return files, manifest_sha256, completeness, int(payload["manifest_version"])


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
            for name in _principal_names(payload)
            if principal.get(name) == "missing"
        ),
        manifest_sha256=manifest_sha256,
        manifest_version=int(payload["manifest_version"]),
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
            for name in _principal_names(payload)
            if principal[name] == "missing"
        ),
        manifest_sha256=manifest_sha256,
        manifest_version=int(payload["manifest_version"]),
    )


def _pending_captured_at(directory: Path) -> str:
    try:
        timestamp = directory.name.split("-", 1)[0]
        parsed = datetime.strptime(timestamp, "%Y%m%dT%H%M%S.%fZ")
    except (ValueError, IndexError) as exc:
        raise ArchiveIntegrityError(
            f"pending capture has an invalid directory name: {directory.name}"
        ) from exc
    return parsed.replace(tzinfo=timezone.utc).isoformat()


def selected_pending_path(dest_root: Path, pending_name: str) -> Path:
    """Resolve one exact direct child of ``pending`` without path traversal."""
    if (
        not pending_name
        or pending_name.startswith(".")
        or Path(pending_name).name != pending_name
        or "/" in pending_name
        or "\\" in pending_name
    ):
        raise ArchiveIntegrityError(
            "pending capture selection must be one non-hidden directory name"
        )
    directory = Path(dest_root).resolve() / "pending" / pending_name
    if directory.is_symlink() or not directory.is_dir():
        raise ArchiveIntegrityError(
            f"selected pending capture does not exist: {pending_name}"
        )
    return directory


def _inspect_pending(
    pending: PendingCapture | Path,
) -> tuple[PendingInspection, dict[str, Any]]:
    directory = pending.dest_dir if isinstance(pending, PendingCapture) else Path(pending)
    captured_at = (
        pending.captured_at
        if isinstance(pending, PendingCapture)
        else _pending_captured_at(directory)
    )
    if directory.is_symlink() or not directory.is_dir() or directory.name.startswith("."):
        raise ArchiveIntegrityError(f"pending capture is not complete: {directory}")

    metadata_path = directory / CAPTURE_METADATA_NAME
    if metadata_path.is_file():
        try:
            capture_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ArchiveIntegrityError("pending capture metadata is invalid") from exc
        if not isinstance(capture_metadata, dict):
            raise ArchiveIntegrityError("pending capture metadata is not an object")
    else:
        capture_metadata = {
            "schema_version": 1,
            "capture_id": directory.name,
            "captured_at": captured_at,
            "trigger": "legacy_pending",
            "termination_kind": "unknown",
            "crash_exception": {"status": "unavailable"},
        }
    actual_names = {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if path.is_file() and path.name not in {MANIFEST_NAME, CAPTURE_METADATA_NAME}
    }
    allowed_names = set(LEGACY_LOG_NAMES) | {"crash/exception.txt"}
    unexpected = actual_names - allowed_names
    if unexpected:
        raise ArchiveIntegrityError(
            "pending capture contains unsupported files: "
            + ", ".join(sorted(unexpected))
        )
    if "error.log" not in actual_names:
        raise ArchiveIntegrityError("pending capture is missing mandatory error.log")

    files: list[CapturedFile] = []
    for name in LEGACY_LOG_NAMES:
        path = directory / name
        if not path.exists():
            continue
        if path.is_symlink() or not path.is_file():
            raise ArchiveIntegrityError(f"pending evidence is not regular: {name}")
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
    exception_path = directory / "crash" / "exception.txt"
    if exception_path.exists():
        if exception_path.is_symlink() or not exception_path.is_file():
            raise ArchiveIntegrityError(
                "pending evidence is not regular: crash/exception.txt"
            )
        stat = exception_path.stat()
        files.append(
            CapturedFile(
                kind="crash",
                identity_path="exception.txt",
                rel_path="crash/exception.txt",
                sha256=hash_file(exception_path),
                bytes=stat.st_size,
                source_mtime_ns=stat.st_mtime_ns,
            )
        )

    captured_files = tuple(files)
    records = tuple(
        (item.kind, item.identity_path, item.sha256) for item in captured_files
    )
    bundle_hash = _live_session_hash(directory.name, records)
    payload = _manifest_payload(
        bundle_hash=bundle_hash,
        captured_at=captured_at,
        files=captured_files,
        capture_id=directory.name,
        capture_metadata=capture_metadata,
    )
    manifest_path = directory / MANIFEST_NAME
    if manifest_path.exists():
        existing_payload, manifest_sha256 = _load_manifest(directory)
        if existing_payload != payload:
            raise ArchiveIntegrityError(
                "pending manifest disagrees with the protected copies"
            )
    else:
        manifest_sha256 = hashlib.sha256(_manifest_bytes(payload)).hexdigest()
    present_logs = {item.identity_path for item in captured_files}
    return (
        PendingInspection(
            source_pending_name=directory.name,
            source_dir=directory,
            captured_at=captured_at,
            files=captured_files,
            missing_principal_logs=tuple(
                name for name in PRINCIPAL_LOG_NAMES if name not in present_logs
            ),
            evidence_bundle_hash=bundle_hash,
            manifest_sha256=manifest_sha256,
            manifest_version=MANIFEST_VERSION,
            manifest_present=manifest_path.exists(),
            metadata_present=metadata_path.is_file(),
        ),
        payload,
    )


def inspect_pending(pending: PendingCapture | Path) -> PendingInspection:
    """Hash and validate one protected capture without changing it."""
    inspection, _payload = _inspect_pending(pending)
    return inspection


def finalize_pending(
    pending: PendingCapture | Path,
    dest_root: Path,
    *,
    expected_evidence_bundle_hash: str | None = None,
    expected_manifest_sha256: str | None = None,
) -> SnapshotResult:
    """Hash a protected copy and promote it without reading live CK3 logs."""
    inspection, payload = _inspect_pending(pending)
    if (
        expected_evidence_bundle_hash is not None
        and inspection.evidence_bundle_hash != expected_evidence_bundle_hash
    ):
        raise ArchiveIntegrityError(
            "pending capture changed after its read-only plan: bundle hash disagrees"
        )
    if (
        expected_manifest_sha256 is not None
        and inspection.manifest_sha256 != expected_manifest_sha256
    ):
        raise ArchiveIntegrityError(
            "pending capture changed after its read-only plan: manifest hash disagrees"
        )
    directory = inspection.source_dir
    captured_at = inspection.captured_at
    captured_files = inspection.files
    bundle_hash = inspection.evidence_bundle_hash
    metadata_path = directory / CAPTURE_METADATA_NAME
    manifest_path = directory / MANIFEST_NAME
    if manifest_path.exists():
        manifest_sha256 = inspection.manifest_sha256
    else:
        manifest_sha256 = _write_manifest(directory, payload)

    sessions_root = Path(dest_root) / "sessions"
    sessions_root.mkdir(parents=True, exist_ok=True)
    final = sessions_root / bundle_hash
    if final.exists():
        if not final.is_dir():
            raise ArchiveIntegrityError("bundle destination is not a directory")
        existing_payload, existing_manifest_sha256 = _load_manifest(final)
        existing_files = _files_from_manifest(existing_payload)
        if (
            existing_payload.get("evidence_bundle_hash") != bundle_hash
            or _evidence_descriptor(existing_files)
            != _evidence_descriptor(captured_files)
        ):
            raise ArchiveIntegrityError(
                "existing archive manifest disagrees with the pending capture"
            )
        shutil.rmtree(directory)
        principal = existing_payload["principal_logs"]
        return SnapshotResult(
            evidence_bundle_hash=bundle_hash,
            dest_dir=final,
            files_copied=len(captured_files),
            was_existing=True,
            captured_at=existing_payload["captured_at"],
            files=existing_files,
            missing_principal_logs=tuple(
                name
                for name in _principal_names(existing_payload)
                if principal[name] == "missing"
            ),
            manifest_sha256=existing_manifest_sha256,
            manifest_version=int(existing_payload["manifest_version"]),
            source_pending_name=directory.name,
        )

    if metadata_path.exists():
        metadata_path.unlink()
    os.rename(directory, final)
    return SnapshotResult(
        evidence_bundle_hash=bundle_hash,
        dest_dir=final,
        files_copied=len(captured_files),
        was_existing=False,
        captured_at=captured_at,
        files=captured_files,
        missing_principal_logs=inspection.missing_principal_logs,
        manifest_sha256=manifest_sha256,
        manifest_version=MANIFEST_VERSION,
        source_pending_name=directory.name,
    )


def finalize_pending_captures(
    dest_root: Path,
    *,
    errors: list[str] | None = None,
) -> tuple[SnapshotResult, ...]:
    """Finalize complete pending copies, optionally isolating per-capture faults."""
    pending_root = Path(dest_root) / "pending"
    if not pending_root.is_dir():
        return ()
    results: list[SnapshotResult] = []
    for directory in sorted(pending_root.iterdir()):
        if directory.is_dir() and not directory.name.startswith("."):
            try:
                results.append(finalize_pending(directory, dest_root))
            except (ArchiveIntegrityError, OSError) as exc:
                if errors is None:
                    raise
                errors.append(f"{directory.name}: {exc}")
    return tuple(results)


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
    """Add a manifest to a verified legacy archive without recopying it."""
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
    """Content-check and promote one legacy/manual archive import."""
    if not any(path.name.casefold() == "error.log" for path in bundle.log_files):
        raise InvalidCaptureInput("mandatory error.log is missing")

    sessions_root = Path(dest_root) / "sessions"
    staging_root = sessions_root / ".staging"
    staging_root.mkdir(parents=True, exist_ok=True)
    stage = _make_inheriting_staging_directory(staging_root, "capture-")
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
            # A concurrent capture won the race. Accept the existing archive
            # only after its complete identity has been validated.
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
            manifest_version=LEGACY_MANIFEST_VERSION,
        )
    finally:
        if not promoted and stage.exists():
            shutil.rmtree(stage)
