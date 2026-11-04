"""Six independent form sources, measured surfaces, motion, and repeat GLB."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import bpy
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from build import build,save
from plan import generate
from cape_plan import PROOF_SEEDS
from cape_check import source_check,check_plan
from cape_lookdev import prepare
from check_mesh import delivery_check
from kit.motion import sweep


def main(a):
    a.out.mkdir(parents=True,exist_ok=True);rows=[]
    for seed in map(int,a.seeds.split(',')):
        plan=generate(seed,json.loads(a.plan.read_text()) if a.plan else None,house_type='cape');check_plan(plan)
        bpy.ops.wm.read_factory_settings(use_empty=True);form=a.out/f'form-{seed}.blend';construction=save(build(plan),form)
        measured=source_check(form);serial=delivery_check(form)
        source=a.out/f'house-{seed}.blend';look=prepare(form,source);actual=source_check(source)
        assert 30000<=look['triangles']<=80000,look['triangles']
        bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
        motions=[dict(node='FrontDoor',axis='Z',range=[0,105],step=3,tolerance_m=.0005),dict(node='ServiceDoor',axis='Z',range=[-100,0],step=5,tolerance_m=.0005)]
        motion=sweep(dict(MOTIONS=motions));(a.out/f'motion-{seed}.json').write_text(json.dumps(motion,indent=2))
        if not motion['passed']:raise AssertionError(f'Motion {seed}: see report')
        m=plan['blocks'][0];rows.append(dict(seed=seed,triangles=look['triangles'],source_triangles=construction['triangles'],main_dimensions_m=[m.width,m.depth],main_ridge_m=m.height(m.cx,m.cy),bounds=look['bounds'],construction=measured,serialization=serial,source=actual,motion=motion))
    first=rows[0];bpy.ops.wm.read_factory_settings(use_empty=True);repeat=save(build(generate(first['seed'],json.loads(a.plan.read_text()) if a.plan else None,house_type='cape')),a.out/'repeat.blend')
    original=json.loads((a.out/f"form-{first['seed']}.json").read_text())
    assert repeat['geometry_sha256']==original['geometry_sha256']
    assert hashlib.sha256((a.out/'repeat.glb').read_bytes()).hexdigest()==first['serialization']['sha256']
    # Exercise caller JSON-equivalent controls independently of the six proofs.
    authored=generate(34,dict(main=dict(pitch=1.,rake=.0508),hood='portico',rear_shed=True,chimney='ridge',garage=dict(kind='none'),siding='cedar',cedar_finish='painted',colors=dict(siding=(.61,.60,.55))),house_type='cape')
    check_plan(authored);bpy.ops.wm.read_factory_settings(use_empty=True);path=a.out/'authored.blend';save(build(authored),path);extra=source_check(path);extra_serial=delivery_check(path)
    painted=a.out/'authored-lookdev.blend';prepare(path,painted);painted_check=source_check(painted)
    (a.out/'checks.json').write_text(json.dumps(dict(passed=True,rows=rows,repeat_geometry_sha256=repeat['geometry_sha256'],authored=extra,authored_serialization=extra_serial,authored_painted_cedar=painted_check),indent=2))
    print('CAPE_SWEEP',len(rows),'sources, surfaces, serializations, motion and repeat passed')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seeds',default=','.join(map(str,PROOF_SEEDS)));p.add_argument('--out',type=Path,default=Path('build/cape'));p.add_argument('--plan',type=Path);main(p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []))
