# Remaining draft prompts — review before Task 06

2026-09-27. Reviewed all seven members of the supplied
`06_RUN_STORAGE_AND_NATIVE_REVIEW.zip` against Task 05's delivered interfaces and
the approved Error Contract. This is a prompt/dependency review, not execution
or approval of the later tasks.

## Recommendation for Task 06

Proceed with the [revised repository prompt](06_RUN_STORAGE_AND_NATIVE_REVIEW.md),
not the ZIP's Task 06. The ZIP contains the older version requiring diagnostic
first/last timestamps, stored rendered text, old emissions interfaces and
semantic eligibility language. The revised prompt already replaces those with
the approved contract and [Task 05 implementation](TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md).

The broader review adds three bounded clarifications to the revised Task 06:

1. **Task 07 receives a complete storage protocol.** Task 06 owns staging,
   publication, transaction completion, abort/cleanup and successful Run identity.
   Its callable interface accepts explicit input facts without depending on the
   future `PreparedInput` class. Task 07 composes it rather than recreating it.
2. **Task 08 receives sufficient stored read interfaces.** Include generation/
   schema/lineage, relationship/counter metadata, source/status filtering, ordering
   and shard-reference resolution. Stored availability is distinct from a live
   filesystem check. Rendering uses stored definitions and values.
3. **Handoffs show both consumers.** Supply a processing/storage composition
   example for Task 07 and a database-only read/render example for Task 08.
   Storage implementation choices are resolved in Task 06; operator command
   choices remain for Task 07's owner review.

These additions do not bring capture, replay orchestration, report handlers,
learner work or application cutover into Task 06. No new upstream implementation
dependency was found that prevents starting storage.

## Required updates before using the later prompts

| Draft | Keep | Change before execution |
|---|---|---|
| **07 — inputs/processing/replay** | Copy-only capture; explicit protected/manual/retained inputs; one processor; duplicate guard; fresh-generation replay; preserve the approved pure playset extraction kernel for later use. | Replace the old emissions/recovery/normalization chain with Task 05's selected package/classifier and contract preparation, then Task 06's actual APIs. Replace semantic-unresolved wording with actual no-match/review/error dispositions. Preserve the command-choice review without reopening approved record semantics. |
| **08 — reports/audit/commands** | Database-only reads and read-only audit; explicit command arguments; root CLI wiring remains later. | Render from stored definitions/values rather than expecting a stored complete-message field. Preserve template/provisional filtering, source and count meanings. Distinguish stored review availability from live inspection. Consume Task 06's generation metadata and Task 07's actual outcomes. |
| **09 — offline dependencies** | Bounded cleanup of real remaining learner/research dependencies before provider retirement. | Replace the old assignment substantially. It refers to superseded learner functions and would reconnect to historical pipeline emissions. Its fixed deletion list includes a current tool. Assign the revised learner changes to the learner team; do not make the pipeline team redesign or reconnect the learner. |
| **10 — retirement manifest** | Inspect actual callers late; exact file actions; retain required behavior at its new destination; owner review of the concrete manifest. | Treat historical pipeline emission/recovery/normalization modules as retirement candidates, not required replacement modules. Use package ID/manifest and current learner entry points. Resolve the specific dependencies named by Task 05. Earlier completed deletions and packaging work must not be repeated blindly. |
| **11 — execute cutover** | Execute the approved manifest, preserving capture/watch/configuration responsibilities and physically retiring superseded paths. | Replace the obsolete requirement that the learner use the new pipeline emission interface. Preserve shared parser/matcher ownership. Make necessary verification-consumer maintenance explicitly scoped before cutover; do not discover permission gaps halfway through deletion. |
| **12 — documentation** | Reconcile implemented facts without claiming unperformed operational acceptance. | Describe shared matching, current contract fields and real learner changes. Remove obsolete normalization-reconciliation and preserved-old-algorithm claims. Keep the final documentation sweep, while each preceding task updates its own current handoff/status. |

## Concrete Task 09 issue

The ZIP orders deletion of `tools/template_learning/evaluate_unseen_session.py`.
The current file is an active native-candidate inspection entry point: it loads
the candidate's pinned parser and calls the shared learner evaluator. It is also
documented in the learner README. Its historical filename is not evidence that
the current implementation is obsolete.

Likewise, current `learn_error_templates.py` already uses explicitly versioned
parsers and current records/artifacts; the draft's old lexer and evaluator symbols
are no longer its implementation. Applying that draft would reverse completed
work. Replace its assumptions with the actual remaining dependencies recorded in
the Task 05 handoff: `build_parser_comparison.py`'s historical baseline,
`inspect_cross_emission_recovery.py`'s old consumer check and the opt-in parser
test's removed API. Give their respective owners exact dispositions before the
dependent pipeline modules are retired. This is not a Task 06 prerequisite.

## Completion and verification gaps across the sequence

All ZIP prompts share an outdated introductory pipeline and allow in-memory
examples. Replace that common text with the actual shared matching path and the
owner's genuine-input-only verification rule. Their completion clauses also
require response-only handoffs. Future revisions should require durable handoff
files and current status updates, as revised Task 06 already does.

Task 11 explicitly stops at source cutover and leaves independent acceptance
unperformed; Task 12 only edits documentation. Thus the set has no assigned final
end-to-end acceptance after CLI wiring. Recommend a separately explicit disposable
native-log check after cutover: installed CLI → processing → SQL plus shard →
reopened database-only reporting/audit, duplicate handling and preserved originals.
It must remain distinct from production activation or live watcher operation.
This needs assignment later, not implementation inside Task 06.

These prompts are a replacement/cutover sequence, not complete Trusted Run product
acceptance. Broader retention, backup/restore and live-operation acceptance remain
separate obligations unless explicitly assigned. Do not grow Task 06 into those
features or allow final documentation to imply they were delivered.

Only the repository Task 06 proposal and this review were changed. ZIP drafts,
source code, selected resources and runtime evidence were not modified. Remaining
prompts should be revised before their individual execution, using each actual
predecessor handoff.
