"""Render contextual review of the genuine all-corpus function-word KEY audit."""
import argparse
from collections import Counter, defaultdict
import html
import json
from pathlib import Path


GRAMMAR = {'8a7b103dfff65e36ea012187','4801c5fa48227a91fa59489f','64e3a738d3655e27f993a28e'}
NAME_PARTS = {'6d3198f1de91025a781b1e33','f0f759d876fcaff5170bc95f','32c2191f6fdd59776673222b','bb124e12f5b445576b7a7d2a','22d4ae478155a24a2f5039ed'}


def review(identifier, template):
    if identifier in GRAMMAR:
        return 'Incorrect grammatical KEYs', 'The phrase is ordinary diagnostic wording, split into three independent KEYs. Its words are not identifiers.'
    if identifier in NAME_PARTS:
        return 'Name / field boundaries need review', 'A multiword display value is divided into KEY positions. Review the whole field; do not replace only its function-word spelling.'
    if identifier == '0e4e3302cde2fc5e07a2227f':
        return 'Spelling coincidence', 'May is a month within the owner-directed format-constrained date KEY, not a modal verb.'
    if template['source_family'] in ('culture_name_equivalency.cpp','characterhistory.cpp','character.cpp'):
        return 'Display / markup content', 'The hit belongs to a displayed name, trait, or markup value, not grammatical diagnostic wording. Slot boundaries may warrant separate review.'
    return 'Identifier / reported value', 'The message reports a script/localization identifier, function/property name, type, or offending token. The spelling is not being used as English sentence grammar here.'


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence',type=Path,required=True)
    args=cli.parse_args();root=args.evidence
    load=lambda name:json.loads((root/name).read_bytes())
    data=load('function-word-audit.json');templates=load('removed-template-analysis.json')['templates']['candidate']
    groups=defaultdict(list)
    for binding in data['bindings']:groups[binding['template_id']].append(binding)
    esc=lambda text:html.escape(str(text))
    def pre(text):
        visible=''.join(c if c in '\r\n\t' or ord(c)>=32 else '\\u%04x'%ord(c) for c in str(text))
        return '<pre>'+esc(visible)+'</pre>'
    phrases=Counter();phrase_occ=Counter()
    for run in data['adjacent_key_runs']:
        if run['template_id'] in GRAMMAR:
            phrases[run['text']]+=run['contextual_messages'];phrase_occ[run['text']]+=run['occurrences']
    assert phrases=={"hasn't been born":154,'the wrong gender':81}
    assert phrase_occ=={"hasn't been born":371,'the wrong gender':117}
    bits=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Function words incorrectly captured as KEY</title>',
        '<style>body{font:16px/1.55 system-ui;max-width:1120px;margin:32px auto;padding:0 24px;color:#243747}h1,h2,h3{line-height:1.2}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef3f6;padding:12px;font-size:13px}table{width:100%;border-collapse:collapse}th,td{padding:9px;text-align:left;vertical-align:top;border-bottom:1px solid #cbd5df}details{border-top:1px solid #cbd5df;padding:12px 0}summary{cursor:pointer}.note{background:#fff0d7;padding:18px}.meta{font-size:13px;color:#506578}a{color:#075e91}</style>',
        '<h1>Function words incorrectly captured as KEY</h1><p><a href="NAME-COMPARISON.html">Name captures: already present in production</a> · <a href="RECOMMENDATIONS.html">Residual survey and all owner concerns</a> · <a href="SEMANTICS.html">Production comparison</a> · <a href="function-word-audit.json">Complete audit evidence</a></p>',
        '<p class="note"><strong>Confirmed:</strong> ordinary diagnostic phrases are split into individual KEYs in 235 contextual messages / 488 occurrences across three templates. The earlier audit omitted contractions and articles; this expanded audit includes them. It changes review tooling only, not the learner or either model.</p>',
        '<h2>The grammatical terms</h2><p><strong>Function words</strong> is the useful umbrella for grammatical words: prepositions, auxiliaries, determiners, pronouns and conjunctions. Before/after have different word classes depending on context. Has not combines an auxiliary with negation; hasn’t is its negative contraction. The is an article/determiner. Born and gender are content words: the defect concerns whole phrases, not only function words.</p>',
        '<p>References: <a href="https://dictionary.cambridge.org/grammar/british-grammar/before">Cambridge: before</a>, <a href="https://dictionary.cambridge.org/grammar/british-grammar/after-afterwards">after</a>, <a href="https://dictionary.cambridge.org/grammar/british-grammar/contractions">contractions</a>, <a href="https://dictionary.cambridge.org/grammar/british-grammar/not">negation</a>.</p>',
        '<h2>Confirmed phrase-splitting defect</h2><table><tr><th>Native phrase</th><th>Selected captures</th><th>Contextual messages</th><th>Occurrences</th></tr>']
    for phrase,count in phrases.items():
        bits.append('<tr><td>'+esc(phrase)+'</td><td>'+esc(' | '.join(phrase.split()))+'</td><td>'+str(count)+'</td><td>'+str(phrase_occ[phrase])+'</td></tr>')
    bits.extend(['</table><p>The actual CK3 wording includes <code>is hasn’t been born</code>; the awkward grammar is preserved. Each alternative has three whitespace-separated words: <code>hasn’t / the</code>, <code>been / wrong</code>, <code>born / gender</code>. That alignment is the observable pattern behind the bad slot layout. It is not by itself proof of which learning step introduced it.</p>',
        '<p>Three saved public-matcher witnesses already confirm the same grammatical KEY captures in production. This is an inherited defect, not evidence of a new candidate regression. The historical v34 investigation documented this phrase-pair failure during regrouping, but the current production/candidate decision history still needs tracing before claiming the same branch caused today’s result. <a href="inherited-key-witnesses.json">Production witnesses</a>.</p>',
        '<h2>Scope and limits</h2><p>'+esc(f"Scanned all 73 logs’ retained training evidence: {data['contextual_messages_scanned']:,} contextual message rows, {data['occurrences_scanned']:,} occurrences, and {sum(data['region_key_capture_counts'].values()):,} nonempty selected KEY/OPTIONAL_KEY captures. All assignment regions were visited; all KEY captures found were in message bodies.")+'</p>',
        '<p>'+esc(f"The explicit {len(data['spelling_inventory'])}-spelling inventory flagged {data['affected_contextual_messages']:,} rows / {data['affected_occurrences']:,} occurrences, with {len(data['bindings'])} template/slot/value bindings. These are review leads, not that many confirmed errors. Case and apostrophe normalization affect lookup only; native values and UTF-8 byte spans are preserved and checked.")+'</p>',
        '<p>Before, from, and the separate value has were absent from the selected KEY captures. The two history phrases after death / from before remain literal in this incremental candidate; their requested PARAM treatment remains separate pending work. After appears as a reported event/namespace identifier in four messages, not as a preposition in the diagnostic sentence. No has not KEY phrase was found. Longer values are searched too, with embedded matches marked separately.</p>',
        '<h2>What the other hits show</h2><p>Place-name fragments include <code>Antiochia in Pisidien</code>, <code>Isle of Wight</code>, and <code>The Isles</code>. These suggest reviewing complete multiword fields. Other apparent English words are name particles in other languages, such as <code>am</code> in <code>Antiochia am Saros</code>. Dotted localization keys ending in <code>.a</code>, the month May, and the trait Just are spelling coincidences, not English grammatical wording.</p>',
        '<h2>Recommended correction direction</h2><p>Do not permit ordinary diagnostic phrases to become independent KEY positions merely because their words satisfy KEY syntax. Trace initial inference and every merge for the three affected templates, using these genuine phrase pairs. Then apply a reusable phrase-level correction: retain established diagnostic wording, or infer one coherent PARAM where supported and owner-approved. Function-word hits should help identify such spans, including adjacent content words; replacing only hasn’t or the would leave the defect.</p>',
        '<p>The owner-directed after death / from before PARAM is an additional acceptance case. Preserve legitimate reported identifiers such as if, not, this and after in their identifier positions. This report implements the audit, not a word blacklist or an unverified learner change.</p>',
        '<h2>Every flagged template and binding</h2><p>Counts below are per binding; do not sum them as unique messages. Multiple flagged words can occur in the same message. Expand each template for values, slots, genuine examples and provenance.</p>'])
    ordered=sorted(groups,key=lambda tid:(0 if tid in GRAMMAR else 1 if tid in NAME_PARTS else 2,tid))
    for tid in ordered:
        category,note=review(tid,templates[tid]);bs=groups[tid]
        bits.append('<details'+(' open' if tid in GRAMMAR else '')+'><summary>'+esc(category+' · '+templates[tid]['source_family']+' · '+tid)+'</summary><p>'+esc(note)+'</p>'+pre(templates[tid]['display']))
        for b in bs:
            e=b['examples'][0]
            bits.append('<details><summary>'+esc(f"{b['slot']}: {b['value']} — {b['contextual_messages']} messages / {b['occurrences']} occurrences")+'</summary><p>'+esc('; '.join(h['word']+' ('+h['kind']+'): '+', '.join(h['categories']) for h in b['hits']))+'</p>'+pre(e['text'])+'<p class="meta">UTF-8 byte span '+esc(e['span'])+' · '+esc(e['provenance'])+'</p>')
            if e['adjacent_key_run']:bits.append('<p>Adjacent KEY captures:</p>'+pre(json.dumps(e['adjacent_key_run'],ensure_ascii=True,indent=2)))
            bits.append('</details>')
        bits.append('</details>')
    bits.extend(['<details><summary>Explicit search vocabulary</summary>'+pre(json.dumps(data['categories'],indent=2))+'</details>','</html>'])
    (root/'FUNCTION-WORDS.html').write_text('\n'.join(bits),encoding='utf-8')
    print(json.dumps(dict(templates=len(groups),bindings=len(data['bindings']),phrase_messages=dict(phrases),phrase_occurrences=dict(phrase_occ))))


if __name__=='__main__':main()
