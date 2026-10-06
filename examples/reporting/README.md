# Reading the reporting examples

The [reporting handoff](../../docs/TASK08B_REPORTING_HANDOFF.md) records
the completed implementation/browser checks and remaining evidence limits.
These examples explain actual CLI operations; they do not imply full live Trusted
Run milestone acceptance.

The generated `outcomes.html` page maps earlier incomplete deliverables to their
completed corrections and links to the relevant reports. It also lists each
still-unverified case and the genuine evidence needed to close it. Open it from
the index or **08B delivery status and remaining gaps** in any example report.
The template example alone is not the assessment of the whole reporting task.

The investigation name and **Read explanation and evidence** both open
`#explanation` in the report. This section contains the question, expected result,
actual outcome and supporting evidence together: template patterns, Run counts,
example diagnostics and their file candidates where applicable. Named links jump
directly to the relevant detail or verbose source excerpt. Every reading copy
links back to its entry in the index. `no-eligible` explains the requested package
and selection error in place; there is no diagnostic result elsewhere to find.

Every CLI report uses this integrated opening; query details and the reading
guide are expandable. The
[check descriptions](checks.json) give each consumer example its specific
question and expected behavior, including checks whose correct outcome is a
clear rejection or a successful empty result. The generated example index uses
these descriptions; an expected behavior is not itself proof that a test passed.

For ordinary content search, use [message-search.json](message-search.json).
Search terms cover literal wording and populated slot values together. The
`message-unrecognized` and `message-context-switch` reports show the actual match
origins and assigned templates. The earlier `bound-phrase-is-not-template` example
is withdrawn: it was a contrived filter combination, not a useful content-search
workflow. Template assignment remains stored result data, not a new classification.

Other investigations:

| Query | What it asks | What it demonstrates |
|---|---|---|
| [symbol-template.json](symbol-template.json) | Find every diagnostic using the common trigger-error template, with no key/reason/message restriction. | The template is a shared placeholder pattern. Many different specific diagnostics can use it, each with separate counts and Run history. |
| [failed-context-switch.json](failed-context-switch.json) | Find script-system messages containing “failed context switch” across up to five eligible Runs. | Message matching includes values filled into a template. Per-Run totals and file rankings describe the same matching diagnostic set. |
| [member-file.json](member-file.json) | Find culture/faith context-switch messages associated with the sea-minority file in EB+EC724 Compatibility Patch. | Mod, file and grouped message filters compose; candidate association does not establish ownership. |

`D1`, `D2`, etc. are specific diagnostics. The number in each heading counts
repetitions of that diagnostic in the selected Run. Template patterns have their
own section and combined totals. Classification metadata explains how a diagnostic
was recognized; it does not turn the diagnostic into a template.

File tables show recorded mod names and load-order numbers beside candidate paths.
They use the stored playset for the Run supplying the evidence. All candidates
remain visible when several mods supply the same path. `ROOT_GAME` playset members
(base game and DLCs) need no mod-name prefix. A stored message remains unchanged;
the adjoining file table supplies this extra context.

The short and full worked reports execute the same query with different display
limits. Text, JSON and HTML are different formats of the same analysis. Their
repeated results are deliberate format/limit comparisons. The separate
`symbol-exact-partial-key` example selects one exact diagnostic to check combined
filters; it is deliberately narrower than `template-only`.

Consumer verification also checks root-command help and that HTML requires an
explicit output destination. Those command checks do not produce diagnostic reports.
The latest unchanged backup supplies seven genuine eligible Runs. `worked-five-runs`
has a full trailing-five window; `five-predecessors` and `five-successors` check
each complete comparison side separately. The earlier four-Run reports remain
available as earlier evidence. No synthetic Runs join those windows.

Opposing filters are ordinary empty queries: `new-contradiction`,
`hotspots-contradiction`, `syntax-contradiction` and `new-zero-count` return zero
matches with exit 0 while keeping the preset condition. `symbol-needs-selector`
is different: required input is missing, so the CLI rejects it before any database
request. The historically named `required-partial` example now succeeds with just
the matching culture diagnostic. The pathless localisation record is excluded
without warning. `path-excludes-unlocated` and `path-only-unlocated` demonstrate
recorded-path filtering and a successful empty result.
`dlc-path` checks plain game/DLC paths beside a named mod candidate;
`syntax-window` discloses the two of nine selectors represented in its four Runs.
The five `syntax-archive-*` reports now exercise all nine selectors using unchanged
genuine logs ingested into separate disposable single-Run databases. Their playsets
were not retained: optional context reports that absence while preserving the
diagnostics; `archive-required-playset` shows the required-filter error.

`synthetic-missing-files` is the owner's two-entry fixture: two complete genuine
emissions with only nonexistent file LOCATOR paths substituted. The normal playset
writer preserves all 133 members/orders and updates log hashes. Its report links
the fixture log, playset JSON, original emissions and verification results.
Both diagnostics remain visible with complete/no-file search results, in text,
JSON and HTML. Related examples check unresolved-path hotspots, recorded path,
directory and absolute-path selection, and successful empty results for unmentioned
paths or absent mod-file candidates. Selecting a file path no longer requires it
to exist on disk. [file-path.json](file-path.json) is the ordinary path query.
The fixture is labelled synthetic throughout and does not test unavailable roots
or alter genuine history. `history-positions` now displays all requested -5 through
+5 positions and marks unavailable Runs. `stored-data-io` traces the CLI and worker
without removing logs or models. The outcome page identifies two specific runtime
fault paths not encountered, separately from these completed checks.
