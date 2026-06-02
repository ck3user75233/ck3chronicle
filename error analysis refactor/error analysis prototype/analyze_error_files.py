"""
analyze_error_files.py

For the top N files by error count in the crash error.log:
  1. Rank files by error count across all script error blocks
  2. For each, walk the full override chain (vanilla → mods in load order)
  3. Flag instances modified within the last 10 days
  4. If our submod (Gambo+EC724 Submod) has an override:
       - Diff vs the original source (lowest load-order instance)
       - Diff vs the immediate predecessor in the chain
       - Warn if deletions >> additions (stale patch removing new content)
  5. If our submod does NOT have an override:
       - Note which mod is winning and whether it was recently updated
  6. Sample the actual error messages for each file

Reads crash log path from .log_path_override if present (consumed once),
otherwise falls back to root:user_docs/logs/error.log.

Output: root:ck3raven_data/wip/error_file_analysis.txt
"""
from __future__ import annotations

import difflib
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap SDK
# ---------------------------------------------------------------------------
_sdk_dir = Path.home() / ".ck3raven" / "wip" / "sdk"
sys.path.insert(0, str(_sdk_dir))
import ck3_sdk as _sdk_mod
sdk = _sdk_mod.CK3SDK()

# ---------------------------------------------------------------------------
# Resolve log path
# ---------------------------------------------------------------------------
ck3_root = sdk.resolve("root:user_docs")
_override = sdk.wip / ".log_path_override"

if _override.exists():
    log_path  = Path(_override.read_text(encoding="utf-8").strip())
    log_canon = str(log_path)
    _override.unlink()
else:
    log_path  = ck3_root / "logs" / "error.log"
    log_canon = "root:user_docs/logs/error.log"

if not log_path.exists():
    print(f"ERROR: log not found: {log_canon}")
    sys.exit(1)

print(f"Reading {log_canon} ...")

# ---------------------------------------------------------------------------
# Parse log — collect script system error blocks
# ---------------------------------------------------------------------------
LINE_START = re.compile(r"^\[\d{2}:\d{2}:\d{2}\]")
SCRIPT_ERR = re.compile(r"Script system error!", re.IGNORECASE)
RE_FILE    = re.compile(r"Script location: file:\s+(\S+)", re.IGNORECASE)
RE_LINE_NO = re.compile(r"line:\s*(\d+)", re.IGNORECASE)
RE_MSG     = re.compile(r"^\s+Error:\s*(.+)", re.IGNORECASE | re.MULTILINE)

raw = log_path.read_bytes().decode("utf-8", errors="replace").splitlines()
blocks: list[str] = []
cur: list[str] = []
for ln in raw:
    if LINE_START.match(ln):
        if cur:
            blocks.append("\n".join(cur))
        cur = [ln]
    else:
        if cur:
            cur.append(ln)
if cur:
    blocks.append("\n".join(cur))

error_blocks = [b for b in blocks if SCRIPT_ERR.search(b)]
print(f"Script error blocks: {len(error_blocks):,}")

# ---------------------------------------------------------------------------
# Group by game-relative file path
# ---------------------------------------------------------------------------
MARKERS = (
    "common/", "events/", "decisions/", "history/",
    "localization/", "gfx/", "gui/", "map_data/",
    "on_action/", "scripted_effects/", "scripted_triggers/",
    "cultures/", "religions/", "characters/", "dynasties/",
)

def rel_path(abs_path: str) -> str:
    p = abs_path.replace("\\", "/")
    for m in MARKERS:
        idx = p.find(m)
        if idx != -1:
            return p[idx:]
    parts = [x for x in p.split("/") if x]
    return "/".join(parts[-2:]) if len(parts) >= 2 else p

file_blocks: dict[str, list[str]] = defaultdict(list)
for block in error_blocks:
    fm = RE_FILE.search(block)
    if fm:
        file_blocks[rel_path(fm.group(1))].append(block)

TOP_N = 25
top_files = sorted(file_blocks.items(), key=lambda x: -len(x[1]))[:TOP_N]
print(f"Top {TOP_N} error files identified")

# ---------------------------------------------------------------------------
# Override chain helpers
# ---------------------------------------------------------------------------
OUR_SUBMOD   = "Gambo+EC724 Submod"
CUTOFF_DAYS  = 10
CUTOFF_DT    = datetime.now() - timedelta(days=CUTOFF_DAYS)

def find_instances(rel: str) -> list[tuple[str, int, Path, datetime]]:
    """Return list of (mod_name, load_order, path, mtime) sorted by load_order asc.
    Uses sdk.resolve() with canonical addresses for all lookups."""
    found = []
    # Vanilla game files (load_order = -1)
    try:
        gf = sdk.resolve(f"root:game/{rel}")
        if gf and Path(gf).exists():
            mtime = datetime.fromtimestamp(Path(gf).stat().st_mtime)
            found.append(("Base Game", -1, Path(gf), mtime))
    except Exception:
        pass
    # Mod files — canonical addressing via sdk.resolve
    for mod in sorted(sdk.mods, key=lambda m: m.load_order):
        try:
            mf = sdk.resolve(f"mod:{mod.name}/{rel}")
            if mf and Path(mf).exists():
                mtime = datetime.fromtimestamp(Path(mf).stat().st_mtime)
                found.append((mod.name, mod.load_order, Path(mf), mtime))
        except Exception:
            pass
    return found

def read_file(path: Path) -> list[str]:
    try:
        return path.read_bytes().decode("utf-8-sig", errors="replace").splitlines()
    except Exception:
        return []

def diff_stats(a_lines: list[str], b_lines: list[str]) -> tuple[int, int]:
    d = list(difflib.unified_diff(a_lines, b_lines, lineterm=""))
    added   = sum(1 for l in d if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in d if l.startswith("-") and not l.startswith("---"))
    return added, removed

# ---------------------------------------------------------------------------
# Build report
# ---------------------------------------------------------------------------
out: list[str] = []
W = out.append
now = datetime.now().strftime("%Y-%m-%d %H:%M")

W("=" * 78)
W("ERROR FILE DEEP ANALYSIS")
W(f"Generated  : {now}")
W(f"Playset    : {sdk.playset_name}")
W(f"Log source : {log_canon}")
W(f"Top files  : {TOP_N}  |  Total script errors: {len(error_blocks):,}")
W("=" * 78)
W("")

# Summary table first
W("RANK  ERRORS  FILE")
W("─" * 78)
for rank, (rel, errs) in enumerate(top_files, 1):
    W(f"  {rank:>2}  {len(errs):>5}  {rel}")
W("")

for rank, (rel, errs) in enumerate(top_files, 1):
    W("=" * 78)
    W(f"#{rank}  [{len(errs)} errors]  {rel}")
    W("=" * 78)
    W("")

    instances = find_instances(rel)

    if not instances:
        W("  No instances found in active playset or vanilla game files.")
        W("")
        continue

    # Winning instance (highest load order)
    winner    = instances[-1]
    our_inst  = next((i for i in instances if i[0] == OUR_SUBMOD), None)

    # ── Override chain ────────────────────────────────────────────────────
    W(f"  OVERRIDE CHAIN  ({len(instances)} instance(s), load order ascending):")
    for mod_name, lo, fpath, mtime in instances:
        flags = []
        if mtime > CUTOFF_DT:
            flags.append(f"RECENT ({mtime.strftime('%Y-%m-%d')})")
        if (mod_name, lo) == (winner[0], winner[1]):
            flags.append("WINNER")
        if mod_name == OUR_SUBMOD:
            flags.append("OUR SUBMOD")
        flag_str = "  <<< " + ", ".join(flags) if flags else ""
        W(f"    [{lo:>3}] {mod_name}{flag_str}")
        W(f"           {fpath}")
        W(f"           Modified: {mtime.strftime('%Y-%m-%d %H:%M')}")
    W("")

    W(f"  WINNING MOD  : {winner[0]}  (load order {winner[1]})")
    W(f"  ERRORS OWNED BY: {winner[0]}")
    W("")

    # ── Our submod analysis ───────────────────────────────────────────────
    if our_inst:
        W("  OUR SUBMOD OVERRIDE: YES")
        original = instances[0]  # lowest load order = originator

        # Diff: our override vs original source
        orig_lines = read_file(original[2])
        our_lines  = read_file(our_inst[2])
        a, r = diff_stats(orig_lines, our_lines)
        W(f"  DIFF vs ORIGINAL [{original[0]}]: +{a} added / -{r} removed")
        if r > 50 and r > a * 1.5:
            W(f"  *** STALE PATCH WARNING: we remove {r} lines but only add {a}.")
            W(f"      Original may have added new content our patch is now deleting.")

        # Diff: our override vs immediate predecessor
        our_idx = instances.index(our_inst)
        if our_idx > 0:
            pred = instances[our_idx - 1]
            if pred[0] != our_inst[0]:
                pred_lines = read_file(pred[2])
                a2, r2 = diff_stats(pred_lines, our_lines)
                W(f"  DIFF vs PREDECESSOR [{pred[0]}]: +{a2} added / -{r2} removed")
                if r2 > 50 and r2 > a2 * 1.5:
                    W(f"  *** PREDECESSOR STALE WARNING: predecessor may have new content we overwrite.")

        # Was original recently updated?
        orig_recent = original[3] > CUTOFF_DT
        if orig_recent:
            W(f"  *** ORIGINAL SOURCE UPDATED {original[3].strftime('%Y-%m-%d')} (<{CUTOFF_DAYS} days ago)")
            W(f"      Our patch was probably written against an older version — review diff.")

        # Was any intermediate mod recently updated?
        intermediates = [i for i in instances if i[0] not in (original[0], OUR_SUBMOD)]
        for iname, ilo, ipath, imtime in intermediates:
            if imtime > CUTOFF_DT:
                W(f"  *** INTERMEDIATE MOD RECENTLY UPDATED: {iname} ({imtime.strftime('%Y-%m-%d')})")

    else:
        W("  OUR SUBMOD OVERRIDE: NO")
        winner_recent = winner[3] > CUTOFF_DT
        if winner_recent:
            W(f"  *** WINNING FILE RECENTLY UPDATED ({winner[3].strftime('%Y-%m-%d')})")
            W(f"      Errors likely introduced by this update.")
        if winner[0] != OUR_SUBMOD:
            W(f"  ACTION: consider creating an override in our submod if fix is needed.")

    W("")

    # ── Recommendation ────────────────────────────────────────────────────
    W("  RECOMMENDATION:")
    if our_inst and our_inst == winner:
        orig_recent = instances[0][3] > CUTOFF_DT
        if orig_recent:
            W("    Our file is winning but the original source was recently updated.")
            W("    -> Diff the original against our patch, check for new content we're removing.")
            W("    -> If significant new content: update our patch to incorporate it.")
        else:
            W("    Our file is winning and source is stable.")
            W("    -> Fix the errors directly in our submod override.")
    elif our_inst and our_inst != winner:
        W(f"    Our override exists but is NOT winning — [{winner[0]}] loads after us.")
        W(f"    -> Either bump our file to load after that mod, or coordinate with it.")
    elif not our_inst:
        if winner[0] == "Base Game":
            W("    Vanilla file is winning (no mod overrides).")
            W("    -> Create an override in our submod to fix the errors.")
        else:
            W(f"    [{winner[0]}] is winning with no override from us.")
            W(f"    -> Assess whether to patch this in our submod or report upstream.")
    W("")

    # ── Sample errors ─────────────────────────────────────────────────────
    W("  SAMPLE ERRORS (up to 5 unique messages):")
    seen: set[str] = set()
    count = 0
    for block in errs:
        mm = RE_MSG.search(block)
        lm = RE_LINE_NO.search(block)
        msg     = mm.group(1).strip() if mm else "?"
        line_no = lm.group(1) if lm else "?"
        key     = msg[:100]
        if key not in seen:
            seen.add(key)
            W(f"    line {line_no:>6}: {msg[:160]}")
            count += 1
            if count >= 5:
                break
    W("")

W("=" * 78)
W(f"END OF ANALYSIS  |  {len(top_files)} files  |  {len(error_blocks):,} total errors")
W("=" * 78)

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------
out_path = sdk.wip / "error_file_analysis.txt"
out_path.write_text("\n".join(out), encoding="utf-8")
print(f"\nReport written to: root:ck3raven_data/wip/error_file_analysis.txt")
print(f"\nTOP {TOP_N} FILES:")
for rank, (rel, errs) in enumerate(top_files, 1):
    print(f"  #{rank:>2}  [{len(errs):>4}]  {rel}")
