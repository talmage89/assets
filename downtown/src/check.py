"""Raw accessors, fresh import, physical rays, party seams and sampled doors.

Serialization and construction evidence are deliberately reported separately.
UVs are staging charts: finite/nondegenerate checks are not finished trim proof.
"""
import hashlib,json,math,sys
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from kit.gltf import GLB
from kit import motion
from plan import PROOF


def read(path):
 g=object.__new__(GLB);g.json=json.loads(path.read_text());g.binary=(path.parent/g.json['buffers'][0]['uri']).read_bytes();g.parents={c:i for i,n in enumerate(g.json['nodes']) for c in n.get('children',[])};return g

def tree(obs,role):
 vs=[];fs=[]
 for ob in obs:
  ob.data.calc_loop_triangles();offset=len(vs);vs += [ob.matrix_world@v.co for v in ob.data.vertices]
  fs += [tuple(offset+i for i in t.vertices) for t in ob.data.loop_triangles if role in ob.data.materials[t.material_index].name]
 return BVHTree.FromPolygons(vs,fs,all_triangles=True)

def ray(t,point,direction):
 hit=t.ray_cast(Vector(point),Vector(direction),100)
 assert hit[0] is not None,('missing physical surface',point,direction)
 return hit[0]

def audit(lot,row,do_motion=False):
 path=Path(row['source']);g=read(path);doc=g.json;tris=0;points=[];normal=0;uv0=0;zero=0
 assert len(doc['materials'])<=6
 assert len(doc.get('images',[]))==1 and all(im['uri'].startswith('textures/') for im in doc['images'])
 for im in doc['images']:assert (path.parent/im['uri']).exists()
 for i,n in enumerate(doc['nodes']):
  if 'mesh' not in n:continue
  xf=g.world(i);assert max(abs(np.linalg.norm(xf[:3,:3],axis=0)-1))<1e-5
  for p in doc['meshes'][n['mesh']]['primitives']:
   a=p['attributes'];v=g.accessor(a['POSITION']);v=(xf@np.c_[v,np.ones(len(v))].T).T[:,:3];v=v[:,[0,2,1]]*np.array([1,-1,1]);points.extend(v)
   normals=g.accessor(a['NORMAL']);normal=max(normal,float(abs(np.linalg.norm(normals,axis=1)-1).max()));assert np.isfinite(v).all()
   ix=g.accessor(p['indices']).reshape(-1,3);tris+=len(ix);w=v[ix];area=np.linalg.norm(np.cross(w[:,1]-w[:,0],w[:,2]-w[:,0]),axis=1)/2;zero+=int((area<1e-11).sum())
   uv=g.accessor(a['TEXCOORD_0']);assert np.isfinite(uv).all();t=uv[ix];du=t[:,1]-t[:,0];dv=t[:,2]-t[:,0];ua=abs(du[:,0]*dv[:,1]-du[:,1]*dv[:,0])/2;uv0+=int((ua<1e-13).sum())
 assert tris==row['triangles'] and tris<=row['budget'] and normal<1e-4 and zero==0 and uv0==0,(lot['id'],tris,normal,zero,uv0)
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
 obs=[o for o in bpy.context.scene.objects if o.type=='MESH'];fresh=[o.matrix_world@v.co for o in obs for v in o.data.vertices]
 kd=KDTree(len(fresh))
 for i,p in enumerate(fresh):kd.insert(p,i)
 kd.balance();err=max(kd.find(p)[2] for p in points);assert err<2e-5
 glass=tree(obs,'Glass');masonry=tree(obs,'Masonry');roof=tree(obs,'Roof');w,d=lot['width'],lot['depth'];front=-d/2
 # The aperture and its glass plane are measured independently of serialization.
 socket=bpy.data.objects[lot['id']+'__Socket_StoreDoorThreshold'].matrix_world.translation
 hit=ray(glass,(socket.x,front-2,1.4),(0,1,0));recess=hit.y-front
 assert .98<recess<1.12,(lot['id'],'door recess',recess)
 wallhit=ray(masonry,(-w/2+lot['chamfer']+.12,front-1,lot['floor_first']+.20),(0,1,0));front_error=abs(wallhit.y-front);assert front_error<1e-4
 roofhit=ray(roof,(0,0,lot['height']+5),(0,0,-1));expected=lot['roof']-.03+.008*d/2;assert abs(roofhit.z-expected)<.001
 # Actual rear scupper must be open through masonry AND membrane upstand.
 scupper=Vector((-w/2+.38,d/2+.05,lot['roof']+.04))
 for field in (masonry,roof):
  h=field.ray_cast(scupper,Vector((0,-1,0)),.45);assert h[0] is None,('blocked scupper',lot['id'])
 corner_floor=None
 if lot['corner']:
  mineral=tree(obs,'Mineral');pt=bpy.data.objects[lot['id']+'__Socket_CornerDoorThreshold'].matrix_world.translation
  floorhit=ray(mineral,(pt.x,pt.y,.10),(0,0,-1));corner_floor=float(floorhit.z);assert abs(corner_floor)<1e-5
 stairs=None
 if lot['fire_escape']:
  steel=tree(obs,'Finish');span=min(5.60,w-.55);left=w/2-span/2;right=w/2+span/2;ax=left+.95;bx=right-.95
  levels=[lot['floor_first']+i*lot['upper']+.02 for i in range(lot['stories']-1)]
  def rear_point(x,y,z):return Vector((w/2-x,d/2-y,z))
  feet=[]
  for side in (-.44,.44):
   pt=rear_point(bx,-1.88+side,0);near=steel.find_nearest(pt);feet.append(near[3]);assert near[3]<1e-5
  headrooms=[]
  for level,z in enumerate(levels[:-1]):
   low=levels[level-1] if level else .18;steps=math.ceil((z-low)/.185)
   for j in range(2,steps-1):
    t=j/steps;zz=z+(low-z)*t+.0175;pt=rear_point(ax+(bx-ax)*t,-1.88,zz+.05)
    hit=steel.ray_cast(pt,Vector((0,0,1)),20)
    if hit[0] is not None:headrooms.append(hit[3]+.05)
  if headrooms:assert min(headrooms)>2.0,('fire-escape headroom',lot['id'],min(headrooms))
  stairs=dict(foot_surface_max_distance_to_grade_m=max(feet),sampled_vertical_headroom_min_m=min(headrooms) if headrooms else None,headroom_samples=len(headrooms),scope='Independent rays on actual exported steel; no structural load certification')
 pivots=[]
 for o in bpy.context.scene.objects:
  if o.get('pivot_axis'):
   assert list(o.get('range_degrees'))==[0,100];pivots.append(o)
 sweep=None
 if do_motion:
  specs=[dict(node=o.name,axis='Z',range=[0,100],step=5,tolerance_m=.001) for o in pivots]
  sweep=motion.sweep(dict(MOTIONS=specs))
  Path('build/motion').mkdir(exist_ok=True);Path('build/motion/'+lot['id']+'.json').write_text(json.dumps(sweep,indent=2)+'\n')
  assert sweep['passed'],(lot['id'],'door sweep failed')
 return dict(id=lot['id'],passed=True,triangles=tris,materials=len(doc['materials']),gltf_bytes=path.stat().st_size,bin_bytes=len(g.binary),
  normal_length_error=normal,zero_area_triangles=zero,zero_area_uvs=uv0,reimport_error_m=err,
  construction=dict(measured_door_recess_m=recess,front_plane_error_m=front_error,measured_roof_center_z_m=roofhit.z),
  corner_lobby_floor_z_m=corner_floor,stairs=stairs,motion=sweep,sha256=hashlib.sha256(path.read_bytes()+g.binary).hexdigest())

def main():
 rows=[];blocks=[]
 for seed,region in PROOF:
  meta=json.loads((Path('build/blocks')/region/'block.json').read_text())
  for lot,row in zip(meta['lots'],meta['buildings']):rows.append(audit(lot,row,do_motion=True))
  source=Path('build/blocks')/region/'block.glb';bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()));bpy.context.view_layer.update();gaps=[]
  for a,b in zip(meta['lots'],meta['lots'][1:]):
   aa=bpy.data.objects[a['id']+'__Socket_PartyRight'].matrix_world.translation;bb=bpy.data.objects[b['id']+'__Socket_PartyLeft'].matrix_world.translation
   # Party lines share X; depths vary so midpoint Y intentionally differs.
   gaps.append(abs(aa.x-bb.x))
  assert max(gaps)<2e-5
  blocks.append(dict(region=region,triangles=sum(r['triangles'] for r in meta['buildings']),party_line_max_gap_m=max(gaps),glb_bytes=source.stat().st_size))
 report=dict(passed=True,stage='form checkpoint; no baked material or final UV claims',buildings=rows,blocks=blocks,
   scopes=dict(raw='Serialization, triangles, normals, staging UVs and canonical image URI',imported='Raw-to-imported surface preservation',physical='Rays on imported doors, masonry and roof; imported party line sockets',motion='All imported leaves, 5 degree sampled sweep against actual triangles'))
 Path('build/check.json').write_text(json.dumps(report,indent=2)+'\n');print('CHECK PASS',len(rows),'buildings',blocks,flush=True)
if __name__=='__main__':main()
