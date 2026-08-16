"""Active-runtime source observations and evidence-bearing file resolution."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from pathlib import Path, PurePosixPath
import re
import sqlite3

from .db import repository


RESOLUTION_CONTRACT_VERSION = "active-runtime-source-observation-v1"


class SourceResolutionError(RuntimeError):
    """A source path or runtime context cannot be resolved safely."""


_FILE_LOCATION = re.compile(
    r"\bfile:\s*(?P<path>.+?)\s+(?:near\s+)?line:\s*\d+",
    re.IGNORECASE,
)


def extract_file_from_location(value: str | None) -> str | None:
    """Extract one CK3-relative file locator without treating it as semantics."""
    if not value:
        return None
    match = _FILE_LOCATION.search(value.replace("\\", "/"))
    if match is None:
        return None
    path = match.group("path").strip().strip("'\"")
    if (
        not path
        or ("/" not in path and "." not in path)
        or path.startswith(("/", "../"))
        or ":/" in path
    ):
        return None
    try:
        return _relative_path(path)
    except SourceResolutionError:
        return None


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


def _domain_policy(relative_path: str) -> str:
    folded = relative_path.casefold()
    if folded.startswith("common/on_action/"):
        return "container_merge_after_file_replacement"
    if folded.startswith("common/culture/cultures/"):
        return "symbol_lios_after_file_replacement"
    return "unclassified_directory_semantics"


def _base_game_root(dlc_rows: list[sqlite3.Row]) -> str | None:
    for row in dlc_rows:
        mount = str(row["mount_path"]).replace("\\", "/")
        marker = "/game/dlc/"
        index = mount.casefold().find(marker)
        if index >= 0:
            return mount[:index] + "/game"
    return None


def _recorded_roots(
    conn: sqlite3.Connection, session_id: int
) -> tuple[sqlite3.Row, sqlite3.Row, list[dict[str, object]]]:
    session = repository.get_session(conn, session_id)
    if session is None:
        raise SourceResolutionError(f"session_id {session_id} not found")
    context = repository.get_runtime_context(conn, session_id)
    if context is None:
        raise SourceResolutionError(
            f"session_id {session_id} runtime context has not been processed"
        )
    if context["status"] != "complete":
        raise SourceResolutionError(
            f"session_id {session_id} runtime context is {context['status']}; "
            "active-root resolution requires a complete Mounted Data block"
        )
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
                "display_name": None,
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
                "display_name": None,
                "root": row["mount_path"],
            }
        )
        order += 1
    return session, context, roots


def _stable_sha256(path: Path) -> tuple[str, int, int]:
    """Hash a source instance once and reject a concurrent source update."""
    before = path.stat()
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise SourceResolutionError(f"source file changed while observed: {path}")
    return digest.hexdigest(), int(after.st_size), int(after.st_mtime_ns)


def _live_projection(
    conn: sqlite3.Connection,
    session_id: int,
    relative_path: str,
    *,
    hash_instances: bool,
) -> dict[str, object]:
    session, context, roots = _recorded_roots(conn, session_id)
    normalized = _relative_path(relative_path)
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
        if hash_instances:
            sha256, bytes_, mtime_ns = _stable_sha256(candidate)
        else:
            stat = candidate.stat()
            sha256 = None
            bytes_ = int(stat.st_size)
            mtime_ns = int(stat.st_mtime_ns)
        item: dict[str, object] = {
            "instance_ordinal": len(instances),
            "mount_order": root["mount_order"],
            "source_kind": root["source_kind"],
            "source_key": root["source_key"],
            "display_name": root["display_name"],
            "root": str(root_path),
            "path": str(candidate),
            "bytes": bytes_,
            "mtime_ns": mtime_ns,
        }
        if sha256 is not None:
            item["sha256"] = sha256
        instances.append(item)
    status = (
        "not_found_in_recorded_roots"
        if not instances
        else "single_instance"
        if len(instances) == 1
        else "multiple_instances"
    )
    return _result(
        session_id=session_id,
        captured_at=str(session["created_at"]),
        relative_path=normalized,
        context_status=str(context["status"]),
        projection="current_filesystem_over_session_recorded_mounts",
        observed_at=None,
        recorded_roots=len(roots),
        missing_roots=missing_roots,
        status=status,
        instances=instances,
    )


def _result(
    *,
    session_id: int,
    captured_at: str,
    relative_path: str,
    context_status: str,
    projection: str,
    observed_at: str | None,
    recorded_roots: int,
    missing_roots: int,
    status: str,
    instances: list[dict[str, object]],
) -> dict[str, object]:
    winner = instances[-1] if instances else None
    domain_policy = _domain_policy(relative_path)
    stored = observed_at is not None
    return {
        "schema": "ck3chronicle.source-resolution",
        "schema_version": 2,
        "session_id": session_id,
        "captured_at": captured_at,
        "relative_path": relative_path,
        "context_status": context_status,
        "projection": projection,
        "observation": {
            "stored": stored,
            "observed_at": observed_at,
            "contract_version": (
                RESOLUTION_CONTRACT_VERSION if stored else None
            ),
        },
        "scope": {
            "recorded_roots": recorded_roots,
            "missing_current_roots": missing_roots,
            "inactive_mod_roots_searched": 0,
        },
        "status": status,
        "instances": instances,
        "file_layer": {
            "rule": "exact_relative_path_last_mounted_wins",
            "winner": winner,
        },
        "domain_layer": {
            "policy": domain_policy,
            "status": "not_evaluated",
        },
        # Compatibility field for the first report/triage projection.
        "last_mounted_candidate": winner,
        "caveat": (
            "The exact-relative-path file winner is resolved. Definitions in "
            "other filenames require the named domain policy; that semantic "
            "merge has not yet been evaluated."
        ),
    }


def _stored_projection(
    conn: sqlite3.Connection, session_id: int, relative_path: str
) -> dict[str, object] | None:
    normalized = _relative_path(relative_path)
    observation = conn.execute(
        """
        SELECT o.*, s.created_at
        FROM source_resolution_observations o
        JOIN sessions s ON s.session_id = o.session_id
        WHERE o.session_id = ? AND o.relative_path = ?
        """,
        (session_id, normalized),
    ).fetchone()
    if observation is None:
        return None
    rows = conn.execute(
        """
        SELECT * FROM source_file_instances
        WHERE session_id = ? AND relative_path = ?
        ORDER BY instance_ordinal
        """,
        (session_id, normalized),
    ).fetchall()
    instances = [
        {
            "instance_ordinal": int(row["instance_ordinal"]),
            "mount_order": int(row["mount_order"]),
            "source_kind": row["source_kind"],
            "source_key": row["source_key"],
            "display_name": row["display_name"],
            "root": row["root_path"],
            "path": row["absolute_path"],
            "bytes": int(row["bytes"]),
            "mtime_ns": int(row["mtime_ns"]),
            "sha256": row["sha256"],
        }
        for row in rows
    ]
    return _result(
        session_id=session_id,
        captured_at=str(observation["created_at"]),
        relative_path=normalized,
        context_status=str(observation["context_status"]),
        projection="persisted_processing_observation",
        observed_at=str(observation["observed_at"]),
        recorded_roots=int(observation["recorded_root_count"]),
        missing_roots=int(observation["missing_root_count"]),
        status=str(observation["status"]),
        instances=instances,
    )


def resolve_file_instances(
    conn: sqlite3.Connection,
    session_id: int,
    relative_path: str,
) -> dict[str, object]:
    """Return immutable stored evidence when present, otherwise a live projection."""
    stored = _stored_projection(conn, session_id, relative_path)
    if stored is not None:
        return stored
    return _live_projection(
        conn, session_id, relative_path, hash_instances=False
    )


def observe_file_instances(
    conn: sqlite3.Connection,
    session_id: int,
    relative_path: str,
) -> tuple[dict[str, object], bool]:
    """Persist the first active-root projection for this session and path."""
    stored = _stored_projection(conn, session_id, relative_path)
    if stored is not None:
        return stored, False
    live = _live_projection(conn, session_id, relative_path, hash_instances=True)
    observed_at = datetime.now(timezone.utc).isoformat()
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute(
            """
            INSERT INTO source_resolution_observations (
                session_id, relative_path, resolution_contract_version,
                observed_at, context_status, status, domain_policy,
                recorded_root_count, missing_root_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                live["relative_path"],
                RESOLUTION_CONTRACT_VERSION,
                observed_at,
                live["context_status"],
                live["status"],
                live["domain_layer"]["policy"],
                live["scope"]["recorded_roots"],
                live["scope"]["missing_current_roots"],
            ),
        )
        conn.executemany(
            """
            INSERT INTO source_file_instances (
                session_id, relative_path, instance_ordinal, mount_order,
                source_kind, source_key, display_name, root_path,
                absolute_path, bytes, mtime_ns, sha256
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    session_id,
                    live["relative_path"],
                    item["instance_ordinal"],
                    item["mount_order"],
                    item["source_kind"],
                    item["source_key"],
                    item["display_name"],
                    item["root"],
                    item["path"],
                    item["bytes"],
                    item["mtime_ns"],
                    item["sha256"],
                )
                for item in live["instances"]
            ],
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raced = _stored_projection(conn, session_id, relative_path)
        if raced is None:
            raise
        return raced, False
    except Exception:
        conn.rollback()
        raise
    stored = _stored_projection(conn, session_id, relative_path)
    assert stored is not None
    return stored, True


def referenced_file_paths(
    conn: sqlite3.Connection, session_id: int
) -> tuple[str, ...]:
    """Return classified file locators for the session's latest model run."""
    run = conn.execute(
        """
        SELECT cr.run_id
        FROM classification_runs cr
        JOIN semantic_projection_runs spr
          ON spr.classification_run_id = cr.run_id
         AND spr.session_id = cr.session_id
        WHERE cr.session_id = ?
        ORDER BY cr.classified_at DESC, cr.run_id DESC
        LIMIT 1
        """,
        (session_id,),
    ).fetchone()
    if run is None:
        return ()
    rows = conn.execute(
        """
        SELECT cp.location_evidence, rb.raw_block
        FROM classification_assignments ca
        JOIN classification_payloads cp ON cp.payload_pk = ca.payload_pk
        JOIN source_blocks sb
          ON sb.session_id = ca.session_id
         AND sb.source_block_pk = ca.source_block_pk
        JOIN raw_block_contents rb
          ON rb.raw_block_pk = sb.raw_block_pk
        WHERE ca.run_id = ?
        """,
        (run["run_id"],),
    ).fetchall()
    paths = {
        path
        for row in rows
        for path in (
            extract_file_from_location(row["location_evidence"])
            or extract_file_from_location(row["raw_block"]),
        )
        if path is not None
    }
    return tuple(sorted(paths, key=lambda value: (value.casefold(), value)))


def observe_session_sources(conn: sqlite3.Connection, session_id: int) -> int:
    """Persist every currently classified source locator exactly once."""
    mutated = 0
    for path in referenced_file_paths(conn, session_id):
        _result_value, changed = observe_file_instances(conn, session_id, path)
        mutated += int(changed)
    return mutated


def compare_file_observations(
    conn: sqlite3.Connection,
    current_session_id: int,
    previous_session_id: int,
    relative_path: str,
) -> dict[str, object] | None:
    """Compare two immutable processing-time observations of one source chain."""
    current = _stored_projection(conn, current_session_id, relative_path)
    previous = _stored_projection(conn, previous_session_id, relative_path)
    if current is None or previous is None:
        return None
    current_map = {
        (str(item["source_kind"]), str(item["source_key"])): item
        for item in current["instances"]
    }
    previous_map = {
        (str(item["source_kind"]), str(item["source_key"])): item
        for item in previous["instances"]
    }
    changes: list[dict[str, object]] = []
    for identity in sorted(set(previous_map) | set(current_map)):
        before = previous_map.get(identity)
        after = current_map.get(identity)
        status = (
            "added"
            if before is None
            else "removed"
            if after is None
            else "changed"
            if before["sha256"] != after["sha256"]
            else "unchanged"
        )
        changes.append(
            {
                "source_kind": identity[0],
                "source_key": identity[1],
                "status": status,
                "previous_sha256": before["sha256"] if before else None,
                "current_sha256": after["sha256"] if after else None,
            }
        )
    previous_winner = previous["file_layer"]["winner"]
    current_winner = current["file_layer"]["winner"]
    winner_changed = (
        (previous_winner is None) != (current_winner is None)
        or (
            previous_winner is not None
            and current_winner is not None
            and (
                previous_winner["source_kind"],
                previous_winner["source_key"],
                previous_winner["sha256"],
            )
            != (
                current_winner["source_kind"],
                current_winner["source_key"],
                current_winner["sha256"],
            )
        )
    )
    return {
        "relative_path": current["relative_path"],
        "previous_observed_at": previous["observation"]["observed_at"],
        "current_observed_at": current["observation"]["observed_at"],
        "changed": any(item["status"] != "unchanged" for item in changes),
        "file_layer_winner_changed": winner_changed,
        "instances": changes,
        "caveat": (
            "This correlates processing-time source observations with session "
            "error deltas; it does not by itself prove causation."
        ),
    }
