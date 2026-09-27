# Native wording survey for literal guidance

Subsequent owner direction (2026-09-21) endorses default words beyond these
specific phrases and CK3 symbol type names. The active declaration is now
[owner_rules.json](../tools/template_learning/owner_rules.json); see
[implementation and comparison](LEARNER_DEFAULT_LITERALS_REVIEW.md).
The proposal-only status below describes this earlier survey.

2026-09-20. This follows the owner's direction to inspect other wording serving
the role of `target`, `Reason` and `due to`, and to inspect the values behind
`Wrong scope for <KEY>` before choosing separate formulations.

## Implemented punctuation correction

The live declaration now contains `target`, `Reason`, `due to`. The colon is
not part of these wording entries. Actual native parser pieces include:

```text
token("Reason") | token(":") | gap(" \r\n")
token("due") | gap(" ") | token("to") | token(":") | gap("\n")
```

The existing punctuation anchors still preserve colons. `Reason` retains its
native capital R; lowercase `reason` is a separate potential guidance entry,
not a case-insensitive alias.

Across all 15,646 distinct source/region/context/text units in the inspected
bundle, removing the colons loses no existing punctuation or guidance anchors.
It additionally protects `due to` in 194 units representing 38,310 occurrences
with no following colon. These include actual messages such as:

```text
Could not find texture due to 'VFSOpen Error:  not found'
Modifier 'trad_authority' doesn't match expected type 'character' due to '}'
```

These are counts of newly protected wording, not measured classification gains.
The prior immutable model retains its original declaration; it has not been
rewritten. A subsequent build will record the corrected declaration and hash.

## Scope and method

The survey uses the complete native evidence behind candidate
`87b4eed8261625c4ba9ff05c`: 48 logs, 110 sources and 1,940,027 message occurrences.
It does not include the additional 25 logs from the previous comparison.
Repeated text is counted separately from distinct formulations. L1 and L2
remain separate learning units within their source; ordinary messages remain
complete messages. Counts for L1 and L2 must not be summed as different errors.
Different trace content can also make ordinary messages distinct; these counts
are not counts of error templates.

The read-only [survey tool](../tools/template_learning/inspect_literal_wording.py)
indexes exact existing word pieces and phrases, including labels before colon
pieces. This is a search inventory, not subphrase-template construction. It
also checks the actual captures of each candidate against its own recorded
support. Examples retain complete native messages, parser pieces, source,
learning region and original byte provenance. Selected original emissions are
freshly reparsed to verify that evidence. Bundle hashes are validated.

No additional proposed wording below has been installed. No model build,
registry change, template confirmation or production promotion occurred.

## Wrong scope: the slot contains effect or trigger

In `jomini_script_system.cpp` L2, the first KEY of the general candidate has
exactly two observed values: `effect` and `trigger`.

| Native wording | Distinct complete L2 texts | Occurrences |
|---|---:|---:|
| `Wrong scope for trigger` | 18 | 190,746 |
| `Wrong scope for effect` | 8 | 425 |

Actual L2 examples:

```text
Wrong scope for trigger: war, expected character
Wrong scope for trigger: character, expected culture
Wrong scope for effect: none, expected faith
Wrong scope for effect: landed_title, expected character
```

I recommend supplying both `Wrong scope for trigger` and `Wrong scope for effect`
as literal wording. This keeps their operation categories literal and allows
the learner to infer the changing scope values. For the single-expected-scope
form, the resulting intended formulations are:

```text
Wrong scope for trigger: <KEY>, expected <KEY>
Wrong scope for effect: <KEY>, expected <KEY>
```

Some native expected-scope lists contain commas, for example
`Wrong scope for trigger: culture, expected character, landed_title, province`.
Those punctuation boundaries remain intact; this recommendation introduces no
special slot type or new list rule. These are independent L2 formulations,
not restrictions on which L1 may accompany them.

Using the complete phrases is a narrower initial instruction than declaring
every occurrence of `trigger` and `effect` literal. The corpus also uses those
words in L1 categories and other sources. For example, `jomini_onaction.cpp`
reports `There is more than one 'effect' defined using most recent:file: ...`.
That example does not prove a variable role; it shows why the Wrong-scope
finding alone should not decide every other context.

## Highest-priority additional wording

These entries have direct evidence that current candidates capture some of the
wording as variables. Counts below are supporting native units and occurrences,
not every message a broad candidate could match and not promised ambiguity
reductions. Each source and region is inspected independently.

| Proposed literal wording | Source and region | Current capture problem | Distinct units / occurrences |
|---|---|---|---:|
| `Wrong scope for trigger` | jomini_script_system.cpp, L2 | `trigger` becomes KEY | 10 / 128,926 |
| `Wrong scope for effect` | jomini_script_system.cpp, L2 | `effect` becomes KEY | 8 / 425 |
| `Event target link` | jomini_script_system.cpp, ordinary message | `Event` becomes KEY; `link` becomes OPTIONAL_KEY | 354 / 11,869 |
| `Undefined event target` | jomini_script_system.cpp, ordinary message | `Undefined` becomes KEY; `event` becomes OPTIONAL_KEY | 176 / 10,401 |
| `Failed to` | jomini_script_system.cpp, ordinary message | Failure wording becomes slots | 22 / 18,673 |
| `Could not` | jomini_script_system.cpp, ordinary message | `Could` and `not` become KEY | 13 / 32 |
| `Invalid` | jomini_script_system.cpp, ordinary message | `Invalid` becomes KEY | 38 / 18,407 |
| `Near file` | jomini_dynamicdescription.cpp, ordinary message | `Near` becomes OPTIONAL_KEY | 7 / 7 |
| `Internal ID` | jomini_script_system.cpp, L2 | `Internal` becomes KEY and `ID` enters PARAM | 7 / 7 |

`Failed to` and `Could not` are also swallowed by candidates in
`pdx_data_factory.cpp`, each in two supporting messages / four occurrences.
Native examples are:

```text
Failed to find type 'sender' in 'sender.Custom2('AppropriateGreetingPositive', ROOT.Char)'.
Could not find promote for 'sender' in 'sender.Custom2('AppropriateGreetingPositive', ROOT.Char)'.
```

Those differing introductions describe different failures; they are not names
for the changing object. Guiding the phrases preserves that distinction while
leaving subsequent variable positions to inference.

The `Near file` candidate has only seven supporting occurrences where it
captures `Near`, but it also competes on the 448 training occurrences documented
in the preceding comparison. Supporting evidence and all accepted matches are
different populations. Protecting the phrase permits formulations with and
without `Near`; it does not introduce an optional literal.

`Internal ID` shows another concrete boundary loss. In one native actor/recipient
dump the ending `(Internal ID 295225)` is captured as KEY `Internal` and PARAM
`ID 295225`. Supplying the label preserves the boundary before the number.
It does not prescribe the numeric slot type or create a new nested template.

## Other useful boundary wording

These phrases recur in native records in roles that mark what a value means or
where a variable region ends. In the inspected candidates' own support, they
are already preserved as literals, so the survey does not establish an immediate
matching improvement from adding them.

| Wording | Native example or role | Evidence in an individual source/region |
|---|---|---|
| `expected`, `Expected`, `but got` | `Event 'pregnancy.2102' expected scope 'character', but got 'none'` | eventmanager.cpp: 5 distinct messages / 1,144 occurrences; case variants remain separate |
| `Scope` | `This scope doesn't support variables. Scope: empty` | jomini_script_system.cpp L2: 281 colon-label variants / 1,241 occurrences |
| `Type` | `Variable not of the 'value' scope type. Type: empty` | jomini_script_system.cpp L2: 86 / 2,101 |
| `near line` | `Malformed token: +7, near line: 12` | pdx_persistent_reader.cpp: 2,801 / 92,715 |
| `at file` | Introduces the file value while retaining the words outside LOCATOR | e.g. jomini_eventscope.cpp: 20 / 4,914 |
| `Historical ID` | Label before an ID in a rendered character description | jomini_script_system.cpp L2: 475 / 627 |
| `was null` | `who was null`, `target slot was null` | jomini_script_system.cpp L2: 28 / 90,578 |
| `not found` | `Key poet not found at Database: common/traits` | databases.h: 2 / 319,417 |
| `does not exist` | `Catalyst 'tct_papal_hre_opinions' does not exist` | jomini_script_system.cpp L2: 4 / 126 |
| `Unknown trigger`, `Unknown effect` | Introductions before the unrecognized symbol | pdx_persistent_reader.cpp: respectively 321 / 43,353 and 5 / 183 |
| lowercase `reason` | `activity with reason: 'Unknown - enable aiwatch to see.'` | ai_activity.cpp: 4 / 603; distinct from `Reason` |
| `because` | Joins a failed operation to its explanation | characterhistory.cpp: 10 / 10; jomini_script_system.cpp L2: 8 / 8 |

These observations establish wording worth reviewing, not new message-splitting
conventions or proof that each word is universally literal in every context.
In particular, reason-introducing phrases do not themselves establish another
L1/L2 architecture. `Unable to` was searched but has no exact native match in
this inspected corpus and is not an evidence-backed addition here.

## Recommendation and evidence

Start with the high-priority wording above, especially the two Wrong-scope
introductions, `Event target link` / `Undefined event target`, failure verbs,
and `Near file`. They address observed literal loss instead of merely selecting
frequent words. Keep the other boundary labels as an explicit second group for
review. Newly supplied wording should be recorded as guidance, followed by a
fresh native comparison; it should not become a hand-authored template catalog.

This survey does not resolve the underlying overgeneralization of unprotected
wording or establish classification gains. Those require rebuilding and comparing
complete records. The only active guidance edit in this task is removal of the
colons from the already supplied wording.

Artifacts in the ignored survey directory:

- [Audit and original native examples](../.codex-tmp/learner-refactor/literal-wording-survey/audit.json)
- [Actual candidate captures of proposed wording](../.codex-tmp/learner-refactor/literal-wording-survey/wording-current-slot-conflicts.json)
- [Colon correction check](../.codex-tmp/learner-refactor/literal-wording-survey/colon-correction-check.json)
- [Colon-label inventory](../.codex-tmp/learner-refactor/literal-wording-survey/colon-label-inventory.json)
- [Word/phrase search inventory](../.codex-tmp/learner-refactor/literal-wording-survey/phrase-inventory.json)
