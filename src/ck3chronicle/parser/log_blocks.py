"""Lossless lexical splitting for CK3 timestamped log blocks.

Block hashes and byte lengths are computed from the exact evidence bytes,
including original line endings and an unterminated final line.  Extractors get
decoded display text, while provenance remains bound to the raw byte slice.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


_HEADER_RE_THREE = re.compile(
    br"^\[(\d{2}:\d{2}:\d{2})\]\[([^\]\r\n]+)\]\[([^\]\r\n]+)\]:"
)
_HEADER_RE_TWO = re.compile(
    br"^\[(\d{2}:\d{2}:\d{2})\]\[([^\]\r\n]+)\]:"
)
_SOURCE_LINE_SUFFIX_RE = re.compile(r":\d+$")
_UTF8_BOM = b"\xef\xbb\xbf"


@dataclass
class TimestampedLogBlock:
    """One exact lexical block from a CK3 log.

    The first seven fields preserve the original extractor API.  C1 provenance
    fields have defaults so older unit fixtures can still construct blocks.
    """

    timestamp: str | None
    source_tag: str
    header_line: str
    continuation_lines: list[str]
    raw_block: str
    log_relpath: str = ""
    line_number: int = 0
    end_line: int = 0
    level: str | None = None
    source_family: str = ""
    raw_block_sha256: str = ""
    raw_byte_length: int = 0
    source_block_id: str = ""


def source_block_id(log_relpath: str, start_line: int, raw_block_sha256: str) -> str:
    """Return the Phase 1 provenance identity for one source block."""
    identity = (
        log_relpath.encode("utf-8")
        + b"\0"
        + str(start_line).encode("ascii")
        + b"\0"
        + raw_block_sha256.encode("ascii")
    )
    return hashlib.sha256(identity).hexdigest()


def _without_line_ending(raw_line: bytes) -> bytes:
    if raw_line.endswith(b"\r\n"):
        return raw_line[:-2]
    if raw_line.endswith((b"\n", b"\r")):
        return raw_line[:-1]
    return raw_line


def _decode(raw: bytes) -> str:
    return raw.decode("utf-8", errors="replace")


def _parse_header(raw_line: bytes) -> tuple[str, str | None, str] | None:
    """Parse a header with strict UTF-8 metadata, matching the frozen oracle."""
    match = _HEADER_RE_THREE.match(raw_line)
    if match is not None:
        try:
            return (
                match.group(1).decode("ascii"),
                match.group(2).decode("utf-8", errors="strict"),
                match.group(3).decode("utf-8", errors="strict"),
            )
        except UnicodeDecodeError:
            return None

    # Retain the two-part form for legacy Chronicle fixtures.  It is represented
    # with an empty level in canonical storage.
    match = _HEADER_RE_TWO.match(raw_line)
    if match is not None:
        try:
            return (
                match.group(1).decode("ascii"),
                None,
                match.group(2).decode("utf-8", errors="strict"),
            )
        except UnicodeDecodeError:
            return None
    return None


def _make_block(
    *,
    raw_lines: list[bytes],
    start_line: int,
    end_line: int,
    log_relpath: str,
    timestamp: str | None,
    level: str | None,
    source_tag: str,
) -> TimestampedLogBlock:
    raw_bytes = b"".join(raw_lines)
    raw_hash = hashlib.sha256(raw_bytes).hexdigest()
    display_lines = [_decode(_without_line_ending(line)) for line in raw_lines]
    family = (
        "<preamble>"
        if timestamp is None
        else _SOURCE_LINE_SUFFIX_RE.sub("", source_tag)
    )
    header_line = display_lines[0] if display_lines else ""
    # A UTF-8 BOM is an encoding signature, not CK3 message semantics.  The
    # lexer recognizes it only at byte zero, but the exact bytes remain in
    # ``raw_block`` and therefore in the evidence hash and source-block ID.
    if timestamp is not None and start_line == 1 and header_line.startswith("\ufeff"):
        header_line = header_line[1:]
    return TimestampedLogBlock(
        timestamp=timestamp,
        level=level,
        source_tag=source_tag,
        source_family=family,
        header_line=header_line,
        continuation_lines=display_lines[1:],
        raw_block=_decode(raw_bytes),
        log_relpath=log_relpath,
        line_number=start_line,
        end_line=end_line,
        raw_block_sha256=raw_hash,
        raw_byte_length=len(raw_bytes),
        source_block_id=source_block_id(log_relpath, start_line, raw_hash),
    )


def iter_log_blocks(
    path: Path,
    *,
    log_relpath: str | None = None,
    retain_preamble: bool = True,
) -> Iterator[TimestampedLogBlock]:
    """Yield exact timestamped blocks and, when present, one preamble block.

    A recognized header begins a block. Every raw physical line belongs either
    to the preamble or to exactly one yielded timestamped block. An empty file
    yields nothing. ``retain_preamble=False`` emits only a lightweight marker
    for preamble cardinality, avoiding whole-file retention when a malformed
    file contains no recognized header.
    """
    relpath = path.name if log_relpath is None else log_relpath
    current_lines: list[bytes] = []
    current_start = 0
    current_timestamp: str | None = None
    current_level: str | None = None
    current_source = ""
    preamble_lines: list[bytes] = []
    preamble_seen = False
    last_line = 0

    with path.open("rb") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            last_line = line_number
            header_view = (
                raw_line[len(_UTF8_BOM) :]
                if line_number == 1 and raw_line.startswith(_UTF8_BOM)
                else raw_line
            )
            parsed = _parse_header(header_view)
            if parsed is None:
                if current_lines:
                    current_lines.append(raw_line)
                elif retain_preamble:
                    preamble_lines.append(raw_line)
                else:
                    preamble_seen = True
                continue

            if preamble_lines or preamble_seen:
                if retain_preamble:
                    yield _make_block(
                        raw_lines=preamble_lines,
                        start_line=1,
                        end_line=line_number - 1,
                        log_relpath=relpath,
                        timestamp=None,
                        level=None,
                        source_tag="<preamble>",
                    )
                else:
                    yield TimestampedLogBlock(
                        timestamp=None,
                        source_tag="<preamble>",
                        header_line="",
                        continuation_lines=[],
                        raw_block="",
                        log_relpath=relpath,
                        line_number=1,
                        end_line=line_number - 1,
                        source_family="<preamble>",
                    )
                preamble_lines = []
                preamble_seen = False

            if current_lines:
                yield _make_block(
                    raw_lines=current_lines,
                    start_line=current_start,
                    end_line=line_number - 1,
                    log_relpath=relpath,
                    timestamp=current_timestamp,
                    level=current_level,
                    source_tag=current_source,
                )

            current_timestamp, current_level, current_source = parsed
            current_start = line_number
            current_lines = [raw_line]

    if current_lines:
        yield _make_block(
            raw_lines=current_lines,
            start_line=current_start,
            end_line=last_line,
            log_relpath=relpath,
            timestamp=current_timestamp,
            level=current_level,
            source_tag=current_source,
        )
    elif preamble_lines or preamble_seen:
        if retain_preamble:
            yield _make_block(
                raw_lines=preamble_lines,
                start_line=1,
                end_line=last_line,
                log_relpath=relpath,
                timestamp=None,
                level=None,
                source_tag="<preamble>",
            )
        else:
            yield TimestampedLogBlock(
                timestamp=None,
                source_tag="<preamble>",
                header_line="",
                continuation_lines=[],
                raw_block="",
                log_relpath=relpath,
                line_number=1,
                end_line=last_line,
                source_family="<preamble>",
            )
