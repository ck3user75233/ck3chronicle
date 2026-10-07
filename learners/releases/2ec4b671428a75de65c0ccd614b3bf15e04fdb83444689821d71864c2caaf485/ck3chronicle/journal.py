"""Local call/checkpoint observations through the sole runtime logging backend.

Counts belong to the caller. No scope, frame or token is transported to workers;
invocation and request metadata remain the backend's existing log_context fields.
"""
from contextvars import ContextVar
import sys
from time import monotonic

from . import runtime_logging

_active_scope = ContextVar('journal_call_scope', default=None)
_FUNCTION_FIELDS = ('module', 'function', 'source_file', 'function_line')


def _identity(frame):
    """Copy scalar identity only; the caller releases its temporary frame."""
    spec = frame.f_globals.get('__spec__')
    module = getattr(spec, 'name', None) or frame.f_globals.get('__name__', '')
    return dict(module=str(module), function=frame.f_code.co_qualname,
                source_file=frame.f_code.co_filename,
                function_line=frame.f_code.co_firstlineno, source_line=frame.f_lineno)


class CallScope:
    """One use of Journal.call(); nesting restores the enclosing local scope."""

    def __init__(self, component):
        self._component = component
        self._identity = None
        self._started = None
        self._last_line = None
        self._last_emission = None
        self._token = None

    def __enter__(self):
        try:
            frame = sys._getframe(1)
            try:
                self._identity = _identity(frame)
            finally:
                del frame
            self._started = monotonic()
            self._token = _active_scope.set(self)
            runtime_logging.event(runtime_logging.get_logger(self._component),
                                  'call_started', **self._identity)
        except Exception:
            # Observation failure must not prevent the application entering.
            pass
        return self

    def __exit__(self, exc_type, exc, traceback):
        try:
            if exc_type is None and self._identity is not None and self._started is not None:
                runtime_logging.event(runtime_logging.get_logger(self._component),
                                      'call_finished', **self._identity,
                                      elapsed_seconds=monotonic() - self._started)
        except Exception:
            pass
        finally:
            try:
                if self._token is not None:
                    _active_scope.reset(self._token)
            except Exception:
                pass
            finally:
                self._token = None
        return False


class Journal:
    def __init__(self, component: str):
        self._component = component

    def call(self) -> CallScope:
        return CallScope(self._component)

    def checkpoint(self, completed: int | None = None,
                   total: int | None = None) -> None:
        try:
            if completed is not None and (type(completed) is not int or completed < 0):
                return
            if total is not None and (type(total) is not int or total < 0
                                      or completed is None or completed > total):
                return
            frame = sys._getframe(1)
            try:
                identity = _identity(frame)
            finally:
                del frame
            fields = identity.copy()
            if completed is not None:
                scope = _active_scope.get()
                if (scope is not None and scope._component == self._component
                        and scope._identity is not None
                        and all(scope._identity[key] == identity[key] for key in _FUNCTION_FIELDS)):
                    now = monotonic()
                    final = completed is not None and total is not None and completed == total
                    if (not final and scope._last_line == identity['source_line']
                            and scope._last_emission is not None
                            and now - scope._last_emission < runtime_logging.CHECKPOINT_INTERVAL_SECONDS):
                        return
                    scope._last_line = identity['source_line']
                    scope._last_emission = now
                fields['completed'] = completed
                if total is not None:
                    fields['total'] = total
            runtime_logging.event(runtime_logging.get_logger(self._component), 'checkpoint', **fields)
        except Exception:
            # Invalid observations or logging failures cannot affect real work.
            pass


def get_journal(component: str) -> Journal:
    return Journal(component)
