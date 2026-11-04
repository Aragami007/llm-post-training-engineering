#!/usr/bin/env python3
"""Publish 133 syllabus topics to GitHub Issues with labels/milestones.

Requires the authenticated GitHub CLI (`gh`) on the user's computer. Read-only
planning is the DEFAULT. `--apply` creates missing resources. Uses an invisible
stable marker to identify already-created issues and avoid duplicates on reruns.
"""
import argparse
import os
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLOR = {
    'concept': '1D76DB', 'lab': '0E8A16', 'experiment': '5319E7',
    'gate': 'B60205', 'stretch': 'FBCA04',
    'local': 'C2E0C6', 'local-or-cloud': 'BFDADC',
    'hybrid': 'D4C5F9', 'cloud-conditional': 'F9D0C4',
}


def cmd(argv, data=None, retries=2):
    for attempt in range(retries+1):
        proc = subprocess.run(argv, input=data, text=True, capture_output=True)
        if proc.returncode == 0:
            return proc.stdout.strip()
        err = proc.stderr.strip()
        # Auth, permission, and bad argument errors require a user fix, not retries.
        if attempt == retries or not any(x in err.lower() for x in ('secondary rate limit', 'too many requests', '502 bad gateway', '503 service')):
            raise RuntimeError(f'Command failed: {argv[:4]} ...\n{err}')
        wait = 3 * (2 ** attempt)
        print(f'GitHub temporary limit/service error; retrying after {wait}s', file=sys.stderr)
        time.sleep(wait)


def gh_json(argv, data=None):
    return json.loads(cmd(['gh', *argv], data=data))


def preflight(repo):
    if not shutil.which('gh'):
        raise RuntimeError('GitHub CLI (gh) is not installed. See docs/GITHUB_PUBLISHING.md.')
    cmd(['gh','auth','status'])
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        if os.environ.get('GITHUB_REPOSITORY','').casefold() != repo.casefold():
            raise RuntimeError('GitHub Actions publishing is allowed only to the current repository.')
        cmd(['gh','repo','view',repo,'--json','nameWithOwner'])
        return
    active = cmd(['gh','api','user','--jq','.login']).strip()
    owner = repo.split('/', 1)[0]
    if active.casefold() != owner.casefold():
        raise RuntimeError(f"Authenticated GitHub login {active!r} does not match requested repo owner {owner!r}. Switch accounts before publishing.")
    cmd(['gh','repo','view',repo,'--json','nameWithOwner'])

def existing_issues(repo):
    rows = gh_json(['issue','list','--repo',repo,'--state','all','--limit','1000','--json','number,title,body,state,url'])
    found = {}
    for x in rows:
        match = re.search(r'<!-- course-topic-id: (P\d{2}-\d{2}) -->', x.get('body') or '')
        if match:
            if match.group(1) in found:
                raise RuntimeError(f'Duplicate existing issue marker {match.group(1)}. Resolve manually before syncing.')
            found[match.group(1)] = x
    return found


def labels_for(topic):
    return [f'phase:{topic["phase"]:02d}', f'kind:{topic["kind"]}',
            'scope:stretch' if topic['optional'] else 'scope:core',
            f'compute:{topic["resource"]}']


def ensure_labels(repo, phases, topics):
    used = {lab for t in topics for lab in labels_for(t)}
    for name in sorted(used):
        if name.startswith('phase:'):
            color, description = '0969DA', f'Curriculum {name} — see SYLLABUS.md'
        elif name.startswith('kind:'):
            typ = name.split(':',1)[1]
            color, description = COLOR[typ], f'Topic category: {typ}'
        elif name.startswith('compute:'):
            typ = name.split(':',1)[1]
            color, description = COLOR[typ], f'Compute mode: {typ}'
        else:
            typ = name.split(':',1)[1]
            color, description = ('FBCA04' if typ == 'stretch' else 'C2E0C6'), f'Course requirement: {typ}'
        cmd(['gh','label','create',name,'--repo',repo,'--color',color,'--description',description,'--force'])


def ensure_milestones(repo, phases):
    raw = cmd(['gh','api','--paginate',f'repos/{repo}/milestones?state=all&per_page=100','--jq','.[] | [.title, .number] | @tsv'])
    known = {}
    for line in raw.splitlines():
        if not line.strip(): continue
        title, number = line.split('\t',1)
        known[title] = int(number)
    for phase in phases:
        title = phase['milestone']
        if title not in known:
            body = {'title':title,'description':f"{phase['weeks']}: {phase['goal']}. Phase gate {phase['gate_id']}. No arbitrary due date set."}
            obj = gh_json(['api','--method','POST',f'repos/{repo}/milestones','--input','-'], data=json.dumps(body))
            known[title] = obj['number']
    return known


def issue_text(topic):
    path = ROOT/'tracker/issues'/f'{topic["id"]}.md'
    text = path.read_text(encoding='utf-8')
    first_line, _, body = text.partition('\n')
    assert first_line == f'# [{topic["id"]}] {topic["title"]}', path
    return body.strip()+'\n'


def with_github_crossrefs(body, issues_by_id):
    # Stable ID stays readable, and existing earlier published dependencies gain clickable issue refs.
    return re.sub(r'`(P\d{2}-\d{2})`', lambda m: f'`{m.group(1)}` (#{issues_by_id[m.group(1)]["number"]})' if m.group(1) in issues_by_id else m.group(0), body)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',required=True,help='GitHub owner/repo, e.g. Aragami007/llm-post-training-engineering')
    group = ap.add_mutually_exclusive_group()
    group.add_argument('--apply',action='store_true',help='Really publish missing issues and labels/milestones')
    group.add_argument('--dry-run',action='store_true',help='Show plan (default)')
    ap.add_argument('--phase',type=int,choices=range(12),help='Only publish one phase (phase 00 first is recommended)')
    ap.add_argument('--limit',type=int,help='Maximum number of new issues for test/batching')
    ap.add_argument('--delay',type=float,default=0.75,help='Delay in seconds after issue creation (default: 0.75)')
    args = ap.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',args.repo):
        ap.error('Use repo as owner/name')
    if args.limit is not None and args.limit <= 0:
        ap.error('--limit must be > 0')
    manifest=json.loads((ROOT/'tracker/topics.json').read_text(encoding='utf-8'))
    topics=[x for x in manifest['topics'] if args.phase is None or x['phase']==args.phase]
    phases=[x for x in manifest['phases'] if args.phase is None or x['id']==args.phase]
    if not args.apply:
        print(f'DRY RUN: repo={args.repo} | selected phases={len(phases)} | selected topic issues={len(topics)}')
        print('Would ensure labels and phase milestones, and publish missing course issues using stable markers.')
        for t in topics[:min(12,len(topics))]:
            print(f'  [{t["id"]}] {t["title"]} | {", ".join(labels_for(t))}')
        if len(topics)>12: print(f'  ... and {len(topics)-12} further issue bodies')
        print('No remote access or mutation occurred. Pass --apply to publish to an EXISTING repo.')
        return
    preflight(args.repo)
    print('Authenticated GitHub CLI and destination repository verified.')
    before=existing_issues(args.repo)
    print(f'Already published according to course-topic markers: {len(before)}')
    ensure_labels(args.repo,phases,topics)
    milestones=ensure_milestones(args.repo,phases)
    created=0; skipped=0
    for t in topics:
        if t['id'] in before:
            skipped+=1
            print(f'SKIP {t["id"]} — existing #{before[t["id"]]["number"]}')
            continue
        if args.limit is not None and created >= args.limit:
            break
        payload={'title':f'[{t["id"]}] {t["title"]}',
                 'body':with_github_crossrefs(issue_text(t),before),
                 'labels':labels_for(t),
                 'milestone':milestones[next(p['milestone'] for p in phases if p['id']==t['phase'])]}
        result=gh_json(['api','--method','POST',f'repos/{args.repo}/issues','--input','-'],data=json.dumps(payload,ensure_ascii=False))
        before[t['id']]={'number':result['number'],'url':result['html_url'],'state':'OPEN','body':payload['body']}
        created+=1
        print(f'CREATE {t["id"]} → #{result["number"]} {result["html_url"]}',flush=True)
        if args.delay: time.sleep(args.delay)
    print(f'DONE: created={created}, existing/skipped={skipped}, remaining selected={len(topics)-created-skipped}')
    print(f'Issues: https://github.com/{args.repo}/issues')

if __name__=='__main__':
    try: main()
    except (RuntimeError,OSError,ValueError,KeyError) as e:
        print('ERROR:',e,file=sys.stderr)
        print('It is safe to rerun after fixing the problem; existing issue markers prevent duplicates.',file=sys.stderr)
        sys.exit(1)
