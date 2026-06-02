# ck3chronicle Latest Session Report

Session: `2026-05-31T01-45-22`  
Compared with: previous session  
Schema version: `1`  
Parser version: `0.1.0`

## Evidence captured

| Log | Captured | Size | Hash |
|---|---:|---:|---|
| error.log | Yes | 2.4 MB | `abc123...` |
| game.log | Yes | 412 KB | `def456...` |
| debug.log | Yes | 91 KB | `ghi789...` |
| database_conflicts.log | No | - | - |

## Crash status

Crash detected: **Yes**  
Crash folder linked: `ck3_20260531_014522`  
Dump present: **Yes**  
Link confidence: **Medium**

## Issue summary

| Status | Count |
|---|---:|
| New issues | 3 |
| Fixed issues | 17 |
| Worse issues | 2 |
| Improved issues | 5 |
| Unchanged issues | 121 |
| Ignored known-noise issues | 31 |

## Top action candidates

### 1. `common/scripted_effects/TCT_scripted_effects.txt`

Fixability score: **91**  
Highest severity: **High**  
Current winning file: **Gambo+EC724 Submod**  
Our submod override: **Yes**  
Recently modified: **Yes**  
Recommendation: **Inspect/fix directly in our submod override.**  
Confidence: **High**

Sample issue:

```text
untyped trigger [ Scoped object of type 'character' is not valid ... ]
```

Call stack:

```text
common/scripted_effects/TCT_scripted_effects.txt line 275 (predict_new_cardinal)
common/scripted_effects/TCT_scripted_effects.txt line 315 (update_cardinal_window)
common/on_action/tct_on_actions.txt line 673 (tct_cardinal_update)
```

### 2. `events/house_traditions_events.txt`

Fixability score: **87**  
Highest severity: **High**  
Current winning file: **Gambo+EC724 Submod**  
Our submod override: **Yes**  
Recommendation: **Inspect/fix directly in our submod override, but review caller chain before assuming root cause.**  
Confidence: **High**

### 3. `common/on_action/hometowns_on_actions.txt`

Fixability score: **54**  
Highest severity: **Medium**  
Current winning file: **Hometowns**  
Our submod override: **No**  
Recommendation: **Assess whether to patch in our submod or report upstream.**  
Confidence: **Medium**

## Known noise collapsed

| Category | Count | Default action |
|---|---:|---|
| Localization duplicate keys | 18,442 | Hidden unless new or user-owned |
| Asset / Graphics | 223 | Show only if user-owned or crash-adjacent |
| Mod Descriptor / Metadata | 64 | Low priority |
