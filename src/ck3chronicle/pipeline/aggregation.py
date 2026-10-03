"""Exact Error Contract aggregation, with digest buckets rather than hash equality."""
from copy import deepcopy
from dataclasses import replace

from .contracts import identity_data, identity_digest
from .domain import DiagnosticRecord, ResultIntegrityError


class RecordAccumulator:
    def __init__(self):
        self._buckets = {}
        self._records = []
        self._definitions = {}

    def add(self, definition: dict, prepared: dict) -> None:
        """Consume one prepare_record result and its materialized definition."""
        values = prepared['values']
        if (prepared['occurrence_count'] != 1 or prepared['error_type'] != 'unknown'
                or prepared['match_status'] not in ('template', 'provisional')
                or values['template_id'] != definition['template_id']
                or values['contract_version'] != definition['contract_version']):
            raise ResultIntegrityError('not a prepared eligible occurrence')
        template = definition['template_id']
        previous = self._definitions.get(template)
        if previous is not None and previous != definition:
            raise ResultIntegrityError('contradictory definition within Run')
        if previous is None:
            self._definitions[template] = deepcopy(definition)
        equality = identity_data(values)
        digest = identity_digest(values)
        bucket = self._buckets.setdefault(digest, [])
        for index, existing_equality in bucket:
            if equality == existing_equality:
                record = self._records[index]
                if record.match_status != prepared['match_status']:
                    raise ResultIntegrityError('contradictory final status for equal identity')
                self._records[index] = replace(record, occurrence_count=record.occurrence_count + 1)
                return
        bucket.append((len(self._records), equality))
        self._records.append(DiagnosticRecord(self._definitions[template], deepcopy(values),
            prepared['match_status'], 1, 'unknown', deepcopy(prepared['provenance'])))

    def records(self) -> tuple[DiagnosticRecord, ...]:
        """Independent snapshot in first-occurrence order; no per-repeat provenance."""
        return deepcopy(tuple(self._records))
