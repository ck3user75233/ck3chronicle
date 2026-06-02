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
