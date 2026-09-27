# Published native model

The selected release is **76630685c4a341ca14bf9c7c**. [selection.json](selection.json)
pins its directory and manifest SHA-256. The immutable release contains model
schema 4, raw parser **ck3-lossless-v1.7**, parser manifest, owner-rule registry,
native validation and hash-covered standalone **assignment.py** / **continuations.py**.
There is no implicit latest-model selection or compatibility fallback.

Learner v41 rediscovers **418 templates: 232 supported and 186 provisional** from
thirty complete native logs. Publication preserves those statuses; it does not
individually confirm templates. Supporting title entries belong to one complete
error with its opening, regardless of list length. Their displayed title is an
opaque PARAM and their repeated character reference must match the opening.

All 1,143,044 unaffected occurrences retain the v40 assignments and captures.
Twenty separate messages become nine complete groups with eleven entries. The
1,143,053 resulting diagnostics replay identically through the learner and runtime,
with 4,429,930 native bindings verified. Additional native-log coverage limits
are recorded in the [delivery ledger](../docs/LEARNER_CONTINUATION_MODEL_STATUS.md).

Use `ck3chronicle.pipeline.catalog.load_selected_classifier(models_root=...)`.
The runtime reader validates model schema, artifact hashes and declarations before
loading the selected parser and standalone helpers. Classifications expose one
`selected` result and its bindings for both full and provisional outcomes. Keep
the outcome with the result; a template ID alone does not imply confirmation.

The wheel packages this selection and all eight release files under
`share/ck3chronicle/models/`. Model/parser identity remains explicit and immutable.
Previous directories are historical artifacts, never fallbacks. Captured logs,
per-occurrence provenance, and generated research reports remain outside Git.

The [existing pipeline handoff](../docs/LEARNER_PARSER_PIPELINE_HANDOFF.md) documents
component-relative matching and absolute bindings. Application ingestion/storage
adoption remains separate; publishing and selecting this release starts no watcher
and performs no production ingestion.
