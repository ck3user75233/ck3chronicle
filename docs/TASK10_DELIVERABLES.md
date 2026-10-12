# Task 10 — Setup, distribution and product documentation

Finalized for owner issuance, 2026-10-07. Launch & Distribution leads Task 10.
The six main prompts and bounded contribution prompt are execution authority
only when issued by the Owner.
This index is scope, assignment and ID navigation; live progress belongs in Trekker.

Owner clarification, 2026-10-12: use the existing working Python/ripgrep payloads.
Additional upstream verification/downloads are not required for Task 10 and must
not block final packaging/acceptance. GitHub access is intentionally restricted;
do not request it for this purpose. See the updated [10B instructions](task10-deliverables/10B_DISTRIBUTION.md)
and [10C instructions](task10-deliverables/10C_ACCEPTANCE.md). Normal local bundle
identity checks and installed-product acceptance remain, along with the newly
Owner-requested manual revision on TREK-11.

## Assignments and recommended issuance

| Assignment | Owner | Independently useful outcome | Dependencies / receiving | Trekker ID |
|---|---|---|---|---|
| [10A — First-use design](task10-deliverables/10A_FIRST_USE_DESIGN.md) | Launch & Distribution | Concrete setup/launch journey and configuration/packaging interface agreement | Issued 2026-10-08 to Launch & Distribution; erroneous parallel chat halted by Owner. [Design proposal](task10/FIRST_USE_DESIGN.md); Pipeline receives the technical interface on this same record. | TREK-7 |
| [10A.1 — Application interfaces and artifact](task10-deliverables/10A1_PIPELINE_INTERFACES.md) | Pipeline | Working central configuration/initialization/selection interfaces and an authenticated application wheel | Issued 2026-10-08; consumes TREK-7 technical agreement. Launch & Distribution receives. | TREK-9 |
| [10B — Standalone distribution](task10-deliverables/10B_DISTRIBUTION.md) | Launch & Distribution | Runnable Windows distribution, setup/launch entry points and installation instructions | Issued 2026-10-08; consumes TREK-9. Received by integrated acceptance in 10C. | TREK-10 |
| [10D — Product reference](task10-deliverables/10D_PRODUCT_REFERENCE.md) | Launch & Distribution — Docs | Versioned CLI/configuration reference, component-owned contributions and verified examples | Issued 2026-10-08; consumes TREK-9/TREK-10 interfaces. Coverage: [documentation handoff](task10/DOCUMENTATION_HANDOFF.md). | TREK-11 |
| [10E — Workflows and external data access](task10-deliverables/10E_USER_WORKFLOWS.md) | Launch & Distribution — Docs | Exercised task guides, basic external SQLite access and separate review-shard reading instructions | Issued 2026-10-08; consumes TREK-9/10/11, coordinates genuine examples with 10D. | TREK-15 |
| [10C — Integrated acceptance](task10-deliverables/10C_ACCEPTANCE.md) | Launch & Distribution | Evidence that a user can install and use the exact distribution by following its documentation | Issued 2026-10-09; receives 10B/10D/10E and 10A.1. [Receiving handoff](TASK10_HANDOFF.md) distinguishes passed C9 checks from final bundle/environment obligations. | TREK-16 |

Issue **10A and 10A.1** first so design and technical review can exchange information
directly; 10A.1 may review/preflight before implementation prerequisites are ready.
Issue **10D plus the Watcher, Reporting and Learner documentation contributions**
in parallel; use the same bounded contribution prompt for each named recipient.
They can supply existing accurate content and identify gaps while Docs structures
the manual. Pipeline's contribution is already in 10A.1; setup/launch content is
in 10B. Issue 10B after a usable setup/interface
agreement; 10E can then verify its drafted workflows. Issue 10C when the distribution
and guides are ready for integrated use. Letters identify work packages, not a
requirement to finish C before starting D or E.

Five main outcomes plus one technical producer assignment preserve the agreed
team boundaries. Do not automatically add a ticket for each module or team. A
concrete required Watcher/Reporting/Learner change gets a bounded owner-issued
assignment if outside these prompts; no team silently repairs another component.

## Governing owner direction

The Owner accepted Launch & Distribution leadership after asking whether it should
lead setup design/testing (Advisory conversation, 2026-10-07: "OK, and I think we
might need to slide in an additional task or set of tasks"). This Task 10 boundary
qualifies [existing governance](team-governance/README.md): Pipeline retains the
application wheel, internal dependencies/resources, configuration/database APIs
and runtime composition; Launch & Distribution owns the outer downloadable
distribution, setup/launch experience, installation acceptance and product manual.
There is one implementer for each shared change. Pipeline remains Task 09's owner.

The same conversation requests documentation for all CLIs, behavior-controlling
JSON configuration and user workflows, including external visualization tools.
The Owner then accepts MVP external access requiring users to reformat data and
states: "we don't need to set up infrastructure that let's them display all in one
view, including the review shard". Thus basic documented SQLite access is required;
new flattened CSV/XML exports, visualization connectors and a unified diagnostic/
review-shard dataset are not requirements. Explain shards separately and how to
view them. This is a scope boundary, not a future unified-view commitment.

The Owner explicitly moved physical outside-repository installation verification
from Task 09 to Task 10; it is required here. NiceGUI remains a possible later
product interface, not commissioned by these assignments. A text-based guided
setup is acceptable; do not turn setup into an investigation dashboard.

[The earlier Task 10 draft](TASK10_PROMPT.md) supplies the underlying first-use
requirements. These owner-qualified prompts supersede its recommended Pipeline
lead and any conflicting scope/sequence. No new learning, model redesign or corpus rebuild.

### Owner correction — paths and config doctor, 2026-10-08

The Owner requires useful setup assistance and meaningful diagnosis. All external
root settings are editable and specific to the user's machine. Setup may suggest
bounded standard Steam locations and Windows-resolved Documents locations, check
them and require individual Yes/Accept for each field. Only the external game/mod/
log contents remain read-only. This qualifies older blanket root-discovery bans
for setup assistance; runtime config-file authority and no silent fallback remain.

The existing doctor must report missing or suspicious setup, evidence, likely
consequences and corrections, including whether a configured directory actually
looks like CK3. Pipeline owns shared validators/doctor; Launch & Distribution owns
the guided confirmations. Expect the logs directory; allow setup without a current
error.log. This supersedes the initial optional/limited doctor description. Exact
design and receiving obligations are in [10A](task10/FIRST_USE_DESIGN.md#path-suggestions-and-meaningful-configuration-diagnosis),
10A.1, 10B and 10C. These are design corrections, not delivered software behavior.

## Documentation ownership and acceptance

The Owner accepted the shared documentation model in the Advisory conversation,
2026-10-07: "ok, go for it, strengthen / finalize the prompts". Component teams
author and maintain technically correct feature references/examples alongside
changes. A Docs role within Launch & Distribution owns the coherent manual and
user-oriented verification; this is not a new permanent team or Trekker team tag.
10C checks the final installed product by following that manual.

Pipeline's 10A.1 and the 10B implementer must deliver their reference contributions
with their interfaces. Watcher, Reporting and Learner each receive the
[bounded component contribution prompt](task10-deliverables/COMPONENT_DOCUMENTATION_INPUT.md)
for their respective public interfaces in this initial documentation pass. The
Owner accepted this explicit issuance sequence in the Advisory conversation:
"ah ok sounds good". These are substantive documentation contributions, not
generic sign-off tickets. Reuse accurate existing content and execution evidence.
Launch & Distribution coordinates and receives the issued work through Trekker;
it does not dispatch teams. Further out-of-scope work gets a concrete continuation
prepared for owner issuance. Documentation remains in Task 10, not Task 11.

Every supported interface is accounted for in the reference, while worked examples
identify fresh execution, applicable reused evidence or unexecuted limits. Core
user journeys are exercised. Record actual commands, release/input, expected and
observed output and relevant state changes. Use copyable CLI snippets and genuine
screenshots where they aid visual navigation, with sanitized public examples.
Neither help output nor a screenshot alone proves the command's effects. Full
flag-combination coverage, repeated model builds and unapproved synthetic cases
are not requirements. 10C verifies the final guides without undocumented fixes,
preferably through an acceptance chat other than the author; disclose actual roles.

### Bounded component contributions

Issued 2026-10-08 alongside 10D using the shared contribution prompt:

| Recipient | Required contribution | Trekker ID |
|---|---|---|
| Watcher | Capture/watch commands, settings, lifecycle effects, source timestamps/playsets and processing controls; [contribution](task10/WATCHER_DOCUMENTATION_HANDOFF.md) | TREK-12 |
| Data Intelligence | Runs/report commands, query JSON, filters/presets, formats and interpretation; [contribution](task10/DATA_INTELLIGENCE_CONTRIBUTION.md) | TREK-13 |
| Learner | Supported learning/release commands, inputs/outputs, identities and release-bound configuration/rules; [contribution](task10/LEARNER_DOCUMENTATION_HANDOFF.md) | TREK-14 |

Each receives only its named component scope. Populate actual returned IDs on
issuance/enrollment and link them from 10D. Technical evidence and section coverage
belong in the documentation handoff; progress stays in Trekker. Do not create
duplicate Pipeline/setup contribution records for obligations already in 10A.1/10B.

## Baseline, publication and shared documents

Consume the [Task 09 baseline](TASK09_RELEASE_BASELINE.md) and actual TREK-6 receipt.
TREK-6 CMT-69 records completed source publication. On 2026-10-08, 10A independently
verified local HEAD and tag `task09-baseline-2026-10-07` both resolve to
`709ea7842a0202c420b43355b18be91d8ca196a3`; remote push is the producer's recorded
receipt. Final distribution must identify the actual source and received pins.
Physical external installation remains unperformed, assigned to 10B/10C.

Task 10 does not silently change the approved model/Learner or historical Run
lineage. Changed application bytes require a new identified artifact with explicit
correspondence to the baseline; retained releases stay immutable.

Task 09's staged-publication freeze ended with CMT-69. Launch & Distribution
coordinates the agreed governance/Task 10/current-plan pointer alignment on TREK-6
and preserves dated history and unrelated work. Refresh producer records before
shared edits; that alignment does not require another approval of settled ownership.

## Trekker use and owner-facing review

Follow the [common assignment instructions](task10-deliverables/WORKING_AGREEMENT.md).
10A is issued and enrolled as **TREK-7**; 10A.1 as **TREK-9**; 10B as **TREK-10**; 10D as **TREK-11**; 10E as **TREK-15**; 10C as **TREK-16** (issued 2026-10-09).
The three component contributions are issued as **TREK-12/13/14**. Preparation is not dispatch;
the delivered pilot prohibits enrolling unassigned Task 10. On first owner issuance,
the assignee creates or locates its one real record, writes its returned ID into
this index and its prompt, then tracks that assignment. No fabricated IDs and no
new helper/status system. All queries use the delivered protected helper.

Dependency links are **10A.1 → 10A; 10B → 10A.1; 10D → 10A.1 and 10B for final
accuracy; 10E → 10A.1 and 10B for final workflow verification; 10C → 10B, 10D, 10E**.
Here `X → Y` means X consumes Y. Add actual native edges when both records exist;
before then name the prerequisite prompt in the record, without enrolling it early.
These are delivery dependencies: usable partial delivery permits the stated
parallel work. Receipt does not wait for a circular demand that the producer must
already be marked completed. Ready queries never dispatch work.

For documentation convergence, 10B first supplies a usable installed candidate
with settled commands/layout. 10D/10E verify against that delivery and freeze their
manual revision; 10B then includes it in the final bundle, and 10C receives that
exact bundle. Do not require the final bundled manual before releasing the earlier
candidate that its authors need to verify it.

Launch & Distribution gives a short owner brief at the first interface handoff,
before integrated installation, and at final receiving, plus actual scope/conflict
decisions: delivered/received result; strongest evidence and limit; remaining owner
and next action; decision needed or "none". Advisory can review these meaningful
convergence points when asked/resumed; no mandatory Advisory gate, timed monitoring
or automatic chat notification is introduced. The Owner need not read every update.
These operating instructions apply the [Task 09 usefulness review](TREKKER_PILOT_USEFULNESS_REVIEW.md)
without creating another tracker, notifications system or process KPI.

Completion means the agreed product/distribution/docs are received and limitations
are visible. A final brief separates implemented, verified, owner-accepted, locally
packaged, source-pinned, uploaded and live-activated facts. Never advertise a
prepared script or proposed publication as executed. No push, upload, source
commit/tag or live upgrade is authorized merely by preparing these prompts.
