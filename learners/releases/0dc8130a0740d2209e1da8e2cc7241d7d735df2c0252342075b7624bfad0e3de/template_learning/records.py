"""Learner-owned native message features. The raw parser never deduplicates."""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field, asdict
import hashlib
import json
from typing import Sequence
from template_learning.evidence import read_evidence
from template_learning.inventory import ProtectedLog
from template_learning.parsers import SelectedParser, iter_recoveries

FEATURE_VERSION = "ck3-native-message-features-v4"


def identity(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=True, sort_keys=True,
        separators=(",", ":")).encode()).hexdigest()


@dataclass
class SequenceRecord:
    source_family: str
    text: str
    pieces: tuple[tuple[str, str], ...]  # kind, native text; no alternate lexer
    context_kind: str = "body"
    contexts: dict = field(default_factory=dict)
    native_occurrences: list[dict] = field(default_factory=list)
    continuations: tuple[dict, ...] = ()

    @property
    def tokens(self):
        return tuple(text for kind,text in self.pieces if kind == "token")

    @property
    def occurrences(self):
        return len(self.native_occurrences)

    @property
    def key(self):
        base = self.source_family, self.context_kind, self.text
        return (*base, identity(self.continuations)) if self.continuations else base

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, row):
        result = cls(**{**row, "pieces": tuple(tuple(p) for p in row["pieces"])})
        if "".join(text for _,text in result.pieces) != result.text:
            raise ValueError("native feature pieces do not reproduce message")
        if any(kind not in {"gap", "token"} for kind,_ in result.pieces):
            raise ValueError("invalid native feature piece kind")
        return result


def bounds(span):
    return [span.start, span.end]


def context_for(emission, recovery):
    """Use established child framing to retain the outer wrapper, without siblings."""
    if recovery.structure != "located-message-wrapper":
        return "body", {}, {}
    ranges = {"prefix": (emission.body_span.start, recovery.messages[0].span.start),
              "suffix": (recovery.messages[-1].span.end, emission.body_span.end)}
    content, spans = {}, {}
    for name,(start,end) in ranges.items():
        selected = emission.select_messages(((start,end),))[0]
        content[name] = dict(text=selected.text,
            pieces=[(p.kind,p.text) for p in selected.pieces])
        spans[name] = [start,end]
    return "located-message-wrapper", content, spans


def collect_records(logs: Sequence[ProtectedLog], *, parser: SelectedParser):
    records, evidence_stats = {}, {}
    for evidence in logs:
        raw = read_evidence(evidence.path, parser=parser)
        actual_sha = hashlib.sha256(raw.source.data).hexdigest()
        if evidence.sha256 != actual_sha:
            raise ValueError(f"native evidence hash changed: {evidence.path}")
        stats = dict(kind=evidence.kind, path=str(evidence.path), sha256=actual_sha,
            bytes=len(raw.source.data), timestamped_blocks=len(raw.emissions),
            recovered_messages=0, deferred_recovered_messages=0,
            unresolved_emissions=[], source_counts={})
        for recovery in iter_recoveries(raw):
            emission = recovery.parent
            if recovery.status != "recovered":
                stats["unresolved_emissions"].append(dict(emission_ordinal=emission.ordinal,
                    source_family=emission.source_family, span=bounds(emission.span),
                    body_span=bounds(emission.body_span), text=emission.decoded_text,
                    reason=recovery.reason))
                continue
            kind, context, context_spans = context_for(emission, recovery)
            context_id = identity(context) if context else None
            for message in recovery.messages:
                text = message.text
                entries = tuple(dict(text=e.message.text,
                    pieces=[(p.kind,p.text) for p in e.message.pieces],
                    **{name:[getattr(e,name).start-e.message.span.start,
                             getattr(e,name).end-e.message.span.start]
                       for name in ('prefix_span','label_span','value_span')})
                    for e in getattr(message,'continuations',()))
                message_kind = 'continuation:' + recovery.structure if entries else kind
                new_record = SequenceRecord(emission.source_family,text,
                    tuple((p.kind,p.text) for p in message.pieces),message_kind,
                    continuations=entries)
                key = new_record.key
                record = records.get(key)
                if record is None:
                    record = new_record
                    records[key] = record
                if context_id:
                    record.contexts[context_id] = context
                record.native_occurrences.append(dict(evidence_id=evidence.evidence_id,
                    evidence_sha256=actual_sha, emission_ordinal=emission.ordinal,
                    message_ordinal=message.ordinal, span=bounds(message.span),
                    emission_span=bounds(emission.span), header_span=bounds(emission.header_span),
                    source_tag=emission.source_tag, timestamp=emission.timestamp, level=emission.level,
                    context_id=context_id, context_spans=context_spans,
                    **(dict(emission_ordinals=[e.ordinal for e in recovery.parents],
                        group_span=[emission.span.start,recovery.parents[-1].span.end],
                        recovery_limitation=recovery.reason,
                        component_spans=[bounds(e.message.span) for e in message.continuations])
                       if entries else {})))
                stats["recovered_messages"] += 1
                stats["source_counts"][emission.source_family] = stats["source_counts"].get(emission.source_family,0)+1
        evidence_stats[evidence.sha256] = stats
    return group_records(records.values()), evidence_stats


def group_records(records):
    grouped = defaultdict(list)
    for record in records:
        grouped[record.source_family].append(record)
    return {source:sorted(rows,key=lambda r:(r.context_kind,r.text)) for source,rows in sorted(grouped.items())}


def merge_records(records):
    merged = {}
    for record in records:
        if record.key not in merged:
            merged[record.key] = record
        else:
            previous = merged[record.key]
            if previous.pieces != record.pieces:
                raise ValueError("selected parser produced inconsistent native pieces")
            previous.contexts.update(record.contexts)
            previous.native_occurrences.extend(record.native_occurrences)
    return group_records(merged.values())
