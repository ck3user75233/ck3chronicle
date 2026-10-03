"""Version-isolated evidence cache and additive cumulative learner builds.

This module never reads CK3's live log directory.  It inventories protected
ck3chronicle session/pending copies, hashes a protected path only when its
size/mtime identity is new, parses each distinct content hash with the explicitly selected
parser artifact and native feature version, and builds models entirely from cached sequence evidence.

New evidence is deliberately ``candidate`` by default.  It cannot influence a
training model until a human or controlled workflow changes its role to
``training``.  ``holdout`` evidence remains available for frozen inference but
is never admitted to training.
"""
from __future__ import annotations

import argparse
import collections
import contextlib
import datetime as dt
import hashlib
import json
import os
import uuid
from pathlib import Path
from typing import Callable, Iterable

from ck3chronicle import config as project_config

from template_learning import records, inventory, artifacts
from template_learning.parsers import SelectedParser, load_parser, reference_from_manifest


REGISTRY_SCHEMA = "ck3chronicle.incremental-template-registry"
REGISTRY_SCHEMA_VERSION = 4
FEATURE_SCHEMA = "ck3chronicle.empirical-sequence-evidence"
FEATURE_SCHEMA_VERSION = 4
ROLES = frozenset({"candidate", "training", "holdout", "ignored"})


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}-{uuid.uuid4().hex}")
    try:
        with temporary.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def write_json(path: Path, value: object) -> None:
    atomic_write(path, canonical_bytes(value))


@contextlib.contextmanager
def state_lock(state_root: Path):
    state_root.mkdir(parents=True, exist_ok=True)
    lock_path = state_root / ".registry.lock"
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as error:
        raise RuntimeError(f"incremental registry is already locked: {lock_path}") from error
    try:
        os.write(descriptor, f"pid={os.getpid()}\n".encode("ascii"))
        os.close(descriptor)
        yield
    finally:
        try:
            os.close(descriptor)
        except OSError:
            pass
        lock_path.unlink(missing_ok=True)


def empty_registry() -> dict:
    return {
        "schema": REGISTRY_SCHEMA,
        "schema_version": REGISTRY_SCHEMA_VERSION,
        "learner": artifacts.learner_identity(),
        "feature_version": records.FEATURE_VERSION,
        "path_inventory": {},
        "evidence": {},
        "revisions": [],
        "current_revision": None,
    }


def load_registry(state_root: Path) -> dict:
    path = state_root / "registry.json"
    if not path.is_file():
        return empty_registry()
    registry = json.loads(path.read_text(encoding="utf-8"))
    if (
        registry.get("schema") != REGISTRY_SCHEMA
        or registry.get("schema_version") != REGISTRY_SCHEMA_VERSION
    ):
        raise ValueError(f"unsupported registry schema; create a fresh learner registry: {path}")
    if registry.get("learner") != artifacts.learner_identity():
        raise ValueError(f"registry belongs to a different learner implementation; create a fresh registry: {path}")
    return registry


def check_registry_parser(registry, parser):
    if registry.get("parser") not in (None, parser.reference.to_dict()):
        raise ValueError("registry is pinned to another parser; create a fresh registry")


def candidate_paths(runtime_root: Path) -> list[tuple[str, str, Path]]:
    candidates: list[tuple[str, str, Path]] = []
    sessions = runtime_root / "sessions"
    if sessions.is_dir():
        for directory in sorted(sessions.iterdir(), key=lambda item: item.name):
            path = directory / "error.log"
            if directory.is_dir() and directory.name != ".staging" and path.is_file():
                candidates.append(("session", directory.name, path))
    pending = runtime_root / "pending"
    if pending.is_dir():
        for directory in sorted(pending.iterdir(), key=lambda item: item.name):
            path = directory / "error.log"
            if (
                directory.is_dir()
                and not directory.name.startswith(".copying-")
                and path.is_file()
            ):
                candidates.append(("pending", directory.name, path))
    return candidates


def feature_key(parser: SelectedParser) -> str:
    return sha256_bytes(canonical_bytes({"learner": artifacts.learner_identity(),
                                        "feature_version": records.FEATURE_VERSION,
                                        "parser": parser.reference.to_dict()}))


def feature_cache_path(state_root: Path, evidence_sha256: str, *, parser: SelectedParser) -> Path:
    version_hash = feature_key(parser)[:12]
    return state_root / "evidence" / evidence_sha256 / f"features-{version_hash}.json"


def feature_from_log(item: inventory.ProtectedLog, *, parser: SelectedParser) -> dict:
    grouped, stats = records.collect_records([item], parser=parser)
    detail = stats[item.sha256]
    return {"schema": FEATURE_SCHEMA, "schema_version": FEATURE_SCHEMA_VERSION,
        "learner": artifacts.learner_identity(),
        "feature_version": records.FEATURE_VERSION, "parser": parser.reference.to_dict(),
        "record_scope": "message", "evidence_sha256": item.sha256, "bytes": item.bytes,
        "timestamped_blocks": detail["timestamped_blocks"],
        "eligible_occurrences": detail["recovered_messages"], "evidence_stats": detail,
        "records": [record.to_dict() for source in sorted(grouped) for record in grouped[source]]}


def validate_feature(feature: dict, evidence_sha256: str, *, parser: SelectedParser) -> None:
    if (feature.get("schema") != FEATURE_SCHEMA or feature.get("schema_version") != FEATURE_SCHEMA_VERSION
        or feature.get("learner") != artifacts.learner_identity()
        or feature.get("feature_version") != records.FEATURE_VERSION
        or feature.get("parser") != parser.reference.to_dict()
        or feature.get("record_scope") != "message" or feature.get("evidence_sha256") != evidence_sha256):
        raise ValueError(f"invalid or stale feature cache for {evidence_sha256}")
    restored = [records.SequenceRecord.from_dict(row) for row in feature["records"]]
    if sum(r.occurrences for r in restored) != feature["eligible_occurrences"]:
        raise ValueError("feature occurrence accounting disagrees")
    if any(o["evidence_sha256"] != evidence_sha256 for r in restored for o in r.native_occurrences):
        raise ValueError("feature native provenance disagrees")
    stats = feature["evidence_stats"]
    if stats["recovered_messages"] != feature["eligible_occurrences"] or stats["sha256"] != evidence_sha256:
        raise ValueError("feature evidence statistics disagree")
    recovered = {ordinal for r in restored for o in r.native_occurrences
                 for ordinal in o.get('emission_ordinals', [o['emission_ordinal']])}
    unresolved = {ordinal for r in stats["unresolved_emissions"]
                  for ordinal in r.get("emission_ordinals", [r["emission_ordinal"]])}
    if stats['deferred_recovered_messages'] != sum(
            r.get('recovery_status') == 'recovered' for r in stats['unresolved_emissions']):
        raise ValueError('feature deferred recovery accounting disagrees')
    if recovered & unresolved or recovered | unresolved != set(range(feature["timestamped_blocks"])):
        raise ValueError("feature emission accounting disagrees")


def _observed_path(kind: str, evidence_id: str, path: Path) -> dict:
    return {"kind": kind, "evidence_id": evidence_id, "path": str(path.resolve())}


def sync_registry(
    runtime_root: Path,
    state_root: Path,
    *,
    parser: SelectedParser,
    default_role: str = "candidate",
    hasher: Callable[[Path], str] = inventory.sha256_file,
) -> dict:
    if default_role not in ROLES:
        raise ValueError(f"invalid evidence role: {default_role}")
    with state_lock(state_root):
        registry = load_registry(state_root)
        check_registry_parser(registry, parser)
        path_inventory = registry.setdefault("path_inventory", {})
        evidence = registry.setdefault("evidence", {})
        summary = {
            "paths_seen": 0,
            "paths_hashed": 0,
            "new_evidence": 0,
            "new_feature_caches": 0,
            "duplicate_observations": 0,
            "known_evidence": 0,
        }
        for kind, evidence_id, path in candidate_paths(runtime_root):
            summary["paths_seen"] += 1
            stat = path.stat()
            path_key = str(path.resolve())
            cached = path_inventory.get(path_key)
            if (
                cached
                and cached.get("bytes") == stat.st_size
                and cached.get("modified_ns") == stat.st_mtime_ns
            ):
                digest = cached["sha256"]
            else:
                digest = hasher(path)
                summary["paths_hashed"] += 1
            path_inventory[path_key] = {
                "bytes": stat.st_size,
                "modified_ns": stat.st_mtime_ns,
                "sha256": digest,
            }

            observation = _observed_path(kind, evidence_id, path)
            entry = evidence.get(digest)
            if entry is None:
                entry = {
                    "sha256": digest,
                    "role": default_role,
                    "bytes": stat.st_size,
                    "first_seen_at": utc_now(),
                    "observed_paths": [],
                    "feature_caches": {},
                }
                evidence[digest] = entry
                summary["new_evidence"] += 1
            else:
                summary["known_evidence"] += 1
            if observation not in entry["observed_paths"]:
                if entry["observed_paths"]:
                    summary["duplicate_observations"] += 1
                entry["observed_paths"].append(observation)

            cache_path = feature_cache_path(state_root, digest, parser=parser)
            relative_cache = cache_path.relative_to(state_root).as_posix()
            cache_record = entry["feature_caches"].get(feature_key(parser))
            feature: dict | None = None
            if cache_record and cache_path.is_file():
                raw = cache_path.read_bytes()
                if sha256_bytes(raw) != cache_record["sha256"]:
                    raise ValueError(f"feature-cache hash mismatch: {cache_path}")
                feature = json.loads(raw)
                validate_feature(feature, digest, parser=parser)
            if feature is None:
                item = inventory.ProtectedLog(
                    evidence_id=digest,
                    kind=kind,
                    path=path,
                    sha256=digest,
                    bytes=stat.st_size,
                    modified_ns=stat.st_mtime_ns,
                )
                feature = feature_from_log(item, parser=parser)
                validate_feature(feature, digest, parser=parser)
                raw = canonical_bytes(feature)
                if cache_path.is_file() and cache_path.read_bytes() != raw:
                    raise ValueError(f"immutable feature cache disagrees: {cache_path}")
                if not cache_path.is_file():
                    atomic_write(cache_path, raw)
                entry["feature_caches"][feature_key(parser)] = {
                    "path": relative_cache,
                    "sha256": sha256_bytes(raw),
                    "timestamped_blocks": feature["timestamped_blocks"],
                    "eligible_occurrences": feature["eligible_occurrences"],
                }
                summary["new_feature_caches"] += 1
        registry["feature_version"] = records.FEATURE_VERSION
        registry["parser"] = parser.reference.to_dict()
        write_json(state_root / "registry.json", registry)
        summary["distinct_evidence"] = len(evidence)
        summary["roles"] = dict(
            sorted(collections.Counter(row["role"] for row in evidence.values()).items())
        )
        return summary


def set_role(state_root: Path, evidence_sha256: str, role: str) -> dict:
    if role not in ROLES:
        raise ValueError(f"invalid evidence role: {role}")
    with state_lock(state_root):
        registry = load_registry(state_root)
        try:
            entry = registry["evidence"][evidence_sha256.casefold()]
        except KeyError as error:
            raise KeyError(f"unknown evidence hash: {evidence_sha256}") from error
        prior = entry["role"]
        entry["role"] = role
        write_json(state_root / "registry.json", registry)
        return {"sha256": evidence_sha256.casefold(), "prior_role": prior, "role": role}


def load_feature(state_root: Path, entry: dict, *, parser: SelectedParser) -> dict:
    cache = entry["feature_caches"].get(feature_key(parser))
    if cache is None:
        raise ValueError(f"no current feature cache for {entry['sha256']}; run sync")
    path = state_root / Path(cache["path"])
    raw = path.read_bytes()
    if sha256_bytes(raw) != cache["sha256"]:
        raise ValueError(f"feature-cache hash mismatch: {path}")
    feature = json.loads(raw)
    validate_feature(feature, entry["sha256"], parser=parser)
    return feature


def combine_training_records(state_root: Path, entries: Iterable[dict], *, parser: SelectedParser) -> tuple[dict, dict]:
    rows, evidence_stats = [], {}
    for entry in sorted(entries, key=lambda row: row["sha256"]):
        feature = load_feature(state_root, entry, parser=parser)
        evidence_stats[entry["sha256"]] = feature["evidence_stats"]
        rows.extend(records.SequenceRecord.from_dict(row) for row in feature["records"])
    return records.merge_records(rows), evidence_stats


def all_patterns(model):
    return {p["template_id"]:p for p in model["templates"]}


def build_revision(state_root: Path, threshold: float = .72, *, parser: SelectedParser) -> dict:
    with state_lock(state_root):
        registry = load_registry(state_root)
        check_registry_parser(registry, parser)
        training = [row for row in registry["evidence"].values() if row["role"] == "training"]
        if not training:
            raise ValueError("no evidence selected for training")
        previous_model = None
        if registry['current_revision'] is not None:
            previous_folder = state_root/'revisions'/registry['current_revision']
            previous_model, _ = artifacts.load_bundle(previous_folder)
            if previous_model['algorithm']['cluster_threshold'] != threshold:
                raise ValueError('additive learning requires the same inference threshold')
        grouped, stats = combine_training_records(state_root, training, parser=parser)
        excluded = [dict(sha256=row["sha256"], role=row["role"], bytes=row["bytes"])
                    for row in registry["evidence"].values() if row["role"] != "training"]
        model, evidence = artifacts.build_model(grouped, stats, parser=parser, threshold=threshold,
            excluded_evidence=sorted(excluded, key=lambda row:row["sha256"]), previous_model=previous_model)
        import sys
        folder = artifacts.write_bundle(state_root/"revisions", model, evidence, parser=parser,
            build_command=[sys.executable,"-m","template_learning.incremental_template_registry",*sys.argv[1:]])
        manifest = json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
        if not any(row["revision_id"] == model["revision_id"] for row in registry["revisions"]):
            registry["revisions"].append({"created_at": utc_now(), **manifest})
        registry["current_revision"] = model["revision_id"]
        write_json(state_root/"registry.json", registry)
        return dict(revision_id=model["revision_id"], bundle=str(folder),
            model_path=str(folder/"empirical_template_model.json"),
            model_sha256=manifest["hashes"]["empirical_template_model.json"],
            **model["summary"])


def status(state_root: Path) -> dict:
    registry = load_registry(state_root)
    return {
        "state_root": str(state_root),
        "learner": registry["learner"],
        "feature_version": registry["feature_version"],
        "distinct_evidence": len(registry["evidence"]),
        "roles": dict(
            sorted(collections.Counter(row["role"] for row in registry["evidence"].values()).items())
        ),
        "revision_count": len(registry["revisions"]),
        "current_revision": registry["current_revision"],
        "evidence": [
            {
                "sha256": row["sha256"],
                "role": row["role"],
                "bytes": row["bytes"],
                "observations": len(row["observed_paths"]),
                "feature_cache_count": len(row["feature_caches"]),
            }
            for row in sorted(registry["evidence"].values(), key=lambda item: item["sha256"])
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    learner = artifacts.learner_identity()
    parser.add_argument(
        "--state-root",
        type=Path,
        default=project_config.ROOT_LEARNER_STATE / (learner['version'] + '-' + learner['sha256'][:12]),
    )
    commands = parser.add_subparsers(dest="command", required=True)
    sync = commands.add_parser("sync")
    sync.add_argument(
        "--runtime-root",
        type=Path,
        default=project_config.ROOT_CK3CHRONICLE,
    )
    sync.add_argument("--parser-manifest", type=Path, required=True)
    sync.add_argument("--default-role", choices=sorted(ROLES), default="candidate")
    role = commands.add_parser("role")
    role.add_argument("sha256")
    role.add_argument("role", choices=sorted(ROLES))
    build = commands.add_parser("build")
    build.add_argument("--parser-manifest", type=Path, required=True)
    build.add_argument("--threshold", type=float, default=0.72)
    commands.add_parser("status")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "sync":
        parser = load_parser(reference_from_manifest(args.parser_manifest))
        result = sync_registry(args.runtime_root, args.state_root, parser=parser, default_role=args.default_role)
    elif args.command == "role":
        result = set_role(args.state_root, args.sha256, args.role)
    elif args.command == "build":
        parser = load_parser(reference_from_manifest(args.parser_manifest))
        result = build_revision(args.state_root, args.threshold, parser=parser)
    else:
        result = status(args.state_root)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
