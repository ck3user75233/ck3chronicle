"""Inventory selected KEY captures in genuine saved candidate training evidence."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

from template_learning.evidence_serialization import native_evidence_rows, write_json


CATEGORIES = {
    'preposition / connective (context dependent)': 'after before from to of in on at by for with without into onto over under through during between among against around as than about above across along amid amongst behind below beneath beside besides beyond despite down except inside like near off outside past per since throughout till toward towards underneath until up upon via within',
    'auxiliary / modal form (may have other uses)': 'am is are was were be been being do does did done doing have has had having can cannot could may might must shall should will would ought need dare',
    'negation / related adverb': 'not never neither nor nowhere hardly scarcely barely',
    'negative contraction': "ain't aren't can't couldn't daren't didn't doesn't don't hadn't hasn't haven't isn't mayn't mightn't mustn't needn't oughtn't shan't shouldn't wasn't weren't won't wouldn't",
    'pronoun / determiner / article': 'a an the all any anybody anyone anything both each either enough every everybody everyone everything few fewer he her hers herself him himself his i it its itself less little many me mine more most much my myself no nobody none nothing one other others our ours ourselves own several she some somebody someone something such that their theirs them themselves these they this those us we what whatever which whichever who whoever whom whomever whose you your yours yourself yourselves',
    'conjunction / connective': 'although and because but even if lest once or provided providing so supposing though unless whereas whether while whilst yet',
    'subject / auxiliary contraction': "i'm you're he's she's it's we're they're i've you've we've they've i'd you'd he'd she'd it'd we'd they'd i'll you'll he'll she'll it'll we'll they'll that's there's here's what's who's let's",
    'related adverb (not all adverbs are function words)': 'again ago already also always away back else ever here hence however just now only otherwise out rather still then there therefore thus together too when whenever where wherever why how',
    'owner diagnostic wording watchlist': 'effect trigger',
}
LOOKUP = {}
for category, words in CATEGORIES.items():
    for word in words.split():
        LOOKUP.setdefault(word, []).append(category)
LEXEMES = re.compile(r"\w+(?:['’]\w+)*", re.UNICODE)


def hits(value):
    """Lookup only: preserve original values/spans, including apostrophe spelling."""
    normalized = value.casefold().replace('’', "'")
    if normalized in LOOKUP:
        return [dict(word=normalized, categories=LOOKUP[normalized], kind='whole value')]
    words={w.casefold().replace('’', "'") for w in LEXEMES.findall(value)}
    return [dict(word=w, categories=LOOKUP[w], kind='within value')
            for w in sorted(words) if w in LOOKUP]


def capture_groups(node, path='assignment'):
    if isinstance(node, dict):
        if isinstance(node.get('captures'), list):
            yield path, node['captures']
        for key, value in node.items():
            if key not in ('captures', 'selection') and isinstance(value, (dict, list)):
                yield from capture_groups(value, path + '/' + key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from capture_groups(value, path + '/' + str(index))


def adjacent_run(captures, cap, text):
    native=text.encode('utf-8', 'surrogateescape')
    ordered = sorted((c for c in captures if c.get('span') and c.get('value')),
                     key=lambda c: c['span'][0])
    index = ordered.index(cap)
    lo = hi = index
    def joins(left, right):
        return (left['type'] in ('KEY', 'OPTIONAL_KEY') and
                right['type'] in ('KEY', 'OPTIONAL_KEY') and
                native[left['span'][1]:right['span'][0]].isspace())
    while lo and joins(ordered[lo-1], ordered[lo]): lo -= 1
    while hi+1 < len(ordered) and joins(ordered[hi], ordered[hi+1]): hi += 1
    run = ordered[lo:hi+1]
    return dict(text=native[run[0]['span'][0]:run[-1]['span'][1]].decode('utf-8','surrogateescape'), captures=run)


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--bundle',type=Path,required=True)
    cli.add_argument('--output',type=Path,required=True)
    args=cli.parse_args(); bindings={};messages=Counter();occurrences=Counter()
    phrases={};regions=Counter();affected=affected_occ=0
    total=0; total_occurrences=0
    for row,count in native_evidence_rows(args.bundle/'native_evidence.json'):
        total+=1;total_occurrences+=count
        chosen=row.get('selected_assignment')
        if not chosen:continue
        native=row['native'].encode('utf-8','surrogateescape')
        for capture in chosen['captures']:
            if capture.get('span') and capture.get('value') is not None:
                a,b=capture['span']
                assert native[a:b].decode('utf-8','surrogateescape')==capture['value'], (row['example_id'],capture)
        values=set();row_phrases=set()
        for region,captures in capture_groups(chosen):
            for cap in captures:
                value=cap.get('value')
                if cap.get('type') not in ('KEY','OPTIONAL_KEY') or not value:continue
                regions[region]+=1
                found=hits(value)
                if not found:continue
                values.add(value)
                key=chosen['template_id'],region,cap.get('name',cap.get('slot_id')),value
                entry=bindings.setdefault(key,dict(template_id=key[0],region=region,slot=key[2],value=value,hits=found,source=row['source_family'],
                    contextual_messages=0,occurrences=0,examples=[]))
                entry['contextual_messages']+=1;entry['occurrences']+=count
                run=adjacent_run(captures,cap,row['native']) if region=='assignment' else None
                if len(entry['examples'])<2:entry['examples'].append(dict(text=row['native'],span=cap['span'],adjacent_key_run=run,
                    provenance=row['native_occurrences'][:1],contexts=row['contexts'] if region!='assignment' else None,
                    continuations=row['continuations'] if region!='assignment' else None))
                if run and len(run['captures'])>1:
                    pk=chosen['template_id'],run['text'],tuple(c['name'] for c in run['captures'])
                    if pk not in row_phrases:
                        row_phrases.add(pk)
                        phrase=phrases.setdefault(pk,dict(template_id=pk[0],text=pk[1],slots=pk[2],source=row['source_family'],
                            contextual_messages=0,occurrences=0,example=dict(text=row['native'],captures=run['captures'],provenance=row['native_occurrences'][:1])))
                        phrase['contextual_messages']+=1;phrase['occurrences']+=count
        if values:affected+=1;affected_occ+=count
        for value in values:
            messages[value]+=1;occurrences[value]+=count
        if total%20000==0:print('Audited contextual rows',total,flush=True)
    result=dict(scope='Controlled incremental candidate; all 73 training logs; selected KEY/OPTIONAL_KEY captures in all assignment regions; contextual messages counted once per exact value, separately per slot in binding rows',
        limitations='Explicit spelling inventory, not automatic grammatical classification. Within-value hits are separate leads, including names and qualified identifiers. Same spelling may serve different grammatical functions.',
        categories=CATEGORIES,region_key_capture_counts=dict(regions),affected_contextual_messages=affected,affected_occurrences=affected_occ,
        spelling_inventory=sorted(LOOKUP),contextual_messages_scanned=total,occurrences_scanned=total_occurrences,
        values=[dict(value=k,messages=v,occurrences=occurrences[k],hits=hits(k)) for k,v in sorted(messages.items())],
        bindings=list(bindings.values()),adjacent_key_runs=list(phrases.values()))
    write_json(args.output,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('bindings','spelling_inventory','categories','adjacent_key_runs','values')},indent=2))


if __name__=='__main__':main()
