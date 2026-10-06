# Agent working practices review

2026-10-03. **Proposal for owner decision; no new instructions, assignments or
Skills are activated by this document.**

The owner subsequently clarified the team responsibilities recorded in
[team governance](team-governance/README.md) on 2026-10-05, including Pipeline's
application packaging ownership. Use that record for those responsibilities;
the remainder of this review retains its proposal status unless separately adopted.

## 1. Assessment and main recommendation

Keep owner-directed specialist conversations, with clearer delivery ownership
and shorter reusable task structures. Do not add permanent teams, an autonomous
coordinator, or one Skill per team. Treat research as a workflow available to
each specialist; commission a separate research conversation when uncertainty
crosses boundaries or merits an independent investigation.

The existing component boundaries are useful. Current deliveries show shared
database access, capture facts, immutable executable packages and reporting
libraries being received through explicit interfaces. The main coordination
weaknesses are tracking later obligations, distinguishing implementation from
activation and acceptance, and keeping corrections current across several
documents. More role instructions alone would not solve those problems.

Recommend this minimal arrangement:

1. Name one delivery lead and one receiving/integration owner in each substantial
   assignment. These are responsibilities within existing conversations, not
   new teams. An implementation task can own both.
2. Carry original work **and subsequently assigned follow-ups** to closure.
   A completed original delivery must not erase an unfinished repair. Keep each
   open item with an accountable owner, next action and evidence limit.
3. Use a short task-opening structure and a short handoff structure, hosted in
   one proposed `docs/AGENT_WORKING_PRACTICES.md`. Keep requirements and API
   detail in their existing owning documents.
4. Keep `AGENTS.md` as the durable entry point; use the existing plan, status
   and current handoff for their distinct purposes. Replace repeated checkpoint
   narratives with links as those documents next need authorized updates.
5. Pilot this without a new Skill. Review meaningful consumer behavior using
   permitted genuine evidence; repeat checks when changes or unresolved
   questions justify them. The advisor is optional support, not a mandatory
   approval stage.

This addresses observed problems without reopening established architecture or
weakening owner restrictions. Supporting project evidence is in section 7;
external sources and their limits are in section 8.

## 2. Proposed responsibilities and authority

All entries below are recommendations, not new assignments. “Owner” in the
decision column means the product owner; a component maintainer's authority is
limited to the assigned technical scope. A chat title does not confer authority.

| Responsibility | Accountable outputs | Decision authority | Interface and receiving ownership |
|---|---|---|---|
| Product owner | Product outcomes, scope decisions, priorities, task authorization and final acceptance | Chooses materially different product behavior, scope transfers and operational authorization; accepts tasks with disclosed limits. Milestone acceptance still requires its ratified checks. | Resolves product/priority conflicts and names a receiving owner when an assignment spans components. Need not approve routine implementation choices. |
| Advisor, when commissioned | Options with evidence, assignment drafts, dependency assessment and receiving findings | May recommend and clarify recorded decisions; cannot turn a proposal into authorization, assign new scope independently, or certify missing evidence | Helps connect producer and consumer work. Owns accuracy of its summaries and prompt drafts. Does not become the sole route between specialists. |
| Learner | Empirical investigations, parser/matcher authoring, candidate artifacts, retained executable releases and comparative evaluation | Chooses implementation within assigned model work; promotion/selection follows existing owner requirements | Owns published package/API meaning and authentic executable delivery. Pipeline owns receiving it in the runtime classifier/contract path. Comparative evaluation remains outside database storage. |
| Pipeline | Approved Error Contract implementation, ingest, persistence, retention APIs and shared handler | Owns assigned contract/storage/handler implementation; cannot redefine capture facts or reporting semantics | Owns `HandlerClient`, public operation/outcome contracts and Run persistence. Receives learner packages and watcher metadata; watcher/reporting owners verify their callers. |
| Watcher | Lifecycle observation, protected publication, capture facts, playset production and automatic triggers | Owns assigned capture/caller implementation; activation is a separately visible authorized action | Owns capture metadata meaning and publication boundary; Pipeline owns preservation. Watcher owns actual trigger/result integration and operational delivery when assigned. |
| Reporting and Analysis | Diagnostic/history services, source search/context, reports and CLI | Owns assigned query/presentation behavior and bounded receiving repairs already authorized, such as 08B's source-scope repair | Receives public handler data and researched selectors; owns the complete query → source → CLI/report path. Repairs belong in the owning library, with its API/handoff updated. |
| Research assignee, in any area | Answer to a bounded question, reproducible evidence, alternatives, uncertainty and a consumer-ready conclusion | Can investigate within authorization; cannot activate its recommendations | Names the intended consumer and deliverable. The consumer receives findings and implements only what its assignment authorizes. A separate research chat is useful for cross-cutting or independent inquiry. |
| Delivery/integration lead, named per task | Complete assigned outcome, tracked follow-ups, affected-consumer verification and consolidated handoff | Coordinates technical dependencies within the assignment; escalates material scope changes | Remains accountable for unresolved delivery work until a transfer is explicitly accepted. For a future full Trusted Run exercise, name one lead for the complete path; do not assume “all teams” owns it. |
| Maintainer of a shared component | Coherent shared API and focused documentation/checks | Technical authority within that component's approved contract | For example, logging configuration remains in `runtime_logging.py`; consumers use its helpers. Name a maintainer in a task that changes it, without creating a Logging team. |

Each implementer owns relevant verification and documentation of its changes.
The receiver owns demonstrating use at the boundary it consumes. The delivery
lead reconciles the combined result; the product owner makes final acceptance
decisions. A reviewer can be a downstream specialist or a separately commissioned
advisor. Routine local fixes need no additional review conversation.

### Proceed, consult or ask

- **Proceed independently:** implementation choices inside the assigned outcome;
  requirement-derived checks allowed by current guidance; documentation of changed
  behavior; bounded repairs explicitly included in the assignment. Complete the
  authorized work without repeatedly asking whether to continue.
- **Consult the component owner:** clarify an existing API, shared-file edit,
  consumer dependency or technical repair spanning ownership. Continue independent
  work while the affected part is resolved. Consultation can be a precise handoff
  for the owner to relay; no autonomous messaging platform is required.
- **Ask the product owner:** materially different behavior, new requirements,
  new acceptance thresholds, priority/scope transfer, unresolved requirement
  conflict, or an operation outside existing authorization. Present the concrete
  choice and effect. Advisor suggestions and old tests are not authorization.

For an upstream defect, the discovering team records the requirement, observed
failure, affected consumer and proposed fix owner in the existing task record.
The component owner is the default technical repair owner. The discovering
delivery lead retains responsibility for getting the dependency resolved until
that owner accepts it; “upstream issue” is not a disposition. An already
authorized bounded receiving repair can be made by the consumer in the owning
component, with coordination if someone else is editing it. A material transfer
goes to the owner. No wrapper, substitute implementation or change of requirement
is introduced simply to avoid the dependency.

## 3. Instruction mechanisms and authoritative homes

| Mechanism | Fit for this project | Cost or limitation | Recommendation |
|---|---|---|---|
| Current approach with limited improvements | Existing detailed prompts and handoffs already capture APIs, evidence limits and restrictions | Owner still repeats opening/closure expectations; evolving status is duplicated | Viable fallback: add only explicit receiving ownership and open follow-up rows to future assignments. |
| Reusable opening and handoff structures | Makes outcome, repair ownership, authorization and partial completion visible at low cost | Overlong forms become another compliance exercise | **Adopt a small pilot.** Embed both structures in one linked document; omit irrelevant fields for small tasks. |
| Root `AGENTS.md` | Durable project rules and conditional navigation for every task | Frequently changing status and copied procedures increase orientation cost and staleness | Retain an entry point and essential constraints; move task progress to its existing home during a later authorized cleanup. |
| Nested `AGENTS.md` | Stable local rules tied to a real subtree, as in learner authoring | Path scope does not match teams that touch CLI, tests and shared libraries; extra files can conflict | Keep the existing learner guidance. Add a nested file only when distinct enduring local rules recur; do not create one per team. |
| Workflow-specific Skill | Can make a repeated multistep workflow discoverable and load resources when relevant | Trigger ambiguity, additional maintenance and duplicated policy; availability is not guaranteed execution | None initially. A receiving-review workflow is a conditional future candidate, specified below. |
| Role-specific Skill | Could orient a specialist with genuinely distinct repeated procedures | “Be the Pipeline team” mixes authority, status and many unrelated workflows; overlaps root instructions and task prompts | Do not adopt. Role boundaries belong in the working agreement and task assignment. |

Proposed authoritative homes, with no mass documentation rewrite:

| Information | Home and maintenance owner |
|---|---|
| Enduring product intent and rejected designs | Existing `OWNER_PRODUCT_INTENT.md`, focused approved specifications and `BANNED_IDEAS.md`; owner decisions govern. A commissioned author records corrections in the relevant home. |
| Repository execution rules | Root `AGENTS.md`; local subtree rules in applicable nested files; environment commands in `DEVELOPMENT_ENVIRONMENT.md`. Link to details instead of copying them into every prompt. |
| Responsibility boundaries and reusable working procedures | Proposed `docs/AGENT_WORKING_PRACTICES.md`, including the two template sections. Owner approves policy; an explicitly designated advisor/maintainer edits it. |
| Task-specific requirements and authorization | Existing task prompt, with a small current-scope header recording accepted amendments and their source/date. The delivery lead maintains the header. A draft remains marked proposed until assigned. |
| Stable interface detail | Existing focused API/specification or current executable handoff, such as `SHARED_MATCHER_API.md`, the accepted 07D handoff and `RELEASES.md`; component maintainer. Do not create a second API catalog here. |
| Milestones and sequencing | `PROJECT_PLAN.md`; owner-directed plan maintainer. It links to deliveries rather than repeating test narratives. |
| Current implementation, activation and evidence limits | `PROJECT_STATUS.md`; task authors supply updates through its designated writer. Keep one current summary and pointers to operational/verification records. |
| Shared-checkout continuation and open assigned obligations | `CURRENT_HANDOFF.md`; current delivery leads, with one writer at a time. Record changed-file ownership, outstanding work and exact next action. |
| Completed task evidence and detailed history | The task's existing handoff/review. Raw evidence remains ignored/outside Git. Closed details need not remain in the mandatory opening read. |

These are different responsibilities for existing documents, not four copies
of a new ledger. For an active task, its current-scope header defines the
obligations; `CURRENT_HANDOFF.md` records their live state and links back.
`PROJECT_STATUS.md` summarizes readiness; `PROJECT_PLAN.md` states sequencing.

### Conditional Skill candidate; not proposed for installation now

If the pilot repeatedly misses receiving obligations despite using the linked
template, consider **`ck3-receiving-review`**, rather than an Advisor Skill.

| Aspect | Conditional design |
|---|---|
| Concrete workflow | Reconcile an assigned delivery and its amendments with the delivered interface, consumer use, evidence and remaining obligations; produce a receiving disposition. |
| Activate | An explicit request to receive/review a CK3Chronicle component delivery or prepare its downstream assignment. Start with explicit invocation; consider implicit matching only if useful and reliable. |
| Do not activate | Ordinary coding, a small bug fix, general research, task execution, model promotion or live activation. It never commissions implementation or launches production commands. |
| Required inputs | Assigned task/amendments, producer handoff, intended consumer, relevant current authority links, permitted inspection/check scope and evidence location. Missing information is labeled, not reconstructed from imagined chat history. |
| Outputs | Met/open/out-of-scope obligations; API/consumer fit; inherited versus newly executed evidence; named repairs/dependencies; accept/return/partial recommendation for the owner. Use the existing handoff/review destination. |
| Supporting resources | Links to the approved working agreement and owning APIs; the shared handoff template remains canonical. No embedded current task status, copied banned list or automatic broad test runner. |
| Location | If separately approved, `.agents/skills/ck3-receiving-review/SKILL.md`, with optional `agents/openai.yaml` for explicit-only invocation. Verify discovery in the actual host before rollout. |
| Maintenance owner | Owner-designated working-practices maintainer; component owners maintain linked interfaces. Changes evaluated on actual subsequent reviews, not synthetic product histories. |
| Why a prompt/document might be insufficient | Only if repeated real reviews show that users omit the procedure or agents fail to select the right linked resources. A Skill could add discoverability and selective loading. The inspected evidence does **not yet establish** that insufficiency, so a linked template currently wins. |

Official documentation describes Skills as selectively loaded instructions and
resources, with explicit or description-based invocation and repository discovery.
That capability supplies neither team authority nor a guarantee of correct
execution. The proposed location follows the current documentation; this review
did not test local Skill discovery. [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)

## 4. Minimal task lifecycle and concrete examples

1. **Assignment:** identify the outcome, delivery lead, receiver, authorized
   scope and relevant current contracts. Record what establishes completion and
   what evidence/operations are available. Preparation of a prompt is not launch.
2. **Execution:** work autonomously within that scope. Inspect the owning code,
   reuse its interfaces, verify affected behavior and update relevant docs.
   Small tasks need only a short opening statement, not a separate prompt file.
3. **Scope change:** keep owner follow-ups in the same active obligation list.
   Record what changed, why, who authorized it and what it supersedes. A
   technical finding can suggest a requirement; it cannot silently create one.
4. **Handoff:** state the actual delivered behavior and interface, checks,
   limits and every unfinished assigned item. Update the existing handoff; do
   not create another document solely because a review iteration occurred.
5. **Receiving review:** inspect the intended consumer path and relevant evidence.
   Resolve bounded receiving repairs, or assign an accepted transfer with its
   next action. Review changes at the seam rather than automatically rerunning
   every upstream campaign.
6. **Closure:** the owner accepts or explicitly defers the disclosed outcome.
   “Original implementation delivered; follow-up open” remains partial. Closing
   the original task can reference a separately accepted successor assignment,
   but the obligation persists. Operational activation and milestone acceptance
   have their own visible status when applicable.

### Proposed task-opening example

This is a structural example using the existing 08B boundary, **not a replacement
prompt or authorization to launch it**. Its detailed requirements stay in
`TASK08B_PROMPT.md`.

```text
Task: 08B reporting delivery
Authority: owner-assigned TASK08B_PROMPT.md and its current amendments.
Delivery/integration lead: Reporting and Analysis conversation assigned 08B.
Receiving owner: that Reporting lead for library-to-CLI/report integration.
Receiving result: root CLI and generated reports using the delivered 08A libraries.
Final acceptance: product owner. Separate advisor review only if commissioned.

Outcome: usable runs/report commands and required report formats/presets.
Included follow-up: finish the assigned scope-before-traversal repair in
SourceSearch and update 08A.2's handoff before accepting source integration.
Inputs: current root/subtree guidance; current status/continuation; 08A handoffs;
accepted handler/logging APIs; syntax selector handoff, at the relevant sections.
Interfaces: HandlerClient -> DiagnosticAnalysis + SourceSearch -> CLI/report.

Verification: genuine stored records through the public handler, genuine source
files, disposable storage, actual CLI output and rendered report inspection.
Unavailable real cases stay unverified; no invented history or acceptance threshold.
Operational boundary: follow the existing prompt's exclusions and permissions.

Completion: original report work AND assigned receiving repair accounted for;
actual checks and limits disclosed; final commands/docs/handoff delivered.
Shared files: coordinate CLI and current-status edits with other active writers.
```

### Proposed partial handoff example

The following reformats the observed 08A/08B checkpoint; it reports no new
implementation or check. A real handoff would link each obligation to its
assigned requirement and give the named conversation/assignee.

```text
Disposition: 08A libraries delivered; source traversal correction open;
08B reports/CLI not implemented. This handoff does not accept Trusted Run.

Delivered: diagnostic analysis and source search integrated through SourceResolver.
Consumer entry: DiagnosticAnalysis(HandlerClient(...),
                                  source_resolver=SourceSearch(client, ...)).

Obligation                     State          Accountable continuation
08A library integration        Delivered      Reporting; receive actual APIs
Scope-before-traversal repair  Open           Assigned to 08B in current prompt
08B CLI/report surface         Not delivered  Reporting/08B assignment
Chronological multi-Run proof  Unverified     Receiving lead tracks eligible evidence

Evidence: prior receiving review reports 15 genuine-data checks passing;
not rerun by this working-practices review. Later history exercise reports
14 genuine Runs with no eligible source timestamps; component passes do not
prove successful chronological investigation windows.

Next: execute the assigned repair and reports; use eligible genuine data when
available. Do not backfill or invent history. Timestamp activation has its own
watcher record; successful future capture and full lifecycle remain distinct.
Changed files / shared work: list only this delivery's edits and overlap concerns.
Acceptance: record the owner's actual disposition; this example establishes none.
```

For a research task, replace “delivered API” with question, method, supported
finding, counterevidence/limits and receiving use. For a small fix, the final
message plus an update to an existing handoff can supply all necessary fields.

## 5. Context, verification and review discipline

### Efficient orientation and correction

A fresh substantial task should follow the current entry instructions, then
read only the opening current status/plan/continuation and the owning contract
and handoff for its boundary. The proposed cleanup would retain these routes
while removing duplicated histories from the opening path. Historical detail
remains available by link. It is not mandatory reading merely because it exists.

An owner correction should be recorded once in its authoritative home with
date, scope and explicit supersession. Add a short link/warning at conflicting
active entry points, rather than reproducing the entire correction everywhere.
Record whether an amendment changes requirements, work authorization, or only
the evidence assessment. If the current owner direction is clear, apply it;
if conflicting authorities remain material, ask about that conflict while
continuing unaffected work. Source code and old test expectations describe
implementation/history, not missing requirements.

On resuming a long chat, refresh the current-scope header and unresolved rows
before acting on an old plan. Instruction files and Skills are not assumed to
refresh every active conversation automatically. The Codex instruction guide
documents an instruction chain built at run start and path-based precedence;
it is not a shared project-status service. When entering another subtree,
inspect applicable nested guidance rather than assuming a root-launched chat
has already read every nested file.
[OpenAI: AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

### Shared checkout

The inspected checkout contains extensive existing modifications and untracked
deliveries. Preserve them. At task start, inspect status and the current handoff;
identify the files this task will touch. Coordinate overlapping edits to shared
CLI, configuration, status and API files. Use one writer per overlapping file
at a time; read-only review can proceed alongside implementation. If a file
changes during an edit, reconcile its latest content instead of replacing it
with an older snapshot. Do not stash, reset or clean others' work for convenience.

Use an isolated worktree when independent concurrent implementation actually
needs it, with an explicit integration owner and base. A new checkout cannot be
assumed to contain this checkout's uncommitted delivery or ignored evidence;
prepare that dependency deliberately. File isolation also does not isolate
configured production services or data. For the present review, no worktree is
needed. Codex documents worktrees for independent chats and separate file copies;
the project-specific preparation above is a recommendation.
[OpenAI: Worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees)

### Proportionate evidence

| Work | Appropriate evidence and boundary |
|---|---|
| Learner/research | Native examples, method, selected executable/model identity where relevant, and limits on conclusions. Compare substantive behavior against owner requirements and source evidence, not old output as an oracle. |
| Pipeline/Watcher | Requirement-derived owning-component and consumer checks using permitted genuine input. Verify the publication/metadata/handler seam affected by the change. Keep implementation checks and separately authorized live activation distinct. |
| Reporting | Genuine stored CK3 records through `HandlerClient`, real source files, and actual public consumer behavior. Do not create synthetic histories, diagnostic/count cases, mocks or injected failures as acceptance evidence. |
| Receiving/Advisor | Inspect the current contract and delivered code; distinguish reported checks from checks personally executed. Run a focused consumer check only when it answers an unresolved receiving question or verifies a changed seam. |
| Documentation-only work | Verify factual support, authority labels, links, proposal status and preservation of unrelated files. Runtime suites add no acceptance evidence for an unchanged runtime. |

08B already requires a representative report through the real root CLI and
inspection of generated output; preserve that requirement. It checks a longer
path than individual library tests: public handler reads, library composition,
filter/identity/count behavior, candidate context and rendered presentation.
Eligible historical evidence is needed to demonstrate actual chronological
comparison. Passing component checks on ineligible Runs does not substitute
for it. Future Trusted Run acceptance needs the owner-defined whole lifecycle,
capture, ingestion, review and stored reporting outcome together.

Keep a small evidence entry with requirement, method, result, evidence location
and limitation; identify inherited versus freshly executed results. Report failed
checks and proposed requirements beyond scope. Once the relevant checks pass,
repeat only for a relevant change, failure, evidence problem or explicit further
assignment. Missing real cases stay unverified until evidence becomes available;
do not make accumulating five eligible Runs a new delivery gate. Do not run a
verification campaign repeatedly against unchanged ineligible data.

No new hash ceremony, benchmark threshold, full-suite mandate or fault-injection
regime is proposed. Existing marker checks retain only their approved purposes.
The required runtime logging ownership check remains applicable to runtime
changes; removed synthetic logging tests stay removed.

### Changes the advisor should make

The 08B receiving review usefully caught an actual traversal defect, reconciled
API details and preserved evidence limits. Its 15-check rerun is reported
evidence, not proof that every later advisor should repeat those suites. The
available record cannot establish that the earlier rerun was unnecessary.

The advisor should keep optional improvements separate from assigned repairs,
avoid extensive prompt rewriting when a narrow amendment suffices, and avoid
copying each checkpoint into plan, status and continuation. Preparing a prompt
must remain distinguishable from launching it. “Ready with a repair” needs the
repair owner and completion condition beside it. The advisor should review the
assigned outcome rather than add unrequested thresholds or architecture, and
should not become the only person able to interpret project history. These
changes reduce dependency on the advisory conversation itself.

## 6. Owner decisions and adoption pilot

These decisions concern a later implementation assignment. Nothing in this
review changes the active 08B prompt or existing team assignments.

| Question | Recommendation | Alternative | Practical consequence |
|---|---|---|---|
| How much process change? | Pilot one short working agreement with embedded opening/handoff structures | Only add receiving owner and open-follow-up lines to future prompts | The smaller alternative minimizes maintenance but leaves more orientation to each author. |
| Is Research a permanent separate role? | Use research across specialists; separate conversations for cross-cutting questions or independence | Route all investigations through a Research team | A standing team may improve concentration but adds a handoff and can detach findings from their consumer. |
| Who owns integration and receiving repairs? | Name a lead per assignment; consumer handles authorized bounded repairs; component owner handles accepted upstream transfers | Return every upstream issue to its originating team | The recommendation avoids unnecessary round trips while retaining technical ownership and explicit scope control. |
| Is advisor approval compulsory? | No; commission it for ambiguous scope, substantial interfaces or independent review | Require advisory receiving review for every delivery | Mandatory review adds a queue and dependence on advisor availability. Neither approach replaces owner acceptance. |
| Where does changing state live? | Use status for readiness, current handoff for live obligations, plan for sequencing; link detailed evidence | Continue full checkpoint summaries in all three | The recommendation needs a small authorized cleanup but reduces conflicting copies. |
| Adopt Skills now? | No; reconsider the single workflow candidate only if the pilot shows a discoverability/procedure problem | Create an explicit-only receiving-review Skill immediately | Immediate adoption adds a resource/trigger to maintain before its benefit is demonstrated; role Skills add still more duplication. |
| How should concurrent work be isolated? | Coordinate overlapping shared files; use worktrees for genuinely independent edits with a prepared base | Require a worktree for every task, or keep all edits in one checkout | Universal worktrees add dependency/evidence setup; unrestricted shared edits risk overwriting work. |
| How should evidence gaps affect closure? | Accept only what evidence supports; explicitly carry unverified obligations and separate milestone acceptance | Hold every delivery until all potential cases are observed | The recommendation permits useful delivery without false completeness. Existing ratified milestone checks still govern acceptance. |

Proposed artifacts and changes, only if authorized:

- **`docs/AGENT_WORKING_PRACTICES.md`**: concise responsibility/authority rules,
  lifecycle and the two reusable structures; no current task inventory or API copy.
- **Existing `AGENTS.md` and current-document openings**: route to that agreement
  and separate status/plan/continuation responsibilities. Preserve governing
  restrictions; do not retroactively rewrite historical evidence.
- **Future task prompts and existing task handoffs**: use the structures in place,
  rather than creating parallel task-opening, closure and review files.
- **Optional later Skill location**: specified in section 3, conditional on a
  separate decision. No Skill files are created in this review.

Pilot on the next two or three owner-selected assignments: ideally one consumer
integration, one research-to-implementation handoff and a small ordinary fix.
Do not relaunch or change 08B solely for the pilot. Use future assignments or an
explicitly approved amendment when the owner chooses.

At assignment, identify the lead/receiver and reuse existing requirement links.
At closure, add a few observations to the task handoff, not a separate tracking
system. The owner-designated maintainer then compares the pilot with the
documented coordination cases below and the owner's recollection, labeling
recollection as such. No reliable historical rate can be calculated from this
small document sample.

| Pilot signal | What to observe | Decision use |
|---|---|---|
| Owner repetition | Instances where an already recorded rule had to be restated; exclude genuinely new decisions | Check whether navigation and supersession reduced avoidable corrections. |
| Scope mistakes | Work added without authorization, omitted assigned follow-ups or decisions repeatedly escalated despite clear scope | Check both overreach and unnecessary stopping. |
| Handoff omissions | Receiver had to rediscover an API, repair owner, activation state or evidence limit | Check whether the short structure captured what mattered. |
| Maintenance effort | Rough time/documents touched for orientation and closure; conflicting copies or unused fields | Remove fields or documents whose upkeep exceeds their value. |
| Integration outcome | Whether the intended consumer ran successfully on allowed evidence, with remaining gaps explicit | Check that paperwork reduction did not hide incomplete behavior. |

Keep the arrangement if it reduces avoidable interventions and receiving
rediscovery without materially increasing writing or waiting. Simplify it if
the forms cost more than they save. If omissions persist, first determine
whether the cause is missing authority, unavailable evidence or an unowned
dependency; a Skill addresses none of those. Consider the Skill only for a
repeatable workflow-selection problem. This is an evaluation proposal, not a
new product acceptance threshold or a scheduled recurring review.

## 7. Supporting project evidence

### Method and limits

Read the root and learner instructions, development environment, opening current
plan/status/handoff, owner intent and banned ideas. Followed README/owning guidance
to accepted watcher and learner references. Sampled the specified 07D/07E/08A/08B
deliveries, the current releases guide, 07C's release handoff, source timestamp
handoff and syntax research handoff. Inspected focused owning code to check
actual dependency direction and the documented traversal problem.

No rejected database-handler design, copy or continuation was opened. No private
conversation history was inferred. No runtime test, database query, capture,
service operation, installation, commit or push was performed for this review.
All test counts and activation events below are **reported by their named
documents**, not independently rerun here. Direct source inspection is identified
separately; it is not runtime acceptance evidence. This is a bounded sample, not
a complete organizational audit.

Document verification performed here: all 31 local Markdown links resolved,
code fences were balanced and no trailing whitespace was found. The final Git
status comparison added only this review's untracked path to the existing list.

| Evidence | Observation and classification | Implication for this proposal |
|---|---|---|
| E1 — [Owner intent](OWNER_PRODUCT_INTENT.md), [banned ideas](BANNED_IDEAS.md), [root instructions](../AGENTS.md) | **Owner requirements:** implemented differs from accepted; agent conclusions and historical tests do not define scope; real reporting evidence is required. Root guidance excludes rejected designs and removed tests. | Separate authority, implementation and evidence. Preserve these rules; no extra verification regime. |
| E2 — [07D accepted handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md), source-timestamp receiving section | **Reported successful integration:** two focused receiving checks preserved exact timestamp/facts through public Run operations and duplicate handling. It distinguishes inherited watcher checks from its own receiving checks and reports no persistence repair needed. | A narrow, explicit seam check can settle responsibility without rerunning a whole upstream campaign. |
| E3 — [07E handoff](TASK07E_RUNTIME_LOGGING_HANDOFF.md) | **Delivered architecture/reported checks:** shared logging owner and preserved handler contract; separate authorized activation. Its opening owner correction invalidates the removed synthetic logging suite as current guidance. September 30 attachment after game start did not prove full lifecycle acceptance. | Retain a shared component owner and separate activation/acceptance status. Current corrections must be easy to find before historical commands. |
| E4 — [08A.1 handoff](TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md), [08A.2 handoff](TASK08A_2_SOURCE_SEARCH_HANDOFF.md) | **Delivered interfaces/reported integration:** `DiagnosticAnalysis` receives `SourceSearch`; public handler supplies stored data. Six diagnostic and nine source checks are reported on genuine evidence; evidence limits are explicit. | Keep query/search/report work in one accountable domain with reusable libraries; no new team split is justified by this sample. |
| E5 — [08B receiving review](TASK08B_RECEIVING_REVIEW.md), [current 08B prompt](TASK08B_PROMPT.md) | **Documented coordination problem and assigned repair:** exact-reference lookup still enumerates broader roots before filtering. The receiving review records the gap and the prompt assigns repair to 08B in the owning library. This review independently confirmed the call order in source, but did not execute it. | Preserve follow-ups after original delivery. “Delivered” alone is not closure; bounded receiving repair ownership is practical. |
| E6 — [current status](PROJECT_STATUS.md), [08A.1 handoff](TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md), [07E correction](TASK07E_RUNTIME_LOGGING_HANDOFF.md) | **Documented owner corrections:** 14 synthetic/injected reporting checks were removed, followed by the seven-test synthetic logging suite; an unrequested query-depth cap was also removed. | The problem includes agent-generated obligations, not merely missing team names. Templates and review must ask which owner requirement justifies a check or constraint. |
| E7 — [multi-Run handoff](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md), [watcher timestamp handoff](WATCHER_SOURCE_MTIME_HANDOFF.md) | **Reported evidence limit and operational explanation:** 14 genuine stored Runs lacked the required timestamp. The watcher record says an older loaded watcher produced six subsequent captures, reports authorized October 2 activation, and leaves confirmation in a subsequent genuine production capture outstanding. | Implementation availability is not running-version evidence. Eligibility gaps cannot be repaired by optimistic summaries or invented history. Do not infer current live state from this record. |
| E8 — [releases guide](RELEASES.md), [07C handoff](TASK07C_SELF_CONTAINED_RELEASES_HANDOFF.md), [learner instructions](../tools/template_learning/AGENTS.md) | **Delivered boundary/reported checks:** retained executable releases, explicit package selection and per-Run lineage; Pipeline can continue with its existing selection. Missing historical executable closures remain explicitly unavailable. | Learner owns empirical/executable delivery; Pipeline owns runtime consumption. Do not turn inventory gaps into automatic historical reconstruction or new compatibility work. |
| E9 — [syntax research](CK3_SYNTAX_DIAGNOSTICS_RESEARCH.md#concrete-selector-handoff), [08B receiving review](TASK08B_RECEIVING_REVIEW.md) | **Research recommendations, then receiving fit:** nine package-scoped selector branches with exclusions; research itself activates no policy. The receiving review reports two matches present in its SQL sample, not verification of all families or the future report preset. | Research can be a bounded workflow with a precise downstream output. Consumer implementation and evidence coverage remain separate responsibilities. |
| E10 — [plan](PROJECT_PLAN.md), [status](PROJECT_STATUS.md), [current handoff](CURRENT_HANDOFF.md), [README](../README.md) | **Direct document observation:** repeated delivery/activation narratives and older “next” sections remain beneath newer checkpoints. Supersession notices help, but a fresh reader must still reconcile several copies. Git status also showed extensive existing uncommitted work. | Reduce duplicated current state; use targeted history links and coordinate shared edits. This demonstrates maintenance risk, not proof that every repeated summary caused an error. |

Focused source observations made during this review:

- [Reporting analysis](../src/ck3chronicle/reporting/analysis.py),
  `DiagnosticAnalysis._read`, calls `client.submit`/`result`; source resolution
  is composed into the investigation.
- [Source search](../src/ck3chronicle/reporting/source_search.py), `_files`
  and `resolve`, pass known references into a path that calls `_inventory`
  with default `['.']` before reference filtering. This supports E5.
- [Capture](../src/ck3chronicle/harvester.py), `spool_logs`, formats the source
  stat's nanoseconds; [ingestion](../src/ck3chronicle/pipeline/ingestion.py)
  passes `facts=metadata` into `write_run`. This is static boundary confirmation,
  not proof about any particular production Run.
- [Watcher processing](../src/ck3chronicle/watcher_processing.py) uses
  `HandlerClient`; [the client](../src/ck3chronicle/pipeline/request_handler.py)
  may start the dedicated host on submission. This review therefore did not use
  a nominally read-only client call as a process-free inspection technique.
- [Catalog](../src/ck3chronicle/pipeline/catalog.py) supplies selected packages
  to the classifier; ingestion obtains lineage from that loaded package.
  [Runtime logging](../src/ck3chronicle/runtime_logging.py) owns handler setup
  and exposes component/event helpers. No alternative owners were added.

## 8. External references and applicability

Official pages were opened on 2026-10-03. Earlier Codex documentation URLs
redirected to the current ChatGPT Learn pages cited here. Documented capabilities
are separated below from project recommendations; no tool installation or local
feature experiment was needed.

| Primary source | Documented guidance | Application and limit |
|---|---|---|
| [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills) | Skills contain metadata/instructions and optional resources; full instructions load when selected. Invocation can be explicit or implicit. Repository discovery uses `.agents/skills`; invocation policy can be configured. | Supports a narrow optional workflow mechanism. It does not establish that CK3Chronicle needs one or that this desktop session's discovery has been tested. |
| [OpenAI — Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Run-start instruction discovery layers global/project/path guidance, with closer-directory precedence and a combined size limit. | Supports short durable routing and local subtree rules. Project authority still comes from owner instructions, not whichever historical document is longest. |
| [OpenAI — Worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees) | Independent chats can use separate Git working copies, with shared repository metadata. | Useful isolation when needed; does not decide this project's integration ownership or evidence/configuration setup. |
| [OpenAI — Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Official guidance cautions about excessive instructions, broad Skill triggers and mandatory reading unrelated to a change; it advocates clearer completion boundaries. | Supports reducing unnecessary orientation and stopping points. This is model-oriented advice, not proof of improvement in this project; the pilot should decide. |
| [Google — The standard of code review](https://google.github.io/eng-practices/review/reviewer/standard.html) | Review should balance forward progress with code health, distinguish optional polish and use technical evidence in disagreements. | Supports proportionate receiving review and clearly optional suggestions. It does not override owner-defined acceptance or evidence restrictions. |
| [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Advises starting with the simplest sufficient approach and adding complexity when justified. The page notes that tooling has changed since its original 2024 publication. | Supports testing a small procedural change before orchestration. Its application-agent architectures are not an organization chart for these owner-directed conversations. |

The proposed arrangement is an inference from the project evidence and these
limited capability/practice references. It remains for the owner to select and
commission; this review implements none of it.
