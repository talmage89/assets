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

def tree(obs,role,mineral_below=None):
 vs=[];fs=[]
 for ob in obs:
  ob.data.calc_loop_triangles();offset=len(vs);vs += [ob.matrix_world@v.co for v in ob.data.vertices]
  fs += [tuple(offset+i for i in t.vertices) for t in ob.data.loop_triangles if role in ob.data.materials[t.material_index].name or (role=='Masonry' and mineral_below is not None and 'MineralRoof' in ob.data.materials[t.material_index].name and max(vs[offset+i].z for i in t.vertices)<=mineral_below+1e-5)]
 return BVHTree.FromPolygons(vs,fs,all_triangles=True)

def ray(t,point,direction):
 hit=t.ray_cast(Vector(point),Vector(direction),100)
 assert hit[0] is not None,('missing physical surface',point,direction)
 return hit[0]

def winding(triangles,point):
 # Jacobson/Kavan/Sorkine-Hornung 2013, oriented solid-angle sum. Coplanar
 # internal faces cancel; air in an assembled storefront is not a solid.
 a,b,c=(triangles-np.asarray(point,dtype=float)).transpose(1,0,2)
 la=np.linalg.norm(a,axis=1);lb=np.linalg.norm(b,axis=1);lc=np.linalg.norm(c,axis=1)
 numerator=np.einsum('ij,ij->i',a,np.cross(b,c))
 denominator=la*lb*lc+np.einsum('ij,ij->i',a,b)*lc+np.einsum('ij,ij->i',b,c)*la+np.einsum('ij,ij->i',c,a)*lb
 return float(np.arctan2(numerator,denominator).sum()/(2*math.pi))


def membership_fixtures():
 def cube(cx):
  v=np.asarray([(cx+x,y,z) for x,y,z in ((-.5,-.5,-.5),(.5,-.5,-.5),(.5,.5,-.5),(-.5,.5,-.5),(-.5,-.5,.5),(.5,-.5,.5),(.5,.5,.5),(-.5,.5,.5))])
  quads=((0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7))
  return v[np.asarray([(f[0],f[1],f[2]) for f in quads]+[(f[0],f[2],f[3]) for f in quads])]
 tests=[]
 for label,tri,p,expected in [('box interior',cube(0),(0,0,0),1),('box exterior',cube(0),(0,.7,0),0),('abutting boxes',np.concatenate((cube(0),cube(1))),(.49,0,0),1),('overlapping members',np.concatenate((cube(0),cube(.3))),(.2,0,0),2)]:
  actual=winding(tri,p);assert abs(actual-expected)<1e-8,(label,actual);tests.append(dict(case=label,winding=actual,expected=expected))
 # A hollow architectural frame must leave its room air clear, while a
 # leaf fully contained in an actual member must still fail the audit.
 def surface(tri):
  points=[Vector(v) for v in tri.reshape(-1,3)];faces=[tuple(range(i,i+3)) for i in range(0,len(points),3)]
  return dict(tree=BVHTree.FromPolygons(points,faces,all_triangles=True),points=points,faces=faces,lo=Vector(tri.min(axis=(0,1))),hi=Vector(tri.max(axis=(0,1))))
 frame=np.concatenate([cube(0)*scale+center for scale,center in [((.2,2,2),(-.9,0,0)),((.2,2,2),(.9,0,0)),((1.6,.2,2),(0,-.9,0)),((1.6,.2,2),(0,.9,0))]])
 fixed=surface(frame);membership=AssemblyMembership(None);membership.triangles[fixed['tree']]=frame;old=motion.inside;motion.inside=membership.inside
 try:
  for label,tri,collides in [('hollow frame air',cube(0)*.08,False),('fully contained leaf',cube(0)*.08+(.9,0,0),True)]:
   moving=surface(tri);membership.triangles[moving['tree']]=tri;depth,_=motion.penetration(moving,fixed,.001)
   assert (depth>.001)==collides,(label,depth);tests.append(dict(case=label,penetration_m=depth,expected_collision=collides))
 finally:motion.inside=old
 return tests


class AssemblyMembership:
 # The kit's three-ray parity can count a shared internal face only once in
 # abutting closed building members. Use actual oriented triangles instead.
 # BVH crossings, edge intervals, nearest distances and tolerance stay stock.
 def __init__(self,surface):self.original=surface;self.triangles={};self.queries=0
 def surface(self,ob):
  s=self.original(ob);self.triangles[s['tree']]=np.asarray(s['points'],dtype=float)[np.asarray(s['faces'])];return s
 def inside(self,tree,point):
  self.queries+=1;return winding(self.triangles[tree],point)>.5


def audit(lot,row,do_motion=False):
 path=Path(row['source']);g=read(path);doc=g.json;tris=0;points=[];normal=0;uv0=0;zero=0
 assert len(doc['materials'])<=6
 assert 10<=len(doc.get('images',[]))<=11 and all(im['uri'].startswith('textures/') for im in doc['images'])
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
 glass=tree(obs,'Glass');masonry=tree(obs,'Masonry',lot['floor_first']-.08 if lot['corner'] else None);roof=tree(obs,'Roof');w,d=lot['width'],lot['depth'];front=-d/2
 # The aperture and its glass plane are measured independently of serialization.
 socket=bpy.data.objects[lot['id']+'__Socket_StoreDoorThreshold'].matrix_world.translation
 hit=ray(glass,(socket.x,front-2,1.4),(0,1,0));recess=hit.y-front
 assert .98<recess<1.12,(lot['id'],'door recess',recess)
 wallhit=ray(masonry,(-w/2+lot['chamfer']+.12,front-1,lot['floor_first']+.20),(0,1,0));front_error=abs(wallhit.y-front);assert front_error<1e-4
 left_hit=ray(masonry,(-w/2-1,0,2),(1,0,0));right_hit=ray(masonry,(w/2+1,0,2),(-1,0,0))
 measured_width=right_hit.x-left_hit.x
 probe_x=-w/2+(lot['chamfer'] if lot['corner']=='left' else 0)+(w-lot['chamfer'])*.25
 fh=ray(masonry,(probe_x,front-1,lot['floor_first']+.20),(0,1,0))
 rh=ray(masonry,(0,d/2+1,lot['floor_first']+.20),(0,-1,0))
 measured_depth=rh.y-fh.y;inner=ray(masonry,fh+Vector((0,.00001,0)),(0,1,0));front_gauge=inner.y-fh.y
 assert abs(measured_width-w)<.0001 and abs(measured_depth-d)<.0001 and abs(front_gauge-.44)<.0001,(lot['id'],measured_width,w,measured_depth,d,front_gauge)
 roofhit=ray(roof,(0,0,lot['height']+5),(0,0,-1));expected=lot['roof']-.03+.008*d/2;assert abs(roofhit.z-expected)<.001
 finish=tree(obs,'Finish');sx=-w*.20;sy=-d*.15;base_gaps=[];pane_gaps=[]
 cast_projection=None
 if lot['storefront']=='iron':
  # A decorated front can still hide its entire shaft behind the masonry.
  # Measure the casting at mid-height, clear of the base, sign and capital.
  shaft=ray(finish,(w/2-.17,front-1,(lot['floor_first']-1.42)*.5),(0,1,0))
  cast_projection=front-shaft.y
  assert .14<cast_projection<.22,('cast shaft buried in masonry',lot['id'],cast_projection)
 for xx in (sx-.65,sx+.65):
  for yy in (sy-.8,sy,sy+.8):
   membrane=ray(roof,(xx,yy,lot['height']+2),(0,0,-1))
   base=ray(finish,(xx,yy,membrane.z-.1),(0,0,1));base_gaps.append(base.z-membrane.z)
   pane=ray(glass,(xx,yy,membrane.z+.1),(0,0,1))
   rail=ray(finish,(xx,yy,pane.z+.1),(0,0,-1));pane_gaps.append(pane.z-rail.z)
 assert max(base_gaps)<.001 and min(base_gaps)>-.04 and max(abs(v) for v in pane_gaps)<1e-5,('skylight support',lot['id'],base_gaps,pane_gaps)
 gallery_feet=[]
 if lot['gallery']:
  for xx in (-w/2+.38,0,w/2-.38):
   near=finish.find_nearest(Vector((xx,front-2.55,0)));gallery_feet.append(near[3]);assert near[3]<1e-5,('gallery foot above grade',lot['id'],near[3])
 roof_details=dict(skylight_curb_base_gap_range_m=[min(base_gaps),max(base_gaps)],skylight_pane_to_rail_max_gap_m=max(abs(v) for v in pane_gaps),gallery_foot_max_distance_to_grade_m=max(gallery_feet) if gallery_feet else None,scope='Independent rays on exported roof membrane, curb rails and glazing; negative base gap is flashing overlap')
 # Actual rear scupper must be open through masonry AND membrane upstand.
 scupper=Vector((-w/2+.38,d/2+.05,lot['roof']+.04))
 for field in (masonry,roof):
  h=field.ray_cast(scupper,Vector((0,-1,0)),.45);assert h[0] is None,('blocked scupper',lot['id'])
 corner_floor=None;entry_steps=None;chamfer=None
 if lot['corner']:
  mineral=tree(obs,'Mineral');pt=bpy.data.objects[lot['id']+'__Socket_CornerDoorThreshold'].matrix_world.translation
  # This establishes an actual cut plane, independently of the door/socket.
  inward=Vector((1 if lot['corner']=='left' else -1,1,0)).normalized()
  old=Vector((-w/2 if lot['corner']=='left' else w/2,front,lot['floor_first']-.30))
  cut=ray(mineral,old-inward,inward)
  setback=(cut-old).dot(inward)*math.sqrt(2)
  assert 4*.3048<=setback<=6*.3048 and abs(setback-lot['chamfer'])<.0001,('actual corner chamfer',lot['id'],setback)
  # Public return stone is measured below the window apertures and above the
  # water-table molding, so this ray cannot mistake a sill for the facade.
  side_x=-w/2 if lot['corner']=='left' else w/2;sign=1 if lot['corner']=='left' else -1
  stone=ray(mineral,(side_x-sign,front+5.,.46),(sign,0,0))
  assert abs(stone.x-side_x)<1e-5
  chamfer=dict(measured_edge_setback_m=setback,measured_diagonal_normal=list(inward),stone_return_face_error_m=abs(stone.x-side_x),scope='Independent rays on exported diagonal ashlar and public return, not socket or manifest values')
  floorhit=ray(mineral,(pt.x,pt.y,pt.z+.10),(0,0,-1));corner_floor=float(floorhit.z);assert abs(corner_floor-(pt.z-.018))<1e-5
  if lot['tenant']=='bank':
   inward=Vector((1 if lot['corner']=='left' else -1,1,0)).normalized();treads=[]
   for setback in (.48,.17):
    q=pt-inward*(.47+setback);hit=ray(mineral,(q.x,q.y,1),(0,0,-1));treads.append(float(hit.z))
   assert abs(treads[0]-.15)<1e-5 and abs(treads[1]-.30)<1e-5
   entry_steps=dict(tread_z_m=treads,riser_heights_m=[treads[0],treads[1]-treads[0]],landing_z_m=corner_floor,scope='Rays on actual exported treads and lobby; the retail leaf remains at grade')
 stairs=None
 if lot['fire_escape']:
  steel=finish;span=min(5.60,w-.55);left=w/2-span/2;right=w/2+span/2;ax=left+.95;bx=right-.95
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
  specs=[dict(node=o.name,axis='Z',range=[0,100],step=1,tolerance_m=.001) for o in pivots]
  old_surface,old_inside=motion.surface,motion.inside;membership=AssemblyMembership(old_surface)
  motion.surface=membership.surface;motion.inside=membership.inside
  try:sweep=motion.sweep(dict(MOTIONS=specs))
  finally:motion.surface=old_surface;motion.inside=old_inside
  sweep['method']='Kit BVH crossings / edge intervals / nearest distances; oriented-solid-angle membership for assembled building members'
  sweep['solid_angle_queries']=membership.queries
  Path('build/motion').mkdir(exist_ok=True);Path('build/motion/'+lot['id']+'.json').write_text(json.dumps(sweep,indent=2)+'\n')
  assert sweep['passed'],(lot['id'],'door sweep failed')
 return dict(id=lot['id'],passed=True,triangles=tris,materials=len(doc['materials']),gltf_bytes=path.stat().st_size,bin_bytes=len(g.binary),
  normal_length_error=normal,zero_area_triangles=zero,zero_area_uvs=uv0,reimport_error_m=err,
  construction=dict(measured_masonry_width_m=measured_width,measured_masonry_depth_m=measured_depth,measured_front_gauge_m=front_gauge,measured_door_recess_m=recess,front_plane_error_m=front_error,measured_roof_center_z_m=roofhit.z),
  corner_lobby_floor_z_m=corner_floor,corner_entry_steps=entry_steps,corner_chamfer=chamfer,cast_shaft_projection_m=cast_projection,roof_details=roof_details,stairs=stairs,motion=sweep,sha256=hashlib.sha256(path.read_bytes()+g.binary).hexdigest())

def main():
 rows=[];blocks=[];fixtures=membership_fixtures()
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
 report=dict(passed=True,stage='shared baked PBR; raw accessors and actual imported construction',buildings=rows,blocks=blocks,membership_fixtures=fixtures,
   scopes=dict(raw='Serialization, triangles, normals, staging UVs and canonical image URI',imported='Raw-to-imported surface preservation',physical='Rays on imported doors, masonry and roof; imported party line sockets',motion='All imported leaves, 1 degree sampled sweep against actual triangles'))
 Path('build/check.json').write_text(json.dumps(report,indent=2)+'\n');print('CHECK PASS',len(rows),'buildings',blocks,flush=True)
if __name__=='__main__':main()
