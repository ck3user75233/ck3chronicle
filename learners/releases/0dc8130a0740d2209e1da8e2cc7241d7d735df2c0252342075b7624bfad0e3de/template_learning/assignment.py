"""Standalone, model-backed choice among complete native assignments.

No parsing, template inference, mutable owner rules or third-party imports.
Consumers supply every eligible complete body/wrapper assignment, not prefixes.
This file is copied and hashed with the model for independent consumers.
"""
import json

POLICY_VERSION = 'complete-assignment-v2'


def canonical_captures(captures):
    return tuple((c['name'], c['type'], tuple(c['span']) if c['span'] is not None
                  else (-1, -1), c['value'] or '') for c in captures)


def evidence_rank(template, policy):
    evidence = template['selection_evidence']
    directions={'min':1,'max':-1}
    return tuple(directions[metric['direction']]*evidence[metric['field']]
                 for metric in policy['metrics'])


def complete_witnesses(assessment):
    witnesses = assessment['witnesses']
    if assessment['count'] != len(witnesses) or not witnesses:
        raise ValueError('selection requires all complete capture assignments')
    return witnesses


def select_assignment(model, candidates):
    """Return one assignment, or None only when no complete candidate exists.

    candidates: template_id, body {count,witnesses}, contexts mapping region name
    to [{template_id,count,witnesses}]. Values/ranges are never repaired here.
    Canonical span order breaks remaining capture ties; it is not a quality claim.
    """
    policy = model['assignment_policy']
    if policy['version'] != POLICY_VERSION:
        raise ValueError('unsupported assignment policy')
    templates = {t['template_id']: t for t in model['templates']}
    ranked = []
    for candidate in candidates:
        template = templates[candidate['template_id']]
        body = complete_witnesses(candidate['body'])
        capture = min(body, key=canonical_captures)
        component_witnesses = candidate['component_witnesses']
        if len(component_witnesses) != len(body):
            raise ValueError('component witnesses must correspond to every complete opening assignment')
        components = component_witnesses[body.index(capture)]
        contexts, wrapper_ranks, count, wrapper_tie = {}, [], len(body), False
        for name, alternatives in sorted(candidate['contexts'].items()):
            patterns = {p['template_id']: p for p in template['context_patterns'][name]}
            choices = []
            for alternative in alternatives:
                pattern = patterns[alternative['template_id']]
                witnesses = complete_witnesses(alternative)
                selected = min(witnesses, key=canonical_captures)
                choices.append((evidence_rank(pattern,policy), pattern['template_id'],
                                canonical_captures(selected), selected, len(witnesses)))
            if not choices:
                raise ValueError('incomplete wrapper assignment')
            choices.sort(key=lambda c: c[:3])
            chosen = choices[0]
            wrapper_tie |= sum(c[0] == chosen[0] for c in choices) > 1 or chosen[4] > 1
            count *= sum(c[4] for c in choices)
            contexts[name] = dict(template_id=chosen[1], captures=chosen[3])
            wrapper_ranks.append(chosen[0])
        own = evidence_rank(template,policy)
        rank = tuple(own[i] + (sum(r[i] for r in wrapper_ranks) if metric['include_wrappers'] else 0)
                     for i,metric in enumerate(policy['metrics']))
        canonical = (template['template_id'], canonical_captures(capture),
                     json.dumps(contexts, sort_keys=True, ensure_ascii=True))
        ranked.append(dict(rank=rank, canonical=canonical, template=template,
                           captures=capture, contexts=contexts, components=components, count=count,
                           capture_tie=len(body) > 1 or wrapper_tie))
    if not ranked:
        return None
    ranked.sort(key=lambda r: (r['rank'], r['canonical']))
    chosen = ranked[0]
    tied = sum(r['rank'] == chosen['rank'] for r in ranked) > 1
    provisional = (chosen['template']['status'] not in {'supported', 'confirmed'}
                   or tied or chosen['capture_tie'])
    return dict(template_id=chosen['template']['template_id'],
                template_status=chosen['template']['status'],
                match_status='provisional' if provisional else 'template',
                captures=chosen['captures'], context_matches=chosen['contexts'],
                component_matches=chosen['components'],
                selection=dict(policy_version=POLICY_VERSION,
                    reason='deterministic_tie_break' if tied or chosen['capture_tie'] else
                           'evidence_rank' if len(ranked)>1 else 'only_complete_candidate',
                    rank=list(chosen['rank']), template_tie=tied,
                    capture_tie=chosen['capture_tie'], competing_templates=len(ranked),
                    complete_assignments=sum(r['count'] for r in ranked),
                    alternatives=[dict(template_id=r['template']['template_id'], rank=list(r['rank']))
                                  for r in ranked]))
