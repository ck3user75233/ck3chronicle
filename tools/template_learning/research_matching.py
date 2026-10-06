"""Inspect complete source-specific native diagnostic candidates."""
from collections import Counter
from dataclasses import replace
from template_learning.native_matching import Matcher


def research_matcher(model):
    """The matcher needs executable definitions, not a copy of research history."""
    from template_learning.publish_native_model import compact_template
    data = {k: v for k, v in model.items() if k not in {
        'refinement_history', 'template_retirement', 'region_discovery',
        'evidence', 'excluded_evidence', 'duplicates', 'learning_update'}}
    data['templates'] = [compact_template(t) for t in model['templates']]
    return Matcher(data)


def evaluate_records(model, grouped, stats):
    from template_learning.learner_loader import require_candidate
    require_candidate(model)
    matcher = research_matcher(model)
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
            construction = matcher.rules.recognize(source,record.text)
            matches, capture_ambiguities, selected = matcher.inspect_record(record)
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
