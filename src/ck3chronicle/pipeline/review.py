"""Native review routing/accounting and the two-file shard format.

Only existing parser emission spans are read. No recovery, rendering, decoding,
matching or second unresolved text representation occurs here.
"""
from collections import Counter
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path

from .domain import NativeClassification, NativeReview, ResultIntegrityError, RunAccounting
from .schema import encode

LOG_NAME = 'review.error.log'
MANIFEST_NAME = 'review-manifest.json'
MANIFEST_VERSION = 3


def sync_file(path, payload):
    with Path(path).open('xb') as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def sync_directory(path):
    # Windows directory handles do not support os.open/fsync. Files are flushed;
    # power-loss guarantees still depend on the OS/filesystem (see handoff).
    if os.name != 'nt':
        fd = os.open(path, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


class ReviewWriter:
    def __init__(self, raw):
        """One pinned RawParse; observe EVERY final result exactly once."""
        self.raw = raw
        self._emissions = {e.ordinal: e for e in raw.emissions}
        if len(self._emissions) != len(raw.emissions):
            raise ResultIntegrityError('duplicate original emission ordinal')
        self._seen = set()
        self._references = Counter()
        self._record_emissions = set()
        self._review_emissions = set()
        self._routes = []
        self._counts = Counter()

    def observe(self, result: NativeClassification | NativeReview) -> None:
        native_review = isinstance(result, NativeReview)
        diagnostic = result if native_review else result.diagnostic
        if diagnostic.original is not self.raw:
            raise ResultIntegrityError('result belongs to another native input')
        unit, provenance = diagnostic.unit, diagnostic.provenance
        ordinals = tuple(provenance['emission_ordinals'])
        key = (ordinals, provenance.get('message_ordinal'))
        if (not ordinals or len(set(ordinals)) != len(ordinals)
                or any(o not in self._emissions for o in ordinals) or key in self._seen):
            raise ResultIntegrityError('missing, repeated or invalid child/emission association')
        self._seen.add(key)
        self._references.update(ordinals)
        unresolved = unit['recovery_status'] == 'unresolved'
        self._counts['observed_units'] += 1
        if unresolved:
            self._counts['unresolved_recovery_units'] += 1
        else:
            self._counts['recovered_occurrences'] += 1
            self._counts['supporting_entries'] += len(unit['continuations'])
            self._counts['recovered_groups'] += bool(unit['continuations'])
        if not native_review:
            self._counts[result.outcome + '_occurrences'] += 1
        elif result.error is not None:
            self._counts['input_failures'] += 1
        if result.disposition == 'record':
            self._record_emissions.update(ordinals)
            self._counts['eligible_occurrences'] += 1
            return
        self._review_emissions.update(ordinals)
        kind = ('native_input_failure' if native_review and result.error is not None else
                'unresolved_recovery' if native_review else 'no_match')
        route = dict(unit_index=len(self._seen) - 1, kind=kind,
                     reason=result.reason if native_review else result.review_reason,
                     source_family=diagnostic.source_family, provenance=deepcopy(provenance))
        if unresolved:
            recovery = unit['recovery']
            route['unresolved_spans'] = [[s.start, s.end] for s in recovery.unresolved_spans]
        else:
            route['regions'] = {'body': deepcopy(unit['body']['provenance']),
                'contexts': {k: deepcopy(v['provenance']) for k, v in unit['contexts'].items()},
                'continuations': [deepcopy(v['provenance']) for v in unit['continuations']]}
        if native_review and result.error is not None:
            route['error_type'] = type(result.error).__name__
        self._routes.append(route)

    def accounting(self, records) -> RunAccounting:
        """Validate complete coverage and occurrence/status totals before any write."""
        if set(self._references) != set(self._emissions):
            raise ResultIntegrityError('not every original emission was accounted for')
        names = ('observed_units', 'recovered_occurrences', 'recovered_groups',
                 'supporting_entries', 'unresolved_recovery_units', 'input_failures',
                 'template_occurrences', 'provisional_occurrences', 'no_match_occurrences',
                 'eligible_occurrences')
        counts = {name: self._counts[name] for name in names}
        counts.update(recognized_emissions=len(self._emissions),
            single_unit_emissions=sum(n == 1 for n in self._references.values()),
            multi_unit_emissions=sum(n > 1 for n in self._references.values()),
            record_emissions=len(self._record_emissions),
            mixed_emissions=len(self._record_emissions & self._review_emissions),
            review_emissions=len(self._review_emissions), review_units=len(self._routes),
            aggregated_records=len(records))
        if (sum(r.occurrence_count for r in records) != counts['eligible_occurrences']
                or any(sum(r.occurrence_count for r in records if r.match_status == status)
                       != counts[status + '_occurrences'] for status in ('template', 'provisional'))
                or counts['eligible_occurrences'] != counts['template_occurrences'] + counts['provisional_occurrences']
                or counts['recovered_occurrences'] != counts['eligible_occurrences'] + counts['no_match_occurrences'] + counts['input_failures']
                or counts['review_units'] != counts['no_match_occurrences'] + counts['unresolved_recovery_units'] + counts['input_failures']
                or counts['observed_units'] != counts['recovered_occurrences'] + counts['unresolved_recovery_units']
                or counts['recognized_emissions'] != counts['record_emissions'] + counts['review_emissions'] - counts['mixed_emissions']):
            raise ResultIntegrityError('Run occurrence/review reconciliation failed')
        return RunAccounting(counts)

    def stage(self, directory: Path) -> dict:
        """Repository-owned exclusive directory; write exact bytes in ordinal order."""
        digest = hashlib.sha256()
        emissions = []
        sources = Counter()
        offset = 0
        with (directory / LOG_NAME).open('xb') as stream:
            for ordinal in sorted(self._review_emissions):
                emission = self._emissions[ordinal]
                payload = self.raw.read_bytes(emission.span)
                if len(payload) != emission.span.end - emission.span.start:
                    raise ResultIntegrityError('short original emission read')
                stream.write(payload)
                digest.update(payload)
                emissions.append(dict(ordinal=ordinal,
                    original_span=[emission.span.start, emission.span.end],
                    header_span=[emission.header_span.start, emission.header_span.end],
                    shard_span=[offset, offset + len(payload)], source_family=emission.source_family))
                sources[emission.source_family] += 1
                offset += len(payload)
            stream.flush()
            os.fsync(stream.fileno())
        return dict(schema='ck3chronicle.native-review', schema_version=MANIFEST_VERSION,
            log_file=LOG_NAME, log_sha256=digest.hexdigest(), log_bytes=offset,
            emissions=emissions, routes=deepcopy(self._routes), source_counts=dict(sources),
            routing_counts=dict(Counter(r['kind'] for r in self._routes)),
            reason_counts=dict(Counter(r['reason'] for r in self._routes)))


def finalize(directory: Path, staged: dict, *, run_id, lineage, log_sha256, accounting, playset):
    """Complete the manifest in staging; repository then publishes both files."""
    manifest = dict(staged, run_id=run_id, lineage=lineage, input_log_sha256=log_sha256,
                    counts=accounting.counts, playset=playset, finalization='complete')
    sync_file(directory / MANIFEST_NAME, (encode(manifest) + '\n').encode('ascii'))
    sync_directory(directory)
    return manifest


def verify_published(directory: Path, expected: dict) -> None:
    """Completion-time verification only. Ordinary DB reads never call this."""
    manifest = json.loads((directory / MANIFEST_NAME).read_bytes())
    if manifest != expected:
        raise ResultIntegrityError('published review manifest differs')
    digest = hashlib.sha256()
    size = 0
    with (directory / LOG_NAME).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
            size += len(chunk)
    if size != expected['log_bytes'] or digest.hexdigest() != expected['log_sha256']:
        raise ResultIntegrityError('published review bytes differ')
