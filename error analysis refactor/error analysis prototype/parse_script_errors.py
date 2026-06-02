"""
parse_script_errors.py

Reads the full CK3 error.log, extracts ALL multi-line script system error
blocks, clusters them by common cause, and writes a compact indexed report
to WIP at root:ck3raven_data/wip/script_error_report.txt

root:user_docs resolves to the CK3 user documents root (the folder that
contains logs/, mod/, etc.)
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Bootstrap SDK (no host paths)
# ---------------------------------------------------------------------------
_sdk_dir = Path.home() / ".ck3raven" / "wip" / "sdk"
sys.path.insert(0, str(_sdk_dir))
import ck3_sdk as _sdk_mod
sdk = _sdk_mod.CK3SDK()

# ---------------------------------------------------------------------------
# Resolve paths via SDK (canonical only — no hardcoded host paths)
# ---------------------------------------------------------------------------
ck3_root  = sdk.resolve("root:user_docs")          # CK3 documents folder
out_path  = sdk.wip / "script_error_report.txt"
out_canon = "root:ck3raven_data/wip/script_error_report.txt"

# Optional --log argument: path to a specific log file (e.g. a crash folder's error.log)
# Defaults to the standard error.log in root:user_docs/logs/
_parser = argparse.ArgumentParser()
_parser.add_argument("--log", default=None, help="Path to log file (default: CK3 error.log)")
_args = _parser.parse_args()

_override_file = sdk.wip / ".log_path_override"

if _args.log:
    log_path  = Path(_args.log)
    log_canon = str(log_path)
elif _override_file.exists():
    log_path  = Path(_override_file.read_text(encoding="utf-8").strip())
    log_canon = str(log_path)
    _override_file.unlink()   # consume once — auto-deletes after use
else:
    log_path  = ck3_root / "logs" / "error.log"
    log_canon = "root:user_docs/logs/error.log"

if not log_path.exists():
    print(f"ERROR: log not found: {log_canon}")
    sys.exit(1)

print(f"Reading {log_canon} ...")

# ---------------------------------------------------------------------------
# Parse log — split into timestamped blocks, collect script system errors
# ---------------------------------------------------------------------------
LINE_START  = re.compile(r"^\[\d{2}:\d{2}:\d{2}\]")
SCRIPT_ERR  = re.compile(r"Script system error!", re.IGNORECASE)

lines = log_path.read_bytes().decode("utf-8", errors="replace").splitlines()

blocks: list[str] = []
current: list[str] = []
for line in lines:
    if LINE_START.match(line):
        if current:
            blocks.append("\n".join(current))
        current = [line]
    else:
        if current:
            current.append(line)
if current:
    blocks.append("\n".join(current))

error_blocks = [b for b in blocks if SCRIPT_ERR.search(b)]
print(f"Total log blocks: {len(blocks):,}  |  Script system errors: {len(error_blocks):,}")

# QC: block line-count distribution — single-line blocks are incomplete captures
_sizes = defaultdict(int)
for b in error_blocks:
    _sizes[len(b.splitlines())] += 1
print("Block line-count QC:")
for s in sorted(_sizes):
    flag = "  *** INCOMPLETE (no continuation lines)" if s == 1 else ""
    print(f"  {s} lines: {_sizes[s]:,} blocks{flag}")

# ---------------------------------------------------------------------------
# Extract fields from each block
# ---------------------------------------------------------------------------
RE_FILE   = re.compile(r'Script location: file:\s+(\S+)',   re.IGNORECASE)
RE_LINE   = re.compile(r'line:\s*(\d+)',                    re.IGNORECASE)
RE_COL    = re.compile(r'column:\s*(\d+)',                  re.IGNORECASE)
RE_OBJECT = re.compile(r'\(([^)]+)\)\s*$',                  re.IGNORECASE | re.MULTILINE)
RE_MSG    = re.compile(r'^\s+Error:\s*(.+)',                 re.IGNORECASE | re.MULTILINE)

def extract(block: str) -> dict:
    fm = RE_FILE.search(block)
    lm = RE_LINE.search(block)
    cm = RE_COL.search(block)
    om = RE_OBJECT.search(block)
    mm = RE_MSG.search(block)
    return {
        "file":    fm.group(1) if fm else None,
        "line":    int(lm.group(1)) if lm else None,
        "col":     int(cm.group(1)) if cm else None,
        "object":  om.group(1).strip() if om else None,
        "message": mm.group(1).strip() if mm else block.splitlines()[0][:300].strip(),
        "raw":     block,
    }

parsed = [extract(b) for b in error_blocks]

# ---------------------------------------------------------------------------
# Cluster classification
# ---------------------------------------------------------------------------
CLUSTERS: list[tuple[str, re.Pattern]] = [
    # High-volume scope/context errors (CK3 1.18 actual patterns)
    ("failed_context_switch",  re.compile(r"Failed context switch", re.I)),
    ("wrong_scope",            re.compile(r"Wrong scope for (?:trigger|effect|modifier)", re.I)),
    ("scope_type_mismatch",    re.compile(r"did not get a matching scope type|expected .{0,60} but got", re.I)),
    ("null_scope_object",      re.compile(r"Scoped object.{0,60}is not valid|\bwas null\b|character was null", re.I)),
    ("unset_scope",            re.compile(r"returned an unset scope|Failed to fetch (?:key|variable) for", re.I)),
    ("null_fetch",             re.compile(r"Fetched null|returned null", re.I)),
    ("invalid_comparison",     re.compile(r"Invalid (?:left|right) side during comparison", re.I)),
    # Variable errors
    ("variable_scope_error",   re.compile(r"Variable not of the .value. scope type|This scope doesn.t support variables|does not have variables", re.I)),
    # Character state errors
    ("no_capital",             re.compile(r"has no capital|Character with no location", re.I)),
    ("invalid_legitimacy",     re.compile(r"doesn.t have valid legitimacy type", re.I)),
    # Asset/visual errors
    ("asset_visual_error",     re.compile(r"Couldn.t determine .asset. visual type", re.I)),
    # Content errors
    ("unknown_loc_key",        re.compile(r"Unknown loc key", re.I)),
    ("postvalidate_false",     re.compile(r"PostValidate.{0,60}returned false|postvalidate", re.I)),
    # Script structure errors
    ("else_not_after_if",      re.compile(r"else.{0,20}not.{0,20}if|else_if.{0,5}not", re.I)),
    ("more_than_one_effect",   re.compile(r"more than one.{0,20}effect|multiple effect", re.I)),
    ("unknown_effect",         re.compile(r"unknown effect", re.I)),
    ("unknown_trigger",        re.compile(r"unknown trigger", re.I)),
    ("unknown_modifier",       re.compile(r"unknown modifier", re.I)),
    ("unknown_value",          re.compile(r"unknown value|invalid value", re.I)),
    ("unknown_token",          re.compile(r"unexpected token|unexpected symbol", re.I)),
    ("duplicate_definition",   re.compile(r"duplicate|already defined|redefinition", re.I)),
    ("type_mismatch",          re.compile(r"type mismatch|wrong type", re.I)),
    ("undefined_symbol",       re.compile(r"undefined|not defined|could not find", re.I)),
    ("out_of_range",           re.compile(r"out of range", re.I)),
]

def classify(msg: str) -> str:
    for label, pat in CLUSTERS:
        if pat.search(msg):
            return label
    return "other"

def short_relpath(p: str | None) -> str:
    """Strip mod root prefix, return game-relative path only."""
    if not p:
        return "unknown"
    p = p.replace("\\", "/")
    for marker in ("common/", "events/", "decisions/", "history/",
                   "localization/", "gfx/", "gui/", "map_data/",
                   "on_action/", "scripted_effects/", "scripted_triggers/",
                   "cultures/", "religions/", "characters/", "dynasties/"):
        idx = p.find(marker)
        if idx != -1:
            return p[idx:]
    parts = [x for x in p.split("/") if x]
    return "/".join(parts[-2:]) if len(parts) >= 2 else p

def to_canonical_path(p: str | None) -> str:
    """Best-effort canonical form for display."""
    if not p:
        return "unknown"
    canonical = sdk.to_canonical(p)
    return canonical if canonical else short_relpath(p)

# Build: cluster → { relpath → [entries] }
clusters: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
for entry in parsed:
    label = classify(entry["message"])
    fp    = short_relpath(entry["file"])
    clusters[label][fp].append(entry)

# Normalise messages for deduplication (strip timestamps, line/col numbers)
def norm_msg(msg: str) -> str:
    msg = re.sub(r"\[\d{4}\.\d{2}\.\d{2}[^\]]*\]", "", msg)
    msg = re.sub(r"\bline \d+\b", "line N", msg)
    msg = re.sub(r"\bcolumn \d+\b", "col N", msg)
    msg = re.sub(r'"[A-Za-z0-9_/\\:.]{50,}"', '"..."', msg)
    return msg.strip()

# ---------------------------------------------------------------------------
# Build report
# ---------------------------------------------------------------------------
lines_out: list[str] = []
W = lines_out.append

def rule(char="─", width=78):
    W(char * width)

now        = datetime.now().strftime("%Y-%m-%d %H:%M")
total_errs = len(parsed)
cluster_order = sorted(clusters.items(), key=lambda x: -sum(len(v) for v in x[1].values()))

W("=" * 78)
W("CK3 SCRIPT SYSTEM ERROR REPORT")
W(f"Generated : {now}")
W(f"Playset   : {sdk.playset_name}")
W(f"Log source: {log_canon}")
W(f"Log blocks: {len(blocks):,}  |  Script errors: {total_errs:,}  |  Clusters: {len(cluster_order)}")
W("=" * 78)
W("")

# ── TABLE OF CONTENTS ──────────────────────────────────────────────────────
W("TABLE OF CONTENTS")
rule()
for i, (label, files) in enumerate(cluster_order, 1):
    count = sum(len(v) for v in files.values())
    W(f"  {i:>2}. [{count:>5}]  {label}")
W("")

# ── MOD INDEX ──────────────────────────────────────────────────────────────
W("ACTIVE PLAYSET  (load order, lowest = loads first)")
rule()
for m in sdk.mods:
    indexed = "indexed" if m.is_indexed else "NOT indexed"
    W(f"  [{m.load_order:>3}] {m.name}  ({indexed})")
W("")

# ── CLUSTER DETAIL SECTIONS ────────────────────────────────────────────────
for i, (label, files) in enumerate(cluster_order, 1):
    total_in_cluster = sum(len(v) for v in files.values())
    W("=" * 78)
    W(f"CLUSTER {i}: {label.upper()}  [{total_in_cluster} errors]")
    W("=" * 78)
    W("")

    # files sorted by error count descending
    for fp, entries in sorted(files.items(), key=lambda x: -len(x[1])):
        W(f"  FILE: {fp}  [{len(entries)} errors]")

        # Mod attribution
        raw_file = entries[0]["file"]
        if raw_file:
            can = sdk.to_canonical(raw_file)
            if can:
                W(f"  PATH: {can}")
            # find owning mod
            for m in sdk.mods:
                mod_fp = str(m.path).replace("\\", "/")
                if raw_file.replace("\\", "/").startswith(mod_fp):
                    W(f"  MOD : {m.name}  [load order {m.load_order}]")
                    break

        # Lines affected (compact)
        affected_lines = sorted(set(e["line"] for e in entries if e["line"]))
        if affected_lines:
            W(f"  LINES: {', '.join(str(l) for l in affected_lines[:30])}" +
              (f" ... (+{len(affected_lines)-30} more)" if len(affected_lines) > 30 else ""))

        # Objects affected
        objects = sorted(set(e["object"] for e in entries if e["object"]))
        if objects:
            W(f"  OBJECTS: {', '.join(objects[:10])}" +
              (f" ... (+{len(objects)-10} more)" if len(objects) > 10 else ""))

        # Deduplicated representative messages (max 5 unique)
        seen: set[str] = set()
        unique: list[str] = []
        for e in entries:
            n = norm_msg(e["message"])
            if n not in seen:
                seen.add(n)
                unique.append(e["message"])
            if len(unique) >= 5:
                break

        W(f"  EXAMPLES ({len(seen)} unique message(s)):")
        for msg in unique:
            # wrap long messages
            for chunk in [msg[j:j+120] for j in range(0, min(len(msg), 360), 120)]:
                W(f"    > {chunk}")

        W("")

# ── FOOTER ─────────────────────────────────────────────────────────────────
W("=" * 78)
W(f"END OF REPORT  |  {total_errs} script system errors  |  {len(cluster_order)} clusters")
W("=" * 78)

# ---------------------------------------------------------------------------
# Write report
# ---------------------------------------------------------------------------
report_text = "\n".join(lines_out)
out_path.write_text(report_text, encoding="utf-8")

print(f"\nReport written to: {out_canon}")
print(f"Total script errors: {total_errs:,}")
print("")
print("CLUSTER SUMMARY:")
for i, (label, files) in enumerate(cluster_order, 1):
    count = sum(len(v) for v in files.values())
    print(f"  {i:>2}. {label:<30} {count:>5} errors  {len(files)} file(s)")
