# Introduction

[Manual contents](README.md) · [Previous: Product Version](PRODUCT_VERSION.md)

CK3's live logs are volatile: the useful evidence from a gaming or testing
session can be replaced by a later session. Modders need to preserve that
evidence, recognize recurring problems, compare changes between sessions and
connect messages with relevant mod sources.

ck3chronicle protects completed `error.log` output, organizes
recognized messages into a local diagnostic history, and lets you revisit that
history after the live log has changed or disappeared. A **Run** represents one
completed CK3 session whose evidence you are investigating.

This is useful when a mod takes several launches to debug. You can investigate
the latest Run, compare a diagnostic across earlier Runs, find messages related
to a script file or identifier, and read relevant source context from the report.

## Who it is for

Use ck3chronicle when you develop or maintain CK3 mods, investigate interactions
in a playset (the loaded game content and mods), or want a repeatable record of what CK3 reported while testing a
change. The Windows setup wizard handles the initial folder and storage
choices. Day-to-day operations use launchers and command-line commands; reports
can be read as text, opened as offline HTML, or saved as JSON for other tools.

You bring an installed copy of CK3 and readable game, mod and log locations.
ck3chronicle keeps its settings and working data separately and accesses game and
mod sources read-only. Processing and storage are local.

## Questions it helps you answer

| Your question | How to investigate it |
|---|---|
| What did my latest test produce? | Open a report for the latest stored Run and review both diagnostics and unresolved-evidence counts. |
| Which messages repeat most often? | Rank diagnostic occurrence counts, then inspect the messages and their context. Frequency describes repetition, not severity. |
| Did this diagnostic appear before my change? | Examine its history across stored Runs, paying attention to the selected model package and any missing comparison evidence. |
| What did CK3 report about this file or identifier? | Filter stored messages and path references, then add source search or excerpts where useful. |
| What was enabled for that Run? | Inspect its recorded playset: the ordered base-game, DLC and mod context extracted from the captured debug log. |
| Can I analyze the results in another tool? | Export report JSON or use the documented read-only SQLite route, with native review evidence available separately. |
| Can an AI assistant help investigate an error or propose a patch? | Give it selected report JSON and relevant source excerpts so it can work from explicit messages, values, locations and coverage. Review its explanation and proposed changes against the source. |

Use these views after ordinary play as well as focused tests. Repeated problems
can guide where you spend investigation time; comparisons after a mod edit or
playset change help you see what appeared, disappeared or changed in frequency.
The comparison establishes what the available Runs reported. You decide whether
the change explains it and what action is appropriate.

## Why templates help

A **template** is an empirical reconstruction of a recurring CK3 message shape.
Think of game code emitting fixed wording and filling variable slots with the
particular key, name, location or explanation for an error. ck3chronicle learns
these shapes from observed logs; each shape describes the evidence from which
it was learned.

The fixed wording is called **literal text**. The changing contents are
**values**, and a value assigned to a particular slot is a **binding**. For
example, this message excerpt comes from a genuine stored diagnostic:

```text
Unknown trigger: adulterer, near line: 414
```

It appeared inside an error referring to
`common/scripted_triggers/zzz_99_religious_triggers.txt`, near line `415`.
The excerpt omits the surrounding error wrapper; both location values are
preserved in the stored diagnostic. A simplified way to display its shape is:

```text
Unknown trigger: <KEY>, near line: <LOCATOR>
```

The angle-bracket notation is illustrative. The published template also allows
the literal label `line:` in that position. In this particular diagnostic:

| Part | Meaning |
|---|---|
| `Unknown trigger: ` and the punctuation/location label | Literal wording selected from the template. |
| `adulterer` | The reported key, stored as a `KEY` value. |
| `414` | A `LOCATOR` value within the message. |
| The script path and `415` | Separate `LOCATOR` values in the surrounding error wrapper. |

Published templates declare which values they support. Some capture keys or
names, some retain complete references or identifiers, and some capture a
variable-length reason as one `REASON` value. A reason can be a phrase rather
than one word; its exact content remains part of that diagnostic. The declaration
determines whether a particular piece of text is literal or variable.

Two messages can share a template while naming different keys, locations or
reasons. Those different values and contexts distinguish individual diagnostic
records within the template family. Different message structures have different
templates. Repeating the same complete diagnostic within one Run increases its
**occurrence count**; the genuine example above has 11 occurrences in its Run.
Selected layout and supporting message entries also participate in the exact
identity, so a template-family total and an individual error's count answer
different questions.

You can still investigate one error directly. Structure adds consistent ways
to group and compare errors and to pass their wording and values to another
tool. [Orientation](ORIENTATION.md#templates-and-packages) explains how the
classification package applies these templates and preserves the result.

## Working with an AI assistant

A report's JSON gives an assistant explicit diagnostic wording, templates,
typed values, references, counts and available context. That reduces how much
structure it must infer from a large text log. Include the Run and package
identities, query scope and coverage, plus relevant current source excerpts, so
the assistant can explain its investigation against the same evidence you see.

Use this material to ask for possible explanations, checks to perform and
proposed patches. Assess the reasoning and review a patch before applying it:
structured evidence helps inspection, while causal attribution and the
correctness of a proposed change still need judgment. The existing
[report export workflow](WORKFLOWS.md#save-reports-for-later-or-for-another-tool)
provides the files to share; choose what to give your assistant and remove
private paths or content as appropriate.

Current source lookup, content search and excerpts support
[source-context investigation](ORIENTATION.md#how-source-context-fits). See
[Planned Features](PLANNED_FEATURES.md) for near-match assistance under exploration.

## From a test session to useful history

Start the watcher before starting CK3. After it observes CK3 exit, it protects
the logs and submits the captured error log for processing when automatic
ingestion is enabled. Successful processing creates a stored Run with compact
diagnostic records, counts, processing identities and references to evidence
that needs review. You can then query that Run from its stored records.

For an existing completed log, the manual capture and ingestion commands provide
an explicit route into the same history. That route records the evidence
available from the supplied files; an observed start and exit belong to the
automatic lifecycle route.

Classification makes recurring messages easier to inspect. Unresolved messages
remain available for review, and a template match tells you how a message was
recognized. Diagnosing the cause still requires interpreting the message and
its context: a referenced file can help locate the investigation without proving
which mod caused the problem. Source excerpts show the files currently on disk,
which may have changed since CK3 ran.

## Where to start

Read [Orientation to ck3chronicle](ORIENTATION.md) for the components, terms and
evidence flow. Then follow [Installation and launch](INSTALLATION.md) and choose
a task from [Everyday workflows](WORKFLOWS.md). Keep the
[report query reference](REPORT_QUERY_REFERENCE.md) nearby when you begin
narrowing an investigation. [Planned Features](PLANNED_FEATURES.md) describes the
near-match assistance being explored beyond the current investigation tools.

[Continue to Orientation](ORIENTATION.md) · [Manual contents](README.md)
