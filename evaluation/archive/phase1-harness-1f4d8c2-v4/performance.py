"""Warmup/five-measurement orchestration with wall/CPU/RSS observations."""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any

from candidate_runtime import direct_capture_process, finalize_and_register_without_derivation, isolated_cli_environment, table_projection
from harness_core import file_identity, host_identity, sha256_file, stage_unit, write_canonical_json
from process_control import run_bounded_process


def _windows_rss(handle: int) -> int | None:
    if os.name != "nt":
        return None
    class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong), ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t), ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t), ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t), ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]
    counters = PROCESS_MEMORY_COUNTERS(); counters.cb = ctypes.sizeof(counters)
    ok = ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.c_void_p(handle), ctypes.byref(counters), counters.cb)
    return int(counters.WorkingSetSize) if ok else None


def _sample_action(context: dict[str, Any], request: dict[str, Any], label: str) -> dict[str, Any]:
    scratch = Path(context["scratch_root"]); candidate = Path(context["candidate_root"]); python = Path(context["python_executable"]); harness = Path(context["harness_root"])
    request_path = scratch / "perf-requests" / f"{label}.json"; request_path.parent.mkdir(parents=True, exist_ok=True); write_canonical_json(request_path, request)
    evidence = Path(request.get("evidence_root", scratch / "perf-profile" / "local" / "ck3chronicle"))
    if evidence.name != "ck3chronicle": evidence = scratch / "perf-profile" / "local" / "ck3chronicle"
    evidence.mkdir(parents=True, exist_ok=True)
    env = isolated_cli_environment(candidate, evidence, harness)
    command = [str(python), "-B", str(harness / "perf_action.py"), "--request", str(request_path)]
    peak_rss = 0; samples = 0
    def sample(process) -> None:
        nonlocal peak_rss, samples
        rss = _windows_rss(int(process._handle)) if os.name == "nt" else None  # type: ignore[attr-defined]
        if rss is not None: peak_rss = max(peak_rss, rss); samples += 1
    transcript_root=Path(context["declared_root"])/"performance-transcripts"; transcript_root.mkdir(parents=True,exist_ok=True)
    stdout_path=transcript_root/f"{label}.stdout.bin"; stderr_path=transcript_root/f"{label}.stderr.bin"
    ceiling=float(context["case"]["timeout_policy"]["performance_action_seconds"])
    process=run_bounded_process(command,timeout_seconds=ceiling,stdout_path=stdout_path,stderr_path=stderr_path,env=env,sample_callback=sample)
    if process["sampler_error"] or not process["process_tree"]["all_observed_processes_terminated"]:
        raise RuntimeError("performance child cleanup could not be proven")
    stdout=stdout_path.read_bytes(); stderr=stderr_path.read_bytes()
    parsed = None
    if stdout:
        try: parsed = json.loads(stdout.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError): pass
    return {"label": label, "action": request["action"], "process_exit_code": process["root_exit_code"], "timed_out": process["timed_out"], "output_limit_exceeded": process["output_limit_exceeded"], "resource_limit_exceeded": process["resource_limit_exceeded"], "sampler_error": process["sampler_error"], "timeout_seconds": ceiling, "bounded_process": process, "peak_rss_bytes": peak_rss if samples else None, "rss_sample_count": samples, "stdout_bytes": len(stdout), "stdout_sha256": hashlib.sha256(stdout).hexdigest(), "stderr_bytes": len(stderr), "stderr_sha256": hashlib.sha256(stderr).hexdigest(), "measurement": parsed}


def _prepare_registered(context: dict[str, Any], source_logs: Path, label: str) -> tuple[Path, int]:
    scratch = Path(context["scratch_root"]); evidence = scratch / f"prep-{label}" / "local" / "ck3chronicle"; evidence.mkdir(parents=True)
    finalize_and_register_without_derivation(source_logs, evidence)
    import sqlite3
    conn = sqlite3.connect(evidence / "ck3chronicle.db"); session_id = int(conn.execute("SELECT session_id FROM sessions ORDER BY session_id DESC LIMIT 1").fetchone()[0]); conn.close()
    return evidence, session_id


def execute_performance_case(context: dict[str, Any]) -> dict[str, Any]:
    recipe = context["case"]["recipe"]; corpus = Path(context["corpus_root"]); scratch = Path(context["scratch_root"])
    source_logs = scratch / "perf-source"
    stage = stage_unit(corpus, "PUB-STRESS-20260806", source_logs)
    observations: list[dict[str, Any]] = []
    storage: dict[str, Any] | None = None
    for index in range(6):
        label = "warmup" if index == 0 else f"measured-{index}"
        if recipe == "perf_lexical":
            request = {"action": "lexical", "path": str(source_logs / "error.log")}
            observation = _sample_action(context, request, label)
        elif recipe in {"perf_parse", "perf_runtime"}:
            evidence, session_id = _prepare_registered(context, source_logs, label)
            request = {"action": "parse" if recipe == "perf_parse" else "runtime", "evidence_root": str(evidence), "session_id": session_id}
            observation = _sample_action(context, request, label)
            observation["stored_projection"] = None if observation["timed_out"] or observation["output_limit_exceeded"] else table_projection(evidence / "ck3chronicle.db")
            shutil.rmtree(evidence.parent.parent)
        elif recipe == "perf_pipeline":
            evidence = scratch / f"pipeline-{label}" / "local" / "ck3chronicle"; evidence.mkdir(parents=True)
            request = {"action": "pipeline", "source_logs": str(source_logs), "copy_target": str(evidence.parent.parent / "timed-copy"), "evidence_root": str(evidence)}
            observation = _sample_action(context, request, label)
            observation["stored_projection"] = None if observation["timed_out"] or observation["output_limit_exceeded"] else table_projection(evidence / "ck3chronicle.db")
            shutil.rmtree(evidence.parent.parent)
        else:
            if storage is None:
                evidence = scratch / "report-stored" / "local" / "ck3chronicle"; evidence.mkdir(parents=True)
                direct_capture_process(logs_root=source_logs, evidence_root=evidence, termination_kind="normal", observed_started_at="2026-08-16T00:00:00+00:00", observed_ended_at="2026-08-16T00:10:00+00:00")
                import sqlite3
                conn=sqlite3.connect(evidence/"ck3chronicle.db"); session_id=int(conn.execute("SELECT session_id FROM sessions ORDER BY session_id DESC LIMIT 1").fetchone()[0]); run_id=int(conn.execute("SELECT observation_id FROM capture_observations ORDER BY observation_id DESC LIMIT 1").fetchone()[0]); conn.close()
                storage={"evidence":evidence,"session_id":session_id,"run_id":run_id,"hash_before":sha256_file(evidence/"ck3chronicle.db")}
            surface=recipe.removeprefix("perf_report_")
            if surface=="function": request={"action":"report_function","evidence_root":str(storage["evidence"]),"session_id":storage["session_id"],"run_id":storage["run_id"]}
            else:
                command,mode=surface.rsplit("_",1); argv=[command,"--json"] if mode=="json" else [command]
                if command in {"report","errors"}: argv[1:1]=["--session",str(storage["session_id"])]
                request={"action":"report_cli","evidence_root":str(storage["evidence"]),"argv":argv}
            observation=_sample_action(context,request,label)
        observation["role"] = "unscored_warmup" if index == 0 else "measured"
        observations.append(observation)
        if observation["timed_out"] or observation["output_limit_exceeded"]:
            break
    if storage is not None:
        storage["hash_after"] = sha256_file(storage["evidence"] / "ck3chronicle.db")
        storage["evidence"] = str(storage["evidence"])
    measured=[item for item in observations if item["role"]=="measured"]
    return {"staged":stage,"repetition_policy":{"warmups":1,"measured":5,"retries":0},"observations":observations,"attempted_repetitions":len(observations),"measured_count":len(measured),"timeout_observed":any(item["timed_out"] for item in observations),"output_limit_observed":any(item["output_limit_exceeded"] for item in observations),"timeout_classification":"neutral_observation_no_harness_gate_verdict","storage":storage,"host":host_identity()}
