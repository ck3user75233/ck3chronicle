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
