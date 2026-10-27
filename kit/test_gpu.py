"""Device-selection fixtures; no rendering or physical GPU required."""
from pathlib import Path
from types import SimpleNamespace as NS
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kit import gpu


class Devices(unittest.TestCase):
    def run_devices(self,kind):
        prefs=NS(devices=[],refresh_devices=lambda:None)
        if kind:prefs.devices=[NS(type=kind,name='Fixture GPU',use=False)]
        scene=NS(cycles=NS(device='GPU'))
        fake=NS(context=NS(preferences=NS(addons={'cycles':NS(preferences=prefs)}),scene=scene))
        with patch.object(gpu,'bpy',fake),patch.dict(os.environ,ASSETS_GPU_HELD='1'):
            result=gpu.enable()
        self.assertEqual(result,kind or 'CPU')
        self.assertEqual(scene.cycles.device,'GPU' if kind else 'CPU')
        if kind:self.assertTrue(prefs.devices[0].use)

    def test_optix(self):self.run_devices('OPTIX')
    def test_cuda(self):self.run_devices('CUDA')
    def test_cpu(self):
        with self.assertWarnsRegex(RuntimeWarning,'falling back to CPU'):
            self.run_devices(None)

    def test_lock_required(self):
        with patch.dict(os.environ,ASSETS_GPU_HELD='0'):
            with self.assertRaisesRegex(RuntimeError,'GPU lock not held'):gpu.enable()


if __name__=='__main__':unittest.main(argv=[__file__])
