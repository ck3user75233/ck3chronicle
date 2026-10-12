"""Windows bundle presentation only; Pipeline owns configuration and operations."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

BUNDLE = Path(__file__).resolve().parent
PYTHON = BUNDLE / "runtime" / "python.exe"
FIELDS = {
    "root_game": "CK3 game content directory",
    "root_steam": "CK3 Steam workshop content directory",
    "root_local_mods": "Local CK3 mods directory",
    "root_logs": "Live CK3 logs directory",
    "root_crashes": "CK3 crashes directory",
}


def application(arguments, *, capture=False):
    return subprocess.run(
        [str(PYTHON), "-I", "-B", "-X", "utf8", "-m", "ck3chronicle.cli", *arguments],
        capture_output=capture, text=True, encoding="utf-8", errors="replace",
    )


def result(arguments):
    completed = application(arguments, capture=True)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="")
    try:
        value = json.loads(completed.stdout)
    except ValueError:
        raise RuntimeError(completed.stdout or "Application returned no structured result")
    if not isinstance(value, dict):
        raise RuntimeError("Application result must be an object")
    return value, completed.returncode


def findings(value, checks=None):
    for item in value.get("findings", []):
        if not isinstance(item, dict):
            print(item)
            continue
        if checks is not None and item["check"] not in checks:
            continue
        print(f"  [{item['severity']}] {item['check']}: {item['evidence']}")
        print(f"    {item['impact']} Action: {item['action']}")


def location_findings(value, field):
    """Explain producer findings without reimplementing filesystem validation."""
    checks = {field}
    if field == "root_game":
        checks.add("ck3_identity")
    if field == "root_logs":
        checks.update(("error_log", "logs_identity"))
    shown = False
    for item in value.get("findings", []):
        if not isinstance(item, dict) or item["check"] not in checks:
            continue
        shown = True
        if item["check"] == field and item["severity"] == "healthy":
            print("  Found: the folder exists and can be read.")
        elif item["check"] == "ck3_identity" and item["severity"] == "healthy":
            print("  Found: expected CK3 game folders and ck3.exe.")
        else:
            label = "Check" if item["severity"] == "healthy" else "Needs attention"
            print(f"  {label}: {item['impact']}")
            if item["severity"] != "healthy":
                print(f"  Details: {item['evidence']}")
                print(f"  What to do: {item['action']}")
    if not shown:
        print("  Not checked yet. Setup will check the selected location before Apply.")


def answer(prompt, default=None):
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"{prompt}{suffix}: ").strip()
    if value.casefold() in {"cancel", "quit"}:
        raise KeyboardInterrupt
    return value or default


def yes(prompt):
    while True:
        value = str(answer(prompt + " (Yes/No)") or "").casefold()
        if value in {"yes", "y", "accept"}:
            return True
        if value in {"no", "n"}:
            return False
        print("Type Yes to apply, No to leave without applying, or Cancel to exit.")


def use_location():
    while True:
        value = str(answer("Use this folder (Use / Change / Cancel)") or "").casefold()
        if value in {"use", "yes", "y", "accept"}:
            return True
        if value in {"change", "edit", "no", "n"}:
            return False
        print("Type Use to save this location, Change to enter another, or Cancel to exit.")


def full_path(prompt, default=None):
    while True:
        value = answer(prompt, default)
        if value:
            candidate = Path(value.strip('"'))
            if candidate.is_absolute():
                return str(candidate.resolve())
        print("Enter a full absolute path, or type cancel.")


def guided_setup(arguments):
    parser = argparse.ArgumentParser(description="Guided CK3Chronicle setup. Type cancel to leave without applying.")
    parser.add_argument("--config", help="Exact configuration file; otherwise application LocalAppData default")
    parser.add_argument("--database", help="Exact database returned by an earlier partially saved setup")
    parser.add_argument("--data-root", help="Editable initial suggestion for a separate writable data directory")
    options = parser.parse_args(arguments)
    from ck3chronicle import config
    config.configure(options.config)
    selected = config.default_config_path()
    print("CK3Chronicle setup")
    print(f"\nInstalled in: {BUNDLE}")
    print(f"Settings folder: {selected.parent}")
    print("Setup saves your settings automatically; there is no file to create or edit.")
    prefix = ["--config", str(selected)]
    saved = {}
    if selected.exists():
        # Central parser owns interpretation/errors. Never rebuild or write TOML here.
        saved, _ = result([*prefix, "doctor", "--format", "json"])
        try:
            config.load_config(selected)
        except (config.ConfigurationError, OSError) as exc:
            print(f"\nFound a settings path, but could not read usable settings: {selected}")
            print(str(exc))
            findings(saved)
            return 2
        print(f"\nFound and read saved settings: {selected}")
        findings(saved, {"paths", "database", "model", "controls"})
        print(f"\nExisting setup selected: {selected}")
        print(f"Its saved data: {saved.get('paths', {}).get('root_wip', 'see doctor findings below')}")
        print("If a watcher is using THESE settings, stop that watcher before applying changes.")
        print(f'Then stop its database handler: ck3chronicle.cmd --config "{selected}" runtime-stop')
        print("A watcher using a different setup does not need to be stopped.")
    else:
        print(f"\nNo saved settings found at: {selected}")
        print("That is expected for first setup. Apply will create the settings file.")
        print("\nLet's set up CK3Chronicle for your CK3 installation.")
    print("Press Enter to keep a suggested folder, or type a different full path.")
    print("You will review and accept each CK3 location before anything is saved.")
    suggested, code = result(["setup", "--suggest-paths", "--format", "json"])
    if code:
        findings(suggested)
        return code
    inventory, code = result(["setup", "--list-models", "--format", "json"])
    if code:
        return code
    choices = inventory["choices"]
    paths = saved.get("paths", {})
    values = {}
    for field, label in FIELDS.items():
        candidate = paths.get(field) or suggested.get("candidates", {}).get(field)
        print(f"\n{label}")
        if candidate:
            print(f"  Suggested location: {candidate}")
            location_findings(saved if paths.get(field) else suggested, field)
        else:
            print("  No location was found to suggest. Enter your actual folder below.")
        values[field] = full_path(label, candidate)
    # The application supplies the data-root default and model default in its preview.
    base = [*prefix, "setup", "--format", "json", "--ripgrep", str(BUNDLE / "tools" / "rg.exe")]
    if options.database:
        base += ["--database", options.database]

    def inputs():
        return [token for field, path in values.items() for token in ("--" + field.replace("_", "-"), path)]

    preview, _ = result([*base, *inputs()])
    default_data = options.data_root or paths.get("root_wip") or preview.get("paths", {}).get("root_wip")
    print("\nCK3Chronicle keeps saved run history and its own logs in a separate data folder.")
    data = full_path("Data folder", default_data)
    base += ["--data-root", data]
    current = (saved.get("model") or inventory["default"])["package_id"]
    print("\nAvailable authenticated models (production order is a catalog sequence):")
    available = [row for row in choices if row.get("authenticated")]
    for index, row in enumerate(available, 1):
        marker = " [current/default]" if row["package_id"] == current else ""
        print(f"  {index}. {row.get('publication_status', 'retained')} order {row.get('production_order', 'n/a')}{marker}")
        print(f"     package {row['package_id']}; manifest {row['manifest_sha256']}")
    while True:
        choice = answer("Model number (Enter keeps current/default)", "")
        if not choice:
            break
        if choice.isdigit() and 1 <= int(choice) <= len(available):
            current = available[int(choice) - 1]["package_id"]
            break
        print("Choose a displayed model number.")
    base += ["--package-id", current]
    accepted = []
    from ck3chronicle.setup import inspect_paths
    for field, label in FIELDS.items():
        while True:
            print(f"\n{label}: {values[field]}")
            checked = {"findings": inspect_paths({key: Path(path) for key, path in values.items()})}
            location_findings(checked, field)
            print("  CK3Chronicle will read this folder without changing its contents.")
            if use_location():
                accepted += ["--accept-path", field]
                break
            values[field] = full_path(label, values[field])
    arguments = [*base, *inputs(), *accepted]
    preview, code = result(arguments)
    print("\nSetup preview")
    print(f"Configuration: {selected}\nData: {data}\nModel: {current}")
    print(f"Database: {preview.get('database') or 'Created once by Apply; returned filename will be saved'}")
    findings(preview)
    if code:
        print("Setup has errors. Nothing applied; correct the reported inputs and run Setup again.")
        return code
    if not yes("Apply these settings"):
        print("Cancelled. No setup changes applied.")
        return 0
    applied, code = result([*arguments, "--apply"])
    findings(applied)
    print("Effects: " + json.dumps(applied.get("effects", []), ensure_ascii=False))
    print(f"Configuration: {selected}\nDatabase: {applied.get('database')}")
    if code or not applied.get("applied"):
        print("Setup did not finish. Preserve these effects and database path; see the recovery instructions.")
        return code or 1
    print("Setup saved. The watcher has not been started by setup.")
    print(f'Run: Start.cmd --config "{selected}"')
    print(f'Diagnose: ck3chronicle.cmd --config "{selected}" doctor')
    print("Doctor can return 2 for unverified write access; read each finding.")
    return 0


def verify():
    manifest = json.loads((BUNDLE / "release-manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["files"].items():
        path = (BUNDLE / name).resolve()
        if not path.is_relative_to(BUNDLE) or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"Bundle member does not match manifest: {name}")
    actual = {p.relative_to(BUNDLE).as_posix() for p in BUNDLE.rglob("*") if p.is_file()}
    if actual != set(manifest["files"]) | {"release-manifest.json"}:
        raise RuntimeError("Bundle has unlisted or missing files; compare a fresh extraction")
    print(f"Verified {len(manifest['files'])} files: {manifest['label']}")
    return 0


def main():
    mode, *arguments = sys.argv[1:]
    if mode == "setup":
        import os
        parser = argparse.ArgumentParser(description="CK3Chronicle Windows setup wizard")
        parser.add_argument("--config")
        parser.add_argument("--data-root")
        parser.add_argument("--database")
        options = parser.parse_args(arguments)
        shell = Path(os.environ["SystemRoot"]) / "System32/WindowsPowerShell/v1.0/powershell.exe"
        command = [str(shell), "-NoProfile", "-STA", "-ExecutionPolicy", "Bypass",
                   "-WindowStyle", "Hidden", "-File", str(BUNDLE / "Setup.ps1")]
        for name, value in (("ConfigPath", options.config), ("DataRoot", options.data_root), ("Database", options.database)):
            if value:
                command += ["-" + name, value]
        completed = subprocess.run(command, capture_output=True, text=True, errors="replace")
        if completed.returncode not in (0, 130):
            import ctypes
            detail = completed.stderr or completed.stdout or "The Windows setup window could not complete."
            ctypes.windll.user32.MessageBoxW(None, detail, "CK3Chronicle Setup", 0x10)
        return completed.returncode
    if mode == "setup-text":
        return guided_setup(arguments)
    if mode == "verify":
        return verify()
    if mode == "start":
        parser = argparse.ArgumentParser(description="Start the CK3 watcher in this terminal; Ctrl+C stops the watcher.")
        parser.add_argument("--config")
        options, rest = parser.parse_known_args(arguments)
        prefix = ["--config", options.config] if options.config else []
        # Do not catch Ctrl+C here: application Watcher owns graceful shutdown.
        sys.argv = ["ck3chronicle", *prefix, "watch", *rest]
        from ck3chronicle.cli import main as entry
    elif mode == "cli":
        sys.argv = ["ck3chronicle", *arguments]
        from ck3chronicle.cli import main as entry
    elif mode == "learner":
        sys.argv = ["ck3chronicle-learner-release", *arguments]
        from template_learning.learner_loader import main as entry
    elif mode == "model":
        sys.argv = ["ck3chronicle-model-release", *arguments]
        from ck3chronicle.pipeline.catalog import main as entry
    else:
        raise ValueError("Unknown bundle entry point")
    return entry()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled. If Apply had started, inspect its reported effects before retrying.")
        raise SystemExit(130)
    except Exception as exc:
        print(f"CK3Chronicle: {exc}", file=sys.stderr)
        raise SystemExit(1)
