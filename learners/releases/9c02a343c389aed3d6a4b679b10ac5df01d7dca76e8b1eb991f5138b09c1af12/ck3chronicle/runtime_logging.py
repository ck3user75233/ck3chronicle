"""The sole owner of runtime JSONL configuration, paths and event conventions.

Call configure_runtime_logging once at process entry, then get_logger/event in
components. Request context is thread-local; queue boundaries copy it explicitly.
Logging is best effort after configuration and never participates in Run success.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import sys

CHECKPOINT_INTERVAL_SECONDS = 5.0

_context = ContextVar('runtime_log_fields', default={})
_root = logging.getLogger('ck3chronicle.runtime')
_root.propagate = False
_root.addHandler(logging.NullHandler())


def runtime_log_path(*, database=None, runtime_root=None, startup_pid=None):
    if database is not None:
        database = Path(database).resolve()
        return database.parent / 'logging' / database.name / 'handler.jsonl'
    name = 'events-watcher.jsonl' if startup_pid is None else f'events-startup-{startup_pid}.jsonl'
    return Path(runtime_root) / 'watch' / name


def invocation_log_path(log_dir, component, invocation_id) -> Path:
    return Path(log_dir) / f'{component}-{invocation_id}.jsonl'


def observer_log_path(runtime_root, *, timestamp, pid) -> Path:
    return Path(runtime_root) / 'watch' / f'log-progress-{timestamp}-{pid}.jsonl'


def bootstrap_log_path(database):
    return runtime_log_path(database=database).with_name('handler-bootstrap.log')


def open_bootstrap_log(database):
    """Latest launch stderr; launcher serializes this with the existing mutex."""
    path = bootstrap_log_path(database)
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.name == 'nt':
        # The venv launcher can outlive the pipe listener briefly. Sharing delete
        # avoids holding disposable storage hostage after graceful shutdown.
        import ctypes
        from ctypes import wintypes
        import msvcrt
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                                      ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        kernel.CreateFileW.restype = wintypes.HANDLE
        handle = kernel.CreateFileW(str(path), 0x40000000, 7, None, 2, 0x80, None)
        if handle == wintypes.HANDLE(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            descriptor = msvcrt.open_osfhandle(handle, os.O_WRONLY)
        except Exception:
            kernel.CloseHandle.argtypes = [wintypes.HANDLE]
            kernel.CloseHandle(handle)
            raise
        return os.fdopen(descriptor, 'w', encoding='utf-8')
    return path.open('w', encoding='utf-8')


def default_logging_settings() -> dict:
    """Fresh settings for explicit destinations, independent of application config."""
    return dict(level='INFO', max_bytes=10 * 1024 * 1024, backup_count=5)


def _validated_settings(values):
    if not isinstance(values, dict):
        raise ValueError('logging configuration must be a table')
    defaults = default_logging_settings()
    level = values.get('level', defaults['level'])
    if level not in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'):
        raise ValueError('logging.level must be DEBUG, INFO, WARNING, ERROR or CRITICAL')
    result = dict(level=level)
    for key in ('max_bytes', 'backup_count'):
        value = values.get(key, defaults[key])
        if type(value) is not int or value <= 0:
            raise ValueError(f'logging.{key} must be a positive integer')
        result[key] = value
    return result


def logging_settings():
    from .config import ConfigurationError, load_config

    values = load_config().get('logging', {})
    try:
        return _validated_settings(values)
    except ValueError as error:
        raise ConfigurationError(str(error)) from error


class _JsonFormatter(logging.Formatter):
    def format(self, record):
        import json
        fields = dict(getattr(record, 'event_fields', {}))
        fields.update(timestamp_utc=datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
                      severity=record.levelname, event=record.getMessage(),
                      component=record.name.removeprefix('ck3chronicle.runtime.'),
                      process_id=record.process, thread_name=record.threadName)
        if record.exc_info:
            fields['traceback'] = self.formatException(record.exc_info)
            fields['exception_class'] = record.exc_info[0].__name__
        return json.dumps(fields, ensure_ascii=False, default=str)


class _RuntimeFileHandler(RotatingFileHandler):
    def handleError(self, record):
        # Match logging.raiseExceptions=False, scoped to our handler rather
        # than altering other libraries. No retry or stderr flood on disk failure.
        pass


def configure_runtime_logging(*, database=None, runtime_root=None, startup_pid=None,
                              settings=None, destination=None):
    if destination is not None and any(value is not None for value in
                                       (database, runtime_root, startup_pid)):
        raise ValueError('destination cannot be combined with database/runtime_root/startup_pid')
    if settings is not None:
        selected_settings = settings
    elif destination is not None:
        selected_settings = default_logging_settings()
    else:
        selected_settings = logging_settings()
    options = _validated_settings(selected_settings)
    path = (Path(destination) if destination is not None else
            runtime_log_path(database=database, runtime_root=runtime_root, startup_pid=startup_pid))
    path.parent.mkdir(parents=True, exist_ok=True)
    handler = _RuntimeFileHandler(path, maxBytes=options['max_bytes'],
                                  backupCount=options['backup_count'], encoding='utf-8')
    handler.setFormatter(_JsonFormatter())
    _root.setLevel(options['level'])
    _root.addHandler(handler)
    return handler


def close_runtime_logging(handler):
    try:
        _root.removeHandler(handler)
    except Exception:
        pass
    try:
        handler.close()
    except Exception:
        pass


def get_logger(component):
    return logging.getLogger('ck3chronicle.runtime.' + component)


def context_fields():
    return dict(_context.get())


@contextmanager
def log_context(**fields):
    token = _context.set({**_context.get(), **fields})
    try:
        yield
    finally:
        _context.reset(token)


def event(logger, event_name, *, level='INFO', exc_info=False, **fields):
    try:
        logger.log(getattr(logging, level), event_name, exc_info=exc_info,
                   extra={'event_fields': {**_context.get(), **fields}})
    except Exception:
        # A logging failure must never replace an application outcome.
        pass


def watcher_event(logger, event_name, fields):
    """Retain the watcher adapter vocabulary and classify optional degradation."""
    optional = event_name in ('debug_capture_failed', 'playset_template_failed')
    warning = optional or 'warning' in event_name or event_name.endswith('_unavailable')
    level = 'WARNING' if warning else 'INFO'
    if not optional and (event_name.endswith('_failed') or fields.get('error')
                         and event_name == 'ingestion_not_completed'):
        level = 'ERROR'
    if event_name == 'retention_completed' and fields.get('problems'):
        level = 'WARNING'
    event(logger, event_name, level=level,
          exc_info=sys.exc_info()[0] is not None and level in ('ERROR', 'WARNING'), **fields)
