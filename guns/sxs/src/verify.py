"""Raw GLB plus fresh-import affine, intended-state and surface verification."""
import sys,json,hashlib
from pathlib import Path
import numpy as np
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import weapon as W,weapon_verify as V,motion
from kit.gltf import GLB
from parameters import generator_digest
from semantics import check as semantics
from contacts import measure,ray
from interface import CLIPS
BASE=Path(__file__).resolve().parents[1]
def main():
 source=BASE/'build/sxs.blend';path=source.with_suffix('.glb')
 bpy.ops.wm.open_mainfile(filepath=str(source));arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
 assert arm['generator_sha256']==generator_digest(),'Stale source generator'
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o]
 sockets=[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')]
 samples=[(name,f/2) for name,s in CLIPS.items() for f in range(s['frames']*2+1)]
 expected=V.capture(arm,samples,sockets);source_semantics=semantics(arm)
 targets={}
 for name,s in CLIPS.items():
  for f in sorted({0,s['frames'],s['frames']/2,*s['events'].values()}):
   W.pose(arm,name,f);targets[name,f]=V.surface_points(parts)
 W.pose(arm,'Idle',0)
 active=[o for o in parts if min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())>.001]
 p=np.array(V.surface_points(active));bounds=[p.min(axis=0).tolist(),p.max(axis=0).tolist()]
 trigger=ray('Front_Trigger',(.0026,.095,-.012),(0,-1,0));butt=ray('Butt_Plate',(0,-.33,-.012),(0,1,0))
 pull=trigger.y-butt.y
 dims={}
 for name in ('Barrel_R','Barrel_L','Stock_Walnut','Forend_Walnut'):
  ob=next(o for o in parts if o.get('part_name')==name);p=np.array(V.surface_points([ob]));dims[name]=((p.max(axis=0)-p.min(axis=0))*1000).tolist()
 spawn={}
 for name,bone,clip in [('shell','LiveR','Idle'),('hull','HullR','IdleSpent')]:
  W.pose(arm,clip,0);spawn[name]=(V.surface_points([o for o in parts if o['bone']==bone]),arm.matrix_world@arm.pose.bones[bone].matrix)
 data=GLB(path);prims=[p for m in data.json['meshes'] for p in m['primitives']]
 count=sum(len(data.accessor(p['indices']))//3 for p in prims)
 assert 25000<=count<=35000,count
 assert not data.json.get('images'),'Checkpoint carries no final atlas'
 assert {a['name'] for a in data.json['animations']}==set(CLIPS)
 for p in prims:
  w=data.accessor(p['attributes']['WEIGHTS_0']);assert np.max(abs(w.sum(axis=1)-1))<1e-6
  assert np.all((w>1e-6).sum(axis=1)==1)
  n=data.accessor(p['attributes']['NORMAL']);assert np.max(abs(np.linalg.norm(n,axis=1)-1))<1e-5
 normals=V.normal_direction(data);arm=V.import_glb(path);imported_semantics=semantics(arm)
 contacts=measure(arm);assert contacts['passed'],[r for r in contacts.get('records',[]) if not r['passed']]
 affine=V.compare(arm,expected,position_tolerance_m=3e-6,linear_tolerance=.001)
 imported=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o]
 errors=[]
 for (clip,f),target in targets.items():
  W.pose(arm,clip,f);error=V.surface_delta(target,V.surface_points(imported));assert error<3e-6,(clip,f,error)
  errors.append(dict(clip=clip,frame=f,error_m=error))
 result=dict(passed=True,stage='unbaked visual form checkpoint',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
  triangles=count,materials=len(data.json['materials']),textures=0,glb_bytes=path.stat().st_size,
  bones=len(arm.data.bones),clips=len(CLIPS),sockets=len(sockets),parts=len(parts),bounds_m=bounds,
  dimensions_mm=((np.array(bounds[1])-bounds[0])*1000).tolist(),measured_parts_mm=dims,length_of_pull_mm=pull*1000,
  normals=normals,affine_samples=len(affine),max_position_error_m=max(r['position_delta_m'] for r in affine),
  max_linear_error=max(r['linear_delta'] for r in affine),surface_poses=errors,
  source_semantics=source_semantics,imported_semantics=imported_semantics,imported_contacts=contacts,standalones={})
 for name,(target,xf) in spawn.items():
  item=BASE/'build'/(name+'.glb');data=GLB(item);normal=V.normal_direction(data);V.import_glb(item)
  meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(meshes)==1 and meshes[0].matrix_world.is_identity
  vertices=V.surface_points(meshes);error=V.surface_delta(target,[xf@Vector(v) for v in vertices]);assert error<3e-6,(name,error)
  p=np.array(vertices);size=(p.max(axis=0)-p.min(axis=0))*1000
  assert abs(size[0]-22.4)<.01 and abs(size[1]-(57.5 if name=='shell' else 69.8))<.2,(name,size)
  result['standalones'][name]=dict(bytes=item.stat().st_size,dimensions_mm=size.tolist(),normals=normal,spawn_error_m=error,
   triangles=sum(len(data.accessor(p['indices']))//3 for m in data.json['meshes'] for p in m['primitives']))
 (BASE/'build/serialization.json').write_text(json.dumps(result,indent=2));print('SERIALIZATION PASS',count,len(affine),'affine samples')
if __name__=='__main__':main()
