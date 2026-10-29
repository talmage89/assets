"""Source/import visual construction, explicit states and sampled clearance.

Mechanical proxies are checked for visible fit only. This does not certify
fire-control engagement, a pressure-bearing lock or firearm function.
"""
import argparse,json,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,motion,assembly
from interface import CLIPS,transition,interrupt
import interface
from guns.common.interface_v1_6 import manifest
from visual_contacts import audit as visual_audit
def part(n):return next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_name',o.name)==n)
def meshes(arm):return [o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==arm and 'bone' in o]
def geometry(arm,imported=False):
 W.pose(arm,'Idle',0);objects=meshes(arm);manifold={};counts={}
 for o in objects:
  counts[o.get('part_name',o.name)]=sum(len(f.vertices)-2 for f in o.data.polygons)
  bm=bmesh.new();bm.from_mesh(o.data)
  if imported:bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8)
  bad=sum(not e.is_manifold for e in bm.edges);bm.free()
  if bad:manifold[o.name]=bad
 points=[p for o in objects if o['bone']!='EjectedCase' for p in motion.surface(o)['points']]
 lo=[min(v[k] for v in points) for k in range(3)];hi=[max(v[k] for v in points) for k in range(3)]
 barrel=motion.surface(part('Barrel'));eye=bpy.data.objects['Socket_Eye'].matrix_world.translation
 comb=motion.surface(part('Stock_Sculpt'))['tree'].ray_cast(eye,Vector((0,0,-1)),.2)
 sheet=motion.surface(part('Receiver_Sheet'))['tree']
 inside=sheet.ray_cast(Vector((0,.005,.070)),Vector((1,0,0)),.03)
 outside=sheet.ray_cast(Vector((.030,.005,.070)),Vector((-1,0,0)),.03)
 gauge=(outside[0]-inside[0]).length;assert .0009<gauge<.0011
 return dict(triangles=sum(counts.values()),parts=counts,bounds_m=dict(lo=lo,hi=hi,size=[b-a for a,b in zip(lo,hi)]),
  barrel_length_m=barrel['hi'].y-barrel['lo'].y,eye_above_comb_m=eye.z-comb[0].z if comb[0] else None,
  measured_receiver_wall_m=gauge,nonmanifold=manifold)
def contacts(arm):
 rows=[]
 def contact(a,b,limit,kind,clip='Idle',frame=0):
  W.pose(arm,clip,frame);d,method=assembly.distance(part(a),part(b))
  rows.append(dict(kind=kind,parts=[a,b],clip=clip,frame=frame,distance_m=d,limit_m=limit,method=method,passed=d<=limit))
 for side,roundname in [(1,'TopRound'),(-1,'SecondRound')]:
  contact('Magazine_FeedLip'+str(side),'Magazine_'+roundname+'_Case',.0004,'visual lip-to-case support')
  W.pose(arm,'Idle',0)
  x=side*.00865;z=.070 if side>0 else .0644
  origin=Vector((x,.120,z+.015));direction=Vector((0,0,-1))
  lip=motion.surface(part('Magazine_FeedLip'+str(side)))['tree'].ray_cast(origin,direction,.025)
  case=motion.surface(part('Magazine_'+roundname+'_Case'))['tree'].ray_cast(origin,direction,.025)
  gap=lip[0].z-case[0].z if lip[0] is not None and case[0] is not None else None
  rows.append(dict(kind='cartridge lies beneath overhanging formed lip',side=side,
   lip_point_m=list(lip[0]) if lip[0] is not None else None,
   cartridge_point_m=list(case[0]) if case[0] is not None else None,
   vertical_outer_surface_gap_m=gap,passed=gap is not None and -.0002<=gap<=.001))
 contact('Magazine_RearCatch','MagRelease_VisualCatch',.0003,'rear magazine display catch seated')
 contact('ChargingHandle','Carrier_PortCheek',.0003,'integral visual handle seated on carrier')
 contact('Stock_Sculpt','Rear_Insert',.001,'stock neck seated in rear receiver')
 for end in ('Rear','Front'):
  contact('Guard_'+end+'Flange','Receiver_Sheet',.0001,'stamped guard flange seated on folded receiver')
 W.pose(arm,'Idle',0);eye=bpy.data.objects['Socket_Eye'].matrix_world.translation;hits=[]
 # The center ray grazes the top of the post; lower it 0.1 mm to avoid an
 # undefined exact-edge hit, retaining its direction and the documented Eye.
 for o in meshes(arm):
  if o['bone']=='EjectedCase':continue
  h=motion.surface(o)['tree'].ray_cast(eye+Vector((0,0,-.0001)),Vector((0,1,0)),1)
  if h[0] is not None:hits.append((h[3],o.get('part_name',o.name)))
 rows.append(dict(kind='Eye parallel ray first visible hit is centered post',hits=sorted(hits)[:8],passed=bool(hits) and min(hits)[1]=='Sight_FrontPost'))
 rear=motion.surface(part('Sight_RearNotch'))['tree'].ray_cast(eye+Vector((.004,0,-.0003)),Vector((0,1,0)),.4)
 rows.append(dict(kind='Eye to actual rear-notch shoulder',distance_m=rear[3] if rear[0] else None,
  passed=bool(rear[0]) and .270<rear[3]<.330))
 return rows+visual_audit(arm,part,meshes)
def semantics(arm):
 rows=[]
 # Independent expected state assertions at intermediate frames. Compare
 # deformation matrices, which survive imported rest-bone conversion.
 def delta(n):
  b=arm.pose.bones[n];return b.matrix@b.bone.matrix_local.inverted()
 for clip,s in CLIPS.items():
  for i in range(s['frames']*2+1):
   f=i*.5;W.pose(arm,clip,f)
   assert max(abs(delta('Root')[i][j]-(i==j)) for i in range(4) for j in range(4))<1e-5
   # Both fixed-to-carrier visual owners must follow the parent's full frame.
   d=(delta('ChargingHandle').translation-delta('BoltCarrier').translation).length
   assert d<2e-5,(clip,f,'nonreciprocating handle',d)
   for n in ('TopRound','SecondRound','ThirdRound','ChamberRound','EjectedCase'):
    scale=delta(n).to_scale()
    assert all(math.isfinite(v) for v in scale)
    assert all(min(abs(v),abs(v-1))<1e-5 for v in scale),(clip,f,n,scale)
   for n in ('TopRound','SecondRound','ThirdRound'):
    d=delta(n)
    if d.to_scale().length>1:
     relative=delta('Magazine').inverted()@d
     assert max(abs(relative[i][j]-(i==j)) for i in range(4) for j in range(4))<1e-5,(clip,f,n,'round moved relative to its feed lips')
   rows.append((clip,f))
 for clip,f in [('FireLast',12),('Charge',60),('IdleEmpty',30)]:
  W.pose(arm,clip,f);assert delta('BoltCarrier').translation.length<1e-5
  assert delta('ChamberRound').to_scale().length<1e-5
 for f in (112,113,114):
  W.pose(arm,'Reload',f);socket=bpy.data.objects['Socket_Magazine'].matrix_world.translation
  assert (socket-Vector((0,.166,.067))).length<2e-5,'front-hook pivot drifts while rocking'
 for clip,f in [('Fire',1.5),('Fire',7.5),('ReloadEmpty',71.5),('ReloadEmpty',72.5)]:
  W.pose(arm,clip,f)
  n='ChamberRound' if clip=='Fire' else 'TopRound';expected=1 if f in (1.5,72.5) else 0
  assert abs(delta(n).to_scale().x-expected)<1e-5,(clip,f,n)
 state='last_ready'
 for c in ('FireLast','ReloadEmpty','Idle'):state=transition(state,c)
 assert state=='ready'
 resumes=[interrupt(c,f) for c in ('Reload','ReloadEmpty') for f in (39.5,56,113.5,137)]
 W.pose(arm,'Idle',0)
 return dict(samples=len(rows),last_round_chain='FireLast → ReloadEmpty → Idle',resume_checks=len(resumes))
def sweep(arm,step=.5):
 # Only bounded bearing/visual occupancy overlaps may be allowed. All are
 # still measured; no unbounded prefix skip is accepted in this asset.
 allow=[dict(a='Receiver_Sheet',b='Trigger_VisualPin',max_penetration_m=.001,
  reason='solid visual pin crosses its sheet bearing; no functional bearing model'),
  dict(a='Carrier_PortCheek',b='ChargingHandle',max_penetration_m=.0015,
  reason='carrier-fixed forged handle root; identical relative deformation throughout'),
  dict(a='MagRelease_Paddle',b='MagRelease_VisualCatch',max_penetration_m=.0021,
  reason='simplified inert catch/link bearing; no operational linkage certification'),
  dict(a='MagRelease_Axle',b='MagRelease_VisualCatch',max_penetration_m=.0021,
  reason='solid visual catch traverses its simplified bearing during hand motion')]
 return motion.sweep_clips(arm,list(CLIPS),step_frames=step,tolerance_m=.0002,allow=allow)
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/ak.blend');p.add_argument('--out',default='build/check.json')
 p.add_argument('--motion',action='store_true');p.add_argument('--step',type=float,default=.5);p.add_argument('--diagnostic',action='store_true')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);path=Path(a.source).resolve()
 if path.suffix=='.glb':
  from kit.weapon_verify import import_glb
  arm=import_glb(path)
 else:
  bpy.ops.wm.open_mainfile(filepath=str(path));arm=bpy.data.objects['R39Armature']
 report=dict(scope='nonfunctional visual assembly; no lock/sear or manufacturing certification',
  contract=manifest(interface),geometry=geometry(arm,path.suffix=='.glb'),contacts=contacts(arm),semantics=semantics(arm))
 if a.motion:report['motion']=sweep(arm,a.step)
 g=report['geometry'];report['passed']=not g['nonmanifold'] and 30000<=g['triangles']<=40000 and all(r['passed'] for r in report['contacts']) and report.get('motion',{}).get('passed',True)
 assert abs(g['bounds_m']['size'][1]-.880)<.002,'Exterior envelope misses original design range'
 assert abs(g['barrel_length_m']-.415)<.00001,'Barrel visual envelope'
 assert .030<g['eye_above_comb_m']<.055,'Eye does not match the estimated comb range'
 Path(a.out).write_text(json.dumps(report,indent=2));print('CHECK',report['passed'],g['triangles'],'triangles',flush=True)
 if not a.diagnostic:assert report['passed'],'See '+a.out
if __name__=='__main__':main()
