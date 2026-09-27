"""Complete native v3 matching with all candidate/capture alternatives retained."""
from __future__ import annotations

from functools import lru_cache

from .bindings import bind_captures
from .domain import (ByteSpan, CandidateMatch, Capture, NativeClassification,
                     NativeDiagnostic, RegionMatch, UnresolvedEmission)
from .matching import DeclarationBoundaryError, Rules
from .model import EmpiricalModel, ModelCompatibilityError
from .raw_input import iter_diagnostics

CLASSIFIER_REVISION = 'ck3-native-message-classifier-v7'


class Classifier:
    def __init__(self, model: EmpiricalModel):
        self._model = model
        self._rules = Rules(model.data['owner_rules'])
        # Cache only relative matching results, never occurrence spans or originals.
        self._match = lru_cache(maxsize=4096)(self._match_content)

    @property
    def model(self) -> EmpiricalModel:
        return self._model

    def read_log(self, path):
        return self.model.parser.parse_file(path)

    def _check_parser(self, raw):
        actual = raw.parser_reference
        selected = self.model.parser.reference
        if actual.get('version') != selected.version or actual.get('sha256') != selected.sha256:
            raise ModelCompatibilityError('raw input does not use the model-pinned parser')

    def classify_raw(self, raw):
        """Yield every recovered occurrence or explicit unresolved parent evidence."""
        self._check_parser(raw)
        for diagnostic in iter_diagnostics(raw):
            yield diagnostic if isinstance(diagnostic, UnresolvedEmission) else self.classify(diagnostic)

    def _match_content(self, source, kind, text, pieces, contexts):
        try:
            structure = self._rules.structure(source, text, pieces)
            context_structures = {
                name: self._rules.structure(source, native, parts)[1]
                for name, native, parts in contexts}
            candidates = []
            for template in self.model.templates_by_source.get(source, ()):
                if (template['status'] == 'unresolved' or template['context_kind'] != kind
                        or (template['construction_id'], template['parameter_structures']) != structure):
                    continue
                assessment = self._rules.analyze(template['parts'], text, pieces=pieces)
                if not assessment['count']:
                    continue
                wrapper = []
                for name, native, parts in contexts:
                    alternatives = []
                    for pattern in template['context_patterns'][name]:
                        if (pattern['status'] == 'unresolved' or
                                pattern['parameter_structures'] != context_structures[name]):
                            continue
                        result = self._rules.analyze(pattern['parts'], native, pieces=parts)
                        if result['count']:
                            alternatives.append((pattern['template_id'], result))
                    if not alternatives:
                        break
                    wrapper.append((name, tuple(alternatives)))
                else:
                    candidates.append((template['template_id'], template['status'], assessment, tuple(wrapper)))
            return tuple(candidates), None
        except DeclarationBoundaryError as exc:
            # Known native empty-reason defect belongs to the model declaration.
            # Keep the whole message for review; never change the parser or slots.
            return (), str(exc)

    @staticmethod
    def _bind(diagnostic, region, name, template_id, assessment):
        witnesses = []
        for witness in assessment['witnesses']:
            captures = tuple(Capture(c['name'], c['type'], c['value'],
                                     ByteSpan(*c['span']) if c['span'] is not None else None)
                             for c in witness)
            witnesses.append(bind_captures(diagnostic.original, region, captures,
                                          template_id=template_id, region_name=name))
        return RegionMatch(template_id, name, assessment['count'], tuple(witnesses))

    def classify(self, diagnostic: NativeDiagnostic) -> NativeClassification:
        self._check_parser(diagnostic.original)
        expected = ('prefix', 'suffix') if diagnostic.context_kind == 'located-message-wrapper' else ()
        if (diagnostic.context_kind not in {'body', 'located-message-wrapper'} and
                not diagnostic.context_kind.startswith('continuation:')) or tuple(
                name for name, _ in diagnostic.contexts) != expected:
            raise ValueError('diagnostic requires its complete native wrapper context')
        content = tuple((name, region.text, region.pieces) for name, region in diagnostic.contexts)
        assessments, issue = self._match(diagnostic.source_family, diagnostic.context_kind,
                                        diagnostic.body.text, diagnostic.body.pieces, content)
        regions = dict(diagnostic.contexts)
        entries = [dict(text=e.body.text,pieces=e.body.pieces,
            **{name:[getattr(e,name).start-e.body.span.start,getattr(e,name).end-e.body.span.start]
               for name in ('prefix_span','label_span','value_span')}) for e in diagnostic.continuations]
        templates = {t['template_id']:t for t in self.model.templates_by_source.get(diagnostic.source_family,())}
        eligible, candidates = [], []
        for template_id,status,assessment,contexts in assessments:
            template = templates[template_id]
            kept, components = [], []
            for witness in assessment['witnesses']:
                matched = self.model.match_components(template['continuation'],entries,witness)
                if matched is not None:
                    kept.append(witness);components.append(matched)
            if not kept:
                continue
            body = dict(count=len(kept),witnesses=kept)
            eligible.append(dict(template_id=template_id,body=body,component_witnesses=components,
                contexts={name:[dict(template_id=identity,**value) for identity,value in alternatives]
                          for name,alternatives in contexts}))
            # Entry captures are fixed by native component ranges. Every retained
            # opening witness has already validated the same reference value.
            if any(value != components[0] for value in components[1:]):
                raise ValueError('native component ranges disagree across opening witnesses')
            candidates.append(CandidateMatch(template_id,status,
                self._bind(diagnostic,diagnostic.body,'message',template_id,body),
                tuple((name,tuple(self._bind(diagnostic,regions[name],name,identity,value)
                      for identity,value in alternatives)) for name,alternatives in contexts),
                tuple(self._bind(diagnostic,diagnostic.continuations[c['index']].body,
                      'continuation:'+str(c['index']),template_id,dict(count=1,witnesses=[c['captures']]))
                      for c in components[0])))
        chosen = self.model.select_assignment(self.model.data,eligible)
        selected = None
        if chosen:
            one = lambda captures: dict(count=1,witnesses=[captures])
            selected = CandidateMatch(chosen['template_id'],chosen['template_status'],
                self._bind(diagnostic,diagnostic.body,'message',chosen['template_id'],one(chosen['captures'])),
                tuple((name,(self._bind(diagnostic,regions[name],name,value['template_id'],one(value['captures'])),))
                      for name,value in chosen['context_matches'].items()),
                tuple(self._bind(diagnostic,diagnostic.continuations[c['index']].body,
                      'continuation:'+str(c['index']),chosen['template_id'],one(c['captures']))
                      for c in chosen['component_matches']))
        outcome = 'full' if chosen and chosen['match_status']=='template' else 'provisional' if chosen else 'unknown'
        reasons = () if outcome != 'provisional' else (chosen['selection']['reason'],)
        if diagnostic.continuations and not chosen and issue is None:
            issue = diagnostic.recovery_limitation or 'no complete opening-and-components template matched'
        return NativeClassification(diagnostic, self.model.revision_id, CLASSIFIER_REVISION,
                                    outcome, tuple(candidates), tuple(reasons), issue,
                                    selected=selected,selection=chosen['selection'] if chosen else None)
