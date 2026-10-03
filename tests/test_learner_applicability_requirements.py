"""Replay retained native proposal decisions; no synthetic CK3 evidence."""
import json
import os
import pickle
from pathlib import Path
import unittest

from template_learning.additive_learning import cluster_view, preserve_wording
from template_learning.diagnostic_wording import reject_wording_loss
from template_learning.matching_defaults import RULES
from template_learning.records import identity


@unittest.skipUnless(os.environ.get('CK3_APPLICABILITY_EVIDENCE'), 'requires retained native research evidence')
class ApplicabilityRequirements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(os.environ['CK3_APPLICABILITY_EVIDENCE'])
        cls.events = json.loads((root/'unmatched-73-derivation.json').read_text())['events']
        result = json.loads((root/'additive/result-60.json').read_text())
        cls.previous = json.loads((Path(result['bundle'])/'empirical_template_model.json').read_text())
        with (root/'batch-all-isolated/records.pickle').open('rb') as stream:
            grouped, _ = pickle.load(stream)
        cls.members = {identity(r.key):r for pool in grouped.values() for r in pool}

    def replay(self, event):
        proposal = event['rejection']['proposed_template']
        refs = [cluster_view(t, self.members) for t in self.previous['templates']
                if t['source_family'] == proposal['source_family']
                and t['status'] in {'supported', 'confirmed', 'provisional'}]
        def unexpected_refinement(*args):
            self.fail('this retained decision requires no new inference')
        review = []
        accepted, rejected = preserve_wording(proposal['source_family'], [proposal], refs,
            self.members, .72, unexpected_refinement, review)
        return proposal, refs, accepted, rejected, review

    def test_inapplicable_four_frame_wording_cannot_veto_one_frame_proposal(self):
        event = next(e for e in self.events if 'reference_applicability_checks' in e)
        proposal, refs, accepted, rejected, _ = self.replay(event)
        self.assertTrue(reject_wording_loss(refs, cluster_view(proposal, self.members), path='native_before'))
        self.assertEqual(accepted, [proposal])
        self.assertEqual(rejected, [])
        for check in event['reference_applicability_checks']:
            record = self.members[check['record_id']]
            self.assertFalse(RULES.applies_to_record(proposal, record))
            self.assertIsNone(RULES.match_record(proposal, record))
        for key in proposal['evidence_record_ids']:
            self.assertIsNotNone(RULES.match_record(proposal, self.members[key]))

    def test_same_structure_wording_protection_is_preserved(self):
        for event in self.events:
            if 'reference_applicability_checks' in event:
                continue
            proposal, _, accepted, rejected, review = self.replay(event)
            self.assertEqual(accepted, [])
            self.assertEqual(rejected, [proposal['template_id']])
            self.assertTrue(review)
