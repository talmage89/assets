"""Fresh final GLBs: atlas, skin/clips, actual surfaces and detached frames."""
import json,sys,io,hashlib
from pathlib import Path
import bpy,numpy as np
from PIL import Image
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import uv,weapon as W,weapon_verify as V
from kit.gltf import GLB
from kit import detachable_verify as DV
from interface import CLIPS
from check import semantics,geometry,meshes
from delivery import split_imported

def main():
 source=BASE/'build/delivery/finalized.blend';bpy.ops.wm.open_mainfile(filepath=str(source))
 arm=bpy.data.objects['R39Armature'];objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')]
 u=uv.report(objects,size=2048)
 assert not u['outside_triangles'] and not u['degenerate_uv_triangles'] and u['overlap_fraction']<1e-5,u
 assert 1200<u['density_px_m']['50']<5000,u['density_px_m']
 source_states=semantics(arm);source_geometry=geometry(arm)
 samples=[(c,i*.5) for c,s in CLIPS.items() for i in range(s['frames']*2+1)]
 expected=V.capture(arm,samples,[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')])
 surfaces={}
 for c,s in CLIPS.items():
  for f in sorted({0,s['frames'],*s['events'].values()}):
   W.pose(arm,c,f);surfaces[c,f]=V.surface_points(meshes(arm))
 magparts=[o for o in meshes(arm) if o['bone'] in ('Magazine','Follower','TopRound','SecondRound','ThirdRound')];spawns={}
 for state,clip in [('loaded','Reload'),('empty','ReloadEmpty')]:
  W.pose(arm,clip,56);visible=[o for o in magparts if min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())>.001]
  spawns[state]=V.surface_points(visible),bpy.data.objects['Socket_Magazine'].matrix_world.copy()
 bake=json.loads((BASE/'build/baked/4k/bake-report.json').read_text());assert bake['size']==4096 and bake['samples']>=32
 for channel in ('BaseColor','BaseColorAlpha','Roughness','Metallic','AO','MaterialAO','Normal'):
  assert bake[channel]['alpha_missed_interior_texels']==0,(channel,bake[channel])
 canonical=sorted(hashlib.sha256((BASE/'textures'/('T_Rill39_'+c+'.png')).read_bytes()).hexdigest() for c in ('BaseColor','Normal','ORM'));outputs={}
 for name,limit in [('ak',40000),('magazine_loaded',7000),('magazine_empty',5000),('cartridge',1100),('case',800)]:
  path=BASE/'export'/(name+'.glb');g=GLB(path)
  tri=sum(len(g.accessor(p['indices']))//3 for m in g.json['meshes'] for p in m['primitives'])
  assert tri<=limit and len(g.json['materials'])==1 and len(g.json['images'])==3,(name,tri)
  hashes=sorted(hashlib.sha256(g.image(i)).hexdigest() for i in range(3))
  subset=None;map_size=2048
  if name=='ak':assert hashes==canonical
  else:
   layout=BASE/'build/delivery/detachables'/name/'layout.json'
   subset=DV.audit(path,BASE/'textures','Rill39',layout,gun=BASE/'export/ak.glb')
   subset['mip_bleed']=DV.mip_bleed(path,BASE/'textures','Rill39',layout,gun=BASE/'export/ak.glb')
   map_size=subset['size'];assert map_size==dict(magazine_loaded=1024,magazine_empty=1024,cartridge=512,case=512)[name]
   assert subset['padding_px']==8
  for i in range(3):assert Image.open(io.BytesIO(g.image(i))).size==(map_size,map_size)
  material=g.json['materials'][0];assert material.get('alphaMode','OPAQUE')=='OPAQUE'
  spec=material['extensions']['KHR_materials_specular']['specularTexture']['index']
  assert g.json['textures'][spec]['source']==g.json['textures'][material['pbrMetallicRoughness']['baseColorTexture']['index']]['source']
  assert Image.open(io.BytesIO(g.image(g.json['textures'][spec]['source']))).mode=='RGBA'
  if name=='ak':
   assert len(g.json['skins'])==1 and {a['name'] for a in g.json['animations']}==set(CLIPS)
   for a in g.json['animations']:
    times=[g.accessor(s['input']) for s in a['samplers']]
    assert abs(min(float(t.min()) for t in times))<1e-7
    assert abs(max(float(t.max()) for t in times)-CLIPS[a['name']]['frames']/60)<1e-6
  else:assert not g.json.get('skins') and not g.json.get('animations')
  for m in g.json['meshes']:
   for p in m['primitives']:
    normals=g.accessor(p['attributes']['NORMAL']);assert np.isfinite(normals).all() and np.max(abs(np.linalg.norm(normals,axis=1)-1))<1e-5
    if name=='ak':
     weights=g.accessor(p['attributes']['WEIGHTS_0']);assert np.max(abs(weights.sum(axis=1)-1))<1e-6 and np.all(np.sum(weights>1e-6,axis=1)==1)
  outputs[name]=dict(triangles=tri,materials=1,images=3,size=map_size,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),image_hashes=hashes,normal_direction=V.normal_direction(g))
  if subset is not None:outputs[name]['standalone_textures']=subset
 arm=V.import_glb(BASE/'export/ak.glb');states=semantics(arm)
 imported_uv=uv.report([o for o in bpy.context.scene.objects if o.type=='MESH'],size=2048)
 assert not imported_uv['outside_triangles'] and not imported_uv['degenerate_uv_triangles'] and imported_uv['overlap_fraction']<1e-5
 affine=V.compare(arm,expected,position_tolerance_m=2e-5,linear_tolerance=5e-4);surface_rows=[]
 for (c,f),points in surfaces.items():
  W.pose(arm,c,f);error=V.surface_delta(points,V.surface_points([o for o in bpy.context.scene.objects if o.type=='MESH']));assert error<2e-6,(c,f,error)
  surface_rows.append(dict(clip=c,frame=f,delta_m=error))
 diagnostic=split_imported(bpy.context.scene,source);W.pose(arm,'Idle',0)
 bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'build/delivery/imported-parts.blend'))
 for name in ('magazine_loaded','magazine_empty','cartridge','case'):
  V.import_glb(BASE/'export'/(name+'.glb'));parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==1
  points=V.surface_points(parts);size=(np.max(points,axis=0)-np.min(points,axis=0)).tolist();outputs[name]['fresh_import_dimensions_m']=size
  if name.startswith('magazine'):
   target,spawn=spawns[name.split('_')[1]];error=V.surface_delta(target,[tuple(spawn@Vector(v)) for v in points]);assert error<2e-6
   outputs[name]['full_rotated_spawn_delta_m']=error
  elif name=='case':assert abs(size[1]-.0386)<.00001
  else:assert abs(size[1]-.0558)<.00001
 keys=('coverage','outside_triangles','degenerate_uv_triangles','overlap_pairs','overlap_fraction','density_px_m')
 result=dict(passed=True,outputs=outputs,source_geometry=source_geometry,uv={k:u[k] for k in keys},imported_uv={k:imported_uv[k] for k in keys},source_states=source_states,imported_states=states,
  bake_size=bake['size'],bake_samples=bake['samples'],missed_interior_texels=0,affine_samples=len(affine),maximum_position_delta_m=max(r['position_delta_m'] for r in affine),maximum_linear_delta=max(r['linear_delta'] for r in affine),posed_surfaces=surface_rows,imported_diagnostic_reconstruction=diagnostic,gpu_memory_mib_bc_with_mips=16)
 (BASE/'build/delivery/verify.json').write_text(json.dumps(result,indent=2));print('RILL39 FINAL ATLAS VERIFIED',len(affine),'samples',flush=True)
if __name__=='__main__':main()
