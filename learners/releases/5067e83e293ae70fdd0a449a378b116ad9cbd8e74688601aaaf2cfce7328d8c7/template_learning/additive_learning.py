"""Same-implementation continuation of one cumulative native candidate.

Supported definitions remain available. Only evidence without a unique complete
supported assignment, and the members of provisional/unresolved definitions,
returns to discovery. The ordinary matcher, inference and retirement rules own
those decisions; this module supplies their evidence pools, not a second matcher.
"""
from copy import deepcopy
from dataclasses import replace
from types import SimpleNamespace

from template_learning.records import identity
from template_learning.matching_primitives import pattern_identity
from template_learning.matching_defaults import match_pattern
from template_learning.diagnostic_wording import reject_wording_loss
from template_learning.clustering import erased_supported_wording

STRATEGY_VERSION = 'same-version-additive-v1'


def contextual_records(record):
    if not record.contexts:
        return [record]
    return [replace(record, contexts={key: value})
            for key, value in record.contexts.items()]


def settled_assignment(matcher, record):
    """Every native wrapper must have exactly one complete supported witness."""
    selected_ids = set()
    for contextual in contextual_records(record):
        _, _, chosen = matcher.inspect_record(contextual)
        if (chosen is None or chosen['match_status'] != 'template'
                or chosen['selection']['complete_assignments'] != 1):
            return None
        selected_ids.add(chosen['template_id'])
    return next(iter(selected_ids)) if len(selected_ids) == 1 else None


def contract(template):
    return dict(parts=pattern_identity(template['parts']),
        context_patterns={name: sorted((dict(parts=pattern_identity(p['parts']),
            parameter_structures=p['parameter_structures']) for p in patterns), key=identity)
            for name, patterns in template['context_patterns'].items()},
        continuation=template['continuation'],
        construction_id=template['construction_id'],
        parameter_structures=template['parameter_structures'],
        context_kind=template['context_kind'], source_family=template['source_family'])


def cluster_view(template, members):
    native = [members[key] for key in template['evidence_record_ids']]
    return SimpleNamespace(source_family=template['source_family'],
        template_id=template['template_id'], parts=template['parts'],
        records=native, medoid=native[0], failures=template['unsupported_members'])


def preserve_wording(source, proposals, references, members, threshold, learn_pool, review):
    """Re-infer rejected unions separately across retained native formulations.

    Provisional status does not erase an established literal assignment. The
    ordinary loss checker decides whether a union is invalid; complete body
    matches to those earlier definitions partition its original members. No
    spelling is promoted from a slot or prescribed as initial literal wording.
    """
    accepted, rejected = [], []
    pending = list(proposals)
    while pending:
        template = pending.pop(0)
        candidate = cluster_view(template, members)
        peers = [peer for peer in references if peer.template_id != candidate.template_id]
        events = []
        lost = reject_wording_loss(peers, candidate, path='additive_learning', review=events)
        erased = [loss for peer in peers for loss in erased_supported_wording(peer, template['parts'])]
        review.extend(events)
        if not lost and not erased:
            accepted.append(template)
            continue
        rejected.append(template['template_id'])
        # Each group retains complete native records, including continuations
        # and wrappers. Strictly smaller groups bound repeated refinement.
        groups = {}
        for record in candidate.records:
            signature = tuple(peer.template_id for peer in peers if not peer.failures
                and match_pattern(peer.parts, record.text, pieces=record.pieces) is not None)
            groups.setdefault(signature, []).append(record)
        review.append(dict(source=source, decision='rejected',
            reason='new proposal erases retained diagnostic wording, including provisional literals',
            proposed_template=template, preserved_wording=erased,
            refinement_groups=[dict(previous_template_ids=list(key),
                record_ids=[identity(r.key) for r in rows]) for key, rows in groups.items()]))
        if len(groups) > 1:
            for rows in groups.values():
                pending.extend(learn_pool(source, rows, threshold, review))
    return accepted, rejected


def learn_source(source, records, previous, matcher, threshold, learn_pool, review):
    """Keep settled work; use cumulative open evidence for supported refinement."""
    members = {identity(record.key): record for record in records}
    retained = {t['template_id']: deepcopy(t) for t in previous}
    if any(key not in members for t in previous for key in t['evidence_record_ids']):
        raise ValueError('additive learning requires the previous complete native evidence')
    open_ids = {key for t in previous if t['status'] not in {'supported', 'confirmed'}
                for key in t['evidence_record_ids']}
    for key, record in members.items():
        chosen = settled_assignment(matcher, record)
        if chosen is None:
            open_ids.add(key)
    # Occurrence growth updates bookkeeping, not diagnostic diversity or rules.
    for template in retained.values():
        template['support_occurrences'] = sum(members[key].occurrences
            for key in template['evidence_record_ids'])
    reopened = set()
    proposed = []
    while open_ids:
        pool = [record for key, record in members.items() if key in open_ids]
        proposed = learn_pool(source, pool, threshold, review)
        # Body IDs predate wrapper inference. A new wrapper can therefore share
        # an ID without sharing the complete contract. Reconsider its old native
        # members together; never overwrite a retained layout with a new one.
        collisions = [retained[t['template_id']] for t in proposed
            if t['template_id'] in retained
            and retained[t['template_id']]['status'] in {'supported', 'confirmed'}
            and contract(t) != contract(retained[t['template_id']])]
        additions = {key for t in collisions for key in t['evidence_record_ids']} - open_ids
        if not additions:
            break
        reopened.update(t['template_id'] for t in collisions)
        open_ids.update(additions)
    references = [cluster_view(t, members) for t in previous
                  if t['status'] in {'supported', 'confirmed', 'provisional'}]
    proposed, rejected = preserve_wording(source, proposed, references, members,
                                          threshold, learn_pool, review)
    for template in proposed:
        prior = retained.get(template['template_id'])
        if prior:
            if template['status'] == 'unresolved' and prior['status'] != 'unresolved':
                review.append(dict(source=source, decision='rejected',
                    reason='an unresolved proposal cannot replace a retained complete definition',
                    proposed_template=template, previous_template_id=prior['template_id']))
                rejected.append(template['template_id'])
                continue
            if prior['status'] in {'supported', 'confirmed'} and contract(prior) == contract(template):
                continue
            if contract(prior) != contract(template) and any(matcher.rules.match_record(template, record) is None
                   for key in prior['evidence_record_ids']
                   for record in contextual_records(members[key])):
                review.append(dict(source=source, decision='rejected',
                    reason='changed complete contract does not preserve retained native members',
                    proposed_template=template, previous_template_id=prior['template_id']))
                rejected.append(template['template_id'])
                continue
        retained[template['template_id']] = template
    kept_ids = {t['template_id'] for t in previous if t['status'] in {'supported', 'confirmed'}}
    summary = dict(source=source, distinct_records=len(records),
        settled_records=len(members)-len(open_ids), discovery_records=len(open_ids),
        settled_occurrences=sum(record.occurrences for key,record in members.items() if key not in open_ids),
        discovery_occurrences=sum(record.occurrences for key,record in members.items() if key in open_ids),
        retained_supported_templates=len(kept_ids), reopened_templates=sorted(reopened),
        rejected_proposals=rejected)
    return list(retained.values()), kept_ids, summary


def lifecycle(previous, current, retirements):
    old = {t['template_id']: t for t in previous}
    new = {t['template_id']: t for t in current}
    retired = {r['retired_template_id']: r for r in retirements}
    changes = []
    for key, template in old.items():
        if key not in new:
            if key not in retired:
                raise ValueError('retained template disappeared without a retirement decision')
            changes.append(dict(action='retired', template_id=key,
                successor=retired[key]['selected_template_id'], reason=retired[key]['reason']))
        elif template['status'] != new[key]['status']:
            changes.append(dict(action='status_changed', template_id=key,
                previous_status=template['status'], status=new[key]['status'],
                learning_support=new[key]['learning_support']))
        elif contract(template) != contract(new[key]):
            changes.append(dict(action='complete_contract_extended', template_id=key))
    changes.extend(dict(action='discovered', template_id=key, status=t['status'])
                   for key,t in new.items() if key not in old)
    return changes
