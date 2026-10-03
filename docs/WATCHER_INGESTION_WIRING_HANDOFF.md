# Watcher ingestion wiring — historical delivery evidence

This records the September 29 predecessor delivery. The [current Task 07D handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md)
is the current API/integration reference. It replaces local ingestion serialization
with shared-handler admission/result delivery and preserves lifecycle observation,
publication, startup submissions, warnings and daily retention. Database arguments
are exact SQLite files; SQL/review format is 3 and playset format is 1. Invalid
playsets warn and permit error ingestion. Activation on 07D code is separate;
this document does not establish current live state.

## Verification

42 checks passed in total. The existing Task 07 native ingestion/retention suite
also passed (2 checks, 28.358 seconds), with retained disposable evidence under
`.codex-tmp/task07/8a5c0092fb8f418dba4ba09589a1e45f/`.

- 31 existing watcher/playset capture checks pass after updating superseded
  debug-failure and extractor-failure expectations to the owner's requirements.
- 9 new checks in `tests/test_watcher_ingestion_requirements.py` pass. They cover
  continued lifecycle polls during blocked worker ingestion; startup selection;
  continued handling after input failure; contention as waiting; daily idle
  retention; concurrent journal writes; and sensible configuration defaults.
- The new native checks run the real `cmd_watch` path with simulated process
  observations and copies of genuine CK3 logs. Both a full pair and an error-only
  capture reach real SQL, with review-manifest/playset agreement and duplicate
  readback. A malformed completed playset also permits native error ingestion,
  produces a warning and remains unchanged on disk.

Commands:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p '*capture_requirements.py'
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_watcher_ingestion_requirements.py -v
```

The native checks use the genuine input selection in ignored
`.codex-tmp/task07/evidence.json` and skip explicitly if it is unavailable.
Production paths are not used as verification output destinations.

