import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_course import validate

class CourseStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((ROOT/'tracker/topics.json').read_text(encoding='utf-8'))
    def test_manifest_count(self):
        self.assertEqual(133,len(self.manifest['topics']))
        self.assertEqual(12,len(self.manifest['phases']))
    def test_issue_integrity(self):
        errors,counts,topics=validate(ROOT)
        self.assertEqual([],errors)
    def test_ids_and_gate_tail(self):
        topics=self.manifest['topics']
        ids=set(t['id'] for t in topics)
        self.assertEqual(len(ids),len(topics))
        for p in self.manifest['phases']:
            pts=[x for x in topics if x['phase']==p['id']]
            self.assertEqual('gate',pts[-1]['kind'])
            self.assertEqual(p['gate_id'],pts[-1]['id'])
    def test_all_dependencies_exist(self):
        ids={t['id'] for t in self.manifest['topics']}
        for t in self.manifest['topics']:
            self.assertTrue(set(t['prerequisites']).issubset(ids),t['id'])
    def test_optional_is_explicit(self):
        for t in self.manifest['topics']:
            self.assertEqual(t['kind']=='stretch',t['optional'])

if __name__=='__main__': unittest.main()
