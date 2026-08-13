"""Same-run DLC and active-mod context from archived ``debug.log`` evidence."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from typing import Iterable

from .db import repository


CONTEXT_CONTRACT_VERSION = "1.0.0"


class RuntimeContextError(RuntimeError):
    """Archived runtime context is missing, corrupt, or structurally invalid."""


@dataclass(frozen=True)
class MountedDlc:
    mount_ordinal: int
    dlc_order: int
    dlc_key: str
    display_name: str | None
    descriptor_path: str | None
    mount_path: str


@dataclass(frozen=True)
class MountedMod:
    mount_ordinal: int
    load_order: int
    mod_key: str
    display_name: str | None
    descriptor_path: str | None
    mount_path: str
    source_kind: str


@dataclass(frozen=True)
class RuntimeContextResult:
    session_id: int
    context_contract_version: str
    status: str
    debug_log_sha256: str | None
    dlcs: tuple[MountedDlc, ...]
    mods: tuple[MountedMod, ...]
    unknown_mount_count: int
    inventory_enabled_mod_count: int
    inventory_dlc_count: int
    warnings: tuple[str, ...]
    mutated: bool


_DLC_MARKER = re.compile(r"^\[[^\]]+\]\[[^\]]+\]\[[^\]]+\]: DLC:$")
_MOUNTED_DATA = re.compile(
    r"^\[[^\]]+\]\[[^\]]+\]\[virtualfilesystem_physfs\.cpp:\d+\]: "
    r"Mounted Data: (?P<path>.+)$",
    re.IGNORECASE,
)
_TIMESTAMPED = re.compile(r"^\[[^\]]+\]\[[^\]]+\]\[[^\]]+\]:")
_DLC_PATH = re.compile(r"(?:^|/)game/dlc/(?P<key>dlc[^/]+)(?:/|$)", re.IGNORECASE)
_DLC_DESCRIPTOR = re.compile(
    r"(?:^|/)dlc/(?P<key>dlc[^/]+)/[^/]+\.dlc$", re.IGNORECASE
)
_WORKSHOP_PATH = re.compile(
    r"(?:^|/)workshop/content/1158310/(?P<key>\d+)(?:/|$)", re.IGNORECASE
)
_WORKSHOP_DESCRIPTOR = re.compile(r"(?:^|/)ugc_(?P<key>\d+)\.mod$", re.IGNORECASE)
_LOCAL_DESCRIPTOR = re.compile(r"(?:^|/)mod/(?P<name>.+)\.mod$", re.IGNORECASE)


def _normalized_path(value: str) -> str:
    return value.strip().replace("\\", "/").rstrip("/")


def _dlc_descriptor_key(path: str) -> str | None:
    match = _DLC_DESCRIPTOR.search(_normalized_path(path))
    return match.group("key").casefold() if match else None


def _mod_descriptor_key(path: str) -> tuple[str, str] | None:
    normalized = _normalized_path(path)
    workshop = _WORKSHOP_DESCRIPTOR.search(normalized)
    if workshop:
        return "workshop", workshop.group("key")
    local = _LOCAL_DESCRIPTOR.search(normalized)
    if local:
        return "local", "local:" + local.group("name").casefold()
    return None


def _unknown_key(path: str) -> str:
    digest = hashlib.sha256(path.casefold().encode("utf-8")).hexdigest()[:16]
    return f"unknown:{digest}"


def _bounded_difference(left: Counter[str], right: Counter[str]) -> list[str]:
    result: list[str] = []
    for key in sorted(left):
        result.extend([key] * max(0, left[key] - right[key]))
        if len(result) >= 20:
            return result[:20]
    return result


def parse_debug_context(lines: Iterable[str]) -> tuple[
    tuple[MountedDlc, ...],
    tuple[MountedMod, ...],
    int,
    int,
    tuple[str, ...],
]:
    """Parse inventory enrichment and authoritative Mounted Data order."""
    mode: str | None = None
    mounted_started = False
    mounted_finished = False
    dlc_inventory: dict[str, tuple[str, str]] = {}
    enabled_mod_inventory: dict[str, tuple[str, str, str]] = {}
    inventory_dlc_keys: list[str] = []
    inventory_enabled_mod_keys: list[str] = []
    dlcs: list[MountedDlc] = []
    mods: list[MountedMod] = []
    warnings: list[str] = []
    mount_ordinal = 0
    dlc_order = 0
    mod_order = 0
    unknown_mount_count = 0

    for raw_line in lines:
        line = raw_line.rstrip("\r\n")
        if mounted_finished:
            continue
        mount = _MOUNTED_DATA.match(line)
        if mount:
            mounted_started = True
            mode = None
            path = _normalized_path(mount.group("path"))
            dlc_match = _DLC_PATH.search(path)
            workshop_match = _WORKSHOP_PATH.search(path)
            if dlc_match:
                key = dlc_match.group("key").casefold()
                inventory = dlc_inventory.get(key)
                dlcs.append(
                    MountedDlc(
                        mount_ordinal=mount_ordinal,
                        dlc_order=dlc_order,
                        dlc_key=key,
                        display_name=inventory[0] if inventory else None,
                        descriptor_path=inventory[1] if inventory else None,
                        mount_path=path,
                    )
                )
                dlc_order += 1
            elif workshop_match:
                key = workshop_match.group("key")
                inventory = enabled_mod_inventory.get(key)
                mods.append(
                    MountedMod(
                        mount_ordinal=mount_ordinal,
                        load_order=mod_order,
                        mod_key=key,
                        display_name=inventory[0] if inventory else None,
                        descriptor_path=inventory[1] if inventory else None,
                        mount_path=path,
                        source_kind="workshop",
                    )
                )
                mod_order += 1
            else:
                leaf = path.rsplit("/", 1)[-1]
                local_key = "local:" + leaf.casefold()
                inventory = enabled_mod_inventory.get(local_key)
                source_kind = "local" if inventory is not None or "/mod/" in path.casefold() else "unknown"
                if source_kind == "unknown":
                    unknown_mount_count += 1
                    local_key = _unknown_key(path)
                mods.append(
                    MountedMod(
                        mount_ordinal=mount_ordinal,
                        load_order=mod_order,
                        mod_key=local_key,
                        display_name=inventory[0] if inventory else None,
                        descriptor_path=inventory[1] if inventory else None,
                        mount_path=path,
                        source_kind=source_kind,
                    )
                )
                mod_order += 1
            mount_ordinal += 1
            continue
        if mounted_started:
            if line:
                mounted_finished = True
            continue

        if _DLC_MARKER.match(line):
            mode = "dlc"
            continue
        if mode == "dlc" and line == "Mod:":
            mode = "mod"
            continue
        if _TIMESTAMPED.match(line):
            mode = None
            continue
        if not line:
            continue
        if mode == "dlc":
            parts = line.rsplit("|", 1)
            if len(parts) != 2:
                warnings.append("malformed DLC inventory entry")
                continue
            display_name, descriptor_path = (item.strip() for item in parts)
            key = _dlc_descriptor_key(descriptor_path)
            if key is None:
                warnings.append(f"unrecognized DLC descriptor: {descriptor_path}")
                continue
            dlc_inventory[key] = (display_name, descriptor_path)
            inventory_dlc_keys.append(key)
        elif mode == "mod":
            parts = line.rsplit("|", 2)
            if len(parts) != 3:
                warnings.append("malformed mod inventory entry")
                continue
            display_name, descriptor_path, state = (item.strip() for item in parts)
            if state.casefold() != "enabled":
                continue
            identity = _mod_descriptor_key(descriptor_path)
            if identity is None:
                warnings.append(f"unrecognized enabled mod descriptor: {descriptor_path}")
                continue
            source_kind, key = identity
            enabled_mod_inventory[key] = (display_name, descriptor_path, source_kind)
            inventory_enabled_mod_keys.append(key)

    mounted_dlc = Counter(item.dlc_key for item in dlcs)
    inventory_dlc = Counter(inventory_dlc_keys)
    mounted_mod = Counter(
        item.mod_key for item in mods if item.source_kind != "unknown"
    )
    inventory_mod = Counter(inventory_enabled_mod_keys)
    if mounted_dlc != inventory_dlc:
        warnings.append(
            "mounted DLC set differs from DLC inventory: mounted_only="
            f"{_bounded_difference(mounted_dlc, inventory_dlc)}, inventory_only="
            f"{_bounded_difference(inventory_dlc, mounted_dlc)}"
        )
    if mounted_mod != inventory_mod:
        warnings.append(
            "mounted mod set differs from Enabled inventory: mounted_only="
            f"{_bounded_difference(mounted_mod, inventory_mod)}, enabled_only="
            f"{_bounded_difference(inventory_mod, mounted_mod)}"
        )
    if unknown_mount_count:
        warnings.append(f"{unknown_mount_count} mounted roots could not be typed")
    if not dlcs and not mods:
        warnings.append("Mounted Data block not found")
    return (
        tuple(dlcs),
        tuple(mods),
        len(inventory_enabled_mod_keys),
        len(inventory_dlc_keys),
        tuple(dict.fromkeys(warnings)),
    )


def _result_from_store(
    conn: sqlite3.Connection,
    session_id: int,
    *,
    mutated: bool,
) -> RuntimeContextResult:
    context = repository.get_runtime_context(conn, session_id)
    if context is None:
        raise RuntimeContextError("runtime context persistence is missing")
    dlcs = tuple(
        MountedDlc(
            mount_ordinal=int(row["mount_ordinal"]),
            dlc_order=int(row["dlc_order"]),
            dlc_key=row["dlc_key"],
            display_name=row["display_name"],
            descriptor_path=row["descriptor_path"],
            mount_path=row["mount_path"],
        )
        for row in repository.get_mounted_dlcs(conn, session_id)
    )
    mods = tuple(
        MountedMod(
            mount_ordinal=int(row["mount_ordinal"]),
            load_order=int(row["load_order"]),
            mod_key=row["mod_key"],
            display_name=row["display_name"],
            descriptor_path=row["descriptor_path"],
            mount_path=row["mount_path"],
            source_kind=row["source_kind"],
        )
        for row in repository.get_mounted_mods(conn, session_id)
    )
    return RuntimeContextResult(
        session_id=session_id,
        context_contract_version=context["context_contract_version"],
        status=context["status"],
        debug_log_sha256=context["debug_log_sha256"],
        dlcs=dlcs,
        mods=mods,
        unknown_mount_count=int(context["unknown_mount_count"]),
        inventory_enabled_mod_count=int(context["inventory_enabled_mod_count"]),
        inventory_dlc_count=int(context["inventory_dlc_count"]),
        warnings=tuple(json.loads(context["warnings_json"])),
        mutated=mutated,
    )


def parse_runtime_context(
    conn: sqlite3.Connection,
    evidence_root: Path,
    session_id: int,
    *,
    reparse: bool = False,
) -> RuntimeContextResult:
    """Parse one immutable debug.log and atomically store mounted runtime state."""
    session = repository.get_session(conn, session_id)
    if session is None:
        raise RuntimeContextError(f"session_id {session_id} not found")
    if session["capture_status"] != "finalized":
        raise RuntimeContextError("session evidence is not finalized")
    manifest = repository.get_log_manifest_row(conn, session_id, "debug.log")
    existing = repository.get_runtime_context(conn, session_id)
    expected_sha = manifest["sha256"] if manifest is not None else None
    if (
        existing is not None
        and not reparse
        and existing["context_contract_version"] == CONTEXT_CONTRACT_VERSION
        and existing["debug_log_sha256"] == expected_sha
    ):
        return _result_from_store(conn, session_id, mutated=False)

    dlcs: tuple[MountedDlc, ...] = ()
    mods: tuple[MountedMod, ...] = ()
    enabled_count = 0
    inventory_dlc_count = 0
    warnings: tuple[str, ...]
    if manifest is None:
        warnings = ("captured debug.log is absent",)
        status = "absent"
    else:
        path = (
            Path(evidence_root)
            / "sessions"
            / session["evidence_bundle_hash"]
            / manifest["rel_path"]
        )
        if not path.is_file():
            raise RuntimeContextError(f"captured debug.log is missing: {path}")
        if path.stat().st_size != int(manifest["bytes"]):
            raise RuntimeContextError("captured debug.log byte length disagrees with manifest")
        digest = hashlib.sha256()

        def decoded_lines():
            with path.open("rb") as evidence:
                for raw_line in evidence:
                    digest.update(raw_line)
                    try:
                        yield raw_line.decode("utf-8")
                    except UnicodeDecodeError as exc:
                        raise RuntimeContextError(
                            "captured debug.log is not valid UTF-8"
                        ) from exc

        dlcs, mods, enabled_count, inventory_dlc_count, warnings = (
            parse_debug_context(decoded_lines())
        )
        if digest.hexdigest() != manifest["sha256"]:
            raise RuntimeContextError("captured debug.log SHA-256 disagrees with manifest")
        status = "absent" if not dlcs and not mods else ("partial" if warnings else "complete")

    repository.replace_runtime_context(
        conn,
        session_id=session_id,
        contract_version=CONTEXT_CONTRACT_VERSION,
        parsed_at=datetime.now(timezone.utc).isoformat(),
        status=status,
        debug_log_sha256=expected_sha,
        mounted_entry_count=len(dlcs) + len(mods),
        dlcs=dlcs,
        mods=mods,
        unknown_mount_count=sum(item.source_kind == "unknown" for item in mods),
        inventory_enabled_mod_count=enabled_count,
        inventory_dlc_count=inventory_dlc_count,
        warnings=warnings,
    )
    return _result_from_store(conn, session_id, mutated=True)
