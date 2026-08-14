"""Same-run DLC and active-mod context from archived ``debug.log`` evidence."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from typing import Any, Iterable

from .db import repository


CONTEXT_CONTRACT_VERSION = "2.0.0"


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
    source_session_file_id: int | None
    block_start_line: int | None
    block_end_line: int | None
    block_start_byte: int | None
    block_end_byte: int | None
    block_sha256: str | None
    block_candidate_count: int
    valid_mount_count: int
    malformed_mount_count: int
    termination_evidence: str | None
    absence_reason: str | None
    dlcs: tuple[MountedDlc, ...]
    mods: tuple[MountedMod, ...]
    unknown_mount_count: int
    inventory_enabled_mod_count: int
    inventory_dlc_count: int
    warnings: tuple[str, ...]
    inventory_warnings: tuple[str, ...]
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


def _local_key(value: str) -> str:
    folded = "".join(character for character in value.casefold() if character.isalnum())
    return "local:" + (folded or hashlib.sha256(value.encode("utf-8")).hexdigest()[:16])


def _mod_descriptor_key(path: str) -> tuple[str, str] | None:
    normalized = _normalized_path(path)
    workshop = _WORKSHOP_DESCRIPTOR.search(normalized)
    if workshop:
        return "workshop", workshop.group("key")
    local = _LOCAL_DESCRIPTOR.search(normalized)
    if local:
        return "local", _local_key(local.group("name"))
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


@dataclass
class _BlockCandidate:
    start_line: int
    start_byte: int
    end_line: int
    end_byte: int
    paths: list[str] = field(default_factory=list)
    malformed_count: int = 0
    terminated: bool = False
    termination_evidence: str = "end_of_file"
    digest: Any = field(default_factory=hashlib.sha256)

    def add(
        self,
        *,
        line_number: int,
        end_byte: int,
        raw: bytes,
        path: str | None,
    ) -> None:
        self.end_line = line_number
        self.end_byte = end_byte
        self.digest.update(raw)
        if path:
            self.paths.append(path)
        else:
            self.malformed_count += 1

    @property
    def sha256(self) -> str:
        return self.digest.hexdigest()


@dataclass(frozen=True)
class _ContextAnalysis:
    status: str
    dlcs: tuple[MountedDlc, ...]
    mods: tuple[MountedMod, ...]
    inventory_enabled_mod_count: int
    inventory_dlc_count: int
    warnings: tuple[str, ...]
    inventory_warnings: tuple[str, ...]
    block_start_line: int | None
    block_end_line: int | None
    block_start_byte: int | None
    block_end_byte: int | None
    block_sha256: str | None
    block_candidate_count: int
    valid_mount_count: int
    malformed_mount_count: int
    termination_evidence: str | None
    absence_reason: str | None


def _typed_mounts(
    paths: Iterable[str],
    dlc_inventory: dict[str, tuple[str, str]],
    enabled_mod_inventory: dict[str, tuple[str, str, str]],
) -> tuple[tuple[MountedDlc, ...], tuple[MountedMod, ...], int]:
    dlcs: list[MountedDlc] = []
    mods: list[MountedMod] = []
    dlc_order = 0
    mod_order = 0
    unknown_mount_count = 0
    for mount_ordinal, path in enumerate(paths):
        dlc_match = _DLC_PATH.search(path)
        workshop_match = _WORKSHOP_PATH.search(path)
        if dlc_match:
            key = dlc_match.group("key").casefold()
            inventory = dlc_inventory.get(key)
            dlcs.append(
                MountedDlc(
                    mount_ordinal,
                    dlc_order,
                    key,
                    inventory[0] if inventory else None,
                    inventory[1] if inventory else None,
                    path,
                )
            )
            dlc_order += 1
        elif workshop_match:
            key = workshop_match.group("key")
            inventory = enabled_mod_inventory.get(key)
            mods.append(
                MountedMod(
                    mount_ordinal,
                    mod_order,
                    key,
                    inventory[0] if inventory else None,
                    inventory[1] if inventory else None,
                    path,
                    "workshop",
                )
            )
            mod_order += 1
        else:
            leaf = path.rsplit("/", 1)[-1]
            key = _local_key(leaf)
            inventory = enabled_mod_inventory.get(key)
            source_kind = (
                "local"
                if inventory is not None or "/mod/" in path.casefold()
                else "unknown"
            )
            if source_kind == "unknown":
                unknown_mount_count += 1
                key = _unknown_key(path)
            mods.append(
                MountedMod(
                    mount_ordinal,
                    mod_order,
                    key,
                    inventory[0] if inventory else None,
                    inventory[1] if inventory else None,
                    path,
                    source_kind,
                )
            )
            mod_order += 1
    return tuple(dlcs), tuple(mods), unknown_mount_count


def _analyze_debug_context(
    records: Iterable[tuple[int, int, int, bytes, str]],
) -> _ContextAnalysis:
    mode: str | None = None
    dlc_inventory: dict[str, tuple[str, str]] = {}
    enabled_mod_inventory: dict[str, tuple[str, str, str]] = {}
    inventory_dlc_keys: list[str] = []
    inventory_enabled_mod_keys: list[str] = []
    warnings: list[str] = []
    inventory_warnings: list[str] = []
    blocks: list[_BlockCandidate] = []
    current: _BlockCandidate | None = None

    for line_number, start_byte, end_byte, raw, text in records:
        line = text.rstrip("\r\n")
        mount = _MOUNTED_DATA.match(line)
        marker_like = mount is not None or (
            "mounted data" in line.casefold()
            and "virtualfilesystem" in line.casefold()
        )
        if marker_like:
            mode = None
            if current is None:
                current = _BlockCandidate(
                    start_line=line_number,
                    start_byte=start_byte,
                    end_line=line_number,
                    end_byte=end_byte,
                )
            path = _normalized_path(mount.group("path")) if mount else None
            current.add(
                line_number=line_number,
                end_byte=end_byte,
                raw=raw,
                path=path or None,
            )
            continue
        if current is not None:
            current.terminated = True
            current.termination_evidence = "next_non_mount_line"
            blocks.append(current)
            current = None
        if blocks:
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
                inventory_warnings.append("malformed DLC inventory entry")
                continue
            display_name, descriptor_path = (item.strip() for item in parts)
            key = _dlc_descriptor_key(descriptor_path)
            if key is None:
                inventory_warnings.append(
                    f"unrecognized DLC descriptor: {descriptor_path}"
                )
                continue
            dlc_inventory[key] = (display_name, descriptor_path)
            inventory_dlc_keys.append(key)
        elif mode == "mod":
            parts = line.rsplit("|", 2)
            if len(parts) != 3:
                inventory_warnings.append("malformed mod inventory entry")
                continue
            display_name, descriptor_path, state = (item.strip() for item in parts)
            if state.casefold() != "enabled":
                continue
            identity = _mod_descriptor_key(descriptor_path)
            if identity is None:
                inventory_warnings.append(
                    f"unrecognized enabled mod descriptor: {descriptor_path}"
                )
                continue
            source_kind, key = identity
            enabled_mod_inventory[key] = (display_name, descriptor_path, source_kind)
            inventory_enabled_mod_keys.append(key)

    if current is not None:
        blocks.append(current)

    selected = blocks[0] if len(blocks) == 1 else None
    dlcs: tuple[MountedDlc, ...] = ()
    mods: tuple[MountedMod, ...] = ()
    unknown_mount_count = 0
    if selected is None:
        if not blocks:
            status = "absent"
            warnings.append("Mounted Data block not found")
            absence_reason = "mounted_data_not_found"
        else:
            status = "ambiguous"
            warnings.append(f"multiple Mounted Data blocks found: {len(blocks)}")
            absence_reason = None
    else:
        absence_reason = None
        if not selected.paths:
            status = "malformed"
            warnings.append("Mounted Data block contains no valid mount paths")
        elif not selected.terminated:
            status = "truncated"
            warnings.append("Mounted Data block reaches end of debug.log")
        elif selected.malformed_count:
            status = "partial"
            warnings.append(
                f"Mounted Data block contains {selected.malformed_count} malformed entries"
            )
        else:
            status = "complete"
        dlcs, mods, unknown_mount_count = _typed_mounts(
            selected.paths, dlc_inventory, enabled_mod_inventory
        )

    mounted_dlc = Counter(item.dlc_key for item in dlcs)
    inventory_dlc = Counter(inventory_dlc_keys)
    mounted_mod = Counter(item.mod_key for item in mods if item.source_kind != "unknown")
    inventory_mod = Counter(inventory_enabled_mod_keys)
    if selected is not None and mounted_dlc != inventory_dlc:
        inventory_warnings.append(
            "mounted DLC set differs from DLC inventory: mounted_only="
            f"{_bounded_difference(mounted_dlc, inventory_dlc)}, inventory_only="
            f"{_bounded_difference(inventory_dlc, mounted_dlc)}"
        )
    if selected is not None and mounted_mod != inventory_mod:
        inventory_warnings.append(
            "mounted mod set differs from Enabled inventory: mounted_only="
            f"{_bounded_difference(mounted_mod, inventory_mod)}, enabled_only="
            f"{_bounded_difference(inventory_mod, mounted_mod)}"
        )
    if unknown_mount_count:
        warnings.append(f"{unknown_mount_count} mounted roots could not be typed")

    return _ContextAnalysis(
        status=status,
        dlcs=dlcs,
        mods=mods,
        inventory_enabled_mod_count=len(inventory_enabled_mod_keys),
        inventory_dlc_count=len(inventory_dlc_keys),
        warnings=tuple(dict.fromkeys(warnings)),
        inventory_warnings=tuple(dict.fromkeys(inventory_warnings)),
        block_start_line=selected.start_line if selected else None,
        block_end_line=selected.end_line if selected else None,
        block_start_byte=selected.start_byte if selected else None,
        block_end_byte=selected.end_byte if selected else None,
        block_sha256=selected.sha256 if selected else None,
        block_candidate_count=len(blocks),
        valid_mount_count=(
            len(selected.paths)
            if selected
            else sum(len(block.paths) for block in blocks)
        ),
        malformed_mount_count=(
            selected.malformed_count
            if selected
            else sum(block.malformed_count for block in blocks)
        ),
        termination_evidence=(
            selected.termination_evidence
            if selected
            else "multiple_blocks"
            if blocks
            else None
        ),
        absence_reason=absence_reason,
    )


def parse_debug_context(lines: Iterable[str]) -> tuple[
    tuple[MountedDlc, ...],
    tuple[MountedMod, ...],
    int,
    int,
    tuple[str, ...],
]:
    """Compatibility projection over the exact streaming analyzer."""
    offset = 0

    def records():
        nonlocal offset
        for line_number, text in enumerate(lines, 1):
            raw = text.encode("utf-8")
            start = offset
            offset += len(raw)
            yield line_number, start, offset, raw, text

    analysis = _analyze_debug_context(records())
    return (
        analysis.dlcs,
        analysis.mods,
        analysis.inventory_enabled_mod_count,
        analysis.inventory_dlc_count,
        tuple(dict.fromkeys(analysis.warnings + analysis.inventory_warnings)),
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
        source_session_file_id=context["source_session_file_id"],
        block_start_line=context["block_start_line"],
        block_end_line=context["block_end_line"],
        block_start_byte=context["block_start_byte"],
        block_end_byte=context["block_end_byte"],
        block_sha256=context["block_sha256"],
        block_candidate_count=int(context["block_candidate_count"]),
        valid_mount_count=int(context["valid_mount_count"]),
        malformed_mount_count=int(context["malformed_mount_count"]),
        termination_evidence=context["termination_evidence"],
        absence_reason=context["absence_reason"],
        dlcs=dlcs,
        mods=mods,
        unknown_mount_count=int(context["unknown_mount_count"]),
        inventory_enabled_mod_count=int(context["inventory_enabled_mod_count"]),
        inventory_dlc_count=int(context["inventory_dlc_count"]),
        warnings=tuple(json.loads(context["warnings_json"])),
        inventory_warnings=tuple(
            json.loads(context["inventory_warnings_json"])
        ),
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
    inventory_warnings: tuple[str, ...] = ()
    source_session_file_id = None
    block_start_line = None
    block_end_line = None
    block_start_byte = None
    block_end_byte = None
    block_sha256 = None
    block_candidate_count = 0
    valid_mount_count = 0
    malformed_mount_count = 0
    termination_evidence = None
    absence_reason = None
    if manifest is None:
        warnings = ("captured debug.log is absent",)
        status = "absent"
        absence_reason = "debug_log_absent"
    else:
        source_session_file_id = int(manifest["session_file_id"])
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
        offset = 0

        def decoded_records():
            nonlocal offset
            with path.open("rb") as evidence:
                for line_number, raw_line in enumerate(evidence, 1):
                    start = offset
                    offset += len(raw_line)
                    digest.update(raw_line)
                    try:
                        text = raw_line.decode("utf-8")
                    except UnicodeDecodeError as exc:
                        raise RuntimeContextError(
                            "captured debug.log is not valid UTF-8"
                        ) from exc
                    yield line_number, start, offset, raw_line, text

        analysis = _analyze_debug_context(decoded_records())
        if digest.hexdigest() != manifest["sha256"]:
            raise RuntimeContextError("captured debug.log SHA-256 disagrees with manifest")
        status = analysis.status
        dlcs = analysis.dlcs
        mods = analysis.mods
        enabled_count = analysis.inventory_enabled_mod_count
        inventory_dlc_count = analysis.inventory_dlc_count
        warnings = analysis.warnings
        inventory_warnings = analysis.inventory_warnings
        block_start_line = analysis.block_start_line
        block_end_line = analysis.block_end_line
        block_start_byte = analysis.block_start_byte
        block_end_byte = analysis.block_end_byte
        block_sha256 = analysis.block_sha256
        block_candidate_count = analysis.block_candidate_count
        valid_mount_count = analysis.valid_mount_count
        malformed_mount_count = analysis.malformed_mount_count
        termination_evidence = analysis.termination_evidence
        absence_reason = analysis.absence_reason

    repository.replace_runtime_context(
        conn,
        session_id=session_id,
        contract_version=CONTEXT_CONTRACT_VERSION,
        parsed_at=datetime.now(timezone.utc).isoformat(),
        status=status,
        debug_log_sha256=expected_sha,
        source_session_file_id=source_session_file_id,
        block_start_line=block_start_line,
        block_end_line=block_end_line,
        block_start_byte=block_start_byte,
        block_end_byte=block_end_byte,
        block_sha256=block_sha256,
        block_candidate_count=block_candidate_count,
        valid_mount_count=valid_mount_count,
        malformed_mount_count=malformed_mount_count,
        termination_evidence=termination_evidence,
        absence_reason=absence_reason,
        mounted_entry_count=len(dlcs) + len(mods),
        dlcs=dlcs,
        mods=mods,
        unknown_mount_count=sum(item.source_kind == "unknown" for item in mods),
        inventory_enabled_mod_count=enabled_count,
        inventory_dlc_count=inventory_dlc_count,
        warnings=warnings,
        inventory_warnings=inventory_warnings,
    )
    return _result_from_store(conn, session_id, mutated=True)
