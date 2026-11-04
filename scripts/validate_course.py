#!/usr/bin/env python3
"""Offline integrity checker for course syllabus and its issue tracker."""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tracker' / 'topics.json'


def validate(root=ROOT):
    errors = []
    document = json.loads((root / 'tracker/topics.json').read_text(encoding='utf-8'))
    topics, phases = document['topics'], document['phases']
    ids = [t['id'] for t in topics]
    if len(phases) != 12:
        errors.append(f'Expected 12 phases; got {len(phases)}')
    if len(topics) != 133:
        errors.append(f'Expected 133 syllabus subtopic issues; got {len(topics)}')
    if len(set(ids)) != len(ids):
        errors.append('Duplicate topic IDs')
    if len(set(t['title'] for t in topics)) != len(topics):
        errors.append('Duplicate topic titles')
    byphase = Counter(t['phase'] for t in topics)
    for p in phases:
        if byphase[p['id']] != p['issue_count']:
            errors.append(f'Phase {p["id"]} issue count mismatch')
        pt = [x for x in topics if x['phase'] == p['id']]
        if not pt or pt[-1]['kind'] != 'gate' or pt[-1]['id'] != p['gate_id']:
            errors.append(f'Phase {p["id"]} does not end in its specified gate issue')
    for t in topics:
        tag = f'P{t["phase"]:02d}-{t["number"]:02d}'
        if t['id'] != tag or not re.fullmatch(r'P\d{2}-\d{2}', t['id']):
            errors.append(f'Bad ID {t["id"]}')
        for dep in t['prerequisites']:
            if dep not in ids:
                errors.append(f'{t["id"]} missing prerequisite {dep}')
        if not t['concepts'] or not t['tasks'] or not t['evidence'] or not t['acceptance']:
            errors.append(f'{t["id"]} lacks concepts/tasks/evidence/acceptance')
        if t['optional'] != (t['kind'] == 'stretch'):
            errors.append(f'{t["id"]} optional/label mismatch')
        filename = root / 'tracker' / 'issues' / (t['id'] + '.md')
        if not filename.exists():
            errors.append(f'Missing issue file {filename.relative_to(root)}')
        else:
            body = filename.read_text(encoding='utf-8')
            if f'<!-- course-topic-id: {t["id"]} -->' not in body:
                errors.append(f'Missing stable issue marker in {filename.name}')
            if t['title'] not in body or t['acceptance'] not in body:
                errors.append(f'Issue body stale: {filename.name}')
            if body.count('### Definition of done') != 1:
                errors.append(f'Issue has wrong completion rubric: {filename.name}')
    with (root / 'tracker/issue_manifest.csv').open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if [x['id'] for x in rows] != ids:
        errors.append('CSV IDs differ from JSON tracker ordering')
    index = (root / 'docs/ISSUE_INDEX.md').read_text(encoding='utf-8')
    for tid in ids:
        if tid not in index:
            errors.append(f'Index missing {tid}')
    for rel in ['README.md','SYLLABUS.md','docs/TECHNICAL_AUDIT.md','docs/ORIGINAL_DRAFT.md','docs/EVALUATION_PROTOCOL.md','docs/COMPUTE_AND_COST.md','docs/CAPSTONE.md','docs/GITHUB_PUBLISHING.md','SECURITY.md']:
        if not (root / rel).is_file():
            errors.append(f'Missing required document {rel}')
    return errors, byphase, topics


if __name__ == '__main__':
    try:
        errs, counts, topics = validate()
    except (OSError, KeyError, json.JSONDecodeError) as ex:
        print(f'Cannot validate course: {ex}', file=sys.stderr)
        raise SystemExit(1)
    for phase, count in sorted(counts.items()):
        print(f'Phase {phase:02d}: {count:2} issues')
    print(f'Total: {len(topics)} (core: {sum(not x["optional"] for x in topics)}, stretch: {sum(x["optional"] for x in topics)})')
    if errs:
        for err in errs: print('ERROR:', err, file=sys.stderr)
        raise SystemExit(1)
    print('OK — all topic IDs, issue bodies, docs, dependencies, and phase gates verified.')
