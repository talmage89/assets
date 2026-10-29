"""Kit form bake with separate material projection and assembled contact AO.

Adjacent dense wood and steel must not project into one another. Their AO still
needs the assembled seams. Both passes use the unchanged kit baker/GPU lock;
only the assembled pass's occlusion channel is combined with isolated G/B.
"""
import argparse,json,sys,hashlib
import bpy
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT))
from kit import bake
from kit.image_io import read_png,write_png

def main():
 p=argparse.ArgumentParser();p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=32)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=BASE/'build/baked/4k';out.mkdir(parents=True,exist_ok=True)
 common=['--low',str(BASE/'build/delivery/finalized.blend'),'--high',str(BASE/'build/delivery/high.blend'),
  '--asset','Covey26','--size',str(a.size),'--samples',str(a.samples)]
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
 names=sorted(o.name for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set'))
 projection=BASE/'build/delivery/isolated-bake.py'
 projection.write_text('import runpy\nglobals().update(runpy.run_path('+repr(str(BASE/'src/config.py'))+'))\nBAKE_POLICY=dict(BAKE_POLICY,isolate_moving=True,isolate_rigid_bones=False,moving_roots='+repr(names)+')\n')
 sys.argv=['blender','--',*common,'--config',str(projection),'--out',str(out)]
 bake.main();isolated=json.loads((out/'bake-report.json').read_text())
 contact=out.parent/'assembled-contact';cfg=BASE/'build/delivery/contact-bake.py'
 cfg.write_text('import runpy\nglobals().update(runpy.run_path('+repr(str(BASE/'src/config.py'))+'))\nBAKE_POLICY=dict(BAKE_POLICY,isolate_moving=False,isolate_rigid_bones=True)\n')
 sys.argv=['blender','--',*common,'--config',str(cfg),'--out',str(contact)]
 bake.main();assembled=json.loads((contact/'bake-report.json').read_text())
 assert assembled['AO']['alpha_missed_interior_texels']==0
 orm=read_png(out/'T_Covey26_ORM.png');ao=read_png(contact/'T_Covey26_ORM.png')[:,:,0]
 orm[:,:,0]=ao;write_png(out/'T_Covey26_ORM.png',orm)
 isolated['isolated_projection_AO']=isolated['AO'];isolated['AO']=assembled['AO']
 isolated['assembled_contact_policy']=assembled['projection_policy']
 isolated['parts_isolated']=names
 isolated['channel_policy']='Isolated BaseColor, Normal, roughness and metallic; assembled stationary-contact AO'
 isolated['source_sha256']={name:hashlib.sha256((BASE/'build/delivery'/name).read_bytes()).hexdigest() for name in ('finalized.blend','high.blend')}
 (out/'bake-report.json').write_text(json.dumps(isolated,indent=2))
 print('FORM BAKE COMPLETE: isolated surfaces and assembled contact occlusion',flush=True)
if __name__=='__main__':main()
