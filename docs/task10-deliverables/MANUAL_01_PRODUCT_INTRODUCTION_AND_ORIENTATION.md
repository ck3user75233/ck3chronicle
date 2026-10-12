# Launch & Distribution — manual introduction and product orientation

Prepared for Owner issuance, 2026-10-12. **Part 1 of the manual revision.**
Checkout: `C:\Users\nateb\Documents\ck3chronicle`.
Owner: **Launch & Distribution, documentation role**. Continue **TREK-11** when
issued; this is an Owner-requested revision to the received manual, not another
producer assignment. Reopen that record for this revision, preserving its prior
delivery/receipt. Preparing this prompt does not dispatch work.

## Outcome and authority

Write the opening of a user manual that explains why ck3chronicle exists, who
it helps, how its parts work together and how to understand its stored results.
A CK3 modder should understand the product before meeting CLI syntax, package
IDs or internal processing terminology. Deliver actual edited manual pages,
not another editorial recommendation.

The Owner specifically rejects the current introduction's internal statements
such as "Final distribution acceptance is pending", "It describes implemented
commands", and distinctions between workflow receiving and reference behavior.
Put execution evidence, Task numbers, receiving status and team obligations in
the technical handoff. Write the manual for a person using the product.

This assignment authorizes documentation edits and read-only technical review.
It does not authorize product changes, service operation, installation of startup
tasks, new acceptance campaigns, model builds, publication or activation.
Keep the separately deferred ingestion/hash-lookup/retry design deferred.

## Read and coordinate

Read root instructions and current plan/status/handoff, then:

- `docs/OWNER_PRODUCT_INTENT.md` and `docs/ARCHITECTURE_AND_DATA_LINEAGE.md`;
- `docs/ERROR_CONTRACT_SPECIFICATION.md` and current component references;
- `docs/TASK10_HANDOFF.md`, `docs/task10/DOCUMENTATION_HANDOFF.md`, and the
  complete current manual under `docs/user/`;
- `docs/task10-deliverables/10D_PRODUCT_REFERENCE.md`, `WORKING_AGREEMENT.md`,
  and `MANUAL_02_STRUCTURE_AND_EDITORIAL_REVIEW.md` in the same directory.

Use the absolute protected helper and canonical store from the pilot handoff:

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot team-state launch-distribution
& $pilotNode $pilot task-show TREK-11
& $pilotNode $pilot task-show TREK-9
& $pilotNode $pilot task-show TREK-10
& $pilotNode $pilot task-show TREK-12
& $pilotNode $pilot task-show TREK-15
& $pilotNode $pilot task-show TREK-16
```

Run tracker operations serially; read later comments. At preparation the received
application is 0.0.3, the manual is 10D-r2, and ingestion redesign is deferred by
CMT-168/169. Refresh those facts; do not copy stale waits into the new manual.

Own `docs/user/PRODUCT_VERSION.md`, `INTRODUCTION.md` and `ORIENTATION.md` for this
part. Part 2 owns the final index and whole-manual edit. Deliver these pages and
their headings before Part 2 integrates them. One editor at a time owns a file.
The two parts can run sequentially in one L&D chat or use an explicit handoff
between chats; they share the existing documentation record. Part 2 starts with
a systematic negative-construction inventory, classification and lead-reviewed
recommendations before its broader quality review; include these new pages in
that pass when delivered.

## Required content, in reading order

### 1. Product Version

Give the application's actual version and applicable platform/distribution,
with a readable explanation of how to identify the installed version. Introduce
the distinction between application version, manual edition and classification
model version. Put exact technical identifiers in a compact reference table or
linked advanced section after their purpose is explained. Long hashes, internal
candidate history and pending acceptance must not dominate the opening.

### 2. Introduction: purpose and use cases

Start with the problem: CK3's volatile logs contain useful evidence from a gaming
or testing session; modders need to preserve it, understand recurring errors,
compare changes between sessions and connect messages with relevant mod sources.
Explain the local product and durable run history in ordinary language.

Develop the Owner's intended uses: reviewing errors after play/testing; deciding
which recurring problems deserve attention; checking what changed after a mod
edit or playset change; locating relevant files; and supplying structured evidence
to an AI assistant that helps investigate errors and propose patches. Keep human
interpretation and machine-readable use equally accessible.

Explain the reason for templates. Treat a template as an empirical reconstruction
of a recurring CK3 message shape, analogous to the game's emitting code filling
variable slots in fixed wording. ck3chronicle learns from observed logs; this
analogy is not a claim of access to CK3's source or perfect recovery of every
emitter. Explain literals and variable values with one small, understandable
example grounded in an existing genuine diagnostic. Label simplified notation as
illustrative; never present invented output as an observed CK3 result.

Show how references/locations, keys, names and variable-length phrases such as an
error's reason can be represented where the published template supports them.
Explain that two messages can share a template but have different values/context,
while different message structures represent different templates. Distinguish
the diagnostic's exact identity and occurrence count from its template family.

Explain the payoff: users can investigate individual errors directly, while
structured templates/values make grouping, comparisons and machine reading more
consistent. AI consumers receive explicit wording, values, references and context
instead of having to infer all of those from a large text log. Do not promise that
structure guarantees correct AI reasoning, causal attribution or safe patches.

Connect this foundation to future analytical help, including near-match
suggestions for missing keys/undefined tokens caused by spelling mistakes, typos
or AI-generated nonexistent identifiers. Label that as planned/exploratory when
not shipped, and link Part 2's planned-features section. Describe source/context
checking as current behavior, accurately bounded below.

### 3. Orientation: how the product works

Describe the normal journey before giving commands:

1. Setup records the user's CK3/mod/log locations and separate product storage.
2. The Watcher runs alongside CK3 and protects the session's logs after observed
   exit. Explain manual launch and user-configured Windows startup separately.
3. Deferred processing identifies messages, applies the selected classification
   package, and stores the result through the shared database handler.
4. Reports, source/context queries and external readers use the stored history.

Use a small labelled flow diagram plus connected prose. Explain each component's
purpose: Watcher/capture, parser, templates/model, matcher/selector, handler and
database, review evidence, report/query tools, source-context tools, and retained
Learner for advanced model development. Keep team names and source-module details
out of this explanation.

Explain a Run as three related groups of information: **Run metadata/context and
processing lineage; diagnostic records with values/counts; unresolved native
review evidence**. Explain the retained raw capture as the input, with its own
retention, rather than implying it is embedded in SQLite. Verify these groupings
against the delivered schemas and use consistent vocabulary throughout.

Explain package IDs only after explaining what a classification package does.
Describe the working model shipped with the application, why its exact identity
and manifest hash are recorded, what the parser/matcher/selector each contribute,
and how a later approved package can be installed/selected through existing
supported operations. Distinguish registration from active selection. Explain
that selection applies to future processing and stored Runs retain their original
lineage. Ordinary users can use the supplied package without training a model.

Explain transparent, pinned components as reproducibility and traceability:
identifiers name exact reviewed resources, and recorded lineage explains which
resources processed a Run. Give a plain-language bridge to advanced commands;
do not turn this section into a catalog administration transcript.

## Accuracy points to resolve in the writing

- A successful ingestion assigns a **Run ID**. A protected **Capture ID** precedes
  that; disabled/failed processing does not automatically create a stored Run.
  A duplicate full-log hash refers to the existing Run rather than creating one.
  Explain this briefly without burying the ordinary journey in failure cases.
- Describe actual capture: live `error.log`, same-session `debug.log` when
  available, reconstructed playset and observed lifecycle/crash metadata.
  Associated crash evidence can include `exception.txt`; do not imply arbitrary
  crash-folder contents or all crash log copies are collected.
- Honor the Owner's desired explanation of launch options. The shipped launcher
  starts observation; Windows startup automation is separately user-configured.
  Document that distinction positively and point to Installation. Include exact
  startup instructions only when checked for the delivered launch/configuration
  contract; do not claim setup already registers a service or scheduled task.
- The effective playset comes from captured debug-log evidence. Explain candidate
  file/mod resolution and the last applicable member in recorded load order.
  Current source files may have changed since the Run; unresolved or ambiguous
  attribution stays explicit. Finding a file is evidence, not proof of fault.
- One handler per database queues requests to one serial database worker.
  Parallel clients are not parallel database writers. External read-only queries
  can overlap that single writer. Correct any claim of multiple application
  writers as a factual error, separately from the negative-construction review;
  preserve useful reader/locking instructions.

## Deliver and hand off

Read the opening as a first-time modder: can the reader explain the purpose,
normal journey, Run contents, template/value distinction and package purpose
without opening CLI reference? Revise until that is true. Check the facts against
current source/handoffs without launching product services. Put source/evidence
mappings and any narrowly unresolved factual point in the internal documentation
handoff, not in the public introduction.

Deliver the three edited pages, heading inventory and concise technical/editorial
handoff on TREK-11 for Part 2. Do not freeze or describe an intermediate opening
as the final bundled manual. Part 2 reviews the full reading experience, creates
the final edition and delivers it to existing TREK-10/16. Preserve old frozen
manual snapshots and received archives; canonical user pages may be revised.
