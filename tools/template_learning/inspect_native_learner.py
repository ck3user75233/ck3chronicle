"""Inspect a native learner build, byte captures, burst invariance and registry parity."""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
from template_learning import artifacts, inventory, records
from template_learning import incremental_template_registry as registry
from template_learning.clustering import cluster_source_records
from template_learning.matching_primitives import SLOT_TYPES
from template_learning.matching_defaults import match_pattern
from template_learning.parsers import load_parser, reference_from_manifest
from template_learning.research_matching import evaluate_records


def inspect(log, manifest, output):
    output.mkdir(parents=True,exist_ok=True)
    parser=load_parser(reference_from_manifest(manifest))
    digest=inventory.sha256_file(log)
    stat=log.stat()
    item=inventory.ProtectedLog(digest,"protected",log.resolve(),digest,stat.st_size,stat.st_mtime_ns)
    grouped,stats=records.collect_records([item],parser=parser)
    raw=parser.parse_file(log)
    original=raw.source.data
    expected={(e.ordinal,m.ordinal):(e,m) for e in raw.emissions for m in e.recovery.messages}
    actual=set()
    for source,rows in grouped.items():
        for record in rows:
            assert source==record.source_family
            assert "".join(t for _,t in record.pieces)==record.text
            for o in record.native_occurrences:
                key=o["emission_ordinal"],o["message_ordinal"]
                assert key not in actual
                actual.add(key)
                e,m=expected[key]
                assert e.source_family==source and m.text==record.text
                assert original[slice(*o["span"])].decode("utf-8","surrogateescape")==record.text
                if o["context_id"]:
                    context=record.contexts[o["context_id"]]
                    for name,span in o["context_spans"].items():
                        assert original[slice(*span)].decode("utf-8","surrogateescape")==context[name]["text"]
    assert actual==set(expected)
    model,evidence=artifacts.build_model(grouped,stats,parser=parser)
    bundle=artifacts.write_bundle(output/"candidates",model,evidence,parser=parser,
        build_command=[sys.executable,"-m","template_learning.inspect_native_learner",*sys.argv[1:]])
    templates=registry.all_patterns(model)
    capture_counts=Counter()
    unsupported=[]
    for row in evidence["records"]:
        selected=[(templates[m["template_id"]],m["captures"],row["native"]) for m in row["matches"]]
        if row["outcome"] != "full":
            unsupported.append(row["record_id"])
        for template,captures,native in selected:
            by_name={c["name"]:c for c in captures}
            reconstructed=[]
            for part in template["parts"]:
                if part["kind"]=="literal":
                    reconstructed.append(part["text"])
                else:
                    capture=by_name[part["name"]]
                    capture_counts[capture["type"]]+=1
                    assert capture["type"] in SLOT_TYPES
                    if capture["value"] is not None:
                        a,b=capture["span"]
                        assert row["native"].encode("utf-8","surrogateescape")[a:b].decode("utf-8","surrogateescape")==capture["value"]
                        reconstructed.extend([part["prefix"],capture["value"],part["suffix"]])
            assert "".join(reconstructed)==native
    # Replay genuine occurrences at greater weight, introducing no new text.
    for source,rows in grouped.items():
        burst=[replace(r,native_occurrences=r.native_occurrences*3) for r in rows]
        rerun=cluster_source_records(source,burst)
        assert [c.template_id for c in rerun]==[t["template_id"] for t in model["templates"] if t["source_family"]==source]
    # Exercise the real cache/build path in isolated research state.
    state=output/"registry"
    state.mkdir(exist_ok=True)
    feature=registry.feature_from_log(item,parser=parser)
    registry.validate_feature(feature,digest,parser=parser)
    cache=registry.feature_cache_path(state,digest,parser=parser)
    registry.write_json(cache,feature)
    entry=dict(sha256=digest,role="training",bytes=stat.st_size,
        observed_paths=[dict(kind="protected",path=str(log.resolve()),evidence_id=digest)],
        feature_caches={registry.feature_key(parser):dict(path=cache.relative_to(state).as_posix(),
            sha256=inventory.sha256_file(cache))})
    fresh=registry.empty_registry()
    fresh["evidence"][digest]=entry
    registry.write_json(state/"registry.json",fresh)
    revision=registry.build_revision(state,parser=parser)
    assert revision["revision_id"]==model["revision_id"]
    assert (Path(revision["model_path"])).read_bytes()==(bundle/"empirical_template_model.json").read_bytes()
    for field,value in (("record_scope","emission"),("schema_version",2)):
        invalid={**feature,field:value}
        try:
            registry.validate_feature(invalid,digest,parser=parser)
        except ValueError:
            pass
        else:
            raise AssertionError("old cache accepted")
    # Load the actual package in a separate interpreter, including the bundled
    # implementation, without requiring a pipeline migration.
    subprocess.run([sys.executable,"-I","-B","-c",
        "from template_learning.artifacts import load_bundle; import sys; m,p=load_bundle(sys.argv[1]); r=p.parse_file(sys.argv[2]); assert sum(len(e.recovery.messages) for e in r.emissions)==m['summary']['messages']",
        str(bundle.resolve()),str(log.resolve())],check=True)
    outcomes,matched,unresolved=evaluate_records(model,grouped,stats)
    (output/"research-matches.json").write_bytes(artifacts.canonical_bytes(dict(summary=outcomes,records=matched,unresolved=unresolved)))
    results=dict(bundle=str(bundle.resolve()),native_input=str(log.resolve()),sha256=digest,
        summary=model["summary"],capture_types=dict(capture_counts),unsupported_members=unsupported,
        exact_native_occurrence_accounting=True,exact_capture_and_literal_reconstruction=True,
        burst_invariant_sources=len(grouped),registry_model_bytes_identical=True,
        incompatible_cache_rejected=True,independent_bundle_replay=True,
        research_outcomes=outcomes,parser_sha256=parser.reference.sha256)
    (output/"inspection.json").write_bytes(artifacts.canonical_bytes(results))
    print(json.dumps(results,ensure_ascii=True,indent=2))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--log",type=Path,required=True)
    p.add_argument("--parser-manifest",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    inspect(a.log,a.parser_manifest,a.output)


if __name__=="__main__":
    main()
