"""Regression coverage for merged density policy and Make delivery settings."""
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest

from kit.policy import density_bands

ROOT=Path(__file__).resolve().parents[1]


class DensityPolicy(unittest.TestCase):
    def test_default_and_legacy_policy(self):
        expected=dict(p5_min=100,median_min=225,median_max=450,p95_max=750)
        self.assertEqual(density_bands({},1024),expected)
        legacy=dict(VERIFY_POLICY=dict(density_reference_size=1024,density_p5_min=300))
        self.assertEqual(density_bands(legacy,2048)['p5_min'],600)

    def test_explicit_and_legacy_absolute_bands(self):
        bands=dict(p5_min=280,median_min=550,median_max=900,p95_max=1500)
        self.assertEqual(density_bands(dict(UV_DENSITY_BANDS=bands),512),bands)
        config=dict(UV_DENSITY_BANDS=dict(reference_size=1024,**bands),VERIFY_POLICY=dict(tube={}))
        self.assertEqual(density_bands(config,512),{k:v/2 for k,v in bands.items()})

    def test_ambiguous_or_invalid_policy(self):
        bands=dict(reference_size=0,p5_min=280,median_min=550,median_max=900,p95_max=1500)
        with self.assertRaises(ValueError):density_bands(dict(UV_DENSITY_BANDS=bands),1024)
        with self.assertRaises(ValueError):
            density_bands(dict(UV_DENSITY_BANDS=bands,VERIFY_POLICY=dict(density_p5_min=200)),1024)


class MakeDelivery(unittest.TestCase):
    def test_gpu_lock_defaults_and_environment_override(self):
        environment={k:v for k,v in os.environ.items() if k!='ASSETS_GPU_LOCK'}
        override=str(ROOT/'build/custom-lab.lock')
        for rules in ('rules.mk','tiling_rules.mk'):
            for value in (None,override):
                env=dict(environment)
                if value is not None:env['ASSETS_GPU_LOCK']=value
                command=['make','--no-print-directory','-f',str(ROOT/'kit'/rules),
                         '--eval','print-lock:;@echo $(ASSETS_GPU_LOCK)','print-lock']
                result=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertEqual(result.stdout.strip(),value or str(ROOT/'build/locks/gpu.lock'))

    def test_final_renderer_alias_and_precedence(self):
        command=['make','--no-print-directory','-f',str(ROOT/'kit/rules.mk'),
                 '--eval','print-studio:;@echo $(STUDIO_SCRIPT)','print-studio']
        for settings,expected in [([],str(ROOT/'kit/studio.py')),
                                  (['FINAL_RENDER_SCRIPT=car.py'],'car.py'),
                                  (['STUDIO_SCRIPT=tree.py'],'tree.py'),
                                  (['FINAL_RENDER_SCRIPT=car.py','STUDIO_SCRIPT=tree.py'],'tree.py')]:
            result=subprocess.run(command+settings,cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(result.stdout.strip(),expected)

    def test_aliases_and_invalidation(self):
        scratch=ROOT/'build'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='delivery-test-',dir=scratch) as folder:
            folder=Path(folder)
            # Tiny stage substitutes exercise the actual kit dependency graph.
            (folder/'Makefile').write_text(f'''ASSET := Fixture
include {ROOT}/kit/rules.mk
$(BUILD)/finalized.blend: ; @touch $@
$(BUILD)/baked.stamp: ; @touch $@
$(BUILD)/textures.stamp: ; @touch $@
export/Fixture.glb: ; @mkdir -p export; touch $@
''')
            (folder/'build').mkdir();(folder/'src').mkdir()
            for name in ('config.py','build.py','markings.py'):(folder/'src'/name).touch()
            for name in ('lookdev.blend','game-audit.blend','parameters.txt'):(folder/'build'/name).touch()
            (folder/'build/markings').mkdir();(folder/'build/markings/.stamp').touch()
            def make(*args):
                return subprocess.run(['make','--no-print-directory','export',*args],cwd=folder,
                                      env={**os.environ,'TMPDIR':str(ROOT/'build/tmp')},capture_output=True,text=True)
            def stamps():
                return [(folder/'build'/name).stat().st_mtime_ns for name in
                        ('finalized.blend','baked.stamp','textures.stamp')]
            self.assertEqual(make().returncode,0)
            baseline=stamps()
            self.assertEqual(make().returncode,0);self.assertEqual(stamps(),baseline)
            time.sleep(.02)
            self.assertEqual(make('BAKE_SIZE=2048').returncode,0)
            baked=stamps();self.assertEqual(baked[0],baseline[0]);self.assertGreater(baked[1],baseline[1])
            time.sleep(.02)
            self.assertEqual(make('BAKE_SIZE=2048','BAKE_SAMPLES=8').returncode,0)
            sampled=stamps();self.assertEqual(sampled[0],baked[0]);self.assertGreater(sampled[1],baked[1])
            time.sleep(.02)
            self.assertEqual(make('TEX_SIZE=1024').returncode,0)
            resized=stamps();self.assertGreater(resized[0],sampled[0])
            self.assertIn('size=1024', (folder/'build/delivery-parameters.txt').read_text())
            self.assertEqual(make('SHIP_SIZE=1024').returncode,0);self.assertEqual(stamps(),resized)
            for setting in ('UV_MARGIN=.003','UV_TARGET_DENSITY=810'):
                before=stamps();time.sleep(.02)
                self.assertEqual(make('SHIP_SIZE=1024',setting).returncode,0)
                self.assertGreater(stamps()[0],before[0])
            self.assertNotEqual(make('SHIP_SIZE=1024','TEX_SIZE=2048').returncode,0)
            before=stamps();time.sleep(.02)
            self.assertEqual(make('SHIP_SIZE=1024','UV_TARGET_DENSITY=810',
                                  'DOWNSAMPLE_ARGS=--alpha-mode independent').returncode,0)
            after=stamps()
            self.assertEqual(after[:2],before[:2])
            self.assertGreater(after[2],before[2])



if __name__=='__main__':unittest.main()
