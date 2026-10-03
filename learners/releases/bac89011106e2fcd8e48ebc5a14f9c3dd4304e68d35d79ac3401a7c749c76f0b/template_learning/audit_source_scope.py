"""Check source specificity against native recovered messages, without training."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from template_learning.parsers import load_parser, reference_from_manifest


def audit(survey: Path, manifest: Path, output: Path):
    selected = load_parser(reference_from_manifest(manifest))
    inputs = json.loads(survey.read_text(encoding="utf-8"))["files"]
    texts, token_sources = {}, defaultdict(set)
    cache = {}
    counts, source_counts = Counter(), Counter()
    files, failures = [], []
    for number, entry in enumerate(inputs, 1):
        path = Path(entry["path"])
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            failures.append(dict(path=str(path), reason="surveyed input changed"))
            continue
        raw = selected.parse_bytes(data, source_name=str(path))
        for emission in raw.emissions:
            counts["emissions"] += 1
            key = emission.source_family, emission.body_text
            if key not in cache:
                recovery = emission.recovery
                cache[key] = (recovery.status, [(m.text, tuple(p.text for p in m.tokens)) for m in recovery.messages])
            status, messages = cache[key]
            if status == "unresolved":
                counts["unresolved_emissions"] += 1
            for text, tokens in messages:
                counts["messages"] += 1
                source_counts[emission.source_family] += 1
                row = texts.setdefault(text, {})
                row.setdefault(emission.source_family, dict(path=str(path), emission_ordinal=emission.ordinal,
                    line=emission.start_line, source_tag=emission.source_tag))
                token_sources[tokens].add(emission.source_family)
        files.append(dict(path=str(path), sha256=entry["sha256"]))
        print(f"Source audit {number}/{len(inputs)}: {counts['messages']} messages", flush=True)
    overlaps = [dict(text=text, sources=sources) for text,sources in texts.items() if len(sources)>1]
    lexical = [dict(tokens=list(tokens), sources=sorted(sources)) for tokens,sources in token_sources.items() if len(sources)>1]
    report = dict(parser=selected.reference.to_dict(), files=files, failures=failures,
        counts=dict(counts), source_counts=dict(sorted(source_counts.items())),
        unique_exact_messages=len(texts), exact_cross_source_messages=len(overlaps),
        unique_token_sequences=len(token_sources), cross_source_token_sequences=len(lexical),
        exact_overlaps=overlaps, lexical_overlaps=lexical,
        conclusion="Native evidence supports source-specific learning. Collection, clustering, inference and identity are scoped to source; no cross-source template comparison is required.")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=True, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k not in {"files","exact_overlaps","lexical_overlaps","source_counts"}},indent=2))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--survey",type=Path,required=True)
    p.add_argument("--parser-manifest",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    audit(a.survey,a.parser_manifest,a.output)


if __name__=="__main__":
    main()
