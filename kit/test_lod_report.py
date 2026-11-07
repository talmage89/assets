"""Family LOD accounting, independent config reports and opt-in Make hooks."""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from kit.lod_report import family_residency,checkpoint_markers,block,stored_totals
from kit.lod import image_limits

ROOT=Path(__file__).resolve().parents[1]


class LODFamilyReportTests(unittest.TestCase):
    def test_stored_counts_measure_full_container_and_deduplicate_siblings(self):
        import numpy as np
        from kit.lod_io import Document,shared_material_bindings
        (ROOT/'build').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='lod-stored-',dir=ROOT/'build') as folder:
            root=Path(folder);stub=root/'stub.gltf'
            stub.write_text(json.dumps(dict(asset=dict(version='2.0'),scene=0,scenes=[dict(nodes=[0,1,2])],
                nodes=[dict(name='A',mesh=0),dict(name='B',mesh=1),dict(name='B2',mesh=1)],
                meshes=[dict(primitives=[dict(attributes={},indices=0,material=i)]) for i in range(2)],
                accessors=[],buffers=[],bufferViews=[],materials=[dict(name='one'),dict(name='two')],images=[])))
            original=Document(stub)
            attrs=dict(POSITION=np.array([[0,0,0],[1,0,0],[0,1,0]],np.float32),
                       NORMAL=np.tile([0,0,1],(3,1)).astype(np.float32))
            for mesh in original.data['meshes']:original.replace(mesh['primitives'][0],attrs,np.array([[0,1,2]],np.uint32))
            source=root/'source.gltf';original.save(source);chains=[];payload={source,source.with_suffix('.bin')}
            for name in ['A','B']:
                doc=Document(source);doc.select([name]);path=root/(name+'.gltf');doc.save(path)
                payload.update([path,path.with_suffix('.bin')])
                manifest=dict(levels=[dict(level=0,path=source.name,triangles=1,draw_calls=1),
                    dict(level=1,path=path.name,triangles=1,draw_calls=1,shared_maps=True,
                         canonical_material_bindings=shared_material_bindings(Document(source),Document(path)))])
                chains.append(('same full source',manifest,root))
            totals=stored_totals(chains)
            self.assertEqual(totals['stored_mesh_triangles'],4) # two in full source, one per new kind
            self.assertEqual(totals['material_resources'],2)
            self.assertEqual(totals['stored_primitive_placements'],5) # source has an instance
            self.assertEqual(totals['distinct_payload_bytes'],sum(p.stat().st_size for p in payload))
            self.assertEqual((totals['active_draw_calls_min'],totals['active_draw_calls_max']),(1,1))

    def test_calibrated_local_limit_cannot_leak_into_far_level(self):
        cfg=dict(silhouette_loss=.073,levels=[dict(image_limits=dict(patch_mean_max=.21)),{},{}])
        self.assertEqual(image_limits(cfg,1),dict(mean=.02,p95=.08,alpha_mae=.05,patch_mean_max=.21,silhouette_loss=.073))
        self.assertEqual(image_limits(cfg,3)['patch_mean_max'],.08)
        cfg['image_limits']=dict(mean=.015)
        self.assertEqual(image_limits(cfg,2)['mean'],.015)
        self.assertEqual(image_limits(cfg,2)['p95'],.08)
        for bad in [dict(typo=.1),dict(mean=float('nan')),dict(mean=-.1),dict(mean=1.1)]:
            cfg['image_limits']=bad
            with self.assertRaises(ValueError):image_limits(cfg,1)

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
