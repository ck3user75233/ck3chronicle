**Learner deliverables: native-message model for the pipeline**


First version the learner's current parser and make it selectable (A2), then
deliver A's native-message model with its exact parser reference. The learner
team owns this setup. Compare parser designs and select a canonical candidate
later in B5. Continue B in parallel after integration; error typing is also
required for the later Error Contracts.
**A. Required outputs**

| Output | Delivery requirement |
|---|---|
| **A1. Loadable model bundle** | Deliver an immutable revision containing `empirical_template_model.json`, `manifest.json`, build command, content hashes, source applicability, template IDs and training provenance. Verify pipeline loading/classification. |
| **A2. Versioned, selectable learner parser** | Package the current parser in a versioned subfolder, e.g. `tools/template_learning/parsers/<version>/`, with a documented callable interface for emissions, individual messages and native spans. Refactor the learner/evaluator to import an explicitly selected version; continue with the current parser initially. Each model must reference the exact parser version, retrievable artifact and content hash covering its implementation. Retain published versions. Demonstrate that an independent consumer using that reference obtains identical boundaries/spans. This parser is the initial canonical candidate. |
| **A3. Complete native templates** | After the selected parser's header/child framing, preserve every message literal, punctuation mark and suffix outside slots. Examples: `Unknown trigger: <KEY>, near line: <LOCATOR>` captures `261`; `<PARAM> of (Internal ID <KEY>)` preserves the surrounding words. Retain script-location tails. Additional preprocessing requires an exact primitive list, rationale and prior owner approval. |
| **A4. Five slot types and consumer definitions** | Use only the five types below unless owner-directed. Document meanings, boundaries, optionality and constraints/limitations. Confirm punctuation/numerics preserve one complete KEY rather than causing decomposition or conversion to PARAM. Remove TYPE and ALT. |
| **A5. Explicit layer structure** | Supply source-applicable L1/L2 boundaries with complete native content. L1 is independently assignable; applicable L2s are reusable across L1s. Agree trailing-location encoding with the pipeline team. |
| **A6. Visible owner overrides** | Deliver the owner-approved rule list, rationale and affected template IDs, or an empty list. Overrides take precedence. Compare raw model versus model-plus-overrides and review changed results. |
| **A7. Integration evidence** | Deliver genuine examples with template IDs, captures and native spans: dotted/numeric KEYs, variable PARAMs, present/absent OPTIONAL_KEYs, LOCATOR/VALUE, preserved suffixes and layered reuse. List unresolved evidence and coverage gaps. |

| Allowed slot | Consumer contract |
|---|---|
| `KEY` | One continuous string, including punctuation and numeric components: e.g. `capital_county.kingdom`, `enfp_test.0001`. Capture the whole value at the supplied position. |
| `OPTIONAL_KEY` | A KEY or absence at an explicitly declared optional position. |
| `PARAM` | Variable-length text, including multi-word names/phrases and quoted/bracketed content. Surrounding template structure determines its boundaries. |
| `LOCATOR` | A location value, including a filename/path, line number or range. Keep labels such as `, near line:` literal; capture the location text itself. |
| `VALUE` | Exact template-declared value; document its meaning/constraints. Downstream applies only supplied constraints. |

**Integration coordination:** the current reader uses schema
`ck3chronicle.empirical-structures` v1, matching view
`ck3-native-literal-view-v2` and recovery `ck3-diagnostic-recovery-v1`.
These are current pipeline identities, not an already shared parser contract.
Agree parser-reference metadata, the consumer interface and layered trailing-content
encoding with the pipeline team; the current layered format only represents
`L1 [ L2 ]`. Pipeline integration must use the model's referenced parser,
verify its hash and wire the corresponding reader/catalog changes. Parser
packaging preserves version identity; A3 still governs the generated templates.

**B. Learner/model improvements after structural integration**

| Work | Concrete result |
|---|---|
| **B1. Literal/slot generalization and repetition** (M3/M4/M9; MODEL-001/002) | Verify defects against templates/native messages. Deduplicate messages for frequency-based derivation; retain occurrence counts separately and test burst invariance. Investigate fixed event prefix `45442966e4e35fa0`, localization KEY-as-PARAM `f0565bd0fc1252a8`, and unexplained KEY before `expected` in `dc3b833218ba04c4`. Reported namespace evidence has 18/21 distinct identifiers sharing a prefix; deduplication alone may be insufficient. |
| **B2. Naming-phrase boundaries** (M5; travel template `991ba68d50653950`) | Improve PARAM boundaries across character/place/title naming variants. Native-literal repair belongs to A3. Verify suspected literal CK3 symbols against templates; test whether symbol references help locate variable positions. Propose useful rules or specialized name slots with demonstrated benefit for owner approval. |
| **B3. Deterministic error typing** (M1) | Verify the earlier proposal. Deliver a defined-corpus word/phrase inventory with co-occurrences, deterministic association-table generator and unresolved cases. Examine unknown/duplicate/orphaned/missing/invalid constructions; cover whole templates and L1/L2 composition. Obtain owner direction and publish one hierarchical `error_type` mapping. |
| **B4. Incomplete historical evidence** (M6) | Trace `1fe888497d57744c` and `21180b4a91934cbc` to learner output or later additions. Recover complete native evidence and regenerate justified structures; list remaining gaps. |
| **B5. Canonical parser evaluation** | The learner and pipeline teams compare the versioned learner parser with pipeline parsing on the same native logs: message boundaries, source attribution, multiline/child recovery and byte spans. Propose the best-fit shared parser with evidence of differences; deliver improvements as new selectable versions. Models retain their exact parser references, so existing versions remain reproducible. |

The KEY-dot-VALUE observation `94db6bb230547781` falls under A4; broader
inference improvements belong to B1. The prior 3,722-file base-game symbol
survey supports punctuation diversity; mods were unexamined and some files
had decoding gaps. It is supporting evidence, not a restrictive KEY alphabet.

**Code/behavior to retire as replacements land**

| Retire | Rationale |
|---|---|
| Sentence-specific rewriting, advance slot masking and suffix stripping | A3 learns and matches the same complete native text. |
| Fragment-level KEY rejection and punctuation-driven slot decomposition | A4 preserves one complete key per KEY slot. |
| TYPE/ALT generation | The delivered vocabulary has five approved types. Re-derive affected literals/slots from native evidence. |
| Embedded, unversioned parser copies in the learner/evaluator | A2 replaces them with imports of the explicitly selected parser version. Later consolidation follows B5's comparison. |
| Truncation that affects learned structures or their supporting evidence | Complete messages are required to establish template applicability. |

Detailed examples and evidence remain in
[MODEL_BUGS.md](../src/ck3chronicle/pipeline/MODEL_BUGS.md).
Current format checks are in [model.py](../src/ck3chronicle/pipeline/model.py).
