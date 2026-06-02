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
