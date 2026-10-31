"""Separate enamel projection from neighboring accepted finish sources.

Use the kit bake unchanged. This wrapper only assigns bake-only projection
owners, splitting each existing rigid group into enamel and non-enamel. The
low target, source shapes, UVs, finish coordinates and delivery stay unchanged.
The kit retains stationary ghost geometry for contact AO.
"""
import json,runpy,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import bake,bake_groups

def main():
 args=sys.argv[sys.argv.index('--')+1:]
 config=Path(args[args.index('--config')+1]).resolve()
 low=Path(args[args.index('--low')+1]).resolve()
 cfg=runpy.run_path(str(config));policy=cfg['BAKE_POLICY']
 bpy.ops.wm.open_mainfile(filepath=str(low))
 objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]
 roots=list(policy.get('moving_roots',[])) if policy.get('isolate_moving') else []
 if policy.get('isolate_rigid_bones'):
  roots+=sorted({'rigid:'+o['bone'] for o in objects if o.get('bone') and o['bone']!='Root'})
 original=bake_groups.owner;aliases={}
 for ob in objects:
  roles=[m.name.removeprefix('CP_').removeprefix('Inspection_').split('.')[0] for m in ob.data.materials]
  enamel=(any(r=='paint' for r in roles) and not ob.name.startswith('Magazine_')) or ob.name.startswith(('TriggerGuard_','Guard_')) or (cfg['EXPORT_VARIANT']=='smg' and ob.name=='Handle_Grip')
  if enamel:aliases[ob.name]='enamel:'+original(ob,roots)
 virtual=sorted(set(aliases.values()))
 def owner(ob,all_roots):
  name=ob.get('finish_part',ob.get('part_name',ob.get('low_target',ob.name)))
  return aliases.get(name,original(ob,all_roots))
 bake_groups.owner=owner
 old_run=runpy.run_path
 def settings(path,*args,**kwargs):
  row=old_run(path,*args,**kwargs)
  if Path(path).resolve()==config:
   row['BAKE_POLICY']=dict(row['BAKE_POLICY'],isolate_moving=True,moving_roots=list(policy.get('moving_roots',[]))+virtual)
  return row
 runpy.run_path=settings
 out=Path(args[args.index('--out')+1]);out.mkdir(parents=True,exist_ok=True)
 (out/'paint-projection.json').write_text(json.dumps(dict(aliases=aliases,scope=__doc__),indent=2))
 bake.main()
if __name__=='__main__':main()
