"""Export compact, traceable native evidence for an interactive candidate review.

Reads a verified immutable bundle; performs no inference or registry writes.
Template examples are actual inference supports, not merely matching messages.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import hashlib

from template_learning.artifacts import load_bundle
from template_learning.artifacts import all_patterns
from template_learning.evidence_serialization import native_evidence_rows
from template_learning.records import identity


def conflict_key(row):
    regions = []
    if len(row["matches"]) > 1:
        regions.append(("message", tuple(sorted(m["template_id"] for m in row["matches"]))))
    if row['capture_ambiguities']:
        regions.append(('capture',tuple(sorted(m['template_id'] for m in row['capture_ambiguities']))))
    return row["source_family"], row["context_kind"], tuple(regions)


def rank_samples(pool, sample, limit, *, distinct_unit):
    key = sample["unit"] if distinct_unit else sample["row"]["example_id"]
    previous = pool.get(key)
    if previous is None or sample["occurrences"] > previous["occurrences"]:
        pool[key] = sample
    keep = sorted(pool, key=lambda k: (-pool[k]["occurrences"], pool[k]["row"]["example_id"]))[:limit]
    for key in list(pool):
        if key not in keep:
            del pool[key]


def build(bundle, output, top=20, examples=3):
    model, _ = load_bundle(bundle)
    patterns = all_patterns(model)
    pools = {"message": model["templates"]}
    selected = {name: sorted(ps, key=lambda p: (-p["support_occurrences"], p["template_id"]))[:top]
                for name, ps in pools.items()}
    targets = {p["template_id"]: p for ps in selected.values() for p in ps}
    support_lookup = defaultdict(list)
    for tid, pattern in targets.items():
        for rid in pattern["evidence_record_ids"]:
            support_lookup[rid].append(tid)
    units, full_samples = defaultdict(dict), defaultdict(dict)
    support_counts, support_ids = Counter(), defaultdict(set)
    conflicts, conflict_samples, conflict_rows = Counter(), defaultdict(dict), Counter()
    counts = Counter()
    for row, count in native_evidence_rows(bundle / "native_evidence.json"):
        counts[row["outcome"]] += count
        assert "".join(t for _, t in row["pieces"]) == row["native"]
        possible = [(row["record_id"], row["native"])]
        for rid, text in possible:
            for tid in support_lookup.get(rid, ()):
                support_counts[tid] += count
                support_ids[tid].add(rid)
                sample = dict(row=row, occurrences=count, unit=text)
                rank_samples(units[tid], sample, examples, distinct_unit=True)
                rank_samples(full_samples[tid], sample, examples, distinct_unit=False)
        if row["outcome"] == "provisional":
            key = conflict_key(row)
            # A single complete provisional definition need not be ambiguous.
            # Its support examples above still belong in the ordinary review.
            if not key[2]:
                continue
            conflicts[key] += count
            conflict_rows[key] += 1
            rank_samples(conflict_samples[key], dict(row=row, occurrences=count, unit=row["native"]),
                         examples, distinct_unit=False)
    assert counts == Counter(model["summary"]["training_outcomes"])
    for tid, pattern in targets.items():
        assert support_counts[tid] == pattern["support_occurrences"], tid
        assert len(support_ids[tid]) == pattern["unique_messages"], tid
    records, used_patterns = {}, set()

    def sample_refs(samples, ids):
        refs = []
        for sample in samples:
            row = sample["row"]
            rid = row["example_id"]
            if rid not in records:
                first = row["native_occurrences"][0]
                spans, cursor = [], 0
                for _, text in row["pieces"]:
                    end = cursor + len(text.encode("utf-8", "surrogateescape"))
                    spans.append([cursor, end])
                    cursor = end
                records[rid] = dict(source=row["source_family"], native=row["native"], pieces=row["pieces"],
                    piece_spans=spans,
                    construction=row["construction"], contexts=row["contexts"], occurrences=sample["occurrences"],
                    outcome=row["outcome"], matches={}, capture_ambiguities=row['capture_ambiguities'], first=first,
                    log_path=model["evidence"][first["evidence_sha256"]]["path"])
            all_matches = row["matches"]
            for tid in ids:
                match = next((m for m in all_matches if m["template_id"] == tid),None)
                assert patterns[tid]["source_family"] == row["source_family"]
                if match is not None:
                    records[rid]["matches"][tid] = match["captures"]
                used_patterns.add(tid)
            refs.append(rid)
        return refs

    views = {}
    for name, ps in selected.items():
        views[name] = []
        for pattern in ps:
            tid = pattern["template_id"]
            samples = sorted(units[tid].values(), key=lambda s: (-s["occurrences"], s["row"]["example_id"]))
            for sample in sorted(full_samples[tid].values(), key=lambda s: -s["occurrences"]):
                if len(samples) < examples and all(s["row"]["example_id"] != sample["row"]["example_id"] for s in samples):
                    samples.append(sample)
            views[name].append(dict(id=tid, source=pattern["source_family"], region=name,
                occurrences=pattern["support_occurrences"], variants=pattern["unique_messages"],
                patterns=[tid], examples=sample_refs(samples, [tid])))
    views["ambiguity"] = []
    for key, count in conflicts.most_common(top):
        source, context, regions = key
        ids = [tid for _, tids in regions for tid in tids]
        views["ambiguity"].append(dict(id=identity(key)[:24], source=source,
            region=" + ".join(name for name, _ in regions), occurrences=count, variants=conflict_rows[key],
            context=context, patterns=ids, regions=dict(regions),
            examples=sample_refs(sorted(conflict_samples[key].values(), key=lambda s: -s["occurrences"]), ids)))
    exported_patterns = {}
    for tid in sorted(used_patterns):
        p = patterns[tid]
        exported_patterns[tid] = dict(source=p["source_family"], region=p["context_kind"], display=p["display"],
            status=p['status'],parts=[{k: v for k, v in part.items() if k in {"kind", "text", "type", "name", "prefix", "suffix", "optional", "alternatives", "location_label", "literal_format", "format_pattern"}}
                   for part in p["parts"]], support=p["support_occurrences"], variants=p["unique_messages"])
    result = dict(revision=model["revision_id"], parser=model["parser"]["version"], bundle=str(bundle.resolve()),
        summary=model["summary"], views=views, patterns=exported_patterns, records=records,
        totals={**{name: len(ps) for name, ps in pools.items()}, "ambiguity": len(conflicts)},
        ambiguity_occurrences=sum(conflicts.values()),
        shown_ambiguity_occurrences=sum(g["occurrences"] for g in views["ambiguity"]),
        selection=dict(top=top, examples=examples,
            templates="Complete diagnostic templates ranked by training support occurrences; identities remain source-specific.",
            example_selection="Most frequent native rows with distinct learning-unit text first; extra contexts fill remaining places.",
            ambiguity="Source-specific competing-candidate sets; each ambiguous native row enters exactly one set."))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=True, separators=(",", ":")), encoding="utf-8")
    print(json.dumps(dict(revision=result["revision"], totals=result["totals"], bytes=output.stat().st_size,
        examples=len(records), ambiguous_covered=result["shown_ambiguity_occurrences"],
        ambiguous_total=result["ambiguity_occurrences"], support_counts_verified=len(targets))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--examples", type=int, default=3)
    parser.add_argument("--diagnostics", action="store_true", help="Export all-template frequencies, outliers and prior cases")
    parser.add_argument("--previous-review", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--html", type=Path, help="Write the interactive diagnostic review fragment")
    args = parser.parse_args()
    if args.top < 1 or args.examples < 1:
        parser.error("top and examples must be positive")
    if args.diagnostics:
        if not args.previous_review or not args.baseline:
            parser.error("diagnostics requires --previous-review and --baseline")
        build_diagnostics(args.bundle, args.output, args.previous_review, args.baseline, args.html)
    else:
        build(args.bundle, args.output, args.top, args.examples)


def build_diagnostics(bundle, output, previous_review, baseline, html_output=None):
    """Read-only review metrics. None of these rankings affects inference."""
    from template_learning.parsers import load_parser, reference_from_manifest
    from template_learning.inspect_outer_diagnostics import row_key

    model, selected_parser = load_bundle(bundle)
    lexer = selected_parser.implementation
    manifest = json.loads((baseline / 'manifest.json').read_text(encoding='utf-8'))
    for name, digest in manifest['hashes'].items():
        path = (baseline / name).resolve()
        assert path.parent == baseline.resolve()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    old_model = json.loads((baseline / 'empirical_template_model.json').read_text(encoding='utf-8'))
    assert old_model['parser'] == model['parser']
    assert set(old_model['evidence']) == set(model['evidence'])
    review = json.loads(previous_review.read_text(encoding='utf-8'))
    wanted = {x['record_id'] for x in review['selected'][:17]}
    before = {row_key(r): r for r, _ in native_evidence_rows(baseline / 'native_evidence.json')
              if r['record_id'] in wanted}
    old_patterns = {p['template_id']: p for p in old_model['templates']}
    patterns = {p['template_id']: p for p in model['templates']}
    support_lookup = defaultdict(list)
    metrics = {}
    for tid, p in patterns.items():
        for rid in p['evidence_record_ids']:
            support_lookup[rid].append(tid)
        slots = Counter(part['type'] for part in p['parts'] if part['kind'] == 'slot')
        words = 0
        chain = longest = 0
        for part in p['parts']:
            if part['kind'] == 'literal':
                text = part['text']
                data = text.encode('utf-8', 'surrogateescape')
                pieces = lexer.lexical_pieces(lexer.Source('saved template literal', data), lexer.Span(0, len(data)))
                words += sum(x.kind == 'token' and any(c.isalnum() for c in x.text) for x in pieces)
                if text.strip():
                    chain = 0
            elif part['type'] in {'KEY', 'OPTIONAL_KEY'}:
                chain += 1
                longest = max(longest, chain)
            else:
                chain = 0
        keys = slots['KEY'] + slots['OPTIONAL_KEY']
        denominator = words + keys + slots['VALUE']
        metrics[tid] = dict(id=tid, source=p['source_family'], display=p['display'],
            support=p['support_occurrences'], variants=p['unique_messages'], full=0, ambiguous=0,
            literal_words=words, keys=keys, denominator=denominator,
            key_share=keys / denominator if denominator else 0, key_chain=longest,
            slots=dict(slots), logs=set(), support_logs=Counter(), support_ids=set(), support_count=0,
            key_value_counts={part['name']: len(part['observed_values']) for part in p['parts']
                              if part.get('type') in {'KEY', 'OPTIONAL_KEY'}},
            candidate_status=p['status'], diagnostic_forms=set(),
            examples=[], word_only_params=sum(part.get('type') == 'PARAM' and not part.get('parameter_definition') and
                part.get('field_support', {}).get('assessment', {}).get('word_only_review', False)
                for part in p['parts']))
    pools = defaultdict(list)
    case_rows = {}
    conflicts = []
    outcomes = Counter()
    for row, count in native_evidence_rows(bundle / 'native_evidence.json', retain_occurrences=True):
        assert ''.join(t for _, t in row['pieces']) == row['native']
        assert len(row['native_occurrences']) == count
        log_counts = Counter(o['evidence_sha256'] for o in row['native_occurrences'])
        # Keep compact examples only after all occurrence provenance is counted.
        row = dict(row, native_occurrences=row['native_occurrences'][:1])
        outcomes[row['outcome']] += count
        sample = dict(row=row, count=count)
        if row['record_id'] in wanted:
            case_rows.setdefault(row['record_id'], []).append(sample)
        for tid in support_lookup.get(row['record_id'], ()):
            m = metrics[tid]
            m['support_ids'].add(row['record_id'])
            m['support_count'] += count
            m['support_logs'].update(log_counts)
            pool = pools[tid]
            if all(s['row']['record_id'] != row['record_id'] for s in pool):
                pool.append(sample)
            pool.sort(key=lambda s: (-s['count'], s['row']['record_id']))
            del pool[2:]
        for match in row['matches']:
            m = metrics[match['template_id']]
            m['full' if row['outcome'] == 'full' else 'ambiguous'] += count
            m['logs'].update(log_counts)
            raw = row['native'].encode('utf-8', 'surrogateescape')
            excluded_fields = {part['name'] for part in patterns[match['template_id']]['parts']
                               if part.get('type') == 'LOCATOR' or part.get('parameter_definition')}
            cursor = 0; form = []
            for capture in match['captures']:
                if capture['name'] not in excluded_fields or capture['span'] is None:
                    continue
                a, b = capture['span']
                form.extend((raw[cursor:a], b'<LOCATOR_OR_DECLARED_PARAM>')); cursor = b
            form.append(raw[cursor:])
            m['diagnostic_forms'].add(b''.join(form))
        for match in row['capture_ambiguities']:
            metrics[match['template_id']]['ambiguous'] += count
        if row['outcome'] == 'provisional':
            conflicts.append(sample)
    assert outcomes == Counter(model['summary']['training_outcomes'])
    records = {}

    def save_sample(sample):
        r = sample['row']; rid = r['example_id']
        if rid not in records:
            records[rid] = dict(source=r['source_family'], native=r['native'], pieces=r['pieces'],
                count=sample['count'], outcome=r['outcome'], matches=r['matches'],
                capture_ambiguities=r['capture_ambiguities'], provenance=r['native_occurrences'][0])
        return rid

    for tid, m in metrics.items():
        assert m.pop('support_count') == m['support']
        assert len(m.pop('support_ids')) == m['variants']
        m['logs'] = len(m['logs'])
        assert sum(m['support_logs'].values()) == m['support']
        m['support_log_count'] = len(m['support_logs'])
        m['diagnostic_forms'] = len(m['diagnostic_forms'])
        m['examples'] = [save_sample(s) for s in pools[tid]]
        peers = [v for v in metrics.values() if v['source'] == m['source']]
        m['source_peers'] = len(peers)
        m['source_percentile'] = (100 * sum(v['key_share'] < m['key_share'] for v in peers) / len(peers)
                                  if len(peers) >= 5 else None)
        m['global_percentile'] = 100 * sum(v['key_share'] < m['key_share'] for v in metrics.values()) / len(metrics)
    assert sum(m['full'] for m in metrics.values()) == outcomes['full']
    cases = []
    for number, x in enumerate(review['selected'][:17], 1):
        samples = case_rows.get(x['record_id'], [])
        assert samples, ('missing native case', number)
        for sample in samples:
            prior = before[row_key(sample['row'])]
            cases.append(dict(number=number, sample=save_sample(sample),
                original=x['templates'], original_outcome=x['after'],
                before=[old_patterns[m['template_id']]['display'] for m in prior['matches']],
                before_outcome=prior['outcome']))
    rank = lambda key: [x['id'] for x in sorted(metrics.values(), key=key)]
    rankings = dict(
        frequency=rank(lambda x: (-x['full'], x['id'])),
        key_share=rank(lambda x: (-x['key_share'], -x['full'], x['id'])),
        key_chain=rank(lambda x: (-x['key_chain'], -x['full'], x['id'])),
        word_params=[x['id'] for x in sorted(metrics.values(), key=lambda x: (-x['word_only_params'], -x['full'], x['id'])) if x['word_only_params']],
        sparse=[x['id'] for x in sorted(metrics.values(), key=lambda x: (-x['literal_words'], -x['full'], x['id']))
                if x['variants'] == 1 and x['keys'] == 0 and x['slots'].get('PARAM', 0) == 0 and x['slots'].get('REASON', 0) == 0],
        ambiguity=[x['id'] for x in sorted(metrics.values(), key=lambda x: (-x['ambiguous'], x['id'])) if x['ambiguous']])
    result = dict(revision=model['revision_id'], baseline=old_model['revision_id'],
        original_revision=review['candidate'], summary=model['summary'], metrics=metrics,
        rankings=rankings, records=records, cases=cases, conflicts=[save_sample(s) for s in conflicts],
        definitions=dict(frequency='Unique complete matches only; ambiguous occurrences appear separately and are not counted twice.',
            key_share='(KEY + OPTIONAL_KEY slots) / (literal alphanumeric raw tokens + KEY + OPTIONAL_KEY + VALUE slots). PARAM, REASON and LOCATOR interiors and slots are excluded. Punctuation and gaps are excluded.',
            percentile='Percentage of templates with a strictly lower KEY share; source percentile is shown only with at least five same-source templates. Ranks flag inspection, not errors.',
            provenance='Support logs and their counts include every saved occurrence, not just displayed examples. Diagnostic forms count matched native texts after replacing captured LOCATOR and owner-declared PARAM values (traces and character descriptions); empirical PARAM and REASON contents remain. KEY diversity counts distinct observed spellings per KEY field. All current validation is on the training corpus, not independent testing.',
            key_chain='Longest run of KEY/OPTIONAL_KEY slots separated only by whitespace.',
            sparse='One distinct supporting message, no KEY, PARAM or REASON slots. Locators and numeric VALUE slots may remain. Not proof of incorrect memorization.',
            word_params='Undeclared PARAM fields whose saved boundary assessment flags absence of adjacent punctuation. Owner-declared traces are excluded.',
            examples='Two most frequent distinct supporting messages; exact native pieces and saved captures. Not a representative random sample.',
            previous_cases='Original outer-delivery cases 01–17, matched by stable native record ID. Before is the immediate v21 baseline; original is the earlier review.'),
        provenance=dict(bundle=str(bundle.resolve()), baseline=str(baseline.resolve()), previous_review=str(previous_review.resolve()),
            parser=model['parser'], input_hashes=sorted(model['evidence']), verified_support_templates=len(metrics)))
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, ensure_ascii=True, separators=(',', ':'))
    output.write_text(payload, encoding='utf-8')
    if html_output:
        inline = json.loads(payload)
        # Keep complete provenance in the JSON export. The bounded inline view
        # has two examples for priority rankings and one for other templates.
        priority = {tid for ranked in rankings.values() for tid in ranked[:10]}
        for tid, item in inline['metrics'].items():
            item.pop('support_logs')
            if tid not in priority:
                item['examples'] = item['examples'][:1]
        retained = {rid for item in inline['metrics'].values() for rid in item['examples']}
        retained.update(c['sample'] for c in inline['cases'])
        retained.update(inline['conflicts'])
        inline['records'] = {rid: row for rid, row in inline['records'].items() if rid in retained}
        inline['definitions']['examples'] = 'Up to two most frequent distinct supporting messages for leading ranks; one for other templates. Exact native pieces and saved captures; not a representative random sample.'
        inline_payload = json.dumps(inline, ensure_ascii=True, separators=(',', ':'))
        markup = Path(__file__).with_name('template_review.html').read_text(encoding='utf-8')
        markup = markup.replace('__REVIEW_DATA__', inline_payload.replace('<', '\\u003c'))
        if len(markup.encode('utf-8')) >= 1_000_000:
            raise ValueError('inline review exceeds 1 MB; reduce exported examples before rendering')
        html_output.parent.mkdir(parents=True, exist_ok=True)
        html_output.write_text(markup, encoding='utf-8')
    print(json.dumps(dict(templates=len(metrics), cases=len(cases), native_examples=len(records),
        verified_unique_occurrences=sum(m['full'] for m in metrics.values()), bytes=len(payload),
        top=[dict(source=metrics[t]['source'], occurrences=metrics[t]['full'], template=metrics[t]['display'])
             for t in rankings['frequency'][:5]]), indent=2))


if __name__ == "__main__":
    main()
