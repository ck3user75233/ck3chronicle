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
