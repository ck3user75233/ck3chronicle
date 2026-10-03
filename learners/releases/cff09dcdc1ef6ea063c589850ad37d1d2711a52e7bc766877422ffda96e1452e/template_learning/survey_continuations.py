"""Inventory native continuation shapes without classifying or splitting messages.

All nonblank continuations are included, regardless of source or vocabulary.
Single-line quoted wrappers and repeated label leads are additional review leads.
Shape labels only organize inspection; they are not a production grammar.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

from template_learning.parsers import load_parser, reference_from_manifest


def line_shape(line: str) -> str:
    """A review index retaining indentation, word leads and punctuation layout."""
    indent = re.match(r"[ \t]*", line).group()
    # Raw lines remain in the separate exact-body inventory; only the index is reduced.
    lead = line[len(indent):]
    words = re.findall(r"[A-Za-z_]+|[^\w\s]", lead)[:8]
    return repr(indent) + " " + " ".join(words)


def survey(roots: list[Path], manifest: Path, output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    discovery = subprocess.run(
        ["rg", "--files", "--hidden", "--no-ignore", *map(str, roots),
         "-g", "*error*.log", "-g", "*error*.log.*"],
        capture_output=True, text=True,
    )
    if discovery.returncode not in (0, 1, 2):
        raise RuntimeError(discovery.stderr)
    paths = sorted({Path(s).resolve() for s in discovery.stdout.splitlines()},
                   key=lambda p: ("runtime/sessions" not in p.as_posix(), str(p)))
    selected = load_parser(reference_from_manifest(manifest))
    files, unique, failures = [], {}, []
    # Hashes here deduplicate copied research input, not a runtime integrity gate.
    for path in paths:
        try:
            before = path.stat()
            payload = path.read_bytes()
            after = path.stat()
            digest = hashlib.sha256(payload).hexdigest()
            row = dict(path=str(path), sha256=digest, bytes=len(payload),
                       changed_during_read=(before.st_size, before.st_mtime_ns) !=
                       (after.st_size, after.st_mtime_ns))
            files.append(row)
            unique.setdefault(digest, []).append(row)
        except OSError as exc:
            failures.append(dict(path=str(path), error=str(exc)))
    (output / "inputs.json").write_text(json.dumps(dict(
        roots=list(map(str, roots)), discovery_errors=discovery.stderr.splitlines(),
        files=files, read_failures=failures), indent=2) + "\n", encoding="utf-8")
    totals, sources, continuations, blanks = Counter(), Counter(), Counter(), Counter()
    groups, bodies, line_leads, stats = {}, {}, {}, []
    occurrence_file = (output / "occurrences.jsonl").open("w", encoding="utf-8")
    for number, (digest, copies) in enumerate(unique.items(), 1):
        path = Path(copies[0]["path"])
        payload = path.read_bytes()
        if hashlib.sha256(payload).hexdigest() != digest:
            failures.append(dict(path=str(path), error="input changed after inventory; not surveyed"))
            continue
        try:
            raw = selected.parse_bytes(payload, source_name=str(path))
        except ValueError as exc:
            failures.append(dict(path=str(path), error=str(exc)))
            continue
        local = Counter()
        for e in raw.emissions:
            totals["emissions"] += 1
            local["emissions"] += 1
            sources[e.source_family] += 1
            body = e.body_text
            # Native LF physical lines; str.splitlines would also split CK3 controls.
            physical = body.split("\n")
            nonblank = [s for s in physical[1:] if s.strip(" \t\r")]
            multiline = e.end_line > e.start_line
            if multiline:
                totals["physical_multiline"] += 1
                if not nonblank:
                    blanks[e.source_family] += 1
                    totals["blank_only_continuation"] += 1
            wrapper = re.search(r'\bError\s*:\s*"', body) is not None
            # Broad lead: repeats of any label at a word boundary, not a list of errors.
            labels = re.findall(r"\b([A-Za-z][A-Za-z_]*(?: [A-Za-z][A-Za-z_]*){0,3}):", body)
            repeats = sorted(k for k, n in Counter(labels).items() if n > 1)
            header_like = any(re.match(r"\s*\[\d\d:\d\d", s) for s in physical[1:])
            if not (nonblank or wrapper or repeats or header_like):
                continue
            flags = []
            if nonblank:
                flags.append("nonblank_continuation")
                continuations[e.source_family] += 1
            if wrapper:
                flags.append("quoted_error_wrapper")
            if repeats:
                flags.append("repeated_label")
            if header_like:
                flags.append("header_like_continuation")
            for f in flags:
                totals[f] += 1
                local[f] += 1
            totals["candidate_emissions"] += 1
            local["candidate_emissions"] += 1
            body_id = hashlib.sha256((e.source_family + "\0" + body).encode("utf-8", "surrogateescape")).hexdigest()
            first_shape = line_shape(physical[0])
            shapes = list(dict.fromkeys(line_shape(s) for s in nonblank))
            key = json.dumps([e.source_family, first_shape, shapes], ensure_ascii=True)
            group_id = hashlib.sha256(key.encode()).hexdigest()[:16]
            ref = dict(input_sha256=digest, path=str(path), ordinal=e.ordinal,
                       start_line=e.start_line, end_line=e.end_line,
                       span=[e.span.start, e.span.end], body_span=[e.body_span.start, e.body_span.end])
            if body_id not in bodies:
                bodies[body_id] = dict(id=body_id, source=e.source_family, body=body,
                    first=ref, group=group_id, flags=flags, repeated_labels=repeats, occurrences=0)
            bodies[body_id]["occurrences"] += 1
            group = groups.setdefault(group_id, dict(id=group_id, source=e.source_family,
                first_line_shape=first_shape, continuation_shapes=shapes, flags=flags,
                occurrences=0, body_ids=set(), input_ids=set(), min_lines=None, max_lines=0))
            group["occurrences"] += 1
            group["body_ids"].add(body_id)
            group["input_ids"].add(digest)
            count = len(nonblank)
            group["min_lines"] = count if group["min_lines"] is None else min(count, group["min_lines"])
            group["max_lines"] = max(count, group["max_lines"])
            for shape in set(shapes):
                lk = (e.source_family, shape)
                item = line_leads.setdefault(lk, dict(source=e.source_family, shape=shape,
                    occurrences=0, example_body_id=body_id))
                item["occurrences"] += 1
            occurrence_file.write(json.dumps(dict(**ref, body_id=body_id, group=group_id, flags=flags)) + "\n")
        stats.append(dict(sha256=digest, path=str(path), copies=len(copies), bytes=len(payload), **local))
        print(f"Surveyed {number}/{len(unique)} unique logs; {totals['emissions']} emissions; {len(groups)} shapes", flush=True)
        del raw, payload
    occurrence_file.close()
    for g in groups.values():
        g["body_ids"] = sorted(g["body_ids"])
        g["input_ids"] = sorted(g["input_ids"])
    with (output / "bodies.jsonl").open("w", encoding="utf-8") as stream:
        for b in bodies.values():
            stream.write(json.dumps(b, ensure_ascii=True) + "\n")
    (output / "groups.json").write_text(json.dumps(sorted(groups.values(), key=lambda g: -g["occurrences"]), indent=2) + "\n", encoding="utf-8")
    (output / "line-leads.json").write_text(json.dumps(sorted(line_leads.values(), key=lambda g: (g["source"], -g["occurrences"])), indent=2) + "\n", encoding="utf-8")
    summary = dict(parser=selected.reference.to_dict(), discovered_files=len(paths),
        readable_files=len(files), unique_contents=len(unique), surveyed_logs=len(stats),
        duplicate_copies=len(files)-len(unique), unique_bytes=sum(s["bytes"] for s in stats),
        discovery_errors=discovery.stderr.splitlines(), failures=failures,
        changed_during_read=[f for f in files if f["changed_during_read"]],
        totals=dict(totals), sources=dict(sources.most_common()),
        nonblank_continuations_by_source=dict(continuations.most_common()),
        blank_only_by_source=dict(blanks.most_common()),
        distinct_candidate_bodies=len(bodies), distinct_review_shapes=len(groups),
        distinct_continuation_leads=len(line_leads), files=stats)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", action="append", required=True, type=Path)
    cli.add_argument("--parser-manifest", required=True, type=Path)
    cli.add_argument("--output", required=True, type=Path)
    args = cli.parse_args()
    result = survey(args.root, args.parser_manifest, args.output)
    print(json.dumps({k: v for k, v in result.items() if k not in ("files", "sources", "discovery_errors")}, indent=2))


if __name__ == "__main__":
    main()
