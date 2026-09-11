# Empirical template quality and model promotion

Status: active model-quality policy as of 2026-08-31.

## Independent claims

The learner mines recurring structures in the finite, software-generated CK3
message domain. It is not an open-ended natural-language generalizer. Four
claims remain separate:

1. emission accounting proves that no recognized `error.log` emission silently
   disappears;
2. structural parsing proves that template plus ordered slot values can
   reconstruct the source emission under the approved normalization contract;
3. grouping evidence shows that a template captures recurring structure
   without incorrect merges, incorrect splits, or degenerate one-message
   templates;
4. semantic review establishes what a structurally valid template means and
   which typed contract, if any, may be approved for runtime use.

Representative real CK3 logs are the principal evidence. A held-out corpus may
be used for a specific discovery, coverage, reconstruction, or merge/split
claim, but is not intrinsically required. The historical 98.5-percent pooled
target remains recorded as a prior owner target; this policy does not activate
it as a blocking threshold without measurement under the revised method.

## Candidate-independent measurement unit

The denominator is recovered diagnostics under a frozen parser,
extractor/splitter registry, and adjudication protocol:

- normally one diagnostic per recognized log emission;
- several diagnostics only when a pre-approved source-specific multi-error
  splitter applies;
- an emission routed unresolved contributes the number of independently
  adjudicated diagnostics defined by the frozen protocol, not a number chosen
  by the candidate model;
- parser failures and invalid/unscored cases are reported separately and cannot
  be excluded after inspecting candidate results.

The splitter/extractor identity and hashes are part of every evaluation. A
candidate model cannot redefine emission boundaries, splitting, or denominator
units to improve its score.

## Measured dispositions

- approved full contract;
- approved partial/L1 contract explicitly permitted as reportable;
- provisional or low-confidence candidate routed to review;
- unresolved/unknown routed to review;
- explicit parser failure;
- protocol-invalid/unscored with adjudicated reason.

Only approved full and approved permitted partial/L1 diagnostics enter the
coverage numerator. Review routing is a legitimate safe result but not covered.

## Practical evidence and metrics

| Metric | Definition |
|---|---|
| Pooled occurrence-weighted approved coverage | Approved full plus approved permitted partial/L1 diagnostics divided by the frozen candidate-independent diagnostic denominator. |
| Per-run approved coverage | The same ratio for every included run, with small-run treatment declared in advance. |
| Distinct normalized-pattern coverage | Unique source-qualified patterns with approved assignment divided by all such patterns; diagnostic, not currently a blocker. |
| Disposition distribution | Pooled/per-run counts and percentages for every measured disposition. |
| Reconstruction fidelity | Exact matches and explicitly enumerated differences after reconstructing each accepted occurrence from template plus ordered slots. |
| Structural compactness | Template count versus occurrence count, occurrences per template, singleton rate, slot-count distribution, and suspected near-duplicate templates. |
| Split/merge review | Human-reviewed examples of templates that may be too narrow, too broad, incorrectly split, or incorrectly merged. |
| Vocabulary discovery rate | Known templates, genuinely new candidate templates, and unresolved material observed as additional diverse real runs are added. |
| Model stability | Templates added, removed, merged, split, and occurrences reassigned when the same approved configuration is rerun or a revision is compared. |
| False-confident assignment rate | Adjudicated incorrect approved assignments divided by approved assignments in the frozen adjudication design. |
| Approved-assignment precision | One minus false-confident rate under the same design. |
| Breadth strata | Coverage and safety by source family, run, frequency band, approved level, changed/new contract status, and other predeclared strata. |
| Review debt | Routed frequency and pattern distribution with bounded examples/references. |
| Splitter behavior | Ordinary/multi-error counts, exact recovered-child cardinality, and splitter failures by version. |
| Invalid/unscored cases | Counts, reasons, owner/adjudicator treatment, and sensitivity effect. |

A frequency-capped diagnostic may reveal domination by one spam pattern, but it
does not replace the owner-selected pooled metric.

## Measurement before thresholds

Do not invent a blocking threshold. First report coverage/accounting,
reconstruction, compactness, split/merge findings, discovery rate, stability,
and representative examples from real CK3 material. If those observations show
that a numeric guard would answer a real product question, return the proposed
denominator, corpus, sampling method, failure meaning, and threshold rationale
to the owner. A sophisticated adjudication framework is not a prerequisite for
useful direct review.

## Corpus provenance

Store source content hashes and the purpose for which each real CK3 log was
used. If a claim-specific held-out comparison is commissioned, content-identical
copies must not cross its discovery/evaluation boundary. A universal permanent
role registry and untouched-future corpus are not product requirements.

Representative logs should cover observed diversity in CK3 versions, playsets,
source families, common spam, rare patterns, continuation emissions, approved
multi-error forms, and normal/crash runs where those facts affect the content.
Do not manufacture malformed logs or arbitrary environmental states merely to
enlarge an evaluator.

## False-confident adjudication

An assignment is false-confident when runtime presents an approved full or
partial result but independent authority finds the contract/template, approved
level, typed slots, source-family boundary, or required semantic role wrong.
Explicit review routing is not false-confident; it reduces coverage.

Report at least:

- wrong contract/template;
- overclaimed full versus justified partial;
- wrong typed slot/locator/key role;
- wrong source family;
- deterministic projection/reference defect after correct matching;
- evaluator/oracle defect or invalid case.

## Promotion workflow

1. Learner produces a candidate and complete provenance manifest.
2. Artifact validation proves schemas, hashes, references, and deterministic
   loading.
3. Known-regression tests and human calibration pass.
4. Reviewers approve every new/changed contract and typed rule.
5. Reviewers inspect reconstruction, compactness, split/merge, discovery, and
   stability evidence over representative real CK3 logs.
6. If a claim-specific held-out comparison was commissioned, review its
   predeclared results without changing the claim after inspection.
7. Promotion authority records approved/rejected, hashes, corpus provenance,
   metrics, limitations, compatibility, and rollback.
8. Only an approved immutable revision enters runtime selection.

Learner output never becomes authority automatically. Similarity never
bypasses typed validation.

## Product relationship

A model may be promoted without a product release. A release may retain a
previous approved model. Trusted Run acceptance and an alpha that bundles a
model require an approved promotion record, but model-quality failure does not
invalidate unrelated capture/database/report implementation.

Every diagnostic record and report identifies represented model/contract
revisions. Reclassification is an explicit versioned operation; failure keeps
the prior accepted state. Source expiry may make some reclassification
unavailable and must say so.

## Evaluation independence

Exact product behavior follows ratified requirements and minimal proof, not a
giant blind evaluator. If a held-out empirical comparison is later
commissioned, its claim and evidence boundary must be explicit. This planning
task creates no evaluator, holdout, scorer, or qualification attempt.

## Promotion record

Record candidate/prior hashes, tool/source versions, evidence-role manifests,
parser/splitter identity, deterministic results, contract reviews, complete
metrics, invalid/unscored accounting, adjudication/isolation statement,
compatibility/rollback, and final approval. Aggregate coverage alone is never
a promotion record.
