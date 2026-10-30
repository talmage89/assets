"""Repository GIF policy, including additions to an otherwise unchanged index."""
from pathlib import Path
import subprocess
import tempfile
import unittest
from PIL import Image

SCRIPT = Path(__file__).with_name('repo_check.py').resolve()
ROOT = SCRIPT.parents[1]


class DocsGIF(unittest.TestCase):
    def setUp(self):
        scratch = ROOT/'build/repo-check-tests'
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)
        self.git('init', '-q')

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True,
                              capture_output=True)

    def image(self, name='asset/docs/motion.gif', width=960):
        path = self.root/name
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new('RGB', (width, 20), '#434649').save(path)
        return path

    def check(self, staged=False):
        return subprocess.run(['python3', str(SCRIPT), *(['--staged'] if staged else [])],
                              cwd=self.root, capture_output=True, text=True)

    def test_one_gif_and_existing_jpg(self):
        self.image()
        self.image('asset/docs/hero.jpg', 1600)
        self.assertEqual(self.check().returncode, 0)
        self.git('add', '.')
        self.assertEqual(self.check(True).returncode, 0)

    def test_width_size_and_location(self):
        path = self.image(width=961)
        self.assertIn('960 px / 450 KB', self.check().stdout)
        self.image()
        with path.open('ab') as f:
            f.write(b'\0'*450_000)
        self.assertIn('960 px / 450 KB', self.check().stdout)
        path.unlink()
        self.image('motion.gif')
        self.assertIn('only final docs', self.check().stdout)

    def test_second_gif_in_later_commit(self):
        self.image()
        self.git('add', '.')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'first')
        self.image('asset/docs/nested/second.gif')
        self.assertIn('at most one', self.check().stdout)
        self.git('add', '.')
        self.assertIn('at most one', self.check(True).stdout)
        self.git('rm', 'asset/docs/motion.gif')
        self.assertEqual(self.check(True).returncode, 0)

    def test_other_docs_rules_retained(self):
        self.image('asset/docs/wide.jpg', 1601)
        self.assertIn('1600 px / 200 KB', self.check().stdout)
        self.image('asset/docs/rebuilt.png')
        self.assertIn('forbidden generated', self.check().stdout)


if __name__ == '__main__':
    unittest.main()
