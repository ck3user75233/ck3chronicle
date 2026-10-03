"""Short-lived OS locks shared by ingest and raw-log retention."""
from contextlib import contextmanager
from datetime import datetime
import os
from pathlib import Path


class CaptureBusyError(RuntimeError):
    """Another ingest/retention call currently owns this capture."""


def regular_file(path: Path) -> Path:
    if path.is_symlink() or not path.is_file() or path.resolve().parent != path.parent.resolve():
        raise ValueError(f'expected a regular, non-linked file: {path}')
    return path


def completed_directory(path: Path) -> Path:
    path = Path(path).absolute()
    if (path.name.startswith('.') or path.is_symlink() or not path.is_dir()
            or path.resolve() != path):
        raise ValueError(f'expected a completed, non-linked capture directory: {path}')
    return path


def capture_time(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError('capture time is unavailable')
    stamp = datetime.fromisoformat(value)
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise ValueError('capture time requires an explicit timezone')
    return stamp


@contextmanager
def capture_access(directory: Path):
    """Nonblocking, cross-process exclusion; OS releases ownership on exit.

    The empty lock file persists; its existence does not signify ownership.
    All cooperating callers lock the same capture directory before reading logs.
    """
    directory = completed_directory(directory)
    path = directory / '.raw-log.lock'
    if path.is_symlink():
        raise ValueError('linked capture lock refused')
    with path.open('a+b') as stream:
        stream.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise CaptureBusyError(f'capture is busy: {directory}') from exc
        try:
            yield directory
        finally:
            if os.name == 'nt':
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)
