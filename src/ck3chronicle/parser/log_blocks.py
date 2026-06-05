"""Split a CK3 error.log into timestamped log blocks.

A timestamped block begins with a line whose leading tokens match
``[HH:MM:SS][source_tag]: ...``. Continuation lines (anything until the
next timestamped header or EOF) belong to that block. The splitter never
drops a line.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator


_HEADER_RE = re.compile(r"^\[(\d{2}:\d{2}:\d{2})\]\[([^\]]+)\]:\s?(.*)$")


@dataclass
class TimestampedLogBlock:
    """One timestamped block as produced by :func:`iter_log_blocks`.

    Field names match the Phase 1 acceptance tests exactly:
    ``timestamp``, ``source_tag``, ``header_line``, ``continuation_lines``,
    ``raw_block``, ``log_relpath``, ``line_number``.
    """

    timestamp: str | None
    source_tag: str
    header_line: str
    continuation_lines: list[str]
    raw_block: str
    log_relpath: str = ""
    line_number: int = 0


def iter_log_blocks(path: Path) -> Iterator[TimestampedLogBlock]:
    """Yield one :class:`TimestampedLogBlock` per timestamped header in *path*.

    An empty file yields nothing. Pre-timestamp preamble lines (if any)
    are collected into a single block with ``timestamp=None`` and
    ``source_tag="<preamble>"``.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text:
        return

    log_relpath = path.name
    lines = text.splitlines()

    cur_ts: str | None = None
    cur_source: str = ""
    cur_header: str = ""
    cur_cont: list[str] = []
    cur_raw: list[str] = []
    cur_line_number: int = 0

    preamble: list[str] = []
    preamble_started = False

    def _emit() -> TimestampedLogBlock:
        return TimestampedLogBlock(
            timestamp=cur_ts,
            source_tag=cur_source,
            header_line=cur_header,
            continuation_lines=list(cur_cont),
            raw_block="\n".join(cur_raw),
            log_relpath=log_relpath,
            line_number=cur_line_number,
        )

    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        m = _HEADER_RE.match(line)
        if m:
            # Flush preamble before first real block (if any non-empty content).
            if preamble_started and not cur_raw and any(p for p in preamble):
                yield TimestampedLogBlock(
                    timestamp=None,
                    source_tag="<preamble>",
                    header_line=preamble[0] if preamble else "",
                    continuation_lines=preamble[1:] if len(preamble) > 1 else [],
                    raw_block="\n".join(preamble),
                    log_relpath=log_relpath,
                    line_number=1,
                )
                preamble = []
                preamble_started = False
            # Flush current block.
            if cur_raw:
                yield _emit()
            cur_ts = m.group(1)
            cur_source = m.group(2)
            cur_header = line
            cur_cont = []
            cur_raw = [line]
            cur_line_number = idx
        else:
            if cur_raw:
                cur_cont.append(line)
                cur_raw.append(line)
            else:
                preamble_started = True
                preamble.append(line)

    if cur_raw:
        yield _emit()
    elif preamble_started and any(p for p in preamble):
        yield TimestampedLogBlock(
            timestamp=None,
            source_tag="<preamble>",
            header_line=preamble[0] if preamble else "",
            continuation_lines=preamble[1:] if len(preamble) > 1 else [],
            raw_block="\n".join(preamble),
            log_relpath=log_relpath,
            line_number=1,
        )
