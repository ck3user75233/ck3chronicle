"""Authority verification, canonical serialization, and result closure."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import shutil
import stat
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable


HARNESS_SCHEMA = "ck3chronicle.phase1-evaluator-harness"
CANDIDATE_COMMIT = "1f4d8c2f5a6e3ec1c5dc7a5324b0bbe4c4b233ac"
CANDIDATE_TREE = "23762ebaa55dba79b448052980c03c5a1c325f14"
CANDIDATE_MANIFEST_SHA256 = "b2f88bb40b9bd5dfba4ad09c080e736a55564212c81042bb177bed441b58805c"
CANDIDATE_SOURCE_SET_SHA256 = "7c9184c7916e379f1f26bcc5aebbf18a717d5be124ce647a156e3b2718f2ee27"
CORPUS_MANIFEST_SHA256 = "407e47d12bc17f30e2abd453dc69c4dda0b4e3fab705e2e361e6d26a8e6a6147"
CORPUS_SOURCE_SET_SHA256 = "f4b95276058f5b4f379de6e443e585b6fe8040ed3202b8f886e91c44a4f60c51"
SCORER_ONLY_RELATIVE_PATH = "units/DEV-SEMANTIC-252/SEMANTIC_LABELS_ADJUDICATED.json"
SCORER_ONLY_SHA256 = "db8a58a9a7f7f7fb0b84d1e39c1b2e724eae8058a00d07bb578367b795723e3d"
SCORER_ONLY_BYTES = 341708
MAX_RETAINED_FILE_BYTES = 64 * 1024 * 1024
MAX_RETAINED_CASE_BYTES = 128 * 1024 * 1024
CASE_COMPLETION_MARKER = "case-complete.json"
RESULT_COMPLETION_MARKER = "result-complete.json"
AGGREGATE_FINAL_FILES = (
    "result-set.json",
    "journal.ndjson",
    "runner-result.journal.json",
    "runner-result.manifest.json",
    RESULT_COMPLETION_MARKER,
)
AGGREGATE_TEMP_PATTERN = re.compile(
    r"^\.(?:" + "|".join(re.escape(name) for name in AGGREGATE_FINAL_FILES) + r")\.[0-9]+\.tmp$"
)
RESULT_BINDING_KEYS = (
    "candidate_commit",
    "candidate_tree",
    "candidate_manifest_sha256",
    "candidate_source_set_sha256",
    "corpus_manifest_sha256",
    "corpus_source_set_sha256",
    "plan_sha256",
    "harness_manifest_sha256",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def write_canonical_json(
    path: Path,
    value: Any,
    *,
    atomic_fault_hook: Callable[[str, Path, Path], None] | None = None,
    replace_operation: Callable[[Path, Path], None] | None = None,
) -> str:
    return write_atomic_bytes(
        path,
        canonical_json_bytes(value),
        atomic_fault_hook=atomic_fault_hook,
        replace_operation=replace_operation,
    )


def write_atomic_bytes(
    path: Path,
    payload: bytes,
    *,
    atomic_fault_hook: Callable[[str, Path, Path], None] | None = None,
    replace_operation: Callable[[Path, Path], None] | None = None,
) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    if atomic_fault_hook is not None:
        atomic_fault_hook("after_fsync", path, temporary)
    (replace_operation or os.replace)(temporary, path)
    return hashlib.sha256(payload).hexdigest()


def write_atomic_readonly_bytes(
    path: Path,
    payload: bytes,
    *,
    atomic_fault_hook: Callable[[str, Path, Path], None] | None = None,
    replace_operation: Callable[[Path, Path], None] | None = None,
) -> str:
    """Publish one immutable file with no visible writable-final interval."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    if atomic_fault_hook is not None:
        atomic_fault_hook("after_fsync", path, temporary)
    temporary.chmod(stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
    (replace_operation or os.replace)(temporary, path)
    return hashlib.sha256(payload).hexdigest()


def path_is_linklike(path: Path) -> bool:
    """Recognize symlinks and Windows junction/reparse links without following."""
    is_junction = getattr(os.path, "isjunction", None)
    return path.is_symlink() or bool(is_junction is not None and is_junction(path))


def nofollow_tree_entries(root: Path) -> list[tuple[Path, str]]:
    """Inventory a regular directory tree without traversing any reparse link."""
    if path_is_linklike(root) or not root.is_dir():
        raise ValueError(f"tree root is linklike or non-directory: {root}")
    discovered: list[tuple[Path, str]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as iterator:
            entries = sorted(iterator, key=lambda entry: entry.name)
        child_directories: list[Path] = []
        for entry in entries:
            path = Path(entry.path)
            if entry.is_symlink() or path_is_linklike(path):
                discovered.append((path, "special"))
            elif entry.is_file(follow_symlinks=False):
                discovered.append((path, "file"))
            elif entry.is_dir(follow_symlinks=False):
                discovered.append((path, "directory"))
                child_directories.append(path)
            else:
                discovered.append((path, "special"))
        pending.extend(reversed(child_directories))
    return discovered


def remove_incomplete_aggregate_temps(results_root: Path) -> list[str]:
    """Remove only exact harness-owned atomic temps before markerless recovery."""
    if path_is_linklike(results_root) or not results_root.is_dir():
        raise RuntimeError("aggregate temp recovery root is linklike or non-directory")
    completion_path = results_root / RESULT_COMPLETION_MARKER
    if os.path.lexists(completion_path):
        raise RuntimeError("aggregate temp recovery is forbidden after final marker publication")
    removed: list[str] = []
    for path in sorted(results_root.iterdir()):
        if not AGGREGATE_TEMP_PATTERN.fullmatch(path.name):
            continue
        if path_is_linklike(path) or not path.is_file():
            raise RuntimeError(f"unsafe aggregate temp entry: {path.name}")
        path.chmod(stat.S_IREAD | stat.S_IWRITE)
        path.unlink()
        removed.append(path.name)
    return removed


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_child(root: Path, relative: str) -> Path:
    # pathlib.resolve() requires directory-handle permissions that a read-only
    # frozen corpus ACL need not grant on Windows.  abspath/commonpath provides
    # the lexical containment check; each manifest path is then separately
    # rejected if any existing component is a symlink.
    root = Path(os.path.abspath(root))
    candidate = Path(os.path.abspath(root / Path(relative.replace("/", os.sep))))
    if candidate == root or os.path.commonpath((str(root), str(candidate))) != str(root):
        raise ValueError(f"path escapes authority root: {relative!r}")
    current = root
    if path_is_linklike(current):
        raise ValueError(f"authority/result root is linklike: {root}")
    for part in candidate.relative_to(root).parts:
        current = current / part
        if os.path.lexists(current) and path_is_linklike(current):
            raise ValueError(f"linklike component is forbidden in authority/result path: {relative!r}")
    return candidate


def paths_overlap(left: Path, right: Path) -> bool:
    left = Path(os.path.abspath(left))
    right = Path(os.path.abspath(right))
    return left == right or left in right.parents or right in left.parents


def assert_isolated_paths(
    *,
    results_root: Path,
    scratch_root: Path,
    candidate_root: Path,
    corpus_root: Path,
    harness_root: Path,
) -> None:
    protected = (candidate_root, corpus_root, harness_root)
    if paths_overlap(results_root, scratch_root):
        raise ValueError("results and scratch roots overlap")
    for writable in (results_root, scratch_root):
        for authority in protected:
            if paths_overlap(writable, authority):
                raise ValueError(f"writable root overlaps protected authority: {writable} / {authority}")


def _git(candidate_root: Path, *args: str) -> str:
    command = [
        "git",
        "-c",
        f"safe.directory={candidate_root.as_posix()}",
        "-C",
        str(candidate_root),
        *args,
    ]
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=60)
    if completed.returncode:
        raise RuntimeError(
            f"git authority query failed ({completed.returncode}): "
            + completed.stderr.decode("utf-8", "replace")
        )
    return completed.stdout.decode("utf-8", "strict")


def verify_authorities(
    candidate_root: Path,
    candidate_manifest_path: Path,
    corpus_root: Path,
    *,
    opaque_hash_scorer_only: bool = False,
) -> dict[str, Any]:
    """Verify authorities while never opening scorer-only answer content."""
    candidate_root = Path(os.path.abspath(candidate_root))
    candidate_manifest_path = Path(os.path.abspath(candidate_manifest_path))
    corpus_root = Path(os.path.abspath(corpus_root))
    corpus_manifest_path = corpus_root / "corpus.manifest.json"
    if not candidate_root.is_dir() or not candidate_manifest_path.is_file() or not corpus_root.is_dir() or not corpus_manifest_path.is_file():
        raise FileNotFoundError("one or more authority roots/manifests are absent")
    problems: list[str] = []

    candidate_manifest_hash = sha256_file(candidate_manifest_path)
    corpus_manifest_hash = sha256_file(corpus_manifest_path)
    if candidate_manifest_hash != CANDIDATE_MANIFEST_SHA256:
        problems.append("candidate_manifest_sha256")
    if corpus_manifest_hash != CORPUS_MANIFEST_SHA256:
        problems.append("corpus_manifest_sha256")

    candidate = read_json(candidate_manifest_path)
    corpus = read_json(corpus_manifest_path)
    if candidate.get("source_set_sha256") != CANDIDATE_SOURCE_SET_SHA256:
        problems.append("candidate_source_set_binding")
    if corpus.get("source_set_sha256") != CORPUS_SOURCE_SET_SHA256:
        problems.append("corpus_source_set_binding")

    status = _git(candidate_root, "status", "--porcelain=v1", "--untracked-files=all")
    head = _git(candidate_root, "rev-parse", "HEAD").strip()
    tree = _git(candidate_root, "rev-parse", "HEAD^{tree}").strip()
    if status:
        problems.append("candidate_worktree_dirty")
    if head != CANDIDATE_COMMIT or candidate.get("candidate_commit") != head:
        problems.append("candidate_commit")
    if tree != CANDIDATE_TREE or candidate.get("candidate_tree") != tree:
        problems.append("candidate_tree")

    tree_rows: dict[str, tuple[str, str]] = {}
    for row in _git(candidate_root, "ls-tree", "-r", "--full-tree", "HEAD").splitlines():
        metadata, path = row.split("\t", 1)
        mode, kind, blob = metadata.split(" ")
        if kind != "blob":
            problems.append(f"candidate_nonblob:{path}")
        tree_rows[path] = (mode, blob)

    candidate_bytes = 0
    candidate_paths: set[str] = set()
    for entry in candidate.get("files", []):
        relative = str(entry["path"])
        candidate_paths.add(relative)
        path = safe_child(candidate_root, relative)
        if not path.is_file():
            problems.append(f"candidate_missing:{relative}")
            continue
        size = path.stat().st_size
        candidate_bytes += size
        if size != int(entry["bytes"]):
            problems.append(f"candidate_size:{relative}")
        if sha256_file(path) != entry["sha256"]:
            problems.append(f"candidate_sha256:{relative}")
        if tree_rows.get(relative) != (entry["mode"], entry["git_blob"]):
            problems.append(f"candidate_git_object:{relative}")
    if candidate_paths != set(tree_rows):
        problems.append("candidate_exact_tracked_set")

    corpus_paths: set[str] = set()
    corpus_bytes = 0
    corpus_files = 0
    scorer_identity: dict[str, Any] | None = None
    for unit in corpus.get("units", []):
        for entry in unit.get("files", []):
            relative = f"{unit['frozen_path'].rstrip('/')}/{entry['relative_path']}"
            corpus_paths.add(relative)
            path = safe_child(corpus_root, relative)
            if not path.is_file():
                problems.append(f"corpus_missing:{relative}")
                continue
            size = path.stat().st_size
            corpus_bytes += size
            corpus_files += 1
            if size != int(entry["bytes"]):
                problems.append(f"corpus_size:{relative}")
            if relative == SCORER_ONLY_RELATIVE_PATH:
                if size != SCORER_ONLY_BYTES or entry["sha256"] != SCORER_ONLY_SHA256:
                    problems.append("scorer_only_manifest_identity")
                actual_hash = sha256_file(path) if opaque_hash_scorer_only else None
                if actual_hash is not None and actual_hash != SCORER_ONLY_SHA256:
                    problems.append("scorer_only_opaque_sha256")
                scorer_identity = {
                    "relative_path": relative,
                    "bytes": size,
                    "sha256": actual_hash or entry["sha256"],
                    "handling": "manifest-bound identity plus physical size only; content never opened, parsed, hashed, or staged",
                }
            elif sha256_file(path) != entry["sha256"]:
                problems.append(f"corpus_sha256:{relative}")

    corpus_disk_entries = nofollow_tree_entries(corpus_root / "units")
    if any(kind == "special" for _path, kind in corpus_disk_entries):
        problems.append("corpus_special_file_entry")
    disk_paths = {path.relative_to(corpus_root).as_posix() for path, kind in corpus_disk_entries if kind == "file"}
    if disk_paths != corpus_paths:
        problems.append("corpus_exact_file_set")
    sidecar = (corpus_root / "corpus.manifest.sha256").read_text(encoding="ascii").strip()
    if not sidecar.startswith(CORPUS_MANIFEST_SHA256):
        problems.append("corpus_manifest_sidecar")

    report = {
        "schema": "ck3chronicle.phase1-authority-verification",
        "schema_version": 1,
        "verified": not problems,
        "problems": problems,
        "candidate": {
            "root": str(candidate_root),
            "worktree_clean": not bool(status),
            "commit": head,
            "tree": tree,
            "manifest_path": str(candidate_manifest_path),
            "manifest_sha256": candidate_manifest_hash,
            "source_set_sha256": candidate.get("source_set_sha256"),
            "file_count": len(candidate_paths),
            "bytes": candidate_bytes,
        },
        "corpus": {
            "root": str(corpus_root),
            "manifest_path": str(corpus_manifest_path),
            "manifest_sha256": corpus_manifest_hash,
            "source_set_sha256": corpus.get("source_set_sha256"),
            "unit_count": len(corpus.get("units", [])),
            "file_count": corpus_files,
            "bytes": corpus_bytes,
            "scorer_only_identity": scorer_identity,
        },
    }
    if problems:
        raise RuntimeError("authority verification failed: " + ", ".join(problems))
    return report


def corpus_unit_map(corpus_root: Path) -> dict[str, dict[str, Any]]:
    manifest = read_json(corpus_root / "corpus.manifest.json")
    return {str(unit["corpus_id"]): unit for unit in manifest["units"]}


def stage_unit(
    corpus_root: Path,
    unit_id: str,
    destination: Path,
    *,
    include_all: bool = False,
) -> dict[str, Any]:
    """Copy one verified unit, refusing to stage the scorer-only answer file."""
    units = corpus_unit_map(corpus_root)
    unit = units[unit_id]
    source_root = safe_child(corpus_root, unit["frozen_path"])
    source_subpath = unit.get("product_logs_subpath")
    if source_subpath is None and not include_all:
        raise ValueError(f"unit {unit_id} is not a product-log unit")
    destination.mkdir(parents=True, exist_ok=False)
    copied: list[dict[str, Any]] = []
    for entry in unit["files"]:
        relative = str(entry["relative_path"])
        if unit_id == "DEV-SEMANTIC-252" and relative == "SEMANTIC_LABELS_ADJUDICATED.json":
            continue
        if include_all:
            unit_relative = relative
        else:
            prefix = "" if source_subpath in (None, ".") else str(source_subpath).rstrip("/") + "/"
            if not relative.startswith(prefix):
                continue
            unit_relative = relative[len(prefix) :]
        source_file = safe_child(source_root, relative)
        target = destination / Path(unit_relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target)
        actual_hash = sha256_file(target)
        if target.stat().st_size != int(entry["bytes"]) or actual_hash != entry["sha256"]:
            raise RuntimeError(f"staged unit verification failed: {unit_id}/{relative}")
        # Locked authority files are read-only.  The exact verified scratch
        # copy is made writable only after its byte identity has been proven.
        target.chmod(stat.S_IREAD | stat.S_IWRITE)
        copied.append({"relative_path": unit_relative.replace("\\", "/"), "bytes": target.stat().st_size, "sha256": actual_hash})
    return {
        "corpus_id": unit_id,
        "tree_sha256": unit["tree_sha256"],
        "files": copied,
        "scorer_only_staged": False,
    }


def file_identity(path: Path, root: Path | None = None) -> dict[str, Any]:
    return {
        "path": path.relative_to(root).as_posix() if root is not None else str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def tree_identities(root: Path) -> list[dict[str, Any]]:
    entries = nofollow_tree_entries(root)
    special = [path.relative_to(root).as_posix() for path, kind in entries if kind == "special"]
    if special:
        raise ValueError("linklike/special tree entries are forbidden: " + ",".join(special))
    return [file_identity(path, root) for path, kind in entries if kind == "file"]


def source_set_hash(entries: Iterable[dict[str, Any]]) -> str:
    reduced = [
        {"path": str(entry["path"]), "bytes": int(entry["bytes"]), "sha256": str(entry["sha256"])}
        for entry in entries
    ]
    return hashlib.sha256(canonical_json_bytes(sorted(reduced, key=lambda item: item["path"]))).hexdigest()


def host_identity() -> dict[str, Any]:
    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "processor": platform.processor(),
        "logical_cpu_count": os.cpu_count(),
    }


def initialize_results(
    results_root: Path,
    scratch_root: Path,
    *,
    plan_sha256: str,
    harness_manifest_sha256: str,
) -> dict[str, Any]:
    if results_root.exists() and any(results_root.iterdir()):
        raise FileExistsError(f"results root is not empty: {results_root}")
    results_root.mkdir(parents=True, exist_ok=True)
    scratch_root.mkdir(parents=True, exist_ok=True)
    (results_root / "cases").mkdir()
    (results_root / ".open").mkdir()
    journal = results_root / "journal.ndjson"
    journal.touch(exist_ok=False)
    payload = {
        "schema": "ck3chronicle.phase1-runner-result-set",
        "schema_version": 1,
        "created_at_utc": utc_now(),
        "status": "open",
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_tree": CANDIDATE_TREE,
        "candidate_manifest_sha256": CANDIDATE_MANIFEST_SHA256,
        "candidate_source_set_sha256": CANDIDATE_SOURCE_SET_SHA256,
        "corpus_manifest_sha256": CORPUS_MANIFEST_SHA256,
        "corpus_source_set_sha256": CORPUS_SOURCE_SET_SHA256,
        "plan_sha256": plan_sha256,
        "harness_manifest_sha256": harness_manifest_sha256,
        "scratch_root": str(scratch_root.resolve()),
    }
    write_canonical_json(results_root / "result-set.json", payload)
    return payload


def append_journal(path: Path, entry: dict[str, Any]) -> None:
    payload = canonical_json_bytes(entry)
    with path.open("ab", buffering=0) as stream:
        stream.write(payload)
        os.fsync(stream.fileno())


def close_case(
    *,
    results_root: Path,
    scratch_case: Path,
    case: dict[str, Any],
    execution: dict[str, Any],
    before_completion_hook: Callable[[Path], None] | None = None,
) -> dict[str, Any]:
    case_id = str(case["case_id"])
    final_dir = results_root / "cases" / case_id
    if final_dir.exists():
        raise FileExistsError(f"case already closed; retries are forbidden: {case_id}")
    legacy_open_dir = results_root / ".open" / case_id
    if legacy_open_dir.exists():
        raise FileExistsError(f"case already has an open envelope: {case_id}")
    result_set = read_json(results_root / "result-set.json")
    if result_set.get("status") != "open":
        raise RuntimeError("cannot close a case into a non-open result set")
    result_bindings = {key: result_set.get(key) for key in RESULT_BINDING_KEYS}
    # Publish directly into the final namespace.  The directory is partial and
    # non-counting until CASE_COMPLETION_MARKER is atomically published last.
    final_dir.mkdir(parents=True)
    artifacts_dir = final_dir / "artifacts"
    artifacts_dir.mkdir()
    retained: list[dict[str, Any]] = []
    total = 0
    declared = scratch_case / "declared"
    if declared.exists():
        for source, kind in nofollow_tree_entries(declared):
            if kind == "special":
                raise RuntimeError(f"declared artifact is linklike or special: {source.relative_to(declared)}")
            if kind != "file":
                continue
            relative = source.relative_to(declared)
            size = source.stat().st_size
            if size > MAX_RETAINED_FILE_BYTES:
                raise RuntimeError(f"declared artifact exceeds per-file bound: {relative}")
            total += size
            if total > MAX_RETAINED_CASE_BYTES:
                raise RuntimeError(f"declared artifacts exceed per-case bound: {case_id}")
            target = artifacts_dir / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            retained.append(file_identity(target, final_dir))
    closed_at = utc_now()
    envelope = {
        "schema": "ck3chronicle.phase1-case-result-envelope",
        "schema_version": 2,
        "case_id": case_id,
        "gate": case["gate"],
        "recipe": case["recipe"],
        "assigned_inputs": case["inputs"],
        "corpus_source_set_sha256": CORPUS_SOURCE_SET_SHA256,
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_tree": CANDIDATE_TREE,
        "result_set_bindings": result_bindings,
        "execution": execution,
        "retained_artifacts": retained,
        "retained_bytes": total,
        "scratch_deletion_policy": "only_after_atomic_completion_marker",
        "completion_marker": CASE_COMPLETION_MARKER,
        "closed_at_utc": closed_at,
    }
    envelope_sha = write_canonical_json(final_dir / "case-result.json", envelope)
    for retained_file, kind in nofollow_tree_entries(final_dir):
        if kind == "file":
            retained_file.chmod(stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
    if before_completion_hook is not None:
        before_completion_hook(final_dir)
    completion = {
        "schema": "ck3chronicle.phase1-case-completion-marker",
        "schema_version": 1,
        "case_id": case_id,
        "case_result_sha256": envelope_sha,
        "artifact_inventory_sha256": hashlib.sha256(canonical_json_bytes(retained)).hexdigest(),
        "retained_bytes": total,
        "closed_at_utc": closed_at,
    }
    completion_path = final_dir / CASE_COMPLETION_MARKER
    completion_sha = write_atomic_readonly_bytes(completion_path, canonical_json_bytes(completion))
    if sha256_file(final_dir / "case-result.json") != envelope_sha or sha256_file(completion_path) != completion_sha:
        raise RuntimeError(f"case completion readback failed: {case_id}")
    # The case is closed before any scratch removal begins.
    shutil.rmtree(scratch_case)
    journal_entry = {
        "case_id": case_id,
        "gate": case["gate"],
        "case_result_sha256": envelope_sha,
        "completion_marker_sha256": completion_sha,
        "retained_bytes": total,
        "scratch_deleted": not scratch_case.exists(),
        "closed_at_utc": closed_at,
    }
    return journal_entry


def _verify_case_directory(
    directory: Path,
    result_set: dict[str, Any],
    expected_cases: dict[str, dict[str, Any]] | None,
) -> tuple[dict[str, Any] | None, list[str], str]:
    """Return a valid closed case or a structured partial/invalid rejection."""
    name = directory.name
    problems: list[str] = []
    if path_is_linklike(directory) or not directory.is_dir():
        return None, [f"unexpected_case_root_file:{name}"], "invalid"
    completion_path = directory / CASE_COMPLETION_MARKER
    if not os.path.lexists(completion_path):
        return None, [f"partial_case_directory:{name}"], "partial"
    if path_is_linklike(completion_path):
        return None, [f"case_completion_marker_special_entry:{name}"], "invalid"
    if not completion_path.is_file():
        return None, [f"partial_case_completion_nonfile:{name}"], "partial"
    try:
        completion = read_json(completion_path)
    except (OSError, json.JSONDecodeError):
        return None, [f"invalid_case_completion_marker:{name}"], "invalid"
    if not isinstance(completion, dict):
        return None, [f"case_completion_object_schema:{name}"], "invalid"
    envelope_path = directory / "case-result.json"
    if not os.path.lexists(envelope_path):
        return None, [f"missing_case_envelope:{name}"], "invalid"
    if path_is_linklike(envelope_path) or not envelope_path.is_file():
        return None, [f"case_envelope_special_entry:{name}"], "invalid"
    try:
        envelope = read_json(envelope_path)
    except (OSError, json.JSONDecodeError):
        return None, [f"invalid_case_envelope:{name}"], "invalid"
    if not isinstance(envelope, dict):
        return None, [f"case_envelope_object_schema:{name}"], "invalid"

    envelope_sha = sha256_file(envelope_path)
    completion_sha = sha256_file(completion_path)
    if completion.get("schema") != "ck3chronicle.phase1-case-completion-marker" or completion.get("schema_version") != 1:
        problems.append(f"case_completion_schema:{name}")
    if completion.get("case_id") != name or completion.get("case_result_sha256") != envelope_sha:
        problems.append(f"case_completion_binding:{name}")
    if envelope.get("schema") != "ck3chronicle.phase1-case-result-envelope" or envelope.get("schema_version") != 2:
        problems.append(f"case_envelope_schema:{name}")
    if envelope.get("completion_marker") != CASE_COMPLETION_MARKER or envelope.get("scratch_deletion_policy") != "only_after_atomic_completion_marker":
        problems.append(f"case_completion_policy:{name}")
    if envelope.get("case_id") != name:
        problems.append(f"case_id_directory_mismatch:{name}")
    if envelope.get("candidate_commit") != CANDIDATE_COMMIT or envelope.get("candidate_tree") != CANDIDATE_TREE:
        problems.append(f"case_candidate_binding:{name}")
    if envelope.get("corpus_source_set_sha256") != CORPUS_SOURCE_SET_SHA256:
        problems.append(f"case_corpus_binding:{name}")
    result_bindings = {key: result_set.get(key) for key in RESULT_BINDING_KEYS}
    if envelope.get("result_set_bindings") != result_bindings:
        problems.append(f"case_result_set_binding:{name}")
    expected_case = expected_cases.get(name) if expected_cases is not None else None
    if expected_cases is not None and expected_case is None:
        problems.append(f"unexpected_case_id:{name}")
    elif expected_case is not None:
        if envelope.get("gate") != expected_case.get("gate"):
            problems.append(f"case_gate_binding:{name}")
        if envelope.get("recipe") != expected_case.get("recipe"):
            problems.append(f"case_recipe_binding:{name}")
        if envelope.get("assigned_inputs") != expected_case.get("inputs"):
            problems.append(f"case_input_binding:{name}")

    retained_entries = envelope.get("retained_artifacts", [])
    if not isinstance(retained_entries, list):
        problems.append(f"retained_artifact_schema:{name}")
        retained_entries = []
    retained_paths: list[str] = []
    retained_total = 0
    for index, entry in enumerate(retained_entries):
        if not isinstance(entry, dict):
            problems.append(f"retained_artifact_entry_schema:{name}/{index}")
            continue
        relative = entry.get("path")
        size = entry.get("bytes")
        digest = entry.get("sha256")
        if not isinstance(relative, str) or not relative.startswith("artifacts/"):
            problems.append(f"retained_artifact_boundary:{name}/{index}")
            continue
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            problems.append(f"retained_artifact_bytes_schema:{name}/{relative}")
            continue
        if not isinstance(digest, str) or len(digest) != 64:
            problems.append(f"retained_artifact_hash_schema:{name}/{relative}")
            continue
        retained_paths.append(relative)
        retained_total += size
        if size > MAX_RETAINED_FILE_BYTES:
            problems.append(f"retained_file_bound:{name}/{relative}")
        try:
            artifact = safe_child(directory, relative)
        except (OSError, ValueError):
            problems.append(f"retained_artifact_escape:{name}/{index}")
            continue
        try:
            identity_matches = not path_is_linklike(artifact) and artifact.is_file() and artifact.stat().st_size == size and sha256_file(artifact) == digest
        except OSError:
            identity_matches = False
        if not identity_matches:
            problems.append(f"artifact_identity:{name}/{relative}")
        elif artifact.stat().st_mode & stat.S_IWUSR:
            problems.append(f"artifact_writable:{name}/{relative}")
    if len(retained_paths) != len(set(retained_paths)):
        problems.append(f"duplicate_retained_artifact:{name}")
    if envelope.get("retained_bytes") != retained_total or retained_total > MAX_RETAINED_CASE_BYTES:
        problems.append(f"retained_case_bound_or_total:{name}")
    if completion.get("retained_bytes") != retained_total or completion.get("closed_at_utc") != envelope.get("closed_at_utc"):
        problems.append(f"case_completion_totals:{name}")
    try:
        inventory_sha = hashlib.sha256(canonical_json_bytes(retained_entries)).hexdigest()
    except (TypeError, ValueError):
        inventory_sha = None
    if completion.get("artifact_inventory_sha256") != inventory_sha:
        problems.append(f"case_completion_artifact_inventory:{name}")
    expected_files = {"case-result.json", CASE_COMPLETION_MARKER, *retained_paths}
    walked_entries = nofollow_tree_entries(directory)
    special_entries = [path.relative_to(directory).as_posix() for path, kind in walked_entries if kind == "special"]
    if special_entries:
        problems.append(f"case_special_entries:{name}:" + ",".join(sorted(special_entries)))
    actual_files = {path.relative_to(directory).as_posix() for path, kind in walked_entries if kind == "file"}
    if actual_files != expected_files:
        problems.append(f"case_exact_file_set:{name}")
    if envelope_path.stat().st_mode & stat.S_IWUSR:
        problems.append(f"case_envelope_writable:{name}")
    if completion_path.stat().st_mode & stat.S_IWUSR:
        problems.append(f"case_completion_marker_writable:{name}")
    if problems:
        return None, problems, "invalid"
    return {
        "case_id": name,
        "gate": envelope.get("gate"),
        "case_result_sha256": envelope_sha,
        "completion_marker_sha256": completion_sha,
        "retained_bytes": envelope.get("retained_bytes"),
        "closed_at_utc": envelope.get("closed_at_utc"),
    }, [], "valid"


def verify_result_set(
    results_root: Path,
    *,
    require_closed: bool = False,
    expected_cases: dict[str, dict[str, Any]] | None = None,
    expected_bindings: dict[str, str] | None = None,
    aggregate_recovery: bool = False,
) -> dict[str, Any]:
    if path_is_linklike(results_root) or not results_root.is_dir():
        return {
            "schema": "ck3chronicle.phase1-result-set-verification",
            "schema_version": 1,
            "verified": False,
            "problems": ["results_root_linklike_or_non_directory"],
            "case_count": 0,
            "cases": [],
            "open_envelope_count": 0,
            "partial_case_count": 0,
            "partial_cases": [],
            "invalid_completed_case_count": 0,
            "invalid_completed_cases": [],
            "aggregate_completed": False,
            "derived_journal_entries": [],
        }
    result_set_path = results_root / "result-set.json"
    result_set_path_problem: str | None = None
    if os.path.lexists(result_set_path) and (path_is_linklike(result_set_path) or not result_set_path.is_file()):
        result_set = None
        result_set_path_problem = "result_set_special_entry"
    else:
        try:
            result_set = read_json(result_set_path)
        except (OSError, json.JSONDecodeError):
            result_set = None
    problems: list[str] = []
    cases: list[dict[str, Any]] = []
    partial_cases: list[str] = []
    invalid_completed_cases: list[str] = []
    if not isinstance(result_set, dict):
        return {
            "schema": "ck3chronicle.phase1-result-set-verification",
            "schema_version": 1,
            "verified": False,
            "problems": [problem for problem in (result_set_path_problem, "result_set_object_schema") if problem is not None],
            "case_count": 0,
            "cases": [],
            "open_envelope_count": 0,
            "partial_case_count": 0,
            "partial_cases": [],
            "invalid_completed_case_count": 0,
            "invalid_completed_cases": [],
            "aggregate_completed": False,
            "derived_journal_entries": [],
        }
    if result_set.get("schema") != "ck3chronicle.phase1-runner-result-set" or result_set.get("schema_version") != 1:
        problems.append("result_set_schema")
    if result_set.get("status") not in {"open", "closed"}:
        problems.append("result_set_status")
    if expected_bindings is not None:
        for key, value in expected_bindings.items():
            if result_set.get(key) != value:
                problems.append(f"result_set_binding:{key}")
    case_root = results_root / "cases"
    case_directories: list[Path] = []
    if not os.path.lexists(case_root):
        problems.append("case_root_missing")
    elif path_is_linklike(case_root) or not case_root.is_dir():
        problems.append("case_root_special_entry")
    else:
        case_directories = sorted(case_root.iterdir())
    for directory in case_directories:
        try:
            case, case_problems, status = _verify_case_directory(directory, result_set, expected_cases)
        except Exception as error:
            case=None; case_problems=[f"case_verification_exception:{directory.name}:{type(error).__name__}"]; status="invalid"
        problems.extend(case_problems)
        if status == "partial":
            partial_cases.append(directory.name)
        elif status == "invalid":
            invalid_completed_cases.append(directory.name)
        elif case is not None:
            cases.append(case)
    actual_case_ids = {entry["case_id"] for entry in cases}
    if require_closed and expected_cases is not None:
        missing = sorted(set(expected_cases) - actual_case_ids)
        extra = sorted(actual_case_ids - set(expected_cases))
        if missing:
            problems.append("closed_case_inventory_missing:" + ",".join(missing))
        if extra:
            problems.append("closed_case_inventory_extra:" + ",".join(extra))
    open_root = results_root / ".open"
    open_entries: list[Path] = []
    if not os.path.lexists(open_root):
        problems.append("open_root_missing")
    elif path_is_linklike(open_root) or not open_root.is_dir():
        problems.append("open_root_special_entry")
    else:
        open_entries = list(open_root.iterdir())
    if open_entries:
        problems.append("open_case_envelopes")
    if require_closed and result_set.get("status") != "closed":
        problems.append("result_set_not_closed")
    raw_journal_entries: list[dict[str, Any]] = []
    journal_path = results_root / "journal.ndjson"
    if not os.path.lexists(journal_path):
        problems.append("raw_journal_missing")
    elif path_is_linklike(journal_path) or not journal_path.is_file():
        problems.append("raw_journal_special_entry")
    elif not aggregate_recovery:
        try:
            decoded = [json.loads(line) for line in journal_path.read_text(encoding="utf-8").splitlines() if line]
            if not all(isinstance(entry, dict) for entry in decoded):
                raise ValueError("journal entries must be objects")
            raw_journal_entries = decoded
        except (UnicodeDecodeError, json.JSONDecodeError):
            problems.append("raw_journal_invalid")
            raw_journal_entries = []
        except ValueError:
            problems.append("raw_journal_entry_schema")
            raw_journal_entries = []
    derived_journal_entries = [
        {
            "case_id": case["case_id"],
            "gate": case["gate"],
            "case_result_sha256": case["case_result_sha256"],
            "completion_marker_sha256": case["completion_marker_sha256"],
            "retained_bytes": case["retained_bytes"],
            "closed_at_utc": case["closed_at_utc"],
        }
        for case in sorted(cases, key=lambda item: item["case_id"])
    ]
    completion_path = results_root / RESULT_COMPLETION_MARKER
    completion_path_present = os.path.lexists(completion_path)
    completion_path_special = completion_path_present and (path_is_linklike(completion_path) or not completion_path.is_file())
    aggregate_completed = completion_path_present and not completion_path_special
    if completion_path_special:
        problems.append("aggregate_completion_marker_special_entry")
    known_aggregate_files = set(AGGREGATE_FINAL_FILES)
    expected_top_files = {"result-set.json", "journal.ndjson"}
    if aggregate_recovery:
        # Aggregate intermediates are disposable until the final marker exists.
        # Case markers, authority bindings, and directory inventory remain strict.
        if aggregate_completed:
            problems.append("aggregate_recovery_refuses_existing_completion_marker")
    elif aggregate_completed:
        expected_top_files = known_aggregate_files
        if result_set.get("status") != "closed":
            problems.append("aggregate_marker_on_nonclosed_result")
        journal_by_case: dict[str, dict[str, Any]] = {}
        for entry in raw_journal_entries:
            case_id = str(entry.get("case_id"))
            if case_id in journal_by_case:
                problems.append(f"raw_journal_duplicate:{case_id}")
            journal_by_case[case_id] = entry
        if len(raw_journal_entries) != len(cases):
            problems.append("raw_journal_cardinality")
        for expected_entry in derived_journal_entries:
            if journal_by_case.get(expected_entry["case_id"]) != expected_entry:
                problems.append(f"raw_journal_case_reconciliation:{expected_entry['case_id']}")
        if set(journal_by_case) != actual_case_ids:
            problems.append("raw_journal_case_inventory")

        manifest_path = results_root / "runner-result.manifest.json"
        canonical_journal_path = results_root / "runner-result.journal.json"
        aggregate_hashes = {
            "result_set": sha256_file(results_root / "result-set.json"),
            "raw_journal": sha256_file(journal_path) if not path_is_linklike(journal_path) and journal_path.is_file() else None,
            "canonical_journal": sha256_file(canonical_journal_path) if not path_is_linklike(canonical_journal_path) and canonical_journal_path.is_file() else None,
            "manifest": sha256_file(manifest_path) if not path_is_linklike(manifest_path) and manifest_path.is_file() else None,
        }
        manifest: dict[str, Any] | None = None
        canonical_journal: dict[str, Any] | None = None
        completion: dict[str, Any] | None = None
        if os.path.lexists(manifest_path) and not path_is_linklike(manifest_path) and manifest_path.is_file():
            try:
                loaded_manifest = read_json(manifest_path)
                if isinstance(loaded_manifest, dict):
                    manifest = loaded_manifest
            except (OSError, json.JSONDecodeError):
                pass
        if os.path.lexists(canonical_journal_path) and not path_is_linklike(canonical_journal_path) and canonical_journal_path.is_file():
            try:
                loaded_journal = read_json(canonical_journal_path)
                if isinstance(loaded_journal, dict):
                    canonical_journal = loaded_journal
            except (OSError, json.JSONDecodeError):
                pass
        try:
            loaded_completion = read_json(completion_path)
            if isinstance(loaded_completion, dict):
                completion = loaded_completion
        except (OSError, json.JSONDecodeError):
            pass
        if manifest is None:
            problems.append("aggregate_manifest_object_schema")
        else:
            if manifest.get("schema") != "ck3chronicle.phase1-runner-result-manifest" or manifest.get("schema_version") != 1:
                problems.append("aggregate_manifest_schema")
            if manifest.get("result_set_sha256") != aggregate_hashes["result_set"]:
                problems.append("aggregate_result_set_identity")
            if manifest.get("journal_sha256") != aggregate_hashes["canonical_journal"]:
                problems.append("aggregate_journal_identity")
            if manifest.get("raw_journal_sha256") != aggregate_hashes["raw_journal"]:
                problems.append("aggregate_raw_journal_identity")
            if manifest.get("cases") != sorted(cases, key=lambda item: item["case_id"]):
                problems.append("aggregate_case_inventory")
            if manifest.get("case_count") != len(cases) or manifest.get("closed_at_utc") != result_set.get("closed_at_utc"):
                problems.append("aggregate_case_count_or_close_time")
            if manifest.get("bindings") != {key: result_set.get(key) for key in RESULT_BINDING_KEYS}:
                problems.append("aggregate_bindings")
            retained_total = sum(int(item.get("retained_bytes") or 0) for item in cases)
            if manifest.get("retained_bytes_total") != retained_total:
                problems.append("aggregate_retained_bytes_total")
            if manifest.get("retention_bounds") != {"per_file_bytes": MAX_RETAINED_FILE_BYTES, "per_case_bytes": MAX_RETAINED_CASE_BYTES}:
                problems.append("aggregate_retention_bounds")
        if canonical_journal is None:
            problems.append("canonical_journal_object_schema")
        else:
            if canonical_journal.get("schema") != "ck3chronicle.phase1-canonical-result-journal" or canonical_journal.get("schema_version") != 1:
                problems.append("canonical_journal_schema")
            if canonical_journal.get("entries") != raw_journal_entries or raw_journal_entries != derived_journal_entries:
                problems.append("canonical_raw_journal_reconciliation")
        if completion is None:
            problems.append("aggregate_completion_object_schema")
        else:
            case_inventory_sha = hashlib.sha256(canonical_json_bytes(sorted(cases, key=lambda item: item["case_id"]))).hexdigest()
            expected_completion = {
                "schema": "ck3chronicle.phase1-result-completion-marker",
                "schema_version": 1,
                "result_set_sha256": aggregate_hashes["result_set"],
                "raw_journal_sha256": aggregate_hashes["raw_journal"],
                "canonical_journal_sha256": aggregate_hashes["canonical_journal"],
                "manifest_sha256": aggregate_hashes["manifest"],
                "case_inventory_sha256": case_inventory_sha,
                "case_count": len(cases),
                "closed_at_utc": result_set.get("closed_at_utc"),
            }
            if completion != expected_completion:
                problems.append("aggregate_completion_binding")
        for path, kind in nofollow_tree_entries(results_root):
            if kind == "file" and path.stat().st_mode & stat.S_IWUSR:
                problems.append(f"closed_result_writable:{path.relative_to(results_root).as_posix()}")
    else:
        if result_set.get("status") == "closed" or require_closed:
            problems.append("aggregate_completion_marker_missing")
        if result_set.get("status") == "open" and raw_journal_entries:
            problems.append("open_result_raw_journal_not_empty")
    top_entries = list(results_root.iterdir())
    top_files = {path.name for path in top_entries if not path_is_linklike(path) and path.is_file()}
    top_directories = {path.name for path in top_entries if not path_is_linklike(path) and path.is_dir()}
    top_special = sorted(path.name for path in top_entries if path_is_linklike(path) or (not path.is_file() and not path.is_dir()))
    if top_special:
        problems.append("result_set_special_top_entries:" + ",".join(top_special))
    if aggregate_recovery:
        if not top_files.issubset(known_aggregate_files) or not {"result-set.json", "journal.ndjson"}.issubset(top_files):
            problems.append("result_set_exact_top_file_set")
    elif top_files != expected_top_files:
        problems.append("result_set_exact_top_file_set")
    if top_directories != {".open", "cases"}:
        problems.append("result_set_exact_top_directory_set")
    return {
        "schema": "ck3chronicle.phase1-result-set-verification",
        "schema_version": 1,
        "verified": not problems,
        "problems": problems,
        "case_count": len(cases),
        "cases": cases,
        "open_envelope_count": len(open_entries),
        "partial_case_count": len(partial_cases),
        "partial_cases": partial_cases,
        "invalid_completed_case_count": len(invalid_completed_cases),
        "invalid_completed_cases": invalid_completed_cases,
        "aggregate_completed": aggregate_completed,
        "derived_journal_entries": derived_journal_entries,
    }


def close_result_set(
    results_root: Path,
    expected_cases: dict[str, dict[str, Any]],
    expected_bindings: dict[str, str],
    before_aggregate_step: Callable[[str, Path], None] | None = None,
    atomic_fault_hook: Callable[[str, Path, Path], None] | None = None,
    replace_operation: Callable[[Path, Path], None] | None = None,
) -> dict[str, Any]:
    if path_is_linklike(results_root) or not results_root.is_dir():
        raise RuntimeError("result root is linklike or non-directory")
    completion_path = results_root / RESULT_COMPLETION_MARKER
    if os.path.lexists(completion_path):
        if path_is_linklike(completion_path) or not completion_path.is_file():
            raise RuntimeError("result completion marker path is a symlink or non-regular entry; recovery is forbidden")
        verification = verify_result_set(
            results_root,
            require_closed=True,
            expected_cases=expected_cases,
            expected_bindings=expected_bindings,
        )
        if not verification["verified"]:
            raise RuntimeError("completed result set is invalid; recovery is forbidden: " + json.dumps(verification["problems"], sort_keys=True))
        return {
            "manifest_sha256": sha256_file(results_root / "runner-result.manifest.json"),
            "journal_sha256": sha256_file(results_root / "runner-result.journal.json"),
            "raw_journal_sha256": sha256_file(results_root / "journal.ndjson"),
            "completion_marker_sha256": sha256_file(completion_path),
            "case_count": verification["case_count"],
            "recovered": False,
            "already_complete": True,
            "removed_incomplete_temps": [],
        }
    removed_incomplete_temps = remove_incomplete_aggregate_temps(results_root)
    verification = verify_result_set(
        results_root,
        expected_cases=expected_cases,
        expected_bindings=expected_bindings,
        aggregate_recovery=True,
    )
    actual = {entry["case_id"] for entry in verification["cases"]}
    missing = sorted(set(expected_cases) - actual)
    extra = sorted(actual - set(expected_cases))
    if verification["problems"] or missing or extra:
        raise RuntimeError(
            "cannot close result set: "
            + json.dumps({"verification": verification["problems"], "missing": missing, "extra": extra}, sort_keys=True)
        )
    result_set_path = results_root / "result-set.json"
    result_set = read_json(result_set_path)
    journal_entries = verification["derived_journal_entries"]
    intermediate_paths = (
        result_set_path,
        results_root / "journal.ndjson",
        results_root / "runner-result.journal.json",
        results_root / "runner-result.manifest.json",
    )
    recovered = (
        result_set.get("status") == "closed"
        or any(path.exists() for path in intermediate_paths[2:])
        or (intermediate_paths[1].is_file() and intermediate_paths[1].stat().st_size > 0)
    )
    for path in intermediate_paths:
        if path.is_file():
            path.chmod(stat.S_IREAD | stat.S_IWRITE)

    def boundary(name: str, path: Path) -> None:
        if before_aggregate_step is not None:
            before_aggregate_step(name, path)

    raw_journal_payload = b"".join(canonical_json_bytes(entry) for entry in journal_entries)
    boundary("raw_journal", results_root / "journal.ndjson")
    raw_journal_hash = write_atomic_bytes(
        results_root / "journal.ndjson",
        raw_journal_payload,
        atomic_fault_hook=atomic_fault_hook,
        replace_operation=replace_operation,
    )
    journal_payload = {
        "schema": "ck3chronicle.phase1-canonical-result-journal",
        "schema_version": 1,
        "entries": journal_entries,
    }
    boundary("canonical_journal", results_root / "runner-result.journal.json")
    journal_hash = write_canonical_json(
        results_root / "runner-result.journal.json",
        journal_payload,
        atomic_fault_hook=atomic_fault_hook,
        replace_operation=replace_operation,
    )
    result_set["status"] = "closed"
    result_set["closed_at_utc"] = utc_now()
    boundary("closed_result_set", result_set_path)
    write_canonical_json(
        result_set_path,
        result_set,
        atomic_fault_hook=atomic_fault_hook,
        replace_operation=replace_operation,
    )
    manifest = {
        "schema": "ck3chronicle.phase1-runner-result-manifest",
        "schema_version": 1,
        "result_set_sha256": sha256_file(result_set_path),
        "journal_sha256": journal_hash,
        "raw_journal_sha256": raw_journal_hash,
        "case_count": len(verification["cases"]),
        "cases": sorted(verification["cases"], key=lambda item: item["case_id"]),
        "bindings": {key: result_set.get(key) for key in RESULT_BINDING_KEYS},
        "retained_bytes_total": sum(int(item.get("retained_bytes") or 0) for item in verification["cases"]),
        "retention_bounds": {"per_file_bytes": MAX_RETAINED_FILE_BYTES, "per_case_bytes": MAX_RETAINED_CASE_BYTES},
        "closed_at_utc": result_set["closed_at_utc"],
    }
    boundary("aggregate_manifest", results_root / "runner-result.manifest.json")
    manifest_hash = write_canonical_json(
        results_root / "runner-result.manifest.json",
        manifest,
        atomic_fault_hook=atomic_fault_hook,
        replace_operation=replace_operation,
    )
    boundary("aggregate_immutability", results_root)
    for path in intermediate_paths:
        path.chmod(stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
    completion = {
        "schema": "ck3chronicle.phase1-result-completion-marker",
        "schema_version": 1,
        "result_set_sha256": sha256_file(result_set_path),
        "raw_journal_sha256": raw_journal_hash,
        "canonical_journal_sha256": journal_hash,
        "manifest_sha256": manifest_hash,
        "case_inventory_sha256": hashlib.sha256(canonical_json_bytes(sorted(verification["cases"], key=lambda item: item["case_id"]))).hexdigest(),
        "case_count": len(verification["cases"]),
        "closed_at_utc": result_set["closed_at_utc"],
    }
    boundary("result_completion_marker", completion_path)
    completion_sha = write_atomic_readonly_bytes(
        completion_path,
        canonical_json_bytes(completion),
        atomic_fault_hook=atomic_fault_hook,
        replace_operation=replace_operation,
    )
    post = verify_result_set(
        results_root,
        require_closed=True,
        expected_cases=expected_cases,
        expected_bindings=expected_bindings,
    )
    if not post["verified"]:
        raise RuntimeError("aggregate post-close verification failed: " + json.dumps(post["problems"], sort_keys=True))
    return {
        "manifest_sha256": manifest_hash,
        "journal_sha256": journal_hash,
        "raw_journal_sha256": raw_journal_hash,
        "completion_marker_sha256": completion_sha,
        "case_count": len(verification["cases"]),
        "recovered": recovered,
        "already_complete": False,
        "removed_incomplete_temps": removed_incomplete_temps,
    }


def new_scratch_directory(scratch_root: Path, case_id: str) -> Path:
    return Path(tempfile.mkdtemp(prefix=f"{case_id}-", dir=scratch_root))
