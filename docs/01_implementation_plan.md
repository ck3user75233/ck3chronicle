# ck3chronicle — Implementation Plan

> **Status:** Authoritative project governance. Companion to
> [00_project_charter.md](00_project_charter.md). The charter answers
> *"what are we building and why."* This plan answers *"how do we build it,
> phase by phase, with which agents, against which gates."*
>
> **Scope:** This document is governance, not code. It does **not** contain
> implementation. Implementation only begins on the user's signoff and only
> inside the phase being executed.
>
> **Created:** 2026-06-02

---

## 1. Relationship to the Charter

| Document | Answers | Audience |
|---|---|---|
| `00_project_charter.md` | Vision, hard boundaries, canonical pipeline, phase roadmap, ratified decisions | Every agent, every phase, public consumers |
| `01_implementation_plan.md` *(this)* | Per-phase task contracts, prototype promotion, branch/PR mechanics, kickoff order, reviewer process | Main agent (orchestrator), subagents, the user |

If the two documents ever disagree, the **charter wins** and this plan is
revised to match. Subagents receive expanded task contracts derived from
this plan; they do not improvise.

The roadmap is **12 phases (0–11)**. The first public/dev release ships after
the phase that delivers evidence preservation, canonical issues,
deltas/baselines, native playset import, override resolution, workspace
context, fixability ranking, and human + JSON reports. In this plan, that is
**Phase 6**.

---

## 2. Branch & PR Mechanics

### 2.1 Branch creation

- All ck3chronicle work happens on a dedicated branch: **`feature/ck3chronicle`**.
- Branch is cut from the current main development line **before Phase 0 begins**.
- The branch where this charter and plan were authored
  (`agent/fix-mcp-invoke-init`) is **not** the ck3chronicle branch.

### 2.2 PR cadence

- **One PR per phase.** Title: `ck3chronicle Phase N — <phase name>`.
- PR body must include:
  1. Phase task contract (link to the section below).
  2. Implementation summary written by the implementer subagent.
  3. Reviewer subagent's approval verdict, verbatim.
  4. Test command output (`pytest` summary line).
  5. End-to-end CLI demo transcript against fixture logs.
- If multiple PRs cannot be cleanly supported by tooling, the fallback is a
  single long-running branch with **phase-sized commits** plus the same
  per-phase reviewer approval gate. The gate is non-negotiable; the PR
  shape is negotiable.

### 2.3 What gets committed

- Product code under `root:repo/ck3chronicle/src/ck3chronicle/`.
- Tests under `root:repo/ck3chronicle/tests/` including tiny synthetic
  fixtures under `tests/fixtures/`.
- Docs under `root:repo/ck3chronicle/docs/`.
- `pyproject.toml`, `README.md`, license, etc.

### 2.4 What is forbidden from commits

- Real CK3 logs, real crash artifacts, real workshop content.
- Generated SQLite databases of any kind.
- Personal paths, machine-specific configs.
- Anything that lives in `root:ck3raven_data/wip/ck3chronicle/`.
- The existing `error analysis refactor/` prototype tree, after promotion
  (see Section 5) — it is removed once the relevant modules have been
  promoted and the prototype is no longer the source of truth.

---

## 3. Validation Gates (Actionable Checklist)

A phase is **not done** until every box below is checked. Reviewer subagent
rejects any PR missing any box.

```
[ ] Task contract in this plan was followed; no scope drift.
[ ] All new/modified Python lives under root:repo/ck3chronicle/.
[ ] No live code imports from `error analysis refactor/` (reference-only).
[ ] No new/edited Python files inside `error analysis refactor/`.
[ ] All filesystem paths obtained via `ck3chronicle.config` (no inline
    discovery, no hardcoded CK3 / Steam / mod / log paths outside config.py).
[ ] No real artifacts, large logs, or generated DBs committed.
[ ] All new tests pass under `pytest`.
[ ] No pre-existing tests regressed.
[ ] Canonical pipeline rule respected
    (no raw log → report shortcuts).
[ ] Parser boundary respected
    (no override resolution, no Git access, no analytics).
[ ] Override-resolver boundary respected
    (no raw-log parsing).
[ ] Report-composer boundary respected
    (no raw-log reads).
[ ] Native-Playset boundary respected
    (no reliance on ck3raven session.mods in core paths).
[ ] Stdlib-only dependency policy respected
    (or the deviation is explicitly approved by the user).
[ ] Implementation summary written.
[ ] End-to-end CLI demo against fixture logs passes.
[ ] Reviewer subagent approval recorded in the PR.
[ ] Human eyeballed the diff.
```

Static checks (pyright/pylance/etc.) are a signal; failure is a blocker only
when the failure is a real syntax/type/import problem.

---

## 4. Reviewer Process

### 4.1 Reviewer is a separate subagent invocation

The implementer subagent does **not** self-review. After implementation, the
main agent invokes a fresh subagent with the **reviewer task contract**:

- Task contract for the phase (from this plan).
- The diff.
- The validation checklist (Section 3).
- The boundary rules from charter §2.2 and §3.3.

### 4.2 Reviewer verdicts

The reviewer returns exactly one of:

- `APPROVE` — all checklist items pass; PR is ready.
- `REQUEST_CHANGES` — itemized list of failed checks, scoped to fixes.
- `REJECT` — the change violates a hard boundary; phase must be redone.

### 4.3 Grounds for `REJECT` (non-exhaustive)

- A raw log is parsed inside a report composer.
- The override resolver imports the log parser.
- Core code imports the ck3raven SDK adapter.
- Product code hardcodes or assumes `root:ck3raven_data/wip/` as a required path.
- Real CK3 artifacts committed.
- A new third-party dependency introduced without explicit user approval.
- A native-Playset-bypass: resolver gets its mod list from anywhere other
  than a `Playset` instance.
- Any product code or test under `src/ck3chronicle/` or `tests/` imports
  from `root:repo/ck3chronicle/error analysis refactor/...` (including
  `ck3chronicle_proto/`). That tree is reference-only (§5.3.1).
- Any new or edited Python file inside `error analysis refactor/`
  (apart from the eventual retirement PR per §5.1).
- Any CLI entrypoint, console script, or end-to-end demo executes a file
  living under `error analysis refactor/`.
- Path-resolution logic (OS-default discovery, scanning the user's home
  directory, reading `config.toml`, constructing `ROOT_*` paths from scratch,
  or hardcoding a CK3 / Steam / launcher / mod / log path inline) appears in
  any module other than `src/ck3chronicle/config.py`. All other modules
  must obtain paths via `ck3chronicle.config`.

---

## 5. Prototype Promotion Plan

The existing prototype lives at:

```
root:repo/ck3chronicle/error analysis refactor/ck3chronicle_proto/
```

Strategy is **promote + harden** (charter §10). Each prototype module has a
designated promotion target, a designated phase, and a harden checklist. No
module is promoted outside its phase.

| Proto module | Promotion target | Phase | Harden actions |
|---|---|---|---|
| `models.py` | `src/ck3chronicle/models/issue.py` (+ split as needed) | Phase 1 | Re-anchor on canonical schema; add schema version; dataclass invariants; tests. |
| `log_parser.py` | `src/ck3chronicle/parser/ck3_error.py` | Phase 1 | Enforce parser boundary (no resolution, no Git, no analytics); fixture-driven tests for each error shape. |
| `normalizers.py` | `src/ck3chronicle/parser/normalize.py` | Phase 1 | Whitelist-only volatile masking (charter §12 #2); deterministic signatures; tests asserting cluster stability. |
| `issue_aggregator.py` | Split: clustering → `parser/normalize.py`; delta → `analysis/delta.py` | Phase 1 (clustering) / Phase 2 (delta) | Decouple clustering from delta; remove any direct report emission. |
| `paths.py` | `src/ck3chronicle/config.py` (+ harvester helpers) | Phase 0 | Replace any hardcoded user paths with config / env discovery; no machine-specific defaults committed. |
| `override_resolver.py` | `src/ck3chronicle/analysis/override_resolver.py` (consumes `playset/`) | Phase 4 | Rebuild on top of the native `Playset` (Phase 3); strip any SDK assumptions; introduce `SourceInstance` / `SourceResolution`. |
| `fixability.py` | `src/ck3chronicle/analysis/fixability.py` | Phase 6 | Confidence is explicit; crash-adjacency rule per charter §12 #5; recommendation language follows charter §2.3 wording discipline. |
| `reports.py` | `src/ck3chronicle/reporting/terminal.py`, `reporting/markdown.py`, and `reporting/json_report.py` | Phase 2 (initial human + minimal JSON) / Phase 6 (recommendations) | Hard split reporting surfaces; report composer reads canonical records only; no raw-log access. |
| `sdk_adapter.py` | `src/ck3chronicle/sdk_adapter.py` **and** `src/ck3chronicle/playset/importers.py` (adapter mode) | Phase 3 | Becomes optional adapter that produces a ck3chronicle `Playset`. Cannot be imported by core parser / resolver / report code. |
| `cli_error_analysis.py` | Reference only — **rewritten** as `src/ck3chronicle/cli.py` | Phase 0 (skeleton) → grows each phase | Argparse subcommand structure; each phase adds its subcommand(s); no business logic in `cli.py`. |
| `__init__.py` | `src/ck3chronicle/__init__.py` | Phase 0 | Version constant; public surface declaration. |

### 5.1 Prototype removal

The `error analysis refactor/` tree is removed only after all promoted modules
pass Phase 6 release-gate tests and the all-in-one prototype behavior is
covered by fixtures. At that point, remove the prototype in a small follow-up
PR titled `ck3chronicle: retire prototype tree`. Until then it stays put for
reference; it must not be edited.

### 5.2 Rewrite rule

A module is **rewritten from scratch** (not promoted) only if the implementer
or reviewer documents a concrete reason in the phase's implementation
summary (e.g. unsalvageable boundary violation, dead code, wrong abstraction).
"Style preference" is not a reason.

### 5.3 Heritage Assets Registry

In addition to the `ck3chronicle_proto/` modules promoted in Section 5, the
project has two adjacent heritage assets that **must** be referenced by the
phases below. They are not optional inspiration; they are required inputs.

| Asset | Path | Required by | Why |
|---|---|---|---|
| **Refactor design spec** | `root:repo/ck3chronicle/error analysis refactor/ck3chronicle_modular_refactor_all_in_one (1).md` | Phase 1, Phase 2, Phase 4, Phase 6 | Canonical-pipeline spec; codifies "CURRENT WINNING FILE" wording change and modular split rationale. |
| **Legacy report output example** | `root:repo/ck3chronicle/error analysis refactor/error_file_analysis - OUTPUT EXAMPLE.txt` | **Phase 2** and **Phase 6** | Reference report shape to **emulate and improve upon** (sections, columns, override-chain block, stale-patch warnings, sample-error dedup, cautious recommendation tone). |
| **Pre-modular prototype scripts** | `root:repo/ck3chronicle/error analysis refactor/error analysis prototype/` (`analyze_error_files.py`, `parse_script_errors.py`, `setup_error_analysis_toolkit.py`, `README.md`) | Phase 1, Phase 2, Phase 6 | "Best of the rest" of the WIP error parsers; captures category clustering, per-file deep-dive workflow, stale-patch detection heuristics, and sample-message dedup limits. |
| **Launcher import / JSON export** | `root:repo/tools/ck3lens_mcp/server.py` — function `_ck3_playset_internal` (command `"import"`), lines ~3795–4130 | **Phase 3** | Working SQLite reader for `launcher-v2.sqlite` and JSON writer with established schema. Cleanly extractable per Phase 3 contract. |
| **Legacy converter reference** | `root:repo/archive/deprecated_scripts/convert_launcher_playset.py` | Phase 3 (reference only) | Older playset converter; informative but deprecated. |

Reviewer subagent **must** confirm the relevant heritage assets were read
before approving the phases marked above. If a phase does not reference its
required assets, the verdict is `REQUEST_CHANGES`.

#### 5.3.1 Reference-only constraint (HARD)

The entire `root:repo/ck3chronicle/error analysis refactor/` tree is
**reference-only source material**. It is treated as documentation, not as a
runnable subpackage of ck3chronicle.

The following are **all** prohibited:

- Importing from `error analysis refactor/...` in any product code under
  `src/ck3chronicle/`.
- Importing from `error analysis refactor/...` in tests under `tests/`.
- Adding, editing, or moving Python files inside
  `error analysis refactor/` (apart from the eventual retirement PR per §5.1).
- Wiring any CLI entrypoint, console script, or PR demo to a file living
  under `error analysis refactor/`.
- Reading data files from `error analysis refactor/` at runtime.

Promotion is the **only** sanctioned path for that code: copy or rewrite the
relevant logic into the correct `src/ck3chronicle/...` module per the
Section 5 promotion table, harden it under the canonical-pipeline and
boundary rules, and add fixture-based tests under `tests/`. Live code lives
in `src/ck3chronicle/` and only in `src/ck3chronicle/`. The same rule
applies to `ck3chronicle_proto/` — it is reference material, not a runtime
package.

---

## 6. Test & Fixture Strategy (Operational)

### 6.1 Directory shapes

```
root:repo/ck3chronicle/tests/
  test_*.py
  fixtures/
    logs/
      minimal/
        error.log
        game.log
      with_crash/
        error.log
        game.log
        crash/
          dump_metadata.txt
      noisy_localization/
        error.log
      database_conflicts/
        database_conflicts.log
    crashes/
      sample_crash_folder/
        ...
    mods/
      synthetic_root/
        base_game/
          common/...
        workshop/
          1000001/
            common/...
        local/
          MySubmod/
            common/...
    playsets/
      minimal.json
      with_overrides.json
      launcher_export_sample.json
    db/
      schema_reference.sql
```

```
root:ck3raven_data/wip/ck3chronicle/
  real_logs/                  # real CK3 logs, gitignored
  real_crashes/               # real crash folders, gitignored
  dev_dbs/                    # dev SQLite DBs, gitignored
  spikes/                     # exploratory scripts, gitignored
  reports/                    # generated reports for manual review
```

### 6.2 Fixture rules

- Each fixture is **as small as possible** to exercise its specific behavior.
- No personal paths, no real character / mod identifiers tied to a real user.
- Fixtures are referenced by tests via `pathlib.Path(__file__).parent / "fixtures" / ...`.
- A fixture-change PR that is not tied to a test change is rejected.

### 6.3 Test naming

- `test_<module>_<behavior>.py::test_<scenario>`
- One assertion per behavior; descriptive ids over magic numbers.

---

## 7. Per-Phase Task Contracts

Each contract has a fixed shape: **Goal**, **Target paths**, **Out of scope**,
**Acceptance tests**, **Definition of done**, **Review checklist additions**.
The contracts below are seed contracts for the full **12-phase roadmap (0–11)**;
the main agent expands each into a full launch packet (with concrete file
lists, command transcripts, and demo script) immediately before invoking the
implementer subagent.

---

### Phase 0 — Evidence Preservation and Session Registry

**Subagent shape:** implementer → reviewer.

**Goal.** Ship the package skeleton plus the ability to snapshot a set of CK3
logs and a crash folder into durable local storage, recording session
metadata in SQLite.

**Sub-goal — central configuration.** Phase 0 establishes
`src/ck3chronicle/config.py` as the **single source of truth** for all
filesystem locations. Every other module in every later phase obtains paths
by reading constants/getters from this module — never by reimplementing
OS-default discovery, scanning the user's home directory, or
hardcoding paths inline.

Required ROOT constants (loaded by `config.py`, exposed as module-level
`Path` objects or `get_*()` callables):

| Constant | Meaning | Default discovery |
|---|---|---|
| `ROOT_GAME` | CK3 install (`.../Crusader Kings III/game`) | OS-default Steam path; override via config. |
| `ROOT_STEAM` | Steam Workshop content root (`.../workshop/content/1158310`) | OS-default Steam path; override via config. |
| `ROOT_LOCAL_MODS` | User's Paradox local mods folder (`.../Documents/Paradox Interactive/Crusader Kings III/mod`) | OS-default Documents path; override via config. |
| `ROOT_LOGS` | CK3 runtime logs folder (`.../Crusader Kings III/logs`) | OS-default Documents path; override via config. |
| `ROOT_WIP` | User scratch / dev artifacts root for ck3chronicle | Defaults to `<ROOT_CK3CHRONICLE>/wip`; override via config. |
| `ROOT_CK3CHRONICLE` | ck3chronicle's own data root (DB, archived evidence, generated reports) | OS-default per-user data dir (e.g. `%LOCALAPPDATA%/ck3chronicle` on Windows, `~/.local/share/ck3chronicle` on Linux/Mac); override via config. |

**User config file.** Phase 0 introduces a single user-editable config file
(stdlib-only formats; TOML via `tomllib` preferred, JSON fallback) at:

```
<ROOT_CK3CHRONICLE>/config.toml   (default location)
```

The file is created with sensible OS-default values on first `doctor` /
`ingest` run if missing. Every ROOT constant may be overridden by the user
editing this file. **No environment variables** are required for normal
operation (env-var overrides may be added later if needed).

**Target paths.**
- `src/ck3chronicle/__init__.py`
- `src/ck3chronicle/cli.py`         (argparse skeleton + `ingest`, `sessions`, `doctor`)
- `src/ck3chronicle/config.py`
- `src/ck3chronicle/doctor.py`
- `src/ck3chronicle/harvester.py`
- `src/ck3chronicle/ingest.py`
- `src/ck3chronicle/db/schema.py`
- `src/ck3chronicle/db/migrations.py`
- `src/ck3chronicle/db/repository.py`
- `pyproject.toml`, `README.md` (stub)
- `tests/test_cli.py`, `tests/test_db.py`, `tests/test_harvester.py`
- `tests/fixtures/logs/minimal/`, `tests/fixtures/logs/with_crash/`

**Out of scope.**
- Parsing log contents into issues (Phase 1).
- Deltas, baselines, ignores (Phase 2).
- Playset model (Phase 3).
- Override resolution (Phase 4).
- Any report richer than `sessions` listing.

**Acceptance tests.**
- `ck3chronicle ingest --logs <fixture>` creates a new session row and
  copies/hashes log files into durable storage.
- `ck3chronicle sessions` lists the new session with timestamp, log count,
  total bytes, crash flag.
- `ck3chronicle doctor` reports paths, Python version, SQLite version,
  durable-storage status.
- `ck3chronicle doctor` prints the resolved value of every `ROOT_*`
  constant and the path to the active `config.toml`. If the config file is
  missing, `doctor` creates it with OS-default values and reports that it
  did so.
- Every `ROOT_*` constant has a passing unit test for: (a) OS-default
  discovery, (b) user override via config file.
- Re-running `ingest` against an evidence bundle with identical captured log
  hashes and identical crash-artifact hashes does not create a duplicate
  session by default. The command reports that the bundle is already ingested
  and returns the existing session ID.
- A `--force` / `--allow-duplicate` policy may be provided for tool-debugging
  scenarios.
- The same normalized issue signatures appearing in a later distinct evidence
  bundle are recorded in that new session (time-series tracking preserved).

**Definition of done.**
- All Phase 0 acceptance tests pass.
- `pytest` green.
- End-to-end CLI demo against `tests/fixtures/logs/with_crash/` recorded
  in PR body.
- Package installable via `pip install -e .` from `root:repo/ck3chronicle/`.

**Review checklist additions.**
- No log content is parsed yet (Phase 1's job).
- No CK3-version string is hardcoded.
- `config.py` is the only module that performs OS-default path discovery,
  reads `config.toml`, or constructs ROOT paths from scratch. All other
  modules import the ROOT constants/getters from `ck3chronicle.config`.

---

### Phase 1 — Canonical Issue Records and Error Clustering

**Subagent shape:** test-designer → implementer → reviewer.

**Goal.** Parse harvested logs into canonical issue records and cluster them
by signature.

**Target paths.**
- `src/ck3chronicle/models/issue.py`
- `src/ck3chronicle/parser/ck3_error.py`
- `src/ck3chronicle/parser/normalize.py`
- `src/ck3chronicle/parser/categorize.py`
- `src/ck3chronicle/db/schema.py` (extend; migration)
- `src/ck3chronicle/cli.py` (`parse` subcommand)
- `tests/test_parser.py`, `tests/test_normalize.py`
- `tests/fixtures/logs/{noisy_localization,database_conflicts,...}`

**Out of scope.**
- Comparison across sessions (Phase 2).
- Source resolution (Phase 4).
- Recommendations (Phase 6).

**Acceptance tests.**
- Multi-line script error parsed as one issue with intact location info.
- 50 occurrences of the same localization error cluster to one issue with
  `occurrences = 50`.
- Volatile masking is whitelist-only (charter §12 #2): line numbers and
  `args#NNN` masked; semantic IDs / names preserved.
- Confidence and severity assigned per the categorizer rules; explicit
  fixture covers each category. The Phase 1 categorizer must consult the
  pre-modular prototype's category set in
  `error analysis prototype/parse_script_errors.py` (heritage asset, §5.3)
  as the baseline taxonomy, and document any additions, removals, or merges
  in the implementation summary.
- `ck3chronicle parse --session N` populates the canonical tables.

**Definition of done.** Charter §3 boundaries respected; checklist green;
issue schema documented in `db/schema.py` docstring.

**Review checklist additions.**
- `parser/` never imports `analysis/`, `playset/`, `reporting/`, or `sdk_adapter`.
- Signature determinism: same input → same signature across runs.

---

### Phase 2 — Delta Reports, Baselines, and Noise Management

**Subagent shape:** implementer → reviewer.

**Goal.** Compare sessions, manage baselines, suppress ignored issues, and
emit first usable human and minimal JSON reports.

**Target paths.**
- `src/ck3chronicle/analysis/delta.py`
- `src/ck3chronicle/analysis/baseline.py`
- `src/ck3chronicle/db/schema.py` (baselines, ignores)
- `src/ck3chronicle/reporting/terminal.py`
- `src/ck3chronicle/reporting/markdown.py` (basic)
- `src/ck3chronicle/reporting/json_report.py` (minimal)
- `src/ck3chronicle/cli.py` (`report`, `report --json`, `diff`,
  `baseline create`, `baseline list`, `ignore add`, `ignore list`)
- `tests/test_delta.py`, `tests/test_report.py`

**Out of scope.** Playset, resolver, fixability, JSON contracts, trends.

**Acceptance tests.**
- Two synthetic sessions produce a delta with new / fixed / worse / improved
  buckets matching expectations.
- Named baselines (arbitrary strings) can be created, listed, and used as
  a diff base.
- Ignored issues are suppressed from `report` output but still present in
  the DB.
- `report --markdown` produces deterministic Markdown for a fixed input.
- `report --json` emits deterministic minimal JSON for a fixed input (pre-release baseline shape; formal contract versioning comes in Phase 7).
- Human report **emulates and improves upon** the legacy shape in
  `error_file_analysis - OUTPUT EXAMPLE.txt` (heritage asset, §5.3):
  ranked impacted-files table, per-file deep dive section header pattern,
  cautious recommendation tone. "ERRORS OWNED BY" wording is forbidden;
  use "CURRENT WINNING FILE". Override-chain block is deferred to Phase 4
  (the resolver phase) — Phase 2's human report may stub that section.

**DoD.** Report composer reads only canonical records — never logs.

---

### Phase 3 — Native Playset Model and Import

**Subagent shape:** test-designer → implementer → reviewer.

**Goal.** Implement the native `Playset` / `PlaysetMod` model and the
importers that populate it. **No core resolver, parser, or report code may
reference ck3raven session/SDK state.**

The native `Playset` is the production source model. The source/override
resolver must consume a `Playset` instance in normal operation. Filesystem
fixture providers are test doubles (or standalone fixture utilities);
ck3raven SDK/session adapters may produce a `Playset`, but may not replace the
`Playset` abstraction.

**Target paths.**
- `src/ck3chronicle/playset/model.py`     (`Playset`, `PlaysetMod`,
                                          `ModSourceType` enum)
- `src/ck3chronicle/playset/importers.py` (manual dict, JSON, launcher export)
- `src/ck3chronicle/playset/launcher.py`  (Paradox launcher DB / export reader)- `src/ck3chronicle/playset/search.py`    (find a game-relative path across
                                          mods in load order)
- `src/ck3chronicle/db/schema.py`         (playsets, playset_mods)
- `src/ck3chronicle/cli.py`               (`playset import`, `playset list`,
                                          `playset show`)
- `tests/test_playset.py`
- `tests/fixtures/playsets/{minimal,with_overrides,launcher_export_sample}.json`
- `tests/fixtures/mods/synthetic_root/...`

**Out of scope.**
- Override-chain analysis on parsed issues — that's Phase 4.
- ck3raven SDK adapter — that's a Phase 3 *optional* deliverable and may be
  deferred to Phase 4 if time-pressed, but the **adapter boundary** must be
  reserved (i.e. the seam exists, importable from `sdk_adapter.py`).

**Acceptance tests.**
- Manual `Playset` construction round-trips through DB save/load.
- JSON importer loads a fixture into a `Playset` with correct load order
  and source types.
- Launcher-export importer parses the sample fixture.
- `playset/search.py` correctly identifies all file instances of a
  game-relative path and the load-order-winning file instance for a simple
  LIOS-style fixture. Directory-specific and symbol-level conflict behavior is
  deferred unless explicitly modeled and tested.
- `playset/launcher.py` is **derived from** the working launcher importer at
  `root:repo/tools/ck3lens_mcp/server.py::_ck3_playset_internal` (command
  `"import"`, lines ~3795–4130), per §5.3.
  - Lift the SQLite read logic (open `launcher-v2.sqlite` read-only via URI;
    join `playsets` → `playsets_mods` → `mods`; extract position, enabled,
    displayName, steamId, dirPath, source) as the starting point.
  - Lift the JSON schema/shape (vanilla block, mods list with load_order,
    local_mods_folder, metadata) as the starting point.
  - **Decouple from ck3raven**: replace the `ROOT_USER_DOCS`, `ROOT_STEAM`,
    `ROOT_GAME` constants with ck3chronicle `ROOT_*` constants imported from
    `ck3chronicle.config` (Phase 0); accept overrides as function/constructor
    parameters for tests; do NOT add new path-discovery logic in
    `playset/launcher.py`. Replace the MCP tool wrapper with a pure function;
    drop any agent_briefing / sub_agent_config fields that are ck3raven-only;
    remove SDK-specific assumptions.
  - The extracted function must work standalone (no MCP, no ck3raven
    imports) and must return a ck3chronicle `Playset` instance (not a raw
    dict) when consumed in-process.
- No `playset/` module imports `parser/`, `analysis/`, `reporting/`, or
  `sdk_adapter`.

**DoD.**
- `Playset` is the **only** mod-list abstraction in the codebase.
- Charter §3.3 boundary is enforced by import structure.

**Review checklist additions.**
- Grep for `session.mods`, `ck3raven`, `mcp_ck3` inside `src/` returns
  matches only in `sdk_adapter.py`.

---

### Phase 4 — Source and Override-Chain Resolver

**Subagent shape:** test-designer → implementer → reviewer.

**Goal.** Enrich canonical issue records with source/override context,
resolving against a `Playset`.

**Target paths.**
- `src/ck3chronicle/analysis/override_resolver.py`
- `src/ck3chronicle/models/` (`SourceInstance`, `SourceResolution`)
- `src/ck3chronicle/db/schema.py` (resolutions table)
- `src/ck3chronicle/cli.py` (`resolve`, `report --with-sources`)
- `tests/test_override_resolver.py`

**Out of scope.** Recommendations (Phase 6); workspace/Git correlation (Phase 5).

**Acceptance tests.**
- Given a canonical issue referencing `common/traits/00_traits.txt` and a
  fixture playset with three mods overriding it, the resolver returns the
  correct winning instance and full chain, in order.
- Our-submod status is correctly flagged when the winner belongs to a mod
  marked as the user's submod.
- Resolver never opens a raw log file.

**DoD.** Charter §2.2 resolver boundary holds; tests cover the four
common load-order shapes (vanilla-only, single-mod, two-mod overlap,
n-mod chain).

---

### Phase 5 — Workspace Context and Likely-Cause Analysis

**Subagent shape:** test-designer → implementer → reviewer.

**Goal.** Capture workspace roots, Git state, recently modified files;
correlate to canonical issues to identify likely culprits.

**Target paths.**
- `src/ck3chronicle/context/workspace.py`
- `src/ck3chronicle/context/correlation.py`
- `src/ck3chronicle/db/schema.py` (workspace_snapshots)
- `src/ck3chronicle/cli.py` (`context capture`, `report --with-context`)
- `tests/test_workspace.py`

**Acceptance tests.**
- Synthetic workspace + Git history fixture produces a snapshot with
  recently modified files.
- Correlation engine surfaces an issue → recently-modified-file link with
  explicit confidence label.

**DoD.** Git access lives only in `context/`; no other module shells out
to `git`.

---

### Phase 6 — Fixability Ranking and Recommendation Report **(first release)**

**Subagent shape:** test-designer → implementer → reviewer.

**Goal.** Rank actionability; produce recommendation text with explicit
confidence. **End of this phase is the first public/dev release per charter §6.**

**Target paths.**
- `src/ck3chronicle/analysis/fixability.py`
- `src/ck3chronicle/reporting/markdown.py` (extend)
- `src/ck3chronicle/reporting/terminal.py` (extend)
- `src/ck3chronicle/cli.py` (`report --recommendations`, `latest`)
- `tests/test_fixability.py`

**Acceptance tests.**
- Fixability scores are reproducible for identical inputs.
- Crash-adjacent boost matches charter §12 #5 (N=25, copied-into-crash,
  crash-metadata).
- Recommendation wording follows charter §2.3 (`Recommendation
  (confidence: medium): inspect ...`, never `Fix: edit ...`).
- A combined end-to-end demo from `ingest` to `report --recommendations`
  succeeds against the with-crash fixture and a 2-mod playset.
- Final human report **fully realizes** the heritage report shape (§5.3,
  legacy `error_file_analysis - OUTPUT EXAMPLE.txt`): ranked impacted-files
  table, per-file override chain (load order indices, winning mod, sample
  errors capped at 5 unique), stale-patch warnings where applicable,
  cautious recommendation phrasing ("consider…", "inspect…", "assess…",
  never "Fix:"). Improvements over the legacy shape are explicitly noted in
  the implementation summary.

**DoD (release gate).**
- All charter §6 capabilities work end-to-end on fixtures.
- `README.md` updated for first-release usage.
- `pyproject.toml` version bumped to `0.1.0`.

---

### Phase 7 — Agentic Query Layer

**Subagent shape:** implementer → reviewer.

**Goal.** Formalize stable, versioned JSON contracts for agent consumers on top
of the minimal JSON introduced before release.

**Target paths.**
- `src/ck3chronicle/contracts/agent_json.py`
- `src/ck3chronicle/cli.py` (`latest --json`, `report --json`)
- `tests/test_agent_json.py`
- `tests/fixtures/contracts/*.json` (golden samples)

**Acceptance tests.**
- JSON outputs validate against an in-repo schema.
- Schema version is present in every payload.

---

### Phase 8 — Cross-Run Analytics and Trend Intelligence

**Subagent shape:** test-designer → implementer → reviewer.

**Goal.** Multi-session trends and recurring-issue history.

**Target paths.**
- `src/ck3chronicle/analysis/trends.py` (new)
- `src/ck3chronicle/cli.py` (`trends`, `history`)
- `tests/test_trends.py`

---

### Phase 9 — IDE and ck3lens Integration

**Subagent shape:** implementer → reviewer.

**Goal.** Optional VS Code / ck3lens integration wrappers. **Strictly
optional and never required by core code paths.**

Phase 9 is the only phase that may target ck3lens/MCP paths outside
`root:repo/ck3chronicle/`, and only under a separately approved integration
task contract.

**Target paths.**
- `src/ck3chronicle/integrations/vscode.py`
- `src/ck3chronicle/integrations/ck3lens.py`
- (Optional) MCP wrapper artifacts under
  `root:repo/tools/ck3lens_mcp/` — coordinated separately with ck3lens.

---

### Phase 10 — Static Validator and Script-Docs Cross-Reference

**Subagent shape:** test-designer → implementer → reviewer.

**Goal.** Cross-reference issues against CK3 script docs / known signatures.

**Target paths.**
- `src/ck3chronicle/analysis/static_validator.py`
- `src/ck3chronicle/data/` (curated signatures; no scraped third-party docs
  in repo without license check)

---

### Phase 11 — Guided Repair Support

**Subagent shape:** implementer → reviewer.

**Goal.** Read-only repair scaffolding; suggested-edit composition. **No
autonomous mutation.**

**Target paths.**
- `src/ck3chronicle/repair/suggestions.py`
- `src/ck3chronicle/cli.py` (`suggest`, `suggest --apply` disabled)

---

## 8. First Kickoff Order

Upon user signoff of charter + this plan:

1. **Main agent** creates the `feature/ck3chronicle` branch off the current
   main line.
2. **Main agent** writes the Phase 0 launch packet:
   - Expands the Phase 0 task contract with concrete files, expected
     `pyproject.toml` minimal contents (stdlib-only), the
     `tests/fixtures/logs/minimal/` synthetic log shape, and the demo
     script transcript shape.
3. **Main agent** invokes the **implementer subagent** with that packet.
4. **Main agent** receives the implementer's diff + summary; invokes the
   **reviewer subagent** with the validation checklist (Section 3) and the
   Phase 0 contract.
5. On `APPROVE`: PR is opened; user reviews; phase closed; Phase 1 launch
   packet drafting begins.
6. On `REQUEST_CHANGES`: implementer subagent is re-invoked with the
   reviewer's itemized list.
7. On `REJECT`: the phase is redone after the main agent diagnoses the
   boundary violation and updates this plan if the contract was at fault.

---

## 9. Plan Maintenance

- This plan is updated when (a) the charter changes, or (b) a phase
  encounters a reality the contract did not anticipate.
- Changes to this plan that are not pure clarifications require the same
  review treatment as a phase: the main agent prepares the diff, the user
  approves.
- The plan is not a snapshot. It is a living governance document; treat
  changes to it with the same care as changes to the charter.

---

## 10. Out-of-Scope (This Document)

This plan does **not**:

- Write any code.
- Move any prototype files.
- Create the `feature/ck3chronicle` branch.
- Modify `pyproject.toml`, `src/`, or any product file.

Those actions begin only after explicit user signoff and only inside the
phase being executed.

---

## 11. Source Documents

- [00_project_charter.md](00_project_charter.md) — vision and boundaries
  (authoritative).
- `ck3chronicle_agent_kickoff_v2/agent_prompts/` — authoritative prompt
  outlines (seed material for task-contract expansion).
- `error analysis refactor/ck3chronicle_proto/` — prototype to be
  promoted per Section 5.
- The user's authoritative decisions on 2026-06-02 — already baked into
  the charter and reflected here.
