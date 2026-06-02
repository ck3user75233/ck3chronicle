# ck3chronicle Multi-Phase Development Plan

## Planning principle

Every phase should deliver usable value, not merely internal plumbing.

The product should grow from:

```text
Preserve evidence → Canonicalize evidence → Compare evidence → Enrich with source context → Rank actionability → Support agents → Integrate with IDE/workflows → Assist repair
```

---

# Phase 0: Evidence Preservation and Session Registry

## Goal

Stop losing CK3 runtime evidence.

## User value

The user can answer:

- What logs did I have after that run?
- Did this session appear to crash?
- Was there a crash folder?
- What files were captured?
- Can I retrieve the raw evidence later?

## Core commands

```bash
ck3chronicle doctor
ck3chronicle ingest
ck3chronicle sessions
ck3chronicle show-session <session_id>
```

## Functional scope

`doctor` verifies:

- logs directory exists
- crashes directory exists
- SQLite database can be created/written
- archive directory can be created/written
- known log files are readable if present
- schema version
- ck3chronicle version

`ingest` should:

- create a session record
- snapshot configured logs
- hash each captured file
- record file size and capture time
- detect newest crash folder if present
- link probable crash folder to session
- inventory crash artifacts
- store metadata in SQLite

## Exit criteria

- `doctor` runs successfully
- `ingest` preserves logs
- crash folders are detected and inventoried
- sessions can be listed and inspected
- no parser is required for the session record to be useful

---

# Phase 1: Canonical Issue Records and Error Clustering

## Goal

Turn large, noisy logs into readable unique issue records using a canonical schema.

## Core commands

```bash
ck3chronicle parse <session_id>
ck3chronicle report
ck3chronicle errors
ck3chronicle latest --json
```

## Functional scope

- streaming parser for `error.log`
- specialized extractors where useful
- canonical issue schema
- multi-line block grouping
- raw block hash
- normalized signature
- conservative normalization
- file path extraction
- category, severity, confidence
- JSON output

## Categories

- Syntax / Structural
- Scope Mismatch
- Missing Reference
- Script Execution
- Localization
- Database Conflict
- Asset / Graphics
- GUI / Interface
- Mod Descriptor / Metadata
- Crash Evidence
- Engine / System
- Unclassified

## Exit criteria

- huge logs parse without memory failure
- repeated errors cluster
- multi-line errors remain intact
- every issue has raw hash + normalized signature
- every extractor emits canonical issue records
- reports are generated from canonical issue records, not raw logs

---

# Phase 2: Delta Reports, Baselines, and Noise Management

## Goal

Show what changed between runs.

## Core commands

```bash
ck3chronicle diff
ck3chronicle report --since previous
ck3chronicle baseline create <name>
ck3chronicle baseline list
ck3chronicle report --since <baseline>
ck3chronicle ignore <issue_id>
ck3chronicle unignore <issue_id>
ck3chronicle ignored
```

## Functional scope

Compare latest session against previous session or named baseline.

Classify issues as:

- New
- Fixed
- Worse
- Improved
- Unchanged
- Ignored

Add ignore state with reason and optional expiry.

## Exit criteria

- latest vs previous comparison works
- latest vs baseline comparison works
- ignored issues are hidden by default
- crash status is included in deltas

---

# Phase 3: Source and Override-Chain Resolver

## Goal

Add the strongest feature from the best observed report: file/source ownership context and load-order/override-chain enrichment.

## User value

The user can answer:

- Is this emitted from our submod, an upstream mod, base game, or unknown?
- Which file currently wins the override chain?
- Do we already override this file?
- Should we fix directly, create an override, or report upstream?

## Core commands

```bash
ck3chronicle sources resolve
ck3chronicle report --with-sources
ck3chronicle errors --file <path>
ck3chronicle suspects
```

## Functional scope

The resolver consumes file paths from canonical issue records and enriches them with:

- override chain
- load-order winner
- source mod
- base game vs workshop vs local mod
- our submod yes/no
- our submod override yes/no
- recently modified yes/no
- diff vs original where available
- diff vs predecessor where available

## Exit criteria

- override chain can be shown for referenced files
- winning mod/file is identified where available
- our submod vs upstream distinction is explicit
- reports avoid overclaiming root cause
- source resolver does not parse raw logs

---

# Phase 4: Workspace Context and Likely-Cause Analysis

## Goal

Connect runtime issues to recent user work without overclaiming certainty.

## Core commands

```bash
ck3chronicle workspace configure <path>
ck3chronicle context
ck3chronicle errors --changed-files
ck3chronicle suspects
ck3chronicle report --with-context
```

## Functional scope

Capture:

- workspace roots
- Git branch
- Git commit
- dirty yes/no
- modified files
- added/deleted files
- active mod/playset hints where available

Use cautious language:

- referenced_file
- emitting_file
- recently_modified_candidate
- load_order_candidate
- probable_cause
- confidence
- reason

## Exit criteria

- errors can be queried by file
- new errors can be correlated to changed files
- reports explain why a file is suggested
- confidence is explicit

---

# Phase 5: Fixability Ranking and Recommendation Report

## Goal

Prioritize what to fix first.

## Functional scope

Create a fixability score based on:

```text
severity weight
+ new/regression weight
+ crash-adjacent weight
+ our-submod-winner weight
+ recently-modified weight
+ small-diff-from-predecessor weight
- upstream-only/no-override penalty
- known-noise penalty
```

## Report output

For each top action candidate:

- file
- issue count
- highest severity
- session delta
- override chain
- winning mod
- our submod yes/no
- recent modification yes/no
- sample canonical issue messages
- recommendation
- confidence

## Exit criteria

- report ranks issues/files by actionability, not only count
- recommendation language is cautious and evidence-based
- upstream-only issues are not ranked above direct submod regressions unless severity demands it

---

# Phase 6: Agentic Query Layer

## Goal

Expose ck3chronicle evidence cleanly to ck3raven and other agents.

## Core commands

```bash
ck3chronicle latest --json
ck3chronicle diff --json
ck3chronicle errors --json
ck3chronicle suspects --json
ck3chronicle crash-status --json
```

## Potential MCP tools

```text
ck3_logs.latest_report()
ck3_logs.new_errors()
ck3_logs.fixed_errors()
ck3_logs.errors_for_file(path)
ck3_logs.session_diff(from_session, to_session)
ck3_logs.top_fatal(limit)
ck3_logs.crash_status()
ck3_logs.baseline_diff(name)
ck3_logs.suspects()
```

## Exit criteria

- an agent can inspect latest runtime state without raw logs
- JSON schemas are stable and documented
- outputs are capped and context-safe

---

# Phase 7: Cross-Run Analytics and Trend Intelligence

## Goal

Use accumulated session history to identify recurring issues, regressions, and stability patterns.

## Core commands

```bash
ck3chronicle trends
ck3chronicle issue-history <issue_id>
ck3chronicle file-history <path>
ck3chronicle stability
ck3chronicle recurring
```

## Exit criteria

- issue history works
- file history works
- recurring regressions are detectable
- crash correlation summaries are available

---

# Phase 8: IDE and ck3lens Integration

## Goal

Bring runtime evidence into the user’s normal CK3 modding workspace.

## Functional scope

- VS Code panel
- ck3lens sidebar integration
- clickable issue reports
- inline annotations
- session history browser

## Exit criteria

- latest session summary is visible in IDE
- issues can link to workspace files
- session history can be browsed
- integration relies on stable ck3chronicle APIs

---

# Phase 9: Static Validator and Script-Docs Cross-Reference

## Goal

Combine runtime evidence with static validation and CK3 scripting reference data.

## Functional scope

Optionally ingest or link results from:

- CWTools
- CK3 Tiger
- ck3raven parsers
- script_docs output
- custom symbol indexes

## Exit criteria

- runtime issues can be enriched with static context
- missing references can be checked against known symbols
- reports separate runtime evidence from inferred explanation

---

# Phase 10: Guided Repair Support

## Goal

Help humans and governed agents move from evidence to repair.

## Core commands

```bash
ck3chronicle repair-plan <issue_id>
ck3chronicle repair-context <issue_id> --json
ck3chronicle verify-fix <issue_id>
```

## Exit criteria

- repair plans are evidence-based
- agent handoff data is structured and scoped
- fix verification works after later sessions
- ck3chronicle does not bypass ck3raven governance for edits

---

# Later Optional Phases

Optional later phases include:

- watch mode
- IDE automation
- community telemetry

These are not part of the core product.
