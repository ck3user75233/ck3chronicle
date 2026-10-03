"""Protect CK3 logs and expose neutral retained-input helpers."""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .playset import PLAYSET_FILENAME, PlaysetMember, PlaysetTemplate

LOG_NAMES = ("error.log",)
MANIFEST_NAME = "manifest.json"
CAPTURE_METADATA_NAME = "capture-metadata.json"


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
class PendingFileStat:
    """Metadata captured from a protected copy without reading its contents."""

    name: str
    bytes: int
    source_mtime_ns: int


@dataclass(frozen=True)
class PendingCapture:
    """A protected pending copy awaiting pipeline processing and registration."""

    dest_dir: Path
    captured_at: str
    files_copied: int
    file_names: tuple[str, ...]
    file_stats: tuple[PendingFileStat, ...]
    debug_capture_failure: dict[str, Any] | None = None


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
    include_debug: bool = False,
    on_logs_copied: Callable[[Path, str, str], None] | None = None,
) -> PendingCapture:
    """Protect logs, optionally completing a paired template before publication.

    Files are copied in priority order into an unpublished ``.copying-*`` directory.
    A complete error copy can be published even if optional debug capture fails.
    Interrupted error copies remain visibly incomplete in staging.
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
    if include_debug:
        log_files.append(root / "debug.log")

    pending_root = Path(dest_root) / "pending"
    pending_root.mkdir(parents=True, exist_ok=True)
    copying = _make_inheriting_staging_directory(pending_root, ".copying-")
    captured_at_dt = datetime.now(timezone.utc)
    copied_names: list[str] = []
    copied_stats: list[PendingFileStat] = []
    debug_failure = None

    for source in log_files:
        target = copying / (".debug.log.incomplete" if source.name == "debug.log" else source.name)
        try:
            if source.is_symlink() or not source.is_file():
                raise InvalidCaptureInput(f"mandatory log is missing or not a regular file: {source}")
            source_stat = _copy_stable_without_hash(source, target)
            if source.name == "debug.log":
                target.rename(copying / "debug.log")
        except Exception as exc:
            if source.name == "debug.log" and isinstance(exc, (OSError, CaptureError)):
                # The protected error log is independently useful. Never expose
                # a partial debug copy under the completed debug.log filename.
                partial = target.name if target.exists() else None
                debug_failure = {
                    "error_type": type(exc).__name__, "error": str(exc),
                    "source_file": str(source), "partial_file": partial,
                }
                continue
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
        if source.name == "error.log":
            seconds, nanoseconds = divmod(source_stat.st_mtime_ns, 1_000_000_000)
            error_log_source_modified_at = (
                datetime.fromtimestamp(seconds, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
                + f".{nanoseconds:09d}+00:00"
            )
        copied_stats.append(
            PendingFileStat(
                name=source.name,
                bytes=source_stat.st_size,
                source_mtime_ns=source_stat.st_mtime_ns,
            )
        )

    metadata = dict(capture_metadata or {})
    if debug_failure is not None:
        metadata["debug_capture_failure"] = debug_failure
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
            "error_log_source_modified_at": error_log_source_modified_at,
            "crash_exception": crash_exception,
        }
    )
    (copying / CAPTURE_METADATA_NAME).write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if "debug.log" in copied_names and on_logs_copied is not None:
        try:
            on_logs_copied(copying, ready_name, captured_at_dt.isoformat())
        except Exception as exc:
            setattr(exc, "capture_stage", "create_playset_template")
            setattr(exc, "capture_context", {"staging_dir": str(copying.resolve())})
            raise
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
        debug_capture_failure=debug_failure,
    )


def write_playset_template(
    directory: Path, *, captured_at: str, members: tuple[PlaysetMember, ...]
) -> PlaysetTemplate:
    """Hash each protected log once and publish its complete UTF-8 template."""
    directory = Path(directory)
    template = PlaysetTemplate(
        error_log_sha256=hash_file(directory / "error.log"),
        debug_log_sha256=hash_file(directory / "debug.log"),
        captured_at=captured_at,
        members=members,
    )
    temporary = directory / f".{PLAYSET_FILENAME}.tmp"
    with temporary.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(template.to_dict(), ensure_ascii=False, indent=2) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(directory / PLAYSET_FILENAME)
    return template


def hash_file(path: Path) -> str:
    """Return the lowercase SHA-256 digest of exact file bytes."""
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def _copy_exact(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with src.open("rb") as source, dst.open("xb") as target:
        shutil.copyfileobj(source, target, length=1024 * 1024)
        target.flush()
        os.fsync(target.fileno())
    shutil.copystat(src, dst, follow_symlinks=False)


def _copy_stable_without_hash(src: Path, dst: Path) -> os.stat_result:
    """Fsync a stable copy and return its validated source stat, not the copy's."""
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
    return after


def read_capture_metadata(directory: Path) -> dict[str, Any] | None:
    """Return session metadata embedded in a current archive manifest."""
    payload, _ = _load_manifest(Path(directory))
    metadata = payload.get("capture_metadata")
    return dict(metadata) if isinstance(metadata, dict) else None


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
