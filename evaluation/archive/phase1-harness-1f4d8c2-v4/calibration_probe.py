"""Minimal non-scoring public-interface calibration.

Uses a labeled synthetic one-block fixture only.  It neither executes a public
gate nor reads any oracle, expected-answer, private, or prior-result material.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True); parser.add_argument("--locator-log", required=True); args = parser.parse_args()
    from ck3chronicle.classification.catalog import load_approved_classifier
    from ck3chronicle.classification.normalize import block_message, semantic_units, tokenize
    from ck3chronicle.harvester import spool_logs
    from ck3chronicle.parser.log_blocks import iter_log_blocks

    temporary = Path(tempfile.mkdtemp(prefix="ck3chronicle-phase1-calibration-"))
    try:
        logs = temporary / "logs"; evidence = temporary / "evidence"; logs.mkdir(); evidence.mkdir()
        source = b"[00:00:00][E][phase1_calibration.cpp:1]: synthetic harness calibration only\r\n"
        (logs / "error.log").write_bytes(source); (logs / "debug.log").write_bytes(b""); (logs / "game.log").write_bytes(b"")
        blocks = list(iter_log_blocks(logs / "error.log", log_relpath="error.log", retain_preamble=True))
        pending = spool_logs(logs, evidence)
        classifier = load_approved_classifier()
        locator_path = Path(args.locator_log)
        locator_block = None
        for block in iter_log_blocks(locator_path, log_relpath="error.log", retain_preamble=True):
            if re.search(r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/]", block.raw_block):
                units = semantic_units(block.source_family, block_message(block.raw_block))
                locator_block = {
                    "line_number": block.line_number,
                    "raw_block_sha256": block.raw_block_sha256,
                    "semantic_unit_count": len(units),
                    "token_sequences": [list(tokenize(unit)) for unit in units],
                    "typed_locator_present": any("<LOCATOR>" in tokenize(unit) for unit in units),
                }
                break
        if locator_block is None:
            raise RuntimeError("authentic locator calibration block not found")
        report = {
            "schema": "ck3chronicle.phase1-harness-calibration",
            "schema_version": 1,
            "classification": "public_non_scoring_calibration",
            "synthetic_fixture": True,
            "product_gate_execution": False,
            "private_material_accessed": False,
            "expected_answer_accessed": False,
            "interfaces": {
                "iter_log_blocks": {
                    "block_count": len(blocks),
                    "field_names": sorted(name for name in vars(blocks[0])) if blocks else [],
                    "module": iter_log_blocks.__module__,
                },
                "spool_logs": {
                    "files_copied": pending.files_copied,
                    "file_names": list(pending.file_names),
                    "published_pending_directory": pending.dest_dir.is_dir(),
                    "module": spool_logs.__module__,
                },
                "approved_classifier": {
                    "model_revision_id": classifier.model.revision_id,
                    "model_sha256": classifier.model.sha256,
                    "module": load_approved_classifier.__module__,
                },
                "authentic_absolute_locator": locator_block,
            },
        }
        Path(args.output).write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    finally:
        shutil.rmtree(temporary, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
