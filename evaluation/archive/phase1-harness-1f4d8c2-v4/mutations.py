"""Byte-exact public-input mutations.

All functions operate only on disposable case scratch copies.  Descriptors are
neutral provenance records; they contain no expected candidate output.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _edit_descriptor(
    *,
    mutation_id: str,
    relative_path: str,
    base: bytes,
    derived: bytes,
    edits: list[dict[str, Any]],
    application_count: int,
    invariants: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if application_count < 1:
        raise ValueError(f"{mutation_id}: mutation application count is zero")
    return {
        "schema": "ck3chronicle.phase1-mutation-descriptor",
        "schema_version": 1,
        "mutation_id": mutation_id,
        "relative_path": relative_path.replace("\\", "/"),
        "base_bytes": len(base),
        "base_sha256": sha256_bytes(base),
        "derived_bytes": len(derived),
        "derived_sha256": sha256_bytes(derived),
        "application_count": application_count,
        "edits": edits,
        "protected_invariants": invariants or {},
    }


def _single_replace(
    path: Path,
    mutation_id: str,
    needle: bytes,
    replacement: bytes,
    *,
    occurrence: int = 0,
    relative_path: str | None = None,
) -> dict[str, Any]:
    base = path.read_bytes()
    offsets = [match.start() for match in re.finditer(re.escape(needle), base)]
    if len(offsets) <= occurrence:
        raise ValueError(f"{mutation_id}: required authentic span is absent")
    start = offsets[occurrence]
    end = start + len(needle)
    derived = base[:start] + replacement + base[end:]
    path.write_bytes(derived)
    edit = {
        "base_start": start,
        "base_end": end,
        "derived_start": start,
        "derived_end": start + len(replacement),
        "before_hex": needle.hex(),
        "after_hex": replacement.hex(),
    }
    return _edit_descriptor(
        mutation_id=mutation_id,
        relative_path=relative_path or path.name,
        base=base,
        derived=derived,
        edits=[edit],
        application_count=1,
        invariants={
            "prefix_sha256": sha256_bytes(base[:start]),
            "suffix_sha256": sha256_bytes(base[end:]),
            "prefix_equal": derived[:start] == base[:start],
            "suffix_equal": derived[start + len(replacement) :] == base[end:],
        },
    )


def _line_spans(data: bytes) -> list[tuple[int, int, bytes]]:
    spans: list[tuple[int, int, bytes]] = []
    start = 0
    for line in data.splitlines(keepends=True):
        end = start + len(line)
        spans.append((start, end, line))
        start = end
    if start < len(data):
        spans.append((start, len(data), data[start:]))
    return spans


def _mounted_line_spans(data: bytes) -> list[tuple[int, int, bytes]]:
    return [item for item in _line_spans(data) if b"]: Mounted Data: " in item[2]]


def _replace_all_newlines(path: Path, mutation_id: str) -> dict[str, Any]:
    base = path.read_bytes()
    positions = [match.start() for match in re.finditer(b"\r\n", base)]
    if not positions:
        raise ValueError(f"{mutation_id}: assigned base contains no CRLF")
    derived = base.replace(b"\r\n", b"\n")
    edits = [
        {
            "base_start": offset,
            "base_end": offset + 2,
            "before_hex": "0d0a",
            "after_hex": "0a",
        }
        for offset in positions
    ]
    path.write_bytes(derived)
    return _edit_descriptor(
        mutation_id=mutation_id,
        relative_path=path.name,
        base=base,
        derived=derived,
        edits=edits,
        application_count=len(positions),
        invariants={
            "decoded_line_payload_sha256": sha256_bytes(base.replace(b"\r\n", b"\n")),
            "derived_equals_decoded_line_payload": derived == base.replace(b"\r\n", b"\n"),
            "changed_offset_count": len(positions),
        },
    )


def _swap_mount_order(path: Path, mutation_id: str) -> dict[str, Any]:
    base = path.read_bytes()
    mounts = _mounted_line_spans(base)
    workshop = [item for item in mounts if b"/workshop/content/1158310/" in item[2]]
    if len(workshop) < 2:
        raise ValueError(f"{mutation_id}: fewer than two authentic Workshop mounts")
    first, second = workshop[0], workshop[1]
    if first[1] != second[0]:
        raise ValueError(f"{mutation_id}: selected mount rows are not adjacent")
    derived = base[: first[0]] + second[2] + first[2] + base[second[1] :]
    path.write_bytes(derived)
    return _edit_descriptor(
        mutation_id=mutation_id,
        relative_path=path.name,
        base=base,
        derived=derived,
        edits=[
            {
                "operation": "swap_adjacent_complete_lines",
                "first_base_start": first[0],
                "first_base_end": first[1],
                "second_base_start": second[0],
                "second_base_end": second[1],
                "first_sha256": sha256_bytes(first[2]),
                "second_sha256": sha256_bytes(second[2]),
            }
        ],
        application_count=1,
        invariants={
            "prefix_sha256": sha256_bytes(base[: first[0]]),
            "suffix_sha256": sha256_bytes(base[second[1] :]),
            "byte_multiset_preserved": sorted(first[2] + second[2]) == sorted(second[2] + first[2]),
            "file_size_preserved": len(base) == len(derived),
        },
    )


def _runtime_absent(path: Path, mutation_id: str) -> dict[str, Any]:
    base = path.read_bytes()
    mounts = _mounted_line_spans(base)
    if not mounts:
        raise ValueError(f"{mutation_id}: Mounted Data block is absent")
    if any(left[1] != right[0] for left, right in zip(mounts, mounts[1:])):
        raise ValueError(f"{mutation_id}: Mounted Data rows are not one contiguous block")
    start, end = mounts[0][0], mounts[-1][1]
    removed = base[start:end]
    derived = base[:start] + base[end:]
    path.write_bytes(derived)
    return _edit_descriptor(
        mutation_id=mutation_id,
        relative_path=path.name,
        base=base,
        derived=derived,
        edits=[{"base_start": start, "base_end": end, "derived_start": start, "derived_end": start, "removed_sha256": sha256_bytes(removed)}],
        application_count=1,
        invariants={
            "mounted_line_count_removed": len(mounts),
            "prefix_sha256": sha256_bytes(base[:start]),
            "suffix_sha256": sha256_bytes(base[end:]),
            "derived_has_no_mounted_data": b"]: Mounted Data: " not in derived,
        },
    )


def _runtime_truncated(path: Path, mutation_id: str) -> dict[str, Any]:
    base = path.read_bytes()
    mounts = _mounted_line_spans(base)
    if len(mounts) < 12:
        raise ValueError(f"{mutation_id}: insufficient authentic mount rows")
    cut = mounts[10][0] + max(1, len(mounts[10][2]) // 2)
    derived = base[:cut]
    removed = base[cut:]
    path.write_bytes(derived)
    return _edit_descriptor(
        mutation_id=mutation_id,
        relative_path=path.name,
        base=base,
        derived=derived,
        edits=[{"base_start": cut, "base_end": len(base), "derived_start": cut, "derived_end": cut, "removed_sha256": sha256_bytes(removed)}],
        application_count=1,
        invariants={"protected_prefix_sha256": sha256_bytes(base[:cut]), "derived_is_exact_prefix": derived == base[:cut]},
    )


def _runtime_ambiguous(path: Path, mutation_id: str) -> dict[str, Any]:
    base = path.read_bytes()
    mounts = _mounted_line_spans(base)
    if not mounts or any(left[1] != right[0] for left, right in zip(mounts, mounts[1:])):
        raise ValueError(f"{mutation_id}: no single authentic mount block")
    block = base[mounts[0][0] : mounts[-1][1]]
    insert_at = mounts[-1][1]
    derived = base[:insert_at] + block + base[insert_at:]
    path.write_bytes(derived)
    return _edit_descriptor(
        mutation_id=mutation_id,
        relative_path=path.name,
        base=base,
        derived=derived,
        edits=[{"base_start": insert_at, "base_end": insert_at, "derived_start": insert_at, "derived_end": insert_at + len(block), "inserted_sha256": sha256_bytes(block)}],
        application_count=1,
        invariants={"inserted_block_is_exact_authentic_copy": derived[insert_at : insert_at + len(block)] == block, "noninserted_bytes_equal": derived[:insert_at] + derived[insert_at + len(block) :] == base},
    )


def _robustness_encoding(path: Path, mutation_id: str) -> dict[str, Any]:
    base = path.read_bytes()
    if base.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{mutation_id}: base unexpectedly begins with BOM")
    derived = b"\xef\xbb\xbf" + base
    path.write_bytes(derived)
    # The later-position guard is a separately hashed sibling derived from the
    # same assigned base, never a substitute scoring input.
    lines = _line_spans(base)
    if len(lines) < 2:
        raise ValueError(f"{mutation_id}: no later header for BOM guard")
    guard_at = lines[1][0]
    guard = base[:guard_at] + b"\xef\xbb\xbf" + base[guard_at:]
    guard_path = path.with_name("error.later-bom.log")
    guard_path.write_bytes(guard)
    descriptor = _edit_descriptor(
        mutation_id=mutation_id,
        relative_path=path.name,
        base=base,
        derived=derived,
        edits=[{"base_start": 0, "base_end": 0, "derived_start": 0, "derived_end": 3, "after_hex": "efbbbf"}],
        application_count=1,
        invariants={"all_base_bytes_preserved_after_bom": derived[3:] == base},
    )
    descriptor["companion_variants"] = [{
        "role": "later_position_guard",
        "relative_path": guard_path.name,
        "base_sha256": sha256_bytes(base),
        "derived_sha256": sha256_bytes(guard),
        "base_bytes": len(base),
        "derived_bytes": len(guard),
        "application_count": 1,
        "edit": {"base_start": guard_at, "base_end": guard_at, "derived_start": guard_at, "derived_end": guard_at + 3, "after_hex": "efbbbf"},
        "noninserted_bytes_equal": guard[:guard_at] + guard[guard_at + 3 :] == base,
    }]
    return descriptor


def _long_line(path: Path, mutation_id: str) -> dict[str, Any]:
    base = path.read_bytes()
    lines = _line_spans(base)
    if not lines:
        raise ValueError(f"{mutation_id}: no authentic line")
    line = lines[0]
    ending = b"\r\n" if line[2].endswith(b"\r\n") else b"\n" if line[2].endswith(b"\n") else b""
    insert_at = line[1] - len(ending)
    insertion = b" X" * (512 * 1024)
    derived = base[:insert_at] + insertion + base[insert_at:]
    path.write_bytes(derived)
    return _edit_descriptor(
        mutation_id=mutation_id,
        relative_path=path.name,
        base=base,
        derived=derived,
        edits=[{"base_start": insert_at, "base_end": insert_at, "derived_start": insert_at, "derived_end": insert_at + len(insertion), "inserted_sha256": sha256_bytes(insertion)}],
        application_count=1,
        invariants={"inserted_bytes": len(insertion), "noninserted_bytes_equal": derived[:insert_at] + derived[insert_at + len(insertion) :] == base},
    )


def _truncate_tail(path: Path, mutation_id: str, *, amount: int = 4096) -> dict[str, Any]:
    base = path.read_bytes()
    if len(base) <= amount:
        raise ValueError(f"{mutation_id}: authentic file is too small")
    cut = len(base) - amount
    derived = base[:cut]
    path.write_bytes(derived)
    return _edit_descriptor(
        mutation_id=mutation_id,
        relative_path=path.name,
        base=base,
        derived=derived,
        edits=[{"base_start": cut, "base_end": len(base), "derived_start": cut, "derived_end": cut, "removed_sha256": sha256_bytes(base[cut:])}],
        application_count=1,
        invariants={"derived_is_exact_prefix": derived == base[:cut], "protected_prefix_sha256": sha256_bytes(base[:cut])},
    )


def apply_mutation(mutation_id: str, logs_root: Path) -> dict[str, Any]:
    """Apply one named mutation to an already verified scratch copy."""
    error = logs_root / "error.log"
    debug = logs_root / "debug.log"

    if mutation_id == "remove_error_log":
        base = error.read_bytes()
        error.unlink()
        return {
            "schema": "ck3chronicle.phase1-mutation-descriptor", "schema_version": 1,
            "mutation_id": mutation_id, "relative_path": "error.log",
            "base_bytes": len(base), "base_sha256": sha256_bytes(base),
            "derived_state": "absent", "derived_sha256": None,
            "application_count": 1, "edits": [{"operation": "remove_exact_file", "base_start": 0, "base_end": len(base)}],
            "protected_invariants": {"other_staged_files_unchanged": True},
        }
    if mutation_id in {"zero_error_log", "zero-error", "missing_error"}:
        base = error.read_bytes(); error.write_bytes(b"")
        return _edit_descriptor(mutation_id=mutation_id, relative_path="error.log", base=base, derived=b"", edits=[{"base_start": 0, "base_end": len(base), "derived_start": 0, "derived_end": 0, "removed_sha256": sha256_bytes(base)}], application_count=1)
    if mutation_id in {"newline_variant", "robustness_newline"}:
        return _replace_all_newlines(error, mutation_id)
    if mutation_id in {"locator_path"}:
        return _single_replace(error, mutation_id, b"gfx/FX/court_scene.shader", b"gfy/FX/court_scene.shader", relative_path="error.log")
    if mutation_id == "absolute_locator_root":
        base = error.read_bytes()
        match = re.search(rb"(?<![A-Za-z0-9_])([A-Za-z]):([\\/])", base)
        if match is None:
            raise ValueError("absolute_locator_root: no authentic drive root")
        before = match.group(1)
        after = b"Z" if before.upper() != b"Z" else b"Y"
        start = match.start(1)
        derived = base[:start] + after + base[start + 1 :]
        error.write_bytes(derived)
        descriptor = _edit_descriptor(mutation_id=mutation_id, relative_path="error.log", base=base, derived=derived, edits=[{"base_start": start, "base_end": start + 1, "derived_start": start, "derived_end": start + 1, "before_hex": before.hex(), "after_hex": after.hex()}], application_count=1, invariants={"root_separator_preserved": derived[start + 1 : start + 3] == base[start + 1 : start + 3], "all_nonroot_bytes_equal": derived[:start] + derived[start + 1 :] == base[:start] + base[start + 1 :], "uri_scheme_excluded": base[start : start + 7].lower() != b"event:/"})
        descriptor["selected_span"] = {"base_start": start, "base_end": start + 3, "before_ascii": base[start : start + 3].decode("ascii"), "after_ascii": derived[start : start + 3].decode("ascii")}
        return descriptor
    if mutation_id == "semantic_literal":
        return _single_replace(error, mutation_id, b"Failed to create material", b"Failed to create materiax", relative_path="error.log")
    if mutation_id in {"truncated_tail", "robustness_truncation"}:
        return _truncate_tail(error, mutation_id)
    if mutation_id in {"swap_mount_order", "runtime_swap_order"}:
        return _swap_mount_order(debug, mutation_id)
    if mutation_id in {"runtime_absent", "runtime_state_absent"}:
        return _runtime_absent(debug, mutation_id)
    if mutation_id in {"runtime_malformed", "runtime_state_malformed"}:
        base = debug.read_bytes(); mounts = _mounted_line_spans(base)
        if not mounts: raise ValueError(f"{mutation_id}: no Mounted Data row")
        line = mounts[0]; local = line[2].find(b"C:/")
        if local < 0: raise ValueError(f"{mutation_id}: no authentic drive root in first mount")
        absolute = line[0] + local + 1
        return _single_replace(debug, mutation_id, b":/", b"?/", occurrence=sum(1 for m in re.finditer(re.escape(b":/"), base[:absolute])) , relative_path="debug.log")
    if mutation_id == "runtime_state_truncated":
        return _runtime_truncated(debug, mutation_id)
    if mutation_id == "runtime_state_ambiguous":
        return _runtime_ambiguous(debug, mutation_id)
    if mutation_id in {"inventory_metadata", "runtime_inventory_metadata"}:
        return _single_replace(debug, mutation_id, b"CFP + EPE Compatibility Patch", b"CFP + EPE Compatibility Patcx", relative_path="debug.log")
    if mutation_id == "robustness_encoding":
        return _robustness_encoding(error, mutation_id)
    if mutation_id == "robustness_long_line":
        return _long_line(error, mutation_id)
    if mutation_id == "robustness_malformed":
        return _single_replace(error, mutation_id, b"][E][", b"][?][", relative_path="error.log")
    if mutation_id == "robustness_replacement_character":
        return _single_replace(error, mutation_id, b"Failed", "Fail\ufffdd".encode("utf-8"), relative_path="error.log")
    raise KeyError(f"unknown mutation: {mutation_id}")
