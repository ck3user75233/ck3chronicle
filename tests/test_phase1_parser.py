"""Phase 1 parser pipeline — acceptance tests (TDD red phase).

All tests in this file are expected to FAIL until Phase 1 is implemented.
They define the required contract for:
  - parser/log_blocks.py      (TimestampedLogBlock, iter_log_blocks)
  - parser/extractors/        (EXTRACTORS registry, extract_block)
  - parser/normalize.py       (normalize, NormalizedIssue)
  - models/issue.py           (KNOWN_CATEGORIES, IssueDraft)
  - db/schema.py + migrations (issues, issue_occurrences tables)
  - cli.py                    (parse subcommand with --session / --reparse)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "logs" / "phase1"


# ===========================================================================
# AT-1 — iter_log_blocks splits a multi-block log into correct parts
# ===========================================================================

def test_iter_log_blocks_splits_correctly(tmp_path):
    """Three-block log file → three TimestampedLogBlocks with correct metadata."""
    from ck3chronicle.parser.log_blocks import iter_log_blocks

    log = tmp_path / "error.log"
    log.write_text(
        '[10:00:01][script_system.cpp:1234]: Script error in "common/traits/00_traits.txt" near line 10.\n'
        "Invalid token: foo_trait\n"
        "[10:00:02][localization.cpp:456]: Localization key 'TRAIT_FOO_NAME' not found.\n"
        '[10:00:03][texture.cpp:100]: Failed to load texture "gfx/interface/icons/foo.dds".\n',
        encoding="utf-8",
    )

    blocks = list(iter_log_blocks(log))

    assert len(blocks) == 3
    assert blocks[0].timestamp == "10:00:01"
    assert blocks[0].source_tag == "script_system.cpp:1234"
    assert "Script error" in blocks[0].raw_block
    assert blocks[0].continuation_lines == ["Invalid token: foo_trait"]
    assert blocks[1].timestamp == "10:00:02"
    assert blocks[1].source_tag == "localization.cpp:456"
    assert blocks[2].timestamp == "10:00:03"
    assert blocks[2].source_tag == "texture.cpp:100"


def test_iter_log_blocks_parses_three_part_ck3_header(tmp_path):
    """Real CK3 header [time][level][source] is parsed with source_tag=source."""
    from ck3chronicle.parser.log_blocks import iter_log_blocks

    log = tmp_path / "error.log"
    log.write_text(
        "[13:04:56][E][dlc_descriptor.cpp:70]: Invalid supported_version in file: mod/ugc_123.mod line: 7\n",
        encoding="utf-8",
    )

    blocks = list(iter_log_blocks(log))

    assert len(blocks) == 1
    assert blocks[0].timestamp == "13:04:56"
    assert blocks[0].source_tag == "dlc_descriptor.cpp:70"
    assert "Invalid supported_version" in blocks[0].header_line


def test_normalize_strips_header_and_primary_file_from_signature():
    """Timestamp/source and primary_file differences should still cluster."""
    from ck3chronicle.models.issue import IssueDraft
    from ck3chronicle.parser.normalize import normalize

    d1 = IssueDraft(
        category="script_system",
        error_type="syntax_error",
        tags=[],
        engine_source="script_system.cpp:1234",
        sample_message='[14:00:01][E][script_system.cpp:1234]: Script system error in "common/traits/00_traits.txt" near line 5.',
        primary_file="common/traits/00_traits.txt",
        primary_line=5,
        referenced_symbols=[],
        referenced_objects=[],
        extra_json={},
        severity="error",
        confidence="high",
        raw_block="x",
        log_relpath="error.log",
        line_number=1,
    )
    d2 = IssueDraft(
        category="script_system",
        error_type="syntax_error",
        tags=[],
        engine_source="script_system.cpp:1234",
        sample_message='[14:25:59][E][script_system.cpp:1234]: Script system error in "common/traits/zzz_patch.txt" near line 99.',
        primary_file="common/traits/zzz_patch.txt",
        primary_line=99,
        referenced_symbols=[],
        referenced_objects=[],
        extra_json={},
        severity="error",
        confidence="high",
        raw_block="y",
        log_relpath="error.log",
        line_number=2,
    )

    n1 = normalize(d1)
    n2 = normalize(d2)

    assert n1.signature == n2.signature
    assert '"<FILE>"' in n1.message_template


# ===========================================================================
# AT-2 — iter_log_blocks returns empty iterator for an empty file
# ===========================================================================

def test_iter_log_blocks_handles_empty_file(tmp_path):
    """Empty log file → empty iterator, no exception."""
    from ck3chronicle.parser.log_blocks import iter_log_blocks

    log = tmp_path / "empty.log"
    log.write_text("", encoding="utf-8")

    blocks = list(iter_log_blocks(log))
    assert blocks == []


# ===========================================================================
# AT-3 — extractor registry ends with the unclassified extractor
# ===========================================================================

def test_extractor_registry_is_ordered_unclassified_last():
    """EXTRACTORS list must be non-empty and its last entry must be 'unclassified'."""
    from ck3chronicle.parser.extractors import EXTRACTORS

    assert len(EXTRACTORS) >= 1, "EXTRACTORS must not be empty"
    assert EXTRACTORS[-1].CATEGORY == "unclassified", (
        f"Last extractor must have CATEGORY='unclassified', got {EXTRACTORS[-1].CATEGORY!r}"
    )


# ===========================================================================
# AT-4 — every extractor CATEGORY is a member of KNOWN_CATEGORIES
# ===========================================================================

def test_all_extractor_categories_known():
    """Each extractor module's CATEGORY must be in KNOWN_CATEGORIES."""
    from ck3chronicle.models.issue import KNOWN_CATEGORIES
    from ck3chronicle.parser.extractors import EXTRACTORS

    for extractor in EXTRACTORS:
        assert extractor.CATEGORY in KNOWN_CATEGORIES, (
            f"Extractor {extractor!r} has unknown CATEGORY={extractor.CATEGORY!r}"
        )


# ===========================================================================
# AT-5 — a script_system log block is claimed by the script_system extractor
# ===========================================================================

def test_extract_block_claims_script_system():
    """Block from script_system.cpp → IssueDraft.category == 'script_system'."""
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock
    from ck3chronicle.parser.extractors import extract_block

    block = TimestampedLogBlock(
        timestamp="14:22:15",
        source_tag="script_system.cpp:1234",
        header_line=(
            '[14:22:15][script_system.cpp:1234]: Script system error in '
            '"common/traits/00_traits.txt" near line 42.'
        ),
        continuation_lines=[
            "Invalid token: foo_trait_invalid",
            "Expected: trait name or block terminator",
        ],
        raw_block=(
            '[14:22:15][script_system.cpp:1234]: Script system error in '
            '"common/traits/00_traits.txt" near line 42.\n'
            "Invalid token: foo_trait_invalid\n"
            "Expected: trait name or block terminator"
        ),
        log_relpath="error.log",
        line_number=1,
    )

    draft = extract_block(block)

    assert draft is not None
    assert draft.category == "script_system"


# ===========================================================================
# AT-6 — a localization log block is claimed by the localization extractor
# ===========================================================================

def test_extract_block_claims_localization():
    """Block from localization.cpp → IssueDraft.category == 'localization'."""
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock
    from ck3chronicle.parser.extractors import extract_block

    block = TimestampedLogBlock(
        timestamp="09:15:03",
        source_tag="localization.cpp:456",
        header_line=(
            "[09:15:03][localization.cpp:456]: Localization key "
            "'MY_KEY_001' not found in any localization file."
        ),
        continuation_lines=[],
        raw_block=(
            "[09:15:03][localization.cpp:456]: Localization key "
            "'MY_KEY_001' not found in any localization file."
        ),
        log_relpath="error.log",
        line_number=42,
    )

    draft = extract_block(block)

    assert draft is not None
    assert draft.category == "localization"


# ===========================================================================
# AT-7 — an unrecognised block falls through to the unclassified extractor
# ===========================================================================

def test_extract_block_falls_through_to_unclassified():
    """Block matching no extractor pattern → IssueDraft.category == 'unclassified'."""
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock
    from ck3chronicle.parser.extractors import extract_block

    block = TimestampedLogBlock(
        timestamp="12:34:56",
        source_tag="unknown_subsystem.cpp:999",
        header_line=(
            "[12:34:56][unknown_subsystem.cpp:999]: "
            "XR749 quantum fluctuation in matrix 7-B at address 0xDEADBEEF."
        ),
        continuation_lines=[],
        raw_block=(
            "[12:34:56][unknown_subsystem.cpp:999]: "
            "XR749 quantum fluctuation in matrix 7-B at address 0xDEADBEEF."
        ),
        log_relpath="error.log",
        line_number=77,
    )

    draft = extract_block(block)

    assert draft is not None, "extract_block must never return None (unclassified is the fallback)"
    assert draft.category == "unclassified"


# ===========================================================================
# AT-8 — every block parsed from multi_block.txt produces a draft
# ===========================================================================

def test_all_blocks_accounted_for():
    """All N blocks from multi_block.txt → N IssueDrafts, none None."""
    from ck3chronicle.parser.log_blocks import iter_log_blocks
    from ck3chronicle.parser.extractors import extract_block

    fixture_path = FIXTURES_DIR / "multi_block.txt"
    assert fixture_path.exists(), f"Fixture not found: {fixture_path}"

    blocks = list(iter_log_blocks(fixture_path))
    assert len(blocks) >= 5, f"Expected >=5 blocks in multi_block.txt, got {len(blocks)}"

    drafts = [extract_block(b) for b in blocks]
    assert len(drafts) == len(blocks)
    assert all(d is not None for d in drafts), (
        "extract_block returned None for some block — unclassified fallback must cover all cases"
    )


# ===========================================================================
# AT-9 — normalize masks volatile tokens in the message_template
# ===========================================================================

def test_normalize_masks_volatile_tokens():
    """Windows file path and 'near line N' in sample_message → <TOKEN> in message_template."""
    from ck3chronicle.models.issue import IssueDraft
    from ck3chronicle.parser.normalize import normalize

    draft = IssueDraft(
        category="script_system",
        error_type="syntax_error",
        tags=[],
        engine_source="script_system.cpp:1234",
        sample_message=(
            r'Script error in "C:\Users\foo\mods\common\traits\00_traits.txt" near line 42.'
        ),
        primary_file=r"C:\Users\foo\mods\common\traits\00_traits.txt",
        primary_line=42,
        referenced_symbols=[],
        referenced_objects=[],
        extra_json={},
        severity="error",
        confidence="high",
        raw_block=(
            "[10:00:01][script_system.cpp:1234]: Script error in "
            r'"C:\Users\foo\mods\common\traits\00_traits.txt" near line 42.'
        ),
        log_relpath="error.log",
        line_number=1,
    )

    result = normalize(draft)

    assert "<TOKEN>" in result.message_template, (
        "message_template must contain <TOKEN> for masked volatile tokens"
    )
    assert r"C:\Users\foo" not in result.message_template, (
        "Windows path must be replaced with <TOKEN> in message_template"
    )
    assert " line 42" not in result.message_template, (
        "'near line 42' must be replaced with <TOKEN> in message_template"
    )


# ===========================================================================
# AT-10 — normalize is deterministic: same IssueDraft → same signature
# ===========================================================================

def test_normalize_determinism():
    """Calling normalize() twice on identical IssueDraft → identical signature."""
    from ck3chronicle.models.issue import IssueDraft
    from ck3chronicle.parser.normalize import normalize

    def _draft() -> IssueDraft:
        return IssueDraft(
            category="localization",
            error_type="missing_key",
            tags=["ui"],
            engine_source="localization.cpp:456",
            sample_message="Localization key 'MY_KEY' not found.",
            primary_file=None,
            primary_line=None,
            referenced_symbols=["MY_KEY"],
            referenced_objects=[],
            extra_json={},
            severity="error",
            confidence="high",
            raw_block="[10:00:02][localization.cpp:456]: Localization key 'MY_KEY' not found.",
            log_relpath="error.log",
            line_number=10,
        )

    r1 = normalize(_draft())
    r2 = normalize(_draft())
    assert r1.signature == r2.signature, (
        "normalize() must produce the same signature for identical inputs"
    )


# ===========================================================================
# AT-11 — localization normalization: key masked in template, preserved in referenced_symbols
# ===========================================================================

def test_localization_occurrence_preserves_concrete_key():
    """MY_KEY_001 → <KEY> in message_template; MY_KEY_001 in referenced_symbols."""
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock
    from ck3chronicle.parser.extractors import extract_block
    from ck3chronicle.parser.normalize import normalize

    block = TimestampedLogBlock(
        timestamp="09:15:03",
        source_tag="localization.cpp:456",
        header_line=(
            "[09:15:03][localization.cpp:456]: Localization key "
            "'MY_KEY_001' not found in any localization file."
        ),
        continuation_lines=[],
        raw_block=(
            "[09:15:03][localization.cpp:456]: Localization key "
            "'MY_KEY_001' not found in any localization file."
        ),
        log_relpath="error.log",
        line_number=1,
    )

    draft = extract_block(block)
    assert draft is not None
    assert draft.category == "localization"

    result = normalize(draft)

    assert "<KEY>" in result.message_template, (
        "Localization key must be masked to <KEY> in message_template"
    )
    assert "MY_KEY_001" not in result.message_template, (
        "Concrete localization key must NOT appear literally in message_template"
    )
    assert "MY_KEY_001" in result.referenced_symbols, (
        "Concrete localization key must be preserved in referenced_symbols"
    )


# ===========================================================================
# AT-12 — migration creates issues and issue_occurrences tables
# ===========================================================================

def test_db_issues_table_created_on_migration(tmp_path):
    """open_db() on a fresh DB must create the issues and issue_occurrences tables."""
    from ck3chronicle.db.repository import open_db

    db_path = tmp_path / "test_v2.db"
    conn = open_db(db_path)

    tables: set[str] = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    conn.close()

    assert "issues" in tables, (
        "Phase 1 migration must create the 'issues' table"
    )
    assert "issue_occurrences" in tables, (
        "Phase 1 migration must create the 'issue_occurrences' table"
    )


# ===========================================================================
# AT-13 — CLI exposes a 'parse' subcommand with --session and --reparse
# ===========================================================================

def test_cli_parse_command_exists():
    """ck3chronicle parse --help exits 0 and mentions --session and --reparse."""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from ck3chronicle.cli import main; main(['parse', '--help'])",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"parse --help should exit 0, got {result.returncode}.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert "--session" in result.stdout, (
        f"'parse --help' must mention '--session' in stdout.\nGot: {result.stdout}"
    )
    assert "--reparse" in result.stdout, (
        f"'parse --help' must mention '--reparse' in stdout.\nGot: {result.stdout}"
    )


# ===========================================================================
# AT-14 — CLI parse subcommand populates the issues table from a real session
# ===========================================================================

def test_cli_parse_runs_and_populates_issues(tmp_path):
    """Ingest a fixture log, then 'parse --session N'; issues table must have >=1 row."""
    import ck3chronicle.config as cfg
    from ck3chronicle.cli import build_parser
    from ck3chronicle.db.repository import open_db
    from ck3chronicle.ingest import ingest

    fixture_logs = FIXTURES_DIR / "for_cli_parse"
    assert fixture_logs.exists(), f"Fixture dir not found: {fixture_logs}"

    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        # Seed a session via ingest
        ingest_result = ingest(logs_root=fixture_logs)
        session_id = ingest_result.session_id

        # Run the parse subcommand in-process
        parser = build_parser()
        args = parser.parse_args(["parse", "--session", str(session_id)])
        rc = args.func(args)

    assert rc == 0, f"parse command should return exit code 0, got {rc!r}"

    db_path = tmp_path / "ck3chronicle.db"
    conn = open_db(db_path)
    count = conn.execute(
        "SELECT COUNT(*) FROM issues WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0]
    conn.close()

    assert count >= 1, (
        f"Expected >=1 row in issues for session {session_id}, got {count}"
    )


# ===========================================================================
# AT-15 — each non-unclassified extractor claims at least one block in multi_block.txt
# ===========================================================================

def test_per_extractor_coverage():
    """For every non-unclassified extractor, multi_block.txt must contain a matching block."""
    from ck3chronicle.parser.extractors import EXTRACTORS
    from ck3chronicle.parser.log_blocks import iter_log_blocks

    fixture_path = FIXTURES_DIR / "multi_block.txt"
    assert fixture_path.exists(), f"Fixture not found: {fixture_path}"

    blocks = list(iter_log_blocks(fixture_path))
    assert blocks, "multi_block.txt must contain at least one block"

    non_unclassified = [e for e in EXTRACTORS if e.CATEGORY != "unclassified"]
    assert non_unclassified, "Must have at least one non-unclassified extractor"

    missing: list[str] = []
    for extractor in non_unclassified:
        claimed = any(extractor.match(block) for block in blocks)
        if not claimed:
            missing.append(extractor.CATEGORY)

    assert not missing, (
        f"These extractor categories claim no block in multi_block.txt: {missing}\n"
        "Add blocks to multi_block.txt or fix the extractor's match() logic."
    )

# ===========================================================================
# AT-16 — 50 identical localization errors cluster to 1 issue, occurrence_count=50
# ===========================================================================

@pytest.mark.skip(
    reason="obsolete collapsed-occurrence SQL; replaced by C1 canonical service tests"
)
def test_clustering_50_identical_localization_errors():
    """Fixture with 50 identical localization errors must cluster to 1 canonical issue row."""
    import json
    import sqlite3

    from ck3chronicle.db.migrations import apply_migrations
    from ck3chronicle.parser.extractors import extract_block
    from ck3chronicle.parser.log_blocks import iter_log_blocks
    from ck3chronicle.parser.normalize import normalize

    fixture = (
        Path(__file__).parent
        / "fixtures"
        / "logs"
        / "noisy_localization"
        / "error.log"
    )
    assert fixture.exists(), f"Fixture not found: {fixture}"

    # Create in-memory DB and apply migrations.
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    apply_migrations(conn)

    # Insert a minimal session row so session_id=1 exists.
    conn.execute(
        "INSERT INTO sessions "
        "(evidence_bundle_hash, created_at, log_count, crash_present, total_bytes) "
        "VALUES (?, ?, ?, ?, ?)",
        ("test_noisy_loc", "2026-06-14T00:00:00", 1, 0, 1024),
    )
    conn.commit()
    session_id: int = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    # Run the parse pipeline (mirrors cmd_parse INSERT/UPDATE logic).
    rel_path = "error.log"
    log_type = "error"
    for block in iter_log_blocks(fixture):
        block.log_relpath = rel_path
        draft = extract_block(block)
        if draft is None:
            continue
        result = normalize(draft)

        existing = conn.execute(
            "SELECT issue_id, occurrence_count FROM issues "
            "WHERE session_id = ? AND signature = ?",
            (session_id, result.signature),
        ).fetchone()
        if existing is None:
            conn.execute(
                """
                INSERT INTO issues (
                    session_id, signature, category, error_type,
                    tags_json, engine_source, severity, confidence,
                    message_template, sample_message, primary_file, primary_line,
                    referenced_symbols_json, referenced_objects_json,
                    extra_json, occurrence_count, log_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    result.signature,
                    result.category,
                    result.error_type,
                    json.dumps(result.tags),
                    result.engine_source,
                    result.severity,
                    result.confidence,
                    result.message_template,
                    result.sample_message,
                    result.primary_file,
                    result.primary_line,
                    json.dumps(result.referenced_symbols),
                    json.dumps(result.referenced_objects),
                    json.dumps(result.extra_json),
                    1,
                    log_type,
                ),
            )
        else:
            conn.execute(
                "UPDATE issues SET occurrence_count = occurrence_count + 1, "
                "log_type = ? WHERE issue_id = ?",
                (log_type, existing["issue_id"]),
            )

        existing_occ = conn.execute(
            "SELECT issue_occurrence_id FROM issue_occurrences "
            "WHERE session_id = ? AND signature = ? AND log_relpath = ?",
            (session_id, result.signature, result.log_relpath),
        ).fetchone()
        if existing_occ is None:
            conn.execute(
                """
                INSERT INTO issue_occurrences (
                    session_id, signature, log_relpath, line_number,
                    raw_block, occurrence_count,
                    referenced_symbols_json, extra_json, log_type
                ) VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?)
                """,
                (
                    session_id,
                    result.signature,
                    result.log_relpath,
                    result.line_number,
                    result.raw_block,
                    json.dumps(result.referenced_symbols),
                    json.dumps(result.extra_json),
                    log_type,
                ),
            )
        else:
            conn.execute(
                "UPDATE issue_occurrences "
                "SET occurrence_count = occurrence_count + 1, log_type = ? "
                "WHERE issue_occurrence_id = ?",
                (log_type, existing_occ["issue_occurrence_id"]),
            )

    conn.commit()

    rows = conn.execute(
        "SELECT category, occurrence_count FROM issues WHERE session_id = ?",
        (session_id,),
    ).fetchall()
    conn.close()

    assert len(rows) == 1, (
        f"Expected exactly 1 issue row (all 50 errors must cluster), got {len(rows)}"
    )
    assert rows[0]["category"] == "localization", (
        f"Expected category='localization', got {rows[0]['category']!r}"
    )
    assert rows[0]["occurrence_count"] == 50, (
        f"Expected occurrence_count=50, got {rows[0]['occurrence_count']}"
    )


# ===========================================================================
# AT-17 — debug_log extractor: pdx_localize.cpp duplicate key
# ===========================================================================

def test_debug_log_matches_pdx_localize():
    """debug_log.match() returns True for pdx_localize.cpp source tags."""
    from ck3chronicle.parser.extractors import debug_log
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock

    block = TimestampedLogBlock(
        timestamp="10:00:01",
        source_tag="pdx_localize.cpp:300",
        header_line="Localization key 'TRAIT_FOO_NAME' is present in both 'base/english/traits_l_english.yml' and 'mod/english/traits_l_english.yml'.",
        continuation_lines=[],
        raw_block="[10:00:01][pdx_localize.cpp:300]: ...",
        log_relpath="debug.log",
        line_number=1,
    )

    assert debug_log.match(block) is True

    draft = debug_log.extract(block)
    assert draft.category == "localization"
    assert draft.error_type == "duplicate_key"
    # Volatile key and file should be templated out
    assert "'TRAIT_FOO_NAME'" not in draft.sample_message
    assert "'<KEY>'" in draft.sample_message
    assert "TRAIT_FOO_NAME" in draft.referenced_symbols


def test_debug_log_50_identical_duplicate_keys_cluster():
    """50 identical pdx_localize duplicate-key blocks → same signature every time."""
    from ck3chronicle.parser.extractors import debug_log
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock
    from ck3chronicle.parser.normalize import normalize

    def _make_block(ts: str) -> TimestampedLogBlock:
        return TimestampedLogBlock(
            timestamp=ts,
            source_tag="pdx_localize.cpp:300",
            header_line="Localization key 'MY_LOC_KEY' is present in both 'file1.yml' and 'file2.yml'.",
            continuation_lines=[],
            raw_block=f"[{ts}][pdx_localize.cpp:300]: ...",
            log_relpath="debug.log",
            line_number=1,
        )

    sigs = set()
    for i in range(50):
        block = _make_block(f"10:00:{i:02d}")
        draft = debug_log.extract(block)
        result = normalize(draft)
        sigs.add(result.signature)

    assert len(sigs) == 1, (
        f"Expected 1 unique signature for 50 identical duplicate_key blocks, got {len(sigs)}"
    )


# ===========================================================================
# AT-18 — debug_log extractor: gamedatabase.h database_override
# ===========================================================================

def test_debug_log_matches_gamedatabase():
    """debug_log.match() returns True for gamedatabase.h source tags."""
    from ck3chronicle.parser.extractors import debug_log
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock

    block = TimestampedLogBlock(
        timestamp="10:00:01",
        source_tag="gamedatabase.h:512",
        header_line="[Trait brave] is being overridden in [mod A], using [mod B] instead.",
        continuation_lines=[],
        raw_block="[10:00:01][gamedatabase.h:512]: ...",
        log_relpath="debug.log",
        line_number=1,
    )

    assert debug_log.match(block) is True

    draft = debug_log.extract(block)
    assert draft.category == "database_reference"
    assert draft.error_type == "database_override"
    assert "[Trait brave]" not in draft.sample_message
    assert "[<OBJECT>]" in draft.sample_message
    # Bracketed tokens preserved in referenced_objects
    assert any("Trait brave" in obj or "brave" in obj for obj in draft.referenced_objects)


# ===========================================================================
# AT-19 — log-type dispatch: debug.log → DEBUG_EXTRACTORS (debug_log first)
# ===========================================================================

def test_log_type_dispatch_debug_routes_to_debug_extractors():
    """extract_block_for_log_type with log_type='debug' routes pdx_localize block to debug_log."""
    from ck3chronicle.parser.extractors import extract_block_for_log_type
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock

    block = TimestampedLogBlock(
        timestamp="10:00:01",
        source_tag="pdx_localize.cpp:300",
        header_line="Localization key 'FOO_KEY' is present in both 'a.yml' and 'b.yml'.",
        continuation_lines=[],
        raw_block="...",
        log_relpath="debug.log",
        line_number=1,
    )

    draft = extract_block_for_log_type(block, "debug")
    assert draft.category == "localization"
    assert draft.error_type == "duplicate_key"
    assert "debug_log" in draft.tags


def test_log_type_dispatch_error_does_not_route_to_debug_log():
    """extract_block_for_log_type with log_type='error' does NOT match debug_log for script_system block."""
    from ck3chronicle.parser.extractors import extract_block_for_log_type
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock

    block = TimestampedLogBlock(
        timestamp="10:00:01",
        source_tag="script_system.cpp:100",
        header_line="Wrong scope for trigger 'is_alive' in 'common/decisions/foo.txt' near line 5.",
        continuation_lines=[],
        raw_block="...",
        log_relpath="error.log",
        line_number=1,
    )

    draft = extract_block_for_log_type(block, "error")
    assert draft.category == "script_system"
    assert "debug_log" not in draft.tags


def test_log_type_dispatch_unknown_falls_back_to_error_extractors():
    """extract_block_for_log_type with log_type='unknown' uses ERROR_EXTRACTORS."""
    from ck3chronicle.parser.extractors import extract_block_for_log_type
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock

    block = TimestampedLogBlock(
        timestamp="10:00:01",
        source_tag="script_system.cpp:100",
        header_line="Some script error.",
        continuation_lines=[],
        raw_block="...",
        log_relpath="some_other.log",
        line_number=1,
    )

    draft = extract_block_for_log_type(block, "unknown")
    # Should still classify script_system (not fall to unclassified)
    assert draft.category == "script_system"


# ===========================================================================
# AT-20 — Heritage error_type taxonomy in script_system extractor
# ===========================================================================

def test_script_system_heritage_wrong_scope():
    """script_system extractor assigns error_type='wrong_scope' for Wrong scope messages."""
    from ck3chronicle.parser.extractors import script_system
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock

    block = TimestampedLogBlock(
        timestamp="10:00:01",
        source_tag="script_system.cpp:100",
        header_line="Wrong scope for trigger 'is_alive' in 'common/decisions/foo.txt' near line 5.",
        continuation_lines=[],
        raw_block="...",
        log_relpath="error.log",
        line_number=1,
    )
    draft = script_system.extract(block)
    assert draft.category == "script_system"
    assert draft.error_type == "wrong_scope"


def test_script_system_heritage_duplicate_definition():
    """script_system extractor assigns error_type='duplicate_definition' for duplicate messages."""
    from ck3chronicle.parser.extractors import script_system
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock

    block = TimestampedLogBlock(
        timestamp="10:00:01",
        source_tag="script_system.cpp:100",
        header_line="Duplicate definition for trait 'brave' in 'common/traits/00_traits.txt' near line 12.",
        continuation_lines=[],
        raw_block="...",
        log_relpath="error.log",
        line_number=1,
    )
    draft = script_system.extract(block)
    assert draft.error_type == "duplicate_definition"


def test_script_system_heritage_unknown_effect():
    """script_system extractor assigns error_type='unknown_effect'."""
    from ck3chronicle.parser.extractors import script_system
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock

    block = TimestampedLogBlock(
        timestamp="10:00:01",
        source_tag="script_system.cpp:100",
        header_line="Unknown effect 'my_broken_effect' in 'events/foo.txt' near line 42.",
        continuation_lines=[],
        raw_block="...",
        log_relpath="error.log",
        line_number=1,
    )
    draft = script_system.extract(block)
    assert draft.error_type == "unknown_effect"


def test_script_system_heritage_syntax_error_default():
    """script_system extractor falls back to error_type='syntax_error' for unrecognized messages."""
    from ck3chronicle.parser.extractors import script_system
    from ck3chronicle.parser.log_blocks import TimestampedLogBlock

    block = TimestampedLogBlock(
        timestamp="10:00:01",
        source_tag="script_system.cpp:100",
        header_line="Something weird and unrecognised happened here.",
        continuation_lines=[],
        raw_block="...",
        log_relpath="error.log",
        line_number=1,
    )
    draft = script_system.extract(block)
    assert draft.error_type == "syntax_error"


# ===========================================================================
# AT-21 — _log_type_from_relpath: database_conflicts mapping
# ===========================================================================

def test_log_type_from_relpath_database_conflicts():
    """_log_type_from_relpath maps database_conflicts.log → 'database_conflicts'."""
    import pathlib
    import importlib
    import sys

    # Import cli._log_type_from_relpath
    import ck3chronicle.cli as cli

    assert cli._log_type_from_relpath("database_conflicts.log") == "database_conflicts"
    assert cli._log_type_from_relpath("error.log") == "error"
    assert cli._log_type_from_relpath("debug.log") == "debug"
    assert cli._log_type_from_relpath("game.log") == "game"
    assert cli._log_type_from_relpath("crash_dump.log") == "unknown"
