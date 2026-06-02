# ck3chronicle Modular Refactor Prototype — All-in-One


---

# File: `README.md`

# ck3chronicle Modular Refactor Prototype

This package separates the functionality from the original CK3 error-analysis scripts into cleaner modules.

It is intended as a **prototype / promotion target**, not a guaranteed drop-in replacement until tested inside your ck3raven/ck3lens environment.

## What this refactor separates

The original scripts mixed several responsibilities:

```text
raw error.log parsing
→ script-error extraction
→ grouping by file
→ override-chain walking
→ diff checks
→ recommendation writing
→ final text report
```

This refactor splits those responsibilities into modules:

```text
ck3chronicle_proto/
  models.py              # dataclasses / canonical issue schema
  paths.py               # game-relative path helpers
  normalizers.py         # signatures, categories, severity/confidence
  log_parser.py          # raw log → canonical issue records
  issue_aggregator.py    # issue records → counts by file/category/signature
  override_resolver.py   # file path → override chain / winner / submod status
  fixability.py          # issue + source context → actionability score
  reports.py             # canonical records + enrichment → human report
  sdk_adapter.py         # optional ck3raven SDK adapter
  cli_error_analysis.py  # command-line composition layer
```

## Core rule

Final reports should not parse raw logs directly.

Instead:

```text
raw log
→ log_parser.parse_error_log()
→ canonical issue records
→ issue_aggregator
→ override_resolver
→ fixability
→ reports
```

## Minimal usage outside ck3raven

```bash
python -m ck3chronicle_proto.cli_error_analysis --log "path/to/error.log" --out report.txt
```

Without the ck3raven SDK, override resolution will be unavailable unless you provide source roots programmatically.

## Intended usage inside ck3raven

Inside ck3raven, use the SDK adapter:

```bash
python -m ck3chronicle_proto.cli_error_analysis --use-sdk
```

The adapter expects:

```text
~/.ck3raven/wip/sdk/ck3_sdk.py
```

and reads:

```text
root:user_docs/logs/error.log
root:ck3raven_data/wip/.log_path_override
```

matching the old scripts.

## What this preserves from the original report

The report still supports:

- top files by script-error count
- sample error messages
- override chain
- winning mod/file
- our submod override status
- diff vs original
- diff vs predecessor
- stale patch warnings
- cautious recommendation language

## Wording change

The original script used:

```text
ERRORS OWNED BY
```

This refactor uses:

```text
CURRENT WINNING FILE
```

and avoids claiming true root-cause ownership.

## Suggested promotion path

1. Put these modules under `root:repo/ck3chronicle/src/ck3chronicle/`.
2. Keep copied logs/reports under `root:ck3raven_data/wip/ck3chronicle/`.
3. Add fixture tests using known CK3 error-log snippets.
4. Have future agents extend extractors only if they emit `CanonicalIssue`.


---

# File: `ck3chronicle_proto/__init__.py`

```python
"""Prototype modular refactor for ck3chronicle error analysis."""

from .models import CanonicalIssue, ScriptLocation, SourceInstance, SourceResolution
from .log_parser import parse_error_log, parse_script_error_blocks

```


---

# File: `ck3chronicle_proto/cli_error_analysis.py`

```python
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

```


---

# File: `ck3chronicle_proto/fixability.py`

```python
from __future__ import annotations

from .issue_aggregator import FileIssueBucket
from .models import FixabilityAssessment, SourceResolution

SEVERITY_WEIGHT = {
    "Fatal": 50,
    "High": 35,
    "Medium": 20,
    "Low": 8,
    "Noise": 0,
    "Unknown": 5,
}


def assess_fixability(
    bucket: FileIssueBucket,
    source_resolution: SourceResolution | None = None,
    *,
    is_new_or_regression: bool = False,
    crash_adjacent: bool = False,
    known_noise: bool = False,
) -> FixabilityAssessment:
    score = 0
    reasons: list[str] = []

    highest = bucket.highest_severity
    score += SEVERITY_WEIGHT.get(highest, 0)
    reasons.append(f"highest severity={highest}")

    count_weight = min(bucket.count, 100) // 5
    score += count_weight
    reasons.append(f"{bucket.count} issue occurrence(s)")

    if is_new_or_regression:
        score += 20
        reasons.append("new/regression")

    if crash_adjacent:
        score += 25
        reasons.append("crash-adjacent")

    if source_resolution and source_resolution.winning_instance:
        winner = source_resolution.winning_instance
        if source_resolution.our_submod_instance and source_resolution.our_submod_instance == winner:
            score += 25
            reasons.append("our submod is winning")
        elif source_resolution.our_submod_instance and source_resolution.our_submod_instance != winner:
            score += 10
            reasons.append("our submod has override but is not winning")
        elif winner.source_type != "base_game":
            score -= 8
            reasons.append("upstream mod is winning")
        elif winner.source_type == "base_game":
            score -= 4
            reasons.append("base game is winning")

        if source_resolution.diff_vs_predecessor and not source_resolution.diff_vs_predecessor.stale_warning:
            score += 5
            reasons.append("small/non-stale predecessor diff")
        if source_resolution.diff_vs_original and source_resolution.diff_vs_original.stale_warning:
            score += 15
            reasons.append("possible stale patch")

    if known_noise:
        score -= 30
        reasons.append("known noise")

    score = max(score, 0)

    recommendation, confidence = recommend(bucket, source_resolution)

    return FixabilityAssessment(
        file_path=bucket.file_path,
        score=score,
        recommendation=recommendation,
        confidence=confidence,  # type: ignore[arg-type]
        reason="; ".join(reasons),
        highest_severity=highest,  # type: ignore[arg-type]
        issue_count=bucket.count,
        source_resolution=source_resolution,
    )


def recommend(bucket: FileIssueBucket, source_resolution: SourceResolution | None) -> tuple[str, str]:
    if not source_resolution or not source_resolution.winning_instance:
        return ("Inspect the referenced file/path if available; source ownership could not be resolved.", "Low")

    winner = source_resolution.winning_instance

    if source_resolution.our_submod_instance and source_resolution.our_submod_instance == winner:
        if source_resolution.diff_vs_original and source_resolution.diff_vs_original.stale_warning:
            return (
                "Our submod is winning, but the diff suggests a possible stale override. Review against original/predecessor before editing.",
                "High",
            )
        return ("Inspect/fix directly in our submod override.", "High")

    if source_resolution.our_submod_instance and source_resolution.our_submod_instance != winner:
        return (
            f"Our override exists but {winner.source_name} wins later in load order. Inspect load order or create a later-loading patch.",
            "Medium",
        )

    if winner.source_type == "base_game":
        return (
            "Base game file is winning. Inspect caller chain and modded data before creating a submod override.",
            "Medium",
        )

    return (
        f"{winner.source_name} is winning and our submod does not override this file. Assess whether to patch in our submod or report upstream.",
        "Medium",
    )

```


---

# File: `ck3chronicle_proto/issue_aggregator.py`

```python
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable

from .models import CanonicalIssue


@dataclass(slots=True)
class FileIssueBucket:
    file_path: str
    issues: list[CanonicalIssue] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.issues)

    @property
    def highest_severity(self) -> str:
        order = {"Fatal": 5, "High": 4, "Medium": 3, "Low": 2, "Noise": 1, "Unknown": 0}
        if not self.issues:
            return "Unknown"
        return max((i.severity for i in self.issues), key=lambda s: order.get(s, 0))

    def sample_messages(self, limit: int = 5) -> list[str]:
        seen: set[str] = set()
        samples: list[str] = []
        for issue in self.issues:
            key = issue.message[:160]
            if key not in seen:
                seen.add(key)
                samples.append(issue.message[:240])
            if len(samples) >= limit:
                break
        return samples


def group_by_primary_file(issues: Iterable[CanonicalIssue]) -> dict[str, FileIssueBucket]:
    buckets: dict[str, FileIssueBucket] = {}
    for issue in issues:
        file_path = issue.primary_file or (issue.extracted_file_paths[0] if issue.extracted_file_paths else "unknown")
        if file_path not in buckets:
            buckets[file_path] = FileIssueBucket(file_path=file_path)
        buckets[file_path].issues.append(issue)
    return buckets


def top_files(issues: Iterable[CanonicalIssue], limit: int = 25) -> list[FileIssueBucket]:
    buckets = group_by_primary_file(issues)
    return sorted(buckets.values(), key=lambda b: b.count, reverse=True)[:limit]


def signature_counts(issues: Iterable[CanonicalIssue]) -> Counter[str]:
    return Counter(issue.normalized_signature for issue in issues)


def category_counts(issues: Iterable[CanonicalIssue]) -> Counter[str]:
    return Counter(issue.category for issue in issues)

```


---

# File: `ck3chronicle_proto/log_parser.py`

```python
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from .models import CanonicalIssue, ScriptLocation
from .normalizers import classify_issue, normalized_signature, raw_hash
from .paths import to_game_relative_path

LINE_START = re.compile(r"^\[\d{2}:\d{2}:\d{2}\]")
SCRIPT_ERR = re.compile(r"Script system error!", re.IGNORECASE)

RE_ERROR_LINE = re.compile(r"^\s+Error:\s*(.+)", re.IGNORECASE | re.MULTILINE)
RE_LOCATION = re.compile(
    r"(?:Script location:\s*)?file:\s+(?P<file>\S+)\s+line:\s*(?P<line>\d+)(?:\s+\((?P<symbol>[^)]+)\))?",
    re.IGNORECASE,
)
RE_SIMPLE_FILE = re.compile(r"file:\s+\"?(?P<file>[^\"\s]+)\"?\s+near line:\s*(?P<line>\d+)", re.IGNORECASE)


def split_timestamped_blocks(lines: Iterable[str]) -> list[tuple[int, int, str]]:
    """Split CK3 log text into timestamp-started blocks."""

    blocks: list[tuple[int, int, str]] = []
    current: list[str] = []
    start_line: int | None = None
    last_line = 0

    for idx, line in enumerate(lines, 1):
        line = line.rstrip("\n")
        if LINE_START.match(line):
            if current and start_line is not None:
                blocks.append((start_line, last_line, "\n".join(current)))
            current = [line]
            start_line = idx
        else:
            if current:
                current.append(line)
        last_line = idx

    if current and start_line is not None:
        blocks.append((start_line, last_line, "\n".join(current)))

    return blocks


def read_log_lines(path: Path) -> list[str]:
    return path.read_bytes().decode("utf-8", errors="replace").splitlines()


def extract_message(block: str) -> str:
    match = RE_ERROR_LINE.search(block)
    if match:
        return match.group(1).strip()
    lines = block.splitlines()
    return lines[0].strip() if lines else ""


def extract_locations(block: str) -> list[ScriptLocation]:
    locations: list[ScriptLocation] = []

    for match in RE_LOCATION.finditer(block):
        raw_file = match.group("file")
        rel_file = to_game_relative_path(raw_file)
        line = int(match.group("line")) if match.group("line") else None
        symbol = match.group("symbol")
        locations.append(ScriptLocation(file=rel_file, line=line, symbol=symbol, raw=match.group(0).strip()))

    if not locations:
        for match in RE_SIMPLE_FILE.finditer(block):
            raw_file = match.group("file")
            rel_file = to_game_relative_path(raw_file)
            line = int(match.group("line")) if match.group("line") else None
            locations.append(ScriptLocation(file=rel_file, line=line, raw=match.group(0).strip()))

    return locations


def parse_block(block: str, *, source_log: str, first_line: int | None = None, last_line: int | None = None) -> CanonicalIssue:
    message = extract_message(block)
    locations = extract_locations(block)
    primary = locations[0] if locations else ScriptLocation()

    category, severity, confidence = classify_issue(block)

    extracted = []
    for loc in locations:
        if loc.file and loc.file not in extracted:
            extracted.append(loc.file)

    return CanonicalIssue(
        schema_version="ck3chronicle.issue.v1",
        source_log=source_log,
        raw_block_hash=raw_hash(block),
        normalized_signature=normalized_signature(block),
        category=category,
        severity=severity,
        confidence=confidence,
        message=message,
        raw_sample=block[:2000],
        first_line_number=first_line,
        last_line_number=last_line,
        primary_file=primary.file,
        primary_line=primary.line,
        primary_symbol=primary.symbol,
        call_stack=locations,
        extracted_file_paths=extracted,
    )


def parse_error_log(log: str | Path | Iterable[str], *, source_log: str = "error.log", script_only: bool = False) -> list[CanonicalIssue]:
    """Parse a CK3 error log into canonical issue records."""

    if isinstance(log, Path):
        lines = read_log_lines(log)
    elif isinstance(log, str) and "\n" not in log and Path(log).exists():
        lines = read_log_lines(Path(log))
    elif isinstance(log, str):
        lines = log.splitlines()
    else:
        lines = list(log)

    issues: list[CanonicalIssue] = []
    for first, last, block in split_timestamped_blocks(lines):
        if script_only and not SCRIPT_ERR.search(block):
            continue
        if not block.strip():
            continue
        issues.append(parse_block(block, source_log=source_log, first_line=first, last_line=last))

    return issues


def parse_script_error_blocks(log: str | Path | Iterable[str], *, source_log: str = "error.log") -> list[CanonicalIssue]:
    return parse_error_log(log, source_log=source_log, script_only=True)

```


---

# File: `ck3chronicle_proto/models.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

Severity = Literal["Fatal", "High", "Medium", "Low", "Noise", "Unknown"]
Confidence = Literal["High", "Medium", "Low"]
SourceType = Literal["base_game", "workshop_mod", "local_mod", "unknown"]


@dataclass(slots=True)
class ScriptLocation:
    """A CK3 script location frame extracted from a log block."""

    file: str | None = None
    line: int | None = None
    symbol: str | None = None
    raw: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CanonicalIssue:
    """Canonical issue record emitted by log parsers/extractors.

    Reports and analytics should consume this object, not raw log text.
    """

    schema_version: str
    source_log: str
    raw_block_hash: str
    normalized_signature: str
    category: str
    severity: Severity
    confidence: Confidence
    message: str
    raw_sample: str
    first_line_number: int | None = None
    last_line_number: int | None = None
    primary_file: str | None = None
    primary_line: int | None = None
    primary_symbol: str | None = None
    call_stack: list[ScriptLocation] = field(default_factory=list)
    extracted_file_paths: list[str] = field(default_factory=list)
    occurrence_count: int = 1

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["call_stack"] = [loc.to_dict() if hasattr(loc, "to_dict") else loc for loc in self.call_stack]
        return data


@dataclass(slots=True)
class SourceInstance:
    """One discovered instance of a game-relative file in base game or a mod."""

    source_name: str
    load_order: int
    path: Path
    modified_at: datetime
    source_type: SourceType = "unknown"

    @property
    def exists(self) -> bool:
        return self.path.exists()

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_name": self.source_name,
            "load_order": self.load_order,
            "path": str(self.path),
            "modified_at": self.modified_at.isoformat(timespec="minutes"),
            "source_type": self.source_type,
        }


@dataclass(slots=True)
class DiffSummary:
    added: int = 0
    removed: int = 0
    stale_warning: bool = False
    compared_to: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SourceResolution:
    """Override/source enrichment for a game-relative file path."""

    file_path: str
    instances: list[SourceInstance] = field(default_factory=list)
    winning_instance: SourceInstance | None = None
    our_submod_name: str | None = None
    our_submod_instance: SourceInstance | None = None
    our_submod_override: bool = False
    diff_vs_original: DiffSummary | None = None
    diff_vs_predecessor: DiffSummary | None = None
    recently_modified_cutoff_days: int = 10
    confidence: Confidence = "Low"
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_path": self.file_path,
            "instances": [i.to_dict() for i in self.instances],
            "winning_instance": self.winning_instance.to_dict() if self.winning_instance else None,
            "our_submod_name": self.our_submod_name,
            "our_submod_instance": self.our_submod_instance.to_dict() if self.our_submod_instance else None,
            "our_submod_override": self.our_submod_override,
            "diff_vs_original": self.diff_vs_original.to_dict() if self.diff_vs_original else None,
            "diff_vs_predecessor": self.diff_vs_predecessor.to_dict() if self.diff_vs_predecessor else None,
            "recently_modified_cutoff_days": self.recently_modified_cutoff_days,
            "confidence": self.confidence,
            "reason": self.reason,
        }


@dataclass(slots=True)
class FixabilityAssessment:
    file_path: str
    score: int
    recommendation: str
    confidence: Confidence
    reason: str
    highest_severity: Severity = "Unknown"
    issue_count: int = 0
    source_resolution: SourceResolution | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_path": self.file_path,
            "score": self.score,
            "recommendation": self.recommendation,
            "confidence": self.confidence,
            "reason": self.reason,
            "highest_severity": self.highest_severity,
            "issue_count": self.issue_count,
            "source_resolution": self.source_resolution.to_dict() if self.source_resolution else None,
        }

```


---

# File: `ck3chronicle_proto/normalizers.py`

```python
from __future__ import annotations

import hashlib
import re

from .models import Confidence, Severity

VOLATILE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bline:\s*\d+\b", re.I), "line:<N>"),
    (re.compile(r"\bline\s+\d+\b", re.I), "line <N>"),
    (re.compile(r"\bnear line:\s*\d+\b", re.I), "near line:<N>"),
    (re.compile(r"\bcolumn:\s*\d+\b", re.I), "column:<N>"),
    (re.compile(r"\bInternal ID:?\s*-?\d+\b", re.I), "Internal ID:<ID>"),
    (re.compile(r"\bHistorical ID\s+[A-Za-z0-9_\-]+\b", re.I), "Historical ID:<ID>"),
    (re.compile(r"\bCharacter\s*-\s*-?\d+\b", re.I), "Character-<ID>"),
    (re.compile(r"\bCulture\s*-\s*-?\d+\b", re.I), "Culture-<ID>"),
    (re.compile(r"\bAccolade\s*-\s*-?\d+\b", re.I), "Accolade-<ID>"),
    (re.compile(r"\bTask_contract\s*-\s*-?\d+\b", re.I), "Task_contract-<ID>"),
    (re.compile(r"\bargs#\d+\b", re.I), "args#<ID>"),
    (re.compile(r"\bhash#\d+\b", re.I), "hash#<ID>"),
    (re.compile(r"0x[a-fA-F0-9]+"), "<HEX>"),
]

CLASSIFIERS: list[tuple[str, Severity, Confidence, re.Pattern[str]]] = [
    ("Syntax / Structural", "Fatal", "High", re.compile(r"Unexpected token|Failed to read key reference|Invalid date string|unbalanced brace|Error parsing", re.I)),
    ("Scope Mismatch", "High", "High", re.compile(r"Wrong scope|Inconsistent .* scopes|expected character|expected title|expected province|scope type", re.I)),
    ("Script Execution", "High", "High", re.compile(r"Script system error|PostValidate|Failed context switch|Scoped object.*not valid|returned an unset scope|Failed to fetch", re.I)),
    ("Missing Reference", "High", "High", re.compile(r"Unknown trigger|Unknown effect|Invalid database object|Cannot find|not found|does not exist|Undefined event target|Failed to find", re.I)),
    ("Localization", "Low", "High", re.compile(r"Duplicate localization key|missing localization|Unrecognized loc key|Unknown loc key|hash collision|Unlocalized text|Key is missing localization", re.I)),
    ("Asset / Graphics", "Low", "Medium", re.compile(r"Duplicate texture|pdxmesh|mesh|DDS|mipmap|3d-type|material|shader|texture streaming|type_icon|icon .*doesn.t exist", re.I)),
    ("GUI / Interface", "Medium", "Medium", re.compile(r"gui/|Widget cannot|animation|data property|pdx_gui", re.I)),
    ("Mod Descriptor / Metadata", "Low", "High", re.compile(r"Invalid supported_version|descriptor", re.I)),
    ("Database Conflict", "Medium", "Medium", re.compile(r"database_conflicts|defined multiple times|only one version will be loaded|overridden", re.I)),
    ("Engine / System", "Low", "Medium", re.compile(r"audio|FMOD|travel plan|succession order|AI tried", re.I)),
]


def raw_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def normalize_text(text: str) -> str:
    result = text
    for pattern, replacement in VOLATILE_PATTERNS:
        result = pattern.sub(replacement, result)
    result = re.sub(r"[ \t]+", " ", result)
    return result.strip()


def normalized_signature(text: str) -> str:
    return raw_hash(normalize_text(text))


def classify_issue(text: str) -> tuple[str, Severity, Confidence]:
    for category, severity, confidence, pattern in CLASSIFIERS:
        if pattern.search(text):
            return category, severity, confidence
    return "Unclassified", "Unknown", "Low"

```


---

# File: `ck3chronicle_proto/override_resolver.py`

```python
from __future__ import annotations

import difflib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol

from .models import DiffSummary, SourceInstance, SourceResolution, SourceType
from .paths import safe_read_lines


class SourceProvider(Protocol):
    """Protocol used by OverrideResolver."""

    def iter_instances(self, rel_path: str) -> list[SourceInstance]:
        ...


@dataclass(slots=True)
class OverrideResolver:
    source_provider: SourceProvider
    our_submod_name: str = "Gambo+EC724 Submod"
    recent_days: int = 10

    def resolve(self, rel_path: str) -> SourceResolution:
        instances = sorted(self.source_provider.iter_instances(rel_path), key=lambda i: i.load_order)
        resolution = SourceResolution(
            file_path=rel_path,
            instances=instances,
            our_submod_name=self.our_submod_name,
            recently_modified_cutoff_days=self.recent_days,
        )

        if not instances:
            resolution.confidence = "Low"
            resolution.reason = "No matching file instances found in configured sources."
            return resolution

        winner = instances[-1]
        our_inst = next((i for i in instances if i.source_name == self.our_submod_name), None)

        resolution.winning_instance = winner
        resolution.our_submod_instance = our_inst
        resolution.our_submod_override = our_inst is not None

        if our_inst:
            original = instances[0]
            resolution.diff_vs_original = diff_summary(original, our_inst)
            our_idx = instances.index(our_inst)
            if our_idx > 0:
                predecessor = instances[our_idx - 1]
                if predecessor.path != our_inst.path:
                    resolution.diff_vs_predecessor = diff_summary(predecessor, our_inst)

        resolution.confidence = "High"
        if our_inst and our_inst == winner:
            resolution.reason = "Our submod has the winning override for this file."
        elif our_inst and our_inst != winner:
            resolution.reason = f"Our submod has an override, but {winner.source_name} wins later in load order."
        elif winner.source_type == "base_game":
            resolution.reason = "Base game file is winning; root cause may still be modded caller/data."
            resolution.confidence = "Medium"
        else:
            resolution.reason = f"{winner.source_name} is winning and our submod does not override this file."
            resolution.confidence = "Medium"

        return resolution


def diff_summary(a: SourceInstance, b: SourceInstance) -> DiffSummary:
    a_lines = safe_read_lines(a.path)
    b_lines = safe_read_lines(b.path)
    diff = list(difflib.unified_diff(a_lines, b_lines, lineterm=""))
    added = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
    return DiffSummary(
        added=added,
        removed=removed,
        stale_warning=removed > 50 and removed > added * 1.5,
        compared_to=a.source_name,
    )


class FilesystemSourceProvider:
    """Simple source provider for tests or non-SDK usage.

    Sources should be provided in load-order ascending.
    """

    def __init__(self, sources: list[tuple[str, int, Path, SourceType]]):
        self.sources = sources

    def iter_instances(self, rel_path: str) -> list[SourceInstance]:
        found: list[SourceInstance] = []
        for source_name, load_order, root, source_type in self.sources:
            path = root / rel_path
            if path.exists():
                found.append(
                    SourceInstance(
                        source_name=source_name,
                        load_order=load_order,
                        path=path,
                        modified_at=datetime.fromtimestamp(path.stat().st_mtime),
                        source_type=source_type,
                    )
                )
        return sorted(found, key=lambda i: i.load_order)

```


---

# File: `ck3chronicle_proto/paths.py`

```python
from __future__ import annotations

from pathlib import Path

GAME_RELATIVE_MARKERS = (
    "common/",
    "events/",
    "decisions/",
    "history/",
    "localization/",
    "gfx/",
    "gui/",
    "map_data/",
    "on_action/",
    "scripted_effects/",
    "scripted_triggers/",
    "cultures/",
    "religions/",
    "characters/",
    "dynasties/",
)


def to_game_relative_path(path: str | None) -> str | None:
    """Return the game-relative portion of a CK3 file path."""

    if not path:
        return None
    p = str(path).replace("\\", "/")
    for marker in GAME_RELATIVE_MARKERS:
        idx = p.find(marker)
        if idx != -1:
            return p[idx:]

    parts = [part for part in p.split("/") if part]
    return "/".join(parts[-2:]) if len(parts) >= 2 else p


def safe_read_lines(path: Path) -> list[str]:
    try:
        return path.read_bytes().decode("utf-8-sig", errors="replace").splitlines()
    except Exception:
        return []

```


---

# File: `ck3chronicle_proto/reports.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Callable

from .fixability import assess_fixability
from .issue_aggregator import top_files
from .models import CanonicalIssue, FixabilityAssessment, SourceResolution


def build_error_file_analysis_report(
    issues: Iterable[CanonicalIssue],
    *,
    playset_name: str = "unknown",
    log_source: str = "unknown",
    source_resolutions: dict[str, SourceResolution] | None = None,
    top_n: int = 25,
) -> str:
    issues = list(issues)
    source_resolutions = source_resolutions or {}

    buckets = top_files(issues, limit=top_n)
    assessments: list[FixabilityAssessment] = []
    for bucket in buckets:
        assessments.append(
            assess_fixability(
                bucket,
                source_resolutions.get(bucket.file_path),
                known_noise=all(i.severity in ("Low", "Noise") for i in bucket.issues),
            )
        )

    by_count = sorted(zip(buckets, assessments), key=lambda pair: pair[0].count, reverse=True)

    out: list[str] = []
    W = out.append
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    W("=" * 78)
    W("ERROR FILE DEEP ANALYSIS")
    W(f"Generated  : {now}")
    W(f"Playset    : {playset_name}")
    W(f"Log source : {log_source}")
    W(f"Top files  : {top_n}  |  Total canonical issues: {len(issues):,}")
    W("=" * 78)
    W("")
    W("RANK  ERRORS  SCORE  FILE")
    W("─" * 78)
    for rank, (bucket, assessment) in enumerate(by_count, 1):
        W(f"  {rank:>2}  {bucket.count:>5}  {assessment.score:>5}  {bucket.file_path}")
    W("")

    for rank, (bucket, assessment) in enumerate(by_count, 1):
        W("=" * 78)
        W(f"#{rank}  [{bucket.count} errors | score {assessment.score}]  {bucket.file_path}")
        W("=" * 78)
        W("")

        resolution = assessment.source_resolution
        if resolution and resolution.instances:
            write_source_section(W, resolution)
        else:
            W("  SOURCE / OVERRIDE CONTEXT:")
            W("    No matching file instances found or source resolver not configured.")
            W("")

        W("  RECOMMENDATION:")
        W(f"    {assessment.recommendation}")
        W(f"    Confidence: {assessment.confidence}")
        W(f"    Reason: {assessment.reason}")
        W("")

        W("  SAMPLE ERRORS (up to 5 unique messages):")
        for sample in bucket.sample_messages(limit=5):
            W(f"    - {sample}")
        W("")

    W("=" * 78)
    W(f"END OF ANALYSIS  |  {len(buckets)} files  |  {len(issues):,} total canonical issues")
    W("=" * 78)
    return "\n".join(out)


def write_source_section(W: Callable[[str], None], resolution: SourceResolution) -> None:
    W(f"  OVERRIDE CHAIN  ({len(resolution.instances)} instance(s), load order ascending):")
    winner = resolution.winning_instance
    for inst in resolution.instances:
        flags: list[str] = []
        if winner and inst.source_name == winner.source_name and inst.load_order == winner.load_order:
            flags.append("WINNER")
        if resolution.our_submod_name and inst.source_name == resolution.our_submod_name:
            flags.append("OUR SUBMOD")
        flag_str = "  <<< " + ", ".join(flags) if flags else ""
        W(f"    [{inst.load_order:>3}] {inst.source_name}{flag_str}")
        W(f"           {inst.path}")
        W(f"           Modified: {inst.modified_at.strftime('%Y-%m-%d %H:%M')}")
    W("")

    if winner:
        W(f"  WINNING MOD  : {winner.source_name}  (load order {winner.load_order})")
        W(f"  CURRENT WINNING FILE: {winner.path}")
        W("")

    if resolution.our_submod_override:
        W("  OUR SUBMOD OVERRIDE: YES")
        if resolution.diff_vs_original:
            diff = resolution.diff_vs_original
            W(f"  DIFF vs ORIGINAL [{diff.compared_to}]: +{diff.added} added / -{diff.removed} removed")
            if diff.stale_warning:
                W("  *** STALE PATCH WARNING: our override removes substantially more than it adds.")
        if resolution.diff_vs_predecessor:
            diff = resolution.diff_vs_predecessor
            W(f"  DIFF vs PREDECESSOR [{diff.compared_to}]: +{diff.added} added / -{diff.removed} removed")
            if diff.stale_warning:
                W("  *** PREDECESSOR STALE WARNING: predecessor may have new content we overwrite.")
    else:
        W("  OUR SUBMOD OVERRIDE: NO")
        W("  ACTION: consider creating an override in our submod if fix is needed.")
    W("")

```


---

# File: `ck3chronicle_proto/sdk_adapter.py`

```python
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import SourceInstance, SourceType


def load_ck3_sdk() -> Any:
    """Load ck3raven's local SDK from ~/.ck3raven/wip/sdk."""

    sdk_dir = Path.home() / ".ck3raven" / "wip" / "sdk"
    sys.path.insert(0, str(sdk_dir))
    import ck3_sdk as ck3_sdk_mod  # type: ignore

    return ck3_sdk_mod.CK3SDK()


class CK3SDKSourceProvider:
    """Source provider backed by ck3raven's CK3SDK.

    This preserves the original script behavior but keeps it outside parsing.
    """

    def __init__(self, sdk: Any):
        self.sdk = sdk

    def iter_instances(self, rel_path: str) -> list[SourceInstance]:
        found: list[SourceInstance] = []

        try:
            game_file = self.sdk.resolve(f"root:game/{rel_path}")
            if game_file and Path(game_file).exists():
                path = Path(game_file)
                found.append(
                    SourceInstance(
                        source_name="Base Game",
                        load_order=-1,
                        path=path,
                        modified_at=datetime.fromtimestamp(path.stat().st_mtime),
                        source_type="base_game",
                    )
                )
        except Exception:
            pass

        for mod in sorted(getattr(self.sdk, "mods", []), key=lambda m: m.load_order):
            try:
                mod_file = self.sdk.resolve(f"mod:{mod.name}/{rel_path}")
                if mod_file and Path(mod_file).exists():
                    path = Path(mod_file)
                    raw_path = str(path).replace("\\", "/")
                    source_type: SourceType = "local_mod" if "/mod/" in raw_path else "workshop_mod"
                    found.append(
                        SourceInstance(
                            source_name=mod.name,
                            load_order=mod.load_order,
                            path=path,
                            modified_at=datetime.fromtimestamp(path.stat().st_mtime),
                            source_type=source_type,
                        )
                    )
            except Exception:
                pass

        return sorted(found, key=lambda i: i.load_order)


def default_log_path_from_sdk(sdk: Any) -> tuple[Path, str]:
    ck3_root = sdk.resolve("root:user_docs")
    override = sdk.wip / ".log_path_override"

    if override.exists():
        log_path = Path(override.read_text(encoding="utf-8").strip())
        override.unlink()
        return log_path, str(log_path)

    return Path(ck3_root) / "logs" / "error.log", "root:user_docs/logs/error.log"

```


---

# File: `tests/test_smoke_parser.py`

```python
from ck3chronicle_proto.log_parser import parse_script_error_blocks


def test_script_error_parser_emits_canonical_issue():
    sample = """
[04:03:16][E][jomini_script_system.cpp:303]: Script system error!
  Error: untyped trigger [ Scoped object of type 'character' is not valid ((no character) weak (Character - 18182)!) ]
  Script location: file: common/scripted_effects/TCT_scripted_effects.txt line: 275 (predict_new_cardinal)
    file: common/scripted_effects/TCT_scripted_effects.txt line: 315 (update_cardinal_window)
    file: common/on_action/tct_on_actions.txt line: 673 (tct_cardinal_update)
""".strip()
    issues = parse_script_error_blocks(sample)
    assert len(issues) == 1
    issue = issues[0]
    assert issue.schema_version == "ck3chronicle.issue.v1"
    assert issue.primary_file == "common/scripted_effects/TCT_scripted_effects.txt"
    assert issue.primary_line == 275
    assert issue.primary_symbol == "predict_new_cardinal"
    assert issue.category == "Script Execution"
    assert len(issue.call_stack) == 3

```
