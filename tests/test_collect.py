import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import collect


class CollectionTests(unittest.TestCase):
    def test_exact_author_receipts_and_new_repository_discovery(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            root = workspace / 'logs-repo'
            (root / 'data/receipts').mkdir(parents=True)
            (root / 'logs').mkdir()
            (root / 'data/config.json').write_text(json.dumps({'author': 'smallyunet', 'start': '2026-01-01T00:00:00+08:00', 'exclude': ['logs-repo']}))
            repo = workspace / 'new-project'
            repo.mkdir()
            def git(*args, author='smallyunet'):
                env = dict(os.environ, GIT_AUTHOR_NAME=author, GIT_COMMITTER_NAME=author, GIT_AUTHOR_EMAIL='test@example.com', GIT_COMMITTER_EMAIL='test@example.com', GIT_AUTHOR_DATE='2026-09-13T10:00:00+08:00', GIT_COMMITTER_DATE='2026-09-13T10:00:00+08:00')
                return subprocess.check_output(['git', '-C', str(repo), *args], env=env, text=True, stderr=subprocess.DEVNULL).strip()
            git('init')
            git('-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-m', 'eligible')
            sha = git('rev-parse', 'HEAD')
            git('-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-m', 'different author', author='smallyunet-bot')
            with patch.object(collect, 'ROOT', root):
                result = collect.collect()['repositories']
                self.assertEqual([c['sha'] for c in result[0]['commits']], [sha])
                receipt = root / 'data/receipts/2026-09-13.json'
                receipt.write_text(json.dumps({'commits': [{'repository': 'new-project', 'sha': sha}]}))
                with self.assertRaises(ValueError):
                    collect.collect()
                (root / 'logs/2026-09-13.md').write_text('# Report\n')
                self.assertEqual(collect.collect()['repositories'][0]['commits'], [])
