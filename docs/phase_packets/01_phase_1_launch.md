# Phase 1 — Launch Packet

> **Phase:** 1 — Canonical Issue Records and Error Clustering  
> **Subagent shape:** test-designer → implementer → reviewer (first three-agent phase)  
> **Source contract:** [01_implementation_plan.md §7 / Phase 1](../01_implementation_plan.md)  
> **Charter:** [00_project_charter.md](../00_project_charter.md)  
> **Prior phase:** [00_phase_0_launch.md](00_phase_0_launch.md) — APPROVED at commit `3ca2ae2`  
> **Branch policy:** one PR per phase (plan §2.2). Implementer creates a feature
> branch (e.g. `feature/phase-1-issue-records`) off `main`, opens a PR, and
> merges only after reviewer `APPROVE` and human eyeball. **Do not commit
> directly to `main`** — including for docs-only changes — unless the human
> orchestrator explicitly approves it in this thread.  
> **Created:** 2026-06-04

This packet is what the **test-designer** subagent receives first. The
test-designer produces a `tests/` diff (failing tests + fixtures). The
**implementer** then receives this packet + the test-designer diff and writes
code until the tests pass. The **reviewer** receives this packet + the
implementer diff + the validation checklist in §3 of the implementation plan
+ the boundary rules in charter §2.2 / §3.3 + the heritage-asset rule in
plan §5.3 / §5.3.1.

---

## 1. Mission (in one sentence)

Parse every timestamped block in harvested CK3 logs through an **extractor
registry** into canonical `Issue` records carrying `(category, error_type,
tags)`, cluster them by a deterministic `signature`, preserve referenced
symbols per occurrence, and persist the result so `ck3chronicle parse
--session N` produces a queryable issue inventory — without ever resolving
overrides, comparing sessions, or generating recommendations.

## 2. Hard Constraints (re-read before writing code)

- All product code under `src/ck3chronicle/`. No exceptions.
- Tests under `tests/`.
- **No live code may live in or import from `error analysis refactor/`**
  (reference-only — plan §5.3.1). This includes the
  `error analysis prototype/` subtree — read it, do not import it.
- **No live code may live in or import from `ck3chronicle_proto/`**
  (reference-only — plan §5.3.1).
- All filesystem paths come from `ck3chronicle.config`. **No** inline
  `Path.home() / ...`, `os.environ[...]`, OS-default discovery, or hardcoded
  CK3 / Steam / launcher / mod / log paths outside `config.py`
  (plan §3 checklist + §4.3).
- Stdlib only. Permitted modules from Phase 0 carry over:
  `argparse, sqlite3, pathlib, dataclasses, json, re, hashlib, difflib,
  datetime, shutil, logging, tomllib, enum`. **No** new third-party deps.
- Python 3.11+ required.
- **Parser boundary (plan §3 + §4.3):** `parser/` never imports from
  `analysis/`, `playset/`, `reporting/`, `resolver/`, or any future
  `sdk_adapter`. Parser also never reads `git`, runs `ck3lens`, or touches
  override resolution.
- No override resolution (Phase 4). No cross-session comparison (Phase 2).
  No recommendation scoring (Phase 6).
- No `ck3raven`, `mcp`, `ck3lens` imports anywhere.
- **Signature determinism is mandatory:** same input bytes → same
  `signature` string across runs, processes, and platforms.
- **Taxonomy is not a fixed enum.** `category` and `error_type` are string
  fields drawn from a curated registry (§5). The registry is open for
  Phase 1 to extend, but every new value is justified in the implementation
  summary.

## 3. Target Files (create / extend)

```
ck3chronicle/                                            (existing standalone repo)
  src/ck3chronicle/
    models/
      __init__.py                                        (new)
      issue.py                                           (new — Issue / IssueDraft / IssueOccurrence)
    parser/
      __init__.py                                        (new)
      log_blocks.py                                      (new — timestamped-block splitter)
      extractors/
        __init__.py                                      (new — extractor registry)
        script_system.py                                 (new — script-system blocks; heritage §4)
        localization.py                                  (new — missing-key / token / formatting)
        descriptor.py                                    (new)
        persistent_reader.py                             (new — multi-line quoted blocks)
        asset_graphics.py                                (new — textures, models, dds, shaders)
        gui_interface.py                                 (new — gui/, interface/, widgets)
        event_system.py                                  (new — event ID resolution / scope errors)
        database_reference.py                            (new — db lookup failures, dup keys)
        history_setup.py                                 (new — history/ load errors)
        culture_faith.py                                 (new — culture / faith / religion loads)
        script_hygiene.py                                (new — deprecated effects, unused vars)
        unclassified.py                                  (new — fallback; emits category=Unclassified)
      normalize.py                                       (new — volatile masking + signature)
    db/
      schema.py                                          (extend — issues, issue_occurrences)
      migrations.py                                      (extend — v1 → v2)
      repository.py                                      (extend — issue CRUD)
    cli.py                                               (extend — `parse` subcommand)
  tests/
    test_models_issue.py                                 (new)
    test_log_blocks.py                                   (new — timestamped block splitter)
    test_extractor_registry.py                           (new — dispatch + ordering)
    test_extractors_script_system.py                     (new)
    test_extractors_localization.py                      (new)
    test_extractors_descriptor.py                        (new)
    test_extractors_persistent_reader.py                 (new)
    test_extractors_asset_graphics.py                    (new)
    test_extractors_gui_interface.py                     (new)
    test_extractors_event_system.py                      (new)
    test_extractors_database_reference.py                (new)
    test_extractors_history_setup.py                     (new)
    test_extractors_culture_faith.py                     (new)
    test_extractors_script_hygiene.py                    (new)
    test_extractors_unclassified.py                      (new)
    test_normalize.py                                    (new)
    test_db_issue.py                                     (new — schema v2 + repo methods)
    test_cli_parse.py                                    (new)
    fixtures/logs/
      noisy_localization/                                (new — see §8)
      multiline_script_error/                            (new)
      persistent_reader_multiline/                       (new)
      categorizer_matrix/                                (new — one block per category)
      unclassified_block/                                (new — block no extractor claims)
      database_conflicts/                                (new)
```

Do not touch any file outside this list.

## 4. Heritage Assets (REQUIRED reads — plan §5.3)

The test-designer and implementer subagents **must** read the following
heritage assets before producing their diffs. The reviewer subagent verifies
the implementation summary cites them. Failure to cite → at minimum
`REQUEST_CHANGES`.

| Asset | Path (within ck3raven workspace) | Use |
|---|---|---|
| Refactor design spec | `root:repo/ck3chronicle/error analysis refactor/ck3chronicle_modular_refactor_all_in_one (1).md` | Canonical-pipeline rules, "CURRENT WINNING FILE" wording, modular split rationale. |
| Pre-modular prototype — script error parser | `root:repo/ck3chronicle/error analysis refactor/error analysis prototype/parse_script_errors.py` | **Reference for the script-system extractor only.** Use it to model `extractors/script_system.py`: how to lift call stacks, file/line/symbol references, and sample-message behavior out of multi-line script-system blocks. **It is NOT the authoritative taxonomy.** Phase 1 taxonomy is `category + error_type + tags`, seeded by bottom-up signature discovery and curated rules (§5). |
| Pre-modular prototype — driver / dedup | `root:repo/ck3chronicle/error analysis refactor/error analysis prototype/analyze_error_files.py` | Reference for per-file deep-dive workflow and sample-message dedup limits. May be consulted. |
| Pre-modular prototype — toolkit setup | `root:repo/ck3chronicle/error analysis refactor/error analysis prototype/setup_error_analysis_toolkit.py` | Optional reference. |

These assets are **read-only inputs**. Do not import them, do not move them,
do not edit them. Promotion is by **rewrite** under `src/ck3chronicle/` with
fixture-based tests (plan §5.2, §5.3.1).

## 5. Taxonomy Model (`category` + `error_type` + `tags`)

Phase 1 abandons monolithic enums (e.g. `Category.MISSING_LOCALIZATION`) in
favor of a three-field model:

- **`category: str`** — broad subsystem / fix-domain. Stable, small set.
  Examples: `Localization`, `ScriptSystem`, `Descriptor`,
  `PersistentReader`, `AssetGraphics`, `GuiInterface`, `EventSystem`,
  `DatabaseReference`, `HistorySetup`, `CultureFaith`, `ScriptHygiene`,
  `Unclassified`.
- **`error_type: str`** — canonical recurring error signature within a
  category. Examples: `missing_key`, `unexpected_localization_token`,
  `unknown_trait_reference`, `unresolved_event_id`, `texture_load_failed`,
  `deprecated_effect`, `unknown`. Snake_case.
- **`tags: list[str]`** — optional cross-cutting descriptors. Examples:
  `["syntax", "parse"]`, `["startup"]`, `["multiline"]`, `["heuristic"]`.
  Order-stable (sorted) for signature determinism.

### Curated registry

`src/ck3chronicle/models/issue.py` defines two `frozenset[str]` registries:
`KNOWN_CATEGORIES` and `KNOWN_ERROR_TYPES`. Each extractor declares the
`(category, error_type)` pairs it emits at module import time, and the
registry validates at startup that every declared pair is in the known set.
An extractor emitting an unknown pair raises `ValueError` at startup — never
silently. New values are added by editing the registries in `issue.py` and
documenting the rationale in the implementation summary.

### Severity and confidence

- **`severity: str`** — one of `info`, `warning`, `error`, `fatal`.
  Determined per `(category, error_type)` by the extractor.
- **`confidence: str`** — one of `high`, `medium`, `low`.
  - `high` — extractor matched a curated rule with high specificity.
  - `medium` — partial match, heuristic fallback applied within a known
    category.
  - `low` — `Unclassified` only.

These are stored as lowercase strings, not enums, to keep the model
serialization-friendly and the registry open.

## 6. Parser Architecture

```
error.log + database_conflicts.log (raw bytes)
        │
        ▼
parser/log_blocks.py
   split into TimestampedLogBlock records
   (timestamp, source_tag, header_line, continuation_lines)
        │
        ▼
parser/extractors/__init__.py
   extractor registry: list of extractors in deterministic order
        │
        ▼
each TimestampedLogBlock → first claiming extractor → IssueDraft
   unclaimed blocks → unclassified extractor (category=Unclassified,
                                              error_type=unknown,
                                              confidence=low)
        │
        ▼
parser/normalize.py
   IssueDraft → (message_template, signature, referenced_symbols)
        │
        ▼
models.issue.Issue       (clustered by signature)
models.issue.IssueOccurrence  (one row per raw block)
```

### `parser/log_blocks.py`

- Function `iter_log_blocks(path: Path) -> Iterator[TimestampedLogBlock]`.
- A **timestamped block** begins with a line whose leading token matches the
  CK3 timestamp shape (e.g. `[HH:MM:SS]`). Continuation lines (anything
  until the next timestamped header or EOF) belong to that block.
- Persistent-reader blocks may contain quoted multi-line content with
  embedded newlines and indentation — those count as continuation lines.
- Empty lines inside a block are preserved; trailing whitespace is stripped
  per line.
- The splitter NEVER drops a line. Pre-timestamp preamble (if any) is
  emitted as a single block with `timestamp=None`, `source_tag="<preamble>"`.

### `parser/extractors/__init__.py`

- Module-level constant `EXTRACTORS: tuple[Extractor, ...]` lists every
  extractor in deterministic dispatch order. The unclassified extractor is
  always last and always claims.
- `Extractor` protocol: `claim(block: TimestampedLogBlock) -> bool` and
  `extract(block) -> IssueDraft`.
- Function `extract_block(block) -> IssueDraft` walks `EXTRACTORS` and
  returns the first claim. Determinism: dispatch order is module-static; no
  set / dict iteration affects the result.

### Per-extractor modules

Each `parser/extractors/<name>.py` defines:
- Module docstring listing the `(category, error_type)` pairs it emits.
- A `claim()` predicate (string / regex pattern on the block header or
  body).
- An `extract()` function returning an `IssueDraft` populated with the
  fields in §7.

The **script-system extractor** is the only one allowed to consult
`parse_script_errors.py` as a reference (heritage §4) — and even then, only
for the shape of script-system block lifting (call stacks, file/line/symbol
extraction). It must not import from that file.

### `parser/normalize.py`

- Function `normalize(draft: IssueDraft) -> NormalizedIssue` returns
  `(message_template, signature, referenced_symbols)`.
- **Volatile masking is whitelist-only** (charter §12 #2). Masked tokens:
  - Line numbers in script-error tails (e.g. `line 12` → `line <N>`).
  - `args#NNN` argument-id references (`args#0042` → `args#<N>`).
  - Numeric tail offsets in localization-position annotations.
  - Concrete localization keys, file paths, trait names, scope names, and
    other **semantic IDs** — these are PRESERVED in `message_template` but
    ALSO captured in `referenced_symbols` so cluster-level views can
    suppress them while per-occurrence views keep them intact.

  > **Clarification on grouping:** if the extractor decides a family of
  > errors should cluster (e.g. all `missing_key` localization errors), it
  > emits a `message_template` that uses a placeholder for the varying
  > token (e.g. `Missing localization key '<KEY>' in <FILE>`) and stuffs
  > the actual key into `referenced_symbols`. Per-occurrence rows preserve
  > the raw line and the concrete key. The cluster row carries
  > `occurrence_count` and the templated message; the concrete keys remain
  > available via `issue_occurrences.referenced_symbols_json` (§7) for
  > fixability.

- `signature = sha256(category + "\n" + error_type + "\n" + ",".join(sorted(tags)) + "\n" + message_template + "\n" + (primary_file or "")).hexdigest()[:16]`.
  Document the exact construction in the module docstring.

## 7. `models/issue.py` Spec

All three types are `@dataclass(frozen=True)` from stdlib `dataclasses`. No
third-party validation libraries. Field order in the dataclass body is the
order below.

### `IssueDraft` — extractor output (pre-normalization)

| Field | Type | Notes |
|---|---|---|
| `category` | `str` | Must be in `KNOWN_CATEGORIES`. |
| `error_type` | `str` | Must be in `KNOWN_ERROR_TYPES`. |
| `tags` | `tuple[str, ...]` | Sorted ascending at construction; empty tuple allowed. |
| `engine_source` | `str` | Source-line tag from the log (e.g. `data_loader.cpp:511`, `localization.cpp:121`, `<preamble>`). |
| `sample_message` | `str` | Verbatim header line of the block. |
| `raw_block` | `str` | The full timestamped block (header + continuations) verbatim. Used by occurrence rows. |
| `primary_file` | `str \| None` | File the error references, if extractable. |
| `primary_line` | `int \| None` | Line number in `primary_file`, if extractable. |
| `referenced_symbols` | `tuple[str, ...]` | Concrete semantic IDs (trait names, keys, event IDs). Sorted, deduped. |
| `referenced_objects` | `tuple[str, ...]` | Coarser referenced entities (file basenames, mod names, scope chains). Sorted, deduped. |
| `extra_json` | `str` | JSON-serialized dict for extractor-specific structured fields. Defaults to `"{}"`. |
| `severity` | `str` | `info` / `warning` / `error` / `fatal`. |
| `confidence` | `str` | `high` / `medium` / `low`. |
| `log_relpath` | `str` | Relative path of the source log within the session bundle. |
| `line_number` | `int` | Header line's 1-based line number in the source log. |

### `Issue` — normalized, clustered row

Same as `IssueDraft` PLUS:

| Field | Type | Notes |
|---|---|---|
| `signature` | `str` | 16-char hex (§6). Deterministic. |
| `message_template` | `str` | Volatile tokens masked per §6. |
| `occurrence_count` | `int` | Set by the repository on upsert (1 on first insert, incremented thereafter). |

`Issue` drops `raw_block`, `log_relpath`, `line_number` (those move to
`IssueOccurrence`).

### `IssueOccurrence` — one row per raw block

| Field | Type | Notes |
|---|---|---|
| `session_id` | `int` | FK → `sessions`. |
| `signature` | `str` | FK → `issues(signature)` within `session_id`. |
| `log_relpath` | `str` | |
| `line_number` | `int` | Header line, 1-based. |
| `raw_block` | `str` | Verbatim. |
| `referenced_symbols` | `tuple[str, ...]` | The concrete symbols THIS occurrence carried (the key the cluster row generalized). |
| `extra_json` | `str` | Per-occurrence extractor-specific data. |

### Determinism rule

`Issue.signature` is a pure function of `(category, error_type, tags,
message_template, primary_file)`. It MUST NOT incorporate timestamps, line
numbers, occurrence counts, raw bytes, or anything volatile. Identical
normalized inputs across any two runs MUST produce byte-identical
signatures.

## 8. DB Schema Extension

`db/schema.py` is extended; `db/migrations.py` ships a v1 → v2 migration.
`db/repository.py` gains issue CRUD. **No** breaking changes to Phase 0
tables.

```sql
-- v2 additions
CREATE TABLE issues (
    issue_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id         INTEGER NOT NULL REFERENCES sessions(session_id),
    signature          TEXT NOT NULL,
    category           TEXT NOT NULL,
    error_type         TEXT NOT NULL,
    tags_json          TEXT NOT NULL DEFAULT '[]',
    engine_source      TEXT NOT NULL,
    severity           TEXT NOT NULL,
    confidence         TEXT NOT NULL,
    message_template   TEXT NOT NULL,
    sample_message     TEXT NOT NULL,
    primary_file       TEXT,
    primary_line       INTEGER,
    referenced_symbols_json  TEXT NOT NULL DEFAULT '[]',
    referenced_objects_json  TEXT NOT NULL DEFAULT '[]',
    extra_json         TEXT NOT NULL DEFAULT '{}',
    occurrence_count   INTEGER NOT NULL DEFAULT 1,
    UNIQUE(session_id, signature)
);

CREATE INDEX idx_issues_session_signature
    ON issues(session_id, signature);
CREATE INDEX idx_issues_category_error_type
    ON issues(category, error_type);

CREATE TABLE issue_occurrences (
    issue_occurrence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id          INTEGER NOT NULL REFERENCES sessions(session_id),
    signature           TEXT NOT NULL,
    log_relpath         TEXT NOT NULL,
    line_number         INTEGER NOT NULL,
    raw_block           TEXT NOT NULL,
    referenced_symbols_json  TEXT NOT NULL DEFAULT '[]',
    extra_json          TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (session_id, signature)
        REFERENCES issues(session_id, signature)
);

CREATE INDEX idx_issue_occurrences_session_sig
    ON issue_occurrences(session_id, signature);
```

`migrations.py` records `('canonical_issues', 2, <iso_ts>)` in
`schema_versions` on successful upgrade. The migration is idempotent and
safe to re-run.

`db/repository.py` adds:
- `upsert_issue(conn, session_id, issue) -> int` — returns `issue_id`;
  increments `occurrence_count` when `(session_id, signature)` already
  exists.
- `add_issue_occurrence(conn, session_id, occurrence) -> int`.
- `list_issues(conn, session_id, *, category=None, error_type=None, limit=None) -> list[Issue]`.
- `list_occurrences(conn, session_id, signature) -> list[IssueOccurrence]`.
- `count_issues_by_category(conn, session_id) -> dict[str, int]`.
- `count_issues_by_error_type(conn, session_id) -> dict[tuple[str, str], int]`.

## 9. Test Fixtures (synthetic — do NOT use real logs)

All fixtures live under `tests/fixtures/logs/` alongside the Phase 0
`minimal/` and `with_crash/` fixtures. No real CK3 artifacts. No personally
identifying mod names, character names, or save data. Each fixture folder
contains an `error.log` and a 3-line harmless `game.log`.

### `tests/fixtures/logs/noisy_localization/`

`error.log` — 50 timestamped blocks, each a missing-localization error with
a **distinct key** but identical message template. All must cluster to ONE
`Issue` with `occurrence_count == 50`. **Each occurrence row must preserve
its concrete missing key** in `referenced_symbols_json`. The cluster row's
`message_template` masks the key into `<KEY>`; the cluster row's
`referenced_symbols_json` is the empty list (cluster-level view suppresses
the concrete value).

### `tests/fixtures/logs/multiline_script_error/`

`error.log` — one timestamped script-system block: header line followed by
3+ indented continuation lines (file path, line number, scope chain). Must
parse as ONE `IssueDraft` with `primary_file` / `primary_line` intact and
the call-stack tokens populated in `referenced_objects`.

### `tests/fixtures/logs/persistent_reader_multiline/`

`error.log` — one timestamped persistent-reader block whose continuation
lines include quoted multi-line content with embedded newlines and
indentation. Must parse as ONE block (no splitting on the embedded
newlines) and the persistent-reader extractor must claim it. Verifies the
block splitter does not break on quoted multi-line payloads.

### `tests/fixtures/logs/categorizer_matrix/`

`error.log` — one representative timestamped block per `category` value in
the curated registry (§5), in registry order. Each block MUST be claimed
by its expected extractor and produce the expected
`(category, error_type, severity, confidence)` tuple. This fixture is the
executable specification for the extractor registry.

### `tests/fixtures/logs/unclassified_block/`

`error.log` — one timestamped block that no specialized extractor claims.
Must be claimed by the unclassified extractor with
`category="Unclassified"`, `error_type="unknown"`, `confidence="low"`. The
`raw_block` and `engine_source` MUST be preserved so a human can triage.

### `tests/fixtures/logs/database_conflicts/`

`error.log` — 5 timestamped blocks mixing duplicate-key and
override-collision shapes. The `database_reference` extractor claims them
all with appropriate `error_type` values.

## 10. CLI Subcommand

```
ck3chronicle parse --session N [--reparse]
```

- Requires `--session N` (no auto-pick). Errors clearly if `N` does not
  exist.
- If issues already exist for the session and `--reparse` is NOT set,
  prints `already parsed; <K> issues across <M> categories; use --reparse
  to recompute` and returns the existing counts.
- With `--reparse`: deletes `issues` + `issue_occurrences` rows for that
  session in a single transaction, then re-parses.
- Prints on success:
  - `parsed <L> timestamped blocks` (count of blocks processed)
  - `produced <K> issues across <M> categories`
  - `top categories: <category>=<n>, <category>=<n>, ...` (top 3 by count)
  - `unclassified: <n>` (count of `Unclassified` issues)

The `ingest`, `sessions`, and `doctor` Phase 0 subcommands MUST continue to
behave exactly as before; their tests MUST remain green.

## 11. Acceptance Tests (must all pass)

- [ ] `pip install -e .` from the ck3chronicle repo root succeeds with
      stdlib-only deps. **No** new requirements added to `pyproject.toml`.
- [ ] **Every timestamped block is accounted for.** A unit test asserts
      that for each fixture, `len(blocks) == len(occurrences)` (no block
      silently dropped). Unmatched blocks land in `Unclassified`.
- [ ] **Multi-line script error** fixture produces exactly one `Issue`
      with intact `primary_file` and `primary_line`, and at least one
      entry in `referenced_objects` (the scope chain or file basename).
- [ ] **Persistent-reader multi-line** fixture parses as ONE block (the
      block splitter does not split on embedded quoted newlines).
- [ ] **Noisy-localization fixture** produces exactly one `Issue` with
      `occurrence_count == 50` AND 50 rows in `issue_occurrences`, AND
      every occurrence row's `referenced_symbols_json` contains exactly
      its concrete missing key (`synth_loc_key_001` … `synth_loc_key_050`).
      A separate assertion verifies the cluster row's `message_template`
      contains `<KEY>` (not any concrete key).
- [ ] **Volatile masking is whitelist-only:** a unit test in
      `test_normalize.py` constructs `IssueDraft`s containing trait
      names, scope names, file paths, and localization keys, and asserts
      those strings appear UNCHANGED in `message_template` after
      normalization EXCEPT where the extractor explicitly templated them
      with a `<KEY>` / `<TRAIT>` / `<FILE>` placeholder. Untemplated
      semantic IDs survive byte-identical.
- [ ] **Signature determinism:** parsing the same fixture twice in the
      same process AND in two separate subprocess invocations produces
      byte-identical `signature` values.
- [ ] **Categorizer matrix:** one assertion per registered `category`
      value verifies the expected `(category, error_type, severity,
      confidence)` tuple is produced for its representative block.
- [ ] **Unclassified fallback:** the `unclassified_block` fixture
      produces exactly one `Issue` with
      `category="Unclassified" AND error_type="unknown" AND confidence="low"`,
      and the `raw_block` is preserved verbatim in the occurrence row.
- [ ] **Per-extractor coverage:** every extractor module in
      `parser/extractors/` has at least one fixture-driven acceptance
      test asserting it claims and extracts correctly. Categories
      required: `Localization`, `ScriptSystem`, `Descriptor`,
      `PersistentReader`, `AssetGraphics`, `GuiInterface`, `EventSystem`,
      `DatabaseReference`, `HistorySetup`, `CultureFaith`,
      `ScriptHygiene`, `Unclassified`.
- [ ] **Registry validation:** importing the parser package on a build
      where an extractor declares an unknown `(category, error_type)`
      pair raises `ValueError` at import time. A regression test induces
      this via monkeypatch and asserts the failure.
- [ ] `ck3chronicle parse --session N` populates the `issues` and
      `issue_occurrences` tables; a follow-up `ck3chronicle parse
      --session N` says "already parsed" and does NOT duplicate rows.
- [ ] `ck3chronicle parse --session N --reparse` deletes prior issue rows
      for the session and re-creates them; row counts match a fresh run.
- [ ] Schema migration v1 → v2 runs cleanly on a Phase-0 DB and is
      idempotent on re-run; `schema_versions` records
      `('canonical_issues', 2, ...)`.
- [ ] `pytest` is green across **all** Phase 0 + Phase 1 tests. Phase 0
      tests show **zero** regressions.
- [ ] grep across `src/ck3chronicle/` and `tests/` shows **zero** imports
      from `error analysis refactor` or `ck3chronicle_proto`
      (charter §3.3, plan §5.3.1, plan §4.3).
- [ ] grep across `src/ck3chronicle/parser/` shows **zero** imports from
      `src/ck3chronicle/analysis/`, `src/ck3chronicle/playset/`,
      `src/ck3chronicle/reporting/`, or `src/ck3chronicle/resolver/`.
- [ ] grep across `src/ck3chronicle/` (excluding `config.py`) shows
      **zero** new uses of `Path.home`, `os.environ`, `expanduser`, or
      any hardcoded `Steam`, `Paradox Interactive`, or
      `Crusader Kings III` path literal.
- [ ] Implementation summary documents:
      1. The full curated `KNOWN_CATEGORIES` and `KNOWN_ERROR_TYPES` sets
         (final values, with one-line justification each).
      2. Which `(category, error_type)` pairs each extractor emits.
      3. Where the script-system extractor borrowed structure from
         `parse_script_errors.py` (heritage §4), and what was
         deliberately NOT copied.

## 12. End-to-End CLI Demo Transcript (paste in PR body)

```
$ python -m pip install -e .
... (success, no new deps)

$ ck3chronicle ingest --logs tests/fixtures/logs/noisy_localization/
evidence_bundle_hash: <sha256>
session_id: 1
copied 2 files (2 logs, 0 crash artifacts) to durable storage

$ ck3chronicle parse --session 1
parsed 50 timestamped blocks
produced 1 issues across 1 categories
top categories: Localization=1
unclassified: 0

$ ck3chronicle parse --session 1
already parsed; 1 issues across 1 categories; use --reparse to recompute

$ ck3chronicle ingest --logs tests/fixtures/logs/categorizer_matrix/
evidence_bundle_hash: <sha256>
session_id: 2
copied 2 files (...)

$ ck3chronicle parse --session 2
parsed 12 timestamped blocks
produced 12 issues across 12 categories
top categories: Localization=1, ScriptSystem=1, Descriptor=1
unclassified: 0

$ ck3chronicle ingest --logs tests/fixtures/logs/unclassified_block/
evidence_bundle_hash: <sha256>
session_id: 3
copied 2 files (...)

$ ck3chronicle parse --session 3
parsed 1 timestamped blocks
produced 1 issues across 1 categories
top categories: Unclassified=1
unclassified: 1

$ pytest
... N passed
```

## 13. Reviewer Hand-off Note

When the implementer reports done, the reviewer subagent must:

1. Run the plan §3 validation checklist on the diff.
2. Confirm §2 hard constraints are intact (grep checks in §11).
3. Confirm acceptance tests pass and the demo transcript is in the PR.
4. Confirm the heritage assets in §4 were read and cited in the
   implementation summary (plan §5.3 — failure → at minimum
   `REQUEST_CHANGES`).
5. Confirm signature determinism by re-running the relevant test in a
   fresh subprocess.
6. Confirm the curated `KNOWN_CATEGORIES` / `KNOWN_ERROR_TYPES` sets are
   documented and the script-system extractor borrows only structure (not
   taxonomy) from the prototype.
7. Confirm the PR targets a feature branch (NOT `main`) and the human has
   eyeballed the diff.
8. Return exactly one verdict: `APPROVE` / `REQUEST_CHANGES` / `REJECT`.

```
Orchestrator tier signal: [A | B]  ← reviewer fills in based on §9.2 of the plan
Reason: <one short sentence>
```

## 14. Out-of-Scope (Phase 1 must NOT do)

- Compare sessions / build deltas. (Phase 2.)
- Introduce `Playset`. (Phase 3.)
- Resolve overrides or rank "current winning file". (Phase 4.)
- Workspace context or likely-cause analysis. (Phase 5.)
- Score fixability or generate recommendations. (Phase 6.)
- Stable agent JSON contracts. (Phase 7.)
- Cross-run analytics. (Phase 8.)
- Any IDE / ck3lens / MCP integration. (Phase 9.)
- Static validator or script-docs cross-reference. (Phase 10.)
- Guided repair support. (Phase 11.)
- Edit, import from, move, or wire any CLI entrypoint to anything inside
  `error analysis refactor/` or `ck3chronicle_proto/`.
- Add ANY third-party Python dependency.
- Touch `git` or any version-control state.
- Commit directly to `main` (use a feature branch + PR per plan §2.2).

---

## §15 Orchestrator Tier Signal (per §9 of implementation plan)

Every reply from this phase's test-designer, implementer, and reviewer MUST
end with:

```
Orchestrator tier signal: [A | B]
Reason: <one short sentence>
```

For Phase 1 specifically:
- **Test-designer success** (failing tests + fixtures landed) → `Tier B`
  (next action: orchestrator dispatches implementer; mechanical).
- **Implementer success** (tests pass, demo transcript captured) →
  `Tier B` (next action: orchestrator invokes reviewer; mechanical).
- **Reviewer `APPROVE`** → `Tier A` (next action: orchestrator drafts
  Phase 2 launch packet — Phase 2 is single-agent, so the packet shape
  changes again).
- **Reviewer `REQUEST_CHANGES`** → `Tier B` (next action: orchestrator
  re-dispatches implementer with the itemized fix list).
- **Reviewer `REJECT`** → `Tier A` (next action: orchestrator diagnoses
  boundary-rule, heritage-rule, or canonical-architecture interpretation).

This applies even when the orchestrator is a human; the signal documents
the recommended tier without forcing it.
