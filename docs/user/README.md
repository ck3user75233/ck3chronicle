# ck3chronicle user manual

For **ck3chronicle 0.0.3 for Windows x64**. Follow the reading order below to
understand the product, set it up and investigate your CK3 Runs.

## Meet the product

1. [Product Version](PRODUCT_VERSION.md) — distinguish the application, model,
   Learner and manual versions; [check your copy](PRODUCT_VERSION.md#check-your-copy).
2. [Introduction](INTRODUCTION.md) — purpose, audience and
   [questions it helps you answer](INTRODUCTION.md#questions-it-helps-you-answer),
   with a worked explanation of [templates](INTRODUCTION.md#why-templates-help).
3. [Orientation to ck3chronicle](ORIENTATION.md) — follow the
   [journey from CK3 exit to a report](ORIENTATION.md#from-ck3-exit-to-a-report),
   understand [Run contents](ORIENTATION.md#what-a-stored-run-contains) and
   [packages](ORIENTATION.md#templates-and-packages), and look up
   [terms](ORIENTATION.md#terms-at-a-glance).

## Install and investigate

4. [Installation and launch](INSTALLATION.md) — verify the bundle,
   [choose folders in the wizard](INSTALLATION.md#choose-folders-and-save-settings),
   [start and stop](INSTALLATION.md#start-and-stop), and optionally
   [start observation at Windows sign-in](INSTALLATION.md#optional-startup-at-windows-sign-in).
   The [Windows launcher reference](DISTRIBUTION_REFERENCE.md) lists the entry points.
5. [Everyday workflows](WORKFLOWS.md) — observe a session,
   [process a protected log](WORKFLOWS.md#process-an-already-captured-log),
   [find diagnostics](WORKFLOWS.md#find-a-run-and-investigate-diagnostics),
   [compare Runs](WORKFLOWS.md#compare-runs) and
   [save reports](WORKFLOWS.md#save-reports-for-later-or-for-another-tool).
6. [Understanding diagnostics, report queries and source context](REPORT_QUERY_REFERENCE.md)
   — choose filters, interpret [history](REPORT_QUERY_REFERENCE.md#history-and-display),
   add [source context](REPORT_QUERY_REFERENCE.md#source-selection-json) and
   read [report JSON](REPORT_QUERY_REFERENCE.md#reading-report-json).
7. [External data access](EXTERNAL_DATA.md) — connect to SQLite safely,
   [query tables and JSON](EXTERNAL_DATA.md#tables-keys-and-json), and
   [view native review evidence](EXTERNAL_DATA.md#locate-and-view-a-native-review-shard-separately).

## Configure and look up details

8. [Configuration reference](CONFIGURATION_REFERENCE.md) — settings authority,
   [TOML fields](CONFIGURATION_REFERENCE.md#toml-fields),
   [raw-log retention](CONFIGURATION_REFERENCE.md#automatic-processing-and-raw-log-retention)
   and generated evidence.
9. [Command reference](CLI_REFERENCE.md) — syntax, options, outputs and exit codes
   for setup, doctor, capture, watch, ingest, runs, report and runtime stop.
10. [Advanced model and Learner administration](RELEASE_REFERENCE.md) — inspect
    [catalogs](RELEASE_REFERENCE.md#model-catalog-commands), select an exact Learner,
    build and evaluate candidates, and maintain immutable releases.
    [Python application interfaces](PIPELINE_REFERENCE.md) covers library callers.
11. [Troubleshooting](TROUBLESHOOTING.md) — resolve setup findings, find an expected
    Run, interpret empty results and collect useful evidence when seeking help.
12. [Planned Features](PLANNED_FEATURES.md) — future direction and exploratory ideas.

## Find a task quickly

| You want to… | Start here |
|---|---|
| Debug a changed script | [Find a Run and investigate diagnostics](WORKFLOWS.md#find-a-run-and-investigate-diagnostics) |
| Inspect your selected model | [Inspect or change the selected model](WORKFLOWS.md#inspect-or-change-the-selected-model) |
| Share results with another tool or assistant | [Save reports](WORKFLOWS.md#save-reports-for-later-or-for-another-tool) |
| Understand a term | [Terms at a glance](ORIENTATION.md#terms-at-a-glance) |
| Locate execution logs | [Find and read execution logs](WORKFLOWS.md#find-and-read-execution-logs) |

Examples use PowerShell from the extracted application folder. Replace
illustrative paths and placeholders with your locations. The CMD launchers use
the bundled Python runtime. Sample output is labelled where shown.
