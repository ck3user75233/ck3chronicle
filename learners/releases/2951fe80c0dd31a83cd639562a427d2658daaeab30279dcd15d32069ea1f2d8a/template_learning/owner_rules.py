"""Load the explicit reference declarations; never rewrite project source code."""
import json
from pathlib import Path
import re
from template_learning.full_ids import FullIdRules

OWNER_RULES = json.loads(Path(__file__).with_name("owner_rules.json").read_text(encoding="utf-8"))
if OWNER_RULES.get("schema") != "ck3chronicle.learner-owner-rules" or OWNER_RULES.get("version") != 1:
    raise ValueError("unsupported learner owner-rule reference")

defaults = OWNER_RULES["default_literals"]
words = []
for group in defaults["groups"]:
    declared = group["words"]
    if len(set(declared)) != len(declared):
        raise ValueError("duplicate wording within default-literal group")
    for word in declared:
        words.append(word)
        if group["first_letter_case_insensitive"] and word:
            words.extend((word[0].lower() + word[1:], word[0].upper() + word[1:]))
# The same spelling can have diagnostic and symbol-type provenance. Keep one
# effective literal; preserve both declarations in the snapshotted reference.
words = list(dict.fromkeys(words))
phrases = defaults["phrases"]
if (any(not isinstance(s, str) or not s or s != s.strip() for s in words + phrases)
        or any(any(c.isspace() for c in word) for word in words)
        or len(set(words + phrases)) != len(words + phrases)):
    raise ValueError("invalid or duplicate default literal wording")

LITERAL_GUIDANCE = dict(schema="ck3chronicle.learner-literal-guidance", version=1,
    enabled=defaults['enabled'],literals=words + phrases if defaults['enabled'] else [],
    authority=defaults['authority'] if defaults['enabled'] else defaults['disabled_authority'],matching=defaults["matching"],
    reference_file="owner_rules.json", rule_id=defaults["id"])
CONSTRUCTIONS = OWNER_RULES["constructions"]
INFERENCE_POLICY = OWNER_RULES["inference_policy"]
LOCATION_LABEL_EQUIVALENCES = OWNER_RULES["location_label_equivalences"]["groups"]
for declaration in OWNER_RULES.get('formatted_literals', ()):
    re.compile(declaration['prefix'])
    compiled = re.compile(declaration['pattern'])
    if compiled.match('') or not declaration['suffix']:
        raise ValueError('formatted literals require nonempty content and an ending marker')
DIAGNOSTIC_WORDING_LOSS = OWNER_RULES['diagnostic_wording_loss']
loss_types = DIAGNOSTIC_WORDING_LOSS['target_slot_types']
if (not loss_types or len(set(loss_types)) != len(loss_types)
        or not set(loss_types) <= {'KEY', 'OPTIONAL_KEY', 'PARAM'}):
    raise ValueError('invalid diagnostic-wording loss target slot types')
enclosed_loss = DIAGNOSTIC_WORDING_LOSS['enclosed_identifier_evidence']
if (not enclosed_loss['slot_types'] or not set(enclosed_loss['slot_types']) <= {'KEY', 'OPTIONAL_KEY'}
        or type(enclosed_loss['minimum_distinct_nonempty_values']) is not int
        or enclosed_loss['minimum_distinct_nonempty_values'] < 2):
    raise ValueError('invalid enclosed identifier evidence declaration')
reference_groups = {group['id']: group for group in defaults['groups']}
symbol_group = reference_groups[DIAGNOSTIC_WORDING_LOSS['symbol_type_group']]
loss_symbols = []
for word in symbol_group['words']:
    loss_symbols.append(word)
    if symbol_group['first_letter_case_insensitive']:
        loss_symbols.extend((word[0].lower()+word[1:], word[0].upper()+word[1:]))
if not set(DIAGNOSTIC_WORDING_LOSS['symbol_type_phrases']) <= set(phrases):
    raise ValueError('diagnostic loss phrases must refer to retained complete phrases')
LOSS_REFERENCE_WORDING = tuple(dict.fromkeys([*loss_symbols,
    *DIAGNOSTIC_WORDING_LOSS['symbol_type_phrases']])) if DIAGNOSTIC_WORDING_LOSS['enabled'] else ()
parameters=OWNER_RULES['parameter_structures']
if len({d['id'] for d in parameters})!=len(parameters):
    raise ValueError('duplicate parameter structure declaration')
for definition in parameters:
    if definition['mechanic']=='full_id':
        continue
    re.compile(definition['prefix'])
    if definition['mechanic']=='line_sequence':
        re.compile(definition['content'])
    elif definition['mechanic'] in {'balanced_interior','through_balanced_suffix'}:
        if len(definition['delimiters'])!=2 or any(len(x)!=1 for x in definition['delimiters']):
            raise ValueError('parameter delimiters must be two raw punctuation tokens')
        if definition['mechanic']=='through_balanced_suffix':
            re.compile(definition['content_required'])
    else:
        raise ValueError('unsupported parameter structure mechanic')
FullIdRules(parameters)  # Validate shared typed-field declarations at load time.
if len({d["id"] for d in CONSTRUCTIONS}) != len(CONSTRUCTIONS):
    raise ValueError("duplicate construction declaration")
for declaration in CONSTRUCTIONS:
    compiled = re.compile(declaration["pattern"])
    if tuple(compiled.groupindex) != tuple(declaration["region_order"]):
        raise ValueError("construction capture names disagree with region order")
    if not (set(declaration["fields"]) | set(declaration["comparison_regions"])) <= set(compiled.groupindex):
        raise ValueError("construction refers to absent regions")
    excluded=set(declaration.get('excludes',()))
    if declaration['id'] in excluded or not excluded <= {d['id'] for d in CONSTRUCTIONS}:
        raise ValueError('invalid construction exclusions')
SLOT_POSITION_CUES = OWNER_RULES["slot_position_cues"]
cue_flags = 0 if SLOT_POSITION_CUES["case_sensitive"] else re.I
LOCATION_CUE = re.compile(SLOT_POSITION_CUES["location_pattern"], cue_flags)
PATH_VALUE_CUE = re.compile(SLOT_POSITION_CUES["path_value_context_pattern"])
FILE_VALUE_CUE = re.compile(SLOT_POSITION_CUES["filename_context_pattern"], cue_flags)
FILENAME_SUFFIXES = frozenset(SLOT_POSITION_CUES["filename_suffixes"])
IDENTIFIER_CUE = re.compile(SLOT_POSITION_CUES["identifier_pattern"], cue_flags)
