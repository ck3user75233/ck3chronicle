# Launch & Distribution — complete manual structure and editorial review

Prepared for Owner issuance, 2026-10-12. **Part 2 of the manual revision.**
Checkout: `C:\Users\nateb\Documents\ck3chronicle`.
Owner: **Launch & Distribution, documentation role**. Continue **TREK-11**,
preserving its prior receipts. This is the same Owner-requested manual revision
as Part 1, not a new numbered work package or duplicate tracker record.

## Outcome and authority

Perform a fine-tooth-comb review and edit of the **whole user manual**, not just
the introduction or the quoted examples. Deliver a coherent user guide with a
table of contents, clear conceptual progression, accurate explanations and
practical instructions. Remove internal delivery/acceptance commentary and
feature-absence boilerplate. Preserve useful safety instructions and exact
operational meaning.

The Owner authorizes editorial revision of all canonical user pages, including
previously received `WORKFLOWS.md` and `EXTERNAL_DATA.md`. Their prior receipt is
not a reason to leave poor wording or stale version labels untouched. Preserve
the old frozen editions and execution evidence; publish new document identities
for this revision. Keep actual historical example provenance in the internal
handoff instead of repeatedly explaining receiving history to users.

This is documentation work. It does not authorize implementation of roadmap
items, ingestion redesign, production changes, service/startup registration,
new model builds, new acceptance campaigns, Git publication or activation.

## Retrieve and coordinate

Read root instructions, current plan/status/handoff, product intent and governance;
the original `10D_PRODUCT_REFERENCE.md`, `WORKING_AGREEMENT.md`,
`MANUAL_01_PRODUCT_INTRODUCTION_AND_ORIENTATION.md`; the current documentation,
distribution and Task 10 receiving handoffs; and every file under `docs/user/`.
Review linked bundle-facing installation/release text for consistency as well.

Retrieve current `team-state launch-distribution` and TREK-9/10/11/12/15/16 through
the absolute protected helper and canonical store in the pilot handoff. Use
`C:\Program Files\nodejs\node.exe` and
`C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs`, serially.
Refresh later comments before final delivery. Existing completion of 10D/10E
does not cancel this newly Owner-requested editorial revision. Continue/reopen
TREK-11 for the combined manual revision; keep TREK-15's original execution
receipt and scope history intact.

Integrate Part 1's three opening pages and give them the same editorial scrutiny
as the rest. Begin independent inventory/review while they are being written;
take over shared pages only at the documented handoff. Do not have two chats
editing the same file. Do not wait for upstream dependency downloads to edit the
manual; provenance work remains 10B's responsibility.

## Required work order: inventory, classify, recommend, edit, then review

Complete the negative-construction pass first so the later structure, factual
accuracy and first-time-reader reviews can focus on their own questions. The
inventory and recommendations are an internal working artifact, not an extra
Owner approval gate. Launch & Distribution reviews them and proceeds with the
authorized edits. Preserve the original page snapshot and inventory before edits.

### 1. Identify all candidates systematically

Inventory every manual page and bundled user-facing document, including prose
in tables, notes, captions, alt text and explanatory code comments. Record the
file set/revision examined and account for every page, including pages with no
findings. Incorporate Part 1's new pages when received. Do not restrict the pass
to the examples quoted by the Owner.

Use either bounded sub-agent review or a suitable prose linting tool to produce
an exhaustive candidate inventory, supported by a broad text search. The Owner
explicitly permits sub-agents for this review and classification. Give reviewers
disjoint document sets or clear review roles; they return findings rather than
independently rewriting shared files. Launch & Distribution remains responsible
for coverage and decisions. No separate team dispatch or new tracker enrollment
is needed for these subtasks.

If using a linter/library, first research established prose-linting tools and
documented practices using primary documentation. Record the selected tool,
version, rules, configuration and coverage limits. Prefer existing tooling or a
small documented rule set over inventing a grammar engine. Keep review tooling
outside product dependencies. A regex search can collect candidates but cannot
establish grammatical or semantic completeness by itself.

Find explicit negatives (`no`, `not`, `never`, `without`, contractions such as
`doesn't`/`cannot`) and implied absence/process language (`lacks`, `unavailable`,
`unsupported`, `unimplemented`, `pending`, `awaiting`, `unverified`, `yet to`).
Read surrounding context and perform a full-page sweep to catch paraphrases and
multiline sentences. Preserve literal command syntax, code and genuine output;
mark non-prose matches rather than treating them as editorial instructions.
Tool hits are candidates, not automatic defects or proof of complete coverage.

### 2. Categorize and recommend before rewriting

For **every candidate**, record its file, section and original line locator;
exact wording and enough surrounding context; category; recommended disposition;
reason; and proposed replacement/destination where applicable. Keep original
locators stable even after editing. Split mixed-purpose sentences into clauses
or give them secondary categories instead of hiding a safety instruction within
a paragraph marked for deletion.

Use these categories:

| Category | Meaning |
|---|---|
| User instruction | An action the user should avoid or a precaution, such as "Do not use immutable=1 against a live database." |
| Negative feature/function descriptor | A list or description of functionality ck3chronicle does not provide. |
| Internal development/receiving commentary | Work not performed, checks not run, pending review/acceptance or internal next steps. |
| User-facing interpretation or operational constraint | A meaningful distinction needed to interpret results or understand effects, rather than an absent-feature list; for example, an unresolved source reference is not proof of which mod caused the error. |
| Non-prose match / false positive | Syntax, literal output or wording that the detection method matched but which is not a prose issue. |

Choose and justify a concrete recommendation per item: **keep useful instruction**;
**keep necessary interpretation/constraint**; **remove entirely**; **rewrite
positively to explain what the user can do**; **move a positively worded feature
idea to Planned Features**; **move valid internal evidence/status to the technical
handoff**; or **leave literal code/output unchanged**. Multiple actions can apply
to separate clauses. An unsupported factual claim needs correction, not merely
relocation; record that separately in the factual-errata register below.

Sub-agents may propose categories and recommendations. **The Launch & Distribution
lead must check every category and disposition**, including retained findings
and false positives, for intent, technical accuracy and preservation of user
instructions. Record corrections to reviewer decisions. The Owner does not need
to approve each row; raise only a material scope question that current direction
and source evidence cannot resolve.

### 3. Apply, rescan and account for the results

Apply the reviewed dispositions. Record the actual replacement or removal and
final location against each original finding. Keep required warnings intact;
do not turn removed absence statements into unsupported roadmap commitments.
Rerun candidate detection and the contextual review on the edited manual,
including newly written prose. Account for every remaining negative as an
intentional retained item, false positive or explicit unresolved issue. Success
is appropriate wording with complete review coverage, not zero negative words.

Report pages reviewed, candidates by category, actions taken and unresolved
items. Save the inventory, lead-reviewed recommendations and final dispositions
with the internal documentation evidence; link them from the documentation
handoff. Then perform the distinct factual/architecture, structure/navigation
and end-to-end reader reviews below. Known factual errors must be corrected
before their surrounding text is approved, even if discovered in the first pass.

## Structure and navigation

Make `docs/user/README.md` the actual **table of contents page**, with descriptive
section headings, numbered reading order and useful subsection links. A small
"You want to..." shortcut table may supplement it, not replace it.

The first sections must be:

1. **Product Version** — Part 1's `PRODUCT_VERSION.md`.
2. **Introduction** — purpose, audience and use cases in `INTRODUCTION.md`.
3. **Orientation to ck3chronicle** — components, Run contents, templates,
   packages and the end-to-end journey in `ORIENTATION.md`.

Follow with installation/launch (including any accurately documented optional
Windows startup route), everyday workflows, understanding diagnostics/reports
and source context, external data access, configuration, command reference,
advanced model/Learner administration, troubleshooting, and **Planned Features**.
Group the existing pages sensibly; create another page only when it improves
navigation. A compact glossary or linked definitions should cover Run ID,
Capture ID, template, binding/value, occurrence, playset, package ID, manifest
pin, review shard and handler before those terms are used without explanation.

Use consistent heading levels, descriptive links and return-to-contents links.
Place screenshots next to the user action they explain. Validate all local links
and anchors after reorganization. Move wizard details to Installation. Keep
advanced catalog/training commands behind the explanations needed to use them.

## Editorial disposition examples

Use these examples to guide the item-by-item decisions above; they are neither
the complete inventory nor blanket deletion rules.

| Current kind of wording | Required treatment |
|---|---|
| "Final distribution acceptance is pending"; workflow/reference receiving distinctions; team/Trekker obligations | Remove from public prose; keep actual status/evidence in the internal handoff. A user's operation must not require interpreting our development process. |
| "It describes implemented commands"; "These instructions describe delivered behavior" | Delete the self-evident claim. Use the space to explain purpose, prerequisites or outcome. |
| "This release has no flattened CSV/XML exporter, visualization connector or combined diagnostic/review dataset" | Explain the available SQLite/JSON route positively, including how users can select/reshape data. Do not turn every removed absence into a promised feature. |
| "This guide does not modify, migrate or repair a database" | Delete the claim about what a document cannot do. Explain the actual read-only operation and user precautions where relevant. |
| "This edition does not provide a snapshot-export command or a complete application backup/restore procedure" | Move the feature ideas into Planned Features as positive user outcomes with truthful planning status. Keep the separate warning about copying a live database safely. |
| "This release has no NiceGUI investigation dashboard" | Describe a future interactive investigation interface in Planned Features. Do not bind the product to NiceGUI as a decided framework or imply it ships now. |
| Owner paths, agent workspace locations, candidate/receipt hashes and test-performer commentary in task instructions | Use portable user examples and concise version applicability. Preserve detailed provenance internally. Keep genuine command output truthful and identify any substitutions/truncation. |

Retain the Owner's explicitly approved database safety instructions, including:

> Use a local tool that honors SQLite's URI/read-only settings. Do not open with
> ordinary writable defaults, change schema/content or turn off locking. Do not
> use `immutable=1` against a live database.

Retain similarly necessary instructions about immutable model files, exact
configuration selection, independent handler shutdown, interpreting counts,
retention and preservation of user data. Feature-absence boilerplate is different
from an instruction that prevents a damaging or misleading operation.
State actual effects positively where possible; never remove a material effect
or limitation just to satisfy a style rule.

## Separate factual and architectural errata review

The sentence **"concurrent-writer timing was not tested" is a factual terminology
error for the supported application architecture**, not an outstanding
concurrent-writer acceptance check. Correct it in a separate factual-errata
register. Do not preserve the misleading claim by moving it into an internal
handoff, or use it as the example that defines the negative-construction problem.
Its words may still be caught by the mechanical scan; cross-reference the
factual correction rather than treating grammatical cleanup as sufficient.

Explain **one request queue and one serial database worker per database**.
Distinguish concurrent request clients from writers. External read-only tools
may read while the application's single writer is active; keep short-transaction,
locking and busy/retry guidance. Do not falsely infer that serialized application
writes make reader interference or unsafe live file copies impossible.

If original execution evidence establishes only an idle-database external read,
record exactly that internally. External-reader overlap with the **single**
application writer is a different condition; describe it only when relevant and
supported. Do not invent an unperformed multiple-writer test or a new requirement.
For every factual erratum, record the erroneous claim, authoritative source,
corrected explanation and affected pages independently of the style decision.

## Planned Features

Create one dedicated, plainly labelled section/page for future direction. Explain
the benefit of each item in positive language, for example:

- Near-match assistance for missing keys/undefined tokens, helping spot typos,
  misspellings and nonexistent identifiers in generated code.
- Snapshot export for a consistent portable copy of stored evidence.
- Guided application-data backup and restore.
- An interactive interface for investigating Runs, diagnostics and source context.

Use the Owner's current direction and product vision to distinguish planned
direction from ideas still under consideration. No invented delivery dates,
approved designs or implementation commitments. A roadmap entry is not a new
Task 10 acceptance requirement. Keep current source-context capability in the
current-feature explanation, not on the roadmap.

Removing a sentence about absent flattened exports, connectors or unified
diagnostic/review views does **not** automatically approve those features.
Respect previously settled scope and banned designs. The separately deferred
ingestion design remains outside this documentation assignment; do not advertise
it as shipped or restart that implementation discussion.

## Full-manual consistency and verification

Confirm version applicability against the received application (0.0.3 at
preparation) and the exact build intended for delivery. Do not falsely relabel
old observed output as a fresh execution. Present reusable examples as examples
with relevant version/schema facts; store original C9 execution provenance in
the internal evidence map. Explain a version distinction only when it changes
what the user must do or how a result should be interpreted.

Include `PIPELINE_REFERENCE.md` and `DISTRIBUTION_REFERENCE.md` in the inventory.
Resolve duplicate producer-reference material deliberately: integrate useful
user content into the canonical manual or clearly separate internal source
contributions from user-facing distribution contents. Coordinate packaging
changes with 10B; do not leave a polished index leading to unedited internal
pages elsewhere in the same ZIP.

Review every example's syntax, option order, prerequisites, effects and expected
result against existing delivered code/help and genuine evidence. Reuse accurate
execution evidence for unchanged examples. Do not start a handler through a
nominal read-only probe, manufacture tests or rerun workflows merely for prose
changes. If a changed procedure needs fresh execution, identify the exact affected
step for 10C; continue the rest of the edit.

After closing the negative-construction pass, keep an internal review matrix in
`docs/task10/DOCUMENTATION_HANDOFF.md`: page,
editorial problems corrected, technical facts checked, examples retained/changed,
evidence source and any remaining concrete issue. A mechanical link check is
necessary but insufficient. Read the manual in TOC order as a first-time modder
and revise jargon, unexplained concepts and abrupt command dumps.

Before delivery verify that a reader can explain why to use the product, what
happens from CK3 exit to report, what a Run contains, why template values and
package pins matter, how source context works, and how to install/start/stop and
inspect results. The public guide must stand alone without Task handoffs.

## Delivery and receiving

Deliver the edited manual, Part 1 integration, functioning TOC and a new frozen
manual edition with exact document hashes and packaging inputs. Preserve 10D-r2,
C9/C10 and their receipts unchanged; update canonical user pages and create a
new snapshot rather than editing a received frozen artifact in place.

Deliver the negative-construction inventory, lead-reviewed item recommendations,
actual dispositions/rescan results and separate factual-errata register as
internal review evidence. State which files and revisions were covered and any
remaining gaps; keep these editorial records out of the bundled user manual.

Record the combined revision on **TREK-11** and deliver the exact new input set
to **10B / TREK-10** and **10C / TREK-16**. The final bundle must include this
Owner-requested replacement manual; do not silently ship the earlier freeze.
10B owns bundle assembly and 10C owns final installed-guide receiving. Editorial
changes do not require another trained model or application wheel unless an
actual owning code change is separately delivered.

Finish with a short Owner-facing account of the restructuring, representative
before/after corrections, exact manual entry link and any genuinely unresolved
user-facing fact. Keep acceptance status, execution limits, artifact receipts
and outstanding team actions out of the literal user guide.
