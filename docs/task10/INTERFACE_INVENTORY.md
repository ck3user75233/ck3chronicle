# Entry-point classification inventory

Task 10D / TREK-11, refreshed 2026-10-12 for reference edition 10D-r2.
Supporting coverage evidence, not a progress tracker.
Application 0.0.3 / C10; the 106-module classification below is unchanged from
the received C9 inventory. No entry point or configuration surface changed in
the received cache/help/version replacement. Exact pins and per-command evidence are in
[DOCUMENTATION_HANDOFF.md](DOCUMENTATION_HANDOFF.md).

The application registers three console scripts: `ck3chronicle`,
`ck3chronicle-model-release`, `ck3chronicle-learner-release`. The C10 outer bundle
adds their `.cmd` launchers plus `Setup.cmd`, `Setup-Text.cmd`, `Start.cmd`,
`Verify.cmd`. Their complete public subcommands are in the coverage table.

The table accounts for every AST-discovered `__main__` module in current src/,
tools/ and packaging/windows/. Producer reference and docs/RELEASES.md establish
the supported aliases. Packaging a research module does not turn it into a
supported user control. The decoder module is a developer read-only inspection
utility; it is not a fourth registered product entry point.

| Module | Classification / reference |
|---|---|
| `src/ck3chronicle/cli.py` | Supported application CLI; CLI_REFERENCE |
| `src/ck3chronicle/decoder.py` | Developer inspection/research/verification utility; not supported product CLI |
| `src/ck3chronicle/pipeline/catalog.py` | Supported model admin; RELEASE_REFERENCE |
| `src/ck3chronicle/pipeline/database_handler.py` | Internal handler child transport; no user CLI |
| `tools/build_reporting_examples.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/check_decoder_corrective.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/check_reporting_io.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/check_reporting_locator_fixture.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/check_reporting_syntax_archives.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/check_runtime_logging.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/check_shared_decoder.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/check_source_recursion.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/export_active_code.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/analyze_removed_templates.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/analyze_script_system_layers.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/audit_coupled_word_inference.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/audit_key_bindings.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/audit_source_scope.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/blind_review/compare_blind_adjudication.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/build_review_pack.py` | Immutable operation via retained run only; direct mutable module is developer utility |
| `tools/template_learning/build_visual_review.py` | Immutable operation via retained run only; direct mutable module is developer utility |
| `tools/template_learning/check_character_dates.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/check_installed_combination.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/check_locator_presence.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/compare_build_history.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/compare_production_candidate.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/compare_training_corpus.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/evaluate_character_dates.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/evaluate_raw_lexers.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/evaluate_unseen_session.py` | Supported evaluation alias; RELEASE_REFERENCE |
| `tools/template_learning/evidence.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/evidence_serialization.py` | Supported data inspection; RELEASE_REFERENCE |
| `tools/template_learning/incremental_template_registry.py` | Immutable operation via retained run only; direct mutable module is developer utility |
| `tools/template_learning/inspect_accumulated_corpus.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inspect_candidate_revision.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inspect_compound_identifiers.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inspect_cross_emission_recovery.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inspect_incremental_learning.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inspect_message_recovery.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inspect_name_capture_changes.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inspect_native_learner.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inspect_outer_diagnostics.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inspect_raw_parse.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inspect_symbol_locations.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inspect_training_overlaps.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inventory_character_dates.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/inventory_location_markers.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/investigate_effect_regression.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/investigate_message_location_variability.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/investigate_production_candidate.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/investigate_quoted_similarity.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/investigate_script_location_stacks.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/learn_error_templates.py` | Immutable operation via retained run only; direct mutable module is developer utility |
| `tools/template_learning/learner_loader.py` | Supported Learner admin; RELEASE_REFERENCE |
| `tools/template_learning/location_candidate_experiment.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/matcher_example.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/measure_serialization_memory.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/mine_symbol_suffixes.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/mirror_incremental_build.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/publish_native_model.py` | Immutable operation via retained run only; direct mutable module is developer utility |
| `tools/template_learning/recover_large_candidate_export.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/release_evaluation.py` | Immutable operation via retained run only; direct mutable module is developer utility |
| `tools/template_learning/report_build_history.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_character_dates.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_character_location.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_effect_regression.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_formatted_references.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_function_words.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_gap_candidate.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_literal_corrections.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_locator_candidate_changes.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_locator_presence.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_message_location_variability.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_owner_recommendations.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_production_comparison.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_production_semantics.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_receiver_location_boundaries.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_removed_templates.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_script_location_stacks.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/report_short_thresholds.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/review_adjacent_field_families.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/review_assignment_changes.py` | Immutable operation via retained run only; direct mutable module is developer utility |
| `tools/template_learning/review_continuation_location_overlap.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/review_history_inference.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/review_presence_slots.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/review_short_thresholds.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/review_unselected_removals.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/survey_category_word_contexts.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/survey_compound_identifiers.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/survey_continuations.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/trace_reviewed_inference.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/verify_formatted_references.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/verify_full_corpus_storage.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/verify_gap_candidate.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/verify_literal_corrections.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/verify_location_candidate.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/verify_matcher_package.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/verify_owner_fields.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/verify_parser_correspondence.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/verify_quoted_discovery.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/verify_refinement_lineage.py` | Developer inspection/research/verification utility; not supported product CLI |
| `tools/template_learning/verify_shared_matcher.py` | Developer inspection/research/verification utility; not supported product CLI |
| `packaging/windows/build.py` | Distribution build/setup implementation; supported front doors are CMD files |
| `packaging/windows/external_check.py` | Distribution build/setup implementation; supported front doors are CMD files |
| `packaging/windows/launcher.py` | Distribution build/setup implementation; supported front doors are CMD files |
| `packaging/windows/setup_gui_backend.py` | Distribution build/setup implementation; supported front doors are CMD files |

Retained `learners/releases/*/launcher.py` and payload modules are immutable
implementation resources selected through `run --release`; old release operation
capabilities vary. Retained model executables likewise run through selected
packages. Private `_execute` protocols and the database-handler child protocol
are internal. Removed providers/Observer are not revived by this inventory.

Shell/JavaScript tools under tools/work_state are developer coordination utilities.
packaging/windows build/fetch/place/verify scripts are distribution-maintainer or
owner acceptance helpers; the shipped CMD front doors are the user interface.
Runtime Python, DLLs, rg.exe and third-party scripts are implementation dependencies,
not independently versioned CK3Chronicle commands.

Configuration-file families: selected runtime TOML and report query/context JSON
are editable; examples/reporting checks.json and delivery-status.json are developer
verification definitions. pyproject.toml, work_state package manifests and
packaging/windows/upstream-inputs.json are build/developer inputs. Shipped and
source catalogs/selections are release inventory/default resources changed through
registration/setup, not arbitrary runtime JSON knobs. Retained/candidate model,
parser, rule and manifest files are authenticated immutable artifacts; generated
registry/capture/playset/database/review/journal state belongs to its owning writer.
config.example.toml is a development example, not an implicit installed bootstrap.
See CONFIGURATION_REFERENCE.md for user-editable field coverage.
