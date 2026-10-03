"""Age-based expiry of raw error/debug logs in completed capture directories."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

from .capture_access import CaptureBusyError, capture_access, capture_time, regular_file


@dataclass(frozen=True)
class RetentionConfig:
    max_age: timedelta = timedelta(days=30)

    def __post_init__(self):
        if not isinstance(self.max_age, timedelta) or self.max_age <= timedelta(0):
            raise ValueError('retention max_age must be positive')


@dataclass(frozen=True)
class FileOutcome:
    path: Path
    reason: str


@dataclass(frozen=True)
class RetentionResult:
    preview: bool
    eligible: tuple[Path, ...]
    removed: tuple[Path, ...]
    skipped: tuple[FileOutcome, ...]
    failures: tuple[FileOutcome, ...]


def retain_raw_logs(captures_root: Path, *, config: RetentionConfig = RetentionConfig(),
                    preview: bool = True, now: datetime | None = None) -> RetentionResult:
    """Scan direct completed children of an explicit pending directory.

    No SQL dependency or ingest-success prerequisite. A preview takes the same
    nonblocking capture locks but never deletes logs. Missing/unusable times are
    skipped, never inferred from filesystem dates. Scheduling belongs to watcher.
    """
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError('now must include a timezone')
    root = Path(captures_root).resolve(strict=True)
    eligible, removed, skipped, failures = [], [], [], []

    def skip_logs(directory, reason):
        for name in ('error.log', 'debug.log'):
            skipped.append(FileOutcome(directory / name, reason))

    for directory in sorted(root.iterdir()):
        if directory.name.startswith('.') or not directory.is_dir():
            continue
        if directory.is_symlink() or directory.resolve().parent != root:
            skip_logs(directory, 'linked capture refused')
            continue
        try:
            with capture_access(directory):
                try:
                    metadata = json.loads(regular_file(directory / 'capture-metadata.json').read_bytes())
                    if not isinstance(metadata, dict):
                        raise ValueError('capture metadata must be an object')
                    captured_at = capture_time(metadata.get('captured_at'))
                except (OSError, ValueError, UnicodeError) as exc:
                    skip_logs(directory, 'unusable capture time: ' + str(exc))
                    continue
                if now - captured_at < config.max_age:
                    skip_logs(directory, 'not expired')
                    continue
                for name in ('error.log', 'debug.log'):
                    path = directory / name
                    if not path.exists() and not path.is_symlink():
                        skipped.append(FileOutcome(path, 'absent'))
                        continue
                    try:
                        regular_file(path)
                        eligible.append(path)
                        if not preview:
                            path.unlink()
                            removed.append(path)
                    except (OSError, ValueError) as exc:
                        failures.append(FileOutcome(path, str(exc)))
        except CaptureBusyError:
            skip_logs(directory, 'capture busy')
        except (OSError, ValueError) as exc:
            failures.append(FileOutcome(directory, str(exc)))
    return RetentionResult(preview, tuple(eligible), tuple(removed), tuple(skipped), tuple(failures))
