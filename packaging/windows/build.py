"""Offline outer bundle builder. Consumes pinned inputs; never builds the wheel."""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import zipfile

HERE = Path(__file__).resolve().parent
ENTRY_POINTS = {
    "Setup.cmd": "setup", "Setup-Text.cmd": "setup-text", "Start.cmd": "start", "ck3chronicle.cmd": "cli",
    "ck3chronicle-learner-release.cmd": "learner",
    "ck3chronicle-model-release.cmd": "model", "Verify.cmd": "verify",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(value):
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or ":" in value or "\\" in value:
        raise ValueError(f"Unsafe archive path: {value}")
    return path


def authenticated(path, expected):
    if digest(path) != expected:
        raise ValueError(f"Input changed: {path}")
    return path


def install_wheel(wheel, runtime):
    """Install authenticated wheel payloads using wheel's purelib/data scheme."""
    installed = {}
    with zipfile.ZipFile(wheel) as archive:
        records = [n for n in archive.namelist() if n.endswith(".dist-info/RECORD")]
        if len(records) != 1:
            raise ValueError("Wheel must have exactly one RECORD")
        rows = {row[0]: row for row in csv.reader(io.StringIO(archive.read(records[0]).decode()))}
        for member in archive.infolist():
            if member.is_dir():
                continue
            name = relative(member.filename)
            payload = archive.read(member)
            row = rows.get(member.filename)
            if row is None:
                raise ValueError(f"Unrecorded wheel member: {name}")
            if row[1]:
                expected = "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(payload).digest()).rstrip(b"=").decode()
                if row[1] != expected or int(row[2]) != len(payload):
                    raise ValueError(f"Wheel RECORD mismatch: {name}")
            elif member.filename != records[0]:
                raise ValueError(f"Missing wheel member hash: {name}")
            if name.parts[0].endswith(".data"):
                scheme = name.parts[1]
                if scheme == "data":
                    target = runtime.joinpath(*name.parts[2:])
                elif scheme in ("purelib", "platlib"):
                    target = runtime.joinpath("Lib", "site-packages", *name.parts[2:])
                else:
                    raise ValueError(f"Unsupported wheel scheme {scheme}; request producer disposition")
            else:
                target = runtime.joinpath("Lib", "site-packages", *name.parts)
            if target.exists():
                raise ValueError(f"Wheel collision: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            installed[member.filename] = {"path": target.relative_to(runtime.parent).as_posix(), "sha256": digest(target)}
    return installed


def build(plan_path, destination):
    plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
    label = plan["label"]
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]+", label):
        raise ValueError("Release label must be a safe folder name")
    destination.mkdir(parents=True, exist_ok=True)
    bundle = destination / label
    bundle.mkdir()  # Never overwrite an earlier candidate or existing user data.
    runtime = bundle / "runtime"
    runtime.mkdir()
    runtime_input = plan["runtime"]
    root = Path(runtime_input["root"])
    for name, sha in runtime_input["files"].items():
        rel = relative(name)
        source = authenticated(root.joinpath(*rel.parts), sha)
        target = runtime.joinpath(*rel.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    # Applies to handler children too; no developer Python/PATH/site-packages fallback.
    (runtime / "python312._pth").write_text(".\nLib\nDLLs\nLib/site-packages\n", encoding="ascii")
    wheels = {}
    for component in ("application", "chardet"):
        value = plan[component]
        wheel = authenticated(Path(value["path"]), value["sha256"])
        wheels[component] = install_wheel(wheel, runtime)
    tool = plan["ripgrep"]
    (bundle / "tools").mkdir()
    shutil.copyfile(authenticated(Path(tool["path"]), tool["sha256"]), bundle / "tools" / "rg.exe")
    shutil.copyfile(authenticated(HERE / "launcher.py", plan["launcher_sha256"]), bundle / "launcher.py")
    for name, sha in plan["gui_files"].items():
        target = bundle.joinpath(*relative(name).parts)
        shutil.copyfile(authenticated(HERE / name, sha), target)
    for name, mode in ENTRY_POINTS.items():
        # %* is normal cmd argument forwarding, without CALL's second expansion.
        executable = "pythonw.exe" if mode == "setup" else "python.exe"
        script = (
            '@echo off\r\nsetlocal\r\n'
            f'"%~dp0runtime\\{executable}" -I -B -X utf8 "%~dp0launcher.py" {mode} %*\r\n'
            'exit /b %errorlevel%\r\n'
        )
        if mode == "setup":
            # Help remains visible in a terminal; normal setup uses the GUI host.
            script = script.replace('setlocal\r\n', 'setlocal\r\nif /I "%~1"=="--help" goto help\r\nif /I "%~1"=="-h" goto help\r\n', 1)
            script += (
                ':help\r\n'
                '"%~dp0runtime\\python.exe" -I -B -X utf8 "%~dp0launcher.py" setup %*\r\n'
                'exit /b %errorlevel%\r\n'
            )
        (bundle / name).write_bytes(script.encode("ascii"))
    for item in plan["documents"] + plan["notices"]:
        target = bundle.joinpath(*relative(item["destination"]).parts)
        if target.exists():
            raise ValueError(f"Document collision: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(authenticated(Path(item["path"]), item["sha256"]), target)
    inventory = {p.relative_to(bundle).as_posix(): digest(p) for p in sorted(bundle.rglob("*")) if p.is_file()}
    manifest = {
        "schema": "ck3chronicle.windows-bundle.v1", "label": label,
        "human_label": plan["human_label"], "status": plan["status"],
        "source_baseline": plan["source_baseline"],
        "application": {k: v for k, v in plan["application"].items() if k != "path"},
        "model": plan["model"], "learner": plan["learner"],
        "runtime": {k: v for k, v in runtime_input.items() if k not in ("root", "files")},
        "runtime_input_inventory_sha256": hashlib.sha256(json.dumps(runtime_input["files"], sort_keys=True).encode()).hexdigest(),
        "ripgrep": {k: v for k, v in tool.items() if k != "path"},
        "chardet": {k: v for k, v in plan["chardet"].items() if k != "path"},
        "manual_revision": plan["manual_revision"], "limits": plan["limits"],
        "build_recipe_sha256": digest(Path(__file__)), "input_plan_sha256": digest(plan_path),
        "installed_wheel_members": wheels, "files": inventory,
    }
    (bundle / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    archive_path = destination / (label + ".zip")
    with zipfile.ZipFile(archive_path, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(bundle.rglob("*")):
            if path.is_file():
                info = zipfile.ZipInfo(label + "/" + path.relative_to(bundle).as_posix(), date_time=(2026, 10, 8, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
    receipt = {"archive": str(archive_path.resolve()), "sha256": digest(archive_path),
               "bytes": archive_path.stat().st_size, "bundle": str(bundle.resolve()),
               "manifest_sha256": digest(bundle / "release-manifest.json"), "files": len(inventory)}
    (destination / (label + ".receipt.json")).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    build(args.plan.resolve(), args.output.resolve())
