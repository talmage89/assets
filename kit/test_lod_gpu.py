"""Same-process LOD GPU lock compatibility, nesting and exception cleanup."""
import fcntl
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from kit.lod_gpu import locked

ROOT=Path(__file__).resolve().parents[1]


class SameProcessLock(unittest.TestCase):
    def test_shared_flock_and_cleanup(self):
        scratch=ROOT/'build/tmp';scratch.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as folder:
            path=Path(folder)/'gpu.lock'
            with patch.dict(os.environ,ASSETS_GPU_LOCK=str(path),ASSETS_GPU_HELD='old'):
                with self.assertRaisesRegex(RuntimeError,'fixture'):
                    with locked():
                        self.assertEqual(os.environ['ASSETS_GPU_HELD'],'1')
                        with path.open('a') as other:
                            with self.assertRaises(BlockingIOError):fcntl.flock(other,fcntl.LOCK_EX|fcntl.LOCK_NB)
                        with locked():self.assertEqual(os.environ['ASSETS_GPU_HELD'],'1')
                        raise RuntimeError('fixture')
                self.assertEqual(os.environ['ASSETS_GPU_HELD'],'old')
                with path.open('a') as other:
                    fcntl.flock(other,fcntl.LOCK_EX|fcntl.LOCK_NB)
                    fcntl.flock(other,fcntl.LOCK_UN)


if __name__=='__main__':unittest.main()
