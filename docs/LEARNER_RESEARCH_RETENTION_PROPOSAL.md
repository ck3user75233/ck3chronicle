# Learner research retention proposal

Later on 2026-10-09, the Owner separately directed removal of the remaining
42.79 GB research payloads in `learner-refactor`; that cleanup is now completed
in the linked receipt. The backlog measurement below is historical. The proposed
future policy, windows and budgets remain unadopted and unimplemented.

2026-10-09. **Proposal for Owner decision; not implemented or an automatic
deletion policy.** The [urgent cleanup receipt](LEARNER_RECLAMATION_RECEIPT_20261009.md)
records the separately authorized removals already completed.

## Protect dependencies before applying age or size

Keep production selections, published releases, rollback artifacts, active build
bases, receiving evidence and their required transitive dependencies. A release
may embed everything needed for runtime yet still have a separately required
research/evaluation source; record which obligation requires the full bundle.
Protect original/canonical training inputs independently of disposable outputs.
Runtime evidence and Trekker remain under their own authorities and exclusions.

Each experiment should name an owner, task, input inventory, executable identity,
candidate lineage, consumers, storage size and current disposition. Record whether
each consumer needs the entire authenticated bundle, particular native evidence,
or only a published report. A historical citation does not automatically require
all payloads forever; unresolved active investigations do require the evidence
they actually consume. Unclear dependencies remain protected until resolved.

## Closure and expiry

| Output | Proposed retention after closure | Required clearance |
|---|---|---|
| Superseded intermediate model/native payload | 7 days | Successor received; no selected registry base, required comparison, active investigation or published-evidence obligation depends on it |
| Final unpromoted research bundle | 30 days | Owner/receiver disposition recorded, findings delivered, full-evidence needs resolved or assigned explicit protection |
| Production/rollback or receiving baseline | No age-based expiry | Explicit release/evidence retirement with dependent consumers accounted for |
| Original/canonical training input | No research-output expiry | Separate input-retention decision; never infer redundancy from filename |
| Feature cache | Separate future proposal | Prove identity-bound regenerability from retained original input and executable; caches are outside this assignment's deletion scope |
| Manifest, input/hash inventory, report, script pin, receipt and removal notice | Indefinite compact record by default | Review individually if metadata/report growth becomes material |

Closure means the relevant delivery/receipt and outstanding findings have an
explicit disposition. A completed process, newer algorithm number or completed
tracker status alone does not close evidence obligations. At expiry, perform a
manual dependency review; expiry creates a candidate for cleanup, not permission
to delete. An extension records the exact use, responsible owner and next review
date. Never relabel unresolved outcomes as successful to obtain expiry.

Before deletion, freeze the explicit-file inventory, freshly hash against the
manifest, verify paths/identities and refuse links/reparse points. Preserve enough
summary and provenance to explain the experiment. After deletion, record actual
bytes/failures and add a removal notice without changing the original manifest.
State plainly that a retired bundle is no longer fully loadable/authenticated.
If later work needs full replay, its reconstruction is new work requiring its own
scope; do not promise exact reproduction from partial artifacts.

## Proposed storage budgets and review cadence

Use separate accounting for protected evidence/inputs, disposable research
payloads, caches and compact reports. Do not charge an indispensable input or
production artifact to a budget that would implicitly authorize its deletion.

- **Per unpromoted experiment:** plan for at most 5 GiB of generated model/native
  payloads. Record expected peak size before running a larger campaign, with the
  useful result, temporary copies and planned closure disposition.
- **Disposable generated research payload pool:** 20 GiB soft budget; at 30 GiB,
  pause new discretionary campaigns until the owner accepts an exception or
  dependency-cleared cleanup restores headroom. Budget pressure never deletes
  protected material or interrupts an active build automatically.
- **Compact reports/metadata:** 2 GiB soft budget, with a size review for any
  single report exceeding 100 MiB. Keep native witnesses necessary to explain
  unresolved findings; prefer references to retained canonical evidence where
  usable, not unauthenticated compression or silent omission.
- **Cadence:** measure at campaign start and closure, with a weekly manual review
  while research is active. Compare actual peak/final sizes to estimates and
  list the largest dependency-cleared candidates first.

These are initial planning values, not measured capacity guarantees. After this
cleanup, model/native payloads alone still total 42.80 GB in learner-refactor;
they include material not cleared for retirement. Classify that existing backlog
before applying the proposed pool cap. Any larger retained set needs a documented
reason and review date, not a blanket purge to reach the number.

Adoption would need Owner agreement on these windows/budgets and a separately
scoped implementation if automation is wanted. This assignment changes no
runtime retention settings, feature-cache expiry, schedules or product code.
