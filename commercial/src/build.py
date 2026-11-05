"""Build independent original stations; --look installs shared baked PBR.

The scalar branch remains available for construction comparisons. Reusable
modules, pivots and sockets survive both the embedded build and external glTF.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
from mathutils import Matrix
from plan import generate,BRANDS,PROOF_SEEDS,rotate
from geometry import *
from building import retail_shell
from equipment import canopy,dispenser,trash,price_sign,ice,propane,air,lightpole,dumpster_enclosure,bollard
from siteworks import site


def build(seed,out,overrides=None,look=False):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 import geometry
 geometry.SHARED_GRAPHICS=look
 reset_prints();p=generate(seed,overrides);brand=BRANDS[p['brand']];palette(brand,p['building']['wall_color'])
 retail_shell(p['building'],brand);can=canopy(p['canopy'],brand);site(p)
 c=p['canopy'];b=p['building']
 for island in p['islands']:
  x,y=island['center'];u,v=rotate((0,-.96),island['angle'])
  dispenser('Dispenser_'+str(island['index']),(x+u,y+v,.1624),island['angle']+90,brand,island['index'])
  u,v=rotate((0,1.95),island['angle']);trash('TrashWasher_'+str(island['index']),(x+u,y+v,.1624),island['angle'])
 sign=price_sign(p['sign'],(*p['sign_center'],0),brand);sign.rotation_euler.z=math.radians(p['sign_yaw'])
 fy=b['front'];ice((3.5,fy-.53,.1524));propane((-4.0,fy-.53,.1524))
 for i,xx in enumerate((-6.4,-2.5,1.95,6.5)):
  # Door/accessible aisle keep-out leaves a continuous pedestrian approach.
  bollard('StoreBollard_'+str(i),(xx,fy-1.72,.1524))
 air((p['lot'][0]/2-2.1,-5,0))
 dumpster_enclosure((-p['lot'][0]/2+3.0,p['lot'][1]/2-3.1,0))
 for i,(x,y) in enumerate(((-p['lot'][0]/2+1.0,3.0),(p['lot'][0]/2-1.0,-p['lot'][1]/2+1.0))):lightpole('LightPole_'+str(i),(x,y,0))
 if look:
  from age import add
  from surfaces import apply
  add(p);apply(p)
 # Quarter-turn the complete property onto a different corner, retaining local origins.
 world=root('Station_'+str(seed),yaw=p['yaw'],kind='Station')
 for ob in list(bpy.context.scene.objects):
  if ob!=world and ob.parent is None:ob.parent=world;ob['reusable_module']=True
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 finish_prints(out.parent/f'form-graphics-{seed}.png')
 bpy.context.view_layer.update()
 p['hoses']=[dict(name=o.name,centerline_m=[list(o.matrix_world@Vector(o['centerline_m'][i:i+3])) for i in range(0,len(o['centerline_m']),3)],radius_m=o['hose_radius_m']) for o in bpy.context.scene.objects if o.get('hose_radius_m')]
 print('Built modules; finalizing',seed,flush=True)
 finalize();bpy.context.view_layer.update()
 from landscape import plant
 p['landscape']=plant(p,world);bpy.context.view_layer.update()
 bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()),compress=True)
 # Stock exporter, no materials replaced or joined across reusable modules.
 if look:
  from kit.tiling import export
  export(out.with_suffix('.glb'))
 else:bpy.ops.export_scene.gltf(filepath=str(out.with_suffix('.glb').resolve()),export_format='GLB',export_extras=True,export_apply=False,export_yup=True,export_texcoords=True,export_normals=True,export_tangents=False,export_materials='EXPORT',export_cameras=False,export_lights=False)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];counts={}
 for ob in meshes:
  owner=ob.parent
  while owner and owner.parent!=world:owner=owner.parent
  key=owner.name if owner else ob.name
  counts[key]=counts.get(key,0)+len(ob.data.polygons)
 p['triangles']=counts;p['total_triangles']=sum(counts.values())
 p['materials']=len({m.name for o in meshes for m in o.data.materials})
 p['glb_bytes']=out.with_suffix('.glb').stat().st_size
 p['glb_sha256']=hashlib.sha256(out.with_suffix('.glb').read_bytes()).hexdigest()
 p['moving_parts']={o.name:dict(position=list(o.matrix_world.translation),axis=o.get('pivot_axis'),range=list(o.get('range_degrees',[])),detachable=o.get('detachable',False)) for o in bpy.context.scene.objects if o.get('pivot_axis') or o.get('detachable')}
 p['sockets']={o.name:list(o.matrix_world.translation) for o in bpy.context.scene.objects if o.get('socket_kind')}
 out.with_suffix('.json').write_text(json.dumps(p,indent=2)+'\n')
 print('STATION',seed,'triangles',p['total_triangles'],'GLB',p['glb_bytes'],counts)
 return p

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=Path('build/station-101.blend'));a.add_argument('--seeds',default=','.join(map(str,PROOF_SEEDS)));a.add_argument('--plan',type=Path);a.add_argument('--look',action='store_true');a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
 seeds=list(map(int,a.seeds.split(',')))
 for seed in seeds:build(seed,a.out.parent/f'station-{seed}.blend',json.loads(a.plan.read_text()) if a.plan else None,a.look)
