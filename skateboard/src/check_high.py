"""Dense source clearance, separate from game construction and GLB serialization."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import bpy
from kit.motion import sweep
from kit.assembly import distance
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));motions=[]
for label in ('Front','Rear'):
    motions.append(dict(node='Hanger_'+label,axis='Z',range=[-12,12],step=1,tolerance_m=.0002,
        exclude_fixed=[('Rear' if label=='Front' else 'Front')],allow=[
            dict(moving='',fixed=label+' barrel bushing',reason='Urethane compliance'),
            dict(moving='',fixed=label+' cone bushing',reason='Urethane compliance'),
            dict(moving=label+' sculpted hanger',fixed=label+' pivot cup',reason='Stem retained in compliant pivot cup')]))
result=sweep({'MOTIONS':motions});result['scope']='Dense manufacturing/finish source; sampled rigid-metal clearance, no serialization claim'
result['delamination_support']=[]
deck=next(o for o in bpy.context.scene.objects if o.get('part')=='deck' and o.get('asset_set'))
for o in bpy.context.scene.objects:
    if o.get('part')=='delamination':
        gap,method=distance(o,deck);result['delamination_support'].append(dict(name=o.name,gap_m=gap,method=method));result['passed'] &= gap<.0002
Path(a.out).write_text(json.dumps(result,indent=2));print('DENSE SOURCE CHECK',result['passed'])
if not result['passed']:raise SystemExit(1)
