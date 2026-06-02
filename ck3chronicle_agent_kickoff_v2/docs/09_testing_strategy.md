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
