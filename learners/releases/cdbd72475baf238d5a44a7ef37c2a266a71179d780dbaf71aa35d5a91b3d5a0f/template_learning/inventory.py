"""Protected native evidence inventory, owned by learner tooling."""
from __future__ import annotations
import dataclasses
import hashlib
from pathlib import Path

@dataclasses.dataclass(frozen=True)
class ProtectedLog:
    evidence_id: str
    kind: str
    path: Path
    sha256: str
    bytes: int
    modified_ns: int


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def protected_error_logs(runtime_root: Path) -> tuple[list[ProtectedLog], list[dict]]:
    """Return distinct protected error logs and duplicate-content evidence."""
    candidates: list[tuple[str, str, Path]] = []
    sessions = runtime_root / "sessions"
    if sessions.is_dir():
        for directory in sorted(sessions.iterdir(), key=lambda item: item.name):
            if not directory.is_dir() or directory.name == ".staging":
                continue
            path = directory / "error.log"
            if path.is_file():
                candidates.append(("session", directory.name, path))
    pending = runtime_root / "pending"
    if pending.is_dir():
        for directory in sorted(pending.iterdir(), key=lambda item: item.name):
            if not directory.is_dir() or directory.name.startswith(".copying-"):
                continue
            path = directory / "error.log"
            if path.is_file():
                candidates.append(("pending", directory.name, path))

    distinct: list[ProtectedLog] = []
    seen: dict[str, ProtectedLog] = {}
    duplicates: list[dict] = []
    for kind, evidence_id, path in candidates:
        stat = path.stat()
        digest = sha256_file(path)
        item = ProtectedLog(
            evidence_id=evidence_id,
            kind=kind,
            path=path,
            sha256=digest,
            bytes=stat.st_size,
            modified_ns=stat.st_mtime_ns,
        )
        prior = seen.get(digest)
        if prior is not None:
            duplicates.append(
                {
                    "sha256": digest,
                    "kept": prior.evidence_id,
                    "skipped": evidence_id,
                }
            )
            continue
        seen[digest] = item
        distinct.append(item)
    distinct.sort(key=lambda item: (item.modified_ns, item.evidence_id))
    return distinct, duplicates


