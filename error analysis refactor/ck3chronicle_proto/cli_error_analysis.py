from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .issue_aggregator import top_files
from .log_parser import parse_error_log, parse_script_error_blocks
from .override_resolver import OverrideResolver
from .reports import build_error_file_analysis_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prototype modular CK3 error-file analysis.")
    parser.add_argument("--log", help="Path to CK3 error.log")
    parser.add_argument("--out", help="Output report path")
    parser.add_argument("--top", type=int, default=25, help="Top files to include")
    parser.add_argument("--all-errors", action="store_true", help="Parse all timestamped error blocks, not only script-system errors")
    parser.add_argument("--use-sdk", action="store_true", help="Use ck3raven SDK for log path and override resolution")
    parser.add_argument("--our-submod", default="Gambo+EC724 Submod", help="Name of local submod to treat as ours")
    args = parser.parse_args(argv)

    playset_name = "unknown"
    log_source = args.log or "unknown"
    source_provider = None

    if args.use_sdk:
        from .sdk_adapter import CK3SDKSourceProvider, default_log_path_from_sdk, load_ck3_sdk

        sdk = load_ck3_sdk()
        playset_name = getattr(sdk, "playset_name", "unknown")
        source_provider = CK3SDKSourceProvider(sdk)
        if not args.log:
            log_path, log_source = default_log_path_from_sdk(sdk)
        else:
            log_path = Path(args.log)
    else:
        if not args.log:
            parser.error("--log is required unless --use-sdk is provided")
        log_path = Path(args.log)

    if not log_path.exists():
        print(f"ERROR: log not found: {log_path}", file=sys.stderr)
        return 1

    if args.all_errors:
        issues = parse_error_log(log_path, source_log=log_source, script_only=False)
    else:
        issues = parse_script_error_blocks(log_path, source_log=log_source)

    source_resolutions = {}
    if source_provider is not None:
        resolver = OverrideResolver(source_provider, our_submod_name=args.our_submod)
        for bucket in top_files(issues, limit=args.top):
            source_resolutions[bucket.file_path] = resolver.resolve(bucket.file_path)

    report = build_error_file_analysis_report(
        issues,
        playset_name=playset_name,
        log_source=log_source,
        source_resolutions=source_resolutions,
        top_n=args.top,
    )

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"Report written to: {out_path}")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
