"""Read-only native-message census for compound-identifier investigation.

This inventories evidence, not identifier types. No learner/model rules run.
Whitespace-free runs are search units only; their raw pieces remain distinct.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time

from template_learning.inventory import protected_error_logs
from template_learning.parsers import load_parser, reference_from_manifest
from template_learning.records import identity


def survey(root, manifest, output):
    started=time.perf_counter()
    parser=load_parser(reference_from_manifest(manifest))
    logs,duplicates=protected_error_logs(root)
    rows={};totals=Counter();inputs=[]
    output.mkdir(parents=True,exist_ok=True)
    for number,log in enumerate(logs,1):
        raw=parser.parse_file(log.path)
        assert hashlib.sha256(raw.source.data).hexdigest()==log.sha256
        counts=Counter(emissions=len(raw.emissions))
        for emission in raw.emissions:
            recovery=emission.recovery
            if recovery.status!='recovered':
                counts['unresolved_emissions']+=1
                continue
            for message in recovery.messages:
                counts['messages']+=1
                text=message.text;key=(emission.source_family,text)
                if key not in rows:
                    pieces=[(p.kind,p.text) for p in message.pieces]
                    assert ''.join(t for _,t in pieces)==text
                    rows[key]=dict(record_id=identity(key),source=emission.source_family,
                        native=text,pieces=pieces,occurrences=0,logs={},
                        example=dict(log_sha256=log.sha256,path=str(log.path.resolve()),
                            emission_ordinal=emission.ordinal,message_ordinal=message.ordinal,
                            source_tag=emission.source_tag,span=[message.span.start,message.span.end]))
                row=rows[key];row['occurrences']+=1
                row['logs'][log.sha256]=row['logs'].get(log.sha256,0)+1
        totals.update(counts)
        inputs.append(dict(path=str(log.path.resolve()),sha256=log.sha256,bytes=log.bytes,**counts))
        print(f'{number}/{len(logs)}: {counts["messages"]} messages; {len(rows)} distinct source/message pairs',flush=True)
    with (output/'native-messages.jsonl').open('w',encoding='utf-8') as stream:
        for key,row in sorted(rows.items()):stream.write(json.dumps(row,ensure_ascii=True)+'\n')
    summary=dict(parser=parser.reference.to_dict(),logs=inputs,duplicate_logs=duplicates,
        totals=dict(totals),distinct_messages=len(rows),seconds=time.perf_counter()-started,
        survey_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        scope='Every recovered message in each complete distinct protected log. Counts are message occurrences, not unique emissions or independent learning examples. No model inference or recognition-rule changes.')
    (output/'census.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in {'logs','parser','duplicate_logs'}},indent=2))


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--root',type=Path,required=True)
    cli.add_argument('--parser-manifest',type=Path,required=True)
    cli.add_argument('--output',type=Path,required=True)
    args=cli.parse_args()
    survey(args.root,args.parser_manifest,args.output)
