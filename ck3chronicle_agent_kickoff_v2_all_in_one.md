# ck3chronicle Agent Kickoff v2 — All-in-One



---

# File: `README.md`

# ck3chronicle Agent Kickoff Wrapper v2

This package contains a practical kickoff kit for using agentic coding support to build **ck3chronicle**, a standalone Python CLI tool for preserving, parsing, enriching, and reporting on Crusader Kings III runtime logs.

This v2 package incorporates the latest recommendations:

- ck3chronicle source code should live under `root:repo/ck3chronicle/`.
- `root:ck3raven_data/wip/ck3chronicle/` should be used only for scratch work, copied logs, parser spikes, generated reports, and temporary agent artifacts.
- Agents may not generate final reports directly from raw `error.log`.
- All final reports must be generated from canonical ck3chronicle issue records.
- New parsers/extractors are allowed only if they emit the canonical issue schema.
- Override-chain analysis is not part of the parser; it is a separate resolver/enrichment layer.
- The north-star report is action triage: issue clustering → file attribution → override-chain resolution → fixability ranking → recommendation.

## What ck3chronicle is

ck3chronicle is a CK3 runtime log history and triage tool.

It should preserve CK3 logs and crash evidence, parse noisy runtime output into structured issue records, compare sessions against previous runs or baselines, enrich those records with source/override context, and expose the result to both humans and agents.

The first product promise is:

> After each CK3 run, ck3chronicle tells you what changed, what matters, whether the game crashed, and which recent or winning files are most likely involved.

## What ck3chronicle is not in the MVP

The MVP is not:

- a VS Code extension
- an MCP server
- a background daemon
- an autonomous repair tool
- a full crash dump parser
- a telemetry system
- a replacement for CWTools or CK3 Tiger
- a CK3 static validator
- a mod file editor

Those may come later. The first release should be a reliable standalone CLI.

## Repository placement decision

Use this as the default layout:

```text
root:repo/
  ck3chronicle/
    README.md
    pyproject.toml
    docs/
    src/ck3chronicle/
    tests/

root:ck3raven_data/wip/
  ck3chronicle/
    scratch_reports/
    sample_logs/
    parser_spikes/
    generated_reports/
    archive/
    db/
```

Product code belongs in `root:repo/ck3chronicle/`.

Scratch artifacts belong in `root:ck3raven_data/wip/ck3chronicle/`.

Large logs, crash folders, generated SQLite databases, and experimental one-off scripts should not be committed to the main repo.

## Recommended usage

Give agents the files in this package as context and then assign one work packet at a time.

Start with:

1. `docs/00_project_charter.md`
2. `docs/01_repo_placement_and_boundaries.md`
3. `docs/02_target_repo_shape.md`
4. `docs/03_canonical_pipeline.md`
5. `docs/04_multiphase_plan.md`
6. `agent_prompts/01_scaffold_cli.md`

Do not start by asking an agent to “build ck3chronicle.” Start with narrow packets.

## Suggested first milestone

The first working vertical slice should be:

```bash
ck3chronicle doctor
ck3chronicle ingest --logs-dir ./tests/fixtures/logs --crashes-dir ./tests/fixtures/crashes --archive-dir ./tmp/archive --db ./tmp/ck3chronicle.sqlite
ck3chronicle report
ck3chronicle latest --json
```

This proves:

- CLI works
- config/options work
- logs are discovered
- logs are snapshotted
- crash folder evidence is detected
- session is persisted
- canonical issue records are produced once parsing exists
- basic report can be generated from canonical issue records

## Operating model

For each agent packet:

1. Give the agent the project charter.
2. Give the agent the repo-placement rules.
3. Give the agent the target repo shape.
4. Give the agent one prompt from `agent_prompts/`.
5. Require the definition of done.
6. Run tests.
7. Ask a second agent to review the diff.
8. Merge only if scope was respected.

## Recommended near-term sequence

1. Scaffold CLI.
2. SQLite foundation.
3. Harvester and crash inventory.
4. Canonical parser and issue model.
5. Normalization and categorization.
6. Reports generated only from canonical issue records.
7. Delta, baseline, ignore.
8. Override-chain resolver and source context.
9. Workspace/Git context.
10. Fixability ranking and recommendation report.
11. Agent JSON contracts or MCP wrapper.

## License / status

This is planning and kickoff material, not production code.


---

# File: `agent_prompts/01_scaffold_cli.md`

# Agent Prompt 01: Scaffold CLI

You are building the initial scaffold for ck3chronicle, a standalone Python CLI tool for preserving and analyzing Crusader Kings III runtime logs.

Product code must be created under:

```text
root:repo/ck3chronicle/
```

Scratch artifacts, generated reports, temporary logs, and parser spikes must go under:

```text
root:ck3raven_data/wip/ck3chronicle/
```

Create the package skeleton, `pyproject.toml`, CLI entrypoint, and empty command handlers for:

- `doctor`
- `ingest`
- `sessions`
- `report`
- `latest --json`

Use explicit CLI options for:

- `--logs-dir`
- `--crashes-dir`
- `--archive-dir`
- `--db`

so tests do not rely on real user paths.

Do not implement parsing yet.

Do not build:

- MCP server
- VS Code extension
- background daemon
- autonomous repair
- telemetry

Acceptance criteria:

- `python -m ck3chronicle.cli doctor` runs.
- CLI has help text for all commands.
- Tests can invoke the CLI.
- `pyproject.toml` defines package metadata and dependencies.
- No CK3-specific hardcoded absolute path is required for tests.
- No large log/copy artifacts are committed.
- Return a summary of files created and commands to run tests.


---

# File: `agent_prompts/02_sqlite_foundation.md`

# Agent Prompt 02: SQLite Foundation

Implement the SQLite database foundation for ck3chronicle.

Create idempotent schema initialization and repository functions for:

- sessions
- log_snapshots
- crash_folders
- crash_artifacts
- issues
- issue_occurrences
- source_resolutions
- fixability_assessments
- baselines
- ignored_issues
- schema_migrations

Use a temporary database in tests.

Do not connect this to real CK3 paths yet.
Do not implement parsing.
Do not write raw SQL in CLI handlers; use repository functions.

Acceptance criteria:

- Database initializes idempotently.
- Schema version is recorded.
- Repository functions can create a session.
- Repository functions can attach log snapshots.
- Repository functions can attach crash folder metadata.
- Repository functions can insert canonical issue records.
- Repository functions can attach source resolution metadata.
- Repository functions can fetch latest session.
- Unit tests use a temporary SQLite database.


---

# File: `agent_prompts/03_harvester_crash_inventory.md`

# Agent Prompt 03: Harvester and Crash Inventory

Implement `ck3chronicle ingest`.

Given:

- `--logs-dir`
- `--crashes-dir`
- `--archive-dir`
- `--db`

Behavior:

- create a new session
- snapshot configured log files into an archive/session folder
- compute sha256 and file size for each captured log
- record log snapshots in SQLite
- detect the newest crash folder, if present
- inventory crash artifacts
- record `dump_present` true/false
- skip missing logs with warnings, not fatal errors

Do not parse dump files.
Do not double-count crash-folder copied logs as primary logs.
Do not implement watch mode.
Do not place archive output inside `root:repo/ck3chronicle/`.

Acceptance criteria:

- Ingest works against test fixtures.
- Missing logs are warnings, not fatal errors.
- Crash folder copied-log artifacts are inventoried but not double-counted as parsed logs.
- Session can be listed after ingest.
- Tests cover logs present, missing logs, and crash folder present.


---

# File: `agent_prompts/04_canonical_parser.md`

# Agent Prompt 04: Canonical Parser

Implement a pure streaming parser for CK3-style logs.

The parser must be side-effect-free.

It should accept:

- a file path, or
- an iterable of lines

and return canonical issue records.

Each issue record must include:

- schema_version
- source_log
- raw_text or capped raw_sample
- raw_block_hash
- normalized_signature
- first_line_number
- last_line_number
- category
- severity
- confidence
- primary_file
- primary_line
- primary_symbol
- message
- call_stack
- extracted_file_paths

It should detect timestamp-prefixed CK3 log lines as new blocks and attach continuation lines to the current block.

Add tests for:

- single-line errors
- multi-line script-system errors
- repeated errors with different line numbers
- localization spam
- asset/graphics errors
- descriptor errors
- empty logs

Do not write to SQLite from the parser.
Do not inspect Git from the parser.
Do not copy files from the parser.
Do not resolve override chains from the parser.
Do not generate final reports directly from raw logs.

Acceptance criteria:

- All parser output conforms to `ck3chronicle.issue.v1`.
- Multi-line script-system call stacks are captured.
- Repeated runtime IDs can be normalized without losing useful identity.
- Tests prove output schema conformance.


---

# File: `agent_prompts/05_normalization_categorization.md`

# Agent Prompt 05: Normalization and Categorization

Implement normalization and categorization helpers.

Normalization should mask:

- line numbers
- near-line references
- memory addresses
- obvious runtime IDs
- volatile internal IDs
- generated argument hashes where appropriate

Do not blindly mask every standalone number.

Categories:

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

Severity values:

- Fatal
- High
- Medium
- Low
- Noise
- Unknown

Confidence values:

- High
- Medium
- Low

Acceptance criteria:

- Fixtures prove repeated line-number variants cluster together.
- Distinct event/object IDs are not accidentally collapsed unless explicitly intended.
- Every issue has category, severity, and confidence.
- Tests cover all initial categories.
- Localization and asset noise can be classified separately from script execution errors.


---

# File: `agent_prompts/06_reports_from_canonical_records.md`

# Agent Prompt 06: Reports from Canonical Issue Records

Implement latest-session reporting for ck3chronicle.

Commands:

- `ck3chronicle report`
- `ck3chronicle report --format markdown`
- `ck3chronicle latest --json`

Reports must consume canonical issue records from the database or parser output.

Reports must not parse raw `error.log` directly.

Reports should include:

- session id
- captured logs
- crash detected yes/no
- crash folder linked yes/no
- unique issue count
- top issues by severity
- top issues by occurrence count
- unclassified count
- referenced files

Reports should not dump full raw logs by default.

Acceptance criteria:

- Terminal report is readable.
- JSON report is compact and stable.
- Markdown report can be saved to file.
- Reports include crash status when available.
- Tests use fixture sessions and canonical issue records.
- Tests prove report generation does not depend on raw log parsing.


---

# File: `agent_prompts/07_delta_baseline_ignore.md`

# Agent Prompt 07: Delta, Baseline, Ignore

Implement session comparison, baselines, and ignored issues.

Commands:

- `ck3chronicle diff`
- `ck3chronicle baseline create <name>`
- `ck3chronicle baseline list`
- `ck3chronicle report --since <baseline>`
- `ck3chronicle ignore <issue_id>`
- `ck3chronicle unignore <issue_id>`
- `ck3chronicle ignored`

Acceptance criteria:

- Latest session can be compared to previous session.
- Issues are classified as new, fixed, worse, improved, or unchanged.
- Ignored issues are hidden from default reports but still stored.
- Baseline comparison works.
- Crash status is included in deltas.
- Delta logic operates on canonical issue records and normalized signatures.


---

# File: `agent_prompts/08_source_override_resolver.md`

# Agent Prompt 08: Source and Override-Chain Resolver

Implement source/override-chain resolution.

This is not a parser.

The resolver consumes file paths from canonical issue records and enriches them with source context.

Inputs:

- canonical issue records
- configured mod roots / playset roots
- base game root if configured
- load order metadata if available
- local submod name/path if configured

Outputs should include:

- referenced_file
- winning_source_name
- winning_source_type: base_game | workshop_mod | local_mod | unknown
- winning_source_path
- load_order_index
- our_submod_override: true/false
- override_chain
- recently_modified
- diff_vs_original_summary where available
- diff_vs_predecessor_summary where available
- confidence
- reason

Do not parse raw logs.
Do not generate final reports directly.
Do not modify files.

Acceptance criteria:

- Synthetic fixture mod tree can resolve a winning file.
- Our submod winner is detected.
- Upstream-only winner is detected.
- Base-game winner is detected.
- Override chain is ordered correctly.
- Output uses cautious language and confidence.


---

# File: `agent_prompts/09_workspace_context.md`

# Agent Prompt 09: Workspace Context

Implement workspace and Git context capture.

Commands:

- `ck3chronicle workspace configure <path>`
- `ck3chronicle context`
- `ck3chronicle errors --changed-files`
- `ck3chronicle errors --file <path>`
- `ck3chronicle suspects`
- `ck3chronicle report --with-context`

Capture:

- workspace roots
- Git branch
- Git commit
- dirty yes/no
- modified files
- added files
- deleted files

Use cautious likely-cause language.

Output fields should distinguish:

- referenced_file
- emitting_file
- recently_modified_candidate
- load_order_candidate
- probable_cause
- confidence
- reason

Acceptance criteria:

- Errors can be queried by file.
- New errors can be correlated to changed files.
- Reports explain why a file is suggested.
- Confidence is explicit.
- The tool does not claim certainty when evidence is only circumstantial.


---

# File: `agent_prompts/10_fixability_ranking.md`

# Agent Prompt 10: Fixability Ranking

Implement fixability/actionability ranking.

The ranking should consider:

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

Inputs:

- canonical issue records
- session deltas
- ignore state
- crash status
- source/override resolver output
- workspace/Git context where available

Outputs:

- fixability score
- recommendation
- confidence
- reason
- top files by actionability
- top issues by actionability

Acceptance criteria:

- Direct submod regressions rank highly.
- Known localization/asset noise ranks lower by default.
- Upstream-only issues do not outrank direct submod regressions unless severity demands it.
- Recommendation language is cautious.
- Tests cover ranking examples.


---

# File: `agent_prompts/11_agent_json_contracts.md`

# Agent Prompt 11: Agent JSON Contracts

Implement stable JSON output contracts for agentic use.

Commands:

- `ck3chronicle latest --json`
- `ck3chronicle diff --json`
- `ck3chronicle errors --json`
- `ck3chronicle suspects --json`
- `ck3chronicle crash-status --json`

JSON outputs should be:

- compact
- deterministic
- schema-versioned
- explicit about confidence
- free of giant raw log dumps by default

Optional raw evidence retrieval should be capped.

Potential future MCP wrappers:

- `ck3_logs.latest_report()`
- `ck3_logs.new_errors()`
- `ck3_logs.fixed_errors()`
- `ck3_logs.errors_for_file(path)`
- `ck3_logs.session_diff(from_session, to_session)`
- `ck3_logs.top_fatal(limit)`
- `ck3_logs.crash_status()`
- `ck3_logs.baseline_diff(name)`
- `ck3_logs.suspects()`

Acceptance criteria:

- JSON schema version is included.
- Latest session summary is available.
- Diffs are available.
- Crash status is available.
- Suspects are available with confidence and reason.
- Output is suitable for agent context.
- Output is based on canonical issue records and enrichment tables, not raw logs.


---

# File: `docs/00_project_charter.md`

# ck3chronicle Project Charter

## Product definition

ck3chronicle is a standalone Python CLI tool for preserving and analyzing Crusader Kings III runtime logs.

It should preserve CK3 logs and crash evidence, convert noisy runtime output into canonical structured issue records, compare sessions against previous runs or baselines, enrich issue records with source/override context, and expose the result to both humans and agents.

## MVP promise

After each CK3 run, ck3chronicle should tell the user:

- what logs were preserved
- whether the session appears to have crashed
- what unique issues appeared
- what issues are new, fixed, worse, or improved
- what known noise can be hidden
- what files are referenced by important issues
- what mod/file currently wins the override chain where resolvable
- whether the likely patch target is the user’s submod, an upstream mod, base game, or unknown
- what structured JSON can be consumed by agents

## Product north star

The best human-facing output is not a generic parser report. It is an action triage report:

```text
issue clustering
→ file attribution
→ override-chain resolution
→ fixability ranking
→ recommendation
```

The report should answer:

```text
Is this probably our file, an upstream mod file, a base-game issue, or an override/compatch issue?
What changed?
What should we inspect first?
```

## MVP commands

The MVP should eventually support:

```bash
ck3chronicle doctor
ck3chronicle ingest
ck3chronicle sessions
ck3chronicle report
ck3chronicle latest --json
ck3chronicle diff
ck3chronicle baseline create <name>
ck3chronicle baseline list
ck3chronicle ignore <issue_id>
ck3chronicle unignore <issue_id>
```

## First useful vertical slice

The first vertical slice is:

```bash
ck3chronicle doctor
ck3chronicle ingest --logs-dir ./tests/fixtures/logs --crashes-dir ./tests/fixtures/crashes --archive-dir ./tmp/archive --db ./tmp/ck3chronicle.sqlite
ck3chronicle report
ck3chronicle latest --json
```

This should work before advanced features are added.

## Design principles

1. Build a working CLI before building integrations.
2. Preserve raw evidence before interpreting it.
3. Keep the parser pure and side-effect-free.
4. Use SQLite for durable local history.
5. Keep reports useful to humans and compact enough for agents.
6. Do not overclaim blame. Use confidence and evidence.
7. Avoid dumping raw logs by default.
8. Every phase must add user-visible value.
9. Agents should receive narrow tasks with clear target files.
10. ck3chronicle should remain read-only with respect to mod files.
11. Final reports must be generated from canonical issue records, not directly from raw logs.
12. Specialized parsers/extractors are allowed only if they emit the canonical issue schema.
13. Override-chain resolution is not parsing; it is enrichment.
14. Product code belongs in `root:repo/ck3chronicle/`; scratch work belongs in `root:ck3raven_data/wip/ck3chronicle/`.


---

# File: `docs/01_repo_placement_and_boundaries.md`

# Repository Placement and Boundaries

## Decision

ck3chronicle source code should live under:

```text
root:repo/ck3chronicle/
```

Scratch work, copied logs, crash artifacts, generated databases, and parser experiments should live under:

```text
root:ck3raven_data/wip/ck3chronicle/
```

## Rationale

`root:repo/ck3chronicle/` is the best long-term home because:

- Agents that develop ck3raven can also work on ck3chronicle.
- Product code is clearly distinguished from scratch work.
- The same repo-level governance, tests, CI, and conventions can apply.
- Contract scopes can target a stable path.
- Integration with ck3raven and ck3lens remains straightforward.
- ck3chronicle can still be split out later if needed.

`root:ck3raven_data/wip/ck3chronicle/` should remain the sandbox, not the product home.

## Recommended layout

```text
root:repo/
  ck3chronicle/
    README.md
    pyproject.toml
    docs/
      product_blueprint.md
      phase_plan.md
      parser_contract.md
      report_contract.md
      override_resolver_contract.md
    src/
      ck3chronicle/
        __init__.py
        cli.py
        config.py
        ingest.py
        parser/
        analysis/
        reporting/
        db/
        models/
    tests/
      fixtures/
      test_*.py

root:ck3raven_data/
  wip/
    ck3chronicle/
      scratch_reports/
      sample_logs/
      parser_spikes/
      generated_reports/
      archive/
      db/
```

## Product-code rule

Product code goes here:

```text
root:repo/ck3chronicle/
```

Temporary work goes here:

```text
root:ck3raven_data/wip/ck3chronicle/
```

## Large artifact rule

Do not put large logs, crash folders, generated SQLite databases, or generated reports in the main repo.

Use WIP/data paths instead:

```text
root:ck3raven_data/wip/ck3chronicle/sample_logs/
root:ck3raven_data/wip/ck3chronicle/archive/
root:ck3raven_data/wip/ck3chronicle/db/
root:ck3raven_data/wip/ck3chronicle/generated_reports/
```

Only small curated fixtures should live in:

```text
root:repo/ck3chronicle/tests/fixtures/
```

## Agent rule

Agents may create temporary experiments, generated reports, copied logs, crash artifacts, and parser spikes under:

```text
root:ck3raven_data/wip/ck3chronicle/
```

No production code should be left in WIP unless explicitly promoted into:

```text
root:repo/ck3chronicle/
```

through a reviewed contract.

## Suggested contract boundary

```text
Allowed product target:
- root:repo/ck3chronicle/**

Allowed scratch target:
- root:ck3raven_data/wip/ck3chronicle/**

Forbidden unless explicitly approved:
- root:repo/tools/ck3lens_mcp/**
- root:repo/ck3lens/**
- root:repo/ck3raven core enforcement/governance files
- real CK3 log directories
- Steam workshop directories
```


---

# File: `docs/02_target_repo_shape.md`

# Target Repository Shape

Recommended starting structure:

```text
root:repo/
  ck3chronicle/
    pyproject.toml
    README.md
    docs/
      parser_contract.md
      report_contract.md
      override_resolver_contract.md
    src/
      ck3chronicle/
        __init__.py
        cli.py
        config.py
        paths.py
        doctor.py
        ingest.py
        parser/
          __init__.py
          ck3_error.py
          normalize.py
          categorize.py
          extractors.py
        analysis/
          __init__.py
          delta.py
          fixability.py
          override_resolver.py
          source_context.py
        reporting/
          __init__.py
          terminal.py
          markdown.py
          json_report.py
        db/
          __init__.py
          connection.py
          schema.py
          migrations.py
          repository.py
        models/
          __init__.py
          session.py
          log_snapshot.py
          issue.py
          crash.py
          override.py
          report.py
    tests/
      fixtures/
        logs/
          simple_error.log
          multiline_script_error.log
          repeated_error.log
          localization_spam.log
          database_conflicts.log
        crashes/
          ck3_20260531_014522/
            error.log
            game.log
            debug.log
            exception.txt
            dump.dmp
      test_doctor.py
      test_ingest.py
      test_parser.py
      test_normalize.py
      test_report.py
      test_override_resolver.py
```

## Notes

- Keep CLI code thin.
- Keep database access in repository modules.
- Keep parsing separate from ingestion.
- Keep override-chain/source resolution separate from parsing.
- Keep normalization and categorization testable independently.
- Use fixtures rather than real CK3 directories in automated tests.
- Add real path auto-detection only after explicit path options work.
- Final reports must consume canonical issue records, not raw logs.


---

# File: `docs/03_canonical_pipeline.md`

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


---

# File: `docs/04_multiphase_plan.md`

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


---

# File: `docs/05_definition_of_done.md`

# Definition of Done

Every agent task must satisfy this checklist unless the user explicitly waives an item.

## Required

1. Code implemented.
2. Tests added or updated.
3. CLI behavior demonstrated where relevant.
4. README or docs updated if user-facing behavior changed.
5. No unrelated files changed.
6. No large raw logs committed.
7. All outputs are deterministic.
8. Parser code remains side-effect-free.
9. CLI code does not contain raw SQL.
10. Missing optional CK3 logs are warnings, not fatal errors.
11. Production code goes under `root:repo/ck3chronicle/`.
12. Scratch artifacts go under `root:ck3raven_data/wip/ck3chronicle/`.
13. Final reports are generated from canonical issue records, not raw logs.

## For database tasks

- Schema initialization is idempotent.
- Schema version is recorded.
- Tests use a temporary SQLite database.
- Repository functions are used rather than direct SQL in command handlers.

## For parser/extractor tasks

- Parser accepts a file path or iterable of lines.
- Parser does not write to SQLite.
- Parser does not inspect Git.
- Parser does not copy files.
- Parser does not resolve override chains.
- Parser preserves raw evidence through hashes and samples.
- Normalization is conservative.
- Parser/extractor emits canonical issue records.
- New extractor tests include representative fixtures.

## For source/override resolver tasks

- Resolver consumes canonical issue records or file paths from issue records.
- Resolver does not parse raw logs.
- Resolver distinguishes winning file, referenced file, and probable cause.
- Resolver uses cautious language.
- Resolver includes confidence and reason where possible.

## For reporting tasks

- Reports do not dump full raw logs by default.
- JSON output is compact and stable.
- Markdown output is readable.
- Crash status is included when available.
- Ignored issues are hidden by default once ignore support exists.
- Reports consume canonical issue records.
- Reports include source/override enrichment only through resolver output.

## For workspace/context tasks

- Blame language is cautious.
- Confidence and reason are explicit.
- Referenced file and probable cause are not treated as the same thing.


---

# File: `docs/06_do_not_build.md`

# Do Not Build Yet

The following features are explicitly out of scope for MVP agent packets unless the user assigns them later.

Do not build:

- VS Code extension
- ck3lens sidebar integration
- MCP server
- background daemon
- autonomous repair
- direct mod file editing
- telemetry
- full crash dump parser
- CK3 static validator
- CWTools replacement
- CK3 Tiger replacement
- community web service
- cloud sync
- GUI application

## Also do not build

Do not create:

```text
raw error.log → one-off parser → custom final report
```

Do not let a parser:

- write final reports
- inspect Git
- resolve override chains
- decide patch recommendations
- mutate files

## Rationale

The initial goal is to create a reliable standalone CLI that preserves logs, detects crash evidence, parses issues into canonical issue records, and reports deltas.

Override-chain analysis, source context, and fixability ranking are important, but they must be layered on top of canonical issue records.


---

# File: `docs/07_data_model.md`

# Data Model

SQLite is the recommended MVP database.

## sessions

```text
session_id
started_at
ended_at
ingested_at
ck3_version
playset_name
mod_list_hash
mod_load_order_hash
git_branch
git_commit
git_dirty
crash_detected
crash_folder_id
parser_version
schema_version
```

## log_snapshots

```text
snapshot_id
session_id
log_name
source_path
retained_path
size_bytes
sha256
captured_at
```

## crash_folders

```text
crash_folder_id
session_id
source_path
folder_name
crash_timestamp
folder_hash
dump_present
readable_metadata_present
linked_by
confidence
```

## crash_artifacts

```text
artifact_id
crash_folder_id
source_path
retained_path
file_name
artifact_type
size_bytes
sha256
captured_at
```

Artifact types:

```text
copied_log
dump
metadata
exception
unknown
```

## issues

```text
issue_id
normalized_signature
normalization_version
first_seen_session_id
first_seen_at
category
severity
confidence
canonical_message
ignored
ignore_reason
ignore_created_at
```

## issue_occurrences

```text
occurrence_id
issue_id
session_id
log_name
raw_block_hash
raw_sample
occurrence_count
first_line_number
last_line_number
primary_file
primary_line
primary_symbol
call_stack_json
extracted_file_paths_json
created_at
```

## source_resolutions

```text
source_resolution_id
session_id
issue_id
file_path
winning_source_name
winning_source_type
winning_source_path
load_order_index
our_submod_override
override_chain_json
recently_modified
diff_vs_original_summary
diff_vs_predecessor_summary
confidence
reason
created_at
```

## fixability_assessments

```text
fixability_id
session_id
issue_id
score
severity_weight
regression_weight
crash_weight
our_submod_weight
recent_modification_weight
small_diff_weight
upstream_penalty
known_noise_penalty
recommendation
confidence
reason
created_at
```

## baselines

```text
baseline_id
name
session_id
created_at
description
```

## ignored_issues

```text
ignored_issue_id
issue_id
reason
created_at
expires_at
```

## schema_migrations

```text
version
applied_at
description
```

## Future tables

Later phases may add:

```text
workspaces
workspace_files
session_file_state
git_state
issue_file_links
external_validator_runs
issue_enrichments
repair_plans
repair_verifications
```


---

# File: `docs/08_cli_contract.md`

# CLI Contract

## MVP commands

```bash
ck3chronicle doctor
ck3chronicle ingest
ck3chronicle sessions
ck3chronicle report
ck3chronicle latest --json
```

## Standard options

The following options should be available where relevant:

```bash
--logs-dir <path>
--crashes-dir <path>
--archive-dir <path>
--db <path>
--config <path>
--format text|markdown|json
```

Tests should use explicit paths rather than relying on real CK3 directories.

## doctor

Checks environment and prints actionable status.

Should verify:

- logs dir exists if supplied
- crashes dir exists if supplied
- archive dir is writable or creatable
- database is writable or creatable
- schema version
- known logs present or absent
- product root is `root:repo/ck3chronicle/` when running in the ck3raven repo
- large artifact paths point to WIP/data locations, not repo paths

## ingest

Creates a session and snapshots evidence.

Should:

- copy configured logs
- hash logs
- record metadata
- detect crash folder
- inventory crash artifacts
- parse logs once parser exists
- store canonical issue records
- produce short summary

## sessions

Lists known sessions.

Suggested columns:

```text
session_id
ingested_at
logs_captured
crash_detected
unique_issues
```

## report

Shows latest session report by default.

Should include:

- session id
- captured logs
- missing logs
- crash detected yes/no
- crash folder linked yes/no
- unique issue count when parser exists
- top issues when parser exists

Important:

```text
report must consume canonical issue records
report must not parse raw logs directly
```

## latest --json

Outputs compact agent-friendly JSON.

Should avoid raw log dumps by default.

## Future source/context commands

```bash
ck3chronicle report --with-sources
ck3chronicle sources resolve
ck3chronicle suspects
ck3chronicle errors --file <path>
```


---

# File: `docs/09_testing_strategy.md`

# Testing Strategy

## Principles

1. Do not test against real CK3 user directories.
2. Use explicit fixture paths.
3. Use temporary SQLite databases.
4. Use small representative logs.
5. Include one stress-style test for repeated log spam.
6. Keep parser tests independent from database tests.
7. Keep override resolver tests independent from parser tests.
8. Test that reports consume canonical issue records, not raw logs.

## Fixture logs

Recommended fixtures:

```text
simple_error.log
multiline_script_error.log
repeated_error.log
localization_spam.log
database_conflicts.log
asset_graphics_errors.log
descriptor_errors.log
empty_error.log
huge_repeated_error.log
```

## Parser fixture cases

Include representative samples for:

- `jomini_script_system.cpp`
- `pdx_persistent_reader.cpp`
- duplicate localization key
- missing localization
- localization hash collision
- unknown trigger
- unknown effect
- failed context switch
- invalid database object
- duplicate texture
- missing mesh/icon
- invalid supported_version
- utf8-bom encoding warning

## Crash fixtures

Recommended crash fixture:

```text
crashes/
  ck3_20260531_014522/
    error.log
    game.log
    debug.log
    exception.txt
    dump.dmp
```

## Override resolver fixtures

Use small synthetic mod trees.

Recommended fixture shape:

```text
tests/fixtures/mods/
  base_game/
    common/scripted_effects/example.txt
  workshop_mod_a/
    common/scripted_effects/example.txt
  gambo_super_compatch/
    common/scripted_effects/example.txt
  gambo_ec724_submod/
    common/scripted_effects/example.txt
```

Test:

- single winner
- upstream-only winner
- our submod winner
- base-game winner
- override chain ordering
- diff summary vs original
- diff summary vs predecessor

## Test groups

### CLI tests

- commands load
- help works
- invalid options produce clear errors

### Database tests

- schema initializes idempotently
- session insert works
- log snapshot insert works
- crash folder insert works
- latest session retrieval works
- issue insert works
- source resolution insert works

### Ingest tests

- logs are copied
- missing logs are warnings
- hashes are recorded
- crash folder is inventoried
- session is persisted

### Parser tests

- single-line errors
- multi-line errors
- repeated errors cluster
- line-number variants cluster
- distinct meaningful IDs are not overcollapsed
- empty logs parse cleanly
- canonical issue schema is emitted

### Report tests

- report renders
- JSON is valid
- Markdown is valid enough to read
- raw logs are not dumped by default
- reports fail or warn if raw logs are passed directly instead of canonical issue records

### Source resolver tests

- resolver consumes issue/file data, not raw logs
- override chain is correct
- winning file is correct
- recommendation language is cautious


---

# File: `examples/sample_agent_json_report.json`

```json
{
  "schema_version": "ck3chronicle.report.v1",
  "session_id": "2026-05-31T01-45-22",
  "crash_detected": true,
  "comparison": {
    "mode": "previous_session",
    "new_issue_count": 3,
    "fixed_issue_count": 17,
    "worse_issue_count": 2,
    "improved_issue_count": 5,
    "ignored_issue_count": 31
  },
  "top_action_candidates": [
    {
      "file": "common/scripted_effects/TCT_scripted_effects.txt",
      "fixability_score": 91,
      "highest_severity": "High",
      "winning_source_name": "Gambo+EC724 Submod",
      "winning_source_type": "local_mod",
      "our_submod_override": true,
      "recently_modified": true,
      "recommendation": "Inspect/fix directly in our submod override.",
      "confidence": "High",
      "sample_issue": {
        "schema_version": "ck3chronicle.issue.v1",
        "category": "Script Execution",
        "message": "untyped trigger [ Scoped object of type 'character' is not valid ... ]",
        "primary_file": "common/scripted_effects/TCT_scripted_effects.txt",
        "primary_line": 275,
        "primary_symbol": "predict_new_cardinal"
      }
    }
  ]
}
```


---

# File: `examples/sample_latest_session_report.md`

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


---

# File: `templates/implementation_summary_template.md`

# Implementation Summary Template

## Summary

`<brief summary of what was implemented>`

## Files changed

```text
<file>
<file>
```

## Scratch files created, if any

```text
<file>
<file>
```

## Commands run

```bash
<command>
<command>
```

## Tests added or updated

```text
<test file>
<test file>
```

## Behavior demonstrated

```text
<example command/output summary>
```

## Canonical pipeline compliance

- [ ] Parser/extractor emits canonical issue records.
- [ ] Reports consume canonical issue records.
- [ ] Override/source resolution is separate from parsing.
- [ ] No final report is generated directly from raw logs.

## Known limitations

- `<limitation>`
- `<limitation>`

## Recommended next step

`<next agent packet or human review step>`


---

# File: `templates/reviewer_checklist.md`

# Reviewer Checklist

Use this checklist when asking a second agent or human to review a diff.

## Scope

- [ ] Did the implementation stay within the assigned task?
- [ ] Were unrelated files avoided?
- [ ] Were forbidden features avoided?
- [ ] Is product code under `root:repo/ck3chronicle/`?
- [ ] Are scratch artifacts under `root:ck3raven_data/wip/ck3chronicle/`?
- [ ] Were large logs/crash folders kept out of the repo?
- [ ] Is the behavior aligned with the MVP charter?

## Canonical pipeline

- [ ] Does parser/extractor output conform to canonical issue schema?
- [ ] Does reporting consume canonical issue records rather than raw logs?
- [ ] Is override-chain resolution separate from parsing?
- [ ] Are final recommendations generated by report/triage code rather than parser code?

## Code quality

- [ ] Is CLI code thin?
- [ ] Is DB access routed through repository functions?
- [ ] Is parser logic side-effect-free?
- [ ] Is normalization conservative?
- [ ] Are errors handled clearly?

## Tests

- [ ] Are tests present?
- [ ] Do tests use fixtures/temp paths?
- [ ] Do tests avoid real CK3 directories?
- [ ] Are missing logs handled as warnings?
- [ ] Are crash fixtures covered where relevant?
- [ ] Are canonical issue schema tests present where relevant?

## Output quality

- [ ] Are reports readable?
- [ ] Is JSON compact?
- [ ] Are raw logs capped or omitted by default?
- [ ] Is crash status included where relevant?
- [ ] Is confidence explicit for inferred claims?
- [ ] Is recommendation language cautious?

## Merge recommendation

- [ ] Merge
- [ ] Merge after minor fixes
- [ ] Do not merge yet

## Notes

`<review notes>`


---

# File: `templates/task_contract_template.md`

# Agent Task Contract Template

## Task name

`<short task name>`

## Goal

`<one sentence goal>`

## In scope

- `<item>`
- `<item>`
- `<item>`

## Out of scope

- `<item>`
- `<item>`
- `<item>`

## Product target files

```text
root:repo/ck3chronicle/<file path>
root:repo/ck3chronicle/<file path>
```

## Scratch target files, if needed

```text
root:ck3raven_data/wip/ck3chronicle/<path>
```

## Forbidden files unless explicitly approved

```text
root:repo/tools/ck3lens_mcp/**
root:repo/ck3lens/**
root:repo/ck3raven core enforcement/governance files
real CK3 log directories
Steam workshop directories
```

## Allowed commands

```bash
pytest
python -m ck3chronicle.cli --help
python -m ck3chronicle.cli doctor
```

## Acceptance criteria

- `<criterion>`
- `<criterion>`
- `<criterion>`

## Definition of done

- Code implemented.
- Tests added or updated.
- CLI behavior demonstrated where relevant.
- Docs updated if user-facing behavior changed.
- No unrelated files changed.
- No large raw logs committed.
- Outputs are deterministic.
- Final reports are generated from canonical issue records, not raw logs.

## Required final response from agent

- Summary of changes.
- Files changed.
- Tests run.
- Known limitations.
- Suggested next task.
