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
from form_gauges import measure as form_gauges
from action_gauges import measure as action_gauges
from head_gauges import measure as head_gauges
from projection_check import measure as projection_ownership
from kit import uv
from PIL import Image
import io
from interface import CLIPS
BASE=Path(__file__).resolve().parents[1]
def main():
 source=BASE/'build/sxs.blend';path=BASE/'export/sxs.glb'
 ownership=projection_ownership();assert ownership['passed'],[r for r in ownership['records'] if r['wrong_constant_texels']]
 (BASE/'build/delivery/projection-ownership.json').write_text(json.dumps(ownership,indent=2))
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
 assert 25000<=count<=39000,count
 assert len(data.json['materials'])==1 and len(data.json['images'])==3
 for i in range(3):assert Image.open(io.BytesIO(data.image(i))).size==(2048,2048)
 png_bits=[data.image(i)[24] for i in range(3)]
 assert sorted(png_bits)==[8,8,16],png_bits
 baked=json.loads((BASE/'build/baked/4k/bake-report.json').read_text())
 assert baked['size']==4096 and baked['samples']>=32 and baked['device']=='GPU'
 for name,digest in baked['source_sha256'].items():
  assert digest==hashlib.sha256((BASE/'build/delivery'/name).read_bytes()).hexdigest(),'Stale baked source '+name
 projection=json.loads((BASE/'build/baked/precise4k/projection-report.json').read_text())
 assert projection['size']==4096 and projection['interior_texels']>0
 assert set(projection['regions'])=={'0','1','2','3','4'}
 assert all(r['triangles']>0 and r['texels']>0 for r in projection['regions'].values())
 assert all(projection['regions'][r]['maximum_projection_distance_mm']<.12 for r in ('1','2','3','4'))
 assert projection['ground_triangles']==99 and projection['ground_texels']>0
 assert projection['gutter_policy']=='Exact action pixel-center occupancy; conservatively block every other part'
 assert projection['source_sha256']==baked['source_sha256']
 assert projection['gpu_normal_sha256']==hashlib.sha256((BASE/'build/baked/4k/T_Covey26_Normal.png').read_bytes()).hexdigest()
 assert projection['output_normal_sha256']==hashlib.sha256((BASE/'build/baked/precise4k/T_Covey26_Normal.png').read_bytes()).hexdigest()
 assert set(baked['parts_isolated'])=={o.name for o in parts}
 assert set(baked['projection_policy']['moving_roots'])==set(baked['parts_isolated'])
 assert 'Stock_Walnut' not in baked['assembled_contact_policy']['moving_roots']
 assert all(baked[c]['alpha_missed_interior_texels']==0 for c in ('BaseColor','Roughness','Metallic','AO','Normal'))
 hashes=sorted(hashlib.sha256(data.image(i)).hexdigest() for i in range(3))
 assert hashes==sorted(hashlib.sha256((BASE/'textures'/('T_Covey26_'+c+'.png')).read_bytes()).hexdigest() for c in ('BaseColor','Normal','ORM'))
 assert {a['name'] for a in data.json['animations']}==set(CLIPS)
 for p in prims:
  w=data.accessor(p['attributes']['WEIGHTS_0']);assert np.max(abs(w.sum(axis=1)-1))<1e-6
  assert np.all((w>1e-6).sum(axis=1)==1)
  n=data.accessor(p['attributes']['NORMAL']);assert np.max(abs(np.linalg.norm(n,axis=1)-1))<1e-5
 normals=V.normal_direction(data);arm=V.import_glb(path);imported_semantics=semantics(arm)
 contacts=measure(arm);gauges=form_gauges(arm);gauges['action_round4']=action_gauges(arm);gauges['head_round5']=head_gauges(arm)
 imported_uv=uv.report([o for o in bpy.context.scene.objects if o.type=='MESH'],size=2048)
 assert not imported_uv['outside_triangles'] and not imported_uv['degenerate_uv_triangles'] and imported_uv['overlap_fraction']<1e-5
 assert 1400<imported_uv['density_px_m']['50']<3000
 assert contacts['passed'],[r for r in contacts.get('records',[]) if not r['passed']]
 affine=V.compare(arm,expected,position_tolerance_m=3e-6,linear_tolerance=.001)
 imported=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o]
 errors=[]
 for (clip,f),target in targets.items():
  W.pose(arm,clip,f);error=V.surface_delta(target,V.surface_points(imported));assert error<3e-6,(clip,f,error)
  errors.append(dict(clip=clip,frame=f,error_m=error))
 result=dict(passed=True,stage='baked form checkpoint; finish and wear held',uv=imported_uv,bake_size=4096,ship_size=2048,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
  triangles=count,materials=len(data.json['materials']),textures=3,texture_png_bits=png_bits,glb_bytes=path.stat().st_size,projection_ownership=ownership,action_normal_projection=projection,
  bones=len(arm.data.bones),clips=len(CLIPS),sockets=len(sockets),parts=len(parts),bounds_m=bounds,
  dimensions_mm=((np.array(bounds[1])-bounds[0])*1000).tolist(),measured_parts_mm=dims,length_of_pull_mm=pull*1000,
  normals=normals,affine_samples=len(affine),max_position_error_m=max(r['position_delta_m'] for r in affine),
  max_linear_error=max(r['linear_delta'] for r in affine),surface_poses=errors,
  form_gauges=gauges,source_semantics=source_semantics,imported_semantics=imported_semantics,imported_contacts=contacts,standalones={})
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
