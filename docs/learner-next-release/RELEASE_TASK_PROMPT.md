# Learner task — integrate, verify and publish the combined release

Updated 2026-10-05 after the focused review and 08C corrective receiving check.
Preparation of this prompt is not execution. Use the reviewed v60 baseline plus
the accepted decoder delivery to publish one new immutable learner release and
reference model/runtime package for Pipeline. Do not activate production services.

## Receive

Read root/applicable `AGENTS.md`, development instructions, current status/handoff
openings, this directory's [README](README.md) and [HANDOFF](HANDOFF.md),
[release mechanics](../RELEASES.md), the current 08C API/handoff, and the consultant's
returned assessment. Reconcile newer parallel work before editing shared files.
Resolve material decoder findings with the delivery owner; proceed independently
on unblocked release preparation. Recommendations alone do not change owner policy.

The two requested decoder corrections are delivered and ready for integration.
Use the opening corrective section of `docs/TASK08C_HANDOFF.md`, the code/evidence
identities in `.codex-tmp/task08c/decoder/pre-integration-corrective/delivery-hashes.json`,
and `.codex-tmp/task08c/decoder/parser-substitution-corrected/results.json`.
The older `parser-substitution-simplified` adapter and consultant ZIP are historical
review inputs; do not copy their physical-file decoder calls into the parser.

Baseline: production package `68f1ae5db205ab46afef9c4d`; verified v60 research
package `840957b2f8e16f1cf0f88ad2`. The latter does **not** contain integrated
decoder changes. Authenticate current inputs against the recorded manifests;
do not activate the earlier v58 prepared selection or trust a version nickname.

## Deliver

1. Integrate `ck3chronicle.decoder.decode_fragment(raw: bytes) -> str` into a new
   owning parser version at `Source.read_text` and the decoded header groups in
   `parse_bytes`, following the corrected HANDOFF. Use this same fragment-safe API
   for the remaining native UTF-8 continuation decoding site identified there.
   It returns plain processing text using UTF-8/surrogateescape, preserving BOM
   characters and undecodable bytes without physical-file header admission,
   detection or normalization. Do not use `decode`, `read`, `Decoder.decode`,
   DecodedText access or file-header checks for these internal spans. Keep parser
   framing, recovery, spans, tokenization and inverse byte encoding unchanged
   unless the owner explicitly directs otherwise; display/search views never
   replace native text. Physical source files retain the existing `decode`/`read`
   operations and header policy, including corrected `bom_bytes` metadata.
   Receive the staged source-search/excerpt changes by focused
   edits against current files, preserving parallel work. Broader 08C folder/scope/
   beta work is outside this release assignment.
2. Close distribution dependencies before freezing. Provide the single shared
   application decoder through an explicit supported loading arrangement for the
   isolated learner and installed application. Preserve authenticated imports and
   prohibit ambient-checkout fallback. Declare the accepted chardet dependency for
   automatic physical-source detection and record its exact verified version;
   known-UTF-8 log ingestion must not require detector availability. No separate
   decoder catalog or pin. Update
   parser-version guards and manifests honestly; never relabel changed bytes with
   an older parser digest or modify retained releases in place.
3. Freeze a fresh learner release and build the reference model from the existing
   73-log hash inventory with the recorded **20 + 20 + 20 + 13** schedule. Reuse
   genuine inputs, not another version's registry/templates as seeds. Publish the
   actual combined parser/learner/matcher/model package; do not assume its IDs or
   template count will equal the v60 research artifact.
4. Run the combined verification specified in HANDOFF against these exact artifacts:
   decoder/parser byte and recovery preservation (including session 55), the same
   retained 20 Runs and 73-log production comparison, original three failures,
   focused field/marked-reference checks, complete outcome accounting and native
   reconstruction. Adapt comparison tools to each package's real parser identity;
   establish input correspondence rather than simply deleting equality guards.
   Reuse valid receipts within this final combination; do not repeat unchanged
   campaigns without a new failure or changed input. No synthetic test is authorized.
5. Register the authenticated final learner and model distributions through the
   existing release owners, with publication evidence/order and external manifest
   pins. Update packaged-resource entries and build/verify the application artifact
   outside checkout assumptions, including the current contract renderer, source
   decoder and dependencies. Provide an exact proposed selection and retain the
   previous selection/artifacts. Publication/registration is distinct from changing
   the live production selection; no commit, push or external upload is implied.

“Reference model” means the ordinary empirically learned model/runtime package;
do not author a separate manual template set for Pipeline. Known activity and
nested-formatting gaps remain disclosed scope limits, not newly commissioned fixes.

The release criterion is dependable ingestion and preservation of genuine Paradox
logs. Missing genuine UTF-16/32, East Asian encoding or double-BOM positive examples,
and the retained low-confidence source-file outcome, remain disclosed source-reading
limitations, not release gates. Do not commission more encoding research, another
sample or universal source-decoding coverage. Preserve the reviewed source behavior;
actual regressions affecting assigned behavior still require a disposition.

## Receive and close visibly

Update this directory's README and HANDOFF rather than creating another release
ledger. Include final artifact locations/hashes, source/application identity,
parser/learner/model/package identities, dependency closure, genuine results and
limits, numbered comparison examples, reproduction commands and proposed/previous
selections. Supply the concrete Pipeline intake paths and installed-artifact receipt.

Keep the stored-report surrogate-display issue attributable to Data Intelligence
unless already repaired and received. State whether it affects this release and
needs a bounded repair or owner disposition; decoder integration alone does not
close it. Distinguish release delivered, Pipeline receiving pending and activation
pending. Fix defects in your delivered artifacts uncovered during receiving.

No production ingestion/reset, capture interruption, service restart or live pin
switch. No blanket completion claim for 08C. The existing explicit restart
restriction is resolved with the owner only when Pipeline has a concrete verified
cutover ready, unless the owner has already superseded it in that assignment.
