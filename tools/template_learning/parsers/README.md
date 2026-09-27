# Selectable lossless parser artifacts

Select an explicit manifest with `reference_from_manifest` and `load_parser`.
Published artifacts are immutable; never edit a previous version or substitute
another parser when its hash fails. Models retain their exact parser reference.

| Version | Manifest | Behavior |
| --- | --- | --- |
| ck3-lossless-v1.6 | `v1/manifest.json` | Published lexical rules and within-emission recovery; retained for existing model pins. |
| ck3-lossless-v1.7 | `v1_7/manifest.json` | Same lexical/framing behavior plus emitter-colon continuation recovery across headers. |

For consumer recovery, call `iter_recoveries(raw)` from this package. It dispatches
the selected published API explicitly. v1.7 also exposes `raw.iter_recoveries()`.
Do not loop over `emission.recovery` to classify v1.7 input: that local inspection
API does not associate following emissions.

v1.7 parser SHA-256:
`a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab`.
Its versioned JSON rule is embedded in `parser.py`; `recovery_rules.json` is the
identical readable copy. Runtime is standalone and imports no learner or model.

The [delivery ledger](../../../docs/LEARNER_CHARACTER_TITLE_CONTINUATION_STATUS.md)
describes ranges, consumer deferral until repeated-component model support, all
73-log validation results and the required new model/parser pin.
