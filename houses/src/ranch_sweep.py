"""Build six ranch sources, sampled surfaces, moving leaves and repeat export."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import bpy
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from build import build,save
from plan import generate
from ranch_plan import PROOF_SEEDS
from ranch_lookdev import prepare
from check_mesh import source_check,delivery_check
from kit.motion import sweep


def main(a):
 a.out.mkdir(parents=True,exist_ok=True);rows=[]
 for seed in map(int,a.seeds.split(',')):
  bpy.ops.wm.read_factory_settings(use_empty=True);form=a.out/f'form-{seed}.blend'
  construction=save(build(generate(seed,json.loads(a.plan.read_text()) if a.plan else None,house_type='ranch')),form)
  measured=source_check(form);serial=delivery_check(form)
  source=a.out/f'house-{seed}.blend';look=prepare(form,source)
  actual=source_check(source)
  # Motion is measured on the unmerged construction components, including
  # all tagged solid geometry. No exclusions or contact exemptions.
  bpy.ops.wm.open_mainfile(filepath=str(form.resolve()))
  motions=[dict(node='FrontDoor',axis='Z',range=[0,105],step=3,tolerance_m=.0005),
   dict(node='PatioDoor',axis='X',kind='translation',range=[0,.8382],step=.04,tolerance_m=.0005)]
  if 'ServiceDoor' in bpy.data.objects:
   # Back-wall service door uses the existing inward-opening hinge.
   motions.append(dict(node='ServiceDoor',axis='Z',range=[-100,0],step=5,tolerance_m=.0005))
  motion=sweep(dict(MOTIONS=motions));(a.out/f'motion-{seed}.json').write_text(json.dumps(motion,indent=2))
  if not motion['passed']:raise AssertionError(f'Motion {seed}: see report')
  assert 30000<=look['triangles']<=80000,look['triangles']
  rows.append(dict(seed=seed,triangles=look['triangles'],dimensions_m=[max(b['x1'] for b in look['blocks'])-min(b['x0'] for b in look['blocks']),max(b['y1'] for b in look['blocks'])-min(b['y0'] for b in look['blocks'])],
   construction=measured,serialization=serial,source=actual,motion=motion))
 first=rows[0];bpy.ops.wm.read_factory_settings(use_empty=True);repeat=save(build(generate(first['seed'],json.loads(a.plan.read_text()) if a.plan else None,house_type='ranch')),a.out/'repeat.blend')
 original=json.loads((a.out/f"form-{first['seed']}.json").read_text())
 assert repeat['geometry_sha256']==original['geometry_sha256']
 assert hashlib.sha256((a.out/'repeat.glb').read_bytes()).hexdigest()==first['serialization']['sha256']
 # A caller-authored JSON-equivalent override must also build and be audited.
 bpy.ops.wm.read_factory_settings(use_empty=True)
 authored=generate(14,dict(main=dict(roof='gable',pitch=3/12),garage=dict(side='left',entry='side'),brick_color='buff'),house_type='ranch')
 from check_plan import check
 check(authored);path=a.out/'authored.blend';save(build(authored),path);extra=source_check(path)
 (a.out/'checks.json').write_text(json.dumps(dict(passed=True,rows=rows,repeat_geometry_sha256=repeat['geometry_sha256'],authored=extra),indent=2))
 print('RANCH_SWEEP',len(rows),'surfaces, serializations, motion and repeat passed')


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--plan',type=Path);p.add_argument('--out',type=Path,default=Path('build/ranch'));p.add_argument('--seeds',default=','.join(map(str,PROOF_SEEDS)));a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);main(a)
