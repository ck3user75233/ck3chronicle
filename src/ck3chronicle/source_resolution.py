"""Active-runtime-only file instance resolution from stored mounted roots."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
import sqlite3

from .db import repository


class SourceResolutionError(RuntimeError):
    """A source path or runtime context cannot be resolved safely."""


def _relative_path(value: str) -> str:
    normalized = value.strip().replace("\\", "/")
    candidate = PurePosixPath(normalized)
    if (
        not normalized
        or not candidate.parts
        or candidate.is_absolute()
        or ":" in candidate.parts[0]
    ):
        raise SourceResolutionError("source path must be relative to a CK3 data root")
    if any(part in {"", ".", ".."} for part in candidate.parts):
        raise SourceResolutionError("source path contains an unsafe traversal segment")
    return candidate.as_posix()


def _base_game_root(dlc_rows: list[sqlite3.Row]) -> str | None:
    for row in dlc_rows:
        mount = str(row["mount_path"]).replace("\\", "/")
        marker = "/game/dlc/"
        index = mount.casefold().find(marker)
        if index >= 0:
            return mount[:index] + "/game"
    return None


def resolve_file_instances(
    conn: sqlite3.Connection,
    session_id: int,
    relative_path: str,
) -> dict[str, object]:
    """Project a session's recorded mount order onto the current filesystem."""
    session = repository.get_session(conn, session_id)
    if session is None:
        raise SourceResolutionError(f"session_id {session_id} not found")
    context = repository.get_runtime_context(conn, session_id)
    if context is None:
        raise SourceResolutionError(
            f"session_id {session_id} runtime context has not been processed"
        )
    normalized = _relative_path(relative_path)
    dlcs = repository.get_mounted_dlcs(conn, session_id)
    mods = repository.get_mounted_mods(conn, session_id)
    roots: list[dict[str, object]] = []
    base_root = _base_game_root(dlcs)
    if base_root is not None:
        roots.append(
            {
                "mount_order": 0,
                "source_kind": "base_game",
                "source_key": "base_game",
                "display_name": "Crusader Kings III",
                "root": base_root,
            }
        )
    order = len(roots)
    for row in dlcs:
        roots.append(
            {
                "mount_order": order,
                "source_kind": "dlc",
                "source_key": row["dlc_key"],
                "display_name": row["display_name"],
                "root": row["mount_path"],
            }
        )
        order += 1
    for row in mods:
        roots.append(
            {
                "mount_order": order,
                "source_kind": row["source_kind"],
                "source_key": row["mod_key"],
                "display_name": row["display_name"],
                "root": row["mount_path"],
            }
        )
        order += 1

    instances: list[dict[str, object]] = []
    missing_roots = 0
    parts = PurePosixPath(normalized).parts
    for root in roots:
        root_path = Path(str(root["root"]))
        if not root_path.is_dir():
            missing_roots += 1
            continue
        candidate = root_path.joinpath(*parts)
        if not candidate.is_file():
            continue
        stat = candidate.stat()
        instances.append(
            {
                "mount_order": root["mount_order"],
                "source_kind": root["source_kind"],
                "source_key": root["source_key"],
                "display_name": root["display_name"],
                "root": str(root_path),
                "path": str(candidate),
                "bytes": int(stat.st_size),
                "mtime_ns": int(stat.st_mtime_ns),
            }
        )
    return {
        "schema": "ck3chronicle.source-resolution",
        "schema_version": 1,
        "session_id": session_id,
        "captured_at": session["created_at"],
        "relative_path": normalized,
        "context_status": context["status"],
        "projection": "current_filesystem_over_session_recorded_mounts",
        "scope": {
            "recorded_roots": len(roots),
            "missing_current_roots": missing_roots,
            "inactive_mod_roots_searched": 0,
        },
        "status": (
            "not_found_in_recorded_roots"
            if not instances
            else "single_instance"
            if len(instances) == 1
            else "multiple_instances"
        ),
        "instances": instances,
        "last_mounted_candidate": instances[-1] if instances else None,
        "caveat": (
            "Last-mounted is a file-level candidate, not proof of CK3 merge or "
            "replace_path semantics; historical contents are not archived."
        ),
    }
