# Task 10E — User workflows and external data access

**Owner: Launch & Distribution — Docs role.** Finalized for owner issuance.
**Trekker ID: TREK-15.** Owner-issued 2026-10-08. Follow the [common instructions](WORKING_AGREEMENT.md)
and [scope/index](../TASK10_DELIVERABLES.md), especially the Owner's MVP limits.

## Outcome

Write practical user instructions for using CK3Chronicle and accessing its stored
data independently. Basic access is sufficient for this MVP: users may write SQL
or reshape JSON fields themselves. No new flattened CSV/XML exporter, visualization
connector, dashboard or combined diagnostic/review-shard dataset is required.

Draft from the existing product now. Retrieve [10A](10A_FIRST_USE_DESIGN.md)'s
journey, [10A.1](10A1_PIPELINE_INTERFACES.md)'s actual technical/data access interface,
[10B](10B_DISTRIBUTION.md)'s installed layout and [10D](10D_PRODUCT_REFERENCE.md)'s
reference. Refresh relevant producer records before asking the Owner to relay
technical information. Distinguish planned interfaces from delivered behavior.
Use 10D's component contributions for technical meaning; Docs owns explaining
the cross-component journey. Return factual gaps to the named component owner
through the same records and the bounded contribution route in 10D.

## Guides and boundaries

Own `docs/user/WORKFLOWS.md` and `docs/user/EXTERNAL_DATA.md`, with links to the
shared manual index/reference. Use goal-oriented steps, expected results, required
inputs and useful troubleshooting. Cover setup/repeat setup, start/stop observation,
manual captured-log processing, investigating/comparing Runs, existing report
exports, selected-model inspection/change and locating/understanding execution logs.
Document backup/recovery only to the extent a supported procedure actually exists;
do not imply a database export preserves all external evidence or full app state.

The external data guide must show:

- How to identify the configured SQLite file/schema and use Pipeline's documented
  read-only or consistent-snapshot route. State whether access is live or a dated
  copy and the applicable connection/writer conditions. Do not assume an arbitrary
  file copy during writes is a consistent export.
- Tables, important keys/relationships and JSON fields. Explain diagnostic records
  versus occurrence counts, Run timestamps, template/provisional status, package
  lineage, missing facts and database scope. Simple documented queries may inspect
  stored fields; do not create another semantic classification/projection layer.
- A worked example opening the data with a compatible external SQLite tool and
  retrieving a meaningful result that agrees with product evidence. Choose one
  readily available supported tool; no obligation to support every visualization
  engine or install unrelated paid software. Tool choice cannot become a new
  mandatory product runtime dependency.
- A separate explanation of review shards: unresolved native evidence, Run-linked
  references, actual file format and supported way to locate/view it. Shard data is
  not ordinary diagnostic rows. Do not combine it into diagnostic counts or design
  one unified view. Do not promise the database reconstructs the original error.log.

Keep manipulation/reshaping examples modest. A user needing to extract JSON fields
is an accepted MVP limitation, not a hidden acceptance defect. If existing access
cannot meet the basic workflow, give Pipeline's issued 10A.1 the exact gap; it owns
any bounded access mechanism. You own no database/schema/handler or product code.

## Evidence and receipt

Actually follow the core guides using the received installed commands and genuine
data. This assignment permits documented read-only access and ordinary setup,
selection, captured-input ingestion and report-output operations in task-owned
isolated configuration/storage. Coordinate shared example runs with 10D and reuse
their exact evidence where it applies. No producer code repair, production action,
new training campaign or synthetic/fault-injection test is authorized.

For each worked journey record product/tool version, prerequisites and input
references, exact commands/steps, expected result, actual output/exit status and
the resulting files or stored facts that establish the outcome. An external SQL
query must yield a meaningful result checked against the product/stored evidence,
not merely demonstrate opening a connection. Use real references and missing-data
explanations; review-shard viewing remains separate evidence, not a join exercise.

Show concise copyable command/output snippets in the guide and real screenshots
where visual navigation matters. Keep original evidence outside Git; sanitize
public examples and label substituted paths or shortened outputs. Follow 10D's
example evidence rules. Distinguish fresh execution, applicable reused receipts and
unexecuted cases. Expensive/admin operations may use applicable prior evidence;
do not claim every variant was tested. Explain any required journey still blocked
and its exact owner/action instead of hiding it in a screenshot or success message.

Write `docs/task10/WORKFLOWS_HANDOFF.md`, linking guide revision, evidence and limits.
Deliver on this record for [10C](10C_ACCEPTANCE.md) to receive by following it.
Documentation errors remain here; technical repairs stay with their owning component.
No ordinary user should have to read this handoff or Trekker to follow the guide.
