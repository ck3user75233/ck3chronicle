"""Find negative-adjective review candidates in native literal/PARAM text.

Language tags propose review candidates, never learner literals or automatic
blockers. This optional offline tool does not participate in inference/matching.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from template_learning.inspect_incremental_learning import native_evidence_rows


def survey(evidence, data_dir, output):
    import nltk
    from nltk.tag import PerceptronTagger
    nltk.data.path.insert(0, str(data_dir.resolve()))
    tagger = PerceptronTagger()
    words = {}
    total_rows = total_occurrences = 0
    excluded = Counter()
    retained_rows = 0
    for row, count in native_evidence_rows(evidence):
        # Use exactly the parser's existing pieces. Do not invoke word_tokenize.
        tokens, token_spans, cursor = [], [], 0
        for kind, text in row['pieces']:
            end = cursor + len(text.encode('utf-8','surrogateescape'))
            if kind == 'token':
                tokens.append(text)
                token_spans.append((cursor,end))
            cursor = end
        present = defaultdict(Counter)
        roles = defaultdict(lambda: defaultdict(Counter))
        unique_assignment = len(row['matches']) == 1 and not row['capture_ambiguities']
        captures = row['matches'][0]['captures'] if unique_assignment else []
        # Classify ranges before the language pass. Excluded fields never enter
        # tagger input, and text on opposite sides is never stitched together.
        runs, run, previous_role = [], [], None
        for word, (a,b) in zip(tokens,token_spans):
            role = next((c['type'] for c in captures if c['span'] is not None
                         and c['span'][0]<=a and b<=c['span'][1]),
                        'literal' if unique_assignment else 'unresolved_assignment')
            if role not in {'literal','PARAM'} or role != previous_role:
                if run:
                    runs.append((previous_role,run))
                    run=[]
            if role in {'literal','PARAM'}:
                run.append(word)
            else:
                excluded[role] += 1
            previous_role = role
        if run:
            runs.append((previous_role,run))
        if runs:
            retained_rows += 1
        observations = [(word,tag,role) for role,run in runs for word,tag in tagger.tag(run)]
        for word, tag, role in observations:
            if word.isalpha():
                present[word][tag] += 1
                roles[word][role][tag] += 1
        for word, tags in present.items():
            entry = words.setdefault(word, dict(word=word, distinct_messages=0,
                occurrences=0, tags=Counter(), sources=Counter(), role_tags=defaultdict(Counter), examples=[]))
            entry['distinct_messages'] += 1
            entry['occurrences'] += count
            entry['tags'].update(tags)
            entry['sources'][row['source_family']] += 1
            for role, role_counts in roles[word].items():
                entry['role_tags'][role].update(role_counts)
            # Retain a witness for each grammatical reading, not just the first
            # few sources. Adjective evidence must show its actual tagged context.
            covered = {(role,tag) for e in entry['examples'] for role,tags_by_role in e['role_tags'].items() for tag in tags_by_role}
            observed = {(role,tag) for role,counts in roles[word].items() for tag in counts}
            if (not observed <= covered or len(entry['examples']) < 3) and row['native'] not in {e['native'] for e in entry['examples']}:
                entry['examples'].append(dict(source=row['source_family'],native=row['native'],
                    pieces=row['pieces'],provenance=row['native_occurrences'][:1],tags=dict(tags),role_tags=dict(roles[word])))
        total_rows += 1
        total_occurrences += count
        if total_rows % 5000 == 0:
            print(f'Scanned {total_rows} native message rows; tagged {retained_rows} eligible rows', flush=True)
    model_dir = data_dir/'taggers'/'averaged_perceptron_tagger_eng'
    result = dict(tool='NLTK PerceptronTagger', nltk_version=nltk.__version__,
        model_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(model_dir.glob('*.json'))},
        native_evidence=str(evidence.resolve()),distinct_contextual_rows=total_rows,
        occurrences=total_occurrences,
        purpose='Review individual negative adjectives observed in literal text, with PARAM observations separate. POS tags nominate candidates; native review determines negative diagnostic use. No default literals or automatic merge blockers.',
        input_scope=['literal','PARAM'],tagged_rows=retained_rows,
        excluded_token_counts=dict(excluded),
        role_caveat='Current unique model captures determine survey regions, not grammatical truth. Excluded fields never enter tagger input. Each contiguous retained region is tagged separately; raw tokens are never joined or retokenized. Ambiguous/unassigned rows are counted but not tagged. REASON is outside this literal/PARAM survey. Counts of tags are token observations across contextual rows, not weighted by log occurrence frequency.',
        words=sorted(words.values(),key=lambda w:(-w['distinct_messages'],w['word'])))
    output.mkdir(parents=True,exist_ok=True)
    (output/'wording-survey.json').write_text(json.dumps(result,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
    lines=['# Scoped grammatical observations for negative-adjective review','',
           f'{total_rows:,} complete native message rows; {total_occurrences:,} occurrences.',
           'Only literal and PARAM regions enter NLTK. LOCATORs, other fields and unresolved assignments are excluded before tagging. POS labels do not establish negative meaning; native review selects recommendations.', '']
    for role in ('literal','PARAM'):
        lines.extend([f'## {role} observations','', '| Word | Tags in this region | Native example |','|---|---|---|'])
        for word in result['words']:
            if not any(t in {'JJ','JJR','JJS'} for t in word['role_tags'].get(role,{})):
                continue
            witness=next(e for e in word['examples'] if any(t in {'JJ','JJR','JJS'} for t in e['role_tags'].get(role,{})))
            sample=witness['native'].replace('|','\\|').replace('\r','').replace('\n',' / ')
            lines.append(f"| {word['word']} | {dict(word['role_tags'][role])} | {sample} |")
    lines.extend(['','## Participles requiring separate review','',
        'VBN/VBG tags may warrant contextual review for adjectival uses. These are not automatically included in the adjective list.',
        '', '| Wording | Native rows | Tags | Example |','|---|---:|---|---|'])
    for word in result['words']:
        if not any(t in {'VBN','VBG'} for t in word['tags']):
            continue
        witness=next(e for e in word['examples'] if any(t in {'VBN','VBG'} for t in e['tags']))
        sample=witness['native'].replace('|','\\|').replace('\r','').replace('\n',' / ')
        lines.append(f"| {word['word']} | {word['distinct_messages']} | {dict(word['tags'])} | {sample} |")
    (output/'ADJECTIVES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='words'},indent=2),flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-evidence',type=Path,required=True)
    parser.add_argument('--nltk-data',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    survey(args.native_evidence,args.nltk_data,args.output)
