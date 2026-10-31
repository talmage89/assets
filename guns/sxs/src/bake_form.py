"""Kit form bake with separate material projection and assembled contact AO.

Adjacent dense wood and steel must not project into one another. Their AO still
needs the assembled seams. Both passes use the unchanged kit baker/GPU lock;
only the assembled pass's occlusion channel is combined with isolated G/B.
"""
import argparse,json,sys,hashlib,time
import bpy,numpy as np
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT))
from kit import bake
from kit.image_io import read_png,write_png

def main():
 p=argparse.ArgumentParser();p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=32)
 p.add_argument('--high',type=Path,default=BASE/'build/delivery/high.blend')
 p.add_argument('--out',type=Path,default=BASE/'build/baked/4k')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
 common=['--low',str(BASE/'build/delivery/finalized.blend'),'--high',str(a.high.resolve()),
  '--asset','Covey26','--size',str(a.size),'--samples',str(a.samples)]
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
 names=sorted(o.name for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set'))
 projection=BASE/'build/delivery/isolated-bake.py'
 projection.write_text('import runpy\nglobals().update(runpy.run_path('+repr(str(BASE/'src/config.py'))+'))\nBAKE_BASECOLOR_ALPHA_CHANNEL="owner"\nBAKE_POLICY=dict(BAKE_POLICY,isolate_moving=True,isolate_rigid_bones=False,moving_roots='+repr(names)+')\n')
 sys.argv=['blender','--',*common,'--config',str(projection),'--out',str(out)]
 bake.main();isolated=json.loads((out/'bake-report.json').read_text())
 color=read_png(out/'T_Covey26_BaseColor.png')
 write_png(out/'projection-owner.png',color[:,:,3:4])
 # Reuse the kit's isolated target, sources, cage, selection and GPU scene
 # for this asset's additional scalar. The first alpha remains an independent
 # source-identity witness; the delivered alpha must use the SAME isolation.
 target=bpy.context.view_layer.objects.active
 assert target.name=='Atlas bake target' and bpy.context.scene.render.bake.use_selected_to_active
 for ob in bpy.context.selected_objects:
  if ob==target:continue
  for mat in ob.data.materials:
   nt=mat.node_tree;emission=nt.nodes['BAKE_EMIT']
   nt.links.new(nt.nodes['OUT_specular_factor'].outputs[0],emission.inputs['Color'])
   nt.links.new(emission.outputs[0],nt.nodes['OUT'].inputs['Surface'])
 image=bpy.data.images.new('Covey isolated reflection',a.size,a.size,alpha=True,float_buffer=True)
 image.colorspace_settings.name='Non-Color';target.active_material.node_tree.nodes.active.image=image
 start=time.time();bpy.ops.object.bake(type='EMIT')
 values=np.empty(a.size*a.size*4,np.float32);image.pixels.foreach_get(values)
 values=np.flipud(values.reshape(a.size,a.size,4));covered=color[:,:,3]>0
 missing=int(np.count_nonzero(covered&(values[:,:,3]<.5)));assert missing==0,missing
 specular=values[:,:,:1].copy()
 isolated['specular_alpha_projection']=dict(seconds=time.time()-start,checked_owner_covered_texels=int(covered.sum()),
  alpha_missed_owner_covered_texels=missing,min=float(specular.min()),max=float(specular.max()))
 isolated['specular_alpha_policy']='Isolated named-part projection in the unchanged kit scene; source dielectric IOR level times two. Independent first-pass owner witness retained.'
 write_png(out/'T_Covey26_BaseColor.png',np.concatenate((color[:,:,:3],specular),axis=2))
 bpy.data.images.remove(image)
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
 isolated['channel_policy']='Isolated BaseColor, reflection factor, Normal, roughness and metallic; assembled stationary-contact AO'
 isolated['source_sha256']={'finalized.blend':hashlib.sha256((BASE/'build/delivery/finalized.blend').read_bytes()).hexdigest(),
  'high.blend':hashlib.sha256(a.high.read_bytes()).hexdigest()}
 isolated['source_files']={'low':str(BASE/'build/delivery/finalized.blend'),'high':str(a.high.resolve())}
 (out/'bake-report.json').write_text(json.dumps(isolated,indent=2))
 print('FORM BAKE COMPLETE: isolated surfaces and assembled contact occlusion',flush=True)
if __name__=='__main__':main()
