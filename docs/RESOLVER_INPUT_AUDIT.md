# Resolver input audit

Date: 2026-08-14

This audit prevents future agents from rebuilding source-resolution mechanics
from scratch or importing the obsolete `session.mods` execution model.

## Accepted inputs

### On-actions

Sources:

- `C:\Users\nateb\.ck3raven\wip\ON_ACTIONS_RESOLVER_DESIGN.md`
- `C:\Users\nateb\.ck3raven\wip\on_action_resolver_v2.py`

Reusable contract:

1. identical relative paths are resolved at the file layer;
2. surviving files with the same on-action name use container merge;
3. append slots accumulate with provenance;
4. single slots such as `effect`, `trigger`, and `weight_multiplier` require an
   explicit winning contribution and conflict record.

The old WIP command/session plumbing is not a production dependency.

### Cultures

Sources:

- `C:\Users\nateb\.ck3raven\wip\EC724_Conflict_Analysis\Culture Utilities\README-culture_resolver.md`
- `C:\Users\nateb\.ck3raven\wip\EC724_Conflict_Analysis\Culture Utilities\culture_resolver.py`

Reusable contract:

1. resolve identical relative paths first;
2. parse definitions from surviving files;
3. apply symbol-level last-definition-wins across culture IDs;
4. retain every losing and winning definition with source/load-order provenance.

Fuzzy duplicate-culture scoring is useful analysis infrastructure but is not a
runtime override rule and is outside the first adapter.

### `ck3_conflicts`

Sources:

- `tools/ck3lens_mcp/ck3lens/unified_tools.py`
- `tools/ck3lens_mcp/ck3lens/policy/executors.py`
- `tools/ck3lens_mcp/ck3lens/impl/conflict_ops.py`
- `tools/ck3lens_mcp/ck3lens/impl/diff_ops.py`

Reusable ideas are active-set scoping, explicit conflict records, per-instance
load order, content hashes, and bounded line/AST diff artifacts. The MCP routing,
broken ck3raven database dependency, CVID/session coupling, and `session.mods`
authority are not reusable in ck3chronicle. Filename substring heuristics may
generate review candidates but cannot establish CK3 merge semantics.

## Production direction

`ck3chronicle.source_resolution` now owns the common active-runtime file chain,
immutable processing-time fingerprints, and file-layer winner. Domain adapters
must consume that chain. The next implementation slice is on-action container
merge, followed by culture symbol LIOS; neither adapter may broaden visibility
beyond the session's archived `Mounted Data:` roots.
