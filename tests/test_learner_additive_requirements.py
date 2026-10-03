"""Owner-directed same-version additive learning on complete native logs.

CK3_ADDITIVE_NATIVE_INPUTS is a path/sha256 inventory. The first complete log
starts a candidate; all remaining complete logs extend it. No synthetic messages
or independent identities made from copies are used.
"""
from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import unittest
import uuid

from template_learning import artifacts, inventory, records, clustering, constructions
from template_learning.additive_learning import contract
from template_learning.native_matching import Matcher
from template_learning.parsers import load_parser, reference_from_manifest


def select_evidence(grouped, stats, hashes):
    selected = []
    for pool in grouped.values():
        for record in pool:
            occurrences = [o for o in record.native_occurrences if o['evidence_sha256'] in hashes]
            if not occurrences:
                continue
            context_ids = {o['context_id'] for o in occurrences}
            selected.append(replace(record, native_occurrences=occurrences,
                contexts={key:value for key,value in record.contexts.items() if key in context_ids}))
    return records.group_records(selected), {key:value for key,value in stats.items() if key in hashes}


@unittest.skipUnless(os.environ.get('CK3_ADDITIVE_NATIVE_INPUTS'), 'requires complete native logs')
class AdditiveNativeRequirements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        inputs = json.loads(Path(os.environ['CK3_ADDITIVE_NATIVE_INPUTS']).read_text())
        logs = []
        for row in inputs:
            path = Path(row['path']); stat = path.stat()
            logs.append(inventory.ProtectedLog(row['sha256'], 'protected', path,
                row['sha256'], stat.st_size, stat.st_mtime_ns))
        assert len({log.sha256 for log in logs}) >= 2
        cls.logs = logs
        cls.parser = load_parser(reference_from_manifest(
            Path(__file__).resolve().parents[1]/'tools/template_learning/parsers/v1_7/manifest.json'))
        cls.grouped, cls.stats = records.collect_records(logs, parser=cls.parser)
        cls.first_grouped, cls.first_stats = select_evidence(cls.grouped, cls.stats, {logs[0].sha256})
        cls.first, cls.first_evidence = artifacts.build_model(cls.first_grouped, cls.first_stats, parser=cls.parser)
        cls.combined, cls.evidence = artifacts.build_model(cls.grouped, cls.stats,
            parser=cls.parser, previous_model=cls.first)

    def test_settled_definitions_and_original_evidence_survive(self):
        definitions = {t['template_id']:t for t in self.combined['templates']}
        matcher = Matcher(self.combined)
        old_records = {records.identity(r.key):r for pool in self.first_grouped.values() for r in pool}
        for template in self.first['templates']:
            if template['status'] != 'supported':
                continue
            retained = definitions[template['template_id']]
            self.assertEqual(retained['status'], 'supported')
            if contract(template) != contract(retained):
                for key in template['evidence_record_ids']:
                    self.assertIsNotNone(matcher.rules.match_record(retained, old_records[key]))
        self.assertLessEqual(set(self.first['evidence']), set(self.combined['evidence']))
        self.assertGreater(sum(s['settled_records'] for s in self.combined['learning_update']['sources']), 0)

    def test_provisionals_have_explicit_promotion_or_retirement(self):
        definitions = {t['template_id']:t for t in self.combined['templates']}
        retired = {r['retired_template_id']:r for r in self.combined['template_retirement']}
        changed = 0
        for template in self.first['templates']:
            if template['status'] != 'provisional':
                continue
            key = template['template_id']
            self.assertTrue(key in definitions or key in retired)
            if key in definitions and definitions[key]['status'] == 'supported':
                self.assertTrue(definitions[key]['learning_support']['eligible'])
                changed += 1
            elif key in retired:
                successor = definitions[retired[key]['selected_template_id']]
                self.assertEqual(successor['status'], 'supported')
                self.assertTrue(retired[key]['reason'])
                changed += 1
        self.assertGreater(changed, 0, 'native inputs must exercise provisional maturation')

    def test_provisional_effect_wording_survives_new_trigger_evidence(self):
        matcher = Matcher(self.combined)
        unknown = [r for r in self.grouped['jomini_script_system.cpp']
                   if 'Script location: Unknown' in r.text]
        self.assertEqual(len(unknown), 2, 'requires both original native formulations')
        selected = set()
        for record in unknown:
            _, _, chosen = matcher.inspect_record(record)
            self.assertIsNotNone(chosen)
            template = next(t for t in self.combined['templates']
                            if t['template_id'] == chosen['template_id'])
            word = 'effect' if 'untyped effect' in record.text else 'trigger'
            self.assertIn('untyped '+word, template['display'])
            self.assertNotIn('untyped <KEY>', template['display'])
            self.assertEqual(template['construction_id'], 'untyped-'+word+'-location-unknown')
            self.assertEqual([c['type'] for c in chosen['captures']], ['REASON'])
            self.assertEqual(constructions.recognize(record.source_family, record.text)['id'],
                             template['construction_id'])
            raw = record.text.encode('utf-8', 'surrogateescape')
            for capture in chosen['captures']:
                self.assertEqual(raw[slice(*capture['span'])],
                                 capture['value'].encode('utf-8', 'surrogateescape'))
            selected.add(template['template_id'])
        self.assertEqual(len(selected), 2)

    def test_distinct_slot_values_count_as_examples_and_fields_count_once(self):
        from template_learning.selection_evidence import native_fields
        matcher = Matcher(self.combined)
        members = {records.identity(r.key): r for pool in self.grouped.values() for r in pool}
        exercised, location_only = set(), False
        for template in self.combined['templates']:
            native = [members[key] for key in template['evidence_record_ids']]
            expected = {(r.text, tuple(e['text'] for e in r.continuations)) for r in native}
            self.assertEqual(template['learning_support']['distinct_diagnostic_examples'], len(expected))
            if template['status'] == 'unresolved':
                continue
            masked = set()
            for record in native:
                match = matcher.rules.match_record(template, record)
                self.assertIsNotNone(match)
                tokens = clustering.learning_tokens(record, template['parts'])
                captures = [c for c in match['captures'] if c['span'] is not None]
                self.assertEqual(sum(t[0] == 'field' for t in tokens), len(captures))
                exercised.update(c['type'] for c in captures)
                raw = record.text.encode('utf-8', 'surrogateescape')
                cursor, form = 0, []
                for a, b, kind in sorted(native_fields(record)):
                    if kind == 'LOCATOR' and a >= cursor:
                        form.extend((raw[cursor:a], b'<LOCATOR>')); cursor = b
                form.append(raw[cursor:])
                masked.add(tuple(form))
            if len(expected) > 1 and len(masked) == 1:
                location_only = True
                self.assertTrue(template['learning_support']['eligible'])
        self.assertTrue({'KEY', 'PARAM', 'REASON', 'LOCATOR', 'CHARACTER_FULL_ID'} <= exercised)
        self.assertTrue(location_only, 'requires genuine locator-only variation')

    def test_one_serializable_model_accounts_for_all_occurrences(self):
        Matcher(json.loads(artifacts.canonical_bytes(self.combined)))
        self.assertEqual(sum(self.combined['summary']['training_outcomes'].values()),
                         sum(s['recovered_messages'] for s in self.stats.values()))
        self.assertEqual(self.combined['learning_update']['parent_revision'], self.first['revision_id'])
        destination = Path(__file__).resolve().parents[1]/'.codex-tmp/learner-all-logs-v42/test-bundles'/uuid.uuid4().hex
        folder = artifacts.write_bundle(destination, self.combined, self.evidence,
            parser=self.parser, build_command=['native-additive-requirement-check'])
        saved = json.loads((folder/'native_evidence.json').read_text())
        self.assertEqual(saved, json.loads(json.dumps(self.evidence)))
        from template_learning.inspect_incremental_learning import native_evidence_rows
        streamed = list(native_evidence_rows(folder/'native_evidence.json', retain_occurrences=True))
        self.assertEqual([row for row, _ in streamed], saved['records'])
        self.assertEqual(sum(n for _, n in streamed), self.combined['summary']['messages'])

    def test_continuation_features_account_for_all_original_emissions(self):
        from template_learning import incremental_template_registry as registry
        for sha, stats in self.stats.items():
            grouped, _ = select_evidence(self.grouped, self.stats, {sha})
            feature = dict(schema=registry.FEATURE_SCHEMA, schema_version=registry.FEATURE_SCHEMA_VERSION,
                learner=artifacts.learner_identity(), feature_version=records.FEATURE_VERSION,
                parser=self.parser.reference.to_dict(), record_scope='message', evidence_sha256=sha,
                bytes=stats['bytes'], timestamped_blocks=stats['timestamped_blocks'],
                eligible_occurrences=stats['recovered_messages'], evidence_stats=stats,
                records=[r.to_dict() for pool in grouped.values() for r in pool])
            registry.validate_feature(feature, sha, parser=self.parser)

    def test_registry_continues_cumulative_learning(self):
        from template_learning import incremental_template_registry as registry
        destination = Path(__file__).resolve().parents[1]/'.codex-tmp/learner-all-logs-v42/test-registries'/uuid.uuid4().hex
        destination.mkdir(parents=True)
        folder = artifacts.write_bundle(destination/'revisions', self.first, self.first_evidence,
            parser=self.parser, build_command=['native-additive-registry-check'])
        manifest = json.loads((folder/'manifest.json').read_text())
        state = registry.empty_registry()
        state['parser'] = self.parser.reference.to_dict()
        state['current_revision'] = self.first['revision_id']
        state['revisions'] = [dict(created_at=registry.utc_now(), **manifest)]
        for log in self.logs:
            feature = registry.feature_from_log(log, parser=self.parser)
            cache = registry.feature_cache_path(destination, log.sha256, parser=self.parser)
            registry.write_json(cache, feature)
            state['evidence'][log.sha256] = dict(sha256=log.sha256, role='training', bytes=log.bytes,
                observed_paths=[dict(path=str(log.path),kind=log.kind,evidence_id=log.evidence_id)],
                feature_caches={registry.feature_key(self.parser):dict(
                    path=cache.relative_to(destination).as_posix(), sha256=inventory.sha256_file(cache))})
        registry.write_json(destination/'registry.json', state)
        result = registry.build_revision(destination, parser=self.parser)
        model, _ = artifacts.load_bundle(Path(result['bundle']))
        self.assertEqual(model['learning_update']['parent_revision'], self.first['revision_id'])
        self.assertEqual(model['summary']['training_outcomes'], self.combined['summary']['training_outcomes'])

    def test_foreign_implementation_and_removed_evidence_are_rejected(self):
        foreign = deepcopy(self.first)
        foreign['algorithm']['learner_identity']['sha256'] = 'foreign-implementation'
        with self.assertRaisesRegex(ValueError, 'implementation'):
            artifacts.build_model(self.grouped, self.stats, parser=self.parser, previous_model=foreign)
        with self.assertRaisesRegex(ValueError, 'cumulative'):
            artifacts.build_model({}, {}, parser=self.parser, previous_model=self.first)
        with self.assertRaisesRegex(ValueError, 'threshold'):
            artifacts.build_model(self.grouped, self.stats, parser=self.parser,
                                  threshold=.8, previous_model=self.first)


if __name__ == '__main__':
    unittest.main()
