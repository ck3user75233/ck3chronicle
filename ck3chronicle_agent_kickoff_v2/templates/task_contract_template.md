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
