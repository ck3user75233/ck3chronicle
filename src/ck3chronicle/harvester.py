"""Harvester: discover and snapshot CK3 evidence bundles."""
from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass, field
from pathlib import Path

_LOG_NAMES = [
    "error.log",
    "game.log",
    "debug.log",
    "database_conflicts.log",
    "setup.log",
    "text.log",
]


@dataclass
class EvidenceBundle:
    logs_root: Path
    log_files: list[Path] = field(default_factory=list)
    crash_folder: Path | None = None
    crash_files: list[Path] = field(default_factory=list)
    evidence_bundle_hash: str = ""


@dataclass
class SnapshotResult:
    evidence_bundle_hash: str
    dest_dir: Path
    files_copied: int
    was_existing: bool


def discover_logs(root: Path) -> list[Path]:
    """Return existing log files from the fixed log name list."""
    return [root / name for name in _LOG_NAMES if (root / name).exists()]


def discover_crash_folder(root: Path) -> Path | None:
    """Return the most recent crash folder.

    Checks <root>/crashes/ subdirectories first (production layout),
    then falls back to a direct <root>/crash/ folder (test fixture layout).
    """
    crashes_dir = root / "crashes"
    if crashes_dir.is_dir():
        candidates = [d for d in crashes_dir.iterdir() if d.is_dir()]
        if candidates:
            return max(candidates, key=lambda d: d.stat().st_mtime)
    crash_dir = root / "crash"
    if crash_dir.is_dir():
        return crash_dir
    return None


def hash_file(path: Path) -> str:
    """Return hex SHA256 of file contents (streaming)."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _compute_bundle_hash(bundle: EvidenceBundle) -> str:
    """Compute the canonical evidence_bundle_hash for an evidence bundle."""
    parts: list[str] = []
    for p in bundle.log_files:
        rel = p.relative_to(bundle.logs_root)
        parts.append(f"log:{rel}:{hash_file(p)}")
    if bundle.crash_folder:
        for p in bundle.crash_files:
            rel = p.relative_to(bundle.crash_folder)
            parts.append(f"crash:{rel}:{hash_file(p)}")
    combined = "\n".join(sorted(parts))
    return hashlib.sha256(combined.encode()).hexdigest()


def build_bundle(logs_root: Path) -> EvidenceBundle:
    """Discover all evidence files and compute the bundle hash."""
    log_files = discover_logs(logs_root)
    crash_folder = discover_crash_folder(logs_root)
    crash_files: list[Path] = []
    if crash_folder:
        crash_files = sorted(f for f in crash_folder.rglob("*") if f.is_file())
    bundle = EvidenceBundle(
        logs_root=logs_root,
        log_files=log_files,
        crash_folder=crash_folder,
        crash_files=crash_files,
    )
    bundle.evidence_bundle_hash = _compute_bundle_hash(bundle)
    return bundle


def snapshot(bundle: EvidenceBundle, dest_root: Path) -> SnapshotResult:
    """Copy evidence bundle files to <dest_root>/sessions/<hash>/.

    Idempotent: if the destination already exists, returns was_existing=True
    and files_copied=0 without re-copying.
    """
    dest_dir = dest_root / "sessions" / bundle.evidence_bundle_hash
    if dest_dir.exists():
        return SnapshotResult(
            evidence_bundle_hash=bundle.evidence_bundle_hash,
            dest_dir=dest_dir,
            files_copied=0,
            was_existing=True,
        )

    dest_dir.mkdir(parents=True, exist_ok=True)
    files_copied = 0

    for src in bundle.log_files:
        dst = dest_dir / src.name
        shutil.copy2(src, dst)
        files_copied += 1

    if bundle.crash_folder and bundle.crash_files:
        crash_dest = dest_dir / "crash"
        for src in bundle.crash_files:
            rel = src.relative_to(bundle.crash_folder)
            dst = crash_dest / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            files_copied += 1

    return SnapshotResult(
        evidence_bundle_hash=bundle.evidence_bundle_hash,
        dest_dir=dest_dir,
        files_copied=files_copied,
        was_existing=False,
    )
