"""Execute one fixed public case and emit neutral declared observations."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import re
import shutil
import sqlite3
from pathlib import Path
from typing import Any

from candidate_runtime import (
    canonical_distribution_export,
    chronological_times,
    direct_capture_process,
    finalize_and_register_without_derivation,
    independent_lexical_scan,
    invoke_cli,
    invoke_direct_with_capture,
    jsonable,
    product_lexical_scan,
    table_projection,
)
from harness_core import (
    SCORER_ONLY_RELATIVE_PATH,
    canonical_json_bytes,
    corpus_unit_map,
    file_identity,
    nofollow_tree_entries,
    sha256_file,
    stage_unit,
    tree_identities,
    write_canonical_json,
)
from mutations import apply_mutation, sha256_bytes


# Deliberately explicit: dry-run imports this inventory and rejects any plan
# recipe that is not backed by an executable worker branch.
SUPPORTED_RECIPES = frozenset({
    "capture_abort_mid", "capture_abort_pre", "capture_archive_integrity",
    "capture_crash_absent", "capture_crash_captured", "capture_duplicate",
    "capture_exception_integrity", "capture_finalize_fault",
    "capture_missing_error", "capture_registration_fault",
    "capture_stale_crash", "capture_zero_error",
    "runtime_complete", "runtime_inventory_metadata", "runtime_mount_forms",
    "runtime_state_absent", "runtime_state_ambiguous", "runtime_state_complete",
    "runtime_state_malformed", "runtime_state_partial", "runtime_state_truncated",
    "runtime_swap_order",
    "parse_classification_contract", "parse_database_audit", "parse_duplicates",
    "parse_exact_blocks", "parse_first_failure", "parse_locator_root",
    "parse_near_misses", "parse_reparse_rollback", "parse_robustness_encoding",
    "parse_robustness_long_line", "parse_robustness_malformed",
    "parse_robustness_newline", "parse_robustness_replacement_character",
    "parse_robustness_truncation", "parse_semantic_252", "parse_zero",
    "report_determinism", "report_four_run_chronology",
    "report_processing_envelope", "report_readonly", "report_stored_only",
    "report_taxonomy_archive", "report_taxonomy_database",
    "report_taxonomy_model", "report_taxonomy_pipeline",
    "report_taxonomy_readiness", "report_taxonomy_success", "report_text_json",
    "mutation_archive_integrity_fault", "mutation_inventory_metadata",
    "mutation_locator_path", "mutation_newline_variant",
    "mutation_remove_error_log", "mutation_runtime_absent",
    "mutation_runtime_malformed", "mutation_semantic_literal",
    "mutation_swap_mount_order", "mutation_truncated_tail",
    "mutation_zero_error_log",
    "perf_lexical", "perf_parse", "perf_pipeline", "perf_report_errors_json",
    "perf_report_errors_text", "perf_report_function", "perf_report_latest_json",
    "perf_report_latest_text", "perf_report_report_json",
    "perf_report_report_text", "perf_runtime",
    "private_placeholder",
})


def _evidence(scratch: Path, name: str) -> Path:
    root = scratch / name / "local" / "ck3chronicle"
    root.mkdir(parents=True, exist_ok=False)
    return root


def _stage_logs(corpus: Path, unit: str, scratch: Path, name: str) -> tuple[Path, dict[str, Any]]:
    destination = scratch / "staged" / name
    return destination, stage_unit(corpus, unit, destination)


def _stage_all(corpus: Path, unit: str, scratch: Path, name: str) -> tuple[Path, dict[str, Any]]:
    destination = scratch / "staged" / name
    return destination, stage_unit(corpus, unit, destination, include_all=True)


def _database_session_id(evidence: Path, newest: bool = True) -> int:
    conn = sqlite3.connect(evidence / "ck3chronicle.db")
    try:
        order = "DESC" if newest else "ASC"
        row = conn.execute(f"SELECT session_id FROM sessions ORDER BY session_id {order} LIMIT 1").fetchone()
        if row is None:
            raise RuntimeError("no registered session")
        return int(row[0])
    finally:
        conn.close()


def _runtime_observe(logs: Path, evidence: Path) -> dict[str, Any]:
    from ck3chronicle.db import repository
    from ck3chronicle.runtime_context import parse_runtime_context

    preparation = finalize_and_register_without_derivation(logs, evidence)
    session_id = _database_session_id(evidence)
    conn = repository.open_db(evidence / "ck3chronicle.db")
    try:
        result = parse_runtime_context(conn, evidence, session_id)
        stored = {
            "context": dict(repository.get_runtime_context(conn, session_id) or {}),
            "dlcs": [dict(row) for row in repository.get_mounted_dlcs(conn, session_id)],
            "mods": [dict(row) for row in repository.get_mounted_mods(conn, session_id)],
        }
    finally:
        conn.close()
    return {"preparation": preparation, "session_id": session_id, "result": jsonable(result), "stored": stored, "database": table_projection(evidence / "ck3chronicle.db")}


def _normal_process(corpus: Path, unit: str, scratch: Path, name: str) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    logs, staged = _stage_logs(corpus, unit, scratch, f"{name}-logs")
    evidence = _evidence(scratch, name)
    process = direct_capture_process(
        logs_root=logs,
        evidence_root=evidence,
        termination_kind="normal",
        observed_started_at="2026-08-16T00:00:00+00:00",
        observed_ended_at="2026-08-16T00:10:00+00:00",
    )
    return evidence, staged, process


def _crash_descriptor(package: Path) -> dict[str, Any]:
    return {
        "folder_name": package.name,
        "folder_path": str(package),
        "detected_at": "2026-08-16T00:09:59+00:00",
        "association_method": "exact_observed_run_window",
        "confidence": "high",
    }


def _mutate_first_archive_byte(evidence: Path, mutation_id: str) -> dict[str, Any]:
    sessions = sorted((evidence / "sessions").iterdir())
    if len(sessions) != 1:
        raise ValueError(f"{mutation_id}: expected exactly one archive")
    target = sessions[0] / "error.log"
    base = target.read_bytes()
    if not base:
        raise ValueError(f"{mutation_id}: archive error.log is empty")
    replacement = bytes([base[0] ^ 1])
    derived = replacement + base[1:]
    target.write_bytes(derived)
    return {
        "schema": "ck3chronicle.phase1-mutation-descriptor", "schema_version": 1,
        "mutation_id": mutation_id, "relative_path": target.relative_to(evidence).as_posix(),
        "base_bytes": len(base), "base_sha256": sha256_bytes(base),
        "derived_bytes": len(derived), "derived_sha256": sha256_bytes(derived),
        "application_count": 1,
        "edits": [{"base_start": 0, "base_end": 1, "derived_start": 0, "derived_end": 1, "before_hex": base[:1].hex(), "after_hex": replacement.hex()}],
        "protected_invariants": {"suffix_sha256": sha256_bytes(base[1:]), "suffix_equal": base[1:] == derived[1:]},
    }


def _capture_case(context: dict[str, Any]) -> dict[str, Any]:
    recipe = context["case"]["recipe"]
    corpus = Path(context["corpus_root"]); scratch = Path(context["scratch_root"])
    candidate = Path(context["candidate_root"]); python = Path(context["python_executable"]); declared = Path(context["declared_root"])

    if recipe.startswith("capture_crash_"):
        nominal, nominal_stage = _stage_logs(corpus, "PUB-NOMINAL-20260510", scratch, "nominal")
        crash, crash_stage = _stage_all(corpus, "PUB-CRASH-20260428", scratch, "crash-package")
        evidence = _evidence(scratch, "evidence")
        if recipe == "capture_crash_captured":
            logs = crash / "logs"; termination = "crash"; crash_info = _crash_descriptor(crash); preparation = None
        elif recipe == "capture_crash_absent":
            logs = nominal; termination = "crash"; crash_info = _crash_descriptor(crash)
            exception = crash / "exception.txt"; before = file_identity(exception, crash); exception.unlink()
            preparation = {"operation": "remove_exception_from_staged_crash_only", "identity": before, "application_count": 1}
        else:
            logs = nominal; termination = "normal"; crash_info = None
            preparation = {"stale_crash_package_present_but_unassociated": tree_identities(crash)}
        result = direct_capture_process(logs_root=logs, evidence_root=evidence, termination_kind=termination, observed_started_at="2026-08-16T00:00:00+00:00", observed_ended_at="2026-08-16T00:10:00+00:00", crash=crash_info)
        return {"staged": [nominal_stage, crash_stage], "preparation": preparation, "capture": result, "filesystem": tree_identities(evidence), "database": table_projection(evidence / "ck3chronicle.db")}

    if recipe == "capture_duplicate":
        logs_a, stage_a = _stage_logs(corpus, "PUB-NOMINAL-20260510", scratch, "logs-a")
        logs_b, stage_b = _stage_logs(corpus, "PUB-NOMINAL-20260510", scratch, "logs-b")
        evidence = _evidence(scratch, "evidence")
        from ck3chronicle.classification.catalog import load_approved_classifier
        from ck3chronicle.harvester import spool_logs
        from ck3chronicle.processing import process_pending
        from ck3chronicle.watcher import write_capture_receipt
        pendings = []
        for index, logs in enumerate((logs_a, logs_b)):
            pending = spool_logs(logs, evidence)
            write_capture_receipt(evidence, pending, trigger="phase1_public_runner", observed_started_at=f"2026-08-16T0{index}:00:00+00:00", observed_ended_at=f"2026-08-16T0{index}:10:00+00:00", termination_kind="normal")
            pendings.append(jsonable(pending))
        processed = process_pending(evidence, load_approved_classifier())
        return {"staged": [stage_a, stage_b], "pending": pendings, "processing": jsonable(processed), "database": table_projection(evidence / "ck3chronicle.db"), "filesystem": tree_identities(evidence)}

    if recipe in {"capture_archive_integrity", "capture_exception_integrity"}:
        if recipe == "capture_archive_integrity":
            evidence, staged, process = _normal_process(corpus, "PUB-NOMINAL-20260510", scratch, "baseline")
            mutation = _mutate_first_archive_byte(evidence, "capture_archive_integrity")
        else:
            crash, staged = _stage_all(corpus, "PUB-CRASH-20260428", scratch, "crash-package")
            evidence = _evidence(scratch, "baseline")
            process = direct_capture_process(logs_root=crash / "logs", evidence_root=evidence, termination_kind="crash", observed_started_at="2026-08-16T00:00:00+00:00", observed_ended_at="2026-08-16T00:10:00+00:00", crash=_crash_descriptor(crash))
            protected = next((evidence / "crash_evidence").rglob("exception.txt"))
            base = protected.read_bytes(); derived = bytes([base[0] ^ 1]) + base[1:]; protected.write_bytes(derived)
            mutation = {"schema": "ck3chronicle.phase1-mutation-descriptor", "schema_version": 1, "mutation_id": "capture_exception_integrity", "relative_path": protected.relative_to(evidence).as_posix(), "base_bytes": len(base), "base_sha256": sha256_bytes(base), "derived_bytes": len(derived), "derived_sha256": sha256_bytes(derived), "application_count": 1, "edits": [{"base_start": 0, "base_end": 1, "derived_start": 0, "derived_end": 1}], "protected_invariants": {"suffix_equal": base[1:] == derived[1:]}}
        transcript = invoke_cli(candidate_root=candidate, python_executable=python, evidence_root=evidence, argv=["process-pending", "--json"], declared_root=declared, transcript_id="strict-reconciliation")
        return {"staged": staged, "baseline": process, "mutation": mutation, "transcript": transcript, "database": table_projection(evidence / "ck3chronicle.db"), "filesystem": tree_identities(evidence)}

    if recipe in {"capture_abort_pre", "capture_abort_mid"}:
        logs, staged = _stage_logs(corpus, "PUB-NOMINAL-20260510", scratch, "logs")
        evidence = _evidence(scratch, "evidence")
        from ck3chronicle.harvester import spool_logs
        calls = 0
        def abort() -> bool:
            nonlocal calls
            calls += 1
            return True if recipe == "capture_abort_pre" else calls >= 2
        result = invoke_direct_with_capture(spool_logs, logs, evidence, abort_if=abort)
        return {"staged": staged, "abort_callback_calls": calls, "call": result, "filesystem": tree_identities(evidence)}

    if recipe in {"capture_finalize_fault", "capture_registration_fault"}:
        crash = None
        if recipe == "capture_registration_fault":
            crash, staged = _stage_all(corpus, "PUB-CRASH-20260428", scratch, "crash-package")
            logs = crash / "logs"
        else:
            logs, staged = _stage_logs(corpus, "PUB-NOMINAL-20260510", scratch, "logs")
        evidence = _evidence(scratch, "evidence")
        from ck3chronicle.classification.catalog import load_approved_classifier
        from ck3chronicle.harvester import spool_logs
        from ck3chronicle.processing import process_pending
        from ck3chronicle.watcher import write_capture_receipt
        import ck3chronicle.harvester as harvester
        import ck3chronicle.processing as processing
        pending = spool_logs(logs, evidence)
        write_capture_receipt(
            evidence,
            pending,
            trigger="phase1_cap05_fault",
            observed_started_at="2026-08-16T00:00:00+00:00",
            observed_ended_at="2026-08-16T00:10:00+00:00",
            termination_kind="crash" if crash is not None else "normal",
            crash=_crash_descriptor(crash) if crash is not None else None,
        )
        calls = 0
        if recipe == "capture_finalize_fault":
            original = harvester.os.rename
            def fault(source, target):
                nonlocal calls
                if Path(target).parent.name == "sessions":
                    calls += 1; raise RuntimeError("phase1 injected finalize publish fault")
                return original(source, target)
            harvester.os.rename = fault
            try: result = invoke_direct_with_capture(process_pending, evidence, load_approved_classifier())
            finally: harvester.os.rename = original
        else:
            original = processing.reconcile_archives
            def fault(*args, **kwargs):
                nonlocal calls
                calls += 1; raise RuntimeError("phase1 injected registration fault")
            processing.reconcile_archives = fault
            try: result = invoke_direct_with_capture(process_pending, evidence, load_approved_classifier())
            finally: processing.reconcile_archives = original
        recoverability_before = {
            "filesystem": tree_identities(evidence),
            "database": table_projection(evidence / "ck3chronicle.db"),
        }
        recovery = invoke_direct_with_capture(process_pending, evidence, load_approved_classifier())
        return {
            "staged": staged,
            "pending": jsonable(pending),
            "fault_calls": calls,
            "faulted_call": result,
            "recoverability_before_retry": recoverability_before,
            "recovery_call_after_fault_removed": recovery,
            "filesystem_after_recovery": tree_identities(evidence),
            "database_after_recovery": table_projection(evidence / "ck3chronicle.db"),
        }

    if recipe in {"capture_missing_error", "capture_zero_error"}:
        logs, staged = _stage_logs(corpus, "PUB-NOMINAL-20260510", scratch, "logs")
        mutation = apply_mutation("remove_error_log" if recipe.endswith("missing_error") else "zero_error_log", logs)
        evidence = _evidence(scratch, "evidence")
        report_projection = None
        if recipe.endswith("missing_error"):
            from ck3chronicle.harvester import spool_logs
            call = invoke_direct_with_capture(spool_logs, logs, evidence)
        else:
            call = invoke_direct_with_capture(direct_capture_process, logs_root=logs, evidence_root=evidence, termination_kind="normal", observed_started_at="2026-08-16T00:00:00+00:00", observed_ended_at="2026-08-16T00:10:00+00:00")
            from ck3chronicle.db import repository
            from ck3chronicle.reporting import build_session_report
            session_id = _database_session_id(evidence)
            conn = repository.open_db_readonly(evidence / "ck3chronicle.db")
            try:
                report_projection = invoke_direct_with_capture(build_session_report, conn, session_id)
            finally:
                conn.close()
        return {"staged": staged, "mutation": mutation, "call": call, "report_projection": report_projection, "filesystem": tree_identities(evidence), "database": table_projection(evidence / "ck3chronicle.db")}
    raise KeyError(recipe)


def _runtime_case(context: dict[str, Any]) -> dict[str, Any]:
    recipe = context["case"]["recipe"]
    corpus = Path(context["corpus_root"]); scratch = Path(context["scratch_root"])
    candidate = Path(context["candidate_root"]); python = Path(context["python_executable"]); declared = Path(context["declared_root"])
    if recipe in {"runtime_swap_order", "runtime_inventory_metadata"}:
        mutation_id = "swap_mount_order" if recipe == "runtime_swap_order" else "inventory_metadata"
        base_logs, base_stage = _stage_logs(corpus, "PUB-RUNTIME-COMPLETE-20260816", scratch, "base-logs")
        derived_logs, derived_stage = _stage_logs(corpus, "PUB-RUNTIME-COMPLETE-20260816", scratch, "derived-logs")
        mutation = apply_mutation(mutation_id, derived_logs)
        base = _runtime_observe(base_logs, _evidence(scratch, "base"))
        derived = _runtime_observe(derived_logs, _evidence(scratch, "derived"))
        return {"staged": [base_stage, derived_stage], "mutation": mutation, "base": base, "derived": derived}
    unit = "PUB-CRASH-20260428" if recipe == "runtime_state_partial" else "PUB-RUNTIME-COMPLETE-20260816"
    if unit == "PUB-CRASH-20260428":
        package, staged = _stage_all(corpus, unit, scratch, "package"); logs = package / "logs"
    else:
        logs, staged = _stage_logs(corpus, unit, scratch, "logs")
    mutation = None
    mutation_for = {
        "runtime_state_absent": "runtime_state_absent",
        "runtime_state_malformed": "runtime_state_malformed",
        "runtime_state_truncated": "runtime_state_truncated",
        "runtime_state_ambiguous": "runtime_state_ambiguous",
    }
    if recipe in mutation_for:
        mutation = apply_mutation(mutation_for[recipe], logs)
    evidence = _evidence(scratch, "evidence")
    observed = _runtime_observe(logs, evidence)
    transcript = invoke_cli(candidate_root=candidate, python_executable=python, evidence_root=evidence, argv=["context", "--session", str(observed["session_id"]), "--json"], declared_root=declared, transcript_id="context-json")
    return {"staged": staged, "mutation": mutation, "observation": observed, "transcript": transcript}


def _semantic_252(context: dict[str, Any]) -> dict[str, Any]:
    corpus = Path(context["corpus_root"]); scratch = Path(context["scratch_root"]); declared = Path(context["declared_root"])
    reference, ref_stage = _stage_logs(corpus, "DEV-REF-63E97B", scratch, "reference")
    semantic, sem_stage = _stage_all(corpus, "DEV-SEMANTIC-252", scratch, "semantic-sample")
    if (semantic / "SEMANTIC_LABELS_ADJUDICATED.json").exists():
        raise RuntimeError("scorer-only answer file was staged")
    sample_path = semantic / "SEMANTIC_CALIBRATION_SAMPLE_CANDIDATE.json"
    sample = json.loads(sample_path.read_text(encoding="utf-8"))
    rows = sample.get("samples") or sample.get("items")
    if not isinstance(rows, list):
        raise ValueError("semantic sample has no row array")
    ids = [row.get("sample_id") for row in rows]; indices = [row.get("manifest_block_index") for row in rows]
    linked_source_hash = ((sample.get("provenance") or {}).get("source_sha256"))
    if (
        sha256_file(sample_path) != "f19a7aa858a14ee62371fa3721fc3c95288b9473c54d487c1608a55fe0480061"
        or sample.get("schema") != "ck3chronicle.reference.semantic_calibration_sample"
        or sample.get("schema_version") != 1
        or sample.get("curation_status") != "candidate_unlabeled"
        or sample.get("semantic_labels_present") is not False
        or len(rows) != 252
        or len(set(ids)) != 252
        or len(set(indices)) != 252
        or linked_source_hash != "675216ebb2dbcd8b24bc0bb15474616826c923781be463ea22a9a5da1042b2bf"
        or sha256_file(reference / "error.log") != linked_source_hash
    ):
        raise ValueError("semantic 252 sample identity/schema/linkage precondition failed")
    sample_proof = {"identity": file_identity(sample_path), "schema": sample.get("schema"), "schema_version": sample.get("schema_version"), "curation_status": sample.get("curation_status"), "semantic_labels_present": sample.get("semantic_labels_present"), "linked_source_sha256": linked_source_hash, "row_count": len(rows), "unique_sample_ids": len(set(ids)), "unique_manifest_block_indices": len(set(indices)), "scorer_only_staged": False}
    scan = independent_lexical_scan(reference / "error.log")
    blocks = {int(row["block_index"]): row for row in scan["records"] if row["kind"] == "timestamped"}
    for row in rows:
        block = blocks.get(int(row["manifest_block_index"]))
        if block is None or block["raw_block_sha256"] != row["raw_sha256"]:
            raise ValueError(f"semantic independent join precondition failed: {row.get('sample_id')}")
    evidence = _evidence(scratch, "evidence")
    process = direct_capture_process(logs_root=reference, evidence_root=evidence, termination_kind="normal", observed_started_at="2026-08-16T00:00:00+00:00", observed_ended_at="2026-08-16T00:10:00+00:00")
    session_id = _database_session_id(evidence)
    conn = sqlite3.connect(evidence / "ck3chronicle.db"); conn.row_factory = sqlite3.Row
    output: list[dict[str, Any]] = []
    try:
        for row in rows:
            block = blocks[int(row["manifest_block_index"])]
            at_line = conn.execute(
                "SELECT sb.source_block_pk,sb.start_line,sb.end_line,sb.issue_count,rb.raw_block_sha256,rb.raw_byte_length "
                "FROM source_blocks sb JOIN raw_block_contents rb ON rb.raw_block_pk=sb.raw_block_pk "
                "WHERE sb.session_id=? AND sb.start_line=? ORDER BY sb.source_block_pk",
                (session_id, int(block["start_line"])),
            ).fetchall()
            exact = conn.execute(
                "SELECT sb.source_block_pk,sb.start_line,sb.end_line,sb.issue_count,rb.raw_block_sha256,rb.raw_byte_length "
                "FROM source_blocks sb JOIN raw_block_contents rb ON rb.raw_block_pk=sb.raw_block_pk "
                "WHERE sb.session_id=? AND sb.start_line=? AND rb.raw_block_sha256=? ORDER BY sb.source_block_pk",
                (session_id, int(block["start_line"]), block["raw_block_sha256"]),
            ).fetchall()
            stored = exact[0] if len(exact) == 1 and len(at_line) == 1 else None
            issues = []
            if stored is not None:
                for issue in conn.execute("SELECT io.issue_ordinal,io.source_block_pk,io.log_relpath,io.line_number,i.signature,i.category,i.error_type,i.severity,i.confidence,i.primary_file,i.primary_line,i.referenced_symbols_json,i.referenced_objects_json FROM issue_occurrences io JOIN issues i ON i.session_id=io.session_id AND i.signature=io.signature WHERE io.session_id=? AND io.source_block_pk=? ORDER BY io.issue_ordinal", (session_id, int(stored["source_block_pk"]))):
                    item = dict(issue); item["referenced_symbols"] = json.loads(item.pop("referenced_symbols_json")); item["referenced_objects"] = json.loads(item.pop("referenced_objects_json")); issues.append(item)
            output.append({"sample_id": row["sample_id"], "manifest_block_index": row["manifest_block_index"], "independent_raw_sha256": block["raw_block_sha256"], "independent_start_line": block["start_line"], "candidate_join_status": "matched_by_index_line_and_raw_hash" if stored is not None else "unmatched_or_duplicate", "candidate_rows_at_start_line": [dict(item) for item in at_line], "candidate_exact_hash_row_count": len(exact), "stored_source_block": dict(stored) if stored is not None else None, "candidate_issues": issues})
    finally:
        conn.close()
    output_path = declared / "semantic-252-candidate-observations.json"
    write_canonical_json(output_path, {"schema": "ck3chronicle.phase1-semantic-252-observation", "schema_version": 1, "rows": output})
    return {"staged": [ref_stage, sem_stage], "sample_proof": sample_proof, "independent_scan": {key: value for key, value in scan.items() if key != "records"}, "processing": process, "observation_artifact": file_identity(output_path, declared), "database": table_projection(evidence / "ck3chronicle.db")}


def _generic_first_message_mutation(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    match = re.search(rb"\]: ([A-Za-z]{4,})", data)
    if match is None:
        raise ValueError("no authentic message literal")
    start, end = match.start(1), match.end(1); before = data[start:end]; after = bytes([before[0] ^ 0x20]) + before[1:]
    derived = data[:start] + after + data[end:]; path.write_bytes(derived)
    return {"schema": "ck3chronicle.phase1-mutation-descriptor", "schema_version": 1, "mutation_id": "near_miss_literal", "relative_path": "error.log", "base_bytes": len(data), "base_sha256": sha256_bytes(data), "derived_bytes": len(derived), "derived_sha256": sha256_bytes(derived), "application_count": 1, "edits": [{"base_start": start, "base_end": end, "derived_start": start, "derived_end": end, "before_hex": before.hex(), "after_hex": after.hex()}], "protected_invariants": {"prefix_equal": data[:start] == derived[:start], "suffix_equal": data[end:] == derived[end:]}}


def _parse_case(context: dict[str, Any]) -> dict[str, Any]:
    recipe = context["case"]["recipe"]
    corpus = Path(context["corpus_root"]); scratch = Path(context["scratch_root"]); declared = Path(context["declared_root"])
    candidate = Path(context["candidate_root"]); python = Path(context["python_executable"])
    if recipe == "parse_semantic_252":
        return _semantic_252(context)
    if recipe == "parse_exact_blocks":
        logs, staged = _stage_logs(corpus, "DEV-REF-63E97B", scratch, "logs")
        independent = independent_lexical_scan(logs / "error.log", declared / "independent-lexical.ndjson.gz")
        product = product_lexical_scan(logs / "error.log", declared / "product-lexical.ndjson.gz")
        evidence = _evidence(scratch, "evidence"); process = direct_capture_process(logs_root=logs, evidence_root=evidence, termination_kind="normal", observed_started_at="2026-08-16T00:00:00+00:00", observed_ended_at="2026-08-16T00:10:00+00:00")
        distribution = canonical_distribution_export(evidence / "ck3chronicle.db", declared / "canonical-distribution.ndjson.gz")
        return {"staged": staged, "independent": independent, "product": product, "processing": process, "distribution": distribution, "database": table_projection(evidence / "ck3chronicle.db")}
    if recipe == "parse_duplicates":
        evidence, staged, process = _normal_process(corpus, "DEV-REF-63E97B", scratch, "evidence")
        conn = sqlite3.connect(evidence / "ck3chronicle.db"); conn.row_factory=sqlite3.Row
        groups = [dict(row) for row in conn.execute("SELECT rb.raw_block_sha256,COUNT(*) AS source_rows,COUNT(DISTINCT io.signature) AS signatures,COUNT(io.issue_occurrence_id) AS occurrences FROM source_blocks sb JOIN raw_block_contents rb ON rb.raw_block_pk=sb.raw_block_pk LEFT JOIN issue_occurrences io ON io.source_block_pk=sb.source_block_pk GROUP BY rb.raw_block_sha256 HAVING COUNT(*)>1 ORDER BY source_rows DESC,rb.raw_block_sha256 LIMIT 1000")]
        conn.close(); path=declared/"duplicate-groups.json"; write_canonical_json(path,{"groups":groups})
        return {"staged": staged, "processing": process, "groups": file_identity(path, declared), "database": table_projection(evidence / "ck3chronicle.db")}
    if recipe == "parse_locator_root":
        # All three assigned units are verified/staged; the authentic root comes
        # only from the prescribed PUB-LONG unit.
        ref, refstage = _stage_logs(corpus,"DEV-REF-63E97B",scratch,"reference")
        tmpl, tmplstage = _stage_logs(corpus,"DEV-TEMPLATE-B9D7",scratch,"template")
        base, basestage = _stage_logs(corpus,"PUB-LONG-20260429",scratch,"base")
        derived, derstage = _stage_logs(corpus,"PUB-LONG-20260429",scratch,"derived")
        mutation=apply_mutation("absolute_locator_root",derived)
        base_scan=independent_lexical_scan(base/"error.log"); selected_offset=int(mutation["selected_span"]["base_start"])
        selected=next(row for row in base_scan["records"] if row["kind"]=="timestamped" and int(row["start_byte"])<=selected_offset<int(row["end_byte"]))
        from ck3chronicle.classification.normalize import block_message, semantic_units, tokenize
        from ck3chronicle.parser.log_blocks import iter_log_blocks
        def token_observation(path: Path):
            block=next(item for item in iter_log_blocks(path,log_relpath="error.log") if item.line_number==selected["start_line"])
            message=block_message(block.raw_block); units=semantic_units(block.source_family,message)
            return {"line":block.line_number,"raw_sha256":block.raw_block_sha256,"units":[{"semantic":unit,"tokens":list(tokenize(unit))} for unit in units]}
        base_tokens=token_observation(base/"error.log"); derived_tokens=token_observation(derived/"error.log")
        if not any("<LOCATOR>" in row["tokens"] for row in base_tokens["units"]):
            raise ValueError("absolute-root mutation base is not already tokenized as <LOCATOR>")
        base_ev=_evidence(scratch,"base-evidence"); derived_ev=_evidence(scratch,"derived-evidence")
        base_result=direct_capture_process(logs_root=base,evidence_root=base_ev,termination_kind="normal",observed_started_at="2026-08-16T00:00:00+00:00",observed_ended_at="2026-08-16T00:10:00+00:00")
        derived_result=direct_capture_process(logs_root=derived,evidence_root=derived_ev,termination_kind="normal",observed_started_at="2026-08-16T00:00:00+00:00",observed_ended_at="2026-08-16T00:10:00+00:00")
        return {"staged":[refstage,tmplstage,basestage,derstage],"mutation":mutation,"selected_independent_block":selected,"base_tokens":base_tokens,"derived_tokens":derived_tokens,"base_processing":base_result,"derived_processing":derived_result,"base_database":table_projection(base_ev/"ck3chronicle.db"),"derived_database":table_projection(derived_ev/"ck3chronicle.db")}
    if recipe in {"parse_near_misses","parse_classification_contract"}:
        observations=[]
        for unit in ("DEV-REF-63E97B","DEV-TEMPLATE-B9D7"):
            base, stage1=_stage_logs(corpus,unit,scratch,f"{unit}-base")
            derived, stage2=_stage_logs(corpus,unit,scratch,f"{unit}-derived")
            mutation=_generic_first_message_mutation(derived/"error.log")
            base_ev=_evidence(scratch,f"{unit}-base-evidence"); der_ev=_evidence(scratch,f"{unit}-derived-evidence")
            base_result=direct_capture_process(logs_root=base,evidence_root=base_ev,termination_kind="normal",observed_started_at="2026-08-16T00:00:00+00:00",observed_ended_at="2026-08-16T00:10:00+00:00")
            der_result=direct_capture_process(logs_root=derived,evidence_root=der_ev,termination_kind="normal",observed_started_at="2026-08-16T00:00:00+00:00",observed_ended_at="2026-08-16T00:10:00+00:00")
            classify_commands = None
            if recipe == "parse_classification_contract":
                base_session = _database_session_id(base_ev); derived_session = _database_session_id(der_ev)
                classify_commands = {
                    "base": invoke_cli(candidate_root=candidate, python_executable=python, evidence_root=base_ev, argv=["classify", "--session", str(base_session), "--reclassify", "--json"], declared_root=declared, transcript_id=f"classify-{unit}-base"),
                    "derived": invoke_cli(candidate_root=candidate, python_executable=python, evidence_root=der_ev, argv=["classify", "--session", str(derived_session), "--reclassify", "--json"], declared_root=declared, transcript_id=f"classify-{unit}-derived"),
                }
            observations.append({"unit":unit,"staged":[stage1,stage2],"mutation":mutation,"base":base_result,"derived":der_result,"classify_json_commands":classify_commands,"base_db":table_projection(base_ev/"ck3chronicle.db"),"derived_db":table_projection(der_ev/"ck3chronicle.db")})
        return {"observations":observations}
    if recipe.startswith("parse_robustness_"):
        form=recipe.removeprefix("parse_robustness_"); unit="PUB-STRESS-20260806" if form=="long_line" else "PUB-NOMINAL-20260510"
        logs,staged=_stage_logs(corpus,unit,scratch,"logs"); mutation=apply_mutation(f"robustness_{form}",logs)
        independent=independent_lexical_scan(logs/"error.log",declared/"independent-derived.ndjson.gz")
        product=invoke_direct_with_capture(product_lexical_scan,logs/"error.log",declared/"product-derived.ndjson.gz")
        companion=None
        if form=="encoding": companion=invoke_direct_with_capture(product_lexical_scan,logs/"error.later-bom.log",declared/"product-later-bom.ndjson.gz")
        evidence=_evidence(scratch,"evidence"); processing=invoke_direct_with_capture(direct_capture_process,logs_root=logs,evidence_root=evidence,termination_kind="normal",observed_started_at="2026-08-16T00:00:00+00:00",observed_ended_at="2026-08-16T00:10:00+00:00")
        return {"staged":staged,"mutation":mutation,"independent":independent,"product":product,"later_bom_guard":companion,"processing":processing,"database":table_projection(evidence/"ck3chronicle.db")}
    if recipe in {"parse_reparse_rollback","parse_first_failure"}:
        logs,staged=_stage_logs(corpus,"PUB-NOMINAL-20260510",scratch,"logs"); evidence=_evidence(scratch,"evidence")
        from ck3chronicle.classification.catalog import load_approved_classifier
        from ck3chronicle.db import repository
        from ck3chronicle.parser.service import parse_session
        import ck3chronicle.db.repository as repository_module
        if recipe=="parse_reparse_rollback":
            baseline=direct_capture_process(logs_root=logs,evidence_root=evidence,termination_kind="normal",observed_started_at="2026-08-16T00:00:00+00:00",observed_ended_at="2026-08-16T00:10:00+00:00")
        else:
            baseline=finalize_and_register_without_derivation(logs,evidence)
        session_id=_database_session_id(evidence); before=table_projection(evidence/"ck3chronicle.db"); calls=0; original=repository_module.append_canonical_block
        def fault(*args,**kwargs):
            nonlocal calls
            calls+=1
            if calls==2: raise RuntimeError("phase1 injected parse replacement fault")
            return original(*args,**kwargs)
        repository_module.append_canonical_block=fault
        conn=repository.open_db(evidence/"ck3chronicle.db")
        try: call=invoke_direct_with_capture(parse_session,conn,evidence,session_id,reparse=(recipe=="parse_reparse_rollback"))
        finally: conn.close(); repository_module.append_canonical_block=original
        after=table_projection(evidence/"ck3chronicle.db")
        return {"staged":staged,"baseline":baseline,"fault_calls":calls,"call":call,"before":before,"after":after}
    if recipe=="parse_zero":
        logs,staged=_stage_logs(corpus,"PUB-NOMINAL-20260510",scratch,"logs"); mutation=apply_mutation("zero_error_log",logs); evidence=_evidence(scratch,"evidence"); process=direct_capture_process(logs_root=logs,evidence_root=evidence,termination_kind="normal",observed_started_at="2026-08-16T00:00:00+00:00",observed_ended_at="2026-08-16T00:10:00+00:00")
        return {"staged":staged,"mutation":mutation,"processing":process,"database":table_projection(evidence/"ck3chronicle.db")}
    if recipe=="parse_database_audit":
        unit=context["case"]["inputs"][0]; evidence,staged,process=_normal_process(corpus,unit,scratch,"evidence")
        before=sha256_file(evidence/"ck3chronicle.db")
        standard=invoke_cli(candidate_root=candidate,python_executable=python,evidence_root=evidence,argv=["audit-db","--json"],declared_root=declared,transcript_id="audit-standard")
        deep=invoke_cli(candidate_root=candidate,python_executable=python,evidence_root=evidence,argv=["audit-db","--deep","--json"],declared_root=declared,transcript_id="audit-deep")
        after=sha256_file(evidence/"ck3chronicle.db"); distribution=canonical_distribution_export(evidence/"ck3chronicle.db",declared/"audit-distribution.ndjson.gz")
        return {"staged":staged,"processing":process,"database_hash_before":before,"database_hash_after":after,"standard":standard,"deep":deep,"distribution":distribution}
    raise KeyError(recipe)


def _report_commands(candidate: Path, python: Path, evidence: Path, declared: Path, prefix: str, *, session_id: int | None=None, run_id: int | None=None) -> list[dict[str, Any]]:
    commands=[]
    target=["--run",str(run_id)] if run_id is not None else ["--session",str(session_id)] if session_id is not None else []
    specs=[("report-text",["report",*target]),("report-json",["report",*target,"--json"]),("latest-text",["latest"]),("latest-json",["latest","--json"]),("errors-text",["errors",*target]),("errors-json",["errors",*target,"--json"])]
    for name,argv in specs: commands.append(invoke_cli(candidate_root=candidate,python_executable=python,evidence_root=evidence,argv=argv,declared_root=declared,transcript_id=f"{prefix}-{name}"))
    return commands


def _report_case(context: dict[str, Any]) -> dict[str, Any]:
    recipe=context["case"]["recipe"]; corpus=Path(context["corpus_root"]); scratch=Path(context["scratch_root"]); declared=Path(context["declared_root"]); candidate=Path(context["candidate_root"]); python=Path(context["python_executable"])
    if recipe=="report_processing_envelope":
        logs,staged=_stage_logs(corpus,"PUB-NOMINAL-20260510",scratch,"logs"); evidence=_evidence(scratch,"evidence")
        from ck3chronicle.harvester import spool_logs
        pending=spool_logs(logs,evidence)
        transcript=invoke_cli(candidate_root=candidate,python_executable=python,evidence_root=evidence,argv=["process-pending","--json"],declared_root=declared,transcript_id="process-pending")
        return {"staged":staged,"pending":jsonable(pending),"transcript":transcript,"filesystem":tree_identities(evidence),"database":table_projection(evidence/"ck3chronicle.db")}
    if recipe in {"report_text_json","report_stored_only","report_readonly"}:
        evidence,staged,process=_normal_process(corpus,"PUB-NOMINAL-20260510",scratch,"evidence"); session_id=_database_session_id(evidence)
        conn=sqlite3.connect(evidence/"ck3chronicle.db"); run_id=int(conn.execute("SELECT observation_id FROM capture_observations ORDER BY observation_id DESC LIMIT 1").fetchone()[0]); conn.close()
        before_db=sha256_file(evidence/"ck3chronicle.db")
        archive_mutation=None
        before_removal_commands=None
        if recipe=="report_stored_only":
            before_removal_commands=_report_commands(candidate,python,evidence,declared,"report_stored_only-before",session_id=session_id)
            sessions=evidence/"sessions"; hidden=scratch/"raw-archive-unavailable"; before=tree_identities(sessions); os.rename(sessions,hidden); archive_mutation={"operation":"move_scratch_archive_out_of_evidence_root","application_count":1,"before":before,"moved_to":str(hidden)}
        if recipe=="report_readonly":
            specs=[("report-session-text",["report","--session",str(session_id)]),("report-session-json",["report","--session",str(session_id),"--json"]),("report-run-text",["report","--run",str(run_id)]),("report-run-json",["report","--run",str(run_id),"--json"]),("latest-text",["latest"]),("latest-json",["latest","--json"]),("errors-session-text",["errors","--session",str(session_id)]),("errors-session-json",["errors","--session",str(session_id),"--json"])]
            commands=[invoke_cli(candidate_root=candidate,python_executable=python,evidence_root=evidence,argv=argv,declared_root=declared,transcript_id=name) for name,argv in specs]
        else: commands=_report_commands(candidate,python,evidence,declared,recipe,session_id=session_id)
        after_db=sha256_file(evidence/"ck3chronicle.db")
        return {"staged":staged,"processing":process,"session_id":session_id,"run_id":run_id,"archive_mutation":archive_mutation,"before_removal_commands":before_removal_commands,"database_hash_before":before_db,"database_hash_after":after_db,"commands_after_removal":commands,"database":table_projection(evidence/"ck3chronicle.db")}
    if recipe=="report_determinism":
        evidence=_evidence(scratch,"evidence"); staged=[]
        from ck3chronicle.classification.catalog import load_approved_classifier
        from ck3chronicle.harvester import spool_logs
        from ck3chronicle.processing import process_pending
        from ck3chronicle.watcher import write_capture_receipt
        for index,unit in enumerate(("PUB-NOMINAL-20260510","PUB-LONG-20260429","PUB-LONG-20260430")):
            logs,stage=_stage_logs(corpus,unit,scratch,f"logs-{index}"); staged.append(stage); pending=spool_logs(logs,evidence); write_capture_receipt(evidence,pending,trigger="phase1_public_runner",observed_started_at=f"2026-08-16T0{index}:00:00+00:00",observed_ended_at=f"2026-08-16T0{index}:10:00+00:00",termination_kind="normal")
        first=jsonable(process_pending(evidence,load_approved_classifier())); first_db=table_projection(evidence/"ck3chronicle.db"); second=jsonable(process_pending(evidence,load_approved_classifier())); second_db=table_projection(evidence/"ck3chronicle.db")
        sid=_database_session_id(evidence); commands=_report_commands(candidate,python,evidence,declared,"determinism-a",session_id=sid)+_report_commands(candidate,python,evidence,declared,"determinism-b",session_id=sid)
        return {"staged":staged,"first_processing":first,"second_processing":second,"first_database":first_db,"second_database":second_db,"commands":commands}
    if recipe=="report_four_run_chronology":
        evidence=_evidence(scratch,"evidence"); times=chronological_times(); staged=[]
        from ck3chronicle.classification.catalog import load_approved_classifier
        from ck3chronicle.harvester import finalize_pending_captures,spool_logs
        from ck3chronicle.processing import process_pending
        from ck3chronicle.archive_registry import reconcile_archives
        from ck3chronicle.run_registry import reconcile_run_receipts
        from ck3chronicle.watcher import write_capture_receipt
        runtime_a,stage=_stage_logs(corpus,"PUB-RUNTIME-COMPLETE-20260816",scratch,"runtime-a"); staged.append(stage)
        runtime_b,stage=_stage_logs(corpus,"PUB-RUNTIME-COMPLETE-20260816",scratch,"runtime-b"); staged.append(stage)
        crash,stage=_stage_all(corpus,"PUB-CRASH-20260428",scratch,"crash"); staged.append(stage)
        captures=[]
        for label,logs,index,termination,crash_info in (("A",runtime_a,0,"normal",None),("B",runtime_b,1,"normal",None),("C",crash/"logs",2,"crash",_crash_descriptor(crash))):
            pending=spool_logs(logs,evidence); write_capture_receipt(evidence,pending,trigger=f"phase1_rep06_{label}",observed_started_at=times[index][0],observed_ended_at=times[index][1],termination_kind=termination,crash=crash_info); captures.append({"label":label,"capture_id":pending.dest_dir.name})
        processed_abc=jsonable(process_pending(evidence,load_approved_classifier()))
        nominal,stage=_stage_logs(corpus,"PUB-NOMINAL-20260510",scratch,"nominal-d"); staged.append(stage); pending=spool_logs(nominal,evidence); write_capture_receipt(evidence,pending,trigger="phase1_rep06_D",observed_started_at=times[3][0],observed_ended_at=times[3][1],termination_kind="normal"); captures.append({"label":"D","capture_id":pending.dest_dir.name})
        finalize_pending_captures(evidence); archive=jsonable(reconcile_archives(evidence,evidence/"ck3chronicle.db",strict_integrity=True)); runs=jsonable(reconcile_run_receipts(evidence,evidence/"ck3chronicle.db",strict_integrity=True))
        conn=sqlite3.connect(evidence/"ck3chronicle.db"); conn.row_factory=sqlite3.Row; run_rows=[dict(row) for row in conn.execute("SELECT * FROM capture_observations ORDER BY observed_ended_at,observation_id")]; sessions=[dict(row) for row in conn.execute("SELECT * FROM sessions ORDER BY session_id")]; conn.close()
        by_capture={row["capture_id"]:row for row in run_rows}; run_a=int(by_capture[captures[0]["capture_id"]]["observation_id"]); run_b=int(by_capture[captures[1]["capture_id"]]["observation_id"]); run_c=int(by_capture[captures[2]["capture_id"]]["observation_id"]); runtime_session=int(by_capture[captures[0]["capture_id"]]["session_id"])
        commands=[]
        for name,argv in (("report-run-a",["report","--run",str(run_a),"--json"]),("errors-run-a",["errors","--run",str(run_a),"--json"]),("report-run-b",["report","--run",str(run_b),"--json"]),("errors-run-b",["errors","--run",str(run_b),"--json"]),("report-run-c",["report","--run",str(run_c),"--json"]),("errors-run-c",["errors","--run",str(run_c),"--json"]),("report-session-runtime",["report","--session",str(runtime_session),"--json"]),("latest",["latest","--json"])):
            commands.append(invoke_cli(candidate_root=candidate,python_executable=python,evidence_root=evidence,argv=argv,declared_root=declared,transcript_id=name))
        return {"staged":staged,"captures":captures,"processed_abc":processed_abc,"d_archive_reconciliation":archive,"d_run_reconciliation":runs,"run_rows":run_rows,"sessions":sessions,"commands":commands,"database":table_projection(evidence/"ck3chronicle.db"),"filesystem":tree_identities(evidence)}
    if recipe.startswith("report_taxonomy_"):
        taxonomy=recipe.removeprefix("report_taxonomy_"); logs,staged=_stage_logs(corpus,"PUB-NOMINAL-20260510",scratch,"logs"); evidence=_evidence(scratch,"evidence"); precondition:dict[str,Any]={}
        extra_path=None; runtime_candidate=candidate
        if taxonomy=="success":
            from ck3chronicle.harvester import spool_logs
            pending=spool_logs(logs,evidence); precondition={"processable_pending":jsonable(pending)}; argv=["process-pending","--json"]
        elif taxonomy=="readiness":
            prep=finalize_and_register_without_derivation(logs,evidence); sid=_database_session_id(evidence); precondition={"finalized_unparsed_session":sid,"preparation":prep}; argv=["report","--session",str(sid),"--json"]
        elif taxonomy=="archive":
            crash,crashstage=_stage_all(corpus,"PUB-CRASH-20260428",scratch,"crash"); baseline=direct_capture_process(logs_root=crash/"logs",evidence_root=evidence,termination_kind="crash",observed_started_at="2026-08-16T00:00:00+00:00",observed_ended_at="2026-08-16T00:10:00+00:00",crash=_crash_descriptor(crash)); mutation=_mutate_first_archive_byte(evidence,"rep07_archive"); precondition={"registered_baseline":baseline,"mutation":mutation,"crash_stage":crashstage}; argv=["process-pending","--json"]
        elif taxonomy=="model":
            runtime=scratch/"candidate-runtime"; shutil.copytree(candidate/"src",runtime/"src"); shutil.copytree(candidate/"models",runtime/"models"); model=runtime/"models"/"93196794a7e0115d"/"empirical_template_model.json"; before=file_identity(model,runtime)
            if before["sha256"] != "3bd189b4c93ad260e925d1a1ac3ece7c79cc63217480b79a939f6f7f5d034db3": raise RuntimeError("copied approved model does not match candidate authority")
            data=model.read_bytes(); model.write_bytes(bytes([data[0]^1])+data[1:]); mutation={"base":before,"derived":file_identity(model,runtime),"application_count":1,"changed_span":[0,1],"nonchanged_suffix_equal":model.read_bytes()[1:]==data[1:]}; runtime_candidate=runtime
            from ck3chronicle.harvester import spool_logs
            pending=spool_logs(logs,evidence); precondition={"processable_pending":jsonable(pending),"runtime_copy_verified_before_mutation":before["sha256"]=="3bd189b4c93ad260e925d1a1ac3ece7c79cc63217480b79a939f6f7f5d034db3","model_mutation":mutation}; argv=["process-pending","--json"]
        elif taxonomy=="database":
            db=evidence/"ck3chronicle.db"; db.write_bytes(b"not a sqlite database\x00phase1"); precondition={"existing_database":file_identity(db,evidence)}; argv=["process-pending","--json"]
        else:
            from ck3chronicle.harvester import spool_logs
            pending=spool_logs(logs,evidence); hook=scratch/"pipeline-hook"; hook.mkdir(); counter=scratch/"pipeline-count.txt"; site=hook/"sitecustomize.py"; site.write_text("import os\nimport ck3chronicle.processing as p\n_count=os.environ['PHASE1_PIPELINE_COUNTER']\ndef _boom(*a,**k):\n    with open(_count,'a',encoding='ascii') as f: f.write('1\\n')\n    raise RuntimeError('phase1 fixed pipeline injection')\np.process_pending=_boom\n",encoding="utf-8",newline="\n"); os.environ["PHASE1_PIPELINE_COUNTER"]=str(counter); extra_path=hook; precondition={"processable_pending":jsonable(pending),"hook_identity":file_identity(site,hook),"installed_before_invocation":True}; argv=["process-pending","--json"]
        transcript=invoke_cli(candidate_root=runtime_candidate,python_executable=python,evidence_root=evidence,argv=argv,declared_root=declared,transcript_id=f"taxonomy-{taxonomy}",extra_pythonpath=extra_path)
        if taxonomy=="pipeline": precondition["injection_reached_count"]=(scratch/"pipeline-count.txt").read_text(encoding="ascii").count("1\n") if (scratch/"pipeline-count.txt").exists() else 0
        return {"staged":staged,"taxonomy":taxonomy,"precondition":precondition,"transcript":transcript,"filesystem":tree_identities(evidence),"database":table_projection(evidence/"ck3chronicle.db")}
    raise KeyError(recipe)


def _mutation_case(context: dict[str, Any]) -> dict[str, Any]:
    variant=context["case"]["mutation"]; corpus=Path(context["corpus_root"]); scratch=Path(context["scratch_root"])
    unit=context["case"]["inputs"][0]
    if unit=="PUB-CRASH-20260428":
        package,staged=_stage_all(corpus,unit,scratch,"package"); base_logs=package/"logs"; derived_logs=scratch/"staged"/"derived"; shutil.copytree(base_logs,derived_logs)
    else:
        base_logs,staged=_stage_logs(corpus,unit,scratch,"base"); derived_logs=scratch/"staged"/"derived"; shutil.copytree(base_logs,derived_logs)
    if variant=="archive_integrity_fault":
        evidence=_evidence(scratch,"derived-evidence"); baseline=direct_capture_process(logs_root=derived_logs,evidence_root=evidence,termination_kind="normal",observed_started_at="2026-08-16T00:00:00+00:00",observed_ended_at="2026-08-16T00:10:00+00:00"); base={"processing":baseline,"database_before_mutation":table_projection(evidence/"ck3chronicle.db"),"filesystem_before_mutation":tree_identities(evidence)}; mutation=_mutate_first_archive_byte(evidence,"archive_integrity_fault")
        from ck3chronicle.classification.catalog import load_approved_classifier
        from ck3chronicle.processing import process_pending
        derived=invoke_direct_with_capture(process_pending,evidence,load_approved_classifier())
    else:
        mutation=apply_mutation(variant,derived_logs)
        if variant in {"swap_mount_order","runtime_absent","runtime_malformed","inventory_metadata"}:
            base=_runtime_observe(base_logs,_evidence(scratch,"base-evidence")); derived=_runtime_observe(derived_logs,_evidence(scratch,"derived-evidence"))
        elif variant=="remove_error_log":
            from ck3chronicle.harvester import spool_logs
            base=invoke_direct_with_capture(spool_logs,base_logs,_evidence(scratch,"base-evidence")); derived=invoke_direct_with_capture(spool_logs,derived_logs,_evidence(scratch,"derived-evidence"))
        else:
            base_ev=_evidence(scratch,"base-evidence"); der_ev=_evidence(scratch,"derived-evidence"); base=invoke_direct_with_capture(direct_capture_process,logs_root=base_logs,evidence_root=base_ev,termination_kind="normal",observed_started_at="2026-08-16T00:00:00+00:00",observed_ended_at="2026-08-16T00:10:00+00:00"); derived=invoke_direct_with_capture(direct_capture_process,logs_root=derived_logs,evidence_root=der_ev,termination_kind="normal",observed_started_at="2026-08-16T00:00:00+00:00",observed_ended_at="2026-08-16T00:10:00+00:00")
    return {"staged":staged,"variant":variant,"mutation":mutation,"base_observation":base,"derived_observation":derived}


def execute(context: dict[str, Any]) -> dict[str, Any]:
    recipe=context["case"]["recipe"]
    if recipe not in SUPPORTED_RECIPES:
        raise KeyError(f"recipe is absent from explicit worker inventory: {recipe}")
    if recipe=="private_placeholder": raise RuntimeError("P1-HOLD-01 is unassigned and cannot be executed")
    if recipe.startswith("capture_"): return _capture_case(context)
    if recipe.startswith("runtime_"): return _runtime_case(context)
    if recipe.startswith("parse_"): return _parse_case(context)
    if recipe.startswith("report_"): return _report_case(context)
    if recipe.startswith("mutation_"): return _mutation_case(context)
    if recipe.startswith("perf_"):
        from performance import execute_performance_case
        return execute_performance_case(context)
    raise KeyError(f"no recipe dispatch: {recipe}")


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--request",required=True); args=parser.parse_args()
    context=json.loads(Path(args.request).read_text(encoding="utf-8")); declared=Path(context["declared_root"]); declared.mkdir(parents=True,exist_ok=True)
    if context.get("harness_selftest_case_watchdog"):
        print("CASE_WATCHDOG_SELFTEST_PARTIAL_STDOUT",flush=True)
        child=subprocess.Popen([sys.executable,"-B",str(Path(context["harness_root"])/"perf_action.py"),"--selftest-descendant","child"])
        print(json.dumps({"selftest_case_worker_pid":os.getpid(),"selftest_child_pid":child.pid},sort_keys=True),flush=True)
        time.sleep(120)
        return 0
    if context.get("harness_selftest_perf02_timeout"):
        from performance import _sample_action
        observation=_sample_action(context,{"action":"runtime","harness_selftest_sleep_tree":True,"sleep_seconds":120},"warmup")
    else:
        try:
            observation=execute(context)
        except Exception as error:
            timeout_records=[]
            for path,kind in nofollow_tree_entries(declared):
                if kind!="file" or path.suffix!=".json":
                    continue
                try:
                    payload=json.loads(path.read_text(encoding="utf-8"))
                except (OSError,UnicodeDecodeError,json.JSONDecodeError):
                    continue
                if isinstance(payload,dict) and (payload.get("timed_out") is True or payload.get("output_limit_exceeded") is True):
                    timeout_records.append({"path":path.relative_to(declared).as_posix(),"payload":payload})
            if not timeout_records:
                raise
            observation={"status":"product_subprocess_bounded_termination_observed","classification":"neutral_observation_no_harness_gate_verdict","timeout_records":timeout_records,"post_timeout_exception":{"type":f"{type(error).__module__}.{type(error).__qualname__}","message":str(error)},"retry_performed":False,"harness_pass_fail_categorization":None}
    def contains_timeout(value: Any) -> bool:
        if isinstance(value,dict):
            return value.get("timed_out") is True or value.get("timeout_observed") is True or any(contains_timeout(item) for item in value.values())
        if isinstance(value,list):
            return any(contains_timeout(item) for item in value)
        return False
    def contains_output_limit(value: Any) -> bool:
        if isinstance(value,dict):
            return value.get("output_limit_exceeded") is True or value.get("output_limit_observed") is True or any(contains_output_limit(item) for item in value.values())
        if isinstance(value,list):
            return any(contains_output_limit(item) for item in value)
        return False
    result={"schema":"ck3chronicle.phase1-neutral-case-observation","schema_version":1,"case_id":context["case"]["case_id"],"gate":context["case"]["gate"],"recipe":context["case"]["recipe"],"observation":observation,"timeout_observed":contains_timeout(observation),"output_limit_observed":contains_output_limit(observation),"timeout_classification":"neutral_observation_no_harness_gate_verdict","expected_answers_embedded":False,"scorer_logic_embedded":False}
    write_canonical_json(declared/"observation.json",result)
    print(json.dumps({"case_id":context["case"]["case_id"],"observation_sha256":sha256_file(declared/"observation.json")},sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
