"""Incremental evidence cache and immutable model revisions for the WIP learner.

This module never reads CK3's live log directory.  It inventories protected
ck3chronicle session/pending copies, hashes a protected path only when its
size/mtime identity is new, parses each distinct content hash once per explicit
normalizer version, and builds models entirely from cached sequence evidence.

New evidence is deliberately ``candidate`` by default.  It cannot influence a
training model until a human or controlled workflow changes its role to
``training``.  ``holdout`` evidence remains available for frozen inference but
is never admitted to training.
"""
from __future__ import annotations

import argparse
import collections
import contextlib
import dataclasses
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import uuid
from pathlib import Path
from typing import Callable, Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import learn_error_templates as learner


REGISTRY_SCHEMA = "ck3chronicle.incremental-template-registry"
REGISTRY_SCHEMA_VERSION = 1
FEATURE_SCHEMA = "ck3chronicle.empirical-sequence-evidence"
FEATURE_SCHEMA_VERSION = 1
REVISION_SCHEMA = "ck3chronicle.empirical-model-revision"
REVISION_SCHEMA_VERSION = 1
ROLES = frozenset({"candidate", "training", "holdout", "ignored"})


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
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
        "normalizer_version": learner.NORMALIZER_VERSION,
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
        raise ValueError(f"unsupported incremental registry schema: {path}")
    return registry


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


def feature_cache_path(state_root: Path, evidence_sha256: str) -> Path:
    version_hash = hashlib.sha256(learner.NORMALIZER_VERSION.encode("utf-8")).hexdigest()[:12]
    return state_root / "evidence" / evidence_sha256 / f"features-{version_hash}.json"


def feature_from_log(item: learner.ProtectedLog) -> dict:
    records_by_source, evidence_stats = learner.collect_records([item])
    records = [
        {
            "source_family": record.source_family,
            "tokens": list(record.tokens),
            "semantic_lead": list(record.semantic_lead),
            "occurrences": record.occurrences,
            "examples": record.examples,
            "location_evidence_examples": record.location_examples,
            "structured_slot_examples": record.structured_slot_examples,
        }
        for source_family in sorted(records_by_source)
        for record in sorted(records_by_source[source_family], key=lambda row: row.tokens)
    ]
    stats = evidence_stats[item.evidence_id]
    return {
        "schema": FEATURE_SCHEMA,
        "schema_version": FEATURE_SCHEMA_VERSION,
        "normalizer_version": learner.NORMALIZER_VERSION,
        "evidence_sha256": item.sha256,
        "bytes": item.bytes,
        "timestamped_blocks": stats["timestamped_blocks"],
        "eligible_occurrences": stats["eligible_messages"],
        "records": records,
    }


def validate_feature(feature: dict, evidence_sha256: str) -> None:
    if (
        feature.get("schema") != FEATURE_SCHEMA
        or feature.get("schema_version") != FEATURE_SCHEMA_VERSION
        or feature.get("normalizer_version") != learner.NORMALIZER_VERSION
        or feature.get("evidence_sha256") != evidence_sha256
    ):
        raise ValueError(f"invalid or stale feature cache for {evidence_sha256}")


def _observed_path(kind: str, evidence_id: str, path: Path) -> dict:
    return {"kind": kind, "evidence_id": evidence_id, "path": str(path.resolve())}


def sync_registry(
    runtime_root: Path,
    state_root: Path,
    *,
    default_role: str = "candidate",
    hasher: Callable[[Path], str] = learner.sha256_file,
    feature_builder: Callable[[learner.ProtectedLog], dict] = feature_from_log,
) -> dict:
    if default_role not in ROLES:
        raise ValueError(f"invalid evidence role: {default_role}")
    with state_lock(state_root):
        registry = load_registry(state_root)
        inventory = registry.setdefault("path_inventory", {})
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
            cached = inventory.get(path_key)
            if (
                cached
                and cached.get("bytes") == stat.st_size
                and cached.get("modified_ns") == stat.st_mtime_ns
            ):
                digest = cached["sha256"]
            else:
                digest = hasher(path)
                summary["paths_hashed"] += 1
            inventory[path_key] = {
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

            cache_path = feature_cache_path(state_root, digest)
            relative_cache = cache_path.relative_to(state_root).as_posix()
            cache_record = entry["feature_caches"].get(learner.NORMALIZER_VERSION)
            feature: dict | None = None
            if cache_record and cache_path.is_file():
                raw = cache_path.read_bytes()
                if sha256_bytes(raw) != cache_record["sha256"]:
                    raise ValueError(f"feature-cache hash mismatch: {cache_path}")
                feature = json.loads(raw)
                validate_feature(feature, digest)
            if feature is None:
                item = learner.ProtectedLog(
                    evidence_id=digest,
                    kind=kind,
                    path=path,
                    sha256=digest,
                    bytes=stat.st_size,
                    modified_ns=stat.st_mtime_ns,
                )
                feature = feature_builder(item)
                validate_feature(feature, digest)
                raw = canonical_bytes(feature)
                if cache_path.is_file() and cache_path.read_bytes() != raw:
                    raise ValueError(f"immutable feature cache disagrees: {cache_path}")
                if not cache_path.is_file():
                    atomic_write(cache_path, raw)
                entry["feature_caches"][learner.NORMALIZER_VERSION] = {
                    "path": relative_cache,
                    "sha256": sha256_bytes(raw),
                    "timestamped_blocks": feature["timestamped_blocks"],
                    "eligible_occurrences": feature["eligible_occurrences"],
                }
                summary["new_feature_caches"] += 1
        registry["normalizer_version"] = learner.NORMALIZER_VERSION
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


def load_feature(state_root: Path, entry: dict) -> dict:
    cache = entry["feature_caches"].get(learner.NORMALIZER_VERSION)
    if cache is None:
        raise ValueError(f"no current feature cache for {entry['sha256']}; run sync")
    path = state_root / Path(cache["path"])
    raw = path.read_bytes()
    if sha256_bytes(raw) != cache["sha256"]:
        raise ValueError(f"feature-cache hash mismatch: {path}")
    feature = json.loads(raw)
    validate_feature(feature, entry["sha256"])
    return feature


def combine_training_records(state_root: Path, entries: Iterable[dict]) -> tuple[dict, dict]:
    merged: dict[tuple[str, tuple[str, ...]], learner.SequenceRecord] = {}
    evidence_stats: dict[str, dict] = {}
    for entry in sorted(entries, key=lambda row: row["sha256"]):
        feature = load_feature(state_root, entry)
        evidence_sha = entry["sha256"]
        first_observation = entry["observed_paths"][0]
        evidence_stats[evidence_sha] = {
            "kind": first_observation["kind"],
            "path": first_observation["path"],
            "sha256": evidence_sha,
            "bytes": feature["bytes"],
            "timestamped_blocks": feature["timestamped_blocks"],
            "eligible_messages": feature["eligible_occurrences"],
        }
        for row in feature["records"]:
            tokens = tuple(row["tokens"])
            key = (row["source_family"], tokens)
            record = merged.get(key)
            if record is None:
                record = learner.SequenceRecord(
                    source_family=row["source_family"],
                    tokens=tokens,
                    semantic_lead=tuple(row["semantic_lead"]),
                )
                merged[key] = record
            elif record.semantic_lead != tuple(row["semantic_lead"]):
                raise ValueError(f"semantic-lead disagreement for {key}")
            record.occurrences += int(row["occurrences"])
            record.evidence_ids.add(evidence_sha)
            for example in row.get("examples", []):
                if len(record.examples) < 3 and example not in record.examples:
                    record.examples.append(example)
            for example in row.get("location_evidence_examples", []):
                if len(record.location_examples) < 3 and example not in record.location_examples:
                    record.location_examples.append(example)
            for slots in row.get("structured_slot_examples", []):
                if len(record.structured_slot_examples) < 3 and slots not in record.structured_slot_examples:
                    record.structured_slot_examples.append(slots)
    by_source: dict[str, list[learner.SequenceRecord]] = collections.defaultdict(list)
    for record in merged.values():
        by_source[record.source_family].append(record)
    return dict(by_source), evidence_stats


def build_revision(state_root: Path, oracle_root: Path, threshold: float = 0.72) -> dict:
    with state_lock(state_root):
        registry = load_registry(state_root)
        training = [row for row in registry["evidence"].values() if row["role"] == "training"]
        if not training:
            raise ValueError("no evidence is approved for training")
        revision_spec = {
            "normalizer_version": learner.NORMALIZER_VERSION,
            "clusterer_version": learner.CLUSTERER_VERSION,
            "threshold": threshold,
            "training_sha256": sorted(row["sha256"] for row in training),
        }
        revision_id = sha256_bytes(canonical_bytes(revision_spec))[:16]
        records_by_source, evidence_stats = combine_training_records(state_root, training)
        clusters_by_source = {
            source: learner.cluster_source_records(source, records, threshold)
            for source, records in sorted(records_by_source.items())
        }
        clusters = [
            cluster
            for source in sorted(clusters_by_source)
            for cluster in clusters_by_source[source]
        ]
        clusters.sort(key=lambda row: (-row.support_occurrences, row.source_family, row.cluster_id))
        evaluation = learner.evaluate_frozen_oracle(clusters_by_source, oracle_root, threshold)
        nontraining = [
            {
                "sha256": row["sha256"],
                "role": row["role"],
                "bytes": row["bytes"],
            }
            for row in registry["evidence"].values()
            if row["role"] != "training"
        ]
        model = {
            "schema": "ck3chronicle-empirical-template-calibration",
            "schema_version": 3,
            "revision": {"revision_id": revision_id, **revision_spec},
            "algorithm": {
                "source_family_hard_partition": True,
                "locator_masking": "deterministic-v2-semantic-evidence-separation",
                "script_location_tail_in_template_identity": False,
                "repeated_clause_expansion": "persistent-reader-v1",
                "structured_key_slots": "multi-key-with-optional-key-v1",
                "script_system_layering": "exact-outer-envelope-plus-reason-contract-v1",
                "alignment": "difflib-sequence-matcher-ordered-tokens",
                "cluster_threshold": threshold,
                "stable_token_ratio": 0.80,
                "normalizer_version": learner.NORMALIZER_VERSION,
                "clusterer_version": learner.CLUSTERER_VERSION,
                "status": "wip_incremental_calibration_not_production",
            },
            "summary": {
                "distinct_error_logs": len(training),
                "excluded_error_logs": len(nontraining),
                "duplicate_copies_skipped": sum(
                    max(0, len(row["observed_paths"]) - 1)
                    for row in registry["evidence"].values()
                ),
                "timestamped_blocks": sum(row["timestamped_blocks"] for row in evidence_stats.values()),
                "source_families": len(records_by_source),
                "unique_masked_sequences": sum(len(rows) for rows in records_by_source.values()),
                "clusters": len(clusters),
            },
            "evidence": evidence_stats,
            "excluded_evidence": sorted(nontraining, key=lambda row: row["sha256"]),
            "duplicates": [],
            "evaluation": evaluation,
            "clusters": [learner.serializable_cluster(cluster) for cluster in clusters],
        }
        stage = state_root / f".revision-{revision_id}-{uuid.uuid4().hex}"
        final = state_root / "revisions" / revision_id
        try:
            stage.mkdir(parents=True)
            model_path = stage / "empirical_template_model.json"
            model_path.write_bytes(canonical_bytes(model))
            learner.write_report(model, stage / "EMPIRICAL_TEMPLATE_CALIBRATION.md")
            model_sha = learner.sha256_file(model_path)
            manifest = {
                "schema": REVISION_SCHEMA,
                "schema_version": REVISION_SCHEMA_VERSION,
                "revision_id": revision_id,
                "spec": revision_spec,
                "model_sha256": model_sha,
            }
            write_json(stage / "manifest.json", manifest)
            final.parent.mkdir(parents=True, exist_ok=True)
            if final.exists():
                existing = json.loads((final / "manifest.json").read_text(encoding="utf-8"))
                if existing != manifest:
                    raise ValueError(f"immutable revision disagrees: {final}")
            else:
                os.replace(stage, final)
            if not any(row["revision_id"] == revision_id for row in registry["revisions"]):
                registry["revisions"].append({"created_at": utc_now(), **manifest})
            registry["current_revision"] = revision_id
            write_json(state_root / "registry.json", registry)
            return {
                "revision_id": revision_id,
                "model_sha256": model_sha,
                "model_path": str(final / "empirical_template_model.json"),
                "training_evidence": len(training),
                "clusters": len(clusters),
                "timestamped_blocks": model["summary"]["timestamped_blocks"],
            }
        finally:
            if stage.exists():
                shutil.rmtree(stage)


def status(state_root: Path) -> dict:
    registry = load_registry(state_root)
    return {
        "state_root": str(state_root),
        "normalizer_version": registry["normalizer_version"],
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
                "cached": learner.NORMALIZER_VERSION in row["feature_caches"],
            }
            for row in sorted(registry["evidence"].values(), key=lambda item: item["sha256"])
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--state-root",
        type=Path,
        default=Path.home() / ".ck3chronicle" / "template-learning",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    sync = commands.add_parser("sync")
    sync.add_argument(
        "--runtime-root",
        type=Path,
        default=Path.home() / "AppData" / "Local" / "ck3chronicle",
    )
    sync.add_argument("--default-role", choices=sorted(ROLES), default="candidate")
    role = commands.add_parser("role")
    role.add_argument("sha256")
    role.add_argument("role", choices=sorted(ROLES))
    build = commands.add_parser("build")
    build.add_argument(
        "--oracle-root",
        type=Path,
        required=True,
    )
    build.add_argument("--threshold", type=float, default=0.72)
    commands.add_parser("status")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "sync":
        result = sync_registry(args.runtime_root, args.state_root, default_role=args.default_role)
    elif args.command == "role":
        result = set_role(args.state_root, args.sha256, args.role)
    elif args.command == "build":
        result = build_revision(args.state_root, args.oracle_root, args.threshold)
    else:
        result = status(args.state_root)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
