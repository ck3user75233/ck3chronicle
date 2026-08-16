"""Independent Phase 1 public-evaluation harness command line."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from harness_core import (
    CASE_COMPLETION_MARKER,
    RESULT_COMPLETION_MARKER,
    CANDIDATE_COMMIT,
    CANDIDATE_MANIFEST_SHA256,
    CANDIDATE_SOURCE_SET_SHA256,
    CANDIDATE_TREE,
    CORPUS_MANIFEST_SHA256,
    CORPUS_SOURCE_SET_SHA256,
    HARNESS_SCHEMA,
    SCORER_ONLY_RELATIVE_PATH,
    append_journal,
    assert_isolated_paths,
    canonical_json_bytes,
    close_case,
    close_result_set,
    file_identity,
    host_identity,
    initialize_results,
    new_scratch_directory,
    nofollow_tree_entries,
    path_is_linklike,
    read_json,
    sha256_file,
    source_set_hash,
    stage_unit,
    tree_identities,
    utc_now,
    verify_authorities,
    verify_result_set,
    write_canonical_json,
)
from mutations import apply_mutation
from phase1_plan import ALL_GATES, PUBLIC_GATES, build_plan
from case_worker import SUPPORTED_RECIPES
from process_control import run_bounded_process
from timeouts import timeout_policy, timeout_table


HARNESS_ROOT = Path(__file__).resolve().parent
DEFAULT_CANDIDATE = Path(r"C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3chronicle")
DEFAULT_CANDIDATE_MANIFEST = Path(r"C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3raven\.ck3raven\wip\ck3chronicle-phase1\candidate-1f4d8c2-v1\candidate.manifest.json")
DEFAULT_CORPUS = Path(r"C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3raven\.ck3raven\wip\ck3chronicle-phase1\locked-corpus-v2-public")
EVALUATOR_PYTHON = Path(r"C:\Users\nateb\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe")
POWERSHELL = Path(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe")
FAILED_V2_RESULTS = Path(r"C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3raven\.ck3raven\wip\ck3chronicle-phase1\public-results-1f4d8c2-v2")
FAILED_V2_RESULT_SET_SHA256 = "8445e80f972e21035be166d3aa05bde76abc9238590076605e4d5a365ce2fd93"
FAILED_V2_JOURNAL_SHA256 = "2d01ba35898710ff64abcf8afafb128f356582c8efc3763ed193b230e299d81b"


def _plan_path() -> Path:
    return HARNESS_ROOT / "public-run-plan.json"


def _manifest_path() -> Path:
    return HARNESS_ROOT / "harness.manifest.json"


def _result_bindings(plan_sha256: str, harness_manifest_sha256: str) -> dict[str, str]:
    return {
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_tree": CANDIDATE_TREE,
        "candidate_manifest_sha256": CANDIDATE_MANIFEST_SHA256,
        "candidate_source_set_sha256": CANDIDATE_SOURCE_SET_SHA256,
        "corpus_manifest_sha256": CORPUS_MANIFEST_SHA256,
        "corpus_source_set_sha256": CORPUS_SOURCE_SET_SHA256,
        "plan_sha256": plan_sha256,
        "harness_manifest_sha256": harness_manifest_sha256,
    }


def _python(candidate: Path) -> Path:
    path = candidate / ".venv" / "Scripts" / "python.exe" if os.name == "nt" else candidate / ".venv" / "bin" / "python"
    if not path.is_file():
        raise FileNotFoundError(f"candidate Python runtime not found: {path}")
    return path


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(os.path.abspath(left)) == os.path.normcase(os.path.abspath(right))


def _canonical_evaluator_runtime(args: argparse.Namespace) -> Path:
    """Pin author checks, blind runner, and product worker to one ACL-capable runtime."""
    invocation = Path(os.path.abspath(sys.executable))
    requested = Path(os.path.abspath(args.python_executable or invocation))
    candidate_runtime = _python(args.candidate)
    if _same_path(invocation, candidate_runtime):
        raise RuntimeError(
            "candidate .venv is not the evaluator runtime; invoke runner.ps1 so "
            "authority verification and the worker remain in the Windows sandbox context"
        )
    if not _same_path(invocation, EVALUATOR_PYTHON):
        raise RuntimeError(f"unexpected evaluator interpreter: {invocation}; expected {EVALUATOR_PYTHON}")
    if not _same_path(requested, invocation):
        raise RuntimeError("split runner/worker Python contexts are forbidden")
    return invocation


def child_metadata_probe(args: argparse.Namespace) -> int:
    """Read only the public metadata needed to prove worker-context ACL access."""
    manifest = Path(os.path.abspath(args.corpus)) / "corpus.manifest.json"
    candidate_entry = Path(os.path.abspath(args.candidate)) / "src" / "ck3chronicle" / "__init__.py"
    manifest_stat = manifest.stat()
    candidate_stat = candidate_entry.stat()
    payload = {
        "schema": "ck3chronicle.phase1-runner-child-metadata-probe",
        "schema_version": 1,
        "runtime": str(Path(os.path.abspath(sys.executable))),
        "corpus_manifest_bytes": manifest_stat.st_size,
        "corpus_manifest_sha256": sha256_file(manifest),
        "candidate_entry_bytes": candidate_stat.st_size,
        "candidate_entry_sha256": sha256_file(candidate_entry),
        "product_imported": False,
        "product_gate_execution": False,
        "expected_answer_accessed": False,
        "private_material_accessed": False,
    }
    if payload["corpus_manifest_sha256"] != CORPUS_MANIFEST_SHA256:
        raise RuntimeError("runner child sees a different corpus manifest")
    print(json.dumps(payload, sort_keys=True))
    return 0


def _worker_metadata_probe(runtime: Path, args: argparse.Namespace) -> dict[str, Any]:
    command = [
        str(runtime), "-B", str(HARNESS_ROOT / "harness.py"), "child-metadata-probe",
        "--candidate", str(args.candidate), "--candidate-manifest", str(args.candidate_manifest),
        "--corpus", str(args.corpus),
    ]
    env = os.environ.copy(); env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=120)
    if completed.returncode != 0:
        raise RuntimeError(
            "evaluator worker cannot read locked public metadata: "
            + completed.stderr.decode("utf-8", "replace")
        )
    payload = json.loads(completed.stdout.decode("utf-8"))
    return {
        "command": command,
        "exit_code": completed.returncode,
        "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
        "observation": payload,
    }


def _blind_runner_preflight(args: argparse.Namespace) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    runtime = _canonical_evaluator_runtime(args)
    authority = verify_authorities(args.candidate, args.candidate_manifest, args.corpus)
    child_probe = _worker_metadata_probe(runtime, args)
    return runtime, authority, child_probe


def blind_runner_probe(args: argparse.Namespace) -> int:
    runtime, authority, child_probe = _blind_runner_preflight(args)
    payload = {
        "schema": "ck3chronicle.phase1-blind-runner-preflight",
        "schema_version": 1,
        "runtime": file_identity(runtime),
        "authority_verification_sha256": hashlib.sha256(canonical_json_bytes(authority)).hexdigest(),
        "worker_metadata_probe": child_probe,
        "product_gate_execution": False,
        "expected_answer_accessed": False,
        "private_material_accessed": False,
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


def _corpus_gate_inputs(corpus: Path) -> dict[str, list[str]]:
    manifest = read_json(corpus / "corpus.manifest.json")
    return {str(gate): [str(item) for item in inputs] for gate, inputs in manifest["gate_inputs"].items()}


def validate_plan(plan: dict[str, Any], corpus: Path) -> dict[str, Any]:
    problems: list[str] = []
    cases = plan.get("cases", [])
    case_ids = [case.get("case_id") for case in cases]
    if len(case_ids) != len(set(case_ids)):
        problems.append("duplicate_case_id")
    plan_recipes = {str(case.get("recipe")) for case in cases}
    if plan_recipes != set(SUPPORTED_RECIPES):
        problems.append("explicit_recipe_inventory")
    gates = {case.get("gate") for case in cases}
    if gates != set(ALL_GATES):
        problems.append("gate_inventory")
    public = [case for case in cases if case["gate"] != "P1-HOLD-01"]
    hold = [case for case in cases if case["gate"] == "P1-HOLD-01"]
    if len(hold) != 1 or hold[0]["recipe"] != "private_placeholder" or hold[0]["actions"]:
        problems.append("private_placeholder")
    mapping = _corpus_gate_inputs(corpus)
    for gate in ALL_GATES:
        union: set[str] = set()
        for case in cases:
            if case["gate"] == gate:
                union.update(case["inputs"])
                recipe = str(case["recipe"])
                if not recipe.startswith(("capture_", "runtime_", "parse_", "report_", "mutation_", "perf_", "private_")):
                    problems.append(f"undispatched_recipe:{recipe}")
                if case.get("scoring") is not None:
                    problems.append(f"scorer_content:{case['case_id']}")
        if union != set(mapping[gate]):
            problems.append(f"gate_input_union:{gate}")
    taxonomy = sorted(case["case_id"] for case in cases if case["gate"] == "P1-REP-07")
    expected_taxonomy = sorted(f"rep07-{name}" for name in ("success", "readiness", "archive", "model", "database", "pipeline"))
    if taxonomy != expected_taxonomy:
        problems.append("rep07_six_case_taxonomy")
    mutations = sorted(case.get("mutation") for case in cases if case["gate"] == "P1-MUT-01")
    required_mutations = sorted(("remove_error_log", "zero_error_log", "archive_integrity_fault", "newline_variant", "locator_path", "semantic_literal", "truncated_tail", "swap_mount_order", "runtime_absent", "runtime_malformed", "inventory_metadata"))
    if mutations != required_mutations:
        problems.append("mutation_eleven_variant_inventory")
    rep06 = [case for case in cases if case["gate"] == "P1-REP-06"]
    if len(rep06) != 1 or rep06[0]["actions"][1:5] != ["create_run_a_normal", "create_run_b_later_normal", "create_run_c_later_crash_with_exception", "create_run_d_newest_unparsed"]:
        problems.append("rep06_fixed_chronology")
    perf = [case for case in cases if case["gate"].startswith("P1-PERF-")]
    if any(case.get("repetition_policy") != {"warmups": 1, "measured": 5, "retry": "forbidden"} for case in perf):
        problems.append("performance_repetition_policy")
    for case in cases:
        policy=case.get("timeout_policy")
        if not isinstance(policy,dict) or policy.get("schema")!="ck3chronicle.phase1-timeout-policy" or policy.get("scoring_threshold") is not False:
            problems.append(f"timeout_policy_schema:{case.get('case_id')}")
            continue
        if case["gate"]=="P1-HOLD-01":
            if policy.get("unassigned_unexecuted") is not True:
                problems.append("hold_timeout_policy")
            if policy != timeout_policy(case["recipe"],case["actions"],private_placeholder=True):
                problems.append("hold_timeout_policy_exact_mapping")
            continue
        if policy != timeout_policy(case["recipe"],case["actions"]):
            problems.append(f"timeout_policy_exact_mapping:{case['case_id']}")
        if not isinstance(policy.get("overall_case_seconds"),int) or policy["overall_case_seconds"]<=0:
            problems.append(f"overall_case_timeout:{case['case_id']}")
        if not isinstance(policy.get("product_subprocess_default_seconds"),int) or policy["product_subprocess_default_seconds"]<=0:
            problems.append(f"product_subprocess_timeout:{case['case_id']}")
        if not isinstance(policy.get("scratch_case_limit_bytes"),int) or policy["scratch_case_limit_bytes"]<=0:
            problems.append(f"scratch_case_limit:{case['case_id']}")
        if policy.get("retry_on_timeout") is not False:
            problems.append(f"timeout_retry_policy:{case['case_id']}")
        declared=policy.get("declared_actions")
        if not isinstance(declared,list) or [item.get("action") for item in declared if isinstance(item,dict)]!=case["actions"] or any(not isinstance(item.get("ceiling_seconds"),int) or item["ceiling_seconds"]<=0 or item.get("enforcement")!="remaining_outer_case_process_tree_deadline" for item in declared if isinstance(item,dict)):
            problems.append(f"declared_action_timeouts:{case['case_id']}")
        if case["gate"].startswith("P1-PERF-") and (not isinstance(policy.get("performance_action_seconds"),int) or policy["performance_action_seconds"]<=0):
            problems.append(f"performance_action_timeout:{case['case_id']}")
        if case["gate"].startswith("P1-PERF-"):
            multiplier=policy.get("action_ceiling_multiple_of_fourth_wall")
            allowance=policy.get("setup_and_observation_allowance_seconds")
            if not isinstance(multiplier,(int,float)) or not math.isfinite(multiplier) or multiplier<=1:
                problems.append(f"performance_timeout_multiplier:{case['case_id']}")
            if not isinstance(allowance,(int,float)) or not math.isfinite(allowance) or allowance<0:
                problems.append(f"performance_setup_allowance:{case['case_id']}")
    action_count = sum(len(case["actions"]) for case in cases)
    return {
        "schema": "ck3chronicle.phase1-run-plan-validation",
        "schema_version": 1,
        "valid": not problems,
        "problems": problems,
        "gate_count": len(gates),
        "public_gate_count": len({case["gate"] for case in public}),
        "public_case_count": len(public),
        "private_placeholder_case_count": len(hold),
        "action_count": action_count,
        "rep07_case_count": len(taxonomy),
        "mutation_case_count": len(mutations),
        "performance_case_count": len(perf),
        "supported_recipe_count": len(SUPPORTED_RECIPES),
        "executable_recipe_coverage": plan_recipes == set(SUPPORTED_RECIPES),
        "scorer_logic_present": False,
        "expected_answers_present": False,
        "timeout_policy_case_count": sum(1 for case in public if isinstance(case.get("timeout_policy"),dict)),
        "all_public_timeouts_finite": not any(problem.startswith(("timeout_","overall_case_timeout","product_subprocess_timeout","declared_action_timeouts","performance_action_timeout","performance_timeout_multiplier","performance_setup_allowance")) for problem in problems),
    }


def build_artifacts(args: argparse.Namespace) -> int:
    _canonical_evaluator_runtime(args)
    authority = verify_authorities(args.candidate, args.candidate_manifest, args.corpus)
    plan = build_plan(); validation = validate_plan(plan, args.corpus)
    if not validation["valid"]:
        raise RuntimeError("run-plan validation failed: " + ", ".join(validation["problems"]))
    write_canonical_json(_plan_path(), plan)
    write_canonical_json(HARNESS_ROOT / "authority-preflight.json", authority)
    write_canonical_json(HARNESS_ROOT / "dry-run.json", validation)
    write_canonical_json(HARNESS_ROOT / "timeout-table.json", timeout_table())
    mutation_report = mutation_preflight(args)
    write_canonical_json(HARNESS_ROOT / "mutation-preflight.json", mutation_report)
    print(json.dumps({"plan": str(_plan_path()), "plan_sha256": sha256_file(_plan_path()), "authority_verified": True, **{key: validation[key] for key in ("gate_count", "public_gate_count", "public_case_count", "private_placeholder_case_count", "action_count")}}, sort_keys=True))
    return 0


def mutation_preflight(args: argparse.Namespace) -> dict[str, Any]:
    """Derive every fixed public mutation once without candidate execution."""
    temporary = Path(tempfile.mkdtemp(prefix="phase1-mutation-preflight-"))
    specifications = [
        ("remove_error_log", "PUB-NOMINAL-20260510"),
        ("zero_error_log", "PUB-NOMINAL-20260510"),
        ("newline_variant", "PUB-NOMINAL-20260510"),
        ("locator_path", "PUB-NOMINAL-20260510"),
        ("semantic_literal", "PUB-NOMINAL-20260510"),
        ("truncated_tail", "PUB-NOMINAL-20260510"),
        ("swap_mount_order", "PUB-RUNTIME-COMPLETE-20260816"),
        ("runtime_absent", "PUB-RUNTIME-COMPLETE-20260816"),
        ("runtime_malformed", "PUB-RUNTIME-COMPLETE-20260816"),
        ("inventory_metadata", "PUB-RUNTIME-COMPLETE-20260816"),
        ("absolute_locator_root", "PUB-LONG-20260429"),
        ("runtime_state_truncated", "PUB-RUNTIME-COMPLETE-20260816"),
        ("runtime_state_ambiguous", "PUB-RUNTIME-COMPLETE-20260816"),
        ("robustness_encoding", "PUB-NOMINAL-20260510"),
        ("robustness_newline", "PUB-NOMINAL-20260510"),
        ("robustness_long_line", "PUB-STRESS-20260806"),
        ("robustness_malformed", "PUB-NOMINAL-20260510"),
        ("robustness_replacement_character", "PUB-NOMINAL-20260510"),
        ("robustness_truncation", "PUB-NOMINAL-20260510"),
    ]
    descriptors=[]
    try:
        for index,(mutation,unit) in enumerate(specifications):
            destination=temporary/f"{index:02d}-{mutation}"; staged=stage_unit(args.corpus,unit,destination); descriptor=apply_mutation(mutation,destination)
            descriptors.append({"unit":unit,"staged_tree_sha256":staged["tree_sha256"],"descriptor":descriptor})
        # The archive-integrity recipe changes one exact byte only after the
        # product has registered an archive.  Its byte operation is preflighted
        # here on the assigned authentic crash error.log without registration.
        crash=temporary/"archive-integrity"; staged=stage_unit(args.corpus,"PUB-CRASH-20260428",crash,include_all=True); target=crash/"logs"/"error.log"; base=target.read_bytes(); derived=bytes([base[0]^1])+base[1:]
        descriptors.append({"unit":"PUB-CRASH-20260428","staged_tree_sha256":staged["tree_sha256"],"descriptor":{"schema":"ck3chronicle.phase1-mutation-descriptor","schema_version":1,"mutation_id":"archive_integrity_fault","relative_path":"logs/error.log","base_bytes":len(base),"base_sha256":hashlib.sha256(base).hexdigest(),"derived_bytes":len(derived),"derived_sha256":hashlib.sha256(derived).hexdigest(),"application_count":1,"edits":[{"base_start":0,"base_end":1,"derived_start":0,"derived_end":1,"before_hex":base[:1].hex(),"after_hex":derived[:1].hex()}],"protected_invariants":{"suffix_equal":base[1:]==derived[1:],"suffix_sha256":hashlib.sha256(base[1:]).hexdigest()}}})
        return {"schema":"ck3chronicle.phase1-public-mutation-preflight","schema_version":1,"classification":"non_scoring_no_candidate_execution","descriptor_count":len(descriptors),"descriptors":descriptors,"all_application_counts_positive":all(int(item["descriptor"]["application_count"])>0 for item in descriptors),"private_material_accessed":False,"expected_answer_accessed":False}
    finally:
        shutil.rmtree(temporary,ignore_errors=True)


def dry_run(args: argparse.Namespace) -> int:
    plan = read_json(_plan_path()) if _plan_path().is_file() else build_plan()
    validation = validate_plan(plan, args.corpus)
    validation["candidate_execution"] = False
    validation["output_scratch_overlap_checked"] = False
    if args.results_root and args.scratch_root:
        assert_isolated_paths(results_root=args.results_root, scratch_root=args.scratch_root, candidate_root=args.candidate, corpus_root=args.corpus, harness_root=HARNESS_ROOT)
        validation["output_scratch_overlap_checked"] = True
    if args.output:
        write_canonical_json(args.output, validation)
    print(json.dumps(validation, sort_keys=True))
    return 0 if validation["valid"] else 2


def self_test(args: argparse.Namespace) -> int:
    from candidate_runtime import independent_lexical_scan
    temp = Path(tempfile.mkdtemp(prefix="phase1-harness-selftest-"))
    checks: list[dict[str, Any]] = []
    try:
        runtime = _canonical_evaluator_runtime(args)
        runner_command = [
            str(POWERSHELL), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
            str(HARNESS_ROOT / "runner.ps1"), "blind-runner-probe",
            "--candidate", str(args.candidate), "--candidate-manifest", str(args.candidate_manifest),
            "--corpus", str(args.corpus),
        ]
        runner_completed = subprocess.run(runner_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=120)
        runner_payload = None
        if runner_completed.returncode == 0:
            try:
                runner_payload = json.loads(runner_completed.stdout.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                runner_payload = None
        checks.append({
            "name": "actual_blind_runner_windows_metadata_path",
            "passed": runner_completed.returncode == 0
                and runner_payload is not None
                and runner_payload.get("worker_metadata_probe", {}).get("observation", {}).get("corpus_manifest_sha256") == CORPUS_MANIFEST_SHA256
                and runner_payload.get("product_gate_execution") is False,
            "details": {
                "command": runner_command,
                "exit_code": runner_completed.returncode,
                "stdout_sha256": hashlib.sha256(runner_completed.stdout).hexdigest(),
                "stderr_sha256": hashlib.sha256(runner_completed.stderr).hexdigest(),
                "observation": runner_payload,
            },
        })
        candidate_runtime_rejected = False
        try:
            rejection_args = argparse.Namespace(candidate=args.candidate, python_executable=_python(args.candidate))
            _canonical_evaluator_runtime(rejection_args)
        except RuntimeError:
            candidate_runtime_rejected = True
        checks.append({
            "name": "candidate_venv_runner_context_rejected_before_authority_access",
            "passed": candidate_runtime_rejected,
            "details": {"forbidden_runtime": str(_python(args.candidate)), "required_runtime": str(runtime)},
        })
        # Synthetic fixtures are restricted to this self-test.
        logs = temp / "synthetic-logs"; logs.mkdir()
        (logs / "error.log").write_bytes(b"[00:00:00][E][x.cpp:1]: Failed to create material in gfx/FX/court_scene.shader\r\n[00:00:01][E][x.cpp:2]: tail\r\n" + b"x" * 5000)
        (logs / "debug.log").write_bytes(b"CFP + EPE Compatibility Patch|mod/ugc_1.mod|Enabled\r\n[00:00:00][D][v.cpp:1]: Mounted Data: C:/game/dlc/dlc001\r\n[00:00:00][D][v.cpp:1]: Mounted Data: C:/workshop/content/1158310/1\r\n[00:00:00][D][v.cpp:1]: Mounted Data: C:/workshop/content/1158310/2\r\n")
        for mutation in ("newline_variant", "locator_path", "semantic_literal", "truncated_tail", "inventory_metadata"):
            case_logs = temp / mutation; shutil.copytree(logs, case_logs); descriptor = apply_mutation(mutation, case_logs)
            checks.append({"name": f"mutation:{mutation}", "passed": descriptor["application_count"] >= 1 and descriptor["base_sha256"] != descriptor.get("derived_sha256")})
        plan = build_plan(); validation = validate_plan(plan, args.corpus); checks.append({"name": "plan_validation", "passed": validation["valid"], "details": validation})
        perf_boundary_problems=[]
        expected_perf_child_actions={"perf_lexical":"lexical","perf_parse":"parse","perf_runtime":"runtime","perf_report_function":"report_function","perf_report_report_text":"report_cli","perf_report_report_json":"report_cli","perf_report_latest_text":"report_cli","perf_report_latest_json":"report_cli","perf_report_errors_text":"report_cli","perf_report_errors_json":"report_cli","perf_pipeline":"pipeline"}
        for perf_case in (item for item in plan["cases"] if item["gate"].startswith("P1-PERF-")):
            for boundary in perf_case["timeout_policy"]["declared_actions"]:
                expected_count=1 if boundary["action"].startswith("run_one_") else 5 if boundary["action"].startswith("run_five_") else None
                measurement=boundary.get("measurement_invocations")
                if boundary["enforcement"]!="remaining_outer_case_process_tree_deadline" or boundary["ceiling_seconds"]!=perf_case["timeout_policy"]["overall_case_seconds"]:
                    perf_boundary_problems.append(f"outer:{perf_case['case_id']}:{boundary['action']}")
                if expected_count is None and (measurement is not None or boundary.get("boundary_kind")!="outer_case_step"):
                    perf_boundary_problems.append(f"unexpected_measurement:{perf_case['case_id']}:{boundary['action']}")
                if expected_count is not None and (boundary.get("boundary_kind")!="measurement_invocation_group_with_outer_case_deadline" or not isinstance(measurement,dict) or measurement.get("count")!=expected_count or measurement.get("child_action")!=expected_perf_child_actions[perf_case["recipe"]] or measurement.get("per_invocation_ceiling_seconds")!=perf_case["timeout_policy"]["performance_action_seconds"] or measurement.get("enforcement")!="dedicated_performance_child_process_tree_deadline"):
                    perf_boundary_problems.append(f"measurement:{perf_case['case_id']}:{boundary['action']}")
        checks.append({"name":"performance_action_specific_timeout_boundary_mapping","passed":not perf_boundary_problems,"details":{"performance_case_count":11,"expected_measurement_invocation_counts":[1,5],"problems":perf_boundary_problems}})
        left = temp / "left"; right = temp / "right"; left.mkdir(); right.mkdir()
        assert_isolated_paths(results_root=left, scratch_root=right, candidate_root=args.candidate, corpus_root=args.corpus, harness_root=HARNESS_ROOT)
        overlap_rejected = False
        try: assert_isolated_paths(results_root=left, scratch_root=left / "nested", candidate_root=args.candidate, corpus_root=args.corpus, harness_root=HARNESS_ROOT)
        except ValueError: overlap_rejected = True
        checks.append({"name": "path_nonoverlap", "passed": overlap_rejected})
        lexical = temp / "lexical-bom.log"
        lexical_bytes = b"\xef\xbb\xbf[00:00:00][E][x.cpp:1]: first\r\ncontinued\r\n[00:00:01][E][y.cpp:2]: second\n"
        lexical.write_bytes(lexical_bytes)
        scan = independent_lexical_scan(lexical)
        checks.append({"name": "independent_lexical_reconstruction", "passed": scan["timestamped_blocks"] == 2 and scan["preamble_blocks"] == 0 and scan["reconstruction_sha256"] == hashlib.sha256(lexical_bytes).hexdigest(), "details": {key: scan[key] for key in ("timestamped_blocks", "preamble_blocks", "reconstruction_sha256")}})

        # Reproduce the authentic failed case's retained size and case/path
        # shape while holding its final directory open without delete sharing.
        publication_root=temp/"authentic-shape-results"; publication_scratch=temp/"authentic-shape-scratch"
        publication_case={"case_id":"run02-workshop-local","gate":"SELFTEST","recipe":"self_test_authentic_publication_shape","inputs":[]}
        publication_cases={publication_case["case_id"]:publication_case}; publication_bindings=_result_bindings("2"*64,"3"*64)
        initialize_results(publication_root,publication_scratch,plan_sha256="2"*64,harness_manifest_sha256="3"*64)
        publication_case_scratch=new_scratch_directory(publication_scratch,publication_case["case_id"]); publication_declared=publication_case_scratch/"declared"/"transcripts"; publication_declared.mkdir(parents=True)
        authentic_payload=publication_declared/"context-json.stdout.bin"; authentic_payload.write_bytes(b"x"*218415)
        held_handles=[]
        def hold_final_directory(final_directory: Path) -> None:
            if os.name != "nt":
                held_handles.append(None); return
            import ctypes
            kernel32=ctypes.windll.kernel32
            kernel32.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p]
            kernel32.CreateFileW.restype=ctypes.c_void_p
            handle=kernel32.CreateFileW(str(final_directory),0,0x1|0x2,None,3,0x02000000,None)
            if handle in (None,ctypes.c_void_p(-1).value):
                raise OSError(ctypes.get_last_error(),"unable to hold final directory")
            held_handles.append(handle)
        publication_journal=close_case(results_root=publication_root,scratch_case=publication_case_scratch,case=publication_case,execution={"worker_exit_code":0,"product_case_attempts":0},before_completion_hook=hold_final_directory)
        if held_handles and held_handles[0] is not None:
            import ctypes
            ctypes.windll.kernel32.CloseHandle(ctypes.c_void_p(held_handles[0]))
        publication_verification=verify_result_set(publication_root,expected_cases=publication_cases,expected_bindings=publication_bindings)
        checks.append({"name":"authentic_size_held_open_directory_atomic_marker_close","passed":publication_journal["retained_bytes"]==218415 and publication_journal["scratch_deleted"] and publication_verification["verified"] and publication_verification["case_count"]==1 and (publication_root/"cases"/publication_case["case_id"]/CASE_COMPLETION_MARKER).is_file(),"details":{"retained_bytes":publication_journal["retained_bytes"],"case_path":str(publication_root/"cases"/publication_case["case_id"]),"completion_marker_sha256":publication_journal["completion_marker_sha256"],"verification_problems":publication_verification["problems"],"canonical_runtime":str(runtime)}})

        # Force the atomic marker target to be an unreplaceable directory.  A
        # pre-marker failure must remain partial, retain scratch, and forbid reuse.
        denied_root=temp/"permission-failure-results"; denied_scratch=temp/"permission-failure-scratch"
        denied_case={"case_id":"run02-workshop-local","gate":"SELFTEST","recipe":"self_test_permission_failure","inputs":[]}; denied_cases={denied_case["case_id"]:denied_case}; denied_bindings=_result_bindings("4"*64,"5"*64)
        initialize_results(denied_root,denied_scratch,plan_sha256="4"*64,harness_manifest_sha256="5"*64)
        denied_case_scratch=new_scratch_directory(denied_scratch,denied_case["case_id"]); denied_declared=denied_case_scratch/"declared"; denied_declared.mkdir(); (denied_declared/"observation.json").write_bytes(b"y"*218415)
        def deny_completion(final_directory: Path) -> None:
            (final_directory/CASE_COMPLETION_MARKER).mkdir()
        permission_failed=False
        try:
            close_case(results_root=denied_root,scratch_case=denied_case_scratch,case=denied_case,execution={"worker_exit_code":0,"product_case_attempts":0},before_completion_hook=deny_completion)
        except OSError:
            permission_failed=True
        denied_verification=verify_result_set(denied_root,expected_cases=denied_cases,expected_bindings=denied_bindings)
        reuse_rejected=False
        try:
            close_case(results_root=denied_root,scratch_case=denied_case_scratch,case=denied_case,execution={"worker_exit_code":0,"product_case_attempts":0})
        except FileExistsError:
            reuse_rejected=True
        checks.append({"name":"permission_failure_partial_detection_scratch_retention_and_reuse_rejection","passed":permission_failed and denied_case_scratch.exists() and not denied_verification["verified"] and denied_verification["partial_cases"]==[denied_case["case_id"]] and denied_verification["case_count"]==0 and reuse_rejected,"details":{"permission_failed":permission_failed,"scratch_retained":denied_case_scratch.exists(),"partial_cases":denied_verification["partial_cases"],"verification_problems":denied_verification["problems"],"reuse_rejected":reuse_rejected}})

        # The abandoned v2 root has legacy case directories without v3 atomic
        # markers plus one .open directory.  Inspect names/bindings only and
        # prove it is rejected without reading its retained observations.
        foreign_before={"result_set_sha256":sha256_file(FAILED_V2_RESULTS/"result-set.json"),"journal_sha256":sha256_file(FAILED_V2_RESULTS/"journal.ndjson")}
        foreign_verification=verify_result_set(FAILED_V2_RESULTS,expected_cases={case["case_id"]:case for case in plan["cases"] if case["gate"]!="P1-HOLD-01"},expected_bindings=_result_bindings(sha256_file(_plan_path()),"v3-harness-binding-not-v2"))
        foreign_after={"result_set_sha256":sha256_file(FAILED_V2_RESULTS/"result-set.json"),"journal_sha256":sha256_file(FAILED_V2_RESULTS/"journal.ndjson")}
        checks.append({"name":"abandoned_v2_result_cannot_be_v3_input","passed":foreign_before==foreign_after=={"result_set_sha256":FAILED_V2_RESULT_SET_SHA256,"journal_sha256":FAILED_V2_JOURNAL_SHA256} and not foreign_verification["verified"] and foreign_verification["case_count"]==0 and foreign_verification["partial_case_count"]==13 and foreign_verification["open_envelope_count"]==1,"details":{"identity_before":foreign_before,"identity_after":foreign_after,"case_count":foreign_verification["case_count"],"partial_case_count":foreign_verification["partial_case_count"],"open_envelope_count":foreign_verification["open_envelope_count"],"verification_problems":foreign_verification["problems"]}})

        # Every aggregate publication boundary is fault-injected independently.
        # With no final marker, each interrupted aggregate is non-closed and can
        # be regenerated only from the already verified immutable case markers.
        aggregate_boundaries = (
            "raw_journal",
            "canonical_journal",
            "closed_result_set",
            "aggregate_manifest",
            "aggregate_immutability",
            "result_completion_marker",
        )
        aggregate_fault_details=[]
        aggregate_faults_passed=True
        for index,boundary_name in enumerate(aggregate_boundaries):
            fault_root=temp/f"aggregate-fault-{index}"; fault_scratch=temp/f"aggregate-fault-scratch-{index}"
            fault_case={"case_id":"selftest-case","gate":"SELFTEST","recipe":"aggregate_fault_boundary","inputs":[]}
            fault_cases={fault_case["case_id"]:fault_case}; plan_hash=f"{index+1:x}"*64; manifest_hash=f"{index+7:x}"*64
            fault_bindings=_result_bindings(plan_hash,manifest_hash)
            initialize_results(fault_root,fault_scratch,plan_sha256=plan_hash,harness_manifest_sha256=manifest_hash)
            fault_case_scratch=new_scratch_directory(fault_scratch,fault_case["case_id"]); fault_declared=fault_case_scratch/"declared"; fault_declared.mkdir(); (fault_declared/"observation.bin").write_bytes(b"fault-boundary")
            close_case(results_root=fault_root,scratch_case=fault_case_scratch,case=fault_case,execution={"worker_exit_code":0,"product_case_attempts":0})
            def inject_failure(step_name: str, _target: Path, *, expected: str=boundary_name) -> None:
                if step_name == expected:
                    raise PermissionError(f"synthetic aggregate boundary fault: {expected}")
            failed=False
            try:
                close_result_set(fault_root,fault_cases,fault_bindings,before_aggregate_step=inject_failure)
            except PermissionError:
                failed=True
            interrupted=verify_result_set(fault_root,require_closed=True,expected_cases=fault_cases,expected_bindings=fault_bindings)
            marker_absent=not (fault_root/RESULT_COMPLETION_MARKER).exists()
            recovered=close_result_set(fault_root,fault_cases,fault_bindings)
            recovered_verification=verify_result_set(fault_root,require_closed=True,expected_cases=fault_cases,expected_bindings=fault_bindings)
            boundary_passed=failed and marker_absent and not interrupted["verified"] and recovered_verification["verified"] and recovered["case_count"]==1
            aggregate_faults_passed = aggregate_faults_passed and boundary_passed
            aggregate_fault_details.append({"boundary":boundary_name,"passed":boundary_passed,"failure_observed":failed,"marker_absent_after_failure":marker_absent,"interrupted_problems":interrupted["problems"],"recovery":recovered,"recovered_problems":recovered_verification["problems"]})
        checks.append({"name":"aggregate_all_boundary_faults_are_nonclosed_and_recoverable","passed":aggregate_faults_passed and len(aggregate_fault_details)==6,"details":{"boundaries":aggregate_fault_details}})

        # Exercise failures inside the atomic helper, after the temp is durable.
        # These are the states created by a real os.replace error or termination.
        fsync_root=temp/"aggregate-after-fsync"; fsync_scratch=temp/"aggregate-after-fsync-scratch"
        fsync_case={"case_id":"selftest-case","gate":"SELFTEST","recipe":"aggregate_after_fsync_fault","inputs":[]}; fsync_cases={fsync_case["case_id"]:fsync_case}; fsync_bindings=_result_bindings("e"*64,"f"*64)
        initialize_results(fsync_root,fsync_scratch,plan_sha256="e"*64,harness_manifest_sha256="f"*64)
        fsync_case_scratch=new_scratch_directory(fsync_scratch,fsync_case["case_id"]); close_case(results_root=fsync_root,scratch_case=fsync_case_scratch,case=fsync_case,execution={"worker_exit_code":0,"product_case_attempts":0})
        def fail_after_fsync(stage_name: str, final_path: Path, _temporary_path: Path) -> None:
            if stage_name == "after_fsync" and final_path.name == "journal.ndjson":
                raise PermissionError("synthetic post-fsync failure")
        fsync_failed=False
        try:
            close_result_set(fsync_root,fsync_cases,fsync_bindings,atomic_fault_hook=fail_after_fsync)
        except PermissionError:
            fsync_failed=True
        fsync_temps=sorted(path.name for path in fsync_root.iterdir() if path.name.startswith(".journal.ndjson.") and path.name.endswith(".tmp"))
        fsync_interrupted=verify_result_set(fsync_root,require_closed=True,expected_cases=fsync_cases,expected_bindings=fsync_bindings)
        fsync_recovery=close_result_set(fsync_root,fsync_cases,fsync_bindings)
        fsync_recovered=verify_result_set(fsync_root,require_closed=True,expected_cases=fsync_cases,expected_bindings=fsync_bindings)
        checks.append({"name":"post_fsync_temp_same_process_retry_recovery","passed":fsync_failed and len(fsync_temps)==1 and not fsync_interrupted["verified"] and fsync_recovery["removed_incomplete_temps"]==fsync_temps and fsync_recovered["verified"],"details":{"failure_observed":fsync_failed,"leftover_temps":fsync_temps,"interrupted_problems":fsync_interrupted["problems"],"recovery":fsync_recovery,"recovered_problems":fsync_recovered["problems"]}})

        replace_root=temp/"aggregate-replace-failure"; replace_scratch=temp/"aggregate-replace-failure-scratch"
        replace_case={"case_id":"selftest-case","gate":"SELFTEST","recipe":"aggregate_replace_fault","inputs":[]}; replace_cases={replace_case["case_id"]:replace_case}; replace_bindings=_result_bindings("1"*64,"2"*64)
        initialize_results(replace_root,replace_scratch,plan_sha256="1"*64,harness_manifest_sha256="2"*64)
        replace_case_scratch=new_scratch_directory(replace_scratch,replace_case["case_id"]); close_case(results_root=replace_root,scratch_case=replace_case_scratch,case=replace_case,execution={"worker_exit_code":0,"product_case_attempts":0})
        def fail_canonical_replace(source: Path, target: Path) -> None:
            if target.name == "runner-result.journal.json":
                raise PermissionError("synthetic os.replace failure")
            os.replace(source,target)
        replace_failed=False
        try:
            close_result_set(replace_root,replace_cases,replace_bindings,replace_operation=fail_canonical_replace)
        except PermissionError:
            replace_failed=True
        current_temps=list(replace_root.glob(".runner-result.journal.json.*.tmp"))
        prior_temp_name=".runner-result.journal.json.424242.tmp"
        if len(current_temps)==1:
            os.replace(current_temps[0],replace_root/prior_temp_name)
        replace_interrupted=verify_result_set(replace_root,require_closed=True,expected_cases=replace_cases,expected_bindings=replace_bindings)
        replace_recovery=close_result_set(replace_root,replace_cases,replace_bindings)
        replace_recovered=verify_result_set(replace_root,require_closed=True,expected_cases=replace_cases,expected_bindings=replace_bindings)
        checks.append({"name":"replace_failure_prior_process_temp_recovery","passed":replace_failed and len(current_temps)==1 and not replace_interrupted["verified"] and replace_recovery["removed_incomplete_temps"]==[prior_temp_name] and replace_recovered["verified"],"details":{"failure_observed":replace_failed,"renamed_prior_process_temp":prior_temp_name,"interrupted_problems":replace_interrupted["problems"],"recovery":replace_recovery,"recovered_problems":replace_recovered["problems"]}})

        # A final-marker path is authoritative by lexical presence.  Neither a
        # dangling nor live symlink may be followed, replaced, or used as a
        # reason to remove an otherwise recoverable aggregate temp.
        symlink_details=[]; symlink_checks_passed=True
        for index,link_kind in enumerate(("dangling","live")):
            link_root=temp/f"aggregate-marker-{link_kind}"; link_scratch=temp/f"aggregate-marker-{link_kind}-scratch"
            link_case={"case_id":"selftest-case","gate":"SELFTEST","recipe":f"aggregate_marker_{link_kind}_symlink","inputs":[]}; link_cases={link_case["case_id"]:link_case}; link_plan_hash=str(index+3)*64; link_manifest_hash=str(index+5)*64; link_bindings=_result_bindings(link_plan_hash,link_manifest_hash)
            initialize_results(link_root,link_scratch,plan_sha256=link_plan_hash,harness_manifest_sha256=link_manifest_hash)
            link_case_scratch=new_scratch_directory(link_scratch,link_case["case_id"]); close_case(results_root=link_root,scratch_case=link_case_scratch,case=link_case,execution={"worker_exit_code":0,"product_case_attempts":0})
            owned_temp=link_root/f".journal.ndjson.{777001+index}.tmp"; owned_temp.write_bytes(b"must-remain")
            link_target=temp/f"{link_kind}-external-marker-target"
            if link_kind=="live":
                link_target.write_bytes(b"{}\n")
            marker_link=link_root/RESULT_COMPLETION_MARKER
            actual_link_kind="symlink"
            try:
                os.symlink(link_target,marker_link,target_is_directory=False)
            except OSError as error:
                if os.name!="nt" or getattr(error,"winerror",None)!=1314:
                    raise
                # The canonical evaluator token has no symlink privilege.  A
                # Windows directory junction is the available real reparse-link
                # equivalent and exercises the same lexists/following defect.
                actual_link_kind="windows_junction_no_symlink_privilege"
                if link_target.is_file():
                    link_target.unlink()
                link_target.mkdir()
                junction=subprocess.run([os.environ.get("ComSpec",r"C:\Windows\System32\cmd.exe"),"/d","/c","mklink","/J",str(marker_link),str(link_target)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,timeout=30)
                if junction.returncode!=0:
                    raise RuntimeError("unable to create Windows junction self-test fixture: "+junction.stderr.decode("utf-8","replace"))
                if link_kind=="dangling":
                    link_target.rmdir()
            refused=False
            try:
                close_result_set(link_root,link_cases,link_bindings)
            except RuntimeError:
                refused=True
            link_verification=verify_result_set(link_root,require_closed=True,expected_cases=link_cases,expected_bindings=link_bindings)
            link_passed=refused and owned_temp.is_file() and owned_temp.read_bytes()==b"must-remain" and os.path.lexists(marker_link) and path_is_linklike(marker_link) and "aggregate_completion_marker_special_entry" in link_verification["problems"] and any(problem.startswith("result_set_special_top_entries:") for problem in link_verification["problems"])
            symlink_checks_passed=symlink_checks_passed and link_passed
            symlink_details.append({"kind":link_kind,"actual_link_kind":actual_link_kind,"passed":link_passed,"recovery_refused":refused,"temp_preserved":owned_temp.is_file(),"marker_lexically_present":os.path.lexists(marker_link),"marker_linklike":path_is_linklike(marker_link),"verification_problems":link_verification["problems"]})
        checks.append({"name":"dangling_and_live_final_marker_symlinks_refuse_without_temp_cleanup","passed":symlink_checks_passed and len(symlink_details)==2,"details":{"variants":symlink_details}})

        # Container and artifact-ancestor junctions must be identified before
        # iteration or hashing; the external targets remain untouched.
        container_root=temp/"junction-container-results"; container_scratch=temp/"junction-container-scratch"; container_bindings=_result_bindings("7"*64,"8"*64)
        initialize_results(container_root,container_scratch,plan_sha256="7"*64,harness_manifest_sha256="8"*64)
        (container_root/"cases").rmdir(); external_cases=temp/"external-cases-target"; external_cases.mkdir(); external_cases_sentinel=external_cases/"must-not-scan.bin"; external_cases_sentinel.write_bytes(b"external-container-sentinel"); external_cases_hash=sha256_file(external_cases_sentinel)
        container_junction=subprocess.run([os.environ.get("ComSpec",r"C:\Windows\System32\cmd.exe"),"/d","/c","mklink","/J",str(container_root/"cases"),str(external_cases)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,timeout=30)
        if container_junction.returncode!=0:
            raise RuntimeError("unable to create cases-container junction fixture: "+container_junction.stderr.decode("utf-8","replace"))
        container_verification=verify_result_set(container_root,expected_cases={},expected_bindings=container_bindings)
        checks.append({"name":"cases_container_junction_rejected_before_iteration","passed":not container_verification["verified"] and "case_root_special_entry" in container_verification["problems"] and container_verification["case_count"]==0 and sha256_file(external_cases_sentinel)==external_cases_hash,"details":{"verification_problems":container_verification["problems"],"external_sentinel_sha256_before":external_cases_hash,"external_sentinel_sha256_after":sha256_file(external_cases_sentinel)}})

        ancestor_root=temp/"junction-artifact-results"; ancestor_scratch=temp/"junction-artifact-scratch"; ancestor_bindings=_result_bindings("9"*64,"a"*64)
        ancestor_case={"case_id":"selftest-case","gate":"SELFTEST","recipe":"artifact_ancestor_junction","inputs":[]}; ancestor_cases={ancestor_case["case_id"]:ancestor_case}
        initialize_results(ancestor_root,ancestor_scratch,plan_sha256="9"*64,harness_manifest_sha256="a"*64)
        ancestor_case_scratch=new_scratch_directory(ancestor_scratch,ancestor_case["case_id"]); ancestor_declared=ancestor_case_scratch/"declared"/"nested"; ancestor_declared.mkdir(parents=True); ancestor_bytes=b"external-artifact-sentinel"; (ancestor_declared/"observation.bin").write_bytes(ancestor_bytes)
        close_case(results_root=ancestor_root,scratch_case=ancestor_case_scratch,case=ancestor_case,execution={"worker_exit_code":0,"product_case_attempts":0})
        nested_path=ancestor_root/"cases"/ancestor_case["case_id"]/"artifacts"/"nested"; nested_file=nested_path/"observation.bin"; nested_file.chmod(stat.S_IREAD|stat.S_IWRITE); nested_file.unlink(); nested_path.rmdir()
        external_artifacts=temp/"external-artifact-target"; external_artifacts.mkdir(); external_artifact=external_artifacts/"observation.bin"; external_artifact.write_bytes(ancestor_bytes); external_artifact_hash=sha256_file(external_artifact)
        ancestor_junction=subprocess.run([os.environ.get("ComSpec",r"C:\Windows\System32\cmd.exe"),"/d","/c","mklink","/J",str(nested_path),str(external_artifacts)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,timeout=30)
        if ancestor_junction.returncode!=0:
            raise RuntimeError("unable to create artifact-ancestor junction fixture: "+ancestor_junction.stderr.decode("utf-8","replace"))
        ancestor_verification=verify_result_set(ancestor_root,expected_cases=ancestor_cases,expected_bindings=ancestor_bindings)
        ancestor_problems=ancestor_verification["problems"]
        checks.append({"name":"artifact_ancestor_junction_rejected_without_traversal","passed":not ancestor_verification["verified"] and ancestor_verification["case_count"]==0 and any(problem.startswith("retained_artifact_escape:selftest-case/") for problem in ancestor_problems) and any(problem.startswith("case_special_entries:selftest-case:") for problem in ancestor_problems) and sha256_file(external_artifact)==external_artifact_hash,"details":{"verification_problems":ancestor_problems,"external_artifact_sha256_before":external_artifact_hash,"external_artifact_sha256_after":sha256_file(external_artifact)}})

        # Malformed JSON value types are observations, never verifier crashes.
        malformed_marker_root=temp/"malformed-marker-results"; malformed_marker_scratch=temp/"malformed-marker-scratch"
        malformed_case={"case_id":"selftest-case","gate":"SELFTEST","recipe":"malformed_marker_type","inputs":[]}; malformed_cases={malformed_case["case_id"]:malformed_case}; malformed_bindings=_result_bindings("a"*64,"b"*64)
        initialize_results(malformed_marker_root,malformed_marker_scratch,plan_sha256="a"*64,harness_manifest_sha256="b"*64)
        malformed_case_scratch=new_scratch_directory(malformed_marker_scratch,malformed_case["case_id"])
        close_case(results_root=malformed_marker_root,scratch_case=malformed_case_scratch,case=malformed_case,execution={"worker_exit_code":0,"product_case_attempts":0})
        malformed_marker_path=malformed_marker_root/"cases"/malformed_case["case_id"]/CASE_COMPLETION_MARKER
        malformed_marker_path.chmod(stat.S_IREAD|stat.S_IWRITE); write_canonical_json(malformed_marker_path,[]); malformed_marker_path.chmod(stat.S_IREAD|stat.S_IRGRP|stat.S_IROTH)
        malformed_marker_verification=verify_result_set(malformed_marker_root,expected_cases=malformed_cases,expected_bindings=malformed_bindings)

        malformed_envelope_root=temp/"malformed-envelope-results"; malformed_envelope_scratch=temp/"malformed-envelope-scratch"
        malformed_envelope_case={"case_id":"selftest-case","gate":"SELFTEST","recipe":"malformed_retained_entry_type","inputs":[]}; malformed_envelope_cases={malformed_envelope_case["case_id"]:malformed_envelope_case}; malformed_envelope_bindings=_result_bindings("c"*64,"d"*64)
        initialize_results(malformed_envelope_root,malformed_envelope_scratch,plan_sha256="c"*64,harness_manifest_sha256="d"*64)
        malformed_envelope_case_scratch=new_scratch_directory(malformed_envelope_scratch,malformed_envelope_case["case_id"])
        close_case(results_root=malformed_envelope_root,scratch_case=malformed_envelope_case_scratch,case=malformed_envelope_case,execution={"worker_exit_code":0,"product_case_attempts":0})
        malformed_case_dir=malformed_envelope_root/"cases"/malformed_envelope_case["case_id"]
        malformed_envelope_path=malformed_case_dir/"case-result.json"; malformed_completion_path=malformed_case_dir/CASE_COMPLETION_MARKER
        malformed_envelope=read_json(malformed_envelope_path); malformed_envelope["retained_artifacts"]=[None]
        malformed_envelope_path.chmod(stat.S_IREAD|stat.S_IWRITE); malformed_envelope_sha=write_canonical_json(malformed_envelope_path,malformed_envelope); malformed_envelope_path.chmod(stat.S_IREAD|stat.S_IRGRP|stat.S_IROTH)
        malformed_completion=read_json(malformed_completion_path); malformed_completion["case_result_sha256"]=malformed_envelope_sha; malformed_completion["artifact_inventory_sha256"]=hashlib.sha256(canonical_json_bytes([None])).hexdigest()
        malformed_completion_path.chmod(stat.S_IREAD|stat.S_IWRITE); write_canonical_json(malformed_completion_path,malformed_completion); malformed_completion_path.chmod(stat.S_IREAD|stat.S_IRGRP|stat.S_IROTH)
        malformed_envelope_verification=verify_result_set(malformed_envelope_root,expected_cases=malformed_envelope_cases,expected_bindings=malformed_envelope_bindings)
        checks.append({"name":"malformed_marker_envelope_and_retained_types_are_contained","passed":not malformed_marker_verification["verified"] and malformed_marker_verification["invalid_completed_case_count"]==1 and "case_completion_object_schema:selftest-case" in malformed_marker_verification["problems"] and not malformed_envelope_verification["verified"] and malformed_envelope_verification["invalid_completed_case_count"]==1 and "retained_artifact_entry_schema:selftest-case/0" in malformed_envelope_verification["problems"],"details":{"marker_problems":malformed_marker_verification["problems"],"envelope_problems":malformed_envelope_verification["problems"]}})

        # Exercise the exact PERF-02 perf_action wrapper with its runtime action
        # label, but a self-test-only sleeping process tree before product import.
        from performance import _sample_action
        perf_timeout_scratch=temp/"perf02-timeout-scratch"; perf_timeout_scratch.mkdir(); perf_timeout_declared=perf_timeout_scratch/"declared"; perf_timeout_declared.mkdir()
        perf_timeout_context={"scratch_root":str(perf_timeout_scratch),"declared_root":str(perf_timeout_declared),"candidate_root":str(args.candidate),"python_executable":str(runtime),"harness_root":str(HARNESS_ROOT),"case":{"case_id":"perf02-runtime-selftest","recipe":"perf_runtime","timeout_policy":{"performance_action_seconds":1}}}
        perf_timeout_observation=_sample_action(perf_timeout_context,{"action":"runtime","harness_selftest_sleep_tree":True,"sleep_seconds":120},"warmup")
        perf_partial=(perf_timeout_declared/"performance-transcripts"/"warmup.stdout.bin").read_bytes()
        perf_bounded=perf_timeout_observation["bounded_process"]
        checks.append({"name":"actual_perf02_wrapper_runtime_action_timeout_tree_death","passed":perf_timeout_observation["timed_out"] and perf_timeout_observation["timeout_seconds"]==1.0 and b"PERF02_TIMEOUT_SELFTEST_PARTIAL_STDOUT" in perf_partial and len(perf_bounded["process_tree"]["descendant_pids_before_termination_or_close"])>=2 and perf_bounded["process_tree"]["created_suspended"] and perf_bounded["process_tree"]["assigned_before_resume"] and perf_bounded["process_tree"]["pid_states_unambiguously_dead"] and perf_bounded["process_tree"]["all_observed_processes_terminated"] and not perf_bounded["retry_performed"],"details":{"action":"runtime","label":"warmup","timeout_seconds":perf_timeout_observation["timeout_seconds"],"elapsed_seconds":perf_bounded["elapsed_seconds"],"partial_stdout":perf_bounded["stdout"],"process_tree":perf_bounded["process_tree"],"retry_performed":perf_bounded["retry_performed"],"product_imported":False}})

        # The root's first fixture action spawns a child and exits. Suspended
        # creation proves Job assignment occurred before that first instruction;
        # active Job descendants are then explicitly terminated after root exit.
        orphan_declared=temp/"immediate-orphan"; orphan_declared.mkdir()
        orphan_process=run_bounded_process([str(runtime),"-B",str(HARNESS_ROOT/"perf_action.py"),"--selftest-immediate-orphan"],timeout_seconds=10,stdout_path=orphan_declared/"stdout.bin",stderr_path=orphan_declared/"stderr.bin")
        orphan_tree=orphan_process["process_tree"]
        checks.append({"name":"windows_suspended_assign_before_first_instruction_immediate_orphan_contained","passed":orphan_process["root_exit_code"]==0 and orphan_tree["created_suspended"] and orphan_tree["assigned_before_resume"] and orphan_tree["resume_previous_suspend_count"]==1 and orphan_tree["job_active_processes_before_cleanup"]>=1 and orphan_tree["termination_requested"] and orphan_tree["job_active_processes_after_cleanup"]==0 and orphan_tree["pid_states_unambiguously_dead"] and orphan_tree["all_observed_processes_terminated"],"details":{"process":orphan_process,"product_imported":False}})

        # A fast writer may exit before the polling loop observes the cap. The
        # joined reader state must still force a neutral output-limit status.
        fast_output_declared=temp/"fast-output"; fast_output_declared.mkdir(); fast_output_bytes=(16*1024*1024)+(64*1024)
        def wait_until_fast_writer_exits(process):
            process.wait(timeout=30)
            return None
        fast_output_process=run_bounded_process([str(runtime),"-B",str(HARNESS_ROOT/"perf_action.py"),"--selftest-fast-output-bytes",str(fast_output_bytes)],timeout_seconds=30,stdout_path=fast_output_declared/"stdout.bin",stderr_path=fast_output_declared/"stderr.bin",sample_callback=wait_until_fast_writer_exits)
        checks.append({"name":"fast_exit_output_cap_reconciled_after_reader_join","passed":fast_output_process["status"]=="output_limit_exceeded" and fast_output_process["output_limit_exceeded"] and not fast_output_process["output_limit_detected_during_monitor"] and fast_output_process["output_limit_detected_after_join"] and fast_output_process["root_exit_code"]==0 and not fast_output_process["process_tree"]["termination_requested"] and fast_output_process["stdout"]["truncated"] and fast_output_process["stdout"]["total_observed_bytes"]==fast_output_bytes and fast_output_process["stdout"]["captured_bytes"]==16*1024*1024 and fast_output_process["process_tree"]["all_observed_processes_terminated"] and not fast_output_process["retry_performed"],"details":{"process":fast_output_process,"product_imported":False}})

        resource_scratch=temp/"resource-limit"; resource_declared=resource_scratch/"declared"; resource_declared.mkdir(parents=True); (resource_scratch/"quota-payload.bin").write_bytes(b"Q"*64)
        resource_sampler=_ScratchQuotaSampler(resource_scratch,limit_bytes=32,interval_seconds=0)
        resource_process=run_bounded_process([str(runtime),"-B",str(HARNESS_ROOT/"perf_action.py"),"--selftest-descendant","grandchild"],timeout_seconds=30,stdout_path=resource_declared/"stdout.bin",stderr_path=resource_declared/"stderr.bin",sample_callback=resource_sampler)
        checks.append({"name":"actual_scratch_sampler_limit_neutral_tree_cleanup","passed":resource_process["status"]=="resource_limit_exceeded" and resource_process["resource_limit_exceeded"] and resource_process["resource_limit_evidence"]["schema"]=="ck3chronicle.phase1-scratch-quota-observation" and not resource_process["resource_limit_evidence"]["post_exit_forced_sample"] and resource_process["process_tree"]["all_observed_processes_terminated"] and not resource_process["retry_performed"],"details":{"process":resource_process,"scratch_high_water_bytes":resource_sampler.high_water_bytes,"product_imported":False}})

        post_quota_scratch=temp/"post-exit-resource-limit"; post_quota_declared=post_quota_scratch/"declared"; post_quota_declared.mkdir(parents=True); (post_quota_scratch/"quota-payload.bin").write_bytes(b"Q"*64)
        post_quota_process=run_bounded_process([str(runtime),"-B","-c","pass"],timeout_seconds=30,stdout_path=post_quota_declared/"stdout.bin",stderr_path=post_quota_declared/"stderr.bin")
        post_quota_sampler=_ScratchQuotaSampler(post_quota_scratch,limit_bytes=32,interval_seconds=3600)
        post_quota_observation=_reconcile_post_exit_scratch_quota(post_quota_process,post_quota_sampler)
        checks.append({"name":"actual_post_exit_scratch_quota_reconciliation","passed":post_quota_process["root_exit_code"]==0 and post_quota_process["status"]=="resource_limit_exceeded" and post_quota_process["resource_limit_exceeded"] and post_quota_observation is not None and post_quota_observation["post_exit_forced_sample"] and post_quota_process["process_tree"]["all_observed_processes_terminated"],"details":{"process":post_quota_process,"scratch_observation":post_quota_observation,"product_imported":False}})

        sampler_declared=temp/"sampler-failure"; sampler_declared.mkdir()
        def selftest_sampler_failure(_process):
            raise RuntimeError("injected sampler failure")
        sampler_process=run_bounded_process([str(runtime),"-B",str(HARNESS_ROOT/"perf_action.py"),"--selftest-descendant","grandchild"],timeout_seconds=30,stdout_path=sampler_declared/"stdout.bin",stderr_path=sampler_declared/"stderr.bin",sample_callback=selftest_sampler_failure)
        checks.append({"name":"sampler_exception_fail_closed_process_tree_cleanup","passed":sampler_process["status"]=="sampler_failed" and "injected sampler failure" in sampler_process["sampler_error"] and sampler_process["process_tree"]["all_observed_processes_terminated"],"details":{"process":sampler_process,"product_imported":False}})

        nested_scratch=temp/"perf02-nested-worker-scratch"; nested_declared=nested_scratch/"declared"; nested_declared.mkdir(parents=True)
        nested_context={"scratch_root":str(nested_scratch),"declared_root":str(nested_declared),"candidate_root":str(args.candidate),"corpus_root":str(args.corpus),"python_executable":str(runtime),"harness_root":str(HARNESS_ROOT),"case":{"case_id":"perf02-runtime-selftest","gate":"SELFTEST","recipe":"perf_runtime","timeout_policy":{"performance_action_seconds":1,"overall_case_seconds":10,"product_subprocess_default_seconds":5}},"harness_selftest_perf02_timeout":True}
        nested_request=nested_scratch/"case-request.json"; write_canonical_json(nested_request,nested_context)
        nested_outer=run_bounded_process([str(runtime),"-B",str(HARNESS_ROOT/"case_worker.py"),"--request",str(nested_request)],timeout_seconds=10,stdout_path=nested_declared/"worker.stdout.bin",stderr_path=nested_declared/"worker.stderr.bin",env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1","PYTHONPATH":os.pathsep.join((str(HARNESS_ROOT),str(args.candidate/"src")))})
        nested_result=read_json(nested_declared/"observation.json"); nested_action=nested_result["observation"]; nested_bounded=nested_action["bounded_process"]
        checks.append({"name":"perf02_nested_action_job_inside_overall_worker_job","passed":nested_outer["status"]=="completed" and nested_outer["root_exit_code"]==0 and nested_outer["process_tree"]["job_object_assigned"] and nested_outer["process_tree"]["assigned_before_resume"] and nested_action["timed_out"] and nested_action["timeout_seconds"]==1.0 and nested_bounded["process_tree"]["job_object_assigned"] and nested_bounded["process_tree"]["assigned_before_resume"] and len(nested_bounded["process_tree"]["descendant_pids_before_termination_or_close"])>=2 and nested_bounded["process_tree"]["pid_states_unambiguously_dead"] and nested_bounded["process_tree"]["all_observed_processes_terminated"] and nested_result["timeout_observed"] and not nested_bounded["retry_performed"],"details":{"outer_worker":nested_outer,"inner_action":nested_action,"neutral_observation":nested_result,"product_imported":False}})

        # Outer case watchdog: close the timeout neutrally, execute the next
        # synthetic case once, and aggregate both immutable envelopes.
        timeout_result_root=temp/"timeout-continuation-results"; timeout_scratch_root=temp/"timeout-continuation-scratch"; timeout_bindings=_result_bindings("b"*64,"c"*64)
        initialize_results(timeout_result_root,timeout_scratch_root,plan_sha256="b"*64,harness_manifest_sha256="c"*64)
        timeout_case={"case_id":"timeout-case","gate":"SELFTEST","recipe":"selftest_case_watchdog","inputs":[]}; continuation_case={"case_id":"continuation-case","gate":"SELFTEST","recipe":"selftest_continuation","inputs":[]}; timeout_cases={timeout_case["case_id"]:timeout_case,continuation_case["case_id"]:continuation_case}
        timeout_case_scratch=new_scratch_directory(timeout_scratch_root,timeout_case["case_id"]); timeout_case_declared=timeout_case_scratch/"declared"; timeout_case_declared.mkdir(); timeout_request={"case":timeout_case,"scratch_root":str(timeout_case_scratch),"declared_root":str(timeout_case_declared),"harness_root":str(HARNESS_ROOT),"harness_selftest_case_watchdog":True}; timeout_request_path=timeout_case_scratch/"case-request.json"; write_canonical_json(timeout_request_path,timeout_request)
        timeout_worker=run_bounded_process([str(runtime),"-B",str(HARNESS_ROOT/"case_worker.py"),"--request",str(timeout_request_path)],timeout_seconds=1,stdout_path=timeout_case_declared/"worker.stdout.bin",stderr_path=timeout_case_declared/"worker.stderr.bin",env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1","PYTHONPATH":str(HARNESS_ROOT)})
        timeout_neutral={"schema":"ck3chronicle.phase1-case-timeout-observation","schema_version":1,"classification":"neutral_infrastructure_observation_no_harness_gate_verdict","case_id":timeout_case["case_id"],"bounded_process":timeout_worker,"retry_performed":False,"harness_pass_fail_categorization":None}; write_canonical_json(timeout_case_declared/"timeout-observation.json",timeout_neutral)
        timeout_close=close_case(results_root=timeout_result_root,scratch_case=timeout_case_scratch,case=timeout_case,execution={"worker_timed_out":True,"bounded_worker_process":timeout_worker,"product_case_attempts":1,"retry_performed":False,"harness_pass_fail_categorization":None})
        continuation_scratch=new_scratch_directory(timeout_scratch_root,continuation_case["case_id"]); continuation_declared=continuation_scratch/"declared"; continuation_declared.mkdir()
        continuation_process=run_bounded_process([str(runtime),"-B","-c","print('CONTINUATION_AFTER_TIMEOUT')"],timeout_seconds=10,stdout_path=continuation_declared/"worker.stdout.bin",stderr_path=continuation_declared/"worker.stderr.bin")
        write_canonical_json(continuation_declared/"observation.json",{"case_id":continuation_case["case_id"],"neutral":True,"bounded_process":continuation_process})
        continuation_close=close_case(results_root=timeout_result_root,scratch_case=continuation_scratch,case=continuation_case,execution={"worker_timed_out":False,"bounded_worker_process":continuation_process,"product_case_attempts":1,"retry_performed":False})
        timeout_aggregate=close_result_set(timeout_result_root,timeout_cases,timeout_bindings); timeout_result_verification=verify_result_set(timeout_result_root,require_closed=True,expected_cases=timeout_cases,expected_bindings=timeout_bindings)
        timeout_partial=(timeout_result_root/"cases"/timeout_case["case_id"]/"artifacts"/"worker.stdout.bin").read_bytes()
        checks.append({"name":"overall_case_timeout_neutral_close_continuation_and_aggregate","passed":timeout_worker["timed_out"] and b"CASE_WATCHDOG_SELFTEST_PARTIAL_STDOUT" in timeout_partial and len(timeout_worker["process_tree"]["descendant_pids_before_termination_or_close"])>=2 and timeout_worker["process_tree"]["assigned_before_resume"] and timeout_worker["process_tree"]["pid_states_unambiguously_dead"] and timeout_worker["process_tree"]["all_observed_processes_terminated"] and timeout_close["scratch_deleted"] and continuation_process["status"]=="completed" and continuation_process["root_exit_code"]==0 and continuation_close["scratch_deleted"] and timeout_result_verification["verified"] and timeout_aggregate["case_count"]==2,"details":{"timeout_seconds":timeout_worker["timeout_seconds"],"elapsed_seconds":timeout_worker["elapsed_seconds"],"timeout_stdout":timeout_worker["stdout"],"timeout_process_tree":timeout_worker["process_tree"],"timeout_case_marker":timeout_close["completion_marker_sha256"],"continuation_status":continuation_process["status"],"continuation_case_marker":continuation_close["completion_marker_sha256"],"aggregate":timeout_aggregate,"verification_problems":timeout_result_verification["problems"],"product_gate_execution":False}})

        result_root=temp/"result-proof"; scratch_root=temp/"scratch-proof"
        initialize_results(result_root,scratch_root,plan_sha256="0"*64,harness_manifest_sha256="1"*64)
        scratch_case=new_scratch_directory(scratch_root,"selftest-case"); declared=scratch_case/"declared"; declared.mkdir(); (declared/"exact.stdout").write_bytes(b"self-test exact bytes\r\n")
        synthetic_case={"case_id":"selftest-case","gate":"SELFTEST","recipe":"self_test_only","inputs":[]}
        journal_entry=close_case(results_root=result_root,scratch_case=scratch_case,case=synthetic_case,execution={"worker_exit_code":0,"product_case_attempts":0})
        selftest_cases={"selftest-case":synthetic_case}; selftest_bindings=_result_bindings("0"*64,"1"*64)
        aggregate=close_result_set(result_root,selftest_cases,selftest_bindings); result_verification=verify_result_set(result_root,require_closed=True,expected_cases=selftest_cases,expected_bindings=selftest_bindings)
        checks.append({"name":"bounded_case_and_aggregate_closure","passed":journal_entry["scratch_deleted"] and result_verification["verified"] and aggregate["case_count"]==1 and (result_root/"runner-result.manifest.json").is_file() and (result_root/"runner-result.journal.json").is_file() and (result_root/RESULT_COMPLETION_MARKER).is_file(),"details":{"journal":journal_entry,"aggregate":aggregate,"verification_problems":result_verification["problems"]}})
        (result_root/"unexpected-read-only.txt").write_bytes(b"tamper")
        (result_root/"unexpected-read-only.txt").chmod(stat.S_IREAD|stat.S_IRGRP|stat.S_IROTH)
        tampered=verify_result_set(result_root,require_closed=True,expected_cases=selftest_cases,expected_bindings=selftest_bindings)
        checks.append({"name":"closed_result_unexpected_top_file_rejected","passed":not tampered["verified"] and "result_set_exact_top_file_set" in tampered["problems"],"details":{"verification_problems":tampered["problems"]}})
        payload = {"schema": "ck3chronicle.phase1-harness-self-test", "schema_version": 1, "classification": "synthetic_publication_faults_plus_public_runner_and_failed-result_metadata_probes", "product_gate_execution": False, "private_material_accessed": False, "expected_answer_accessed": False, "passed": all(item["passed"] for item in checks), "checks": checks}
        write_canonical_json(HARNESS_ROOT / "self-test.json", payload)
        print(json.dumps(payload, sort_keys=True))
        return 0 if payload["passed"] else 2
    finally:
        def make_writable_and_retry(function, path, _error_info):
            os.chmod(path, stat.S_IWRITE|stat.S_IREAD)
            function(path)
        shutil.rmtree(temp, onerror=make_writable_and_retry)


def calibrate(args: argparse.Namespace) -> int:
    runtime = _canonical_evaluator_runtime(args)
    output = HARNESS_ROOT / "calibration.json"
    env = os.environ.copy(); env["PYTHONPATH"] = os.pathsep.join((str(HARNESS_ROOT), str(args.candidate / "src"))); env["PYTHONDONTWRITEBYTECODE"] = "1"
    locator_log=args.corpus/"units"/"PUB-LONG-20260429"/"error.log"
    completed = subprocess.run([str(runtime), "-B", str(HARNESS_ROOT / "calibration_probe.py"), "--output", str(output), "--locator-log", str(locator_log)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=600)
    if completed.returncode:
        raise RuntimeError("calibration failed: " + completed.stderr.decode("utf-8", "replace"))
    payload = read_json(output)
    payload["probe_stdout_sha256"] = hashlib.sha256(completed.stdout).hexdigest(); payload["probe_stderr_sha256"] = hashlib.sha256(completed.stderr).hexdigest()
    write_canonical_json(output, payload)
    print(json.dumps({"calibration": str(output), "sha256": sha256_file(output), "product_gate_execution": False}, sort_keys=True))
    return 0


def _harness_files() -> list[Path]:
    ignored = {"harness.manifest.json"}
    entries = nofollow_tree_entries(HARNESS_ROOT)
    special = [path.relative_to(HARNESS_ROOT).as_posix() for path, kind in entries if kind == "special"]
    if special:
        raise RuntimeError("special harness entries are forbidden: " + ",".join(special))
    return [path for path, kind in entries if kind == "file" and path.name not in ignored and "__pycache__" not in path.parts]


def freeze(args: argparse.Namespace) -> int:
    required = ("public-run-plan.json", "authority-preflight.json", "dry-run.json", "mutation-preflight.json", "timeout-table.json", "self-test.json", "calibration.json", "independent-review.json")
    missing = [name for name in required if not (HARNESS_ROOT / name).is_file()]
    if missing: raise RuntimeError("freeze prerequisites missing: " + ", ".join(missing))
    review = read_json(HARNESS_ROOT / "independent-review.json")
    if review.get("verdict") != "GO": raise RuntimeError("independent reviewer has not issued GO")
    for cache, kind in nofollow_tree_entries(HARNESS_ROOT):
        if kind == "directory" and cache.name == "__pycache__":
            if os.path.commonpath((str(HARNESS_ROOT), str(Path(os.path.abspath(cache))))) != str(HARNESS_ROOT):
                raise RuntimeError(f"refusing cache cleanup outside harness: {cache}")
            shutil.rmtree(cache)
    entries = [file_identity(path, HARNESS_ROOT) for path in _harness_files()]
    manifest = {
        "schema": HARNESS_SCHEMA,
        "schema_version": 1,
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_tree": CANDIDATE_TREE,
        "candidate_manifest_sha256": CANDIDATE_MANIFEST_SHA256,
        "candidate_source_set_sha256": CANDIDATE_SOURCE_SET_SHA256,
        "corpus_manifest_sha256": CORPUS_MANIFEST_SHA256,
        "corpus_source_set_sha256": CORPUS_SOURCE_SET_SHA256,
        "public_run_plan_sha256": sha256_file(_plan_path()),
        "file_count": len(entries),
        "files": entries,
        "source_set_algorithm": "sha256(canonical-json(sorted [{path,bytes,sha256}]))",
        "source_set_sha256": source_set_hash(entries),
        "expected_answers_embedded": False,
        "scorer_logic_embedded": False,
        "private_holdout_embedded": False,
        "scorer_only_answer_identity": {"relative_path": SCORER_ONLY_RELATIVE_PATH, "staged_by_runner": False},
        "frozen_at_utc": utc_now(),
    }
    manifest_hash = write_canonical_json(_manifest_path(), manifest)
    for path in [*_harness_files(), _manifest_path()]:
        path.chmod(stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
    verification = verify_harness_manifest()
    print(json.dumps({"harness_root": str(HARNESS_ROOT), "manifest_path": str(_manifest_path()), "manifest_sha256": manifest_hash, "source_set_sha256": manifest["source_set_sha256"], "verification": verification}, sort_keys=True))
    return 0


def verify_harness_manifest() -> dict[str, Any]:
    manifest = read_json(_manifest_path()); problems=[]; actual=[]
    bytecode_entries = [path.relative_to(HARNESS_ROOT).as_posix() for path, kind in nofollow_tree_entries(HARNESS_ROOT) if (kind == "directory" and path.name == "__pycache__") or (kind == "file" and path.suffix == ".pyc")]
    if bytecode_entries:
        problems.append("post_freeze_bytecode:" + ",".join(sorted(bytecode_entries)))
    for entry in manifest["files"]:
        path = HARNESS_ROOT / Path(entry["path"])
        if not path.is_file() or path.stat().st_size != int(entry["bytes"]) or sha256_file(path) != entry["sha256"]: problems.append(f"file:{entry['path']}")
        elif path.stat().st_mode & stat.S_IWUSR: problems.append(f"writable:{entry['path']}")
        actual.append(entry)
    expected_paths={str(entry["path"]) for entry in manifest["files"]}
    disk_paths={path.relative_to(HARNESS_ROOT).as_posix() for path in _harness_files()}
    if disk_paths != expected_paths: problems.append("exact_harness_file_set")
    if source_set_hash(actual) != manifest["source_set_sha256"]: problems.append("source_set")
    if _manifest_path().stat().st_mode & stat.S_IWUSR: problems.append("writable:harness.manifest.json")
    return {"verified": not problems, "problems": problems, "manifest_sha256": sha256_file(_manifest_path()), "source_set_sha256": manifest["source_set_sha256"], "file_count": len(actual)}


def verify_harness(args: argparse.Namespace) -> int:
    report = verify_harness_manifest(); print(json.dumps(report, sort_keys=True)); return 0 if report["verified"] else 2


def init_results(args: argparse.Namespace) -> int:
    _canonical_evaluator_runtime(args)
    verification = verify_harness_manifest()
    if not verification["verified"]: raise RuntimeError("harness is not frozen/verified")
    assert_isolated_paths(results_root=args.results_root, scratch_root=args.scratch_root, candidate_root=args.candidate, corpus_root=args.corpus, harness_root=HARNESS_ROOT)
    payload = initialize_results(args.results_root, args.scratch_root, plan_sha256=sha256_file(_plan_path()), harness_manifest_sha256=verification["manifest_sha256"])
    print(json.dumps(payload, sort_keys=True)); return 0


class _ScratchQuotaSampler:
    def __init__(self, root: Path, limit_bytes: int, interval_seconds: float = 0.25) -> None:
        self.root=root; self.limit_bytes=limit_bytes; self.interval_seconds=interval_seconds
        self.sampled_at=0.0; self.high_water_bytes=0

    def sample(self, _process=None, *, force: bool = False) -> dict[str,Any] | None:
        now=time.perf_counter()
        if not force and now-self.sampled_at<self.interval_seconds:
            return None
        self.sampled_at=now; total=0; files=0
        try:
            scratch_entries=nofollow_tree_entries(self.root)
        except FileNotFoundError:
            return None
        for path,kind in scratch_entries:
            if kind=="special":
                raise RuntimeError(f"special entry in case scratch: {path.relative_to(self.root).as_posix()}")
            if kind=="file":
                try:
                    total+=path.stat().st_size; files+=1
                except FileNotFoundError:
                    continue
        self.high_water_bytes=max(self.high_water_bytes,total)
        if total>self.limit_bytes:
            return {"schema":"ck3chronicle.phase1-scratch-quota-observation","schema_version":1,"limit_bytes":self.limit_bytes,"observed_bytes":total,"observed_file_count":files,"sample_interval_seconds":self.interval_seconds,"post_exit_forced_sample":force}
        return None

    def __call__(self, process) -> dict[str,Any] | None:
        return self.sample(process)


def _reconcile_post_exit_scratch_quota(process: dict[str,Any], sampler: _ScratchQuotaSampler) -> dict[str,Any] | None:
    observation=sampler.sample(force=True)
    if observation is not None:
        process["resource_limit_exceeded"]=True; process["resource_limit_evidence"]=observation
        if process["status"]=="completed": process["status"]="resource_limit_exceeded"
    return observation


def run_case(args: argparse.Namespace) -> int:
    harness_verification=verify_harness_manifest()
    if not harness_verification["verified"]: raise RuntimeError("harness manifest verification failed")
    runtime, authority, runner_child_probe = _blind_runner_preflight(args)
    plan=read_json(_plan_path()); by_id={case["case_id"]:case for case in plan["cases"]}
    if args.case_id not in by_id: raise KeyError(args.case_id)
    case=by_id[args.case_id]
    if case["gate"]=="P1-HOLD-01": raise RuntimeError("P1-HOLD-01 is unassigned and unexecutable")
    expected_cases={case_id:item for case_id,item in by_id.items() if item["gate"]!="P1-HOLD-01"}
    expected_bindings=_result_bindings(sha256_file(_plan_path()),harness_verification["manifest_sha256"])
    open_verification=verify_result_set(args.results_root,expected_cases=expected_cases,expected_bindings=expected_bindings)
    if not open_verification["verified"]: raise RuntimeError("open result set verification failed: "+json.dumps(open_verification["problems"],sort_keys=True))
    result_set=read_json(args.results_root/"result-set.json"); scratch_root=Path(result_set["scratch_root"])
    assert_isolated_paths(results_root=args.results_root,scratch_root=scratch_root,candidate_root=args.candidate,corpus_root=args.corpus,harness_root=HARNESS_ROOT)
    if (args.results_root/"cases"/args.case_id).exists(): raise FileExistsError("case already executed; retries are forbidden")
    scratch_case=new_scratch_directory(scratch_root,args.case_id); declared=scratch_case/"declared"; declared.mkdir()
    request={"case":case,"candidate_root":str(Path(os.path.abspath(args.candidate))),"corpus_root":str(Path(os.path.abspath(args.corpus))),"scratch_root":str(scratch_case),"declared_root":str(declared),"harness_root":str(HARNESS_ROOT),"python_executable":str(runtime)}
    request_path=scratch_case/"case-request.json"; write_canonical_json(request_path,request)
    env=os.environ.copy(); env["PYTHONPATH"]=os.pathsep.join((str(HARNESS_ROOT),str(args.candidate/"src"))); env["PYTHONDONTWRITEBYTECODE"]="1"; env["LOCALAPPDATA"]=str(scratch_case/"worker-local"); env["USERPROFILE"]=str(scratch_case/"worker-profile")
    env["CK3CHRONICLE_PHASE1_PRODUCT_SUBPROCESS_TIMEOUT_SECONDS"]=str(case["timeout_policy"]["product_subprocess_default_seconds"])
    worker_command=[str(runtime),"-B",str(HARNESS_ROOT/"case_worker.py"),"--request",str(request_path)]
    scratch_sampler=_ScratchQuotaSampler(scratch_case,int(case["timeout_policy"]["scratch_case_limit_bytes"]))
    worker_process=run_bounded_process(worker_command,timeout_seconds=float(case["timeout_policy"]["overall_case_seconds"]),stdout_path=declared/"worker.stdout.bin",stderr_path=declared/"worker.stderr.bin",env=env,sample_callback=scratch_sampler)
    _reconcile_post_exit_scratch_quota(worker_process,scratch_sampler)
    if not worker_process["process_tree"]["all_observed_processes_terminated"]:
        raise RuntimeError("worker process tree survived bounded termination")
    if worker_process["sampler_error"]:
        raise RuntimeError("case resource sampler failed after process-tree cleanup: "+worker_process["sampler_error"])
    bounded_termination=worker_process["timed_out"] or worker_process["output_limit_exceeded"] or worker_process["resource_limit_exceeded"]
    if bounded_termination:
        timeout_observation={"schema":"ck3chronicle.phase1-case-bounded-termination-observation","schema_version":1,"classification":"neutral_infrastructure_observation_no_harness_gate_verdict","case_id":case["case_id"],"gate":case["gate"],"recipe":case["recipe"],"active_scope":"overall_case_worker_process_tree","timeout_policy":case["timeout_policy"],"bounded_process":worker_process,"retry_performed":False,"harness_pass_fail_categorization":None}
        write_canonical_json(declared/"bounded-termination-observation.json",timeout_observation)
    execution={"worker_exit_code":worker_process["root_exit_code"],"worker_timed_out":worker_process["timed_out"],"worker_output_limit_exceeded":worker_process["output_limit_exceeded"],"worker_resource_limit_exceeded":worker_process["resource_limit_exceeded"],"scratch_high_water_observed_bytes":scratch_sampler.high_water_bytes,"timeout_policy":case["timeout_policy"],"timeout_classification":"neutral_observation_no_harness_gate_verdict","bounded_worker_process":worker_process,"worker_stdout":file_identity(declared/"worker.stdout.bin",declared),"worker_stderr":file_identity(declared/"worker.stderr.bin",declared),"authority_verification_sha256":hashlib.sha256(canonical_json_bytes(authority)).hexdigest(),"runner_child_metadata_probe":runner_child_probe,"python_runtime":file_identity(runtime),"host":host_identity(),"product_case_attempts":1,"retry_performed":False}
    journal=close_case(results_root=args.results_root,scratch_case=scratch_case,case=case,execution=execution)
    print(json.dumps(journal,sort_keys=True)); return 0 if worker_process["root_exit_code"]==0 or bounded_termination else 2


def close_results(args: argparse.Namespace) -> int:
    harness_verification=verify_harness_manifest()
    if not harness_verification["verified"]: raise RuntimeError("harness manifest verification failed")
    plan=read_json(_plan_path()); expected={case["case_id"]:case for case in plan["cases"] if case["gate"]!="P1-HOLD-01"}; bindings=_result_bindings(sha256_file(_plan_path()),harness_verification["manifest_sha256"]); result=close_result_set(args.results_root,expected,bindings); verification=verify_result_set(args.results_root,require_closed=True,expected_cases=expected,expected_bindings=bindings)
    if not verification["verified"]: raise RuntimeError("aggregate post-close verification failed: "+json.dumps(verification["problems"],sort_keys=True))
    print(json.dumps({"close":result,"verification":verification},sort_keys=True)); return 0


def verify_results(args: argparse.Namespace) -> int:
    harness_verification=verify_harness_manifest()
    if not harness_verification["verified"]: raise RuntimeError("harness manifest verification failed")
    plan=read_json(_plan_path()); expected={case["case_id"]:case for case in plan["cases"] if case["gate"]!="P1-HOLD-01"}; bindings=_result_bindings(sha256_file(_plan_path()),harness_verification["manifest_sha256"]); report=verify_result_set(args.results_root,require_closed=args.require_closed,expected_cases=expected,expected_bindings=bindings); print(json.dumps(report,sort_keys=True)); return 0 if report["verified"] else 2


def parser() -> argparse.ArgumentParser:
    common=argparse.ArgumentParser(add_help=False); common.add_argument("--candidate",type=Path,default=DEFAULT_CANDIDATE); common.add_argument("--candidate-manifest",type=Path,default=DEFAULT_CANDIDATE_MANIFEST); common.add_argument("--corpus",type=Path,default=DEFAULT_CORPUS); common.add_argument("--python-executable",type=Path)
    root=argparse.ArgumentParser(description=__doc__); sub=root.add_subparsers(dest="command",required=True)
    p=sub.add_parser("build-artifacts",parents=[common]); p.set_defaults(func=build_artifacts)
    p=sub.add_parser("verify-authorities",parents=[common]); p.set_defaults(func=lambda a:(print(json.dumps(verify_authorities(a.candidate,a.candidate_manifest,a.corpus),sort_keys=True)) or 0))
    p=sub.add_parser("dry-run",parents=[common]); p.add_argument("--output",type=Path); p.add_argument("--results-root",type=Path); p.add_argument("--scratch-root",type=Path); p.set_defaults(func=dry_run)
    p=sub.add_parser("self-test",parents=[common]); p.set_defaults(func=self_test)
    p=sub.add_parser("calibrate",parents=[common]); p.set_defaults(func=calibrate)
    p=sub.add_parser("blind-runner-probe",parents=[common]); p.set_defaults(func=blind_runner_probe)
    p=sub.add_parser("child-metadata-probe",parents=[common]); p.set_defaults(func=child_metadata_probe)
    p=sub.add_parser("freeze",parents=[common]); p.set_defaults(func=freeze)
    p=sub.add_parser("verify-harness"); p.set_defaults(func=verify_harness)
    p=sub.add_parser("init-results",parents=[common]); p.add_argument("--results-root",type=Path,required=True); p.add_argument("--scratch-root",type=Path,required=True); p.set_defaults(func=init_results)
    p=sub.add_parser("run-case",parents=[common]); p.add_argument("--results-root",type=Path,required=True); p.add_argument("--case-id",required=True); p.set_defaults(func=run_case)
    p=sub.add_parser("close-results"); p.add_argument("--results-root",type=Path,required=True); p.set_defaults(func=close_results)
    p=sub.add_parser("verify-results"); p.add_argument("--results-root",type=Path,required=True); p.add_argument("--require-closed",action="store_true"); p.set_defaults(func=verify_results)
    return root


def main() -> int:
    args=parser().parse_args(); return int(args.func(args))


if __name__=="__main__": raise SystemExit(main())
