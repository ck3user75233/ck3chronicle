"""Inventory genuine date and short-character spellings in complete retained logs."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

from template_learning.location_candidate_experiment import save

MONTHS = 'January February March April May June July August September October November December Jan Feb Mar Apr Jun Jul Aug Sep Oct Nov Dec'.split()
DATE = re.compile(r'(?<![\w.])(?P<day>[0-9]{1,2})(?P<sep>[- ])(?P<month>'+ '|'.join(MONTHS) +r')(?P=sep)(?P<year>[0-9]+):')
ENDING = re.compile(r'\((?P<id>[0-9]+), (?P<place>[^()\r\n]+)\)')
HEADER = re.compile(r'^\[[^\]]+\](?:\[[^\]]+\])?\[(?P<source>[^\]]+)\]:')
WORD = r'[^\W\d_]+(?:[\x27\u2019-][^\W\d_]+)*'
NAME_TAIL = re.compile(r'(?P<name>'+WORD+r'(?: '+WORD+r')*) $')
TITLED = re.compile(r'(?P<name>'+WORD+r'(?: '+WORD+r')*) of (?P<title>'+WORD+r'(?: '+WORD+r')*)')


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--inventory',type=Path,required=True)
    cli.add_argument('--output',type=Path,required=True)
    args=cli.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    inventory=json.loads(args.inventory.read_text())
    counts=Counter();dates={};shorts={};receivers={};titles={};full=Counter()
    def keep(pool,key,source,text,row,line,**extra):
        item=pool.setdefault(key,dict(source=source,text=text,count=0,example=dict(path=row['snapshot'],sha256=row['sha256'],line=line),**extra))
        item['count']+=1
    for no,row in enumerate(inventory['inputs']):
        raw=Path(row['snapshot']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==row['sha256']
        source='unheaded'
        for number,line in enumerate(raw.decode('utf-8','surrogateescape').split('\n'),1):
            line=line.removesuffix('\r')
            header=HEADER.match(line)
            if header:
                source=header['source'].rsplit(':',1)[0]
                line=line[header.end():]
            counts['lines']+=1
            if 'Internal ID' in line: full[source]+=line.count('Internal ID')
            for date in DATE.finditer(line):
                tail=line[date.end():]
                family=re.sub(r'^ .*?\([0-9]+, [^()]+\): ', '<CHARACTER_ID_SHORT>: ',tail)
                family=re.sub(r'receiver is .*?, default location is .*','receiver is <NAME>, default location is <PLACE>',family)
                family=re.sub(r'[0-9]+','<N>',family)
                keep(dates,(source,line),source,line,row,number,date=date.group(),year_digits=len(date['year']),separator=date['sep'],family=family)
            endings=list(ENDING.finditer(line))
            for end in endings:
                name_match=NAME_TAIL.search(line[:end.start()])
                name=name_match['name'] if name_match else None
                # Longest suffix of capitalized words: inventory hypothesis only.
                words=name.split(' ') if name else []
                words=list(reversed(list(__import__('itertools').takewhile(lambda w:w[0].isupper(),reversed(words)))))
                name=' '.join(words) or None
                keep(shorts,(source,line,end.start()),source,line,row,number,ending=end.group(),place=end['place'],name=name,name_words=len(words),preceding=line[max(0,end.start()-160):end.start()],following=line[end.end():])
            for receiver in re.finditer(r'receiver is (?P<value>.*?)(?=, default location is |$)',line):
                keep(receivers,(source,line),source,line,row,number,value=receiver['value'])
            # Survey possible plain name-of-place expressions outside any labelled
            # full-ID line or numeric short-ID line. These are hypotheses, not slots.
            if 'Internal ID' not in line and not endings and ' of ' in line:
                for m in TITLED.finditer(line):
                    words=m['name'].split();suffix=[]
                    for word in reversed(words):
                        if not word[0].isupper(): break
                        suffix.insert(0,word)
                    title=[]
                    for word in m['title'].split():
                        if not word[0].isupper(): break
                        title.append(word)
                    if suffix and title:
                        keep(titles,(source,line,m.start()),source,line,row,number,value=' '.join(suffix)+' of '+' '.join(title))
        print('Scanned',no+1,'/',len(inventory['inputs']),flush=True)
    result=dict(scope=inventory['scope'],logs=len(inventory['inputs']),bytes=sum(r['bytes'] for r in inventory['inputs']),counts=counts,
                dates=list(dates.values()),short_endings=list(shorts.values()),receivers=list(receivers.values()),plain_titled_candidates=list(titles.values()),full_id_markers_by_source=full)
    save(args.output/'corpus.json',result)
    print(json.dumps({k:dict(distinct=len(result[k]),occurrences=sum(r['count'] for r in result[k])) for k in ['dates','short_endings','receivers','plain_titled_candidates']},indent=2))


if __name__=='__main__':main()
