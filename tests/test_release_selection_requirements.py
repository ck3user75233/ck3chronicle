"""Task 07C: exact retained code selection and explicit integrity failures.

Native parity uses owner-retained evidence supplied by environment, never fixtures.
Disposable corruption tests test authentication only, not matching behavior.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import unittest
import uuid

from template_learning.learner_loader import authenticate, resolve_release, ReleaseError
from ck3chronicle.pipeline.catalog import load_selected_package, list_releases, evaluate_package

ROOT = Path(__file__).resolve().parents[1]


class ReleaseSelectionRequirements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT/'learners/catalog.json').read_bytes())
        cls.complete = next(r for r in cls.catalog['releases'] if r['availability']=='available')
        cls.source, cls.pin = resolve_release(ROOT/'learners', cls.complete['release_id'])
        cls.output = ROOT/'.codex-tmp/task07c-releases/tests'/uuid.uuid4().hex
        cls.output.mkdir(parents=True)

    def copy(self, name):
        target=self.output/name
        shutil.copytree(self.source,target)
        return target

    def test_every_registered_learner_authenticates_its_own_bytes(self):
        for row in self.catalog['releases']:
            if row['availability'] not in {'available','partial'}:
                continue
            folder,pin=resolve_release(ROOT/'learners',row['release_id'])
            manifest,payloads=authenticate(folder,pin)
            self.assertEqual(manifest['release_id'],row['release_id'])
            self.assertIn('template_learning/parsers/__init__.py',payloads)
            self.assertIn('template_learning/release_evaluation.py',payloads)

    def test_missing_dependency_fails_without_current_source_fallback(self):
        target=self.copy('missing')
        (target/'template_learning/parsers/__init__.py').unlink()
        with self.assertRaises(ReleaseError):authenticate(target,self.pin)

    def test_changed_dependency_fails_without_current_source_fallback(self):
        target=self.copy('changed')
        with (target/'template_learning/owner_rules.json').open('ab') as stream:stream.write(b' ')
        with self.assertRaises(ReleaseError):authenticate(target,self.pin)

    def test_manifest_disagreement_fails(self):
        with self.assertRaises(ReleaseError):authenticate(self.source,'0'*64)

    def test_incompatible_release_is_not_substituted(self):
        target=self.copy('incompatible')
        manifest=json.loads((target/'manifest.json').read_bytes());manifest['schema_version']=999
        data=json.dumps(manifest).encode();(target/'manifest.json').write_bytes(data)
        with self.assertRaises(ReleaseError):authenticate(target,hashlib.sha256(data).hexdigest())

    def test_absent_learner_selection_is_not_substituted(self):
        with self.assertRaises(ReleaseError):resolve_release(ROOT/'learners','0'*64)

    def test_all_available_model_packages_select_their_own_bootstrap(self):
        for row in list_releases(models_root=ROOT/'models'):
            if row['availability']!='available':continue
            package=load_selected_package(models_root=ROOT/'models',package_id=row['package_id'])
            self.assertEqual(package.manifest_sha256,row['manifest_sha256'])
            self.assertEqual(package.manifest['package_id'],row['package_id'])
            self.assertIn(row['manifest_sha256'],package.parser.__name__)

    def test_conflicting_model_selectors_fail(self):
        with self.assertRaises(ValueError):
            load_selected_package(models_root=ROOT/'models',package_id='0'*24,selection_path=ROOT/'models/selection.json')

    def test_unknown_model_package_fails(self):
        with self.assertRaises(ValueError):load_selected_package(models_root=ROOT/'models',package_id='0'*24)

    @unittest.skipUnless(os.environ.get('CK3CHRONICLE_RELEASE_TEST_LOG'),'supply a genuine retained log')
    def test_all_available_packages_reach_real_contract_preparation(self):
        log=Path(os.environ['CK3CHRONICLE_RELEASE_TEST_LOG'])
        before=(ROOT/'models/selection.json').read_bytes()
        for row in list_releases(models_root=ROOT/'models'):
            if row['availability']!='available':continue
            receipt=evaluate_package(row['package_id'],log,models_root=ROOT/'models')
            self.assertEqual(receipt['lineage']['package_id'],row['package_id'])
            self.assertEqual(receipt['lineage']['package_manifest_sha256'],row['manifest_sha256'])
            self.assertEqual(sum(receipt['counts'].values()),len(receipt['records']))
        self.assertEqual((ROOT/'models/selection.json').read_bytes(),before)


if __name__=='__main__':
    unittest.main()
