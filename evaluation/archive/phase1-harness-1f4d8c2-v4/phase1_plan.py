"""Frozen public execution inventory for candidate 1f4d8c2.

This module contains actions and observation requests only.  It deliberately
contains no expected product values, gate decisions, thresholds, or scorer
logic.
"""
from __future__ import annotations

from typing import Any

from timeouts import timeout_policy


PUBLIC_GATES = (
    *(f"P1-CAP-{index:02d}" for index in range(1, 7)),
    *(f"P1-RUN-{index:02d}" for index in range(1, 6)),
    *(f"P1-PAR-{index:02d}" for index in range(1, 12)),
    *(f"P1-REP-{index:02d}" for index in range(1, 8)),
    "P1-MUT-01",
    *(f"P1-PERF-{index:02d}" for index in range(1, 5)),
)
ALL_GATES = (*PUBLIC_GATES[:29], "P1-HOLD-01", *PUBLIC_GATES[29:])


def _case(
    case_id: str,
    gate: str,
    recipe: str,
    inputs: list[str],
    actions: list[str],
    observations: list[str],
    *,
    mutation: str | None = None,
    repetition_policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "gate": gate,
        "recipe": recipe,
        "inputs": inputs,
        "mutation": mutation,
        "actions": actions,
        "observations": observations,
        "repetition_policy": repetition_policy,
        "timeout_policy": timeout_policy(recipe, actions, private_placeholder=gate == "P1-HOLD-01"),
        "scoring": None,
    }


def build_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    add = cases.append

    # Capture: the split cases keep every lifecycle preparation isolated.
    for suffix, recipe, inputs in (
        ("captured-exception", "capture_crash_captured", ["PUB-NOMINAL-20260510", "PUB-CRASH-20260428"]),
        ("absent-exception", "capture_crash_absent", ["PUB-NOMINAL-20260510", "PUB-CRASH-20260428"]),
        ("stale-unassociated", "capture_stale_crash", ["PUB-NOMINAL-20260510", "PUB-CRASH-20260428"]),
    ):
        add(_case(f"cap01-{suffix}", "P1-CAP-01", recipe, inputs,
                  ["verify_assigned_units", "stage_authentic_logs", "spool_logs", "write_run_receipt", "process_pending", "observe_capture_state"],
                  ["pending_and_archive_paths", "protected_exception_identity", "run_receipts", "manifest", "database_projection", "processing_envelope", "evidence_hashes"]))
    add(_case("cap02-identical-resubmission", "P1-CAP-02", "capture_duplicate", ["PUB-NOMINAL-20260510"],
              ["verify_assigned_unit", "stage_two_exact_copies", "capture_a", "capture_b", "process_pending", "observe_deduplication"],
              ["bundle_identities", "session_rows", "run_rows", "registration_counters", "stdout_stderr_exit"]))
    for suffix, recipe, inputs in (
        ("archive-byte", "capture_archive_integrity", ["PUB-NOMINAL-20260510"]),
        ("protected-exception", "capture_exception_integrity", ["PUB-CRASH-20260428"]),
    ):
        add(_case(f"cap03-{suffix}", "P1-CAP-03", recipe, inputs,
                  ["verify_assigned_units", "create_registered_baseline", "apply_exact_integrity_mutation", "invoke_strict_reconciliation", "observe_integrity_state"],
                  ["mutation_descriptor", "manifest_verification", "artifact_verification", "command_bytes", "archive_index_projection"]))
    for suffix, recipe in (("precopy", "capture_abort_pre"), ("midcopy", "capture_abort_mid")):
        add(_case(f"cap04-{suffix}", "P1-CAP-04", recipe, ["PUB-NOMINAL-20260510"],
                  ["verify_assigned_unit", "stage_authentic_logs", "install_fixed_abort_signal", "spool_logs", "observe_publication_state"],
                  ["exception_or_exit", "pending_tree", "archive_tree", "receipt_tree", "input_hashes"]))
    for suffix, recipe, inputs in (
        ("publish-fault", "capture_finalize_fault", ["PUB-NOMINAL-20260510"]),
        ("registration-fault", "capture_registration_fault", ["PUB-CRASH-20260428"]),
    ):
        add(_case(f"cap05-{suffix}", "P1-CAP-05", recipe, inputs,
                  ["verify_assigned_units", "stage_and_spool", "install_single_fault_point", "invoke_processing", "remove_fault_point", "observe_recoverability"],
                  ["fault_counter", "archive_tree", "command_bytes", "database_projection", "recoverability_projection"]))
    for suffix, recipe in (("missing-error", "capture_missing_error"), ("zero-error", "capture_zero_error")):
        add(_case(f"cap06-{suffix}", "P1-CAP-06", recipe, ["PUB-NOMINAL-20260510"],
                  ["verify_assigned_unit", "derive_exact_input", "invoke_capture", "invoke_processing_if_available", "observe_completeness"],
                  ["mutation_descriptor", "exception_or_envelope", "stored_counters", "report_projection", "filesystem_projection"], mutation=suffix.replace("-", "_")))

    # Runtime context.
    add(_case("run01-complete", "P1-RUN-01", "runtime_complete", ["PUB-RUNTIME-COMPLETE-20260816"],
              ["verify_assigned_unit", "register_finalized_evidence", "parse_runtime_context", "invoke_context_json", "observe_runtime_tables"],
              ["status", "provenance", "counts", "ordered_dlcs", "ordered_mods", "warnings", "stored_projection"]))
    add(_case("run02-workshop-local", "P1-RUN-02", "runtime_mount_forms", ["PUB-RUNTIME-COMPLETE-20260816"],
              ["verify_assigned_unit", "register_finalized_evidence", "parse_runtime_context", "observe_mount_forms"],
              ["mod_key", "mount_path", "source_kind", "load_order", "runtime_provenance"]))
    add(_case("run03-order-swap", "P1-RUN-03", "runtime_swap_order", ["PUB-RUNTIME-COMPLETE-20260816"],
              ["verify_assigned_unit", "derive_two-line_swap", "process_base_and_derived", "observe_authoritative_sequences"],
              ["mutation_descriptor", "base_runtime_projection", "derived_runtime_projection", "database_hashes"], mutation="swap_mount_order"))
    for state in ("complete", "partial", "absent", "malformed", "truncated", "ambiguous"):
        inputs = ["PUB-RUNTIME-COMPLETE-20260816"] if state not in {"partial"} else ["PUB-CRASH-20260428"]
        add(_case(f"run04-{state}", "P1-RUN-04", f"runtime_state_{state}", inputs,
                  ["verify_assigned_unit", "derive_state_input_if_needed", "register_finalized_evidence", "parse_runtime_context", "observe_runtime_state"],
                  ["mutation_descriptor", "status", "termination_evidence", "absence_reason", "counts", "warnings", "ordered_mounts"],
                  mutation=None if state in {"complete", "partial"} else f"runtime_{state}"))
    add(_case("run05-inventory-separation", "P1-RUN-05", "runtime_inventory_metadata", ["PUB-RUNTIME-COMPLETE-20260816"],
              ["verify_assigned_unit", "derive_inventory_only_change", "process_base_and_derived", "observe_authority_and_enrichment"],
              ["mutation_descriptor", "authoritative_mounts", "inventory_enrichment", "resolver_roots", "provenance"], mutation="inventory_metadata"))

    # Parser, persistence, and semantic observations.
    add(_case("par01-exact-blocks", "P1-PAR-01", "parse_exact_blocks", ["DEV-REF-63E97B"],
              ["verify_assigned_unit", "independent_lexical_scan", "register_finalized_evidence", "parse_session", "export_exact_lexical_and_persisted_rows"],
              ["lexical_blocks_gzip", "source_block_projection_gzip", "parse_counters", "raw_reconstruction_hash", "database_hash"]))
    add(_case("par02-semantic-252", "P1-PAR-02", "parse_semantic_252", ["DEV-REF-63E97B", "DEV-SEMANTIC-252"],
              ["verify_reference_and_sample_only", "independently_recompute_block_indices_and_hashes", "register_and_parse_reference", "join_candidate_rows_by_index_and_raw_hash", "export_252_observations"],
              ["sample_identity_and_cardinality", "independent_join_keys", "candidate_issue_fields", "occurrence_source_linkage", "parse_counters"],
              mutation=None))
    add(_case("par03-duplicates", "P1-PAR-03", "parse_duplicates", ["DEV-REF-63E97B"],
              ["verify_assigned_unit", "register_and_parse", "export_duplicate_groups"],
              ["separate_source_occurrences", "shared_signatures", "per_block_counts", "per_signature_counts", "provenance"]))
    add(_case("par04-absolute-root", "P1-PAR-04", "parse_locator_root", ["DEV-REF-63E97B", "DEV-TEMPLATE-B9D7", "PUB-LONG-20260429"],
              ["verify_assigned_units", "pretokenize_authentic_absolute_locator", "derive_one_letter_root_change", "prove_protected_bytes_and_tokens", "classify_base_and_derived", "export_comparison"],
              ["mutation_descriptor", "token_proof", "canonical_fields", "classification_payloads", "raw_hashes"], mutation="absolute_locator_root"))
    add(_case("par05-near-misses", "P1-PAR-05", "parse_near_misses", ["DEV-REF-63E97B", "DEV-TEMPLATE-B9D7"],
              ["verify_assigned_units", "select_authentic_structural_units", "derive_fixed_near_miss_family", "classify_base_and_derived", "export_assignments"],
              ["mutation_descriptors", "normalized_tokens", "assignment_payloads", "model_identity"]))
    add(_case("par06-positive-negative", "P1-PAR-06", "parse_classification_contract", ["DEV-REF-63E97B", "DEV-TEMPLATE-B9D7"],
              ["verify_assigned_units", "register_parse_classify", "export_authentic_and_derived_assignment_rows", "invoke_classify_json"],
              ["assignment_level", "contract_id", "l1_template", "l2_template", "typed_slots", "model_identity", "aggregate_counts"]))
    for form in ("encoding", "newline", "long_line", "malformed", "replacement_character", "truncation"):
        inputs = ["PUB-STRESS-20260806"] if form == "long_line" else ["PUB-NOMINAL-20260510"]
        add(_case(f"par07-{form.replace('_', '-')}", "P1-PAR-07", f"parse_robustness_{form}", inputs,
                  ["verify_assigned_unit", "derive_exact_robustness_input", "independent_lexical_scan", "invoke_iter_log_blocks", "register_and_parse", "export_reconstruction_and_state"],
                  ["mutation_descriptor", "exact_byte_line_provenance", "raw_reconstruction_hash", "parse_counters_or_failure", "semantic_projection"], mutation=f"robustness_{form}"))
    add(_case("par08-reparse-rollback", "P1-PAR-08", "parse_reparse_rollback", ["PUB-NOMINAL-20260510"],
              ["verify_assigned_unit", "create_successful_parse", "hash_prior_projection", "install_single_reparse_fault", "invoke_reparse", "hash_final_projection"],
              ["fault_counter", "exception_or_exit", "prior_projection", "final_projection", "parse_state"]))
    add(_case("par09-first-parse-rollback", "P1-PAR-09", "parse_first_failure", ["PUB-NOMINAL-20260510"],
              ["verify_assigned_unit", "register_unparsed_session", "install_single_first_parse_fault", "invoke_parse", "observe_database_projection"],
              ["fault_counter", "exception_or_exit", "parse_state", "source_blocks", "occurrences", "issues"]))
    add(_case("par10-zero", "P1-PAR-10", "parse_zero", ["PUB-NOMINAL-20260510"],
              ["verify_assigned_unit", "derive_zero_error", "register_parse_classify", "build_session_report"],
              ["mutation_descriptor", "parse_result", "stored_state", "classification_counts", "report_projection"], mutation="zero_error_log"))
    for suffix, unit in (("reference", "DEV-REF-63E97B"), ("stress", "PUB-STRESS-20260806")):
        add(_case(f"par11-audit-{suffix}", "P1-PAR-11", "parse_database_audit", [unit],
                  ["verify_assigned_unit", "process_evidence", "hash_database_before", "invoke_standard_and_deep_audit", "hash_database_after", "export_aggregate_projection"],
                  ["audit_json", "database_hashes", "totals", "per_block_distribution", "per_signature_distribution", "provenance_invariants"]))

    # Reporting and command envelopes.
    add(_case("rep01-processing", "P1-REP-01", "report_processing_envelope", ["PUB-NOMINAL-20260510"],
              ["verify_assigned_unit", "stage_processable_pending", "invoke_process_pending_json", "observe_side_effects"],
              ["exact_stdout", "exact_stderr", "exit_code", "filesystem_projection", "database_projection"]))
    add(_case("rep02-text-json", "P1-REP-02", "report_text_json", ["PUB-NOMINAL-20260510"],
              ["verify_assigned_unit", "prepare_one_stored_target", "invoke_report_text_json", "invoke_latest_text_json", "invoke_errors_text_json"],
              ["command_transcripts", "stored_target_identity", "database_hashes"]))
    add(_case("rep03-stored-only", "P1-REP-03", "report_stored_only", ["PUB-NOMINAL-20260510"],
              ["verify_assigned_unit", "prepare_one_stored_target", "record_report_baseline", "make_raw_archive_unavailable", "invoke_all_report_surfaces"],
              ["archive_mutation_descriptor", "before_after_reports", "command_transcripts", "database_hashes"]))
    add(_case("rep04-readonly", "P1-REP-04", "report_readonly", ["PUB-NOMINAL-20260510"],
              ["verify_assigned_unit", "prepare_one_stored_target", "hash_storage", "invoke_eight_read_commands", "rehash_storage"],
              ["per_command_transcripts", "before_after_storage_hashes", "database_projection"]))
    add(_case("rep05-determinism", "P1-REP-05", "report_determinism", ["PUB-NOMINAL-20260510", "PUB-LONG-20260429", "PUB-LONG-20260430"],
              ["verify_assigned_units", "process_fixed_insertion_order", "invoke_repeat_processing", "capture_stored_projection", "invoke_repeat_reports"],
              ["processing_transcripts", "mutation_counters", "stored_projection_hashes", "json_bytes", "pattern_order"]))
    add(_case("rep06-four-run-chronology", "P1-REP-06", "report_four_run_chronology", ["PUB-RUNTIME-COMPLETE-20260816", "PUB-CRASH-20260428", "PUB-NOMINAL-20260510"],
              ["verify_assigned_units", "create_run_a_normal", "create_run_b_later_normal", "create_run_c_later_crash_with_exception", "create_run_d_newest_unparsed", "invoke_exact_run_session_and_latest_surfaces"],
              ["run_receipts", "capture_and_run_ids", "session_links", "command_transcripts", "crash_exception_projection", "principal_file_origins", "database_projection"]))
    for taxonomy in ("success", "readiness", "archive", "model", "database", "pipeline"):
        add(_case(f"rep07-{taxonomy}", "P1-REP-07", f"report_taxonomy_{taxonomy}", ["PUB-NOMINAL-20260510", "PUB-CRASH-20260428"] if taxonomy == "archive" else ["PUB-NOMINAL-20260510"],
                  ["verify_assigned_unit", f"prepare_{taxonomy}_condition", "verify_precondition", "invoke_one_json_command", "capture_exact_process_result"],
                  ["precondition_proof", "exact_stdout", "exact_stderr", "exit_code", "result_envelope", "filesystem_and_database_hashes"]))

    # Eleven individually closed input/metamorphic variants.
    mut_units = {
        "remove_error_log": "PUB-NOMINAL-20260510",
        "zero_error_log": "PUB-NOMINAL-20260510",
        "archive_integrity_fault": "PUB-CRASH-20260428",
        "newline_variant": "PUB-NOMINAL-20260510",
        "locator_path": "PUB-NOMINAL-20260510",
        "semantic_literal": "PUB-NOMINAL-20260510",
        "truncated_tail": "PUB-NOMINAL-20260510",
        "swap_mount_order": "PUB-RUNTIME-COMPLETE-20260816",
        "runtime_absent": "PUB-RUNTIME-COMPLETE-20260816",
        "runtime_malformed": "PUB-RUNTIME-COMPLETE-20260816",
        "inventory_metadata": "PUB-RUNTIME-COMPLETE-20260816",
    }
    for variant, unit in mut_units.items():
        add(_case(f"mut01-{variant.replace('_', '-')}", "P1-MUT-01", f"mutation_{variant}", [unit],
                  ["verify_assigned_unit", "derive_exact_variant", "verify_mutation_descriptor", "invoke_declared_product_seams", "export_base_and_derived_observations"],
                  ["mutation_descriptor", "precondition_proof", "base_observation", "derived_observation", "stdout_stderr_exit", "database_projection"], mutation=variant))

    # Each performance case is executed once; its one warmup and five measured
    # repetitions are prescribed actions, not retry behavior.
    repetitions = {"warmups": 1, "measured": 5, "retry": "forbidden"}
    add(_case("perf01-lexical", "P1-PERF-01", "perf_lexical", ["PUB-STRESS-20260806"],
              ["verify_assigned_unit", "prepare_outside_timed_region", "run_one_warmup", "run_five_measured", "export_metrics_and_logical_projections"],
              ["five_wall_cpu_rss_records", "lexical_counts", "projection_hashes", "host_identity"], repetition_policy=repetitions))
    add(_case("perf01-parse", "P1-PERF-01", "perf_parse", ["PUB-STRESS-20260806"],
              ["verify_assigned_unit", "prepare_six_isolated_registered_sessions", "run_one_warmup", "run_five_measured", "export_metrics_and_stored_projections"],
              ["five_wall_cpu_rss_records", "parse_counters", "projection_hashes", "host_identity"], repetition_policy=repetitions))
    add(_case("perf02-runtime", "P1-PERF-02", "perf_runtime", ["PUB-STRESS-20260806"],
              ["verify_assigned_unit", "prepare_six_isolated_registered_sessions", "run_one_warmup", "run_five_measured", "export_metrics_and_runtime_projections"],
              ["five_wall_cpu_rss_records", "runtime_projections", "projection_hashes", "host_identity"], repetition_policy=repetitions))
    for surface in ("function", "report_text", "report_json", "latest_text", "latest_json", "errors_text", "errors_json"):
        add(_case(f"perf03-{surface.replace('_', '-')}", "P1-PERF-03", f"perf_report_{surface}", ["PUB-STRESS-20260806"],
                  ["verify_assigned_unit", "prepare_one_stored_projection", "hash_storage", "run_one_warmup", "run_five_measured", "rehash_storage", "export_metrics"],
                  ["five_wall_cpu_rss_records", "command_or_function_outputs", "storage_hashes", "host_identity"], repetition_policy=repetitions))
    add(_case("perf04-pipeline", "P1-PERF-04", "perf_pipeline", ["PUB-STRESS-20260806"],
              ["verify_assigned_unit", "prepare_six_empty_isolated_roots", "run_one_copy_through_processing_warmup", "run_five_copy_through_processing_measurements", "export_metrics_and_results"],
              ["five_wall_cpu_rss_records", "processing_envelopes", "logical_projection_hashes", "host_identity"], repetition_policy=repetitions))

    # The private release gate is deliberately a non-runnable placeholder.
    add(_case("hold01-unassigned", "P1-HOLD-01", "private_placeholder", ["PRIVATE-HOLDOUT-UNASSIGNED"],
              [], ["unassigned_unexecuted_placeholder"]))
    return cases


def build_plan() -> dict[str, Any]:
    cases = build_cases()
    return {
        "schema": "ck3chronicle.phase1-public-run-plan",
        "schema_version": 1,
        "candidate_commit": "1f4d8c2f5a6e3ec1c5dc7a5324b0bbe4c4b233ac",
        "candidate_tree": "23762ebaa55dba79b448052980c03c5a1c325f14",
        "corpus_manifest_sha256": "407e47d12bc17f30e2abd453dc69c4dda0b4e3fab705e2e361e6d26a8e6a6147",
        "corpus_source_set_sha256": "f4b95276058f5b4f379de6e443e585b6fe8040ed3202b8f886e91c44a4f60c51",
        "gate_count": len(ALL_GATES),
        "public_gate_count": len(PUBLIC_GATES),
        "private_placeholder_count": 1,
        "cases": cases,
    }
