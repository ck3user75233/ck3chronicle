"""Stable agent-facing result envelope for public vertical-slice commands."""

from __future__ import annotations

from typing import Any


SCHEMA = "ck3chronicle.command-result"
SCHEMA_VERSION = 1


def command_envelope(
    command: str,
    *,
    status: str,
    exit_code: int,
    result: dict[str, Any] | None = None,
    error_code: str | None = None,
    message: str | None = None,
    stage: str | None = None,
    retryable: bool = False,
) -> dict[str, Any]:
    """Build one deterministic success, warning, or error response."""
    if status not in {"succeeded", "warning", "failed"}:
        raise ValueError("command status is invalid")
    if exit_code < 0:
        raise ValueError("command exit code is invalid")
    if status == "succeeded":
        if exit_code != 0 or any(
            value is not None for value in (error_code, message, stage)
        ):
            raise ValueError("successful command envelope cannot contain an error")
        error = None
    else:
        if exit_code == 0 or not error_code or not message or not stage:
            raise ValueError("non-success command envelope requires an error")
        error = {
            "code": error_code,
            "message": message,
            "stage": stage,
            "retryable": bool(retryable),
        }
    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "command": command,
        "status": status,
        "exit_code": exit_code,
        "result": result,
        "error": error,
    }
