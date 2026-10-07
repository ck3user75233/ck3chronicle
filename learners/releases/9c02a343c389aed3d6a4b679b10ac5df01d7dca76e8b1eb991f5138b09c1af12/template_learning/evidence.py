"""Native learner input, shared with independent pipeline consumers.

Emissions and recovered messages retain their native order and ranges here.
Aggregation, feature selection and template learning belong to later stages.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from template_learning.parsers import SelectedParser, load_parser, reference_from_manifest


def read_evidence(path: Path | str, *, parser: SelectedParser):
    return parser.parse_file(path)


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--log", required=True, type=Path)
    cli.add_argument("--parser-manifest", required=True, type=Path)
    cli.add_argument("--raw-output", required=True, type=Path)
    args = cli.parse_args()
    parser = load_parser(reference_from_manifest(args.parser_manifest))
    result = read_evidence(args.log, parser=parser)
    result.save_debug(args.raw_output)
    print(f"Wrote raw parse with message recovery: {args.raw_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
