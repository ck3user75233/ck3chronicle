"""Inspect complete source-specific native diagnostic candidates."""
from collections import Counter, defaultdict
from dataclasses import replace
from template_learning.patterns import match_pattern, analyze_match_pattern, parameter_piece_ranges
from template_learning.constructions import recognize
from template_learning.assignment import select_assignment
from template_learning.continuations import match_components


def match_record(template, record, *, capture_ambiguities=None):
    if template["status"] == "unresolved" or template["source_family"] != record.source_family:
        return None
    if template["context_kind"] != record.context_kind:
        return None
    construction=recognize(record.source_family,record.text)
    if template['construction_id'] != (construction['id'] if construction else None):
        return None
    structures=[v[1] for _,v in sorted(parameter_piece_ranges(record.pieces,record.source_family).items())]
    if template['parameter_structures']!=structures:
        return None
    assessment = analyze_match_pattern(template["parts"],record.text,pieces=record.pieces,witness_limit=None)
    captures = assessment['captures']
    if not assessment['count']:
        return None
    component_witnesses = []
    kept = []
    for witness in assessment['witnesses']:
        components = match_components(template.get('continuation'),record.continuations,witness)
        if components is not None:
            kept.append(witness)
            component_witnesses.append(components)
    if not kept:
        return None
    assessment = dict(count=len(kept),witnesses=kept,captures=kept[0] if len(kept)==1 else None)
    captures = assessment['captures']
    contexts = {}
    ambiguous=assessment['count']>1
    for context_id,context in record.contexts.items():
        regions = {}
        for name in ("prefix","suffix"):
            possible = []
            for pattern in template["context_patterns"].get(name,[]):
                if pattern['status']=='unresolved':
                    continue
                structures=[v[1] for _,v in sorted(parameter_piece_ranges(tuple(map(tuple,context[name]['pieces'])),record.source_family).items())]
                if pattern['parameter_structures']!=structures:
                    continue
                result=analyze_match_pattern(pattern["parts"],context[name]["text"],pieces=context[name]["pieces"],witness_limit=None)
                if result['count']:
                    possible.append(dict(template_id=pattern["template_id"],captures=result['captures'],
                        capture_count=result['count'],capture_witnesses=result['witnesses']))
            ambiguous=ambiguous or len(possible)>1 or any(p['capture_count']>1 for p in possible)
            regions[name] = possible
        if not all(regions.values()):
            return None
        contexts[context_id] = regions
    if ambiguous:
        if capture_ambiguities is not None:
            capture_ambiguities.append(dict(template_id=template['template_id'],context_matches=contexts,
                component_witnesses=component_witnesses,**assessment))
        return None
    return dict(template_id=template["template_id"],captures=captures,context_matches=contexts,
                template_status=template['status'],component_witnesses=component_witnesses)


def assignment_candidates(matches, ambiguities):
    """Adapt existing complete matcher results to the standalone selector."""
    result=[]
    for match in [*matches,*ambiguities]:
        contexts=list(match['context_matches'].values())
        if len(contexts)>1:
            raise ValueError('select one contextual diagnostic at a time')
        wrappers={name:[dict(template_id=p['template_id'],count=p['capture_count'],
                             witnesses=p['capture_witnesses']) for p in patterns]
                  for name,patterns in (contexts[0] if contexts else {}).items()}
        result.append(dict(template_id=match['template_id'],
            body=dict(count=match.get('count',1),witnesses=match.get('witnesses',[match.get('captures')])),
            component_witnesses=match['component_witnesses'],
            contexts=wrappers))
    return result


def evaluate_records(model, grouped, stats):
    by_source = defaultdict(list)
    for template in model["templates"]:
        by_source[template["source_family"]].append(template)
    rows,counts = [],Counter({name:0 for name in ("full","provisional","unknown")})
    for source,records in grouped.items():
        contextual_records = []
        for record in records:
            if not record.contexts:
                contextual_records.append(record)
            else:
                for context_id,context in record.contexts.items():
                    contextual_records.append(replace(record,contexts={context_id:context},
                        native_occurrences=[o for o in record.native_occurrences if o["context_id"]==context_id]))
        for record in contextual_records:
            construction = recognize(source,record.text)
            capture_ambiguities=[]
            matches = [m for t in by_source[source] if (m := match_record(t,record,capture_ambiguities=capture_ambiguities)) is not None]
            selected=select_assignment(model,assignment_candidates(matches,capture_ambiguities))
            outcome = 'full' if selected and selected['match_status']=='template' else 'provisional' if selected else 'unknown'
            reasons=[]
            if any(m['template_status']=='provisional' for m in matches):reasons.append('insufficient_distinct_learning_examples')
            if len(matches)>1:reasons.append('competing_templates')
            if capture_ambiguities:reasons.append('ambiguous_capture_boundaries')
            counts[outcome] += record.occurrences
            rows.append(dict(source_family=source,native=record.text,pieces=record.pieces,contexts=record.contexts,
                context_kind=record.context_kind,continuations=record.continuations,
                native_occurrences=record.native_occurrences,outcome=outcome,matches=matches,capture_ambiguities=capture_ambiguities,
                provisional_reasons=reasons, selected_assignment=selected,
                construction=construction,status="research_only",
                unmatched_complete_message=outcome == "unknown"))
    unresolved = [dict(evidence_sha256=sha,**r) for sha,s in stats.items() for r in s["unresolved_emissions"]]
    return dict(counts=dict(counts),recovered_messages=sum(counts.values()),
        unresolved_emissions=len(unresolved),status="candidate_structural_inspection_not_production_acceptance"),rows,unresolved
