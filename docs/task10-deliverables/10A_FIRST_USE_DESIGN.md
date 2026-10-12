# Task 10A — First-use design

**Owner: Launch & Distribution. Receiver: Pipeline for the technical interface.**
Issued 2026-10-08 to Launch & Distribution; Owner halted the erroneous parallel
chat. **Trekker ID: TREK-7.** Resume this exact assignment using the
[common instructions](WORKING_AGREEMENT.md).
Read [scope, owner decisions and sequence](../TASK10_DELIVERABLES.md).
Design proposal: [FIRST_USE_DESIGN.md](../task10/FIRST_USE_DESIGN.md).
Live delivery/technical receipt remains on TREK-7.

## Outcome

Deliver a concrete, implementable journey from downloading CK3Chronicle to setup,
starting/stopping observation and reading reports. Use the received Task 09 product;
this is not a new analysis UI or a NiceGUI implementation.

Read the existing Task 10 draft, Owner Product Intent, root instructions and Task 09
baseline. Inspect actual CLI/configuration/release interfaces and existing help.
Refresh TREK-6 and [10A.1](10A1_PIPELINE_INTERFACES.md); later refresh 10B/10D/10E
for questions about the proposed flow. Do not confuse a proposed interface with
one already delivered.

Write `docs/task10/FIRST_USE_DESIGN.md`, concise enough to implement, with:

- The user's actual steps and representative prompts/results: choose installation
  and writable data locations, configure CK3/mod/log paths, inspect the shipped
  model identity, initialize storage, start/stop and obtain a report. Support setup
  before a live error.log exists. Identify required paths and what setup creates.
- One central configuration entry: explicit `--config <path>` or the established
  fixed LocalAppData `ck3chronicle/paths.toml` bootstrap; no runtime discovery or
  fallback searches. Owner correction, 2026-10-08: setup may suggest/check bounded
  Steam and Windows Known Folder paths, requiring individual user acceptance for
  each external root. Values remain editable and specific to the user's machine;
  only external game/mod/log contents are read-only. Specify precedence, relative-path base and propagation to child
  processes. Separate read-only installed files from writable user data.
- Repeat-setup and existing-data behavior, model-selection timing, useful errors
  and basic recovery instructions. Never reset history or silently activate startup
  services. Setup must work before a configuration file exists.
- A Windows distribution recommendation and application/launcher boundary. Prefer
  a versioned runnable bundle with its runtime/dependencies and a guided setup
  launcher unless concrete evidence favors another format. Choose routine packaging
  details with Pipeline; bring only material user-facing tradeoffs to the Owner.
- Observable acceptance examples using genuine available evidence, with mappings
  to 10C and documentation needs for 10D/10E. Do not invent product features to
  fill a checklist. Owner correction, 2026-10-08: the existing doctor must diagnose
  missing/suspicious configuration and explain likely consequences and corrections,
  including CK3 identity beyond path existence. Expect the logs directory; allow
  setup before a current error.log exists. See the revised design for the contract.

## Technical agreement and limits

Deliver the proposed configuration/initialization/launch interface to Pipeline on
this record. Pipeline's issued 10A.1 reviews it for feasibility, returns concrete
corrections and receives the usable agreement. Resolve routine details directly
through those records. Only unmet requirements/material scope choices need Owner
disposition; Advisory is not a gate. 10B can prepare against the received agreement.

Permitted edits: this design/handoff, proposed user-facing examples, owned Task 10
documentation and the coordinated governance/pointer alignment described in the
index after Task 09's frozen publication. No application/configuration code or
installer implementation in 10A. Technical implementation belongs to 10A.1; setup
launcher/distribution implementation belongs to 10B.

Completion: the journey, ownership and interfaces are actionable, Pipeline has
received its technical boundary, and remaining product choices have a concrete
recommendation and accountable owner. An unaccepted material choice blocks only
affected work. Record the design delivery/receipt and provide the first short owner
brief: result, evidence/limit, remaining action, decision or "none".
