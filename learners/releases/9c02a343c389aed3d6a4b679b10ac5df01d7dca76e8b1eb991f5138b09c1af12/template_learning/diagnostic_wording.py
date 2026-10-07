"""Block loss of listed, already-literal CK3 symbol types to declared slot types.

This does not assign literals or slot types. All ranges come from existing raw
pieces and verified template captures; no language tagger runs during inference.
"""
from template_learning.literal_guidance import guided_ranges
from template_learning.owner_rules import DIAGNOSTIC_WORDING_LOSS, LOSS_REFERENCE_WORDING, INFERENCE_POLICY
from template_learning.matching_defaults import match_pattern
from template_learning.matching_primitives import pattern_identity
from template_learning.records import identity
from template_learning.regions import enclosing_pair


def established_wording(cluster):
    """Cache listed literal spans for each native member, excluding old slots."""
    signature = identity(pattern_identity(cluster.parts))
    cached = getattr(cluster, '_loss_wording', None)
    if cached is not None and cached[0] == signature and cached[1] == len(cluster.records):
        return cached[2]
    result = []
    for record in cluster.records:
        ranges = guided_ranges(record.pieces, LOSS_REFERENCE_WORDING)
        if not ranges:
            continue
        old = match_pattern(cluster.parts, record.text, pieces=record.pieces)
        if old is None:
            continue  # Not an established literal/capture assignment.
        variables = [c['span'] for c in old if c['span'] is not None]
        offsets = [0]
        for _, value in record.pieces:
            offsets.append(offsets[-1] + len(value.encode('utf-8', 'surrogateescape')))
        hits = []
        for start, end in ranges:
            a = len(record.text[:start].encode('utf-8', 'surrogateescape'))
            b = len(record.text[:end].encode('utf-8', 'surrogateescape'))
            if not any(x < b and a < y for x, y in variables):
                hits.append((record.text[start:end], a, b))
        if hits:
            result.append((record, identity(record.key), offsets, hits))
    cluster._loss_wording = (signature, len(cluster.records), result)
    return result


def diagnostic_wording_loss(cluster, proposed):
    """Return native witnesses of old literals swallowed by proposed fields.

    Proposed field-support ranges come from inference and have already passed
    complete-capture validation at merge call sites. Check every native member,
    retaining one witness per lost spelling and proposed field in the report.
    """
    guarded_types = frozenset(DIAGNOSTIC_WORDING_LOSS['target_slot_types'])
    fields = [p for p in proposed if p.get('type') in guarded_types]
    if not LOSS_REFERENCE_WORDING or not fields or cluster.failures:
        return []
    members = {p['name']: {m['record_id']: m['pieces']
               for m in p.get('field_support', {}).get('members', [])} for p in fields}
    types = {p['name']: p['type'] for p in fields}
    losses = {}
    for record, record_id, offsets, hits in established_wording(cluster):
        spans = []
        for part in fields:
            field = members[part['name']].get(record_id)
            if field is not None:
                spans.append((part['name'], offsets[field[0]], offsets[field[1]]))
        # Inspection can compare frozen patterns on other native evidence too.
        if len(spans) != len(fields):
            captures = match_pattern(proposed, record.text, pieces=record.pieces)
            spans = [(c['name'], *c['span']) for c in captures or []
                     if c['type'] in guarded_types and c['span'] is not None]
        for phrase, a, b in hits:
            for name, start, end in spans:
                # Recognize the complete phrase first. Losing even one of its
                # word tokens breaks it; moving only a gap does not.
                swallowed_start, swallowed_end = max(start, a), min(end, b)
                swallowed = record.text.encode('utf-8','surrogateescape')[swallowed_start:swallowed_end].decode('utf-8','surrogateescape') if swallowed_start < swallowed_end else ''
                if swallowed.strip():
                    losses.setdefault((phrase, name), dict(
                        wording=phrase, literal_span=[a, b], proposed_slot=name,
                        proposed_slot_type=types[name],
                        swallowed_wording=swallowed,
                        proposed_span=[start, end], record_id=record_id,
                        native=record.text, previous_template=cluster.template_id))
    return list(losses.values())


def key_run_wording_loss(cluster, proposed):
    """Preserve an established word run against newly inferred KEY content.

    A previous formulation must have independent non-location field variation.
    Only complete raw words previously outside every capture count. This checks
    a proposed merge, not vocabulary membership or initial slot assignment.
    """
    policy = INFERENCE_POLICY['established_wording_key_run_loss']
    if (not policy['enabled'] or cluster.failures or len(cluster.records) < 2
            or not any(p.get('kind') == 'slot' and p['type'] != 'LOCATOR'
                       and len(p['observed_values']) > 1 for p in cluster.parts)):
        return []
    names = {part['name'] for part in proposed
             if part.get('type') in {'KEY', 'OPTIONAL_KEY'}}
    if not names:
        return []
    record = cluster.medoid
    old = match_pattern(cluster.parts, record.text, pieces=record.pieces)
    new = match_pattern(proposed, record.text, pieces=record.pieces)
    if old is None or new is None:
        return []
    variables = [c['span'] for c in old if c['span'] is not None]
    captures = {c['name']: c['span'] for c in new if c['span'] is not None}
    word_runs, words, cursor = [], [], 0
    for kind, text in record.pieces:
        end = cursor + len(text.encode('utf-8', 'surrogateescape'))
        literal = not any(a < end and cursor < b for a, b in variables)
        if literal and kind == 'token' and text.isalpha():
            words.append((text, cursor, end))
        elif not (literal and kind == 'gap' and '\n' not in text and '\r' not in text):
            if words:
                word_runs.append(words)
            words = []
        cursor = end
    if words:
        word_runs.append(words)
    losses = []
    for run in word_runs:
        if len(run) < policy['minimum_words']:
            continue
        swallowed = [(word, a, b, name) for word, a, b in run for name in sorted(names)
                     if name in captures and captures[name][0] <= a and b <= captures[name][1]]
        if not swallowed:
            continue
        losses.append(dict(established_word_run=[word for word, _, _ in run],
            wording=[word for word, _, _, _ in swallowed],
            literal_spans=[[a, b] for _, a, b, _ in swallowed],
            proposed_slots=[name for _, _, _, name in swallowed],
            record_id=identity(record.key), native=record.text,
            previous_template=cluster.template_id))
    return losses


def enclosed_identifier_evidence(proposed, names):
    """Positive native boundary/variation evidence, not a symbol-word exemption."""
    policy = DIAGNOSTIC_WORDING_LOSS['enclosed_identifier_evidence']
    result = {}
    for part in proposed.parts:
        if part.get('name') not in names or part.get('type') not in policy['slot_types']:
            continue
        values = {v for v in part['observed_values'] if v}
        if len(values) < policy['minimum_distinct_nonempty_values']:
            continue
        members = {m['record_id']: m['pieces']
                   for m in part.get('field_support', {}).get('members', [])}
        if any(identity(record.key) not in members for record in proposed.records):
            continue
        spans = [members[identity(record.key)] for record in proposed.records]
        pair = enclosing_pair(proposed.records, spans)
        if pair is not None:
            result[part['name']] = dict(enclosing_pair=pair,
                distinct_nonempty_values=len(values), native_members=len(proposed.records),
                type=part['type'])
    return result


def reject_wording_loss(previous, proposed, *, path, review=None):
    losses = [loss for cluster in previous for loss in diagnostic_wording_loss(cluster, proposed.parts)]
    if losses:
        bounded = enclosed_identifier_evidence(proposed, {loss['proposed_slot'] for loss in losses})
        allowed = [loss for loss in losses if loss['proposed_slot'] in bounded]
        if allowed and review is not None:
            review.append(dict(decision='allowed_by_field_evidence',
                reason='corresponding enclosed identifier fields have distinct native values; symbol words here are demonstrated field contents',
                rule=DIAGNOSTIC_WORDING_LOSS['id'], path=path, source=proposed.source_family,
                previous_patterns=[pattern_identity(c.parts) for c in previous],
                proposed_pattern=pattern_identity(proposed.parts), lost_wording=allowed,
                field_evidence=bounded))
        losses = [loss for loss in losses if loss['proposed_slot'] not in bounded]
    if not losses:
        key_losses = [loss for cluster in previous for loss in key_run_wording_loss(cluster, proposed.parts)]
        if key_losses:
            if review is not None:
                review.append(dict(decision='rejected',
                    reason='independently established word sequence would lose wording to KEY slots',
                    rule='established-wording-to-key-run-loss', path=path, source=proposed.source_family,
                    previous_patterns=[pattern_identity(c.parts) for c in previous],
                    proposed_pattern=pattern_identity(proposed.parts), lost_wording=key_losses))
            return True
    if not losses:
        return False
    event = dict(decision='rejected', reason='listed established diagnostic wording would become variable slot content',
        rule=DIAGNOSTIC_WORDING_LOSS['id'], path=path, source=proposed.source_family,
        previous_patterns=[pattern_identity(c.parts) for c in previous],
        proposed_pattern=pattern_identity(proposed.parts), lost_wording=losses)
    if review is not None:
        review.append(event)
    return True
