"""Raw GLB, fresh imports, intended contacts/states and full affine round trip."""
import sys,argparse,json,hashlib
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import weapon as W,weapon_verify as V
from kit.gltf import GLB
from interface import CLIPS
from semantics import check
from contacts import measure
from check import geometry,sweep
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/shotgun.blend');p.add_argument('--out',default='build/serialization.json');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 source=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(source));arm=bpy.data.objects['ShotgunArmature']
 assert bpy.context.scene.get('generator_sha256')==hashlib.sha256((Path(__file__).parent/'build.py').read_bytes()).hexdigest(),'Stale modeled source'
 source_states=check(arm);source_contacts=measure(arm);source_geometry=geometry(arm)
 samples=[(c,i*.5) for c,s in CLIPS.items() for i in range(s['frames']*2+1)]
 sockets=[o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')]
 expected=V.capture(arm,samples,sockets)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o and not o.get('bake_only')]
 surfaces={}
 for c,s in CLIPS.items():
  for f in sorted({0,s['frames'],*s['events'].values()}):
   W.pose(arm,c,f);surfaces[(c,f)]=V.surface_points(meshes)
 raw=GLB(source.with_suffix('.glb'));triangles=0
 for m in raw.json['meshes']:
  for p in m['primitives']:
   triangles+=len(raw.accessor(p['indices']))//3
   weights=raw.accessor(p['attributes']['WEIGHTS_0'])
   assert np.max(np.abs(weights.sum(axis=1)-1))<1e-6
   assert np.all(np.sum(weights>1e-6,axis=1)==1)
   normals=raw.accessor(p['attributes']['NORMAL']);positions=raw.accessor(p['attributes']['POSITION'])
   assert np.isfinite(normals).all() and np.isfinite(positions).all()
   assert np.max(np.abs(np.linalg.norm(normals,axis=1)-1))<1e-5
 assert triangles==source_geometry['triangles']
 assert {a['name'] for a in raw.json['animations']}==set(CLIPS)
 assert not raw.json.get('images')
 assert any(s['interpolation']=='STEP' for a in raw.json['animations'] for s in a['samplers'])
 normal=V.normal_direction(raw)
 arm=V.import_glb(source.with_suffix('.glb'));imported_states=check(arm);imported_contacts=measure(arm);imported_geometry=geometry(arm)
 imported_motion=sweep(arm);assert imported_motion['passed'],'Imported motion clearance'
 rows=V.compare(arm,expected,position_tolerance_m=2e-5,linear_tolerance=5e-4)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];errors=[]
 for (c,f),points in surfaces.items():
  W.pose(arm,c,f);d=V.surface_delta(points,V.surface_points(meshes));assert d<2e-5,(c,f,d)
  errors.append(dict(clip=c,frame=f,delta_m=d))
 result=dict(passed=True,triangles=triangles,bytes=source.with_suffix('.glb').stat().st_size,
  materials=len(raw.json['materials']),texture_images=0,normal_direction=normal,
  source_states=source_states,imported_states=imported_states,source_contacts=source_contacts,imported_contacts=imported_contacts,
  source_geometry=source_geometry,imported_geometry=imported_geometry,imported_motion=imported_motion,affine_samples=len(rows),
  maximum_position_delta_m=max(r['position_delta_m'] for r in rows),maximum_linear_delta=max(r['linear_delta'] for r in rows),
  surface_samples=errors,standalones={})
 for name,limit,length in [('shell',600,.0575),('hull',400,.0698)]:
  path=source.parent/(name+'.glb');raw=GLB(path)
  tri=sum(len(raw.accessor(p['indices']))//3 for m in raw.json['meshes'] for p in m['primitives']);assert tri<=limit
  normal=V.normal_direction(raw);assert not raw.json.get('animations') and not raw.json.get('skins')
  rim=[];alignment=[]
  for m in raw.json['meshes']:
   for p in m['primitives']:
    xyz=raw.accessor(p['attributes']['POSITION']);nrm=raw.accessor(p['attributes']['NORMAL'])
    radius=np.linalg.norm(xyz[:,:2],axis=1)
    rim.extend(xyz[np.abs(radius-.0112)<2e-7,:2])
    if raw.json['materials'][p['material']]['name'].startswith('CP_hull'):
     # The optimized cylinder has only end rings, with no middle vertices.
     # Sample its actual outer end ring, excluding the crimp and muzzle bevel.
     select=(radius>.00999)&(radius<.01013)&(np.abs(xyz[:,2])>.0104)&(np.abs(xyz[:,2])<.055)
     if np.any(select):alignment.extend(np.sum(nrm[select,:2]*xyz[select,:2]/radius[select,None],axis=1))
  sides=len(np.unique(np.round(np.asarray(rim),7),axis=0))
  assert sides>=(32 if name=='shell' else 28),(name,sides)
  assert alignment,(name,'No exterior cylinder samples')
  assert min(alignment)>.9999,(name,min(alignment))
  V.import_glb(path);parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(parts)==1 and parts[0].matrix_world.is_identity
  points=V.surface_points(parts);lo=np.min(points,axis=0);hi=np.max(points,axis=0);dims=hi-lo
  assert abs(dims[1]-length)<.0001,(name,dims)
  assert max(abs(dims[0]-.0224),abs(dims[2]-.0224))<.0001
  assert abs(lo[1])<1e-5,(name,lo)
  result['standalones'][name]=dict(triangles=tri,bytes=path.stat().st_size,dimensions_m=dims.tolist(),normal_direction=normal,
   outer_rim_sides=sides,minimum_outer_hull_radial_normal_alignment=float(min(alignment)),fresh_import=True)
 Path(a.out).write_text(json.dumps(result,indent=2));print('VERIFIED',triangles,len(rows),'affine and semantic samples; named imported contacts; standalone fresh imports')
if __name__=='__main__':main()
