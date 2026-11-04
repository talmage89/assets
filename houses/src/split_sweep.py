"""Build independent split sources; verify surface, motion and repeat bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import bpy
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from build import build,save
from plan import load,generate
from split_check import check_plan,source_check
from split_lookdev import prepare
from check_mesh import delivery_check
from kit.motion import sweep


def run(a):
    out=Path('build/split');out.mkdir(parents=True,exist_ok=True);rows=[]
    for seed in map(int,a.seeds.split(',')):
        plan=load(seed,a.plan,'split');check_plan(plan)
        bpy.ops.wm.read_factory_settings(use_empty=True);form=out/f'form-{seed}.blend';construction=save(build(plan),form)
        if a.quick:
            prepare(form,out/f'house-{seed}.blend');continue
        measured=source_check(form);serial=delivery_check(form)
        source=out/f'house-{seed}.blend';look=prepare(form,source);actual=source_check(source)
        bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
        motions=[dict(node='FrontDoor',axis='Z',range=[0,105],step=3,tolerance_m=.0005),dict(node='ServiceDoor',axis='Z',range=[-100,0],step=5,tolerance_m=.0005)]
        motion=sweep(dict(MOTIONS=motions));(out/f'motion-{seed}.json').write_text(json.dumps(motion,indent=2))
        assert motion['passed'],f'Motion seed {seed}; see report'
        from split_motion import check as sectional_check
        garage_motion=sectional_check(plan);(out/f'garage-motion-{seed}.json').write_text(json.dumps(garage_motion,indent=2))
        assert garage_motion['passed'],f'Sectional motion {seed}; see garage-motion report'
        rows.append(dict(seed=seed,triangles=look['triangles'],source_triangles=construction['triangles'],levels_m=plan['levels'],blocks=[dict(name=b.name,width_m=b.width,depth_m=b.depth) for b in plan['blocks']],construction=measured,serialization=serial,source=actual,motion=motion,garage_motion=garage_motion))
    if a.quick:return
    seed=int(a.seeds.split(',')[0]);bpy.ops.wm.read_factory_settings(use_empty=True);repeat=save(build(load(seed,a.plan,'split')),out/'repeat.blend')
    original=json.loads((out/f'form-{seed}.json').read_text());assert repeat['geometry_sha256']==original['geometry_sha256']
    assert hashlib.sha256((out/'repeat.glb').read_bytes()).hexdigest()==hashlib.sha256((out/f'form-{seed}.glb').read_bytes()).hexdigest()
    authored_plan=generate(58,dict(kind='side',floor=.6096,main=dict(width=30*.3048,roof='gable',pitch=4/12),wing=dict(side='left',axis='X'),garage=dict(kind='none'),hood='flat',siding='wood'),house_type='split')
    check_plan(authored_plan);bpy.ops.wm.read_factory_settings(use_empty=True)
    path=out/'authored.blend';save(build(authored_plan),path);authored=source_check(path);authored_serial=delivery_check(path)
    (out/'checks.json').write_text(json.dumps(dict(passed=True,rows=rows,authored=authored,authored_serialization=authored_serial,repeat_geometry_sha256=repeat['geometry_sha256'],repeat_glb_sha256=hashlib.sha256((out/'repeat.glb').read_bytes()).hexdigest()),indent=2))
    print('SPLIT_SWEEP',len(rows),'passed')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seeds',default='51,52,53,54,55,56');p.add_argument('--plan',type=Path);p.add_argument('--quick',action='store_true');run(p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []))
