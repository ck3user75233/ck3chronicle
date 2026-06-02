# ck3chronicle Modular Refactor Prototype

This package separates the functionality from the original CK3 error-analysis scripts into cleaner modules.

It is intended as a **prototype / promotion target**, not a guaranteed drop-in replacement until tested inside your ck3raven/ck3lens environment.

## What this refactor separates

The original scripts mixed several responsibilities:

```text
raw error.log parsing
→ script-error extraction
→ grouping by file
→ override-chain walking
→ diff checks
→ recommendation writing
→ final text report
```

This refactor splits those responsibilities into modules:

```text
ck3chronicle_proto/
  models.py              # dataclasses / canonical issue schema
  paths.py               # game-relative path helpers
  normalizers.py         # signatures, categories, severity/confidence
  log_parser.py          # raw log → canonical issue records
  issue_aggregator.py    # issue records → counts by file/category/signature
  override_resolver.py   # file path → override chain / winner / submod status
  fixability.py          # issue + source context → actionability score
  reports.py             # canonical records + enrichment → human report
  sdk_adapter.py         # optional ck3raven SDK adapter
  cli_error_analysis.py  # command-line composition layer
```

## Core rule

Final reports should not parse raw logs directly.

Instead:

```text
raw log
→ log_parser.parse_error_log()
→ canonical issue records
→ issue_aggregator
→ override_resolver
→ fixability
→ reports
```

## Minimal usage outside ck3raven

```bash
python -m ck3chronicle_proto.cli_error_analysis --log "path/to/error.log" --out report.txt
```

Without the ck3raven SDK, override resolution will be unavailable unless you provide source roots programmatically.

## Intended usage inside ck3raven

Inside ck3raven, use the SDK adapter:

```bash
python -m ck3chronicle_proto.cli_error_analysis --use-sdk
```

The adapter expects:

```text
~/.ck3raven/wip/sdk/ck3_sdk.py
```

and reads:

```text
root:user_docs/logs/error.log
root:ck3raven_data/wip/.log_path_override
```

matching the old scripts.

## What this preserves from the original report

The report still supports:

- top files by script-error count
- sample error messages
- override chain
- winning mod/file
- our submod override status
- diff vs original
- diff vs predecessor
- stale patch warnings
- cautious recommendation language

## Wording change

The original script used:

```text
ERRORS OWNED BY
```

This refactor uses:

```text
CURRENT WINNING FILE
```

and avoids claiming true root-cause ownership.

## Suggested promotion path

1. Put these modules under `root:repo/ck3chronicle/src/ck3chronicle/`.
2. Keep copied logs/reports under `root:ck3raven_data/wip/ck3chronicle/`.
3. Add fixture tests using known CK3 error-log snippets.
4. Have future agents extend extractors only if they emit `CanonicalIssue`.
