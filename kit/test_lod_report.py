"""Family LOD accounting, independent config reports and opt-in Make hooks."""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from kit.lod_report import family_residency,checkpoint_markers,block

ROOT=Path(__file__).resolve().parents[1]


class LODFamilyReportTests(unittest.TestCase):
    def test_shared_container_and_images_are_counted_once(self):
        image=dict(sha256='shared',compressed_mip_bytes=1000)
        def chain(a,b):return dict(levels=[dict(level=0,mesh_gpu_bytes=100,images=[image,image]),dict(level=1,mesh_gpu_bytes=a,images=[image]),dict(level=2,mesh_gpu_bytes=b,images=[image])])
        a,b=chain(50,30),chain(40,20)
        result=family_residency([('source',a),('source',b)])
        self.assertEqual(result['total_gpu_bytes'],1240)
        self.assertEqual(result['lod0_total_gpu_bytes'],1100)
        self.assertEqual(result['additional_mesh_gpu_bytes'],140)
        self.assertTrue(result['passed'])
        proxy=dict(level=3,mesh_gpu_bytes=10,proxy=True,images=[dict(sha256='far',compressed_mip_bytes=200)])
        a['levels'].append(proxy)
        self.assertEqual(family_residency([('source',a),('source',b)])['total_gpu_bytes'],1450)
        self.assertEqual(family_residency([('source-a',a),('source-b',b)])['total_gpu_bytes'],1550)
        b['levels'][1]['images']=[dict(sha256='unexpected',compressed_mip_bytes=300)]
        self.assertFalse(family_residency([('source',a),('source',b)])['passed'])
        b['levels'][0]['mesh_gpu_bytes']=99
        with self.assertRaises(ValueError):family_residency([('source',a),('source',b)])

    def test_kind_markers_do_not_overwrite_siblings(self):
        self.assertEqual(checkpoint_markers({}),('<!-- LOD checkpoint: begin -->','<!-- LOD checkpoint: end -->'))
        self.assertNotEqual(checkpoint_markers(dict(readme_key='section')),checkpoint_markers(dict(readme_key='gate')))

    def test_family_make_is_serial_and_single_override_selects_one_kind(self):
        (ROOT/'build').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='lod-make-',dir=ROOT/'build') as temp:
            root=Path(temp)
            (root/'capture.py').write_text('''import json,sys
from pathlib import Path
args=sys.argv[1:]
with Path('calls.jsonl').open('a') as out:out.write(json.dumps(args)+'\\n')
raise SystemExit(3 if 'check' in args and args[-1]=='src/one.json' else 0)
''')
            (root/'Makefile').write_text(f'''KIT := {ROOT/'kit'}
BP := python3 capture.py
LOD_CONFIGS := src/one.json src/two.json
.DEFAULT_GOAL := all
.PHONY: all check
all:
\t@touch original-all
check:
\t@touch original-check
include {ROOT/'kit/lod_rules.mk'}
''')
            def run(*args):return subprocess.run(['make','--no-print-directory',*args],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            def calls():return [json.loads(line) for line in (root/'calls.jsonl').read_text().splitlines()]
            result=run('lod-mesh');self.assertEqual(result.returncode,0,result.stdout)
            self.assertEqual([a[-1] for a in calls()],['src/one.json','src/two.json'])
            (root/'calls.jsonl').unlink()
            result=run('lod-mesh','LOD_CONFIG=src/two.json');self.assertEqual(result.returncode,0,result.stdout)
            self.assertEqual([a[-1] for a in calls()],['src/two.json'])
            (root/'calls.jsonl').unlink()
            result=run('check-lod');self.assertNotEqual(result.returncode,0)
            self.assertEqual([a[-1] for a in calls()],['src/one.json','src/one.json','src/two.json','src/two.json'])
            count=len(calls());self.assertEqual(run().returncode,0);self.assertEqual(run('check').returncode,0)
            self.assertEqual(len(calls()),count)
            self.assertTrue((root/'original-all').exists() and (root/'original-check').exists())


if __name__=='__main__':unittest.main()
