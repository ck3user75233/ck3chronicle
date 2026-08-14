"""Functional contracts for same-run DLC and active-mod evidence."""

from __future__ import annotations

from dataclasses import replace
import hashlib
import json
import sqlite3

import pytest

from ck3chronicle import config
from ck3chronicle.cli import build_parser
from ck3chronicle.db import repository
from ck3chronicle.db.schema import SESSIONS_DDL
from ck3chronicle.harvester import MANIFEST_VERSION, finalize_pending, spool_logs
from ck3chronicle.runtime_context import RuntimeContextError, parse_runtime_context
from ck3chronicle.source_resolution import SourceResolutionError, resolve_file_instances

from foundation_oracle import SIX_LOG_BYTES, write_logs


DEBUG_CONTEXT = (
    b"[12:00:00][D][jomini_game_setup.cpp:130]: DLC:\n"
    b"Alpha Pack|dlc/dlc001_alpha/dlc001.dlc\n"
    b"Beta Pack|dlc/dlc002_beta/dlc002.dlc\n"
    b"Mod:\n"
    b"Inactive Noise|mod/ugc_999.mod|Disabled\n"
    b"Active | Workshop|mod/ugc_222.mod|Enabled\n"
    b"Local Patch|mod/Local Patch.mod|Enabled\n"
    b"\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
    b"C:/CK3/game/dlc/dlc002_beta\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
    b"C:/CK3/game/dlc/dlc001_alpha\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
    b"C:/Steam/workshop/content/1158310/222\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
    b"C:/Users/test/CK3/mod/LocalPatch\n"
    b"[12:00:01][D][virtualfilesystem.cpp:339]: Startup continues\n"
)


def _captured_session(tmp_path, debug_log: bytes | None = DEBUG_CONTEXT):
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    files = dict(SIX_LOG_BYTES)
    if debug_log is None:
        files.pop("debug.log")
    else:
        files["debug.log"] = debug_log
    write_logs(logs, files)
    captured = finalize_pending(spool_logs(logs, runtime), runtime)
    conn = repository.open_db(runtime / "ck3chronicle.db")
    session_id, _duplicate = repository.register_finalized_session(
        conn,
        evidence_bundle_hash=captured.evidence_bundle_hash,
        captured_at="2026-08-14T00:00:00+00:00",
        manifest_version=MANIFEST_VERSION,
        manifest_sha256=captured.manifest_sha256,
        evidence_completeness=("partial" if debug_log is None else "complete"),
        files=captured.files,
    )
    return runtime, captured, conn, session_id


def test_rcontext_001_mounted_data_is_authoritative_membership_and_order(
    tmp_path,
) -> None:
    runtime, _captured, conn, session_id = _captured_session(tmp_path)

    result = parse_runtime_context(conn, runtime, session_id)

    assert result.mutated is True
    assert result.status == "complete"
    assert result.warnings == ()
    assert result.inventory_warnings == ()
    assert result.inventory_dlc_count == 2
    assert result.inventory_enabled_mod_count == 2
    assert [item.dlc_key for item in result.dlcs] == [
        "dlc002_beta",
        "dlc001_alpha",
    ]
    assert [item.display_name for item in result.dlcs] == ["Beta Pack", "Alpha Pack"]
    assert [item.mod_key for item in result.mods] == ["222", "local:localpatch"]
    assert [item.display_name for item in result.mods] == [
        "Active | Workshop",
        "Local Patch",
    ]
    assert [item.source_kind for item in result.mods] == ["workshop", "local"]
    assert [item.mount_ordinal for item in (*result.dlcs, *result.mods)] == [0, 1, 2, 3]
    assert all(item.mod_key != "999" for item in result.mods)
    stored = repository.get_runtime_context(conn, session_id)
    assert stored["mounted_entry_count"] == 4
    assert stored["debug_log_sha256"] == result.debug_log_sha256
    lines = DEBUG_CONTEXT.splitlines(keepends=True)
    mounted_indexes = [
        index for index, line in enumerate(lines) if b"Mounted Data:" in line
    ]
    expected_block = b"".join(lines[mounted_indexes[0] : mounted_indexes[-1] + 1])
    assert result.source_session_file_id is not None
    assert result.block_start_line == mounted_indexes[0] + 1
    assert result.block_end_line == mounted_indexes[-1] + 1
    assert result.block_start_byte == sum(
        len(line) for line in lines[: mounted_indexes[0]]
    )
    assert result.block_end_byte == result.block_start_byte + len(expected_block)
    assert result.block_sha256 == hashlib.sha256(expected_block).hexdigest()
    assert result.block_candidate_count == 1
    assert result.valid_mount_count == 4
    assert result.malformed_mount_count == 0
    assert result.termination_evidence == "next_non_mount_line"
    assert result.absence_reason is None

    second = parse_runtime_context(conn, runtime, session_id)
    assert second.mutated is False
    assert second == replace(result, mutated=False)
    conn.close()


def test_rcontext_002_inventory_mismatch_is_visible_but_cannot_add_a_mod(
    tmp_path,
) -> None:
    debug = DEBUG_CONTEXT.replace(
        b"Local Patch|mod/Local Patch.mod|Enabled\n",
        b"Local Patch|mod/Local Patch.mod|Enabled\n"
        b"Not Mounted|mod/ugc_333.mod|Enabled\n",
    )
    runtime, _captured, conn, session_id = _captured_session(tmp_path, debug)

    result = parse_runtime_context(conn, runtime, session_id)

    assert result.status == "complete"
    assert result.inventory_enabled_mod_count == 3
    assert [item.mod_key for item in result.mods] == ["222", "local:localpatch"]
    assert all(item.mod_key != "333" for item in result.mods)
    assert result.warnings == ()
    assert "enabled_only=['333']" in result.inventory_warnings[0]
    conn.close()


def test_rcontext_003_missing_debug_is_explicit_absent_state(tmp_path) -> None:
    runtime, _captured, conn, session_id = _captured_session(tmp_path, None)

    result = parse_runtime_context(conn, runtime, session_id)

    assert result.status == "absent"
    assert result.debug_log_sha256 is None
    assert result.dlcs == ()
    assert result.mods == ()
    assert result.warnings == ("captured debug.log is absent",)
    assert result.source_session_file_id is None
    assert result.block_candidate_count == 0
    assert result.absence_reason == "debug_log_absent"
    conn.close()


def test_rcontext_004_failed_reparse_preserves_prior_context(tmp_path) -> None:
    runtime, captured, conn, session_id = _captured_session(tmp_path)
    accepted = parse_runtime_context(conn, runtime, session_id)
    debug_path = captured.dest_dir / "debug.log"
    debug_path.write_bytes(debug_path.read_bytes() + b"corruption")

    with pytest.raises(RuntimeContextError, match="byte length"):
        parse_runtime_context(conn, runtime, session_id, reparse=True)

    preserved = parse_runtime_context(conn, runtime, session_id)
    assert preserved.status == accepted.status
    assert preserved.mods == accepted.mods
    assert preserved.mutated is False
    conn.close()


def test_rcontext_005_cli_json_exposes_complete_ordered_context(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, _captured, conn, session_id = _captured_session(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    args = build_parser().parse_args(
        ["context", "--session", str(session_id), "--json"]
    )

    assert args.func(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema"] == "ck3chronicle.runtime-context"
    assert payload["schema_version"] == 2
    assert payload["status"] == "complete"
    assert [item["dlc_key"] for item in payload["dlcs"]] == [
        "dlc002_beta",
        "dlc001_alpha",
    ]
    assert [item["mod_key"] for item in payload["active_mods"]] == [
        "222",
        "local:localpatch",
    ]
    assert payload["provenance"]["candidate_count"] == 1
    assert payload["provenance"]["valid_mount_count"] == 4
    assert payload["inventory_enrichment"]["enabled_mod_count"] == 2


def test_rcontext_006_debug_without_mounted_data_has_distinct_absence_reason(
    tmp_path,
) -> None:
    runtime, _captured, conn, session_id = _captured_session(
        tmp_path,
        b"[12:00:00][D][virtualfilesystem.cpp:339]: Startup continues\n",
    )

    result = parse_runtime_context(conn, runtime, session_id)

    assert result.status == "absent"
    assert result.source_session_file_id is not None
    assert result.absence_reason == "mounted_data_not_found"
    assert result.block_candidate_count == 0
    conn.close()


def test_rcontext_007_valid_and_malformed_mount_lines_are_partial(tmp_path) -> None:
    debug = (
        b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: C:/Steam/workshop/content/1158310/111\n"
        b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data:\n"
        b"[12:00:01][D][virtualfilesystem.cpp:339]: Startup continues\n"
    )
    runtime, _captured, conn, session_id = _captured_session(tmp_path, debug)

    result = parse_runtime_context(conn, runtime, session_id)

    assert result.status == "partial"
    assert result.block_candidate_count == 1
    assert result.valid_mount_count == 1
    assert result.malformed_mount_count == 1
    assert [item.mod_key for item in result.mods] == ["111"]
    with pytest.raises(SourceResolutionError, match="requires a complete"):
        resolve_file_instances(conn, session_id, "common/test.txt")
    conn.close()


def test_rcontext_008_malformed_only_block_is_not_authoritative(tmp_path) -> None:
    debug = (
        b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data:\n"
        b"[12:00:01][D][virtualfilesystem.cpp:339]: Startup continues\n"
    )
    runtime, _captured, conn, session_id = _captured_session(tmp_path, debug)

    result = parse_runtime_context(conn, runtime, session_id)

    assert result.status == "malformed"
    assert result.valid_mount_count == 0
    assert result.malformed_mount_count == 1
    assert result.mods == ()
    conn.close()


def test_rcontext_009_eof_during_mounted_block_is_truncated(tmp_path) -> None:
    debug = b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: C:/Steam/workshop/content/1158310/111\n"
    runtime, _captured, conn, session_id = _captured_session(tmp_path, debug)

    result = parse_runtime_context(conn, runtime, session_id)

    assert result.status == "truncated"
    assert result.valid_mount_count == 1
    assert result.termination_evidence == "end_of_file"
    conn.close()


def test_rcontext_010_multiple_mounted_blocks_are_ambiguous(tmp_path) -> None:
    debug = (
        b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: C:/Steam/workshop/content/1158310/111\n"
        b"[12:00:01][D][virtualfilesystem.cpp:339]: Between blocks\n"
        b"[12:00:02][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: C:/Steam/workshop/content/1158310/222\n"
        b"[12:00:03][D][virtualfilesystem.cpp:339]: Startup continues\n"
    )
    runtime, _captured, conn, session_id = _captured_session(tmp_path, debug)

    result = parse_runtime_context(conn, runtime, session_id)

    assert result.status == "ambiguous"
    assert result.block_candidate_count == 2
    assert result.block_start_line is None
    assert result.mods == ()
    conn.close()


def test_rcontext_011_v1_summary_migrates_without_inventing_provenance(
    tmp_path,
) -> None:
    db_path = tmp_path / "legacy.db"
    legacy = sqlite3.connect(db_path)
    legacy.execute(SESSIONS_DDL)
    legacy.execute(
        """
        CREATE TABLE session_runtime_contexts (
            session_id INTEGER PRIMARY KEY REFERENCES sessions(session_id),
            context_contract_version TEXT NOT NULL,
            parsed_at TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('complete', 'partial', 'absent')),
            debug_log_sha256 TEXT,
            mounted_entry_count INTEGER NOT NULL,
            dlc_count INTEGER NOT NULL,
            mod_count INTEGER NOT NULL,
            unknown_mount_count INTEGER NOT NULL,
            inventory_enabled_mod_count INTEGER NOT NULL,
            inventory_dlc_count INTEGER NOT NULL,
            warnings_json TEXT NOT NULL DEFAULT '[]'
        )
        """
    )
    legacy.execute(
        """
        INSERT INTO sessions (
            evidence_bundle_hash, created_at, log_count, crash_present,
            total_bytes, capture_status, evidence_completeness
        ) VALUES (?, ?, 0, 0, 0, 'legacy_unverified', 'partial')
        """,
        ("a" * 64, "2026-08-14T00:00:00+00:00"),
    )
    legacy.execute(
        """
        INSERT INTO session_runtime_contexts VALUES (
            1, '1.1.0', '2026-08-14T00:01:00+00:00', 'complete',
            ?, 0, 0, 0, 0, 0, 0, '[]'
        )
        """,
        ("b" * 64,),
    )
    legacy.commit()
    legacy.close()

    migrated = repository.open_db(db_path)
    row = repository.get_runtime_context(migrated, 1)
    assert row["context_contract_version"] == "1.1.0"
    assert row["status"] == "complete"
    assert row["source_session_file_id"] is None
    assert row["block_sha256"] is None
    assert row["block_candidate_count"] == 0
    assert migrated.execute(
        "SELECT version FROM schema_versions WHERE component = 'runtime_context'"
    ).fetchone()[0] == 2
    migrated.close()


def test_rcontext_012_inventory_names_cannot_change_authoritative_mounts(
    tmp_path,
) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_runtime, _capture, first_conn, first_id = _captured_session(first_root)
    changed_inventory = DEBUG_CONTEXT.replace(b"Alpha Pack", b"Other Name")
    second_runtime, _capture, second_conn, second_id = _captured_session(
        second_root, changed_inventory
    )

    first = parse_runtime_context(first_conn, first_runtime, first_id)
    second = parse_runtime_context(second_conn, second_runtime, second_id)
    first_authority = [
        (item.mount_ordinal, item.dlc_key, item.mount_path) for item in first.dlcs
    ] + [
        (item.mount_ordinal, item.mod_key, item.mount_path) for item in first.mods
    ]
    second_authority = [
        (item.mount_ordinal, item.dlc_key, item.mount_path) for item in second.dlcs
    ] + [
        (item.mount_ordinal, item.mod_key, item.mount_path) for item in second.mods
    ]
    assert second_authority == first_authority
    assert first.dlcs[1].display_name == "Alpha Pack"
    assert second.dlcs[1].display_name == "Other Name"
    first_conn.close()
    second_conn.close()
