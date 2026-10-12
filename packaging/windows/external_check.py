"""Owner-run genuine installed checks; no synthetic history and no live watcher."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--capture-directory", type=Path)
    parser.add_argument("--check-repeat", action="store_true")
    args = parser.parse_args()
    bundle, state = args.bundle.resolve(), args.state.resolve()
    config_path = state / "settings/paths.toml"
    if not Path(sys.executable).resolve().is_relative_to(bundle):
        raise RuntimeError("Check must use this bundle's interpreter")
    from ck3chronicle.config import configure, load_config, paths_for, watcher_settings
    configure(config_path)
    document = load_config()
    roots = paths_for(document, config_path)
    if roots["root_wip"].resolve() != state / "data":
        raise RuntimeError("Setup selected different data; preserve it and review before continuing")
    database = watcher_settings().database
    evidence = state / "evidence"
    evidence.mkdir(exist_ok=True)
    result_path = state / "verification.json"
    if args.check_repeat:
        previous = json.loads(result_path.read_text(encoding="utf-8"))
        for path, expected in previous["preserved_files"].items():
            if sha(Path(path)) != expected:
                raise RuntimeError(f"Repeat setup changed stored evidence: {path}")
        if document["model"] != previous["selected_model"]:
            raise RuntimeError("Repeat setup changed selected model; review the deliberate choice")
        previous["repeat_setup_preserved"] = True
        previous["status"] = "bounded installed checks and repeat preservation passed"
        result_path.write_text(json.dumps(previous, indent=2) + "\n", encoding="utf-8")
        print("Repeat setup preserved database, captures, review files and selected model.")
        return
    commands = []
    def run(name, arguments, expected=0):
        completed = subprocess.run([str(x) for x in arguments], cwd=state, capture_output=True,
                                   text=True, encoding="utf-8", errors="replace", timeout=180)
        (evidence / (name + ".stdout")).write_text(completed.stdout, encoding="utf-8")
        (evidence / (name + ".stderr")).write_text(completed.stderr, encoding="utf-8")
        commands.append({"name": name, "args": [str(x) for x in arguments], "cwd": str(state), "exit": completed.returncode})
        (evidence / "commands.json").write_text(json.dumps(commands, indent=2) + "\n", encoding="utf-8")
        print(f"{name}: exit {completed.returncode}")
        if completed.returncode not in ((expected,) if isinstance(expected, int) else expected):
            raise RuntimeError(f"{name} failed; inspect its retained output")
        return completed.stdout
    cli = [bundle / "ck3chronicle.cmd", "--config", config_path]
    summary = {"status": "in_progress", "bundle": str(bundle), "config": str(config_path),
               "database": str(database), "python": sys.version, "executable": sys.executable,
               "sys_path": sys.path, "selected_model": document["model"], "clean_machine": False,
               "capture_and_reports": "unverified; no genuine capture supplied", "live_lifecycle": "unperformed",
               "repeat_setup_preserved": False}
    from ck3chronicle.pipeline import catalog
    import ck3chronicle
    summary["application"] = ck3chronicle.__file__
    summary["models_root"] = str(catalog.selected_models_root())
    if not all(Path(p).resolve().is_relative_to(bundle) for p in sys.path):
        raise RuntimeError("Interpreter import path escaped installed bundle")
    if not Path(summary["models_root"]).resolve().is_relative_to(bundle):
        raise RuntimeError("Model resources escaped installed bundle")
    try:
        run("verify-before", [bundle / "Verify.cmd"])
        run("help", [*cli, "--help"])
        run("start-help", [bundle / "Start.cmd", "--help"])
        run("watch-help", [*cli, "watch", "--help"])
        models = json.loads(run("models", [*cli, "setup", "--list-models", "--format", "json"]))
        summary["shipped_model"] = models["default"]
        doctor = json.loads(run("doctor", [*cli, "doctor", "--format", "json"], expected=(0, 2)))
        if any(f["severity"] == "error" for f in doctor["findings"]):
            raise RuntimeError("Doctor reports errors; inspect findings before acceptance")
        run("ripgrep-version", [bundle / "tools/rg.exe", "--version"])
        if args.capture_directory:
            source = args.capture_directory.resolve()
            capture = roots["root_ck3chronicle"] / "pending" / source.name
            shutil.copytree(source, capture)  # Refuses existing destination; original stays untouched.
            outcome = json.loads(run("genuine-ingest", [*cli, "ingest", "--capture-directory", capture, "--database", database]))
            if outcome["status"] != "COMPLETED":
                raise RuntimeError("Genuine capture did not complete; inspect stored outcome")
            summary.update(run_id=outcome["run_id"], log_sha256=outcome["log_sha256"])
            for fmt in ("text", "json", "html"):
                arguments = [*cli, "report", outcome["run_id"], "--preset", "frequent", "--limit", "5", "--format", fmt]
                if fmt == "html":
                    arguments += ["--output", evidence / "report.html"]
                run("report-" + fmt, arguments)
            summary["capture_and_reports"] = "genuine supplied capture, text/JSON/HTML exercised"
        run("runs", [*cli, "runs", "--package-id", document["model"]["package_id"], "--format", "json"])
        from ck3chronicle.pipeline.request_handler import HandlerClient
        summary["handler"] = HandlerClient(database).probe()
        if summary["handler"] is None:
            raise RuntimeError("Expected request handler identity is unavailable")
        identity = summary["handler"]["runtime_identity"]
        if not Path(identity["python"]).resolve().is_relative_to(bundle) or Path(identity["config"]).resolve() != config_path:
            raise RuntimeError("Handler identity differs from external install/config")
        run("stop", [*cli, "runtime-stop"])
        if HandlerClient(database).probe() is not None:
            raise RuntimeError("Handler still present after stop; inspect before repeating setup")
        summary["preserved_files"] = {str(p): sha(p) for p in roots["root_ck3chronicle"].rglob("*")
            if p.is_file() and (p == database or "pending" in p.parts or "review" in p.parts)}
        run("verify-after", [bundle / "Verify.cmd"])
        summary["journals"] = [str(p) for p in roots["root_ck3chronicle"].rglob("*")
                               if p.is_file() and p.suffix in (".log", ".jsonl") and "logging" in p.parts]
        summary["status"] = "bounded installed checks passed; repeat setup not performed"
    except Exception as exc:
        summary.update(status="failed", error=str(exc))
        # Isolated task only. Leave a clear recovery instruction, never kill processes.
        summary["recovery"] = f'Inspect effects; if its handler is running, use ck3chronicle.cmd --config "{config_path}" runtime-stop.'
        raise
    finally:
        result_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
