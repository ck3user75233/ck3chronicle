# v46 quoted discovery and duplicate consolidation — 2026-10-03

## Correction: the original 20-log selection omitted the rare targets

The owner correctly challenged the first experiment's relevance. That training
set contained zero occurrences of the original war/casus_belli, Jevna and
Wijayatunggadewi diagnostics, and zero house_head/dynasty_house witnesses. IS3QON
was evaluated only after learning. The earlier same-input parity result was a
regression check, not evidence of learning from those rare cases. Selecting the
old first 20 logs was inadequate for that question.

The v46 code did run: compiled/imported hashes in its authenticated receipt match
the retained clustering/regions bytes. Its saved eventmanager discovery trace
reaches the shared scope template without the accepted regrouping recorded by v45.
This execution proof does not remedy the original data-selection mistake.

The corrected experiment retains the first 18 logs and substitutes the complete
IS3QON and house_head witness logs for the final two. Presence assertions verify
all four rare cases, all five observed scope formulations and 11 travel-receiver
occurrences before either build. Both frozen v45 and frozen v46 learned fresh on
this same corrected set, with no further implementation changes.

| Target | v45 corrected set | v46 corrected set | Distinct supporting diagnostics |
|---|---|---|---:|
| war / casus_belli | provisional | provisional | 1 |
| Jevna | provisional | provisional | 1 |
| Wijayatunggadewi | provisional | provisional | 1 |
| house_head / dynasty_house | full | full | 6 |

The travel dates, short identities and receiver text remain literal in their
separate singleton templates. War's link/scope text also remains literal; its two
declared located-parenthetical fields differ from the shared scope template's
three-field applicability signature. Thus the three original errors now receive
complete provisional assignments, but reusable generalization remains unsolved.
Both versions have the same target results: this coverage change is attributable
to the corrected evidence, not demonstrated classification improvement from v46.

Both builds retain identical selected template IDs, statuses and captures across
731,529 messages / 36,588 contextual records: 600,141 full, 131,388 provisional,
zero unknown. Both have 381 definitions; eight alternative IDs differ, with no
selected-assignment changes. V46 completed in 210.81 seconds and v45 in 212.22;
they ran concurrently, so this is not a controlled performance comparison.

The corrected v46 export checked 166,135 native captures with zero discrepancies.
Read-only public classifier/contract preparation of the full IS3QON log produces
59,157 template and 156 provisional assignments, zero no-matches; all three target
results are provisional. No stored Run was changed, and this is training-evidence
validation rather than unseen accuracy.

Corrected artifacts: `.codex-tmp/learner-v46-targeted20/`, including
[RESULTS.html](../.codex-tmp/learner-v46-targeted20/RESULTS.html), `audit.json`,
exact input membership, both execution receipts, target patterns/support,
controlled comparison, export and pipeline validation. Learner v46 release is
unchanged from the first experiment. Corrected candidate:
`65cb90c11b1d09ea32c1f3e2`; model: `552c1bba09ed740f7d5cb91e`; package:
`f4b4dcade0a6740f40118246`; manifest pin:
`fd62afca04801ca9afffc7bf78e5134d272cef7bf80862721efc667db868590d`.

All 20 input hashes and production catalog/selection hashes were reverified.
Production processes retain their previous start times. Future targeted experiments
must establish target presence before learning and distinguish training coverage,
post-training evaluation and genuine generalization in their results.

## Historical first-20-log regression experiment

The owner approved the quote-neutral discovery change and batched identical-template
consolidation, followed by a fresh run on 20 genuine logs. Both changes are implemented;
the isolated candidate completed in 211.85 seconds. Production remains unchanged.

## Implementation

- `tools/template_learning/regions.py` proposes conservative single-quote ranges
  over existing parser pieces. Ambiguous/nested/unclosed/multiline quotations abstain.
- `clustering.py` excludes recognized quoted contents from initial comparison.
  Their ordered positions contribute no positive agreement; missing/misaligned
  positions and empty-versus-present differences penalize similarity. Existing
  opaque fields and diagnostic comparison ranges retain ownership. The native
  inference/matching paths still establish and validate actual slot boundaries.
- `consolidate_identical_templates` combines each exact identity's original groups
  once, chooses its representative once and infers the combined evidence once.
  It checks every constituent for wording loss and reports progress. It remains
  after the one-sweep regrouping pass, preserving that pass's proposal order.

The threshold remains .72. No .60 tier, short-character type, textual date grammar,
L1/L2 split or generic remainder field was added. No frozen release was modified.

## Genuine evidence and outcomes

Inputs are exactly the v45 first-20-log set, verified by SHA-256. Baseline candidate:
`78878bcc7909a6270594404e`. Fresh inference uses no prior model or registry state.

| Measure | v45 | v46 |
|---|---:|---:|
| Native messages | 671,898 | 671,898 |
| Distinct / contextual messages | 35,327 / 35,362 | 35,327 / 35,362 |
| Full selected assignments | 545,688 | 545,688 |
| Provisional selected assignments | 126,210 | 126,210 |
| Unknown / unresolved emissions | 0 / 0 | 0 / 0 |
| Definitions | 362 | 361 |
| Supported / provisional definitions | 247 / 115 | 244 / 117 |

Every contextual record retains its selected template ID, status and complete
body/context/component capture bindings. Four alternative definitions are removed
and three added, all characterhistory name-localization formulations. None changes
the winner on the training corpus. This is not proof of unchanged unseen behavior.
Exact patterns, IDs and supporting records are in the ignored review artifacts.

Focused verification covers 129 genuine messages from 13 hash-verified logs. The
eventmanager scope pair now forms its three-KEY template before regrouping. Nine
identical culture-name candidates consolidate with exactly one derivation, all 18
native records and every field-support member retained; all nine constituents
enter the wording guard. No synthetic messages were used.

Authenticated compact export checks all 35,362 contextual messages / 671,898
occurrences, including 153,431 captures against native bytes, with zero matching
or outcome differences. Export/validation took 83.20 seconds. The 211.85-second
build includes parsing and writing. Historical v45 timing excluded raw-log parsing;
do not interpret these different runs as a controlled speedup ratio.

Seven duplicate identities were consolidated once each in the 20-log build. This
corpus contains only six pdx_locstring records; it does not reproduce the interrupted
104-log build's 19,288-record localization source. Large-corpus runtime remains
unverified. The cumulative re-inference loop itself has been removed.

## Original Run and operational boundary

Read-only classifier/contract preparation of the unchanged IS3QON capture produced
58,990 template assignments, 122 provisional assignments and 201 no-matches. All
three originally reported diagnostics remain no-match in this limited 20-log model.
The original production model had 73 training logs; this extra check is not a
same-corpus regression comparison and does not complete the original diagnostic task.

No database writes, stored Run replacement, source-log edits, production catalog
changes, model selection changes or runtime restarts occurred. The active handler
and watcher retained their October 2 start times. The 20 input hashes and production
selection/catalog hashes were reverified after completion.

An initial invocation was rejected before learning because its parser path named
the pre-registration snapshot rather than the selected registered release. The
path was corrected; the completed build/export receipts are authenticated. The
rejection log is retained, and no failed verification was hidden.

## Candidate delivery

All generated artifacts are ignored under `.codex-tmp/learner-v46-20logs/`:

- Human review: [RESULTS.html](../.codex-tmp/learner-v46-20logs/RESULTS.html).
- Learner release: `6da59b624068327fef08cb0aee02443cae786980da91c2f38a3e33f92059e2c8`.
- Learner manifest pin: `4c5f2cf71c4f36628164704db7f45866d301da76e6999a149ba9c9a74eabfe22`.
- Learner identity: `0e1b6bc3cdca12abc422867cba81dcc81b9fa51cae33af85ef727a618e83bd86`.
- Candidate revision: `427ab272da7728c03c146843`.
- Exported model revision: `a55ed62d7914e7f98c0fa575`.
- Package: `b14e663775c741bdf96ed8f7`.
- Package manifest pin: `ad926f7c63c3e1da1a77fe8948b091be1bb25cd34afafacc401e7bcb1b4eff9a`.

The research catalog is local to that artifact directory. Neither the immutable
export format's `published` status nor `candidate-selection.json` activates it.
Review before production registration/pinning. The original diagnostic objective
and any 104-log rerun remain separate continuation work.

Reproduce focused checks with the repository interpreter:

```powershell
.\.venv\Scripts\python.exe -B -m template_learning.verify_quoted_discovery --probe .codex-tmp/learner-all-logs-20261003/quoted-similarity-input.json --trial .codex-tmp/learner-all-logs-20261003/quoted-similarity-probe.json --inventory .codex-tmp/learner-all-logs-20261003/inventory.json --output .codex-tmp/learner-v46-20logs/focused-verification.json
```

Build, comparison and export commands/receipts, original input inventory, changed
definitions, all native validation and final preservation checks accompany the
HTML report. Core source equals the retained v46 bytes used for this candidate.
