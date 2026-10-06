"""08A.2 acceptance using unchanged retained CK3 SQL and installed source files.

Set CK3_TASK08A2_EVIDENCE to a JSON file naming database, package_id,
output_root and external_root. No generated source/diagnostic fixtures or injected
failures. Assertions describe the inspected 20260930-CWO6LH evidence; a changed
installation needs renewed inspection, not changes to product requirements.
"""
import json
import os
from pathlib import Path
import sqlite3
from time import perf_counter
import unittest
import uuid

from ck3chronicle.pipeline.request_handler import HandlerClient
from ck3chronicle.reporting import DiagnosticAnalysis, SourceSearch, source_references


@unittest.skipUnless(os.environ.get('CK3_TASK08A2_EVIDENCE'), 'requires real CK3 database and installed sources')
class GenuineSourceChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads(Path(os.environ['CK3_TASK08A2_EVIDENCE']).read_bytes())
        cls.out = Path(cls.config['output_root']) / uuid.uuid4().hex
        cls.out.mkdir(parents=True)
        cls.database = cls.out / 'genuine.sqlite3'
        source = sqlite3.connect(Path(cls.config['database']).as_uri() + '?mode=ro', uri=True)
        target = sqlite3.connect(cls.database)
        try:
            source.backup(target)
        finally:
            source.close()
            target.close()
        cls.client = HandlerClient(cls.database)
        cls.addClassCleanup(cls.client.shutdown)
        cls.package = cls.config['package_id']
        cls.sql = DiagnosticAnalysis(cls.client)
        cls.baseline = cls.sql.investigate('latest', package_id=cls.package)
        cls.run_id = cls.baseline.run['run_id']
        cls.search = SourceSearch(cls.client, scratch_directory=cls.out)
        cls.reference = 'common/on_action/sea_minority_on_actions.txt'
        print('08A.2 genuine evidence:', cls.out, flush=True)

    def save(self, name, value):
        (self.out / (name + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

    def test_01_recorded_playset_and_full_inventory_reuse(self):
        playset = self.search.read_playset(self.run_id)
        stored = self.client.result(self.client.submit('read_playset', {'run_id': self.run_id})).value
        self.assertEqual(playset['stored'], stored)
        self.assertEqual(len(playset['members']), 133)
        self.assertTrue(all(m['available'] for m in playset['members']))
        selection = {'filename': {'exact': ['sea_minority_on_actions.txt']}}
        start = perf_counter()
        first = self.search.search(selection, run_id=self.run_id)
        construction = perf_counter() - start
        builds = self.search.metrics['inventory_builds']
        start = perf_counter()
        reused = self.search.search(selection, run_id=self.run_id)
        lookup = perf_counter() - start
        self.assertTrue(first['coverage']['complete'])
        self.assertEqual([f['member']['load_order'] for f in first['files']], [114, 115])
        self.assertEqual(first['files'], reused['files'])
        self.assertEqual(builds, self.search.metrics['inventory_builds'])
        self.save('playset', playset)
        self.save('filename', {'first_seconds': construction, 'reused_seconds': lookup, 'first': first, 'reused': reused})

    def test_02_large_playset_batched_content(self):
        start = perf_counter()
        result = self.search.search({'directories': ['common'], 'extensions': ['txt'], 'content': {'and': [
            {'contains': 'do_culture_faith_migration'}, {'contains': 'tradition_isolationist'}]}}, run_id=self.run_id)
        self.assertTrue(result['files'])
        for file in result['files']:
            actual = Path(file['physical_path']).read_text(encoding='utf-8-sig')
            self.assertIn('do_culture_faith_migration', actual.casefold())
            self.assertIn('tradition_isolationist', actual.casefold())
            for line in file['matching_lines']:
                self.assertEqual(line['text'], actual.splitlines()[line['line'] - 1])
        self.save('large-content', {'seconds': perf_counter() - start, 'result': result})
        print('Large content coverage:', result['coverage']['complete'], 'issues:', len(result['coverage']['issues']), flush=True)

    def test_03_file_level_groups_negatives_and_windows_no_match(self):
        selection = {'files': [self.reference]}
        files = self.search.search(selection, run_id=self.run_id)['files']
        actual = {f['physical_path']: Path(f['physical_path']).read_text(encoding='utf-8-sig') for f in files}
        expressions = [
            {'and': [{'contains': 'DO_CULTURE_FAITH_MIGRATION'}, {'contains': 'tradition_isolationist'}]},
            {'and': [{'contains': 'do_culture_faith_migration'}, {'or': [
                {'contains': 'exists = scope:source_county'}, {'contains': 'do_minority_culture_growth'}]},
                {'not_contains': 'exists = scope:source_county'}]},
            {'not_contains': 'exists = scope:source_county'},
            {'contains': 'DO_CULTURE_FAITH_MIGRATION', 'case_sensitive': True},
        ]
        results = [self.search.search({**selection, 'content': e}, run_id=self.run_id) for e in expressions]
        expected = [set(actual), {p for p, t in actual.items() if 'exists = scope:source_county' not in t},
                    {p for p, t in actual.items() if 'exists = scope:source_county' not in t}, set()]
        for result, paths in zip(results, expected):
            self.assertTrue(result['coverage']['complete'])
            self.assertEqual({f['physical_path'] for f in result['files']}, paths)
        self.assertTrue(all(not f['matching_lines'] for f in results[2]['files']))
        self.assertEqual(results[-1]['coverage']['metrics']['ripgrep_invocations'][-1]['exit_code'], 1)
        for file in results[0]['files']:
            self.assertGreater(len({l['line'] for l in file['matching_lines']}), 1)
        self.save('content-groups', results)

    def test_04_explicit_unrecorded_root_and_path_filters(self):
        root = self.config['external_root']
        members = self.search.read_playset(self.run_id)['stored']['members']
        self.assertNotIn(os.path.normcase(os.path.abspath(root)), {os.path.normcase(os.path.abspath(m['path'])) for m in members})
        result = SourceSearch(scratch_directory=self.out).search({'roots': [root], 'recursive': False,
            'extensions': ['mod'], 'include': ['*.mod'], 'exclude': ['thumbnail.*'],
            'filename': {'text': {'contains': 'descriptor'}}, 'relative_path': {'exact': ['descriptor.mod']},
            'filename_globs': ['descriptor.*'], 'path_globs': ['*.mod'], 'content': {'contains': 'More Bookmarks+'}})
        self.assertTrue(result['coverage']['complete'])
        self.assertEqual([f['relative_path'] for f in result['files']], ['descriptor.mod'])
        self.assertIsNone(result['files'][0]['member'])
        self.save('external-root', result)

    def test_05_many_diagnostic_references_preserve_sql_totals(self):
        start = perf_counter()
        resolver = SourceSearch(self.client, scratch_directory=self.out)
        result = DiagnosticAnalysis(self.client, source_resolver=resolver).investigate('latest', package_id=self.package)
        self.assertEqual(result.totals, self.baseline.totals)
        # 08B receiving adds candidate-bearing per-Run contributors/rankings.
        # Optional source context must still leave the SQL counts/history intact.
        for actual, expected in zip(result.window['runs'], self.baseline.window['runs']):
            self.assertEqual({k: v for k, v in actual.items() if k not in {'records', 'rollups'}},
                             {k: v for k, v in expected.items() if k not in {'records', 'rollups'}})
            self.assertEqual([e['history'] for e in actual['records']],
                             [e['history'] for e in expected['records']])
        self.assertTrue(any(len(e['candidates']) > 1 for e in result.records))
        self.assertTrue(result.rollups['candidate_files']['overlapping_records'])
        self.assertFalse(result.rollups['candidate_files']['bucket_totals_are_additive'])
        self.save('many-references', {'seconds': perf_counter() - start, 'totals': result.totals,
            'coverage': result.coverage, 'reference_records': sum(bool(e['references']) for e in result.records),
            'candidate_records': sum(bool(e['candidates']) for e in result.records),
            'overlapping_records': result.rollups['candidate_files']['overlapping_records']})

    def test_06_member_file_template_exact_identity_composition_and_excerpts(self):
        selected = next(e for e in self.baseline.records if 'culture trigger [ Failed context switch' in e['message'])
        resolver = SourceSearch(self.client, excerpts=True, scratch_directory=self.out)
        service = DiagnosticAnalysis(self.client, source_resolver=resolver)
        query = {'scope': {'source': {'members': [{'load_order': 114}, {'load_order': 115}], 'files': [self.reference]}},
            'refinement': {'templates': [selected['identity']['definition']], 'identities': [selected['identity']],
                'bindings': [{'type': 'KEY', 'value': 'culture'}], 'template_text': {'contains': 'trigger'},
                'message': {'contains': 'Failed context switch'}}, 'display': {'limit': 1}}
        result = service.investigate('latest', package_id=self.package, query=query)
        self.assertEqual(result.totals['occurrences'], 5)
        self.assertEqual(result.totals['distinct_records'], 1)
        entry = result.records[0]
        self.assertEqual([c['member']['load_order'] for c in entry['candidates']], [114, 115])
        self.assertEqual(entry['reference_details'][0]['slot_id'], 's2')
        for candidate in entry['candidates']:
            excerpt = candidate['excerpts'][0]
            self.assertTrue(excerpt['available'])
            self.assertEqual([l['line'] for l in excerpt['lines']], list(range(131, 152)))
            actual = Path(candidate['physical_path']).read_text(encoding='utf-8-sig').splitlines()
            self.assertEqual(next(l for l in excerpt['lines'] if l['target'])['text'], actual[140])
        self.save('composed-investigation', result.to_dict())

    def test_07_script_stack_and_real_boundary_excerpt(self):
        query = {'refinement': {'message': {'contains': 'Failed context switch'}}}
        resolver = SourceSearch(self.client, excerpts=True, scratch_directory=self.out)
        result = DiagnosticAnalysis(self.client, source_resolver=resolver).investigate('latest', package_id=self.package, query=query)
        self.assertEqual(result.totals['distinct_records'], 8)
        self.assertEqual(result.totals['occurrences'], 16)
        health = next(e for e in result.records if any(r['path'] == 'common/on_action/health_on_actions.txt' for r in e['reference_details']))
        self.assertTrue(any(r['role'] == 'supporting' for r in health['reference_details']))
        excerpts = [x for c in health['candidates'] for x in c['excerpts'] if x['line'] == 4 and x['available']]
        self.assertTrue(excerpts)
        for excerpt in excerpts:
            self.assertEqual(excerpt['lines'][0]['line'], 1)
            self.assertEqual(excerpt['lines'][-1]['line'], min(14, excerpt['total_lines']))
        self.save('eight-diagnostics', result.to_dict())

    def test_08_source_filters_exclude_unlocated_records(self):
        unlocated = next(e for e in self.baseline.records if not source_references(e['stored_record'])['references'])
        located = next(e for e in self.baseline.records if 'culture trigger [ Failed context switch' in e['message'])
        service = DiagnosticAnalysis(self.client, source_resolver=SourceSearch(self.client, scratch_directory=self.out))
        query = {'scope': {'source': {'members': [{'load_order': 115}]}},
                 'refinement': {'identities': [unlocated['identity'], located['identity']]}}
        result = service.investigate('latest', package_id=self.package, query=query)
        self.assertEqual([e['identity'] for e in result.records], [located['identity']])
        self.assertEqual(len(result.records[0]['candidates']), 1)
        self.assertTrue(result.coverage['source'][self.run_id]['complete'])
        self.assertEqual(result.coverage['source'][self.run_id]['records_without_source_path'], 0)
        query['scope']['source'] = {'files': [self.reference]}
        path = service.investigate('latest', package_id=self.package, query=query)
        self.assertEqual([e['identity'] for e in path.records], [located['identity']])
        self.assertEqual(path.coverage['source'][self.run_id]['metrics']['inventory_builds'], 0)
        query['refinement']['identities'] = [unlocated['identity']]
        empty = service.investigate('latest', package_id=self.package, query=query)
        self.assertEqual(empty.totals['distinct_records'], 0)
        self.assertFalse(empty.coverage['source'][self.run_id]['issues'])
        self.save('unlocated-excluded', {'member': result.to_dict(), 'path': path.to_dict(), 'empty': empty.to_dict()})

    def test_09_stored_reference_filter_and_explicit_basename_mode(self):
        service = DiagnosticAnalysis(self.client, source_resolver=SourceSearch(self.client, scratch_directory=self.out))
        result = service.investigate('latest', package_id=self.package, query={
            'scope': {'source': {'referenced_paths': [self.reference]}},
            'refinement': {'message': {'contains': 'Failed context switch'}}})
        self.assertEqual(result.totals['distinct_records'], 2)
        self.assertEqual(result.totals['occurrences'], 10)
        self.assertEqual(result.coverage['source'][self.run_id]['metrics']['inventory_builds'], 0)
        combined_paths = {'files': [self.reference], 'directories': ['common/on_action'], 'recursive': False,
                          'extensions': ['txt'], 'filename': {'exact': ['sea_minority_on_actions.txt']},
                          'relative_path': {'text': {'and': [{'contains': 'common/'}, {'contains': 'on_action/'}]}},
                          'filename_globs': ['sea_*.txt'], 'path_globs': ['common/*'], 'include': ['*.txt']}
        query = {'scope': {'source': combined_paths}, 'refinement': {'message': {'contains': 'Failed context switch'}}}
        composed = service.investigate('latest', package_id=self.package, query=query)
        self.assertEqual(composed.totals, result.totals)
        self.assertEqual(composed.coverage['source'][self.run_id]['metrics']['inventory_builds'], 0)
        query['scope']['source']['exclude'] = [self.reference]
        excluded = service.investigate('latest', package_id=self.package, query=query)
        self.assertEqual(excluded.totals['distinct_records'], 0)
        self.assertFalse(excluded.coverage['source'][self.run_id]['issues'])
        first = self.search.search({'referenced_paths': [self.reference]}, run_id=self.run_id)
        broad = self.search.search({'referenced_paths': ['sea_minority_on_actions.txt'], 'reference_mode': 'basename'}, run_id=self.run_id)
        self.assertEqual(first['files'], broad['files'])
        self.save('stored-reference', result.to_dict())
