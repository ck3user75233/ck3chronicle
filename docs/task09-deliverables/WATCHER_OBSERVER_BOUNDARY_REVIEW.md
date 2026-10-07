# Watcher — Verify dependencies before Observer deletion

The Owner considers Watcher the sole owner of identifying and capturing new CK3
logs, recording the source log timestamp, and producing the active playset JSON
in the required format for ingestion into the database.

The Owner believes the Observer is a parallel construction and has ordered its
deletion. Before deletion, determine whether any necessary Watcher functions are
supported by or routed through the Observer, or whether it is completely separate
and can be deleted without affecting those functions.

For this review, identify the Observer concretely through:

- `src/ck3chronicle/logging_observer.py`;
- `cmd_observe_logging` and the `observe-logging` command in
  `src/ck3chronicle/cli.py`; and
- `observer_log_path` in `src/ck3chronicle/runtime_logging.py`.

Trace the required Watcher path through `src/ck3chronicle/watcher.py`,
`src/ck3chronicle/harvester.py`, `src/ck3chronicle/watcher_processing.py`,
the CLI wiring and relevant ingestion interfaces. Check code dependencies and
consumption of files or metadata, not just direct imports. Establish where log
identification, exit-triggered capture, source-log timestamp recording and active
playset JSON production occur, and whether any of them depend on Observer code
or output. Do not assume separation from the component names.

Return a concise finding with file/function references:

1. Whether necessary Watcher functions depend on the Observer, and the evidence.
2. If independent, the exact Observer code and references that can be removed
   without affecting those functions.
3. If dependencies exist, the necessary behavior that must be preserved and the
   bounded changes needed before deletion can safely proceed.
4. Any uncertainty that prevents a supported conclusion.

This assignment is the dependency review preceding the ordered deletion. Use
source inspection and existing evidence; report the findings before making code
or release changes. No new CK3 run or synthetic test is requested.

Use the protected Trekker helper to read Watcher team state and the relevant
TREK-3/4/6 records and handoffs. Record the findings in normal Watcher handoff
material and on existing TREK-3, linking them for Pipeline's TREK-6 receiving.
Do not create a new task or mark deletion complete from this review.
