"""Independent dimension/contact/clearance audit of the source game form."""
import argparse,json,sys,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,motion
from contacts import measure
from interface import CLIPS
from optical import passage
from trigger_check import measure as trigger_measure

def main():
 p=argparse.ArgumentParser();p.add_argument('--motion',action='store_true');p.add_argument('--source',default='build/bolt.blend');p.add_argument('--out',default='build/check.json');p.add_argument('--dense',action='store_true')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
 arm=bpy.data.objects['B24Armature'];W.pose(arm,None,0);parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o]
 counts={o.name:sum(len(f.vertices)-2 for f in o.data.polygons) for o in parts};bad={}
 for o in parts:
  bm=bmesh.new();bm.from_mesh(o.data);n=sum(not e.is_manifold for e in bm.edges);bm.free()
  if n and not o.get('allow_boundary'):bad[o.name]=n
 points=[v.co for o in parts for v in o.data.vertices]
 lo=[min(v[i] for v in points) for i in range(3)];hi=[max(v[i] for v in points) for i in range(3)]
 barrel=motion.surface(bpy.data.objects['Barrel']);trigger=motion.surface(bpy.data.objects['Trigger_Shoe'])
 pad=motion.surface(bpy.data.objects['Recoil_Pad']);lop=trigger['hi'].y-pad['lo'].y
 # Measure the trigger face at finger height, instead of using the shoe bounds.
 hit=trigger['tree'].ray_cast(Vector((0,.06,.01)),Vector((0,-1,0)),.1)[0]
 if hit:lop=hit.y-pad['lo'].y
 result=dict(stage='form checkpoint; no UV/bake claim',triangles=sum(counts.values()),parts=counts,
  bounds_m=dict(low=lo,high=hi,size=[b-a for a,b in zip(lo,hi)]),barrel_length_m=barrel['hi'].y-barrel['lo'].y,
  length_of_pull_m=lop,materials=len({m.name for o in parts for m in o.data.materials}),nonmanifold=bad,
  contacts=measure(arm),bones=list(arm.data.bones.keys()),clips=list(CLIPS))
 result['trigger_blade']=trigger_measure(arm)
 # An actual sight ray must meet coated ocular glass before any stock/action.
 eye=bpy.data.objects['Socket_Eye'].matrix_world.translation;hits=[]
 for o in parts:
  if o.get('allow_boundary'):continue
  hitrow=motion.surface(o)['tree'].ray_cast(eye,Vector((0,1,0)),.5)
  if hitrow[0] is not None:hits.append((hitrow[3],o.name))
 hits.sort();assert hits[0][1]=='Lens_Ocular',hits[:5]
 stock=motion.surface(bpy.data.objects['Stock_Mold'])['tree']
 cheek=stock.ray_cast(eye,Vector((0,0,-1)),.2)[0];assert cheek is not None
 result['aimed_clearance']=dict(first_surface=hits[0][1],ocular_distance_m=hits[0][0],
    eye_above_comb_m=eye.z-cheek.z,comb_surface_m=list(cheek))
 # A sight ray meeting glass first is insufficient: the structural tube and
 # turret saddle must also leave the path to the objective open. Ignore only
 # the two optical proxies and the intentionally opaque etched pattern.
 result['optical_passage']=passage(parts,eye)
 scope=motion.surface(bpy.data.objects['Scope_Body'])
 left=scope['tree'].ray_cast(Vector((-.04,0,.113)),Vector((1,0,0)),.1)[0]
 right=scope['tree'].ray_cast(Vector((.04,0,.113)),Vector((-1,0,0)),.1)[0]
 result['scope_measured']=dict(length_m=scope['hi'].y-scope['lo'].y,tube_diameter_m=right.x-left.x)
 # Independent external shape measurements; none of these is a copied parameter.
 def diameter_at_y(ob,y,z=.065):
  tree=motion.surface(ob)['tree']
  left=tree.ray_cast(Vector((-.05,y,z)),Vector((1,0,0)),.1)[0]
  right=tree.ray_cast(Vector((.05,y,z)),Vector((-1,0,0)),.1)[0]
  assert left is not None and right is not None
  return right.x-left.x
 result['barrel_contour_m']={label:diameter_at_y(bpy.data.objects['Barrel'],y)
                           for label,y in [('shank',.24),('muzzle_before_crown',.818)]}
 tree=motion.surface(bpy.data.objects['Receiver'])['tree'];origin=Vector((.014,.136,.065))
 ends=[tree.ray_cast(origin,Vector((0,s,0)),.15)[0] for s in (-1,1)]
 assert all(v is not None for v in ends)
 result['ejection_port_length_m']=ends[1].y-ends[0].y
 pad=motion.surface(bpy.data.objects['Recoil_Pad'])
 result['pad_height_m']=pad['hi'].z-pad['lo'].z
 stud=motion.surface(bpy.data.objects['Sling_Stud'])
 under=stock.ray_cast(Vector((0,-.255,-.1)),Vector((0,0,1)),.15)[0]
 assert under is not None
 exposed=under.z-stud['lo'].z;assert .004<exposed<.010,exposed
 result['rear_sling_stud_exposed_m']=exposed
 result['bipod_diameters_m']={name:motion.surface(bpy.data.objects[name])['hi'].x-motion.surface(bpy.data.objects[name])['lo'].x
                            for name in ('Bipod_Sleeve','Bipod_Extension','Bipod_Foot')}
 stock_surface=motion.surface(bpy.data.objects['Stock_Mold'])
 gap=[]
 for y in (.26,.32,.40):
  candidates=[]
  for face in stock_surface['faces']:
   vs=[stock_surface['points'][i] for i in face];hits=[]
   for va,vb in zip(vs,vs[1:]+vs[:1]):
    if (va.y-y)*(vb.y-y)<0:hits.append(va+(vb-va)*((y-va.y)/(vb.y-va.y)))
   if len(hits)==2:
    va,vb=hits;delta=vb-va
    t=max(0,min(1,(-va.x*delta.x+(.065-va.z)*delta.z)/max(1e-18,delta.x**2+delta.z**2)))
    for v in [va,vb,va+delta*t]:
     if (v.x*v.x+(v.z-.065)**2)**.5<.023:candidates.append(v)
  assert candidates
  radius=diameter_at_y(bpy.data.objects['Barrel'],y)/2
  clearance=min((v.x*v.x+(v.z-.065)**2)**.5-radius for v in candidates)
  assert clearance>.0008,(y,clearance)
  gap.append(dict(station_m=y,minimum_sampled_radial_clearance_m=clearance))
 result['barrel_float_samples']=gap
 W.pose(arm,'Fire',0);bolt0=motion.surface(bpy.data.objects['Bolt_Body'])['hi'].y
 W.pose(arm,'Fire',70);bolt1=motion.surface(bpy.data.objects['Bolt_Body'])['hi'].y
 result['bolt_measured_stroke_m']=bolt0-bolt1
 W.pose(arm,'BipodDeploy',78)
 axis=(arm.pose.bones['BipodSplayL'].matrix.to_3x3()@Vector((0,1,0))).normalized()
 intervals=[]
 for name in ('Bipod_Sleeve','Bipod_Extension'):
  ps=motion.surface(bpy.data.objects[name])['points'];values=[v.dot(axis) for v in ps]
  intervals.append((min(values),max(values)))
 overlap=min(v[1] for v in intervals)-max(v[0] for v in intervals)
 assert overlap>.02,overlap
 result['bipod_extended_rod_overlap_m']=overlap
 W.pose(arm,None,0)
 errors=[]
 if not a.dense and not 40000<=result['triangles']<=50000:errors.append('triangle budget')
 if abs(result['barrel_length_m']-.6096)>.00005:errors.append('barrel length')
 if abs((hi[1]-lo[1])-1.1296)>.0001:errors.append('overall length')
 if not .339<=lop<=.350:errors.append('pull length')
 if bad:errors.append('nonmanifold solids')
 if not all(r['passed'] for r in result['contacts']):errors.append('required contacts')
 if a.motion:
  # Intentional visual joint overlaps are still measured, with finite bounds.
  allow=[dict(a='ChamberRound',b='Barrel',reason='visual chamber surrounds case',max_penetration_m=.0003),
         dict(a='Trigger_Shoe',b='Trigger_Pin',reason='solid visual pin inside trigger bearing',max_penetration_m=.0019),
         dict(a='Safety_PivotPin',b='Safety_Stem',reason='visual pin seats in safety bearing',max_penetration_m=.0014),
         dict(a='Bipod_ReturnSpring',b='Bipod_SpringTail',reason='connected return coil/tail at visual splay joint; spring deformation not simulated',max_penetration_m=.00075)]
  result['motion']=motion.sweep_clips(arm,list(CLIPS),step_frames=.5,tolerance_m=.0002,allow=allow)
  if not result['motion']['passed']:errors.append('motion clearance')
 result.update(passed=not errors,errors=errors)
 Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ('parts','motion')},indent=2))
 if errors:raise RuntimeError(errors)
if __name__=='__main__':main()
