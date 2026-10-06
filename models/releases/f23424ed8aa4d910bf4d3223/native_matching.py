"""Public, model-pinned complete native assignment API. Standard library only."""
from copy import deepcopy
from types import SimpleNamespace

from .assignment import select_assignment, POLICY_VERSION
from .matching_primitives import (Rules, MatcherIntegrityError,
    MatcherCompatibilityError, MatcherDeclarationError, NativeInputError, MatcherError)
from .matching_validation import validate_model
from . import location_sequences, formatted_literals

API_VERSION = 'ck3-native-matcher-v3'


def assignment_candidates(matches, ambiguities):
    """Adapt all complete witnesses to the unchanged model-pinned selector."""
    result = []
    for match in [*matches, *ambiguities]:
        contexts = list(match['context_matches'].values())
        if len(contexts) > 1:
            raise NativeInputError('select one contextual diagnostic at a time')
        wrappers = {name: [dict(template_id=p['template_id'], count=p['capture_count'],
                               witnesses=p['capture_witnesses']) for p in patterns]
                    for name, patterns in (contexts[0] if contexts else {}).items()}
        result.append(dict(template_id=match['template_id'],
            body=dict(count=match.get('count', 1),
                      witnesses=match.get('witnesses', [match.get('captures')])),
            component_witnesses=match['component_witnesses'], contexts=wrappers))
    return result


class Matcher:
    """Own a defensive snapshot of explicit model data; never read learner rules."""
    def __init__(self, model):
        self._data = deepcopy(model)
        validate_model(self._data)
        self.rules = Rules(self._data['owner_rules'])
        self.by_source = {}
        self.by_id = {}
        for template in self._data['templates']:
            self.by_source.setdefault(template['source_family'], []).append(template)
            self.by_id[template['template_id']] = template

    @property
    def data(self):
        return deepcopy(self._data)

    def inspect_record(self, record):
        """Learner inspection: complete alternatives and exactly one selection."""
        ambiguities = []
        matches = [m for t in self.by_source.get(record.source_family, ())
                   if (m := self.rules.match_record(t, record,
                          capture_ambiguities=ambiguities)) is not None]
        selected = select_assignment(self._data, assignment_candidates(matches, ambiguities))
        return matches, ambiguities, selected

    def match(self, unit, *, inspect=False):
        """Return one selected assignment or explicit no_match; never bind offsets.

        Each region starts at byte zero in that region's unchanged UTF-8 /
        surrogateescape text. Caller provenance is passed through by identity.
        """
        try:
            actual = unit['parser']
            if any(actual.get(k) != self._data['parser'][k] for k in ('version', 'sha256')):
                raise MatcherCompatibilityError('native unit does not use the pinned parser')
            if unit.get('recovery_status', 'recovered') != 'recovered':
                raise NativeInputError('unresolved recovery is not a complete native unit')
            kind = unit['context_kind']
            contexts = unit['contexts']
            expected = {'prefix', 'suffix'} if kind == 'located-message-wrapper' else set()
            if set(contexts) != expected or (kind not in {'body', 'located-message-wrapper'}
                                            and not kind.startswith('continuation:')):
                raise NativeInputError('native unit requires its complete wrapper regions')
            body = unit['body']
            entries = unit['continuations']
            if bool(entries) != kind.startswith('continuation:'):
                raise NativeInputError('continuation kind and ordered regions disagree')
            for region in [body, *contexts.values(), *entries]:
                if (any(k not in {'token', 'gap'} or not isinstance(t, str)
                        for k, t in region['pieces'])
                    or ''.join(t for _, t in region['pieces']) != region['text']):
                    raise NativeInputError('pieces do not reproduce the original region')
            record = SimpleNamespace(source_family=unit['source_family'], context_kind=kind,
                text=body['text'], pieces=tuple(map(tuple, body['pieces'])),
                contexts={'native': contexts} if contexts else {}, continuations=entries)
        except (KeyError, TypeError) as exc:
            raise NativeInputError(f'incomplete native input: {exc}') from exc
        try:
            matches, ambiguities, chosen = self.inspect_record(record)
        except MatcherError:
            raise
        except ValueError as exc:
            raise NativeInputError(str(exc)) from exc
        except (KeyError, TypeError, IndexError) as exc:
            raise MatcherIntegrityError(f'inconsistent matching result: {exc}') from exc
        result = dict(api_version=API_VERSION, status='matched' if chosen else 'no_match',
                      assignment=None, provenance=unit.get('provenance'),
                      source_family=unit['source_family'], source_tag=unit.get('source_tag'))
        if chosen is not None:
            template = self.by_id[chosen['template_id']]
            regions = [self._region('body', template['parts'], body,
                chosen['captures'], dict(template_id=template['template_id'], region='body'))]
            for name in ('prefix', 'suffix'):
                if name not in chosen['context_matches']:
                    continue
                wrapper = chosen['context_matches'][name]
                pattern = next(p for p in template['context_patterns'][name]
                               if p['template_id'] == wrapper['template_id'])
                regions.append(self._region(name, pattern['parts'], contexts[name],
                    wrapper['captures'], dict(template_id=template['template_id'],
                        region=name, wrapper_template_id=pattern['template_id'])))
            if len(chosen['component_matches']) != len(entries):
                raise MatcherIntegrityError('selected component count differs from native input')
            for component in chosen['component_matches']:
                i = component['index']
                layout_index = component['layout_index']
                layout = template['continuation']['layouts'][layout_index]
                parts = [dict(kind='literal', text=layout['leading']),
                         dict(kind='slot', name='reference', type=template['continuation']['reference_type'],
                              prefix='', suffix='', optional=False),
                         dict(kind='literal', text=layout['label']),
                         dict(kind='slot', name='value', type=template['continuation']['value_type'],
                              prefix='', suffix='', optional=False),
                         dict(kind='literal', text=layout['trailing'])]
                regions.append(self._region('continuation:' + str(i), parts, entries[i],
                    component['captures'], dict(template_id=template['template_id'],
                        region='continuation', layout_index=layout_index), component_index=i))
            selection = {k: v for k, v in chosen['selection'].items() if k != 'alternatives'}
            result['assignment'] = dict(template_id=chosen['template_id'],
                template_status=chosen['template_status'], match_status=chosen['match_status'],
                regions=regions, selection=selection)
        if inspect:
            result['inspection'] = dict(matches=matches, capture_ambiguities=ambiguities,
                                        selected_assignment=chosen)
        return result

    @staticmethod
    def _region(name, parts, native, captures, layout, **extra):
        """Validate the selected relative result once; no absolute bindings."""
        parts, repeated, _ = location_sequences.expand(parts,pieces=native['pieces'])
        if parts is None:
            raise MatcherIntegrityError('selected location sequence differs')
        if repeated:
            layout = {**layout,'repeat_choices':repeated}
        slots = [p for p in parts if p['kind'] == 'slot']
        if [(p['name'], p['type']) for p in slots] != [(c['name'], c['type']) for c in captures]:
            raise MatcherIntegrityError('selected captures disagree with the selected layout')
        ordered, rendered, cursor, index = [], [], 0, 0
        literal_choices = []
        for part_index, part in enumerate(parts):
            if part['kind'] == 'literal':
                text = part['text']
                if 'literal_format' in part:
                    tail = native['text'].encode('utf-8', 'surrogateescape')[cursor:].decode('utf-8', 'surrogateescape')
                    text = formatted_literals.spelling(part, tail)
                    if text is None:
                        raise MatcherIntegrityError('selected formatted literal is missing')
                    literal_choices.append([part_index, text])
                elif 'alternatives' in part:
                    tail = native['text'].encode('utf-8', 'surrogateescape')[cursor:]
                    choices = [(i, s) for i, s in enumerate(part['alternatives'])
                               if tail.startswith(s.encode('utf-8', 'surrogateescape'))]
                    if len(choices) != 1:
                        raise MatcherIntegrityError('selected literal choice is not unique')
                    choice, text = choices[0]
                    literal_choices.append([part_index, choice])
                rendered.append(text)
                cursor += len(text.encode('utf-8', 'surrogateescape'))
                continue
            capture = captures[index]
            index += 1
            present = capture['span'] is not None
            if not present:
                if capture['value'] is not None or not part['optional']:
                    raise MatcherIntegrityError('invalid absent capture')
            else:
                value = capture['value']
                if not isinstance(value, str):
                    raise MatcherIntegrityError('present capture must contain exact native text')
                a = cursor + len(part['prefix'].encode('utf-8', 'surrogateescape'))
                b = a + len(value.encode('utf-8', 'surrogateescape'))
                if capture['span'] != [a, b]:
                    raise MatcherIntegrityError('capture is inconsistent with selected literal layout')
                rendered.append(part['prefix'] + value + part['suffix'])
                cursor = b + len(part['suffix'].encode('utf-8', 'surrogateescape'))
            ordered.append(dict(slot_id=capture['name'], type=capture['type'],
                value=capture['value'], present=present, span=capture['span']))
        if ''.join(rendered) != native['text']:
            raise MatcherIntegrityError('selected assignment does not reproduce the complete native region')
        if literal_choices:
            layout = {**layout, 'literal_choices': literal_choices}
        return dict(name=name, layout=layout, captures=ordered,
                    provenance=native.get('provenance'), **extra)


def match(model, unit, *, inspect=False):
    """Public operation: a loaded Matcher (or package) and one complete unit."""
    return model.match(unit, inspect=inspect)


def iter_native_units(raw):
    """Project pinned parser ranges into API inputs; no matching or new recovery.

    Unresolved parser output is yielded intact with recovery_status='unresolved'.
    It must be retained for review, not passed as a recovered unit to match().
    """
    if raw.parser_reference['version'] != 'ck3-lossless-v1.7':
        raise MatcherCompatibilityError('unsupported native recovery API')
    bounds = lambda span: [span.start, span.end]
    def region(message):
        return dict(text=message.text, pieces=[(p.kind, p.text) for p in message.pieces],
                    provenance=dict(span=bounds(message.span)))
    for recovery in raw.iter_recoveries():
        emission = recovery.parent
        provenance = dict(source_tag=emission.source_tag,
            emission_ordinals=[e.ordinal for e in recovery.parents],
            ordered_spans=[bounds(s) for s in recovery.ordered_spans],
            recovery_limitation=recovery.reason)
        if recovery.status != 'recovered':
            yield dict(recovery_status='unresolved', provenance=provenance, recovery=recovery)
            continue
        contexts = {}
        if recovery.structure == 'located-message-wrapper':
            ranges = {'prefix': (emission.body_span.start, recovery.messages[0].span.start),
                      'suffix': (recovery.messages[-1].span.end, emission.body_span.end)}
            contexts = {name: region(emission.select_messages((span,))[0])
                        for name, span in ranges.items()}
        for message in recovery.messages:
            entries = []
            for entry in message.continuations:
                component = region(entry.message)
                component.update({name: [getattr(entry, name).start - entry.message.span.start,
                                        getattr(entry, name).end - entry.message.span.start]
                                  for name in ('prefix_span', 'label_span', 'value_span')})
                entries.append(component)
            yield dict(parser=raw.parser_reference, recovery_status='recovered',
                source_family=emission.source_family, source_tag=emission.source_tag,
                context_kind='continuation:' + recovery.structure if entries else
                    'located-message-wrapper' if contexts else 'body',
                body=region(message), contexts=contexts, continuations=entries,
                provenance={**provenance, 'message_ordinal': message.ordinal})
