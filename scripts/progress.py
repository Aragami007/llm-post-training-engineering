#!/usr/bin/env python3
"""Build docs/PROGRESS.md from actual GitHub issue state (not stale assumptions)."""
import argparse
import json
import re
import shutil
import subprocess
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run(repo):
    if not shutil.which('gh'):
        raise SystemExit('Install and authenticate GitHub CLI; see docs/GITHUB_PUBLISHING.md')
    p=subprocess.run(['gh','issue','list','-R',repo,'--state','all','--limit','1000','--json','number,title,body,state,url'],capture_output=True,text=True)
    if p.returncode: raise SystemExit(p.stderr.strip())
    return json.loads(p.stdout)

def write_report(repo,output):
    man=json.loads((ROOT/'tracker/topics.json').read_text(encoding='utf-8'))
    present={}
    for obj in run(repo):
        match=re.search(r'<!-- course-topic-id: (P\d{2}-\d{2}) -->',obj.get('body') or '')
        if match:present[match.group(1)]=obj
    lines=[f'# Learning progress — live GitHub snapshot','',f'Updated: {datetime.now(timezone.utc).isoformat(timespec="seconds")} (UTC). Repository: https://github.com/{repo}','','| Phase | Closed | Open | Not published | Total | Gate |','|---|---:|---:|---:|---:|---|']
    all_counts=[0,0,0]
    for phase in man['phases']:
        tt=[t for t in man['topics'] if t['phase']==phase['id']]
        closed=sum(present[t['id']]['state'].upper()=='CLOSED' for t in tt if t['id'] in present)
        open_=sum(present[t['id']]['state'].upper()=='OPEN' for t in tt if t['id'] in present)
        missing=sum(t['id'] not in present for t in tt)
        all_counts[0]+=closed;all_counts[1]+=open_;all_counts[2]+=missing
        gate=present.get(phase['gate_id'])
        gate_status=(f'[#{gate["number"]}]({gate["url"]}) — {gate["state"]}' if gate else 'not published')
        lines.append(f'| {phase["id"]:02d} | {closed} | {open_} | {missing} | {len(tt)} | {gate_status} |')
    lines.extend([f'| **TOTAL** | **{all_counts[0]}** | **{all_counts[1]}** | **{all_counts[2]}** | **{len(man["topics"])}** | |','',f'**Completion:** {all_counts[0]}/{len(man["topics"])} topics closed ({100*all_counts[0]/len(man["topics"]):.1f}%).','','Status reflects GitHub issue states, **not an independent audit of linked evidence**. Inspect the gate issues and attached code/logs before claiming competence.',''])
    output.write_text('\n'.join(lines),encoding='utf-8')
    print(f'Wrote {output} from {len(present)} published course issues.')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',required=True)
    ap.add_argument('--output',default='docs/PROGRESS.md')
    args=ap.parse_args()
    destination=Path(args.output)
    if not destination.is_absolute(): destination=ROOT/destination
    write_report(args.repo,destination)
