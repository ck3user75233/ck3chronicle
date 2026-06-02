# Canonical Pipeline and Parser-Control Rules

## Problem

Agents tend to create new parsers every time they inspect CK3 logs. This has been hard to stop.

The solution is not to ban all new parsing code. The solution is to define a canonical pipeline and a canonical issue schema.

Agents may build specialized extractors, but all extractors must emit canonical issue records.

## Hard rule

Agents may not generate final log-analysis reports directly from raw `error.log`.

All final reports must be generated from canonical ck3chronicle issue records.

## Pipeline

```text
raw CK3 logs
→ harvester snapshots evidence
→ parser/extractors emit canonical issue records
→ normalizer clusters related records
→ database stores sessions/issues/occurrences
→ delta engine compares sessions/baselines
→ source/override resolver enriches file references
→ fixability engine ranks actionability
→ report composer generates human/agent output
```

## Three separate engines

ck3chronicle should keep three concerns separate.

### 1. Log parser / extractor

Converts raw CK3 logs into canonical issue records.

It does not:

- write reports
- inspect Git
- resolve override chains
- decide recommendations
- mutate files

### 2. Source / override resolver

Consumes file paths from canonical issue records and enriches them with:

- base game/mod/submod source
- load-order winner
- override chain
- whether the winning file is the user’s submod
- whether a submod override exists
- optional diff vs original/predecessor

It does not parse raw logs.

### 3. Triage / report composer

Combines:

- issue severity
- occurrence count
- new/fixed/worse/improved status
- crash status
- source/override context
- recent modification/Git context
- fixability score

and produces recommendations.

It does not parse raw logs directly.

## Canonical issue schema

All parser/extractor output must conform to this shape or a versioned successor.

```json
{
  "schema_version": "ck3chronicle.issue.v1",
  "source_log": "error.log",
  "raw_block_hash": "...",
  "normalized_signature": "...",
  "category": "Script Execution",
  "severity": "High",
  "confidence": "High",
  "primary_file": "common/scripted_effects/TCT_scripted_effects.txt",
  "primary_line": 275,
  "primary_symbol": "predict_new_cardinal",
  "message": "untyped trigger [ Scoped object of type 'character' is not valid ... ]",
  "call_stack": [
    {
      "file": "common/scripted_effects/TCT_scripted_effects.txt",
      "line": 315,
      "symbol": "update_cardinal_window"
    },
    {
      "file": "common/on_action/tct_on_actions.txt",
      "line": 673,
      "symbol": "tct_cardinal_update"
    }
  ],
  "extracted_file_paths": [
    "common/scripted_effects/TCT_scripted_effects.txt",
    "common/on_action/tct_on_actions.txt"
  ],
  "raw_sample": "..."
}
```

## Specialized extractors

Specialized extractors are permitted for known CK3 patterns, such as:

- `jomini_script_system.cpp`
- `pdx_persistent_reader.cpp`
- localization duplicate keys
- missing localization
- asset/graphics errors
- GUI localization/layout errors
- database conflicts
- crash-folder metadata

But each extractor must emit canonical issue records.

## Forbidden pattern

Do not allow this:

```text
raw error.log
→ one-off parser
→ custom Markdown report
```

Use this instead:

```text
raw error.log
→ extractor
→ canonical issue records
→ report composer
```

## Report wording

Avoid overclaiming causality.

Prefer:

```text
CURRENT WINNING FILE / LIKELY PATCH TARGET
```

or:

```text
Runtime error attributed to winning file
```

Avoid:

```text
ERRORS OWNED BY
```

unless ownership is specifically defined as “the winning file where CK3 emitted the error,” not the true root cause.

## North-star report structure

The strongest report format is:

```text
Top files by actionability

For each file:
- issue count
- highest severity
- new/fixed/worse status
- override chain
- winning mod/file
- our submod override yes/no
- recent modification yes/no
- diff vs original/predecessor where available
- sample canonical issue messages
- recommendation
```

## Recommendation language

Use cautious recommendations:

```text
Our submod is the winning file and recent changes are present.
Recommendation: inspect/fix directly in our submod override.
Confidence: High.
```

```text
An upstream mod is the winning file and our submod does not override it.
Recommendation: assess whether to patch in our submod or report upstream.
Confidence: Medium.
```

```text
Base game is the winning file but the failure may be caused by modded data or caller context.
Recommendation: inspect caller chain and active mod interactions before patching base behavior.
Confidence: Low/Medium.
```
