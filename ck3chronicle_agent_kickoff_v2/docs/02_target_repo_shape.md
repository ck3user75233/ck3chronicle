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
