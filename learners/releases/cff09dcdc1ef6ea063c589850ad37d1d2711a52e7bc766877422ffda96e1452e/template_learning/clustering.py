"""Source-partitioned ordered alignment, independent of repetition counts."""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
import difflib
from functools import lru_cache
from template_learning.records import SequenceRecord, identity
from template_learning.patterns import derive_pattern, inference_units, literal_anchor_signature, UnsupportedField, field_structure, location_label_forms
from template_learning.matching_defaults import match_pattern, parameter_piece_ranges
from template_learning.matching_primitives import pattern_identity, punctuation_piece
from template_learning import constructions, regions, parameter_structures
from template_learning.owner_rules import INFERENCE_POLICY
from template_learning.literal_guidance import guided_piece_indices
from template_learning.diagnostic_wording import reject_wording_loss

CLUSTERER_VERSION = "outer-diagnostic-consensus-v45"


@lru_cache(maxsize=32768)
def sequence_similarity(left,right):
    if not left or not right:
        return float(left == right)
    matched = sum(b.size for b in difflib.SequenceMatcher(None,left,right,autojunk=False).get_matching_blocks())
    shortest,longest = sorted((len(left),len(right)))
    return .55*matched/longest + .35*matched/shortest + .10*shortest/longest


def learning_tokens(record, parts=None):
    # Initial discovery compares the outside of probable balanced regions.
    # An accepted field contributes one typed position, never its value words.
    # Probable regions have not established a field and receive no such credit.
    if parts is None and hasattr(record,'_comparison_tokens'):
        return record._comparison_tokens
    excluded = []
    fields = []
    if parts is not None:
        captures = match_pattern(parts, record.text, pieces=record.pieces)
        if captures is None:
            raise ValueError("only supported captures can affect similarity")
        excluded = [c["span"] for c in captures if c["span"] is not None]
        fields = [(c['span'][0], 0, ('field', c['type'])) for c in captures
                  if c['span'] is not None]
    offsets, cursor = [0], 0
    for _, text in record.pieces:
        cursor += len(text.encode("utf-8", "surrogateescape"))
        offsets.append(cursor)
    keys, spans = inference_units(record,region_first=parts is None)
    diagnostic=constructions.comparison_ranges(record.source_family,record.text)
    units = list(fields)
    for key, (a, b) in zip(keys, spans):
        if any(x <= offsets[a] and offsets[b] <= y for x, y in excluded):
            continue
        if key[0] == 'location-label':
            units.append((offsets[a], 1, key))
        elif key[0] == 'token' and any(c.isalnum() for c in key[1]):
            if any(x <= offsets[a] and offsets[b] <= y for x, y in diagnostic):
                units.append((offsets[a], 1, key))
        elif parts is None:
            kind = None
            if key[0] == 'declared':
                kind = key[3]
            elif key[0] == 'parameter':
                kind = parameter_structures.BY_ID[key[1]].get('slot_type', 'PARAM')
            elif key[0] == 'location':
                kind = 'LOCATOR'
            elif key[0] == 'date-key':
                kind = 'KEY'
            if kind is not None:
                units.append((offsets[a], 0, ('field', kind)))
    result = tuple(key for _, _, key in sorted(units))
    if parts is None:
        record._comparison_tokens=result
    return result


def grouping_scope(record):
    if hasattr(record,'_grouping_scope'):
        return record._grouping_scope
    construction=constructions.identity(record.source_family,record.text)
    parameters=tuple(v[1] for _,v in sorted(parameter_piece_ranges(record.pieces,record.source_family).items()))
    if construction is None:
        record._grouping_scope=(record.context_kind,None,(),parameters)
        return record._grouping_scope
    ranges=constructions.comparison_ranges(record.source_family,record.text)
    guided=set(guided_piece_indices(record.pieces))
    wording=[];cursor=0
    for i,(kind,text) in enumerate(record.pieces):
        end=cursor+len(text.encode('utf-8','surrogateescape'))
        if i in guided and any(a<=cursor and end<=b for a,b in ranges):
            wording.append((kind,text))
        cursor=end
    record._grouping_scope=(record.context_kind,construction,tuple(wording),parameters)
    return record._grouping_scope


def comparable(left,right,threshold):
    """Short formulations may propose a group; joint field evidence must accept it."""
    if not left or not right:
        return left==right
    if len(left)==len(right)<=INFERENCE_POLICY['short_form_max_tokens']:
        shared=sum(a==b for a,b in zip(left,right))
        return shared>0 and shared/len(left)>=INFERENCE_POLICY['short_form_shared_fraction']
    return sequence_similarity(left,right)>=threshold


def anchors(tokens):
    words = [t for t in tokens if t[0] == "token" and any(c.isalnum() for c in t[1])]
    if len(words)<3:
        return {("word",word) for word in words}
    return set(zip(words,words[1:]))


def _spread(records, limit):
    # Bounded reference selection only; every member participates in alignment.
    if len(records)<=limit:
        return records
    return [records[i*(len(records)-1)//(limit-1)] for i in range(limit)]


def choose_medoid(records):
    ordered = sorted(records,key=lambda r:r.text)
    comparisons = _spread(ordered,100)
    candidates=_spread(ordered,40)
    tokens={id(r):learning_tokens(r) for r in [*comparisons,*candidates]}
    return max(candidates,key=lambda r:sum(sequence_similarity(tokens[id(r)],tokens[id(s)]) for s in comparisons))


@dataclass
class TemplateCluster:
    source_family: str
    context_kind: str
    records: list[SequenceRecord]
    medoid: SequenceRecord
    parts: list[dict] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    refinements: list[dict] = field(default_factory=list)
    hypotheses: list[dict] = field(default_factory=list)

    @property
    def template_id(self):
        structures=tuple(v[1] for _,v in sorted(parameter_piece_ranges(self.medoid.pieces,self.source_family).items()))
        return identity([self.source_family,self.context_kind,structures,pattern_identity(self.parts)])[:24]


def refine_literal_variants(cluster, *, allow_division=True):
    """Similarity proposes a group; it does not establish every differing slot.

    Keep case-only alternatives as distinct literal formulations. Explicit
    supplied wording is already anchored during grouping and alignment.
    """
    # Equivalent location labels share a function, not a variable KEY slot.
    # Expand only observed exact formulations, during inference; later union
    # proposals pass this same guard. No generated-model patch is necessary.
    label_groups = defaultdict(list)
    for record in cluster.records:
        label_groups[location_label_forms(record)].append(record)
    label_scopes = {tuple((ordinal, group) for ordinal, group, _ in forms)
                    for forms in label_groups}
    if len(label_groups) > 1 and len(label_scopes) == 1:
        if not allow_division:
            return []
        return [child for forms, records in label_groups.items()
                for child in refine_literal_variants(TemplateCluster(
                    cluster.source_family, cluster.context_kind, records, records[0],
                    refinements=[*cluster.refinements, dict(
                        reason='declared equivalent location labels retain exact native formulations',
                        retained_labels=forms, previous_members=len(cluster.records), members=len(records))]))]
    cluster.medoid = choose_medoid(cluster.records)
    cluster.hypotheses = []
    try:
        cluster.parts,cluster.failures = derive_pattern(cluster.records,cluster.medoid,hypotheses=cluster.hypotheses)
    except UnsupportedField as exc:
        # Do not coerce the failed position to PARAM. A proposed union may be
        # rejected; an initial group is partitioned and re-inferred completely.
        if not allow_division:
            return []
        groups=defaultdict(list)
        for record in cluster.records:
            a,b=exc.spans[identity(record.key)]
            groups[field_structure(record.pieces[a:b])].append(record)
        basis='raw field structure'
        if len(groups)==1:
            groups=defaultdict(list)
            for record in cluster.records:
                a,b=exc.spans[identity(record.key)]
                groups[''.join(t for _,t in record.pieces[a:b])].append(record)
            basis='literal field spelling; no supported type'
        if len(groups)<2:
            raise ValueError('unsupported field did not partition native evidence') from exc
        return [child for key,records in groups.items()
                for child in refine_literal_variants(TemplateCluster(cluster.source_family,cluster.context_kind,
                    records,records[0],refinements=[*cluster.refinements,dict(
                        reason=str(exc),partition_basis=basis,retained_partition=key,
                        previous_members=len(cluster.records),members=len(records))]))]
    rejected=next((p for p in cluster.parts if p.get('rejection_reason')),None)
    if rejected:
        members={m['record_id']:m for m in rejected['field_support']['members']}
        groups=defaultdict(list)
        for record in cluster.records:
            a,b=members[identity(record.key)]['pieces']
            groups[''.join(t for _,t in record.pieces[a:b])].append(record)
        if len(groups)>1:
            if not allow_division:
                return []
            return [child for value,records in groups.items()
                for child in refine_literal_variants(TemplateCluster(cluster.source_family,cluster.context_kind,
                    records,records[0],refinements=[*cluster.refinements,dict(reason=rejected['rejection_reason'],
                    observed_values=rejected['observed_values'],retained_value=value)]))]
    if cluster.failures:
        failed=set(cluster.failures)
        supported=[r for r in cluster.records if r.text not in failed]
        unsupported=[r for r in cluster.records if r.text in failed]
        if allow_division and supported and unsupported:
            # Re-infer both smaller native pools, not merely the successful
            # captures. Failed evidence is retained and may remain unresolved.
            # Each split reduces pool size, so this cannot recurse indefinitely.
            return [child for records in (supported,unsupported)
                    for child in refine_literal_variants(TemplateCluster(cluster.source_family,cluster.context_kind,
                        records,records[0],refinements=[*cluster.refinements,dict(
                            reason='reconsidered native members after complete capture inconsistency',
                            previous_members=len(cluster.records),members=len(records))]))]
        return [cluster]
    for part in cluster.parts:
        if part["kind"] != "slot" or part['type']=='REASON' or part.get('parameter_definition') or part.get('empirical_region'):
            continue
        values = part["observed_values"]
        reason = None
        if len(values)>1 and len({v.casefold() for v in values}) == 1:
            reason = "case-only variation does not establish a variable slot"
        presence_only = (part["type"] == "PARAM" and part["optional"] and values
                         and all(punctuation_piece("token", value) for value in values))
        if presence_only:
            reason = "optional literal punctuation is not a PARAM boundary"
        insufficient = part["type"] == "PARAM" and part["optional"] and len(values)==1
        if insufficient:
            presence_only = True
            reason = "insufficient PARAM evidence: one nonempty spelling plus absence; retain literal formulations"
        if reason is None:
            continue
        groups = defaultdict(list)
        for record in cluster.records:
            captures = match_pattern(cluster.parts,record.text,pieces=record.pieces)
            capture = next(c for c in captures if c["name"] == part["name"])
            groups[(capture["value"] is not None) if presence_only else capture["value"]].append(record)
        if len(groups)<2:
            raise ValueError("literal refinement must partition distinct native variants")
        if not allow_division:
            return []
        result = []
        for value,records in groups.items():
            child = TemplateCluster(cluster.source_family,cluster.context_kind,records,records[0],
                refinements=[*cluster.refinements,dict(reason=reason,values=values,
                    observed_absence=part["optional"],retained_value=value)])
            result.extend(refine_literal_variants(child))
        return result
    return [cluster]


def refine_supported_wording(cluster, peers, review=None):
    """Separate an erased interior phrase when independent groups retain it.

    Every native member must select exactly one observed phrase. No sentence
    dictionary, partial-message learning, or best-match suppression is used.
    """
    if cluster.failures:
        return [cluster]
    for index,part in enumerate(cluster.parts):
        if (part["kind"] != "literal" or 'alternatives' in part or index == 0 or index == len(cluster.parts)-1
                or cluster.parts[index-1]["kind"] != "slot"
                or cluster.parts[index-1]["optional"]
                or not any(c.isalpha() for c in part["text"])):
            continue
        prefix = pattern_identity(cluster.parts[:index])
        cues = set()
        for peer in peers:
            if (peer is cluster or peer.failures or len(peer.records)<2
                    or peer.context_kind != cluster.context_kind or len(peer.parts)<=index
                    or pattern_identity(peer.parts[:index]) != prefix):
                continue
            other = peer.parts[index]
            if (other["kind"] == "literal" and other["text"].startswith(part["text"])
                    and any(c.isalpha() for c in other["text"][len(part["text"]):])):
                cues.add(other["text"])
        # Nested cues are not independent alternatives.
        cues = {cue for cue in cues if not any(cue != shorter and cue.startswith(shorter) for shorter in cues)}
        if len(cues)<2:
            continue
        groups = defaultdict(list)
        for record in cluster.records:
            captures = match_pattern(cluster.parts,record.text,pieces=record.pieces)
            preceding = next(c for c in captures if c["name"] == cluster.parts[index-1]["name"])
            position = preceding["span"][1] + len(cluster.parts[index-1]["suffix"].encode("utf-8","surrogateescape"))
            tail = record.text.encode("utf-8","surrogateescape")[position:].decode("utf-8","surrogateescape")
            matches = [cue for cue in cues if tail.startswith(cue)]
            if len(matches)!=1:
                break
            groups[matches[0]].append(record)
        else:
            if len(groups)>=2:
                result = []
                for cue,records in sorted(groups.items()):
                    child = TemplateCluster(cluster.source_family,cluster.context_kind,records,records[0],
                        refinements=[*cluster.refinements,dict(
                            reason="independent native groups retain distinct interior wording",
                            retained_literal=cue, alternatives=sorted(groups))])
                    result.extend(refine_literal_variants(child))
                if any(reject_wording_loss([cluster],child,path='refine_supported_wording',review=review)
                       for child in result if not child.failures):
                    return [cluster]
                return result
    return [cluster]


def wording_shape(parts):
    """Compare fixed wording, ignoring only whitespace beside text fields.

    This is an inference grouping key, never a transformed native message.
    Typed numeric/location fields and internal literal spacing stay exact.
    """
    text_types = {"KEY", "OPTIONAL_KEY", "PARAM"}
    result = []
    for index,part in enumerate(parts):
        if part["kind"] == "literal":
            if 'alternatives' in part:
                result.append(('literal-choice', part['location_label'], tuple(part['alternatives'])))
                continue
            text = part["text"]
            if index and parts[index-1].get("type") in text_types:
                text = text.lstrip()
            if index+1<len(parts) and parts[index+1].get("type") in text_types:
                text = text.rstrip()
            if text:
                result.append(("literal",text))
        elif part["type"] in text_types:
            result.append(("text-field",))
        else:
            result.append(("typed-field",identity(pattern_identity([part]))))
    return tuple(result)


def consolidate_same_wording(clusters, review=None):
    groups = defaultdict(list)
    for cluster in clusters:
        key = (grouping_scope(cluster.medoid),wording_shape(cluster.parts))
        groups[key].append(cluster)
    result = []
    for key,peers in groups.items():
        if len(peers)==1 or any(p.failures for p in peers):
            result.extend(peers)
            continue
        records = [r for p in peers for r in p.records]
        refinements = [r for p in peers for r in p.refinements]
        child = TemplateCluster(peers[0].source_family,peers[0].context_kind,records,records[0],
            refinements=[*refinements,dict(
                reason="joint native evidence retains the same fixed wording",
                previous_candidates=len(peers))])
        revised = refine_literal_variants(child)
        if any(p.failures or wording_shape(p.parts)!=key[1] for p in revised) or any(
                reject_wording_loss(peers, p, path='consolidate_same_wording', review=review) for p in revised):
            result.extend(peers)
        else:
            result.extend(revised)
    return result


def erased_supported_wording(cluster, proposed):
    """Independent variable examples can establish a phrase as literal wording.

    Inspect existing raw alphabetic word runs, not a sentence vocabulary or a
    new lexer. Opaque identifiers and singleton observations do not supply this
    phrase evidence. Return the evidence when a proposed PARAM would erase it.
    """
    if len(cluster.records)<2 or not any(p['kind']=='slot' and p['type']!='LOCATOR'
            and len(p['observed_values'])>1 for p in cluster.parts):
        return []
    old = match_pattern(cluster.parts,cluster.medoid.text,pieces=cluster.medoid.pieces)
    new = match_pattern(proposed,cluster.medoid.text,pieces=cluster.medoid.pieces)
    if old is None or new is None:
        return []
    variables=[c['span'] for c in old if c['span'] is not None]
    fields={p['name']:p for p in proposed if p['kind']=='slot'}
    parameters=[c['span'] for c in new if c['type']=='PARAM' and c['span'] is not None
                and not fields[c['name']].get('field_support',{}).get('assessment',{}).get('paired_boundaries')]
    runs, words, cursor = [], [], 0
    for kind,text in cluster.medoid.pieces:
        end=cursor+len(text.encode('utf-8','surrogateescape'))
        literal=not any(a<end and cursor<b for a,b in variables)
        if kind=='token' and text.isalpha() and literal:
            words.append((text,cursor,end))
        elif not (kind=='gap' and literal and '\n' not in text and '\r' not in text):
            if len(words)>=2:
                runs.append(words)
            words=[]
        cursor=end
    if len(words)>=2:
        runs.append(words)
    return [dict(phrase=cluster.medoid.text.encode('utf-8','surrogateescape')[run[0][1]:run[-1][2]].decode('utf-8','surrogateescape'),
                 independent_variants=len(cluster.records),
                 erased_words=[text for text,a,b in run if any(x<=a and b<=y for x,y in parameters)])
            for run in runs if any(x<=a and b<=y for _,a,b in run for x,y in parameters)]


def refine_region_groups(clusters, threshold, review):
    """Investigate joint evidence, then compare wording outside accepted fields.

    No text is excluded to create the hypothesis that is supposed to justify
    exclusion. Each accepted union redoes inference on all members. Only disjoint
    original groups can merge in this sweep; new groups are never reopened.
    """
    seen = set()
    identities={}
    wording={}
    comparison_tokens={}
    memberships={}
    def cached(cluster):
        key=id(cluster)
        if key not in identities:
            # Keep the object alive while its identity keys these local caches.
            identities[key]=(cluster,cluster.template_id)
            memberships[key]=identity(sorted(r.key for r in cluster.records))
            comparison_tokens[key]=learning_tokens(cluster.medoid,cluster.parts)
            wording[key]=frozenset(value for _,value in comparison_tokens[key])
        return identities[key][1]
    def concise(hypotheses):
        # Event.records names every native member. Exact field spans remain on
        # the accepted candidate; failed proposals need no duplicate span tables.
        return [{k:v for k,v in h.items() if k!='members'} for h in hypotheses]
    iteration = 1
    active = {id(c) for c in clusters}
    ordered = sorted(clusters,key=lambda c:(-len(c.records),cached(c)))
    # Bound discovery work, not member coverage. Rank by the full candidate's
    # retained wording (once per word), avoiding punctuation/count vetoes.
    word_sets=wording
    for i,left in enumerate(ordered):
        if id(left) not in active:
            continue
        changed = False
        possible=[right for right in ordered[i+1:] if id(right) in active and grouping_scope(left.medoid)==grouping_scope(right.medoid)]
        words=word_sets[id(left)]
        possible.sort(key=lambda right:(-len(words & word_sets[id(right)])/max(1,len(words | word_sets[id(right)])),cached(right)))
        limit=INFERENCE_POLICY['region_proposal_neighbors']
        for right in possible[:limit]:
            if grouping_scope(left.medoid) != grouping_scope(right.medoid):
                continue
            key = tuple(sorted((memberships[id(left)],memberships[id(right)])))
            if key in seen:
                continue
            seen.add(key)
            if len(seen)%100==0:
                print(f"Regrouping {left.source_family}: {len(ordered)} groups, {len(seen)} considered pairs",flush=True)
            if not (anchors(comparison_tokens[id(left)]) & anchors(comparison_tokens[id(right)])):
                continue
            event = dict(source=left.source_family,context=left.context_kind,iteration=iteration,
                groups=list(key),records=[identity(r.key) for r in [*left.records,*right.records]])
            child = TemplateCluster(left.source_family,left.context_kind,
                [*left.records,*right.records],left.medoid,
                refinements=[*left.refinements,*right.refinements])
            proposed = refine_literal_variants(child,allow_division=False)
            if len(proposed) != 1 or proposed[0].failures:
                event.update(decision="rejected", reason="joint evidence divides into literal formulations or fails native coverage")
                event['hypotheses'] = concise(child.hypotheses)
            else:
                candidate = proposed[0]
                a,b = learning_tokens(left.medoid,candidate.parts),learning_tokens(right.medoid,candidate.parts)
                score = sequence_similarity(a,b)
                supported = any(p['kind']=='slot' and len(p['observed_values'])>1 for p in candidate.parts)
                erased = erased_supported_wording(left,candidate.parts)+erased_supported_wording(right,candidate.parts)
                event.update(score_after_supported_regions=score,
                    diagnostic_comparison=dict(left=list(a),right=list(b),
                        excluded='all slot value contents; each recognized field contributes one typed position'),
                    proposed_pattern=pattern_identity(candidate.parts),hypotheses=concise(candidate.hypotheses))
                if reject_wording_loss([left, right], candidate, path='refine_region_groups', review=review):
                    event.update(decision='rejected', reason='established diagnostic wording would be lost to proposed variable fields')
                elif erased:
                    event.update(decision="divided",reason="independent variable examples retain distinct literal wording; reject the broader PARAM",preserved_wording=erased)
                elif not supported:
                    event.update(decision="rejected",reason="no observed variable region; insufficient evidence for regrouping")
                elif not {u for u in a if u[0] == 'token'} & {u for u in b if u[0] == 'token'}:
                    event.update(decision="rejected",reason="no shared diagnostic word outside accepted fields; field positions alone do not establish a formulation")
                elif not comparable(a,b,threshold):
                    event.update(decision="rejected",reason="remaining case-sensitive wording is below the similarity threshold")
                else:
                    event.update(decision="accepted",reason="joint region evidence supports regrouping by remaining wording")
                    candidate.refinements.append(dict(reason=event['reason'],iteration=iteration,previous_candidates=[left.template_id,right.template_id]))
                    clusters = [c for c in clusters if c is not left and c is not right]+[candidate]
                    active.difference_update((id(left), id(right)))
                    changed = True
            if review is not None:
                review.append(event)
            if changed:
                break
    if review is not None:
        review.append(dict(decision="stopped", reason="one original-group sweep completed; merged groups are not reopened",
            source=clusters[0].source_family if clusters else None, iteration=iteration, groups=len(clusters)))
    return clusters


def cluster_source_records(source_family, records, threshold=.72, *, review=None):
    if not 0 < threshold <= 1:
        raise ValueError("cluster threshold must be in (0,1]")
    if any(r.source_family != source_family for r in records):
        raise ValueError("cross-source records cannot enter a source learner")
    clusters, index = [], defaultdict(set)
    for record in sorted(records,key=lambda r:(r.context_kind,r.text)):
        keys = anchors(learning_tokens(record))
        scope = grouping_scope(record)
        candidates = set().union(*(index[(scope,k)] for k in keys)) if keys else set()
        best,score = None,-1
        for n in sorted(candidates):
            value = sequence_similarity(learning_tokens(record),learning_tokens(clusters[n].medoid))
            if comparable(learning_tokens(record),learning_tokens(clusters[n].medoid),threshold) and value > score:
                best,score = n,value
        if best is None:
            best = len(clusters)
            clusters.append(TemplateCluster(source_family,record.context_kind,[record],record))
            for key in keys:
                index[(scope,key)].add(best)
        else:
            clusters[best].records.append(record)
    clusters = [refined for cluster in clusters for refined in refine_literal_variants(cluster)]
    clusters = [refined for cluster in clusters for refined in refine_supported_wording(cluster,clusters,review)]
    clusters = consolidate_same_wording(clusters,review)
    clusters = refine_region_groups(clusters,threshold,review)
    # Separate discovery groups can converge to exactly the same pattern.
    # Merge that evidence into one candidate rather than reporting repeated
    # copies of an identical contract as competing alternatives.
    unique = {}
    for cluster in clusters:
        key = cluster.template_id
        if key not in unique:
            unique[key] = cluster
            continue
        previous = unique[key]
        child = TemplateCluster(source_family,previous.context_kind,[*previous.records,*cluster.records],previous.medoid,
            refinements=[*previous.refinements,*cluster.refinements])
        child.medoid=choose_medoid(child.records)
        child.parts,child.failures=derive_pattern(child.records,child.medoid,hypotheses=child.hypotheses)
        if reject_wording_loss([previous,cluster],child,path='duplicate_id_consolidation',review=review):
            raise ValueError('identical-template consolidation unexpectedly erased diagnostic wording')
        unique[key]=child
    return sorted(unique.values(),key=lambda c:c.template_id)
