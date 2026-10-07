# Learner — Build the production-scope model for the Task 09 baseline

Prepared for owner issuance, 2026-10-07. Continue **TREK-2**; **Pipeline receives on
TREK-6**. This assignment takes effect when issued by the owner.

Produce a fresh, authenticated model using the delivered logging-enabled,
Observer-free Learner and the same genuine 73-log build basis as the existing
production model. This explicitly authorizes that production-scope build, replacing
the earlier two-input limit for this assignment. It does not authorize a new
algorithm, an expanded corpus or a production switch.

## Build and verify

Read root instructions, current component handoffs, [owner decisions](../TASK09_OWNER_DECISIONS.md),
[release procedures](../RELEASES.md), the [previous production build](../learner-next-release/HANDOFF.md)
and [logging acceptance](../learner-next-release/LOGGING_ACCEPTANCE.md).

Use the existing authenticated Learner release:

- Release: `2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485`.
- Manifest SHA-256: `9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e`.

Authenticate its retained bytes and confirm correspondence with the intended
current Learner source. Reuse that immutable release if it is still the correct
closure; building another model does not itself require another Learner release.
Surface any source discrepancy before choosing different executable bytes.
Keep the existing algorithm identity; do not rename it v62 merely for this build.

Use `.codex-tmp/combined-release-20261005/build/build-basis.json` and its associated
receipts to recover and authenticate the exact input inventory, order, settings
and incremental schedule: **20 + 20 + 20 + 13**, with cumulative checkpoints
20/40/60/73. Use the supported retained execution/build mechanism and fresh output
locations. Do not substitute a one-shot build, reuse the old executable identity,
add logs, alter thresholds or silently replace an unavailable input.

Build, evaluate and export the complete model through the normal authenticated
process. Compare with production package `4ac4e8ee92346e6d14eacfbf`, manifest
`839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f`.
Account for model content and genuine classification semantics, including captures,
statuses and unresolved evidence, rather than only aggregate counts. Identify
expected provenance/identity differences separately from behavioral differences.
Explain any unexpected difference; do not retune the model to hide it. Reuse valid
existing evaluation evidence where its exact inputs and executable bytes apply.

Inspect the journals from this actual build against the
[canonical design](../CANONICAL_LOGGING_SYSTEM_V1.md). Show representative actual
invocation/code identities, call completion, truthful progress and terminal/receipt
agreement, with file/line references. In `collect_records`, progress counts inputs
after processing against that invocation's input total, not distinct evidence hashes.
Report unobserved behavior honestly; no synthetic or fault-injection tests.

## Delivery and boundaries

Extend the normal Learner handoff with the exact executable/model/parser/matcher
pins, ordered input inventory and hashes, commands/settings, build/evaluation/export
receipts, semantic comparison, journal review and immutable artifact locations.
Identify the new package as the production-scope baseline candidate. The prior
two-log acceptance package `a6d9bfcde287f2f9f3961503` is not the production model.

Learner owns model generation, authentication and its normal delivery material.
Pipeline owns application packaging, packaged defaults and integrated receiving.
Coordinate shared catalog/resource edits before writing; keep registration for
this exercise in isolated roots. Preserve retained artifacts and the exact prior
bytes/absence of files actually edited. Do not change live selections, production
catalogs, databases, configuration or running services. No historical reingestion,
external publication, commit, tag or push. A newly discovered component defect
must have a named owner and bounded disposition; this is not an algorithm redesign.

On startup/resume use only the [protected pilot](../TREKKER_CLI_PILOT_HANDOFF.md):

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot team-state learner
& $pilotNode $pilot task-show TREK-2
& $pilotNode $pilot task-show TREK-6
```

Read current checkpoints, later deliveries/receipts and linked handoffs before
acting. Link this owner-issued assignment in the current record. Keep updates
concise: result, evidence, limitation, next actor/action. Deliver on TREK-2 for
Pipeline's [baseline receiving](RELEASE_BASELINE_PIPELINE.md); Pipeline records
receipt on that same record. Its external-placement obligation belongs on TREK-6
and does not invent further Learner work after the component is received.
