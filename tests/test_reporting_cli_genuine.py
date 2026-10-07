"""08B consumer acceptance: real retained SQL/source evidence, actual root CLI.

CK3_TASK08B_EVIDENCE names the unchanged upstream backup, package_id, output_root
and optional single_database/external_root. No synthetic history, mock clients,
modified source files or injected failures. Only disposable handlers are stopped.
"""
from copy import deepcopy
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import unittest
from urllib.parse import unquote, urlsplit
import uuid

from ck3chronicle.pipeline.request_handler import HandlerClient, COMPLETED
from ck3chronicle.pipeline.contracts import render_segments
from ck3chronicle.reporting import DiagnosticAnalysis, SourceSearch, source_references, template_text
from ck3chronicle.reporting.presets import SYNTAX_ROWS, ASSIGNMENT_REASON


class HTMLLinks(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.scripts = set(), [], []
        self.visible_diagnostics, self.article, self.details_depth = {}, None, 0
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'details':
            self.details_depth += 1
        if tag == 'article':
            self.article = attrs.get('id')
            self.visible_diagnostics[self.article] = []
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag == 'script':
            self.scripts.append(attrs)

    def handle_endtag(self, tag):
        if tag == 'details':
            self.details_depth -= 1
        if tag == 'article':
            self.article = None

    def handle_data(self, value):
        if self.article and not self.details_depth:
            self.visible_diagnostics[self.article].append(value)


@unittest.skipUnless(os.environ.get('CK3_TASK08B_EVIDENCE'), 'requires genuine retained SQL/source evidence')
class GenuineReportingCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads(Path(os.environ['CK3_TASK08B_EVIDENCE']).read_bytes())
        cls.out = Path(cls.config['output_root']) / uuid.uuid4().hex
        cls.out.mkdir(parents=True)
        cls.database = cls.out / 'genuine.sqlite3'
        # Evidence preparation only; all runtime reads below use HandlerClient.
        with sqlite3.connect(Path(cls.config['database']).as_uri() + '?mode=ro', uri=True) as source:
            with sqlite3.connect(cls.database) as target:
                source.backup(target)
        cls.client = HandlerClient(cls.database)
        cls.addClassCleanup(cls.client.shutdown)
        cls.package = cls.config['package_id']
        cls.service = DiagnosticAnalysis(cls.client)
        cls.order = cls.service.list_runs(cls.package)
        cls.baseline = cls.service.investigate('latest', package_id=cls.package)
        cls.latest = cls.baseline.run['run_id']
        cls.calls = []
        print('08B CLI evidence:', cls.out, flush=True)
        cls.addClassCleanup(lambda: (cls.out / 'commands.json').write_text(json.dumps(cls.calls, indent=2), encoding='utf-8'))

    def cli(self, name, *args, expected=0, fmt='json', query=None, preset='frequent', run=None, mode='report'):
        command = [sys.executable, '-I', '-B', '-m', 'ck3chronicle.cli', mode]
        if mode == 'report':
            command += [run or 'latest']
            command += ['--preset', preset] if preset else ['--custom']
        command += ['--database', str(self.database), '--package-id', self.package, '--format', fmt]
        if query is not None:
            path = self.out / (name + '-query.json')
            path.write_text(json.dumps(query, ensure_ascii=False, indent=2), encoding='utf-8')
            command += ['--query', str(path)]
        destination = self.out / (name + '.' + ('txt' if fmt == 'text' else fmt))
        command += ['--output', str(destination), *map(str, args)]
        result = subprocess.run(command, capture_output=True, encoding='utf-8', timeout=240)
        self.calls.append({'command': command, 'returncode': result.returncode, 'stderr': result.stderr})
        (self.out / (name + '.stderr.txt')).write_text(result.stderr, encoding='utf-8')
        self.assertEqual(result.returncode, expected, result.stderr)
        self.assertTrue(destination.is_file(), result.stderr)
        text = destination.read_bytes().decode('utf-8')
        if fmt == 'json':
            explanation = json.loads(text)['explanation']
            for field in ('question', 'expected', 'result', 'reading_guide'):
                self.assertTrue(explanation[field], (name, field))
        else:
            for heading in ('What this report checks', 'What the result should show', 'What this result shows', 'How to read the entries'):
                self.assertIn(heading, text, name)
        return json.loads(text) if fmt == 'json' else text

    def test_01_run_selection_and_package_errors(self):
        result = self.cli('runs', mode='runs')
        self.assertEqual([r['run_id'] for r in result['runs']], [r['run_id'] for r in self.order['runs']])
        self.assertEqual(result['exclusions'], self.order['exclusions'])
        page = self.cli('runs-page', '--offset', 1, '--limit', 1, mode='runs')
        self.assertEqual(page['runs'], result['runs'][1:2])
        self.assertEqual(page['exclusions'], result['exclusions'])
        self.cli('runs-readable', mode='runs', fmt='text')
        excluded = result['exclusions'][0]['run_ids'][0]
        self.assertEqual(self.cli('ineligible', run=excluded, expected=2)['status'], 'run_selection_error')
        self.assertEqual(self.cli('unknown', run='unknown-run-selector', expected=2)['status'], 'run_selection_error')
        self.assertEqual(self.cli('conflicting-package', '--package-id', 'unrepresented-package', run=self.latest, expected=2)['status'], 'run_selection_error')
        none = self.cli('no-eligible', '--package-id', 'unrepresented-package', expected=2)
        self.assertIn('no eligible Run', none['error'])
        self.assertEqual(none['request']['run'], 'latest')
        self.assertEqual(none['request']['package_id'], 'unrepresented-package')
        rejected = self.cli('no-eligible', '--package-id', 'unrepresented-package', expected=2, fmt='html')
        self.assertIn('actual-result', HTMLLinks(rejected).ids)
        self.assertIn('href="#actual-result"', rejected)
        self.assertIn('no eligible Run is available in this processing package', rejected)
        self.assertIn('unrepresented-package', rejected)
        inferred = self.out / 'inferred-package.json'
        cmd = [sys.executable, '-I', '-B', '-m', 'ck3chronicle.cli', 'report', self.latest,
               '--database', str(self.database), '--preset', 'frequent', '--no-history', '--limit', '0', '--format', 'json']
        reply = subprocess.run(cmd, capture_output=True, encoding='utf-8', timeout=240)
        self.assertEqual(reply.returncode, 0, reply.stderr)
        value = json.loads(reply.stdout)
        self.assertEqual(value['package_id'], self.package)
        inferred.write_text(reply.stdout, encoding='utf-8')
        self.assertEqual(value['totals']['occurrences'], self.baseline.totals['occurrences'])

    def test_02_worked_window_formats_links_and_limits(self):
        query = {'purpose': 'Failed context switches across a trailing five-Run window',
                 'scope': {'source_families': ['jomini_script_system.cpp']},
                 'refinement': {'message': {'contains': 'failed context switch'}},
                 'analytics': {'trailing_runs': 5}, 'display': {'limit': 3, 'historical_limit': 2}}
        data = self.cli('worked', '--verbose', preset=None, query=query)
        html = self.cli('worked', '--verbose', preset=None, query=query, fmt='html')
        text = self.cli('worked', '--verbose', preset=None, query=query, fmt='text')
        expected = self.service.investigate('latest', package_id=self.package, query=query)
        self.assertEqual(data['totals'], expected.totals)
        self.assertEqual(data['effective_query'], expected.effective_query)
        self.assertEqual([e['identity'] for e in data['records']], [e['identity'] for e in expected.records])
        self.assertEqual([e['history'] for e in data['records']], [e['history'] for e in expected.records])
        self.assertEqual(len(data['window']['runs']), min(5, len(self.order['runs'])))
        for entry in data['records'] + data['historical']:
            self.assertIn(entry['message'], text)
            self.assertIn(escape(entry['message'], quote=False), html)
            self.assertIn(escape(entry['template_text'], quote=False), html)
            self.assertTrue(entry['candidates'])
        for run in data['window']['runs']:
            self.assertEqual(sum(run['identity_counts'].values()), run['occurrences'])
            self.assertIn(run['run_id'], text)
            self.assertIn(run['timestamp'], html)
            self.assertLessEqual(len(run['records']), 3)
        self.assertEqual(data['window']['runs'][-1]['occurrences'], data['totals']['occurrences'])
        self.assertEqual(data['window']['totals']['occurrences'], sum(r['occurrences'] for r in data['window']['runs']))
        self.assertEqual(data['window']['totals']['distinct_records'], len({
            key for r in data['window']['runs'] for key in r['identity_counts']}))
        for bucket in data['window']['rollups']['candidate_files']['buckets']:
            members = [b for r in data['window']['runs'] for b in r['rollups']['candidate_files']['buckets'] if b['key'] == bucket['key']]
            self.assertEqual(bucket['occurrences'], sum(b['occurrences'] for b in members))
            self.assertEqual(bucket['distinct_records'], len({key for b in members for key in b['identity_keys']}))
        main = HTMLLinks(html)
        for index, entry in enumerate(data['records'], 1):
            visible = ''.join(main.visible_diagnostics[f'D{index}'])
            self.assertIn('Specific diagnostic recorded in Run', visible)
            self.assertNotIn('Match status: matched template', visible)
            for candidate in entry['candidates']:
                member = candidate['member']
                if member and member['root_ID'] != 'ROOT_GAME':
                    self.assertIn(member['name'], visible)
                    self.assertIn(str(member['load_order']), visible)
                    self.assertIn(candidate['relative_path'], visible)
                elif member:
                    self.assertIn(candidate['relative_path'], visible)
                    self.assertNotIn(member['name'] + ' — recorded load order', visible)
        appendix_text = (self.out / 'worked-sources.html').read_text(encoding='utf-8')
        appendix = HTMLLinks(appendix_text)
        self.assertFalse(main.scripts + appendix.scripts)
        for href in main.links + appendix.links:
            parsed = urlsplit(href)
            self.assertFalse(parsed.scheme, href)
            if parsed.fragment:
                target = main if not parsed.path or unquote(parsed.path) == 'worked.html' else appendix
                # Fragment-only links in the main document target main sections.
                self.assertIn(parsed.fragment, target.ids, href)
        self.assertIn('worked-sources.html#source-', html)
        for run in data['window']['runs']:
            for entry in run['records']:
                for c in entry['candidates']:
                    self.assertIn(str(c['member']['load_order']), html)
                    for excerpt in c.get('excerpts', []):
                        if not excerpt['available']:
                            continue
                        actual = Path(c['physical_path']).read_text(encoding='utf-8-sig').splitlines()
                        self.assertEqual(excerpt['lines'][0]['line'], max(1, excerpt['line'] - 10))
                        self.assertEqual(excerpt['lines'][-1]['line'], min(len(actual), excerpt['line'] + 10))
                        for line in excerpt['lines']:
                            self.assertEqual(line['text'], actual[line['line'] - 1])
                            self.assertIn(escape(line['text'], quote=False), appendix_text)
        limited = self.cli('worked-limit-zero', '--limit', 0, '--historical-limit', 0, preset=None, query=query)
        self.assertEqual(limited['totals'], data['totals'])
        self.assertEqual(limited['window']['runs'][-1]['identity_counts'], data['window']['runs'][-1]['identity_counts'])
        self.assertEqual(limited['rollups'], data['rollups'])
        # Retained complete worked example: current/historical/per-Run sets fit this bound.
        self.cli('worked-full', '--limit', 200, '--historical-limit', 200, '--verbose', preset=None, query=query, fmt='html')

    def test_03_member_file_exact_and_optional_context(self):
        message = {'contains': 'failed context switch'}
        source = {'files': ['common/on_action/sea_minority_on_actions.txt']}
        q = {'scope': {'source': source}, 'refinement': {'message': message}, 'analytics': {'trailing_runs': 5}}
        files = self.cli('file-scope', query=q)
        self.assertEqual(files['totals']['distinct_records'], 2)
        self.assertEqual(files['totals']['occurrences'], 64)
        self.assertEqual([c['member']['load_order'] for c in files['records'][0]['candidates']], [114, 115])
        scopes = files['coverage']['source'][self.latest]['metrics']['inventory_scopes']
        self.assertTrue(scopes)
        self.assertTrue(all(s['directories'] == ['common/on_action'] and not s['recursive'] for s in scopes))
        q['scope']['source']['members'] = [{'load_order': 115}]
        combined = self.cli('member-file', query=q)
        self.assertEqual(combined['totals'], files['totals'])
        self.assertEqual([c['member']['load_order'] for c in combined['records'][0]['candidates']], [115])
        q['refinement']['identities'] = [files['records'][0]['identity']]
        exact = self.cli('member-file-exact', query=q)
        self.assertEqual(exact['totals']['distinct_records'], 1)
        q['scope']['source'] = {'members': [{'name': 'EB+EC724 Compatibility Patch'}]}
        del q['refinement']['identities']
        mod = self.cli('member-only', query=q)
        self.assertEqual(mod['totals']['occurrences'], 84)
        self.assertEqual(mod['totals']['distinct_records'], 15)
        q['scope']['source'] = {'referenced_paths': source['files']}
        references = self.cli('stored-reference-context', query=q)
        self.assertEqual(references['totals'], files['totals'])
        self.assertEqual(references['records'][0]['candidates'], files['records'][0]['candidates'])
        sql_only = DiagnosticAnalysis(self.client, source_resolver=SourceSearch(self.client)).investigate('latest', package_id=self.package, query=q)
        self.assertEqual(sql_only.coverage['source'][self.latest]['metrics']['inventory_builds'], 0)
        outside = self.config.get('external_root')
        if outside:
            outside_entry = next((e for e in self.baseline.records if any(
                (Path(outside) / ref['path']).is_file()
                for ref in source_references(e['stored_record'])['references'])), files['records'][0])
            explicit = self.cli('outside-playset', '--source-root', outside, query={
                'refinement': {'identities': [outside_entry['identity']]}, 'analytics': {'history': False}})
            # An explicit root is a context scope, not a promise that this record
            # has a file there. Use actual files to establish expected candidates.
            expected_paths = {str(Path(outside) / ref['path']) for ref in
                source_references(outside_entry['stored_record'])['references']
                if (Path(outside) / ref['path']).is_file()}
            self.assertEqual({os.path.normcase(c['physical_path']) for c in explicit['records'][0]['candidates']},
                             {os.path.normcase(p) for p in expected_paths})
            self.assertTrue(all(c['member'] is None for c in explicit['records'][0]['candidates']))

    def test_04_template_binding_grouped_message_and_successful_empty(self):
        chosen = next(e for e in self.baseline.records if 'failed context switch' in e['message'].casefold())
        base = {'identities': [chosen['identity']]}
        q = {'refinement': {**base, 'message': {'and': [{'contains': 'failed context switch'},
              {'or': [{'contains': 'trigger'}, {'contains': 'effect'}]}, {'not_contains': 'unrepresented literal'}]}},
              'analytics': {'history': False}}
        exact = self.cli('grouped-message', preset=None, query=q)
        self.assertEqual(exact['totals']['distinct_records'], 1)
        pattern = chosen['template_text']
        q['refinement']['template_text'] = {'and': [{'contains': pattern[:8]}, {'contains': pattern[-8:]}]}
        q['refinement']['template_exact'] = [pattern]
        q['refinement']['templates'] = [chosen['identity']['definition']]
        binding = next(b for r in chosen['stored_record']['values']['regions'] for b in r['bindings'] if b['type'] == 'KEY' and b['present'])
        q['refinement']['bindings'] = [{'type': 'KEY', 'value': binding['value']}]
        result = self.cli('symbol-exact-partial-key', preset='symbol', query=q)
        self.assertEqual(result['records'][0]['identity'], chosen['identity'])
        templates = list(dict.fromkeys(e['identity']['definition']['template_id'] for e in self.baseline.records))[:2]
        selected = self.cli('template-or', preset='symbol', query={'refinement': {'templates': [{'template_id': t} for t in templates]}, 'analytics': {'history': False}})
        wanted = [e for e in self.baseline.records if e['identity']['definition']['template_id'] in templates]
        self.assertEqual(selected['totals']['distinct_records'], len(wanted))
        self.assertEqual(selected['totals']['occurrences'], sum(e['selected_count'] for e in wanted))
        # Template summaries include every matching exact record, even when the
        # displayed diagnostic list is bounded or omitted entirely.
        self.assertTrue(selected['rollups']['templates']['buckets'])
        for bucket in selected['rollups']['templates']['buckets']:
            reference = {k: bucket['template'][k] for k in ('template_id', 'model_revision', 'contract_version')}
            contributors = [e for e in wanted if e['identity']['definition'] == reference]
            self.assertEqual(bucket['occurrences'], sum(e['selected_count'] for e in contributors))
            self.assertEqual(bucket['distinct_records'], len(contributors))
            self.assertEqual(set(bucket['identity_keys']), {e['identity_key'] for e in contributors})
            self.assertTrue(all(e['template_text'] == bucket['template']['text'] for e in contributors))
        limited = self.cli('template-summary-no-details', '--limit', 0, '--historical-limit', 0,
                           preset='symbol', query={'refinement': {'templates': [{'template_id': t} for t in templates]},
                                                   'analytics': {'history': False}})
        self.assertEqual(limited['rollups']['templates'], selected['rollups']['templates'])
        self.assertEqual(limited['window']['rollups']['templates'], selected['window']['rollups']['templates'])
        self.assertEqual(limited['records'], [])

    def test_05_presets_and_contradictions(self):
        syntax = self.cli('syntax', preset='syntax', query={'analytics': {'history': False}})
        pairs = {(t, f) for t, f, _ in SYNTAX_ROWS}
        def is_syntax(e):
            row = e['stored_record']
            d = row['definition']
            if (d['template_id'], d['source_family']) not in pairs:
                return False
            return d['template_id'] != '0b2804538785c71278ea37e7' or any(
                r['name'] == 'body' and b['slot_id'] == 's1' and b['type'] == 'REASON' and b['present'] and b['value'] == ASSIGNMENT_REASON
                for r in row['values']['regions'] for b in r['bindings'])
        wanted = [e for e in self.baseline.records if is_syntax(e)]
        self.assertEqual(syntax['totals']['distinct_records'], len(wanted))
        self.assertEqual({e['identity_key'] for e in syntax['records']}, {e['identity_key'] for e in wanted})
        # Every well-formed conjunction can complete, including an empty set.
        empty = self.cli('syntax-empty', preset='syntax', query={'refinement': {'message': {'contains': 'failed context switch'}}, 'analytics': {'history': False}})
        self.assertEqual(empty['totals']['distinct_records'], 0)
        opposing = self.cli('syntax-contradiction', preset='syntax', query={'scope': {'source_families': ['jomini_effect.cpp']}})
        self.assertEqual(opposing['totals']['distinct_records'], 0)
        self.cli('syntax-unsupported', '--package-id', 'unrepresented-package', preset='syntax', expected=2)
        for name, preset, query in (
                ('new-contradiction', 'new', {'refinement': {'newly_observed': False}}),
                ('hotspots-contradiction', 'hotspots', {'scope': {'has_source_reference': False}})):
            opposing = self.cli(name, preset=preset, query=query)
            self.assertEqual(opposing['status'], 'completed')
            self.assertEqual(opposing['totals'], {'occurrences': 0, 'distinct_records': 0, 'historical_entries': 0})
            self.assertTrue(all(r['occurrences'] == 0 for r in opposing['window']['runs']))
            # Both the user's filter and the preset condition remain exported.
            for section, filters in query.items():
                for field, value in filters.items():
                    self.assertEqual(opposing['effective_query'][section][field], value)
            self.assertTrue(opposing['effective_query']['refinement']['all'])
        constrained = self.cli('new-zero-count', preset='new', query={'refinement': {'occurrences': {'max': 0}}})
        self.assertEqual(constrained['totals']['distinct_records'], 0)
        missing = self.cli('symbol-needs-selector', preset='symbol', run=self.latest, expected=2)
        self.assertEqual(missing['failure_stage'], 'input_validation')
        self.assertIn('no investigation was submitted', ' '.join(missing['explanation']['result']))
        hot = self.cli('hotspots', '--limit', 2, preset='hotspots', query={'analytics': {'history': False}})
        wanted = [e for e in self.baseline.records if source_references(e['stored_record'])['references']]
        self.assertEqual(hot['totals']['distinct_records'], len(wanted))
        self.assertEqual(hot['totals']['occurrences'], sum(e['selected_count'] for e in wanted))
        self.assertTrue(hot['rollups']['candidate_files']['overlapping_records'])

    def test_06_newness_and_previously_observed(self):
        result = self.cli('new', '--limit', 2000, preset='new')
        expected = {e['identity_key'] for e in self.baseline.records if e['history']['newly_observed']}
        self.assertEqual({e['identity_key'] for e in result['records']}, expected)
        oldest = self.order['runs'][-1]['run_id']
        single = self.cli('selected-only-new', '--limit', 1, preset='new', run=oldest, query={'analytics': {'trailing_runs': 1}})
        self.assertTrue(single['records'][0]['history']['newly_observed'])
        self.assertIsNone(single['records'][0]['history']['preceding_fraction'])
        absent = self.cli('previously-observed', '--limit', 1, '--historical-limit', 2)
        self.assertTrue(absent['historical'])
        self.assertTrue(all(e['selected_count'] == 0 for e in absent['historical']))
        positive = self.cli('positive-excludes-historical', '--limit', 1, query={'refinement': {'occurrences': {'min': 1}}})
        self.assertFalse(positive['historical'])
        self.assertEqual(positive['totals']['occurrences'], absent['totals']['occurrences'])

    def test_07_source_filters_exclude_unlocated_and_nonmatching(self):
        unlocated = next(e for e in self.baseline.records if not source_references(e['stored_record'])['references'])
        located = next(e for e in self.baseline.records if 'sea_minority_on_actions.txt' in e['message'] and 'Failed context switch' in e['message'])
        q = {'refinement': {'identities': [unlocated['identity'], located['identity']]}, 'analytics': {'history': False}}
        optional = self.cli('optional-unlocated', query=q)
        self.assertEqual(optional['totals']['distinct_records'], 2)
        unlocated_entry = next(e for e in optional['records'] if e['identity'] == unlocated['identity'])
        self.assertEqual(unlocated_entry['source_path_status'], 'no_path')
        self.assertNotIn('reference_complete', optional['coverage']['source'][self.latest])
        no_path_query = {'refinement': {'identities': [unlocated['identity']]}, 'analytics': {'history': False}}
        no_path = self.cli('pathless-emission', query=no_path_query)
        self.assertFalse(any('Match recorded file paths' in c for c in no_path['explanation']['conditions']))
        self.assertTrue(any('source lookup is not applicable' in r for r in no_path['explanation']['result']))
        coverage = no_path['coverage']['source'][self.latest]
        self.assertTrue(coverage['complete'])
        self.assertFalse(coverage['searched'])
        self.assertFalse(coverage['issues'])
        self.assertEqual(coverage['search_counts']['files_searched'], 0)
        for fmt in ('text', 'html'):
            rendered = self.cli('pathless-emission', query=no_path_query, fmt=fmt)
            self.assertIn('Source lookup: not applicable. This emission supplies no file path.', rendered)
            self.assertNotIn('Incomplete source coverage', rendered)
        q['scope'] = {'source': {'members': [{'load_order': 115}]}}
        result = self.cli('required-partial', query=q)
        self.assertEqual(result['status'], 'completed')
        self.assertEqual([r['identity'] for r in result['records']], [located['identity']])
        self.assertEqual(result['coverage']['source'][self.latest]['records_without_source_path'], 0)
        readable = self.cli('required-partial', query=q, fmt='text')
        self.assertIn(located['message'], readable)
        self.assertNotIn(unlocated['message'], readable)
        html = self.cli('required-partial', query=q, fmt='html')
        self.assertNotIn('unidentified-records', HTMLLinks(html).ids)
        self.assertNotIn('Occurrences by Run', html)
        self.assertNotIn(unlocated['message'], html)
        q['scope']['source'] = {'files': ['common/on_action/sea_minority_on_actions.txt']}
        path = self.cli('path-excludes-unlocated', query=q)
        self.assertEqual([r['identity'] for r in path['records']], [located['identity']])
        q['refinement']['identities'] = [unlocated['identity']]
        empty = self.cli('path-only-unlocated', query=q)
        self.assertEqual(empty['totals']['distinct_records'], 0)
        self.assertTrue(empty['coverage']['source'][self.latest]['complete'])
        self.assertFalse(empty['coverage']['source'][self.latest]['issues'])

    def test_08_existing_commands_and_html_destination(self):
        for command in ('ingest', 'watch', 'capture', 'doctor', 'runs', 'report'):
            result = subprocess.run([sys.executable, '-I', '-B', '-m', 'ck3chronicle.cli', command, '--help'], capture_output=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stderr)
        reply = subprocess.run([sys.executable, '-I', '-B', '-m', 'ck3chronicle.cli', 'report', 'latest', '--preset', 'frequent', '--format', 'html'], capture_output=True, encoding='utf-8')
        self.assertEqual(reply.returncode, 2)
        self.assertIn('explicit --output', reply.stderr)

    def test_10_relative_path_across_playset(self):
        relative = 'common/on_action/sea_minority_on_actions.txt'
        query = {'purpose': 'Find every diagnostic referencing this relative path across the recorded playset.',
                 'scope': {'source': {'relative_path': {'exact': ['/' + relative]}}},
                 'analytics': {'history': False}}
        original = deepcopy(query)
        expected = [e for e in self.baseline.records if any(
            r['path'] == relative for r in source_references(e['stored_record'])['references'])]
        data = self.cli('relative-path-all-members', preset=None, query=query)
        self.assertEqual(query, original)
        self.assertEqual(data['totals']['occurrences'], sum(e['selected_count'] for e in expected))
        self.assertEqual(data['totals']['distinct_records'], len(expected))
        self.assertEqual(data['totals']['occurrences'], 64)
        self.assertEqual(data['totals']['distinct_records'], 2)
        self.assertEqual([r['identity'] for r in data['records']], [r['identity'] for r in expected])
        coverage = data['coverage']['source'][self.latest]
        self.assertTrue(coverage['complete'])
        self.assertEqual(len(coverage['roots']), 133)
        scopes = coverage['metrics']['inventory_scopes']
        self.assertTrue(scopes)
        self.assertTrue(all(s['directories'] == ['common/on_action'] and not s['recursive'] for s in scopes))
        for record in data['records']:
            self.assertEqual([c['member']['load_order'] for c in record['candidates']], [114, 115])
            self.assertTrue(all(c['relative_path'] == relative for c in record['candidates']))
            self.assertTrue(record['file_line_sources'])
            for source in record['file_line_sources']:
                self.assertEqual(source['rule'], 'last_load_order')
                self.assertEqual(source['error_source']['member']['load_order'], 115)
                self.assertEqual(source['error_source']['physical_path'], record['candidates'][-1]['physical_path'])
        for fmt in ('text', 'html'):
            rendered = self.cli('relative-path-all-members', '--verbose', preset=None, query=query, fmt=fmt)
            self.assertIn('optional leading /', rendered)
            self.assertIn('Error source', rendered)
            self.assertIn('Mod name', rendered)
            self.assertNotIn('recorded load order', rendered)
            self.assertNotIn('Current file candidate', rendered)
            for record in data['records']:
                self.assertIn(escape(record['message'], quote=False) if fmt == 'html' else record['message'], rendered)
                for candidate in record['candidates']:
                    name = candidate['member']['name']
                    self.assertIn(escape(name, quote=False) if fmt == 'html' else name, rendered)
        # Both spellings are the same stored filter, including without any disk lookup.
        sql_only = DiagnosticAnalysis(self.client, source_resolver=SourceSearch(self.client)).investigate(
            'latest', package_id=self.package, query=query)
        self.assertEqual(sql_only.totals, data['totals'])
        self.assertFalse(sql_only.coverage['source'][self.latest]['searched'])
        for name, path in [('relative-path-no-slash', relative), ('relative-path-backslashes', relative.replace('/', '\\'))]:
            query['scope']['source']['relative_path']['exact'] = [path]
            equivalent = self.cli(name, preset=None, query=query)
            self.assertEqual(equivalent['totals'], data['totals'])
            self.assertEqual(equivalent['records'], data['records'])
        # The same basename at another relative location is a different query.
        query['scope']['source']['relative_path']['exact'] = ['/common/scripted_effects/sea_minority_on_actions.txt']
        wrong_parent = self.cli('relative-path-other-directory', preset=None, query=query)
        self.assertEqual(wrong_parent['totals']['distinct_records'], 0)
        self.assertFalse(wrong_parent['coverage']['source'][self.latest]['searched'])
        # Standalone source search and cached scopes obey the same relative location.
        sources = SourceSearch(self.client)
        selection = {'relative_path': {'exact': ['/' + relative]}, 'directories': ['/common/on_action']}
        current = sources.search(selection, run_id=self.latest)
        self.assertEqual([f['member']['load_order'] for f in current['files']], [114, 115])
        self.assertEqual(current['effective_selection']['relative_path']['exact'], [relative])
        self.assertEqual(selection['relative_path']['exact'], ['/' + relative])
        self.assertEqual(sources.search(selection, run_id=self.latest)['files'], current['files'])
        # Explicit physical-file access keeps its existing separate meaning.
        physical = current['files'][0]['physical_path']
        explicit = sources.search({'files': [physical]}, run_id=self.latest)
        self.assertEqual([f['physical_path'] for f in explicit['files']], [physical])

    def test_09_current_path_resolution(self):
        unlocated = next(e for e in self.baseline.records if not source_references(e['stored_record'])['references'])
        located = next(e for e in self.baseline.records if 'sea_minority_on_actions.txt' in e['message'] and 'Failed context switch' in e['message'])
        q = {'refinement': {'identities': [unlocated['identity'], located['identity']]},
             'analytics': {'history': False}, 'scope': {'source': {'resolution': 'resolved'}}}
        resolved = self.cli('resolved-paths', query=q)
        self.assertEqual([r['identity'] for r in resolved['records']], [located['identity']])
        self.assertEqual(resolved['totals']['occurrences'], located['selected_count'])
        entry = resolved['records'][0]
        self.assertTrue(all(r['status'] == 'resolved' for r in entry['reference_resolution']))
        self.assertEqual({c['member']['load_order'] for c in entry['candidates']}, {114, 115})
        for fmt in ('text', 'html'):
            rendered = self.cli('resolved-paths', query=q, fmt=fmt)
            self.assertIn('Resolved', rendered)
            self.assertNotIn('Resolved: current file found', rendered)
            self.assertNotIn(unlocated['message'], rendered)
        q['scope']['source']['resolution'] = 'unresolved'
        unresolved = self.cli('unresolved-excludes-existing-and-pathless', query=q)
        self.assertEqual(unresolved['totals']['distinct_records'], 0)
        self.assertTrue(unresolved['coverage']['source'][self.latest]['complete'])
        self.cli('unresolved-excludes-existing-and-pathless', query=q, fmt='html')
        # Optional content that matches no file must not label an existing path missing.
        context = self.out / 'resolution-context.json'
        context.write_text(json.dumps({'content': {'contains': '__08B_NO_SUCH_SOURCE_TOKEN__'}}), encoding='utf-8')
        optional = self.cli('resolution-content-independent', '--source-context', context,
                            query={k: v for k, v in q.items() if k != 'scope'})
        found = next(r for r in optional['records'] if r['identity'] == located['identity'])
        self.assertFalse(found['candidates'])
        self.assertTrue(all(r['status'] == 'resolved' for r in found['reference_resolution']))
        html = self.cli('resolution-content-independent', '--source-context', context,
                        query={k: v for k, v in q.items() if k != 'scope'}, fmt='html')
        self.assertIn('Resolved', html)
        self.assertNotIn('>File not found<', html)
        self.assertEqual(found['file_line_sources'][0]['error_source']['member']['load_order'], 115)
        self.assertIn('EB+EC724 Compatibility Patch', html)


    def test_12_requested_history_positions_include_unavailable_runs(self):
        chronological = list(reversed(self.order['runs']))
        selected_index = len(chronological) // 2
        selected = chronological[selected_index]['run_id']
        query = {'refinement': {'message': {'contains': 'failed context switch'}}}
        result = self.cli('history-positions', '--limit', 2, preset=None, query=query, run=selected)
        positions = result['window']['positions']
        self.assertEqual([p['offset'] for p in positions], list(range(-5, 6)))
        for position in positions:
            index = selected_index + position['offset']
            available = 0 <= index < len(chronological)
            self.assertEqual(position['available'], available)
            self.assertEqual(position['run_id'], chronological[index]['run_id'] if available else None)
        self.assertTrue(any(not p['available'] for p in positions), 'Requires genuine short window')
        self.assertFalse(result['coverage']['comparison_errors'])
        self.assertFalse(result['coverage']['comparison_unavailable'])
        for fmt in ('html', 'text'):
            output = self.cli('history-positions', '--limit', 2, preset=None, query=query, run=selected, fmt=fmt)
            for offset in range(-5, 6):
                self.assertIn('Run 0 (selected)' if offset == 0 else f'Run {offset:+d}', output)
            self.assertIn('Not available', output)
            for run in result['window']['runs']:
                self.assertIn(run['run_id'], output)

    def test_11_whole_message_search_and_stored_match_origins(self):
        origins_seen = set()
        for name, term in (('message-unrecognized', 'unrecognized'),
                           ('message-context-switch', 'failed context switch')):
            q = {'refinement': {'message': {'contains': term}}, 'analytics': {'history': False}}
            result = self.cli(name, '--limit', 8, preset=None, query=q)
            wanted = [e for e in self.baseline.records if term.casefold() in e['message'].casefold()]
            self.assertTrue(wanted, 'No genuine example for ' + term)
            self.assertEqual(result['totals']['distinct_records'], len(wanted))
            self.assertEqual(result['totals']['occurrences'], sum(e['selected_count'] for e in wanted))
            summaries = result['rollups']['message_matches']['buckets']
            self.assertTrue(summaries)
            for bucket in summaries:
                origins_seen.add(bucket['message_match']['kind'])
                contributors = [e for e in wanted if e['identity_key'] in bucket['identity_keys']]
                self.assertEqual(bucket['distinct_records'], len(contributors))
                self.assertEqual(bucket['occurrences'], sum(e['selected_count'] for e in contributors))
                self.assertEqual({json.dumps(t, sort_keys=True) for t in bucket['templates']},
                                 {json.dumps(e['identity']['definition'], sort_keys=True) for e in contributors})
            for entry in result['records']:
                original = next(e for e in wanted if e['identity'] == entry['identity'])
                self.assertEqual(entry['message'], original['message'])
                parts = render_segments(entry['stored_record']['definition'], entry['stored_record']['values'])
                self.assertEqual(''.join(p['text'] for p in parts), original['message'])
                self.assertTrue(entry['message_matches'])
                for match in entry['message_matches']:
                    self.assertEqual(entry['message'][match['start']:match['end']].casefold(), term.casefold())
                    self.assertEqual(''.join(o['text'] for o in match['origins']), match['text'])
                    for origin in match['origins']:
                        self.assertEqual(entry['message'][origin['start']:origin['end']], origin['text'])
                        if origin['kind'] == 'slot':
                            binding = next(b for r in entry['stored_record']['values']['regions']
                                           if r['name'] == origin['region'] for b in r['bindings']
                                           if b['slot_id'] == origin['slot_id'])
                            self.assertEqual(binding['type'], origin['type'])
                            self.assertIn(origin['text'], binding['value'])
            for fmt in ('html', 'text'):
                output = self.cli(name, '--limit', 8, preset=None, query=q, fmt=fmt)
                self.assertIn('Where the search matched', output)
                self.assertIn('Assigned template', output)
                for bucket in summaries:
                    self.assertIn(str(bucket['distinct_records']), output)
                    for ref in bucket['templates']:
                        self.assertIn(ref['template_id'], output)
            limited = self.cli(name + '-summary', '--limit', 0, preset=None, query=q)
            self.assertEqual(limited['rollups']['message_matches'], result['rollups']['message_matches'])
            self.assertEqual(limited['totals'], result['totals'])
        self.assertEqual(origins_seen, {'slot', 'literal'}, 'Genuine queries must demonstrate both origins')


if __name__ == '__main__':
    unittest.main()
