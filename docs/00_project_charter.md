# ck3chronicle — Project Charter

> **Status:** Authoritative. This document is the single source of truth for the
> ck3chronicle project. Every agent — planner, test-designer, implementer,
> reviewer — reads this first. It consolidates the kickoff vision with the
> user-ratified decisions on topology, structure, dependencies, gating, and
> boundaries.
>
> **This document is not the implementation plan.** A separate implementation
> plan will be drafted next, derived from this charter.
>
> **Created:** 2026-06-02

---

## 1. Vision & Scope

**ck3chronicle** is a standalone Python CLI tool for preserving, parsing, and
triaging Crusader Kings III runtime logs and crash evidence. It addresses a
concrete pain felt by CK3 modders: **CK3 logs are volatile and are overwritten
or replaced across launches, sessions, and crashes**, so by the time you sit
down to debug a problem, the evidence may already be gone.

By archiving each play session's logs and crash evidence into a local SQLite
database, ck3chronicle unlocks **time-series analysis** of mod behavior — what
errors are new, what's been fixed, what's regressed, what's likely to blame —
and produces deterministic, agent-friendly reports that can drive ongoing
patch and mod-development work in any context (human, IDE, agent).

### Product promise (MVP)

> After each CK3 run, ck3chronicle tells you what changed, what matters,
> whether the game crashed, and which recent or winning files are most likely
> involved.

### Target users

CK3 modders working with non-trivial playsets — compatch authors, submod
maintainers, total-conversion teams, and gameplay-overhaul teams. The tool
is built for environments where mods interact in unpredictable ways and
where reproducible error triage is essential.

### Public release intent

ck3chronicle is intended for **public release**. The first public/dev release
ships after **Phase 5** (see Section 6). Earlier phases must keep the door
open for a clean public release: portable dependencies, no MCP coupling in
core, no private paths in fixtures, no real user logs committed.

---

## 2. Architectural Principles

### 2.1 The canonical pipeline (hard rule)

All evidence flows through one canonical pipeline:

```
raw CK3 logs
  → harvester (snapshot raw evidence to durable local storage; record
                hashes/metadata in SQLite)
  → parser/extractors (emit canonical issue records)
  → normalizer (cluster by signature/category/severity/confidence)
  → database (sessions, issues, occurrences, crash artifacts)
  → delta engine (compare sessions and baselines)
  → source/override resolver (enrich with winning-file context, using the
                              native Playset model)
  → fixability engine (rank actionability)
  → report composer (human/agent output)
```

**Final reports must be generated from canonical issue records, never
directly from raw logs.** This is the single most important architectural
constraint in the project.

**Allowed:**

```
raw log → parser/extractor → canonical issue records → report composer
```

**Forbidden:**

```
raw log → one-off parser → custom final report
```

If a phase or agent finds itself wanting to parse `error.log` inline to
produce report content, it is doing the wrong thing. The fix is to extend the
canonical schema and the parser, not to short-circuit the pipeline.

### 2.2 Three separable engines

The canonical pipeline factors into three engines with strict boundaries:

#### Parser / extractor
**May:** read log text, split timestamped blocks, extract messages,
extract locations and call stacks, classify category / severity / confidence,
emit canonical issue records.
**May not:** write final reports, inspect Git, resolve override chains,
decide recommendations, mutate files, write directly to the production
database except when called by the ingest layer.

#### Source / override resolver
**May:** consume canonical issue records or file paths, resolve source
instances, determine the winning file, build override chains, identify our
submod status, compute diff summaries, emit `SourceResolution` records.
**May not:** parse raw logs.

#### Report composer
**May:** consume canonical issue records, source resolutions, delta /
baseline data, and fixability scores; produce terminal / Markdown / JSON
output.
**May not:** read raw logs directly.

These three boundaries are non-negotiable. Reviewers must reject any change
that crosses them.

### 2.3 Wording discipline

ck3chronicle reports are **evidence-based, not authoritative**. Use cautious
language:

| ❌ Avoid | ✅ Prefer |
|---|---|
| `ERRORS OWNED BY` | `CURRENT WINNING FILE` |
| `<mod> is causing X` | `<mod> wins file X; issue Y references file X` |
| `Fix: edit Z` | `Recommendation (confidence: medium): inspect Z` |

Confidence is always explicit (`high` / `medium` / `low`) and surfaced in the
report.

---

## 3. Hard Boundaries

### 3.1 Product / WIP boundary

| Location | What goes here |
|---|---|
| `root:repo/ck3chronicle/` | **Product code only.** Source, tests, docs, fixtures (tiny synthetic). |
| `root:ck3raven_data/wip/ck3chronicle/` | **All scratch.** Real logs, real crash artifacts, generated reports, SQLite databases under development, exploratory parser spikes. |

**No large logs, real user logs, real crash artifacts, Steam Workshop files,
private local paths, or generated databases are ever committed to the repo.**

Test fixtures committed to the repo must be tiny, synthetic, and curated
specifically to exercise a known parser/resolver/report behavior.

### 3.2 MCP / extension independence

The MVP must work **without** the ck3raven MCP server and without the
VS Code extension. The CLI is the product. MCP integration is an optional
later phase; optional ck3raven SDK integration is supported but never
required for core operation.

### 3.3 Native Playset Independence

ck3chronicle must own a native `Playset` / `PlaysetMod` model. Core source
and override resolution must operate against `playset.mods`, **not** against
ck3raven `session.mods`, MCP resolution, or ck3raven SDK state.

ck3raven SDK integration is an **optional adapter only**. It may export or
convert ck3raven session data into a ck3chronicle `Playset`, but no core
resolver, parser, report, or MVP workflow may require ck3raven to be running.

The intended flow:

```
manual / launcher / JSON playset import
  → ck3chronicle Playset
  → playset.mods
  → native source/override resolver
```

And, only as an optional adapter path:

```
ck3raven session.mods
  → adapter/export
  → ck3chronicle Playset
```

---

## 4. Package & Repo Layout

ck3chronicle is an **independent package** inside the ck3raven monorepo, with
its own `pyproject.toml`. This preserves the standalone-CLI promise, keeps
the public-release path open, and avoids unnecessary MCP coupling, while
still allowing ck3raven agents to develop it in-place.

```
root:repo/ck3chronicle/
  pyproject.toml
  README.md
  src/
    ck3chronicle/
      __init__.py
      cli.py
      config.py
      doctor.py
      harvester.py
      ingest.py
      db/
        schema.py
        migrations.py
        repository.py
      parser/
        ck3_error.py
        normalize.py
        categorize.py
      models/
        issue.py
      playset/
        model.py
        importers.py
        launcher.py
        resolver.py
        search.py
      analysis/
        delta.py
        baseline.py
        override_resolver.py
        fixability.py
      context/
        workspace.py
        correlation.py
      reporting/
        terminal.py
        markdown.py
        json_report.py
      contracts/
        agent_json.py
      sdk_adapter.py            # optional ck3raven SDK bridge
  tests/
    test_cli.py
    test_db.py
    test_parser.py
    test_normalize.py
    test_report.py
    test_delta.py
    test_playset.py
    test_override_resolver.py
    test_workspace.py
    test_fixability.py
    test_agent_json.py
    fixtures/
      logs/                     # tiny synthetic CK3 log snippets
      crashes/                  # tiny synthetic crash folders
      mods/                     # synthetic mod trees for resolver tests
      playsets/                 # synthetic playset imports (JSON / launcher)
      db/                       # reference schema
  docs/
    00_project_charter.md       # this document
    (implementation plan, ADRs, etc.)
```

> Exact module placement may shift during implementation; the above is the
> intended shape, not a contract. The boundaries in Section 2.2 are the
> contract.

---

## 5. Dependency & Tooling Policy

### Python version
**Python 3.11+** minimum.

### MVP: stdlib-only
The first public release uses only the standard library:

```
argparse, sqlite3, pathlib, dataclasses, json, re, hashlib, difflib
```

No `click`, `rich`, `pydantic`, or similar until a concrete need is
demonstrated and approved. Stdlib-only keeps the first release portable and
reduces packaging friction.

### Test runner
**pytest.** Test fixtures live in `root:repo/ck3chronicle/tests/fixtures/`;
real artifacts live in `root:ck3raven_data/wip/ck3chronicle/`.

### Static checks
Repo-standard checks (whatever ck3raven uses — pyright/pylance, etc.) run
per phase where Python is touched. Diagnostics are useful but **not a hard
blocker** unless they identify real syntax, type, or import breakage.

### CK3 version targeting
Do not hardcode a CK3 version claim in the README. Use language such as:

> Designed for modern CK3 logs and tested initially against the user's current
> CK3 1.18 / 1.19-era modded environment.

If the installed CK3 version can be read from session metadata at runtime,
capture it dynamically.

---

## 6. Phase Roadmap

The roadmap is **12 phases (0–11)**. Each phase produces user-visible value,
has a narrow scope, and is gated by mandatory reviewer approval (Section 8).

| Phase | Name | Subagent shape | User-visible value |
|---|---|---|---|
| **0** | Evidence Preservation and Session Registry | implementer → reviewer | `ck3chronicle ingest` snapshots logs and crash evidence; `sessions` lists what's been captured. |
| **1** | Canonical Issue Records and Error Clustering | test-designer → implementer → reviewer | Parser emits canonical issue records; normalizer clusters by signature; categories / severity / confidence assigned. |
| **2** | Delta Reports, Baselines, and Noise Management | implementer → reviewer | `report`, `diff`, `baseline create`, `ignore`; new/fixed/worse/improved classification; ignored-issue suppression. |
| **3** | Native Playset Model and Import | test-designer → implementer → reviewer | `Playset` / `PlaysetMod` model; importers for manual definition, launcher data, and JSON; `playset` CLI surface. Source-resolution prerequisite. |
| **4** | Source and Override-Chain Resolver | test-designer → implementer → reviewer | Enrich issues with winning file, override chain, our-submod status — resolving against the native Playset. |
| **5** | Workspace Context and Likely-Cause Analysis | test-designer → implementer → reviewer | Capture workspace roots, Git state, recently modified files; correlate to errors. |
| **6** | Fixability Ranking and Recommendation Report | test-designer → implementer → reviewer | Actionability scoring; recommendation engine with explicit confidence. **First public/dev release here.** |
| **7** | Agentic Query Layer | implementer → reviewer | Stable JSON outputs, schema versioning, `latest --json` agent-friendly contracts. |
| **8** | Cross-Run Analytics and Trend Intelligence | test-designer → implementer → reviewer | Multi-session trends, recurring-issue history, stability tracking. |
| **9** | IDE and ck3lens Integration | implementer → reviewer | Optional VS Code / ck3lens integration (MCP wrappers, status surfacing). |
| **10** | Static Validator and Script-Docs Cross-Reference | test-designer → implementer → reviewer | Cross-reference issues against CK3 script docs / known signatures. |
| **11** | Guided Repair Support | implementer → reviewer | Read-only repair scaffolding; suggested-edit composition (no autonomous mutation). |

### Phase 0 implicit scaffolding

Phase 0 carries the package skeleton (`pyproject.toml`, CLI entrypoint,
`doctor` command, test scaffolding) as a prerequisite for evidence
preservation. Scaffolding is not a separate phase; it is a non-optional
deliverable of Phase 0.

### Release trigger: capability-based (lands at end of Phase 6)

The first public/dev release ships once ck3chronicle can:

- preserve evidence (logs and crash artifacts);
- emit canonical issue records;
- compare sessions and baselines;
- manage ignored noise;
- **import or define a native playset;**
- resolve source / override context against that playset;
- correlate to workspace / Git changes;
- rank fixability and produce useful human + JSON reports.

In the current roadmap these capabilities are complete at the end of
**Phase 6 — Fixability Ranking and Recommendation Report**. The release
criterion is the capability list above, not the phase number; if phases are
later renumbered or reordered, the criterion stands.

Phases 7–11 deepen integration and intelligence; none are required for the
first ship.

---

## 7. Sub-agent Topology

ck3chronicle uses a **hybrid model** of two pipelines, applied per phase:

### 7.1 Three-agent pipeline (non-trivial logic phases)

```
test-designer → implementer → reviewer
```

Applied to phases with substantive logic and architectural risk:

- Phase 1 — Canonical Issue Records and Error Clustering
- Phase 3 — Native Playset Model and Import
- Phase 4 — Source and Override-Chain Resolver
- Phase 5 — Workspace Context and Likely-Cause Analysis
- Phase 6 — Fixability Ranking and Recommendation Report
- Phase 8 — Cross-Run Analytics and Trend Intelligence
- Phase 10 — Static Validator and Script-Docs Cross-Reference

**Test-designer** writes failing tests and acceptance fixtures from the
phase's task contract before implementation begins. **Implementer** makes
the tests pass. **Reviewer** enforces gates.

### 7.2 Single-implementer pipeline (mechanical phases)

```
implementer → reviewer
```

Applied to phases that are mostly mechanical, integration-shaped, or where
the canonical pipeline already constrains the design:

- Phase 0 — Evidence Preservation and Session Registry
- Phase 2 — Delta Reports, Baselines, and Noise Management
- Phase 7 — Agentic Query Layer
- Phase 9 — IDE and ck3lens Integration
- Phase 11 — Guided Repair Support

### 7.3 Orchestration

The **main agent** (the agent operating in the user's chat session) remains
the planner / orchestrator across all phases. It expands each kickoff prompt
into a concrete task contract using the template before launching the
implementer. A separate **planning subagent** is invoked only if a phase
proves ambiguous or too large for one orchestration pass.

### 7.4 Reviewer focus

The reviewer subagent must check, at minimum:

- scope drift (does the diff exceed the task contract?)
- canonical pipeline compliance (no raw-log → report shortcuts)
- parser boundary (no analytics / override resolution / Git access)
- override-resolver boundary (no raw-log parsing)
- report-composer boundary (no raw-log reads)
- repo / WIP boundary (no scratch in product paths, no product code in WIP)
- test adequacy (acceptance tests cover the task contract)

Reviewer approval is **mandatory**. No phase is complete until tests pass,
the reviewer approves, and an implementation summary is written.

### 7.5 Task contracts

Each phase's prompt is expanded by the orchestrator into a concrete task
contract containing:

- **Target files** (canonical addresses)
- **Explicit out-of-scope items**
- **Allowed commands**
- **Acceptance tests**
- **Definition of done**
- **Review checklist**

The 11 prompt files in `ck3chronicle_agent_kickoff_v2/agent_prompts/` are
treated as **authoritative outlines**, not final task contracts. They seed
the orchestrator; they do not bypass contract expansion.

---

## 8. Validation Gates

A phase is complete only when **all** of the following pass:

1. **Reviewer agent approves** (Section 7.4 checklist).
2. **Tests pass** (`pytest` for the touched package).
3. **Human eyeballs the diff** (the user reviews the PR / branch).
4. **End-to-end CLI demo against fixture logs passes** (the phase's
   user-visible value is demonstrated against tiny synthetic fixtures
   committed in `tests/fixtures/`).
5. **Repo-standard static checks pass** for touched Python (used as a signal,
   not a hard blocker, unless real syntax / type / import breakage is found).

---

## 9. Branch & PR Workflow

- A dedicated feature branch: **`feature/ck3chronicle`**, created off the
  current main development line.
- ck3chronicle work does **not** continue on `agent/fix-mcp-invoke-init` or
  any other unrelated branch.
- **One PR per phase.** Small, reviewable, phase-sized.
- If tooling cannot cleanly support multiple PRs, fall back to one long-running
  branch with **phase-sized commits and phase-sized review gates** — but
  reviewer approval per phase remains mandatory.

---

## 10. Prototype Promotion Strategy

The existing prototype at:

```
root:repo/ck3chronicle/error analysis refactor/ck3chronicle_proto/
```

already embodies the architecture we want: parser, normalizer, canonical
issue model, aggregator, override resolver, fixability engine, report
composer, SDK adapter. Approach: **promote + harden**, not clean slate.

For each prototype module, the relevant phase will:

1. Lift the module into `root:repo/ck3chronicle/src/ck3chronicle/` under the
   target path (Section 4).
2. Bring it under the canonical schema and boundaries (Section 2).
3. Add fixture-based tests (Section 11).
4. Refactor only where the prototype violates a boundary or where the harden
   step demands it.

**Do not rewrite a prototype module from scratch** unless it is demonstrably
unsuitable, and document the reason in the phase's implementation summary.

---

## 11. Test & Fixture Strategy

### Fixtures live where the boundary says they live

- **Tiny synthetic fixtures** committed in
  `root:repo/ck3chronicle/tests/fixtures/`.
- **Real CK3 logs, real crash folders, generated reports, dev SQLite
  databases, parser spikes** live in `root:ck3raven_data/wip/ck3chronicle/`
  and **never** in the repo.

### Required fixture coverage by phase

Each phase's task contract specifies its acceptance fixtures. Minimum
coverage at each gate:

- **Phase 0:** sample log directory, one synthetic crash folder.
- **Phase 1:** multi-line script error, repeated error (signature clustering),
  localization spam, database conflict block.
- **Phase 2:** two synthetic sessions with new / fixed / worse / improved
  deltas; one baseline.
- **Phase 3:** synthetic playset definitions (manual / JSON / launcher-shaped
  inputs); enabled / disabled / load-order variants; mod source-type variety
  (base game, workshop, local, our submod).
- **Phase 4:** synthetic mod tree with base game / workshop / local / submod
  layers; an override chain producing a clear winner; resolved against a
  Phase 3 playset fixture.
- **Phase 5:** synthetic workspace + Git state.
- **Phase 6:** canonical issue set spanning severities and submod-winner
  variations.
- **Phase 7:** JSON-schema-validated sample report.
- **Phase 8+:** as defined when those phases plan.

### No real artifacts committed

No real user logs, real crash artifacts, large logs, Steam Workshop files, or
private local paths in the repo — ever.

---

## 12. Ratified Open Decisions

The following decisions are now settled and binding on all phases.

| # | Topic | Decision |
|---|---|---|
| 1 | **Crash confidence** | `High` / `Medium` / `Low` — matches issue confidence model. |
| 2 | **Volatile masking** | Whitelist of known volatile patterns only. Mask: line numbers, near-line references, memory addresses, generated runtime IDs, internal character IDs known to be volatile, argument hashes (`args#123`). Preserve semantic IDs and names unless explicitly known volatile. **Never blindly mask every standalone number.** |
| 3 | **Baseline naming** | User-arbitrary strings (e.g. `clean-boot`, `pre-tct-fix`, `post-house-traditions-cleanup`). |
| 4 | **Log discovery (early phases)** | Fixed configured list: `error.log`, `game.log`, `debug.log`, `database_conflicts.log`, `setup.log`, `text.log`. Dynamic discovery is permitted later if trivial; not required for first release. |
| 5 | **Crash-adjacent fixability boost** | An issue is crash-adjacent if **any** of: appears in the last `N` canonical issue blocks before a crash-linked session end (default `N = 25`); appears in logs copied into the linked crash folder; appears in crash-specific readable metadata if present. Confidence must be explicit. |
| 6 | **Raw sample size cap in reports** | 2000 characters (prototype default). Configurable in a later phase. |
| 7 | **Target CK3 version** | Do not hardcode. Use language like "Designed for modern CK3 logs and tested initially against the user's current CK3 1.18 / 1.19-era modded environment." Capture installed version dynamically from session metadata when possible. |
| 8 | **Package structure** | Independent package: `root:repo/ck3chronicle/` with its own `pyproject.toml`. |
| 9 | **Python / deps** | Python 3.11+; stdlib-only for MVP. |
| 10 | **Branch strategy** | Dedicated `feature/ck3chronicle` branch; one PR per phase. |
| 11 | **MCP / SDK / Playset** | MVP independent of MCP and SDK. **The core resolver is native-Playset-backed.** Filesystem fixture resolver is required for tests. ck3raven SDK / session integration is an optional adapter that converts ck3raven session data into a ck3chronicle `Playset`; it is not a core dependency. |

---

## 13. Non-Goals (Do Not Build Yet)

Explicit non-goals for the MVP — not because they are bad ideas, but because
they are out of scope for the first ship:

- VS Code extension (Phase 8 introduces optional integration only).
- MCP server tooling for ck3chronicle (Phase 8 may add optional wrappers).
- Background daemon / always-on process.
- Autonomous repair (Phase 10 is guided / read-only).
- Full crash-dump parser (binary minidump analysis).
- Telemetry of any kind.
- CWTools / CK3 Tiger replacement.

---

## 14. Subagent Budget Policy

Subagents (`runSubagent`) are used **aggressively but deliberately**:

- Test design, implementation, review, and targeted research / inspection
  are appropriate uses.
- Every subagent invocation must carry a **concrete task contract** —
  expanded from the kickoff outline by the orchestrator.
- Vague open-ended subagent invocations are forbidden.

---

## 15. Glossary

| Term | Meaning |
|---|---|
| **canonical issue record** | Normalized, schema-versioned representation of a single problem detected in a CK3 log. Produced by the parser; consumed by everything else. |
| **session** | One ingestion event — one CK3 run's worth of evidence captured to SQLite. |
| **baseline** | A named session snapshot the user has marked for later comparison. |
| **Playset** | ck3chronicle's native representation of an active CK3 mod list, including mod names, paths, enabled status, source type, and load order. Owned by ck3chronicle; not a wrapper around ck3raven session state. |
| **SourceInstance** | One discovered instance of a game-relative file in base game or in a specific mod. |
| **winning file** | The file instance ck3chronicle believes is active for a referenced game-relative path under the current playset / load-order model. This is evidence for triage, not proof of root cause. |
| **our-submod status** | Whether the winning file belongs to a submod under the user's active development, as opposed to vanilla / workshop / unrelated local mod. |
| **fixability** | A confidence-explicit score expressing how actionable an issue is. |

---

## 16. Source Documents

This charter is derived from and supersedes:

- `root:repo/ck3chronicle/ck3chronicle_agent_kickoff_v2_all_in_one.md` —
  original vision and roadmap.
- `root:repo/ck3chronicle/ck3chronicle_agent_kickoff_v2/README.md` and
  `agent_prompts/`, `templates/`, `examples/`, `docs/` — kickoff scaffolding
  (treated as authoritative outlines per Section 7.5).
- `root:repo/ck3chronicle/error analysis refactor/` — prototype to be
  promoted per Section 10.
- The user's authoritative decisions delivered on 2026-06-02 — incorporated
  throughout Sections 4–14.

---

## 17. Next Step

The next deliverable is a **written implementation plan** (not
implementation), drafted by the main agent and saved under
`root:ck3raven_data/wip/ck3chronicle/`. That plan will translate this charter
into concrete per-phase task contracts, kickoff order, branch creation
mechanics, and the first phase's launch packet.
