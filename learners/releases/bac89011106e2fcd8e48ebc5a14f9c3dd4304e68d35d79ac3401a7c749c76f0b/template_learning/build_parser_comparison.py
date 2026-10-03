"""Build a deliberately selected native before/after parser review pack.

The historical learner is executed only to describe previous inputs. No training,
model promotion, caller migration or production processing is performed.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
from dataclasses import replace
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import types

from template_learning.parsers import load_parser, reference_from_manifest
from ck3chronicle.parser.log_blocks import iter_log_blocks
from ck3chronicle.pipeline.domain import SourceProvenance
from ck3chronicle.pipeline.emissions import iter_emissions
from ck3chronicle.pipeline.diagnostics import recover_diagnostics
from ck3chronicle.pipeline.normalization import normalize_for_match


def select_cases(survey: Path, random_examples: Path):
    pool = [json.loads(line) for line in (survey / "bodies.jsonl").open()]
    representatives = json.loads((survey / "review-examples.json").read_text())
    by_title = {r["title"]: r["evidence"] for r in representatives}
    chosen, used = [], set()

    def add(row, group, reason):
        identity = (row["source"], row["body"])
        if identity in used:
            return False
        used.add(identity)
        chosen.append(dict(group=group, selection_reason=reason, evidence=row))
        return True

    def inner(row):
        return row["body"].lstrip().removeprefix('Error: "').rsplit('" in file:', 1)[0]

    multi = [r for r in pool if r["source"] == "pdx_persistent_reader.cpp" and "\n" in inner(r)]
    group = "Multiple messages in one emission"
    for title in ("Repeated Unknown trigger messages", "Repeated Unexpected token messages",
                  "Repeated Unknown effect messages", "Repeated Malformed token messages",
                  "Variable text inside the error introduction", "Different error types in one wrapper",
                  "Longest observed repeated-message wrapper"):
        add(by_title[title], group, title + "; compare previous and current message boundaries and shared wrapper ranges.")
    add(min((r for r in multi if len(inner(r).split("\n")) == 449), key=lambda r: r["id"]),
        group, "449-message batch: check repeated occurrences and shared storage without duplicating the wrapper.")
    candidates = sorted((r for r in multi if len(inner(r).split("\n")) <= 16), key=lambda r: (len(r["body"]), r["id"]))
    seen_shapes = set()
    for r in candidates:
        shape = (len(inner(r).split("\n")), inner(r).split(":", 1)[0])
        if shape in seen_shapes:
            continue
        seen_shapes.add(shape)
        add(r, group, f"Sibling boundary variation: {shape[0]} entries introduced by {shape[1]!r}; wording is not a splitting rule.")
        if len(chosen) == 30:
            break
    for r in candidates:
        if len(chosen) == 30:
            break
        add(r, group, "Additional distinct sibling text/location values; verify message-local literals and the enclosing context separately.")
    assert len(chosen) == 30

    group = "One message inside a location wrapper"
    singles = [r for r in pool if r["source"] == "pdx_persistent_reader.cpp" and "\n" not in inner(r)]
    requests = [
        ("Expansion annotation stays with the message; its closing punctuation can share an emission token with the wrapper quote.", lambda r: "(expanded from file:" in r["body"]),
        ("A second expansion annotation uses a different native filename or empty filename.", lambda r: "(expanded from file:" in r["body"]),
        ("Named-value message: compare the old preprocessing with preserved literals and location.", lambda r: inner(r).startswith("Named value not found")),
        ("Scoped-pointer message: the same wrapper applies to a different error introduction.", lambda r: inner(r).startswith("Scoped pointer")),
        ("Quoted holy-site key is retained inside its message.", lambda r: inner(r).startswith("Unknown holy site")),
        ("Named-value expression is part of the native message, not a parser-supplied slot.", lambda r: inner(r).startswith("Failed to read named value or literal")),
        ("Long explanatory introduction remains complete inside one located message.", lambda r: "are both defined" in inner(r)),
        ("Empty wrapper filename remains an exact shared value with its quote literals.", lambda r: 'in file: ""' in r["body"]),
        ("A single Unknown trigger has the same framing contract as a sibling in a repeated wrapper.", lambda r: inner(r).startswith("Unknown trigger:")),
        ("A single Unexpected token retains its own near-line ending and parent filename.", lambda r: inner(r).startswith("Unexpected token:")),
    ]
    for reason, predicate in requests:
        match = next(r for r in sorted(singles, key=lambda r: (len(r["body"]), r["id"]))
                     if predicate(r) and (r["source"], r["body"]) not in used)
        add(match, group, reason)
    assert len(chosen) == 40

    group = "Multiline single script error"
    scripts = [r for r in pool if r["source"] == "jomini_script_system.cpp"]
    for title in ("Script error with the longest observed trace", "Tooltip/description script-error variant",
                  "Multiline script reason with several conditions", "Actor and recipient details within a script reason",
                  "Building-state dump within a script reason", "Quoted newline within a script reason"):
        add(by_title[title], group, title + "; preserve failure/reason as one message and compare native trace/literal retention.")
    for needle, reason in [
        ("Script location: Unknown", "Unknown location is literal message content; it does not remove the error or introduce another message."),
        ("Error: Event target link", "Plain Error field without L1/L2 brackets; same single-message envelope."),
        ("Error: add_title_law effect", "Reason continues to a closing bracket on another physical line."),
        ("Error: trigger_situation_catalyst effect", "Multiline reason has an empty-looking final line that still belongs to the message."),
        ("Error: vassal_contract_set_obligation_level effect", "Formatted failure reason contains identifiers and embedded control characters."),
        ("Error: activate_struggle_catalyst effect", "Another multiline reason introduction uses the same message boundary contract."),
    ]:
        match = next(r for r in sorted(scripts, key=lambda r: (len(r["body"]), r["id"]))
                     if needle in r["body"] and (r["source"], r["body"]) not in used)
        add(match, group, reason)
    seen_leads = set()
    for r in sorted(scripts, key=lambda r: (len(r["body"]), r["id"])):
        error = r["body"].split("  Error: ", 1)[-1].split("\n", 1)[0]
        lead = error.split(" [", 1)[0]
        if lead in seen_leads:
            continue
        seen_leads.add(lead)
        add(r, group, "Distinct native Error field; compare complete failure/reason, internal key punctuation and preserved location tail.")
        if len(chosen) == 70:
            break
    assert len(chosen) == 70

    group = "Other multiline single-message forms"
    for source, count in [("jomini_effect_impl.cpp", 4), ("activity_type.cpp", 3),
                          ("event.cpp", 2), ("faction.cpp", 2), ("character_commands.cpp", 2),
                          ("pdx_data_localize.cpp", 1), ("pdx_text_formatter.cpp", 1)]:
        candidates = [r for r in pool if r["source"] == source and "nonblank_continuation" in r["flags"]]
        if source == "jomini_effect_impl.cpp":
            add(by_title["Non-script-system stack trace"], group, "Stack trace from another source remains attached to its single message.")
            count -= 1
        for r in sorted(candidates, key=lambda r: (len(r["body"]), r["id"])):
            if add(r, group, "Observed " + source + " continuation: retain explanation, details or quoted value as part of one message; inspect all whitespace and control characters."):
                count -= 1
            if count == 0:
                break
    assert len(chosen) == 85

    # Retain selected familiar examples for direct continuity with the earlier review.
    old = json.loads(random_examples.read_text())
    indexes = [1, 4, 6, 8, 11, 12, 14, 15, 16, 18, 20, 21, 22, 23, 25]
    for number in indexes:
        r = old["samples"][number - 1]
        add(dict(source=r["source"].rsplit(":", 1)[0], body=r["raw"],
                 first=dict(path=old["source"], start_line=r["line"])),
            "Single-line diagnostics and lexical changes",
            f"Earlier random example {number}, deliberately retained here for punctuation, path/key, location, naming or whitespace comparison.")
    assert len(chosen) == len(used) == 100
    return chosen


class Original:
    def __init__(self, data):
        self.data = data

    def read_bytes(self, span):
        return self.data[span.start:span.end]


def build(root: Path, survey: Path, random_examples: Path, manifest: Path, output: Path, baseline: str):
    output.mkdir(parents=True, exist_ok=True)
    cases_dir = output / "cases"
    cases_dir.mkdir(exist_ok=True)
    choices = select_cases(survey, random_examples)
    old_source = subprocess.run(["git", "show", baseline + ":tools/template_learning/learn_error_templates.py"],
        cwd=root, check=True, capture_output=True).stdout
    old = types.ModuleType("_parser_comparison_historical_learner")
    old.__file__ = str(root / "tools/template_learning/learn_error_templates.py")
    sys.modules[old.__name__] = old
    exec(compile(old_source, old.__file__, "exec"), old.__dict__)
    parser = load_parser(reference_from_manifest(manifest))
    by_path = defaultdict(list)
    for i, choice in enumerate(choices, 1):
        choice["number"] = i
        by_path[choice["evidence"]["first"]["path"]].append(choice)
    complete = []
    inputs = []

    def span(s):
        return [s.start, s.end]

    for path_text, selected in by_path.items():
        path = Path(path_text)
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        inputs.append(dict(path=str(path), sha256=digest, bytes=len(data)))
        raw = parser.parse_bytes(data, source_name=str(path))
        selected_lines = {r["evidence"]["first"]["start_line"] for r in selected}
        emitted = {e.start_line: e for e in raw.emissions if e.start_line in selected_lines}
        blocks = {b.line_number: b for b in iter_log_blocks(path, log_relpath="error.log") if b.line_number in selected_lines}
        provenance = SourceProvenance(path.parent.name, "error.log", digest)
        with path.open("rb") as stream:
            previous = {e.start_line: e for e in iter_emissions(stream, provenance=provenance, original=Original(data))
                        if e.start_line in selected_lines}
        # Execute the real serializer on selected emissions in their original
        # source context. Export exact emission nodes; the review package itself
        # is not a complete-log save_debug document or a new parser schema.
        doc = replace(raw, emissions=tuple(emitted.values())).debug_document()
        nodes = {e["start_line"]: e for e in doc["emissions"]}
        del doc
        for choice in selected:
            ref = choice["evidence"]["first"]
            e = emitted[ref["start_line"]]
            assert e.body_text == choice["evidence"]["body"]
            if "input_sha256" in ref:
                assert digest == ref["input_sha256"]
            b, prev = blocks[e.start_line], previous[e.start_line]
            children = recover_diagnostics(prev)
            before = []
            for child in children:
                view = normalize_for_match(child)
                before.append(dict(ordinal=child.ordinal, text=child.decoded_text,
                    local_spans=[span(s) for s in child.local_spans], shared_spans=[span(s) for s in child.shared_spans],
                    tokens=[dict(text=t.text, joined_to_previous=t.joined_to_previous,
                        origins=[dict(span=span(o.span), scope=o.scope) for o in t.origins]) for t in view.tokens]))
            units = old.semantic_units(b.source_family, old.block_message(b))
            recovery = e.recovery
            resolved = [dict(ordinal=m.ordinal, span=span(m.span), text=m.text,
                pieces=[dict(span=span(p.span), text=p.text, kind=p.kind) for p in m.pieces]) for m in recovery.messages]
            shared = [dict(json_path=f"recovery.shared_spans[{i}]", span=span(s), text=raw.read_text(s))
                      for i, s in enumerate(recovery.shared_spans)]
            order = sorted([dict(kind="shared", ordinal=i, span=row["span"], text=row["text"]) for i,row in enumerate(shared)] +
                           [dict(kind="message", ordinal=row["ordinal"], span=row["span"], text=row["text"]) for row in resolved],
                           key=lambda r:r["span"][0])
            assert b"".join(row["text"].encode("utf-8", "surrogateescape") for row in order) == e.native_bytes()
            changes = []
            if len(before) != len(resolved):
                changes.append(f"Message count: previous pipeline {len(before)} → current parser {len(resolved)}. Iterate recovered messages; do not classify the whole emission as one error.")
            else:
                changes.append(f"Message count remains {len(resolved)}; compare message boundaries, native content and associated shared ranges below.")
            missing = [m["ordinal"] for m in resolved if not any(
                s[0] < m["span"][1] and m["span"][0] < s[1]
                for previous_message in before for s in previous_message["local_spans"])]
            if missing:
                changes.append(f"Current message ordinal(s) {missing} have no overlapping previous local message range. Inspect the previous shared ranges: content preserved there was not recovered as its own error.")
            if [r["text"] for r in before] != [r["text"] for r in resolved]:
                changes.append("Message text differs in framing, retained content and/or whitespace. Current message text is the exact native byte slice; inspect the previous output alongside it.")
            if [[t["text"] for t in r["tokens"]] for r in before] != [[p["text"] for p in r["pieces"] if p["kind"]=="token"] for r in resolved]:
                changes.append("Token sequences differ. Use selected-parser pieces and byte ranges; old matching token indexes are not interchangeable.")
            if recovery.structure == "located-message-wrapper":
                changes.append("Header, wrapper filename/location and separator line endings are in emission.recovery.shared_spans; message spans contain only each complete enclosed entry.")
            crossings = []
            boundaries = {n for m in recovery.messages for n in (m.span.start,m.span.end)}
            for p in e.pieces:
                if any(p.span.start < n < p.span.end for n in boundaries):
                    crossings.append(dict(span=span(p.span),text=p.text))
            if crossings:
                changes.append("An emission lexical piece crosses a message boundary. Retrieve the message range and its pieces; filtering whole emission tokens would lose or add punctuation.")
            case = dict(number=choice["number"], group=choice["group"], selection_reason=choice["selection_reason"],
                caller_changes=changes, evidence=dict(path=str(path), sha256=digest,
                    start_line=e.start_line,end_line=e.end_line,emission_span=span(e.span)),
                native_emission=e.decoded_text, native_base64=base64.b64encode(e.native_bytes()).decode(),
                previous_lexer=dict(header_line=b.header_line,continuation_lines=b.continuation_lines),
                previous_learner=[dict(text=u,tokens=list(old.tokenize(u))) for u in units],
                previous_pipeline=dict(emission_span=span(prev.span),header_span=span(prev.header_span),messages=before),
                current_parser_json=nodes[e.start_line],
                resolved_current=dict(messages=resolved,shared=shared,ordered_ranges=order,crossing_pieces=crossings))
            complete.append(case)
        print(f"Compared {len(complete)}/100 cases",flush=True)
    complete.sort(key=lambda r:r["number"])
    sources = ["src/ck3chronicle/parser/log_blocks.py", "src/ck3chronicle/pipeline/emissions.py",
               "src/ck3chronicle/pipeline/diagnostics.py", "src/ck3chronicle/pipeline/normalization.py", "src/ck3chronicle/pipeline/domain.py"]
    report = dict(parser=parser.reference.to_dict(), previous_learner_commit=baseline,
        previous_learner_sha256=hashlib.sha256(old_source).hexdigest(),
        previous_pipeline_sources={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sources},
        selection="Purposeful caller-impact selection; 30 multiple-message, 10 single-message wrapper, 30 script, 15 other multiline, 15 lexical/ordinary cases. Not random or frequency representative.",
        inputs=inputs, cases=complete)
    (output/"comparison-100.json").write_text(json.dumps(report,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
    compressed=base64.b64encode(gzip.compress(json.dumps(report,ensure_ascii=True,separators=(",",":")).encode(),mtime=0)).decode()
    (output/"comparison-data.b64").write_text(compressed,encoding="ascii")
    index=["# 100 native parser comparisons", "",report["selection"],"",
        "Each case shows the exact original emission, previous pipeline messages/tokens, previous learner processed patterns, the current parser's actual emission JSON, and a separately labelled readable resolution of its native ranges. All data is generated from the stated code paths, not hand-written output.","",
        "The current JSON node is emitted by RawParse.debug_document. A complete debug document also contains format, parser, source_name and original_base64 at the top level. These per-case review files are excerpts with original file byte positions; they are not standalone complete-log debug files.","",
        "Previous pipeline means the current unmigrated pipeline reader/recovery/tokenizer, with source hashes in comparison-100.json. Previous learner means the historical learner at the stated commit. Their transformations are separately labelled.","",
        "## Shared ranges, precisely", "",
        "recovery.shared_spans appears once in the emission JSON. recovery.messages contains only each message's ordinal and byte span. Both address the same original source bytes. Shared ranges include header/wrapper content and separator whitespace. There is no shared_text field in the parser JSON: the readable text shown by this report is obtained with raw.read_text(span). In memory, all messages reference the same shared_spans tuple.","",
        "Sort the message and shared ranges by byte start to reconstruct the emission. Do not concatenate all messages followed by all shared ranges. A single-message body generally shares only its header; a wrapped message also shares its wrapper and line separators.","",
        "## Index", "", "| Case | Group | Previous → current messages | Why selected |", "|---|---|---:|---|"]
    for c in complete:
        number=c["number"]; name=f"{number:03}.md"
        index.append(f"| [{number:03}](cases/{name}) | {c['group']} | {len(c['previous_pipeline']['messages'])} → {len(c['resolved_current']['messages'])} | {c['selection_reason'].replace('|','/')} |")
        md=[f"# Case {number:03}: {c['group']}","",f"[Index](../INDEX.md) · [Exact review JSON]({number:03}.json)","",
            c["selection_reason"],"",f"Native file: `{c['evidence']['path']}`, lines {c['evidence']['start_line']}–{c['evidence']['end_line']}; original emission bytes `{c['evidence']['emission_span']}`.","",
            "## Caller changes", "", *["- "+change for change in c["caller_changes"]],"",
            "## Original native emission", "", "```text",c["native_emission"].replace("\r","\\r").replace("\x15","\\u0015").replace("\x16","\\u0016"),"```","",
            "Display exposes carriage returns and CK3 controls; the JSON string/base64 preserves the exact bytes.","",
            "## Previous pipeline output", "", "```json",json.dumps(c["previous_pipeline"],ensure_ascii=True,indent=2),"```","",
            "## Previous learner processed input", "", "```json",json.dumps(c["previous_learner"],ensure_ascii=True,indent=2),"```","",
            "## Current parser output: exact emission node", "", "```json",json.dumps(c["current_parser_json"],ensure_ascii=True,indent=2),"```","",
            "## Current ranges resolved for inspection (report view)", "", "```json",json.dumps(c["resolved_current"],ensure_ascii=True,indent=2),"```",""]
        (cases_dir/name).write_text("\n".join(md),encoding="utf-8")
        (cases_dir/f"{number:03}.json").write_text(json.dumps(c,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
    (output/"INDEX.md").write_text("\n".join(index)+"\n",encoding="utf-8")
    print(json.dumps(dict(cases=len(complete),groups=dict(Counter(c["group"] for c in complete)),
                         compressed_bytes=len(compressed),changed_message_counts=sum(len(c["previous_pipeline"]["messages"])!=len(c["resolved_current"]["messages"]) for c in complete)),indent=2))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--survey",type=Path,required=True)
    p.add_argument("--random-examples",type=Path,required=True)
    p.add_argument("--parser-manifest",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--previous-learner-commit",required=True)
    a=p.parse_args()
    build(Path(__file__).resolve().parents[2],a.survey,a.random_examples,a.parser_manifest,a.output,a.previous_learner_commit)


if __name__=="__main__":
    main()
