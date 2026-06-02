"""
setup_error_analysis_toolkit.py

Creates wip/error_analysis/ folder, copies the two analysis scripts
into it, and writes README.md.
Run once to organise the toolkit; safe to re-run (overwrites).
"""
from __future__ import annotations
import shutil
import sys
from pathlib import Path

_sdk_dir = Path.home() / ".ck3raven" / "wip" / "sdk"
sys.path.insert(0, str(_sdk_dir))
import ck3_sdk as _sdk_mod
sdk = _sdk_mod.CK3SDK()

wip     = sdk.wip
dest    = wip / "error_analysis"
dest.mkdir(exist_ok=True)

# ── Copy scripts ──────────────────────────────────────────────────────────
for name in ("parse_script_errors.py", "analyze_error_files.py"):
    src = wip / name
    if not src.exists():
        print(f"WARNING: {name} not found in wip, skipping")
        continue
    shutil.copy2(src, dest / name)
    print(f"Copied {name}")

# ── Write README ──────────────────────────────────────────────────────────
readme = dest / "README.md"
readme.write_text("""\
# CK3 Error Analysis Toolkit

Scripts for parsing the CK3 `error.log`, clustering script system errors
by cause, and producing a deep per-file analysis with override chain data,
diff stats, and fix recommendations.

---

## Scripts

### `parse_script_errors.py`
Reads the CK3 `error.log`, extracts every script system error block,
and clusters them into ~24 named categories (unset_scope, null_scope_object,
failed_context_switch, invalid_comparison, undefined_symbol, …).

**Output:** `wip/script_error_report.txt`  
Format: table of contents → mod index → per-cluster detail with FILE, PATH,
MOD attribution, affected LINES, OBJECTS, and up to 5 unique example messages.

---

### `analyze_error_files.py`
Builds on the same log to rank the top 25 files by error count, then for
each file:

1. Walks the full override chain across all active-playset mods (vanilla →
   load order ascending) using `sdk.resolve()` canonical addressing.
2. Identifies the **winning** mod (highest load order = last word).
3. Flags instances modified within the last 10 days.
4. If our submod (`Gambo+EC724 Submod`) has an override:
   - Diffs our file vs the original source (lowest load order).
   - Diffs our file vs the immediate predecessor in the chain.
   - Warns if deletions >> additions (stale patch removing content the
     original has since changed or added).
5. If we do NOT have an override, notes the winning mod and whether it was
   recently updated.
6. Prints up to 5 unique sample error messages per file.

**Output:** `wip/error_file_analysis.txt`

---

## How to Run

Both scripts require the CK3 Lens MCP **sign → contract → exec** workflow.

### Step 1 – Choose log source

**Default** (regular `error.log` from this session):  
No extra step — scripts fall back to `root:user_docs/logs/error.log`.

**Crash log** (recommended after a crash):  
Write the path to `wip/.log_path_override` *before* signing.
The file is consumed (auto-deleted) on first read.

```
# Example override file content:
C:\\Users\\nateb\\Documents\\Paradox Interactive\\Crusader Kings III\\crashes\\ck3_20260528_092736\\logs\\error.log
```

Crash folders are at:
`root:user_docs/crashes/<ck3_YYYYMMDD_HHMMSS>/logs/error.log`

### Step 2 – Sign the script

Ask Copilot:
> "Sign and run `parse_script_errors.py`" or "Sign and run `analyze_error_files.py`"

Copilot will call `ck3_contract(sign_script)` — approve the CodeLens prompt
that appears at the top of the file in VS Code.

### Step 3 – Open contract and exec

Copilot handles this automatically after you approve.

### Step 4 – Read the output

Open `wip/script_error_report.txt` or `wip/error_file_analysis.txt` directly
in VS Code.  Both files are plain text, ~1,500 lines for a typical session log.

---

## Typical Workflow After a Crash

```
1. Note the crash folder name from root:user_docs/crashes/
2. Tell Copilot: "run the error analysis against crash log <folder name>"
3. Copilot writes .log_path_override, signs, and runs analyze_error_files.py
4. Open wip/error_file_analysis.txt
5. Review files where our submod is WINNER + STALE PATCH WARNING
6. For those files, ask Copilot to diff and update the override patch
```

---

## Key Constants (edit in `analyze_error_files.py` if needed)

| Constant | Default | Purpose |
|---|---|---|
| `OUR_SUBMOD` | `"Gambo+EC724 Submod"` | Submod name to track |
| `CUTOFF_DAYS` | `10` | Days threshold for "recently updated" flag |
| `TOP_N` | `25` | Number of top files to analyse |

---

## SDK Bootstrap (both scripts)

```python
_sdk_dir = Path.home() / ".ck3raven" / "wip" / "sdk"
sys.path.insert(0, str(_sdk_dir))
import ck3_sdk as _sdk_mod
sdk = _sdk_mod.CK3SDK()
```

File lookups use canonical addressing:
```python
sdk.resolve("root:game/common/...")          # vanilla
sdk.resolve("mod:Gambo+EC724 Submod/...")    # our submod
sdk.resolve(f"mod:{mod.name}/{rel}")         # any mod in playset
```
""", encoding="utf-8")
print(f"README.md written")

print(f"\\nDone. Toolkit at: root:ck3raven_data/wip/error_analysis/")
print(f"  parse_script_errors.py")
print(f"  analyze_error_files.py")
print(f"  README.md")
