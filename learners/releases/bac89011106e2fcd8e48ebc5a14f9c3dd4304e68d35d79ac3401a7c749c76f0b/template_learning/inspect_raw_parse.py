"""Explore a genuine raw parse; observations are review leads, not pass gates.

Writes complete raw output, anomaly/outlier observations and selected native
examples to an explicitly supplied directory. Does not classify or change input.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import statistics

from template_learning.parsers import load_parser, reference_from_manifest


def inspect(log: Path, manifest: Path, output: Path) -> dict:
    parser = load_parser(reference_from_manifest(manifest))
    raw = parser.parse_file(log)
    output.mkdir(parents=True, exist_ok=True)
    raw.save_debug(output / "raw-parse.json")
    rows = []
    leads = defaultdict(list)
    chars = Counter()
    source_counts = Counter()
    suffixes = Counter()
    lengths = []
    sizes = []
    cursor = 0
    defects = []
    token_total = gap_total = 0

    def lead(kind, emission, **details):
        leads[kind].append({"ordinal": emission.ordinal, "line": emission.start_line, **details})

    for emission in raw.emissions:
        pieces = emission.pieces
        tokens = [p for p in pieces if p.kind == "token"]
        token_total += len(tokens)
        gap_total += len(pieces) - len(tokens)
        source_counts[emission.source_family] += 1
        sizes.append(emission.span.end - emission.span.start)
        lengths.append(len(tokens))
        if emission.span.start != cursor:
            defects.append({"kind": "emission gap/overlap", "ordinal": emission.ordinal})
        cursor = emission.span.end
        body = raw.read_bytes(emission.body_span)
        if b"".join(raw.read_bytes(p.span) for p in pieces) != body:
            defects.append({"kind": "body differs from token/gap reconstruction", "ordinal": emission.ordinal})
        position = emission.body_span.start
        for piece in pieces:
            if piece.span.start != position:
                defects.append({"kind": "lexical gap/overlap", "ordinal": emission.ordinal})
            position = piece.span.end
        if position != emission.span.end:
            defects.append({"kind": "lexical extent disagreement", "ordinal": emission.ordinal})
        if not emission.body_text.strip():
            lead("empty_body", emission)
        endings = re.search(rb"[\r\n]+$", body)
        suffixes[repr(endings.group() if endings else b"")] += 1
        for index, line in enumerate(emission.body_text.splitlines()[1:], 1):
            if re.match(r"^\s*\[\d{2}:\d{2}", line):
                lead("header_looking_continuation", emission, text=line, relative_line=index)
        for char, count in Counter(emission.body_text).items():
            if (ord(char) < 32 and char not in "\t\r\n") or 0xD800 <= ord(char) <= 0xDFFF or ord(char) == 127:
                chars[f"U+{ord(char):04X}"] += count
                lead("control_or_undecodable_character", emission, character=f"U+{ord(char):04X}", occurrences=count)
        # Examine actual whitespace-delimited strings beside resulting tokens.
        groups = []
        group = []
        for piece in pieces:
            if piece.kind == "gap":
                if group:
                    groups.append(group)
                    group = []
            else:
                group.append(piece)
        if group:
            groups.append(group)
        for group in groups:
            native = "".join(p.text for p in group)
            texts = [p.text for p in group]
            if len(group) > 1 and re.match(r"^[+-]\d", native):
                lead("signed_number_split", emission, native=native, tokens=texts, span=[group[0].span.start, group[-1].span.end])
            if len(group) > 1 and (native.startswith("_") or native.endswith("_")):
                lead("edge_underscore_split", emission, native=native, tokens=texts)
            if len(group) > 1 and (native.startswith(("/", "\\", "./", "../")) or native.endswith(("/", "\\"))):
                lead("edge_path_punctuation_split", emission, native=native, tokens=texts)
            if len(group) > 1 and any(re.search(r"[a-zA-Z0-9][.,:/\\_-][a-zA-Z0-9]", t) for t in texts):
                lead("internal_punctuation_with_edge_split", emission, native=native, tokens=texts)
        for token in tokens:
            if len(token.text) > 1 and all(not c.isalnum() and c != "_" for c in token.text):
                lead("multi_character_symbol_token", emission, token=token.text, span=[token.span.start, token.span.end])
            if any(c.isalnum() for c in token.text) and any(
                token.text.count(left) != token.text.count(right)
                for left, right in [("[", "]"), ("(", ")"), ("{", "}")]
            ):
                lead("unbalanced_delimiter_inside_token", emission, token=token.text,
                     span=[token.span.start, token.span.end])
        rows.append({"ordinal": emission.ordinal, "line": emission.start_line,
                     "end_line": emission.end_line, "source": emission.source_family,
                     "bytes": sizes[-1], "tokens": len(tokens),
                     "physical_lines": emission.end_line - emission.start_line + 1})

    if cursor != len(raw.source.data):
        defects.append({"kind": "final extent disagreement"})
    if b"".join(e.native_bytes() for e in raw.emissions) != raw.source.data:
        defects.append({"kind": "emissions differ from original input"})
    for row in rows:
        if source_counts[row["source"]] <= 3:
            leads["rare_source"].append(row)

    def distribution(values):
        ordered = sorted(values)
        return {"min": min(values), "median": statistics.median(values),
                "p95": ordered[int((len(values) - 1) * .95)], "max": max(values)}

    report = {
        "source": str(log.resolve()), "parser": parser.reference.to_dict(),
        "bytes": len(raw.source.data), "emissions": len(rows),
        "physical_lines": len(raw.source.data.splitlines()),
        "multiline_emissions": sum(r["physical_lines"] > 1 for r in rows),
        "tokens": token_total, "gaps": gap_total,
        "byte_accounting_disagreements": defects,
        "empty_bodies": len(leads["empty_body"]),
        "header_looking_continuations": len(leads["header_looking_continuation"]),
        "edge_underscore_splits": len(leads["edge_underscore_split"]),
        "edge_path_punctuation_splits": len(leads["edge_path_punctuation_split"]),
        "bytes_per_emission": distribution(sizes), "tokens_per_emission": distribution(lengths),
        "source_counts": dict(source_counts.most_common()),
        "control_character_occurrences": dict(chars), "native_ending_forms": dict(suffixes),
        "longest_emissions": sorted(rows, key=lambda r: r["bytes"], reverse=True)[:8],
        "review_leads": {key: {"occurrences": len(items),
                               "emissions": len({x['ordinal'] for x in items}),
                               "examples": items[:20]} for key, items in leads.items()},
    }
    # Select actual evidence across source families and outlier shapes. Limits
    # affect the review display only; full parsing/output above is never capped.
    selected = {}
    sample_queries = [
        (lambda e: "has_graphical_celtic_culture_group_trigger" in e.body_text, "Inline and enclosing locations"),
        (lambda e: e.body_text.count("Unknown trigger: kinslayer_3, near line:") >= 3, "Repeated errors in one emission"),
        (lambda e: "capital_county.kingdom trigger" in e.body_text, "Dotted key and complete script-location tail"),
        (lambda e: "set_knight_status effect" in e.body_text and e.body_text.count("file:") == 3, "Three trace frames in one emission"),
        (lambda e: "\x15weak" in e.body_text, "Native control characters"),
    ]
    for query, reason in sample_queries:
        match = next((e for e in raw.emissions if query(e)), None)
        if match:
            selected[match.ordinal] = [reason]
    for kind, items in leads.items():
        for item in items[:2]:
            selected.setdefault(item["ordinal"], []).append(kind)
    for row in report["longest_emissions"][:3]:
        selected.setdefault(row["ordinal"], []).append("Longest emissions")
    for family in source_counts:
        emission = next(e for e in raw.emissions if e.source_family == family)
        selected.setdefault(emission.ordinal, []).append("Source-family sample")
    examples = []
    for ordinal, reasons in selected.items():
        e = raw.emissions[ordinal]
        examples.append({"ordinal": ordinal, "line": e.start_line, "end_line": e.end_line,
                         "source": e.source_tag, "reasons": reasons,
                         "span": [e.span.start, e.span.end], "body_span": [e.body_span.start, e.body_span.end],
                         "raw": e.decoded_text, "body": e.body_text,
                         "pieces": [{"text": p.text, "kind": p.kind, "start": p.span.start, "end": p.span.end}
                                    for p in e.pieces]})
    (output / "observations.json").write_text(json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    (output / "review-examples.json").write_text(json.dumps(examples, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    (output / "all-review-leads.json").write_text(json.dumps(leads, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--log", required=True, type=Path)
    cli.add_argument("--parser-manifest", required=True, type=Path)
    cli.add_argument("--output-dir", required=True, type=Path)
    args = cli.parse_args()
    report = inspect(args.log, args.parser_manifest, args.output_dir)
    print(json.dumps(report, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
