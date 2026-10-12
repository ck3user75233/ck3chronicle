# Task 10D — Product reference

**Owner: Launch & Distribution — Docs role.** Finalized for owner issuance.
**Trekker ID: TREK-11.** Owner-issued 2026-10-08. Follow the [common instructions](WORKING_AGREEMENT.md)
and [scope/index](../TASK10_DELIVERABLES.md).

Issued component contributions: Watcher **TREK-12**, Data Intelligence **TREK-13**,
Learner **TREK-14**. Exact sections, evidence and receipt status are in the
[documentation coverage handoff](../task10/DOCUMENTATION_HANDOFF.md).

## Outcome

Deliver a coherent, release-specific reference for every supported product CLI
and behavior-controlling configuration surface. A user should not need to read
component handoffs or reconstruct past conversations to understand a command.
Documentation is part of the product, not another restatement of task history.

## Component contributions and editorial ownership

Each feature team owns its technical reference content and updates it when its
interface changes. Docs owns the manual's structure, terminology, accessibility
and cross-component consistency, and verifies the examples from a user's position.
An existing component handoff is evidence/input, not automatically a finished
user-facing reference. Do not reverse-engineer missing semantics and silently
attribute them to a component owner.

Pipeline's 10A.1 delivers reference drafts for configuration, database/access,
selection and application commands; 10B delivers setup/distribution/launch drafts.
Watcher owns capture/lifecycle controls, Reporting owns queries/report JSON and
output interpretation, and Learner owns supported learning/release commands and
release-bound rules. The issuance plan includes a bounded documentation assignment
to each of those three teams using the [component contribution prompt](COMPONENT_DOCUMENTATION_INPUT.md),
alongside 10D. Retrieve their existing material and actual contribution records;
coordinate technical details directly after owner issuance. They can supply drafts
while you organize the manual, without waiting for a completed framework. If an
assignment has not been issued, name that missing dispatch to the Owner and continue
independent work. A comment does not dispatch a team or reopen completed Task 09.

Receive contributions on their producer records and link their actual IDs here
and in the coverage handoff. Prepare a concrete owner-assignable continuation only
for additional scope beyond the issued contributions. Do not make the Owner relay
drafts or technical answers between active assigned chats.

Maintain a compact inventory in the documentation handoff: interface/section,
technical owner, contribution or existing source, documented release, example and
verification status, and any outstanding discrepancy. This is content coverage,
not another progress tracker. Current action/receipt remains on the real record.
For changed/new interfaces require the owning producer's explicit technical
delivery or review disposition. Unchanged documented facts can reuse applicable
evidence without another generic sign-off cycle.

Start with a current interface inventory: installed application entry points,
subcommands, retained Learner and model administration CLIs, report-query JSON,
TOML configuration, model selection/catalog interfaces and other user-controlled
files. Account for every discovered entry point as supported user/admin interface,
developer-only utility, generated state or immutable implementation resource.
Do not silently omit advanced supported commands, or imply every internal script
and JSON file is a supported user control.

Draft against the delivered Task 09 baseline now, clearly labeling implemented
behavior. Refresh [10A.1](10A1_PIPELINE_INTERFACES.md) and [10B](10B_DISTRIBUTION.md)
before describing their changed setup/CLI interfaces as delivered. 10A supplies
the intended journey; executable help/parsers and technical handoffs supply facts.

## Reference contents and edit boundary

Create the user manual under `docs/user/`, with an index, `CLI_REFERENCE.md` and
`CONFIGURATION_REFERENCE.md`; split further only where it aids reading. Coordinate
shared index/README edits with 10E and 10B. README provides orientation and links
to the manual rather than reproducing the whole reference. Keep technical evidence in
`docs/task10/DOCUMENTATION_HANDOFF.md`, not in the user's instructions.

For each supported CLI cover purpose/audience, syntax and subcommands, argument
meaning/types/defaults, required inputs, outputs/formats, exit behavior, side effects,
configuration precedence and at least a meaningful example. Distinguish read-only
queries from commands that create state, ingest, publish or activate a selection.
Use installed-product commands and user-chosen paths; no dependency on Nate's
checkout, agent workspaces or development venv.

For editable configuration cover field meaning, accepted values, required/default
behavior, relative paths, validation, when changes take effect and restart needs.
Include reporting query JSON, not just installation settings. Explain generated
catalog/selection files and supported ways to change them. Authenticated model,
Learner, rule and manifest payloads are not ordinary runtime-editable settings;
document their release-bound nature without commissioning a rule editor.

Use task-relevant examples and link 10E workflows instead of duplicating them.
Where descriptions would contradict implementation or owner intent, identify the
exact discrepancy and owner; do not fix code or redefine behavior through prose.
NiceGUI and proposed future commands must not be advertised as available.

## Verification and receiving

Cross-check every supported command and configuration field against the exact
delivered version and owning reference/validation. For each documented command or
subcommand give a meaningful example and an explicit evidence status: freshly
executed, applicable prior execution reused, or unexecuted with the reason/limit.
Full reference coverage does not require every flag combination or a repeated
expensive model build. Help output establishes syntax, not the command's effects.

Actually exercise representative installed commands for the core journeys with
genuine inputs, coordinating execution with 10E/10C to avoid duplicate runs. This
assignment permits documented read-only operations and ordinary setup, selection,
captured-input ingestion and report-output examples only in task-owned isolated
configuration/storage through supported interfaces. Reuse producer receipts for
expensive build/release operations rather than rerunning them for a screenshot.
No production publication/activation, live-service interference or synthetic tests.

For each executed example retain the exact product identity, command, prerequisites,
input references, expected outcome, actual stdout/stderr/exit status and relevant
files/database effects. Inspect the claimed result: ingestion needs stored-result
evidence, and a configuration example needs evidence of the effective setting.
Do not treat a success message or screen capture alone as proof of the outcome.

Prefer copyable command/output snippets for CLI examples. Use real screenshots
where visual layout helps (setup, HTML report or external database browser), with
context and alt text. Never invent or recreate a screen as execution evidence.
Remove private paths/data from public examples, label substitutions/truncation,
and retain the original genuine evidence privately outside Git. Include only
necessary sanitized excerpts/assets in the manual, not raw captured logs.

Deliver the reference and interface-coverage inventory on this record, including
the exact product revision, component contributions, worked-example evidence and
any unresolved factual gap. A required core workflow cannot be called verified
merely because its missing run is listed; name the remaining owner/action in Trekker.
[10C](10C_ACCEPTANCE.md) uses the manual against the installed distribution and
records receipt here. Documentation defects remain here; code defects retain
component ownership. Close on actual receipt, not on the number of pages written.
