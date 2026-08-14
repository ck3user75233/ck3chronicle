"""Development checks for separated runner/scorer infrastructure."""
from __future__ import annotations

import copy
import hashlib
from pathlib import Path
import sys

from foundation_oracle import LEXICAL_BLOCK_ORACLE, LEXICAL_ERROR_BYTES


TOOLS = Path(__file__).resolve().parents[1] / "tools" / "phase1_exit"
sys.path.insert(0, str(TOOLS))
from run_lexical_candidate import run  # noqa: E402
from score_lexical import score  # noqa: E402


def _oracle() -> dict[str, object]:
    blocks = []
    for index, item in enumerate(LEXICAL_BLOCK_ORACLE[1:], start=1):
        blocks.append(
            {
                "index": index,
                "start_line": item["start_line"],
                "end_line": item["end_line"],
                "line_count": item["end_line"] - item["start_line"] + 1,
                "timestamp": item["timestamp"],
                "level": item["level"],
                "source_tag": "first.cpp:10" if index == 1 else "second.cpp:20",
                "source_family": item["source_family"],
                "raw_sha256": item["raw_sha256"],
                "byte_count": item["bytes"],
            }
        )
    return {
        "source": {
            "sha256": hashlib.sha256(LEXICAL_ERROR_BYTES).hexdigest(),
            "byte_count": len(LEXICAL_ERROR_BYTES),
        },
        "summary": {
            "block_count": 2,
            "block_byte_count": sum(item["byte_count"] for item in blocks),
            "preamble_byte_count": LEXICAL_BLOCK_ORACLE[0]["bytes"],
        },
        "blocks": blocks,
    }


def test_rexit_001_blind_lexical_runner_contains_no_expected_answers(
    tmp_path: Path,
) -> None:
    error_log = tmp_path / "error.log"
    error_log.write_bytes(LEXICAL_ERROR_BYTES)

    result = run(error_log, repo=Path(__file__).resolve().parents[1])

    assert result["schema"] == "ck3chronicle.phase1.lexical-run"
    assert result["input"] == {
        "relative_role": "error.log",
        "sha256": hashlib.sha256(LEXICAL_ERROR_BYTES).hexdigest(),
        "byte_count": len(LEXICAL_ERROR_BYTES),
    }
    assert result["candidate"]["commit"] == result["candidate_commit"]
    assert result["candidate"]["imported_module"] == (
        "src/ck3chronicle/parser/log_blocks.py"
    )
    assert len(result["candidate"]["imported_module_sha256"]) == 64
    assert len(result["blocks"]) == 2
    assert "expected" not in repr(result).casefold()


def test_rexit_002_independent_scorer_passes_exact_and_rejects_mutation(
    tmp_path: Path,
) -> None:
    error_log = tmp_path / "error.log"
    error_log.write_bytes(LEXICAL_ERROR_BYTES)
    result = run(error_log, repo=Path(__file__).resolve().parents[1])
    oracle = _oracle()

    accepted = score(result, oracle)
    assert accepted["status"] == "pass"
    assert accepted["gate_component"] == "P1-PAR-01-LEXICAL"
    assert accepted["blocks_compared"] == 2

    mutated = copy.deepcopy(result)
    mutated["blocks"][0]["source_family"] = "wrong.cpp"
    rejected = score(mutated, oracle)
    assert rejected["status"] == "fail"
    assert rejected["field_mismatch_counts"] == {"source_family": 1}


def test_rexit_003_runner_and_scorer_keep_opposite_authority_boundaries() -> None:
    """Guardrail: runner cannot accept answers; scorer cannot execute product code."""
    runner_source = (TOOLS / "run_lexical_candidate.py").read_text(encoding="utf-8")
    scorer_source = (TOOLS / "score_lexical.py").read_text(encoding="utf-8")

    assert "--oracle" not in runner_source
    assert "from ck3chronicle" not in scorer_source
    assert "import ck3chronicle" not in scorer_source
    assert "subprocess" not in scorer_source
