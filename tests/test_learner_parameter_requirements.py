"""Outer diagnostic requirements on a complete real-native candidate bundle.

Set CK3_LEARNER_NATIVE_BUNDLE. No synthetic or recombined messages are used.
"""
import os
import json
from collections import defaultdict
from pathlib import Path
import unittest
from template_learning.artifacts import load_bundle
from template_learning.clustering import comparable, learning_tokens
from template_learning.inspect_incremental_learning import native_evidence_rows
from template_learning.patterns import derive_pattern, match_pattern, analyze_match_pattern, parameter_piece_ranges, key_piece_sequence
from template_learning.records import SequenceRecord
from template_learning.literal_guidance import LITERAL_WORDING, guided_piece_indices
from template_learning.regions import span_variation


@unittest.skipUnless(os.environ.get('CK3_LEARNER_NATIVE_BUNDLE'),'requires a complete native bundle')
class NativeOuterRequirements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=Path(os.environ['CK3_LEARNER_NATIVE_BUNDLE'])
        cls.model,_=load_bundle(cls.folder)
        cls.patterns={p['template_id']:p for p in cls.model['templates']}
        cls.field_members={tid:{p['name']:{m['record_id']:m for m in p['field_support']['members']}
                               for p in template['parts'] if p['kind']=='slot'} for tid,template in cls.patterns.items()}
        cls.rows=[row for row,_ in native_evidence_rows(cls.folder/'native_evidence.json')]
        cls.records={r['record_id']:SequenceRecord(r['source_family'],r['native'],tuple(map(tuple,r['pieces'])),r['context_kind']) for r in cls.rows}

    def test_complete_diagnostic_contract(self):
        self.assertEqual(self.model['schema_version'],3)
        self.assertNotIn('layers_by_source',self.model)
        self.assertFalse(self.model['diagnostic_policy']['detached_component_learning'])
        for p in self.patterns.values():self.assertFalse(p['context_kind'].startswith('layer:'))

    def test_presumed_literal_guidance_is_disabled_everywhere(self):
        self.assertFalse(self.model['owner_rules']['default_literals']['enabled'])
        self.assertFalse(self.model['literal_guidance']['enabled'])
        self.assertEqual(self.model['literal_guidance']['literals'],[])
        self.assertEqual(LITERAL_WORDING,())
        for record in self.records.values():
            self.assertEqual(guided_piece_indices(record.pieces),[])
        for pattern in self.patterns.values():
            for part in pattern['parts']:
                if part['kind']=='slot':self.assertEqual(part['constraints']['literal_guidance'],[])

    def test_single_example_cannot_yield_full_outcome(self):
        provisional=0
        for pattern in self.patterns.values():
            support=pattern['learning_support']
            self.assertEqual(support['eligible'],support['distinct_nonlocation_examples']>=2)
            self.assertLessEqual(support['distinct_nonlocation_examples'],pattern['unique_messages'])
            if support['distinct_nonlocation_examples']<2:
                provisional+=1
                self.assertEqual(pattern['status'],'provisional')
        self.assertGreater(provisional,0)
        for row in self.rows:
            if row['outcome']=='full':
                self.assertTrue(self.patterns[row['matches'][0]['template_id']]['learning_support']['eligible'])
            if len(row['matches'])==1 and not row['capture_ambiguities'] and row['matches'][0]['template_status']=='provisional':
                self.assertEqual(row['outcome'],'provisional')
                self.assertIn('insufficient_distinct_learning_examples',row['provisional_reasons'])

    def test_native_brace_singleton_remains_provisional(self):
        row=next(r for r in self.rows if r['native'].startswith('Failed to read key reference: }: },'))
        pattern=self.patterns[row['matches'][0]['template_id']]
        self.assertEqual(pattern['learning_support']['distinct_nonlocation_examples'],1)
        self.assertEqual(pattern['unique_messages'],1)
        self.assertGreater(pattern['support_occurrences'],1)
        self.assertEqual(pattern['status'], 'provisional')

    def test_equal_length_native_mesh_spans_need_no_whitespace_or_nesting(self):
        # Actual member interiors, not synthetic strings or reconstructed logs.
        groups=[]
        for pattern in self.patterns.values():
            if 'for mesh [' not in pattern['display']:continue
            for part in pattern['parts']:
                if not part.get('empirical_region'):continue
                values=[]
                for member in part['field_support']['members']:
                    p=self.records[member['record_id']].pieces[slice(*member['pieces'])]
                    if sum(k=='token' for k,_ in p)==5 and not any(k=='gap' for k,_ in p):values.append(p)
                if len(set(values))>=2:groups.append(values)
        self.assertTrue(groups)
        for values in groups:
            facts=span_variation(values,atomic=[key_piece_sequence(p) for p in values])
            self.assertEqual(facts['raw_token_counts'],[5])
            self.assertFalse(facts['observed_length_variation'])
            self.assertTrue(facts['supported'])

    def test_native_outer_parent_region_is_opaque(self):
        # Complete native messages reviewed by the owner, not recombinations.
        values=['Agrippina Octavianus of  (Internal ID: 59 - Historical ID julio_claudian_021)',
                '(no character)']
        for value in values:
            rows=[r for r in self.rows if r['source_family']=='characterhistory.cpp'
                  and r['native'].startswith(' Parent ('+value+') of ')]
            self.assertTrue(rows,value)
            for row in rows:
                self.assertTrue(row['matches'],row['record_id'])
                rec=self.records[row['record_id']]
                words=[t for _,t in learning_tokens(rec)]
                self.assertNotIn('Internal',words)
                self.assertNotIn('Historical',words)
                a=len(' Parent ('.encode());b=a+len(value.encode())
                for match in row['matches']:
                    captures=[c for c in match['captures'] if c['span'] and c['span'][0]<b and a<c['span'][1]]
                    self.assertEqual([(c['type'],c['span'],c['value']) for c in captures],[('PARAM',[a,b],value)])

    def test_empirical_regions_have_native_outer_boundary_evidence(self):
        found=0
        for pattern in self.patterns.values():
            for part in pattern['parts']:
                region=part.get('empirical_region')
                if not region:continue
                found+=1
                self.assertEqual(part['type'],'PARAM')
                self.assertGreaterEqual(region['distinct_nonempty'],2)
                self.assertTrue(region['multi_token_content'])
                for member in part['field_support']['members']:
                    rec=self.records[member['record_id']];a,b=member['pieces']
                    self.assertEqual(rec.pieces[a-1],('token',region['opener']))
                    self.assertEqual(rec.pieces[b],('token',region['closer']))
        self.assertGreater(found,0)

    def test_single_native_character_description_does_not_prove_param(self):
        row=next(r for r in self.rows if r['source_family']=='characterhistory.cpp'
                 and r['native'].startswith(' Parent (Agrippina Octavianus of '))
        rec=self.records[row['record_id']]
        parts,failures=derive_pattern([rec],rec)
        self.assertFalse(failures)
        self.assertFalse(any(p.get('type')=='PARAM' for p in parts))
        self.assertIn('Agrippina Octavianus of', ''.join(p['text'] for p in parts if p['kind']=='literal'))

    def test_ordinary_param_has_positive_raw_span_evidence(self):
        count=0
        for pattern in self.patterns.values():
            for part in pattern['parts']:
                if part.get('type')!='PARAM' or part.get('parameter_definition') or part.get('empirical_region'):
                    continue
                pieces=[self.records[m['record_id']].pieces[slice(*m['pieces'])]
                        for m in part['field_support']['members']]
                self.assertTrue(span_variation(pieces,atomic=[key_piece_sequence(tuple(p for p in ps if p[0]!='gap')) for ps in pieces])['supported'],(pattern['display'],part['name']))
                count+=1
        self.assertGreater(count,0)

    def test_punctuation_outlier_does_not_retype_native_key_references(self):
        selected=[r for r in self.rows if r['source_family']=='pdx_persistent_reader.cpp'
                  and r['native'].startswith('Failed to read key reference: ')]
        self.assertTrue(selected)
        brace=False;ordinary=False
        for row in selected:
            self.assertTrue(row['matches'])
            for match in row['matches']:
                self.assertFalse(any(c['type']=='PARAM' for c in match['captures']))
                if row['native'].startswith('Failed to read key reference: }: },'):
                    brace=True
                    self.assertTrue(any(p['kind']=='literal' and '}: }' in p['text']
                                        for p in self.patterns[match['template_id']]['parts']))
                if 'always_bce_cadet_branch' in row['native']:
                    ordinary=True
                    self.assertEqual([c['value'] for c in match['captures'] if c['type'] in {'KEY','OPTIONAL_KEY'}],
                                     ['always_bce_cadet_branch']*2)
        self.assertTrue(brace and ordinary)

    def test_native_reference_qualification_is_preserved_inside_key(self):
        rows=[r for r in self.rows if r['source_family']=='pdx_data_factory.cpp'
              and r['native'].startswith(" Could not find promote for '")]
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row['outcome'],'full')
            match=row['matches'][0]
            self.assertTrue(all(c['type']=='KEY' for c in match['captures']))
            self.assertEqual(len(match['captures']),2)
            if "'scope:" in row['native']:
                self.assertTrue(all(c['value'].startswith('scope:') for c in match['captures']))

    def test_native_title_reference_is_one_key(self):
        rows=[r for r in self.rows if r['native'].startswith('Unexpected token: title:h_china.holder,')]
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row['outcome'],'full')
            self.assertEqual([c['value'] for c in row['matches'][0]['captures'] if c['type']=='KEY'],['title:h_china.holder'])
            self.assertIn(['token',':'],row['pieces'])

    def test_native_variable_mesh_regions_are_params(self):
        rows=[r for r in self.rows if r['source_family']=='pdxassetutil.cpp' and 'for mesh [' in r['native']]
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row['outcome'],'full')
            value=row['native'].split('for mesh [',1)[1].split(']',1)[0]
            kinds={'PARAM'} if '|' in value else {'KEY','PARAM'}
            self.assertTrue(any(c['type'] in kinds and c['value']==value for c in row['matches'][0]['captures']))

    def test_native_declared_character_description_is_whole_param(self):
        value='Basilia de Clare of c_buckinghamshire (Internal ID: 82542 - Historical ID MBenglish0003)'
        rows=[r for r in self.rows if r['native'].startswith(' Spouse Character: '+value)]
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row['outcome'],'full')
            self.assertTrue(any(c['type']=='PARAM' and c['value']==value for c in row['matches'][0]['captures']))

    def test_native_expression_field_retains_param_for_short_members(self):
        rows=[r for r in self.rows if r['native']==" Failed converting statement for 'war_goal_title.GetName'\r\n"]
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row['outcome'],'full')
            self.assertEqual([(c['type'],c['value']) for c in row['matches'][0]['captures']],
                             [('PARAM','war_goal_title.GetName')])
            pattern=self.patterns[row['matches'][0]['template_id']]
            slot=next(p for p in pattern['parts'] if p['kind']=='slot')
            values=[]
            for member in slot['field_support']['members']:
                record=self.records[member['record_id']]
                self.assertEqual(record.source_family,row['source_family'])
                self.assertTrue(record.text.startswith(" Failed converting statement for '"))
                a,b=member['pieces'];pieces=record.pieces[a:b]
                self.assertEqual(record.pieces[a-1],('token',"'"))
                self.assertEqual(record.pieces[b],('token',"'"))
                values.append(pieces)
            self.assertGreaterEqual(len(set(values)),2)
            lengths={sum(k=='token' for k,_ in pieces) for pieces in values}
            self.assertIn(1,lengths)
            self.assertGreater(max(lengths),1)
            self.assertTrue(span_variation(values,atomic=[key_piece_sequence(p) for p in values])['supported'])

    def test_native_token_error_wording_stays_literal(self):
        prefixes=('Unexpected token: modifier,','Malformed token: +10,')
        for prefix in prefixes:
            rows=[r for r in self.rows if r['source_family']=='pdx_persistent_reader.cpp' and r['native'].startswith(prefix)]
            self.assertTrue(rows,prefix)
            for row in rows:
                self.assertEqual(row['outcome'],'full')
                match=row['matches'][0]
                parts=self.patterns[match['template_id']]['parts']
                self.assertEqual(parts[0]['kind'],'literal')
                self.assertTrue(parts[0]['text'].startswith(prefix.split(':',1)[0]+':'))
                self.assertFalse(any(c['type']=='PARAM' for c in match['captures']))

    def test_matching_respects_declared_construction(self):
        for row in self.rows:
            expected=row['construction']['id'] if row['construction'] else None
            for match in row['matches']:
                self.assertEqual(self.patterns[match['template_id']]['construction_id'],expected)
                pieces=tuple(map(tuple,row['pieces']))
                structures=[v[1] for _,v in sorted(parameter_piece_ranges(pieces,row['source_family']).items())]
                self.assertEqual(self.patterns[match['template_id']]['parameter_structures'],structures)

    def test_intact_reason_independent_of_reason_classification(self):
        selected=[r for r in self.rows if 'unlearn_language effect [ Trying to unlearn native language ]' in r['native']]
        self.assertTrue(selected)
        for row in selected:
            self.assertTrue(row['matches'])
            for m in row['matches']:
                reason=[c for c in m['captures'] if c['type']=='REASON']
                self.assertEqual(len(reason),1)
                self.assertEqual(reason[0]['value'],'Trying to unlearn native language')
                start=row['native'].encode().index(b'Trying to unlearn native language')
                self.assertEqual(reason[0]['span'],[start,start+len(b'Trying to unlearn native language')])

    def test_short_candidate_consideration_uses_real_heads(self):
        records=[]
        for head in ('unlearn_language effect','add_character_flag effect'):
            row=next(r for r in self.rows if r['construction'] and r['construction']['regions'].get('L1',{}).get('text')==head)
            records.append(self.records[row['record_id']])
        left,right=map(learning_tokens,records)
        self.assertEqual(len(left),2);self.assertEqual(len(right),2)
        self.assertTrue(comparable(left,right,.72))

    def test_unbracketed_failure_compares_its_own_wording(self):
        row=next(r for r in self.rows if r['construction']
                 and r['construction']['id']=='script-system-unbracketed'
                 and r['construction']['regions']['message']['text']=="Event target link 'scope' returned an unset scope")
        words=[text for _,text in learning_tokens(self.records[row['record_id']])]
        self.assertIn('returned',words)
        for boilerplate in ('Script','Error','location','file','line'):
            self.assertNotIn(boilerplate,words)

    def test_slot_evidence_is_its_own_candidate_members(self):
        for p in self.patterns.values():
            members=set(p['evidence_record_ids'])
            for part in p['parts']:
                if part['kind']!='slot':continue
                support=part['field_support']
                self.assertEqual({v['record_id'] for v in support['members']},members)
                for v in support['members']:
                    rec=self.records[v['record_id']];a,b=v['pieces'];x,y=v['bytes']
                    self.assertEqual(''.join(t for _,t in rec.pieces[a:b]).encode('utf-8','surrogateescape'),rec.text.encode('utf-8','surrogateescape')[x:y])

    def test_all_saved_matches_reconstruct_exactly(self):
        for row in self.rows:
            rec=self.records[row['record_id']];offsets={0};n=0
            for _,t in rec.pieces:n+=len(t.encode('utf-8','surrogateescape'));offsets.add(n)
            for m in row['matches']:
                p=self.patterns[m['template_id']]
                self.assertEqual(p['source_family'],rec.source_family)
                self.assertEqual(match_pattern(p['parts'],rec.text,pieces=rec.pieces),m['captures'])
                by_name={c['name']:c for c in m['captures']};parts=[]
                for part in p['parts']:
                    if part['kind']=='literal':parts.append(part['text']);continue
                    cap=by_name[part['name']]
                    own=self.field_members[p['template_id']][part['name']].get(row['record_id'])
                    if own:
                        x,y=own['bytes']
                        expected=None if x==y and part['optional'] else [
                            x+len(part['prefix'].encode('utf-8','surrogateescape')),
                            y-len(part['suffix'].encode('utf-8','surrogateescape'))]
                        self.assertEqual(cap['span'],expected)
                    if cap['span'] is None:continue
                    a,b=cap['span'];self.assertIn(a,offsets);self.assertIn(b,offsets)
                    self.assertEqual(rec.text.encode('utf-8','surrogateescape')[a:b].decode('utf-8','surrogateescape'),cap['value'])
                    parts.extend([part['prefix'],cap['value'],part['suffix']])
                self.assertEqual(''.join(parts),rec.text)

    def test_reason_label_colon_stays_literal(self):
        rows=[r for r in self.rows if r['source_family']=='culture_history_entry.cpp' and 'Reason:' in r['native']]
        self.assertTrue(rows)
        for row in rows:
            for match in row['matches']:
                self.assertTrue(any(p['kind']=='literal' and 'Reason:' in p['text']
                                    for p in self.patterns[match['template_id']]['parts']))

    def test_parentheses_do_not_force_param(self):
        row=next(r for r in self.rows if 'unlearn_language effect [ Trying to unlearn native language ]' in r['native'])
        rec=self.records[row['record_id']];parts,failures=derive_pattern([rec],rec)
        self.assertFalse(failures)
        self.assertFalse(any(p.get('type')=='PARAM' and not p.get('parameter_definition') for p in parts))
        self.assertTrue(any(p.get('parameter_definition') for p in parts))
        self.assertTrue(any(p.get('type')=='REASON' for p in parts))

    def test_guidance_relaxation_requires_field_evidence(self):
        for pattern in self.patterns.values():
            for p in pattern['parts']:
                if p.get('type')=='PARAM' and not p['constraints']['literal_guidance']:
                    evidence=p['field_support']['assessment']
                    self.assertTrue(evidence['supported'])
                    if p.get('parameter_definition'):
                        self.assertEqual(evidence['declared_structure'],p['parameter_definition'])
                        self.assertNotIn('declared_field',p['constraints'])
                        continue
                    self.assertTrue(evidence['punctuation_left'] or evidence['punctuation_right'] or evidence['stronger_word_evidence'])
                    self.assertGreaterEqual(len(p['observed_values']),2)

    def test_supported_param_zero_weight(self):
        found=False
        for p in self.patterns.values():
            if p['unsupported_members'] or not any(q.get('type')=='PARAM' for q in p['parts']):continue
            records=[self.records[k] for k in p['evidence_record_ids']]
            peers=defaultdict(list)
            for r in records:
                caps=match_pattern(p['parts'],r.text,pieces=r.pieces)
                key=tuple((c['name'],c['value']) for c in caps if c['type'] not in {'PARAM','LOCATOR'})
                peers[key].append(r)
            for group in peers.values():
                if len(group)<2:continue
                before={learning_tokens(r) for r in group};after={learning_tokens(r,p['parts']) for r in group}
                if len(before)>1:self.assertEqual(len(after),1);found=True
        self.assertTrue(found,'native fields with differing PARAM contents must exercise zero comparison weight')

    def test_full_results_have_one_complete_assignment(self):
        for row in self.rows:
            if row['outcome']!='full':continue
            self.assertEqual(len(row['matches']),1)
            self.assertFalse(row['capture_ambiguities'])
            p=self.patterns[row['matches'][0]['template_id']]
            result=analyze_match_pattern(p['parts'],row['native'],pieces=row['pieces'])
            self.assertEqual(result['count'],1)
            self.assertEqual(result['captures'],row['matches'][0]['captures'])

    def test_ambiguous_capture_witnesses_are_complete_and_distinct(self):
        checked=0
        patterns=list(self.patterns.values())
        if baseline:=os.environ.get('CK3_LEARNER_BASELINE_BUNDLE'):
            # Saved ambiguous contracts are negative controls on the same real
            # messages. No historical inference code or runtime fallback runs.
            patterns+=json.loads((Path(baseline)/'empirical_template_model.json').read_text())['templates']
        for p in patterns:
            for h in p['region_hypotheses']:
                if h.get('proposal')!='capture_ambiguity':continue
                rec=self.records[h['record_id']]
                result=analyze_match_pattern(p['parts'],rec.text,pieces=rec.pieces)
                self.assertEqual(result['count'],h['count'])
                self.assertGreater(result['count'],1)
                self.assertIsNone(result['captures'])
                self.assertEqual(len(result['witnesses']),2)
                self.assertNotEqual(*result['witnesses'])
                for witness in result['witnesses']:
                    caps={c['name']:c for c in witness}
                    rebuilt=''.join(part['text'] if part['kind']=='literal' else
                        '' if caps[part['name']]['span'] is None else
                        part['prefix']+caps[part['name']]['value']+part['suffix'] for part in p['parts'])
                    self.assertEqual(rebuilt,rec.text)
                checked+=1
        if not checked:
            self.skipTest('selected native evidence has no recorded capture ambiguity to check')

    def test_declared_parameters_keep_exact_recognized_ranges(self):
        covered=0
        for row in self.rows:
            rec=self.records[row['record_id']]
            fields=parameter_piece_ranges(rec.pieces,rec.source_family)
            if not fields:continue
            offsets=[0]
            for _,s in rec.pieces:offsets.append(offsets[-1]+len(s.encode('utf-8','surrogateescape')))
            for match in row['matches']:
                for a,(b,definition) in fields.items():
                    self.assertTrue(any(c['type']=='PARAM' and c['span']==[offsets[a],offsets[b]]
                                        for c in match['captures']),(row['record_id'],definition))
                    covered+=1
        self.assertGreater(covered,0)

    def test_trace_declaration_does_not_capture_unknown_or_id_parentheses(self):
        unknown=[r for r in self.rows if 'Script location: Unknown' in r['native']]
        self.assertTrue(unknown)
        for r in unknown:
            rec=self.records[r['record_id']]
            self.assertFalse(parameter_piece_ranges(rec.pieces,rec.source_family))
            self.assertTrue(r['matches'])
            self.assertFalse(any(self.patterns[m['template_id']]['parameter_structures'] for m in r['matches']))
        for r in self.rows:
            if r['source_family']!='characterhistory.cpp':continue
            rec=self.records[r['record_id']]
            self.assertTrue(all(definition=='character-history-description'
                                for _,definition in parameter_piece_ranges(rec.pieces,rec.source_family).values()))

    def test_word_only_parameters_need_stronger_native_evidence(self):
        for p in self.patterns.values():
            if p['status']=='unresolved':continue
            for part in p['parts']:
                if part.get('type')!='PARAM':continue
                assessment=part['field_support']['assessment']
                self.assertTrue(assessment['supported'])
                if assessment['word_only_review']:
                    self.assertTrue(assessment['stronger_word_evidence'])

    def test_reviewed_native_names_remain_inside_parameter(self):
        # Actual complete emissions from the owner's review, never fabricated
        # messages. These expected captures are checks, not inference rules.
        for value in ('Alvise of Salisbury of', 'Mark of Baghdad of', 'Constantine of Nishapur of'):
            rows=[r for r in self.rows if value+'  (Internal ID:' in r['native']]
            self.assertTrue(rows,value)
            for row in rows:
                self.assertEqual(row['outcome'],'full')
                self.assertTrue(any(c['type']=='PARAM' and (c['value'].strip()==value or
                                    c['value'].startswith(value+'  (Internal ID:') and c['value'].endswith(')'))
                                    for c in row['matches'][0]['captures']),value)

    def test_native_nested_quotes_retain_outer_boundary(self):
        value="GetTitleByKey('c_siracusa').GetHolder.GetFaith.HouseOfWorship"
        rows=[r for r in self.rows if r['source_family']=='pdx_data_factory.cpp'
              and r['native'].startswith(' Failed converting statement for ') and value in r['native']]
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row['outcome'],'full')
            match=row['matches'][0]
            # A sole expression spelling may remain literal. Nested punctuation
            # is not evidence for forcing its entire family into PARAM.
            if not any(c['value']==value for c in match['captures']):
                wording=''.join(p['text'] for p in self.patterns[match['template_id']]['parts'] if p['kind']=='literal')
                self.assertIn("'"+value+"'",wording)


if __name__=='__main__':unittest.main()
