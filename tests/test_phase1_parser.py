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
        confidence=1.0,
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
            confidence=1.0,
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
