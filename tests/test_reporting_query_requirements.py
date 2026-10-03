"""Task 08A.1 checks against genuine retained SQL records only.

CK3_TASK08A_EVIDENCE names an existing disposable genuine-input database and an
ignored output_root. No fabricated records, Run metadata, responses or failures.
"""
import json
import os
from pathlib import Path
import sqlite3
import unittest
import uuid

from ck3chronicle.pipeline.request_handler import HandlerClient
from ck3chronicle.reporting import (
    DiagnosticAnalysis, exact_identity, identity_key,
    template_text,
)


@unittest.skipUnless(os.environ.get('CK3_TASK08A_EVIDENCE'), 'requires genuine retained SQL evidence')
class GenuineStoredInvestigationChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        evidence = json.loads(Path(os.environ['CK3_TASK08A_EVIDENCE']).read_bytes())
        cls.out = Path(evidence['output_root']) / uuid.uuid4().hex
        cls.out.mkdir(parents=True)
        cls.database = cls.out / 'genuine.sqlite3'
        # Offline backup of an earlier disposable genuine-input exercise. Runtime
        # investigation below ONLY uses the public handler, never this connection.
        source = sqlite3.connect(Path(evidence['database']).as_uri() + '?mode=ro', uri=True)
        target = sqlite3.connect(cls.database)
        try:
            source.backup(target)
        finally:
            source.close()
            target.close()
        cls.client = HandlerClient(cls.database)
        cls.addClassCleanup(cls.client.shutdown)
        cls.service = DiagnosticAnalysis(cls.client)
        cls.package = evidence['package_id']
        cls.baseline = cls.service.investigate('latest', package_id=cls.package)
        cls.rows = [entry['stored_record'] for entry in cls.baseline.records]
        (cls.out / 'baseline.json').write_text(json.dumps(cls.baseline.to_dict(), ensure_ascii=False, indent=2), encoding='utf-8')
        print('Task 08A.1 genuine SQL evidence:', cls.out, flush=True)

    def test_public_reads_exact_totals_review_and_short_history(self):
        self.assertTrue(self.rows)
        expected = sum(r['occurrence_count'] for r in self.rows)
        self.assertEqual(self.baseline.totals['occurrences'], expected)
        self.assertEqual(self.baseline.totals['distinct_records'], len(self.rows))
        self.assertIsNotNone(self.baseline.review)
        self.assertTrue(any(r['match_status'] == 'provisional' for r in self.rows))
        self.assertTrue(any(r['match_status'] == 'template' for r in self.rows))
        self.assertEqual(self.baseline.window['obtained']['preceding'], 0)
        self.assertTrue(all(e['history']['newly_observed'] for e in self.baseline.records))
        result = self.service.investigate('latest', package_id=self.package, query={'analytics': {'trailing_runs': 5}})
        self.assertEqual(len(result.window['runs']), 1)
        self.assertEqual(result.window['runs'][0]['occurrences'], expected)

    def test_display_limits_do_not_change_counts_or_rollups(self):
        result = self.service.investigate('latest', package_id=self.package, query={'display': {'limit': 2}})
        self.assertEqual(len(result.records), 2)
        self.assertEqual(result.totals, self.baseline.totals)
        self.assertEqual(result.rollups, self.baseline.rollups)
        self.assertEqual(sum(b['occurrences'] for b in result.rollups['emitters']['buckets']), result.totals['occurrences'])

    def test_template_or_exact_identity_binding_and_message_compose(self):
        grouped = {}
        for row in self.rows:
            grouped.setdefault(row['definition']['template_id'], []).append(row)
        siblings = next(group for group in grouped.values() if len(group) > 1)
        first, second = siblings[:2]
        self.assertNotEqual(exact_identity(first), exact_identity(second))
        self.assertNotEqual(identity_key(first), identity_key(second))
        templates = list(grouped)[:2]
        result = self.service.investigate('latest', package_id=self.package, query={
            'refinement': {'templates': [{'template_id': t} for t in templates]}})
        self.assertEqual(result.totals['distinct_records'], sum(len(grouped[t]) for t in templates))
        definition = first['definition']
        entry = next(e for e in self.baseline.records if e['identity'] == exact_identity(first))
        binding = next(b for r in first['values']['regions'] for b in r['bindings'] if b['present'])
        query = {'refinement': {'templates': [{'template_id': definition['template_id']}],
                  'identities': [exact_identity(first)], 'message': {'contains': entry['message']},
                  'bindings': [{k: binding[k] for k in ('type', 'value', 'present')}]}}
        exact = self.service.investigate('latest', package_id=self.package, query=query)
        self.assertEqual(exact.totals['distinct_records'], 1)
        self.assertEqual(exact.records[0]['identity'], exact_identity(first))
        query['refinement']['templates'] = [{'template_id': next(t for t in grouped if t != definition['template_id'])}]
        self.assertEqual(self.service.investigate('latest', package_id=self.package, query=query).totals['distinct_records'], 0)

    def test_template_text_never_searches_bound_values(self):
        row, value = next((r, b['value']) for r in self.rows for region in r['values']['regions']
                         for b in region['bindings'] if b['present'] and len(b['value']) > 5
                         and b['value'].casefold() not in template_text(r['definition']).casefold())
        base = {'identities': [exact_identity(row)]}
        message = self.service.investigate('latest', package_id=self.package, query={
            'refinement': {**base, 'message': {'contains': value}}})
        pattern = self.service.investigate('latest', package_id=self.package, query={
            'refinement': {**base, 'template_text': {'contains': value}}})
        self.assertEqual(message.totals['distinct_records'], 1)
        self.assertEqual(pattern.totals['distinct_records'], 0)
        text = template_text(row['definition'])
        exact = self.service.investigate('latest', package_id=self.package, query={
            'refinement': {**base, 'template_exact': [text], 'template_text': {'and': [
                {'contains': text[:4]}, {'contains': text[-4:]}, {'not_contains': value}]}}})
        self.assertEqual(exact.totals['distinct_records'], 1)

    def test_record_selector_and_positive_occurrence_filter(self):
        row = self.rows[0]
        query = {'scope': {'source_families': [row['definition']['source_family']]},
                 'refinement': {'selectors': [{'templates': [{'template_id': row['definition']['template_id']}],
                                               'identities': [exact_identity(row)]}],
                                'occurrences': {'min': row['occurrence_count'], 'max': row['occurrence_count']}}}
        result = self.service.investigate('latest', package_id=self.package, query=query)
        self.assertEqual(result.totals['distinct_records'], 1)
        query['refinement']['occurrences']['min'] += 1
        query['refinement']['occurrences']['max'] += 1
        self.assertEqual(self.service.investigate('latest', package_id=self.package, query=query).totals['distinct_records'], 0)

    def test_newness_uses_included_predecessors(self):
        result = self.service.investigate('latest', package_id=self.package,
            query={'refinement': {'newly_observed': True}})
        expected = {e['identity_key'] for e in self.baseline.records
                    if e['selected_count'] > 0 and e['history']['preceding_observed'] == 0}
        self.assertEqual({e['identity_key'] for e in result.records}, expected)
        self.assertTrue(result.coverage['filter_complete'])


if __name__ == '__main__':
    unittest.main()
