#!/usr/bin/env python3
"""Collect unpublished commit metadata without modifying source repositories."""
import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()


def collect():
    config = json.loads((ROOT / 'data/config.json').read_text())
    start = datetime.fromisoformat(config['start']).timestamp()
    seen = set()
    for path in (ROOT / 'data/receipts').glob('*.json'):
        receipt = json.loads(path.read_text())
        if not (ROOT / 'logs' / (path.stem + '.md')).is_file():
            raise ValueError(f'Receipt without report: {path.name}')
        seen.update((row['repository'], row['sha']) for row in receipt['commits'])
    repos = []
    for repo in sorted(ROOT.parent.iterdir()):
        if not repo.is_dir() or repo.name in config['exclude'] or not (repo / '.git').exists():
            continue
        head = git(repo, 'rev-parse', 'HEAD')
        branch = git(repo, 'branch', '--show-current')
        rows = git(repo, 'log', '--no-merges', '--format=%H%x09%an%x09%ct', head)
        commits = []
        for row in rows.splitlines():
            sha, author, timestamp = row.split('\t')
            if author != config['author'] or int(timestamp) < start or (repo.name, sha) in seen:
                continue
            commits.append({'repository': repo.name, 'sha': sha, 'committedAt': int(timestamp)})
        repos.append({'repository': repo.name, 'branch': branch, 'head': head, 'commits': list(reversed(commits))})
    return {'collectedAt': datetime.now().astimezone().isoformat(), 'repositories': repos}


if __name__ == '__main__':
    print(json.dumps(collect(), ensure_ascii=False, indent=2))
