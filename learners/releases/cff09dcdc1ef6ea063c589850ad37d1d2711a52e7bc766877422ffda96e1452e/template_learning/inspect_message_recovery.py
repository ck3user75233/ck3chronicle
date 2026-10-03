"""Replay a surveyed native corpus and inspect automatic message recovery.

Checks byte accounting on every emission, lexical retrieval on each distinct
recovered message, and saves owner-review examples. Does not train, classify,
write SQL or change the supplied logs. Corpus counts are observations, not quotas.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from template_learning.parsers import load_parser, reference_from_manifest


def inspect(survey_path: Path, examples_path: Path, manifest: Path, output: Path):
    selected = load_parser(reference_from_manifest(manifest))
    survey = json.loads(survey_path.read_text(encoding="utf-8"))
    examples = json.loads(examples_path.read_text(encoding="utf-8"))
    wanted = defaultdict(dict)
    for example in examples:
        ref = example["evidence"]["first"]
        wanted[ref["path"]][ref["ordinal"]] = example
    output.mkdir(parents=True, exist_ok=True)
    structures, statuses, sizes = Counter(), Counter(), Counter()
    single_sources, multiple_sources, unresolved_sources = Counter(), Counter(), Counter()
    totals = Counter()
    seen_messages, seen_unknowns = set(), set()
    reviewed, files, input_failures = [], [], []
    unknown_file = (output / "unresolved.jsonl").open("w", encoding="utf-8")

    def bounds(span):
        return [span.start, span.end]

    for index, entry in enumerate(survey["files"], 1):
        path = Path(entry["path"])
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            input_failures.append(dict(path=str(path), reason="surveyed input changed"))
            continue
        raw = selected.parse_bytes(data, source_name=str(path))
        reconstructed = hashlib.sha256()
        cursor = 0
        local = Counter()
        for emission in raw.emissions:
            recovery = emission.recovery
            assert emission.span.start == cursor
            position = cursor
            for span in recovery.ordered_spans:
                assert span.start == position and span.end <= emission.span.end
                reconstructed.update(raw.read_bytes(span))
                position = span.end
            assert position == emission.span.end
            cursor = position
            totals["emissions"] += 1
            local["emissions"] += 1
            statuses[recovery.status] += 1
            structures[recovery.structure or "unresolved"] += 1
            if recovery.status == "recovered":
                assert recovery.messages and not recovery.unresolved_spans
                sizes[len(recovery.messages)] += 1
                totals["messages"] += len(recovery.messages)
                local["messages"] += len(recovery.messages)
                (multiple_sources if len(recovery.messages) > 1 else single_sources)[emission.source_family] += 1
            else:
                assert not recovery.messages and recovery.unresolved_spans
                unresolved_sources[emission.source_family] += 1
                digest = hashlib.sha256(emission.native_bytes()).hexdigest()
                if digest not in seen_unknowns:
                    seen_unknowns.add(digest)
                    unknown_file.write(json.dumps(dict(path=str(path), line=emission.start_line,
                        span=bounds(emission.span), reason=recovery.reason,
                        body=emission.body_text), ensure_ascii=True) + "\n")
            for message in recovery.messages:
                assert message.parent is emission
                assert message.shared_spans is recovery.shared_spans
                native = message.native_bytes()
                digest = hashlib.sha256(native).hexdigest()
                if digest not in seen_messages:
                    seen_messages.add(digest)
                    pieces = message.pieces
                    assert b"".join(raw.read_bytes(piece.span) for piece in pieces) == native
                    assert "".join(piece.text for piece in pieces).encode("utf-8", "surrogateescape") == native
            if emission.ordinal in wanted[str(path)]:
                example = wanted[str(path)][emission.ordinal]
                assert emission.body_text == example["evidence"]["body"]
                reviewed.append(dict(title=example["title"], interpretation=example["interpretation"],
                    path=str(path), line=emission.start_line, end_line=emission.end_line,
                    emission_span=bounds(emission.span), body=emission.body_text,
                    status=recovery.status, structure=recovery.structure, reason=recovery.reason,
                    shared_spans=[bounds(s) for s in recovery.shared_spans],
                    shared_text=[raw.read_text(s) for s in recovery.shared_spans],
                    messages=[dict(ordinal=m.ordinal, span=bounds(m.span), text=m.text,
                                   tokens=[piece.text for piece in m.tokens])
                              for m in recovery.messages]))
        assert cursor == len(data) and reconstructed.hexdigest() == entry["sha256"]
        files.append(dict(path=str(path), sha256=entry["sha256"], bytes=len(data), **local))
        print(f"Inspected {index}/{len(survey['files'])} logs; {totals['emissions']} emissions; "
              f"{totals['messages']} messages; {statuses['unresolved']} unresolved", flush=True)
    unknown_file.close()
    assert len(reviewed) == len(examples), "not all review examples were replayed"
    summary = dict(parser=selected.reference.to_dict(), survey=str(survey_path.resolve()),
        surveyed_logs=len(files), input_failures=input_failures, counts=dict(totals),
        statuses=dict(statuses), structures=dict(structures), messages_per_emission=dict(sorted(sizes.items())),
        multiple_message_sources=dict(multiple_sources), single_message_sources=dict(single_sources),
        unresolved_sources=dict(unresolved_sources), distinct_message_lexical_roundtrips=len(seen_messages),
        reconstruction="every emission partition and every complete input reconstructed exactly",
        review_examples=len(reviewed), files=files)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (output / "examples.json").write_text(json.dumps(reviewed, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    markdown = ["# Native message recovery: inspected outputs", "",
        "Actual parser output for the 23 surveyed native examples. Single-message bodies retain failure/reason and all associated content. Wrapped siblings share the original header, wrapper and separators by range. All positions are original absolute byte offsets.", ""]
    for number, row in enumerate(reviewed, 1):
        markdown.extend([f"## {number}. {row['title']}", "", row["interpretation"], "",
            f"`{row['path']}` lines {row['line']}–{row['end_line']}. "
            f"Outcome: **{row['status']}**, `{row['structure']}`, **{len(row['messages'])} message(s)**.", "",
            f"Emission range: `{row['emission_span']}`. Shared content is recorded once in examples.json.", ""])
        messages = row["messages"]
        displayed = messages if len(messages) <= 10 else [*messages[:3], messages[-1]]
        if len(displayed) != len(messages):
            markdown.extend(["Display shows the first three and last message; every message, token and shared range is retained in examples.json.", ""])
        for message in displayed:
            markdown.extend([f"Message {message['ordinal']} — bytes `{message['span']}`:", "",
                "```json", json.dumps(message["text"], ensure_ascii=True), "```", ""])
    (output / "RECOVERED_EXAMPLES.md").write_text("\n".join(markdown), encoding="utf-8")
    return summary


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--survey-summary", required=True, type=Path)
    cli.add_argument("--review-examples", required=True, type=Path)
    cli.add_argument("--parser-manifest", required=True, type=Path)
    cli.add_argument("--output", required=True, type=Path)
    args = cli.parse_args()
    result = inspect(args.survey_summary, args.review_examples, args.parser_manifest, args.output)
    print(json.dumps({key: value for key, value in result.items() if key not in ("files", "single_message_sources")}, indent=2))


if __name__ == "__main__":
    main()
