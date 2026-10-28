"""Checkpoint geometry, support, half-frame intended state and clearance checks."""
import argparse,json,sys,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from kit import weapon as W,motion,assembly
from contacts import part,measure
from interface import CLIPS
from semantics import check as semantic_check

def form_details():
 trigger=motion.surface(part('Trigger_Shoe'))['points']
 bands={n:[v for v in trigger if a<v.z<b] for n,a,b in [('toe',.007,.013),('middle',.024,.031),('head',.040,.045)]}
 front={n:max(v.y for v in ps) for n,ps in bands.items()}
 assert front['toe']>front['middle']+.004 and front['head']>front['middle']+.002,'reversed trigger concavity'
 drum=motion.surface(part('Sight_RearDrum'))['tree']
 cap=drum.ray_cast(Vector((0,-.005,.18)),Vector((0,0,-1)),.05)
 assert cap[0] is not None and cap[0].z>.150 and cap[1].z>.8,'open drum roof'
 eye=bpy.data.objects['Socket_Eye'].matrix_world.translation
 rear=drum.ray_cast(eye+Vector((.0027,0,0)),Vector((0,1,0)),.12)
 assert rear[0] is not None and .030<rear[3]<.060,'eye relief outside photo estimate'
 supports=[]
 for suffix,head in [('', 'Handguard_Pin_L'),('.001','Handguard_Pin_R')]:
  surround=part('Handguard_PinSurround'+suffix);pin=part(head)
  a=motion.surface(surround);b=motion.surface(pin)
  centers=[(v['lo']+v['hi'])*.5 for v in (a,b)]
  alignment=(centers[0].yz-centers[1].yz).length
  distance,_=assembly.distance(surround,part('Handguard_Mold'))
  assert alignment<.00015 and distance<.00005,('pin surround seating',suffix,alignment,distance)
  supports.append(dict(side=head,axis_alignment_m=alignment,mold_surface_distance_m=distance))
 # Four detents and their intermediate travel, without altering the accepted
 # clip catalog. Work in armature space so imported rest-bone roll is irrelevant.
 ob=part('Sight_RearDrum');arm=ob.parent;W.pose(arm,None,0)
 fixed=[motion.surface(o) for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==arm and o.get('bone')!='RearDrum']
 b=arm.pose.bones['RearDrum'];pivot=b.bone.head_local.copy()
 axis=arm.matrix_world.to_3x3().inverted()@Vector((0,-math.sin(math.radians(16)),math.cos(math.radians(16))))
 maximum=0
 for degrees in range(0,271,15):
  xf=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(degrees),4,axis)@Matrix.Translation(-pivot)
  b.matrix=xf@b.bone.matrix_local;bpy.context.view_layer.update();moving=motion.surface(ob)
  for other in fixed:
   if any(min(moving['hi'][k],other['hi'][k])-max(moving['lo'][k],other['lo'][k])<=.0002 for k in range(3)):continue
   depth,_=motion.penetration(moving,other,.0002);maximum=max(maximum,depth)
   assert depth<=.0002,('drum detent sweep',degrees,depth)
 W.pose(arm,'Idle',0)
 return dict(pin_surround_supports=supports,drum_detent_sweep=dict(samples=19,range_degrees=[0,270],max_penetration_m=maximum),trigger_front_y_m=front,closed_drum_roof_m=list(cap[0]),
             eye_to_near_drum_face_m=rear[3],method='evaluated surface bands and first-hit triangle rays')

def geometry(arm,imported=False):
 W.pose(arm,'Idle',0)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==arm and 'bone' in o]
 counts={o.get('part_name',o.name):len(o.data.polygons) for o in meshes}
 points=[p for o in meshes for p in motion.surface(o)['points']]
 lo=[min(p[k] for p in points) for k in range(3)];hi=[max(p[k] for p in points) for k in range(3)]
 size=[b-a for a,b in zip(lo,hi)];barrel=motion.surface(part('Barrel'));length=barrel['hi'].y-barrel['lo'].y
 assert abs(size[1]-.680)<.0003,size
 assert abs(length-.225)<.00005,length
 assert 30000<=sum(counts.values())<=42000,sum(counts.values())
 manifold={}
 for o in meshes:
  bm=bmesh.new();bm.from_mesh(o.data)
  if imported:bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8)
  bad=sum(not e.is_manifold for e in bm.edges);bm.free()
  if bad:manifold[o.name]=bad
 assert not manifold,manifold
 eye=bpy.data.objects['Socket_Eye'].matrix_world.translation
 stock=motion.surface(part('Stock_Mold'))
 h=stock['tree'].ray_cast(eye,Vector((0,0,-1)),.2);assert h[0] is not None
 height=eye.z-h[0].z;assert .018<height<.05,height
 # First-person cone must clear the stock in its sight corridor, not just one ray.
 # The full 70-degree camera includes a normal foreground comb; the central
 # 7-degree optical corridor must stay open through the rear/front rings.
 obstruction=[]
 for p in stock['points']:
  d=p-eye
  if d.y>0 and abs(d.x)<d.y*.0612 and abs(d.z)<d.y*.0612:obstruction.append(list(p))
 assert not obstruction,'stock obstructs central sight corridor'
 return dict(form_details=form_details(),triangles=sum(counts.values()),per_part=counts,bounds_m=dict(lo=lo,hi=hi,size=size),
  barrel_length_m=length,eye_above_actual_comb_m=height,comb_ray_point_m=list(h[0]),
  central_sight_corridor_degrees=7,nonmanifold=manifold,
  topology_policy='diagnostic weld of GLB normal/UV attribute splits at 1e-8 m' if imported else 'raw unsplit source topology')

def sweep(arm,step=.5):
 allow=[dict(a='ChamberRound',b='Bolt_Face',max_penetration_m=.0001,reason='primer meets visual bolt face'),
  dict(a='Magazine_FeedLip',b='Magazine_TopRound',max_penetration_m=.00015,reason='formed lip retains cartridge'),
  dict(a='Magazine_FeedLip',b='Magazine_SecondRound',max_penetration_m=.00015,reason='formed lip retains staggered cartridge'),
  dict(a='Magazine_Follower',b='Magazine_ThirdRound',max_penetration_m=.00015,reason='follower supports display stack'),
  dict(a='MagazineRelease_Catch',b='Magazine_Body',max_penetration_m=.0002,reason='catch bears against magazine ledge'),
  dict(a='Cocking_Tube',b='Handle_Stem',max_penetration_m=.0002,reason='handle rear land seated against notch')]
 return motion.sweep_clips(arm,list(CLIPS),step_frames=step,tolerance_m=.0002,allow=allow)

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/smg.blend');p.add_argument('--out',default='build/check.json')
 p.add_argument('--motion',action='store_true');p.add_argument('--step',type=float,default=.5)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
 arm=bpy.data.objects['SMGArmature'];result=geometry(arm);result['states']=semantic_check(arm);result['contacts']=measure(arm)
 if a.motion:result['motion']=sweep(arm,a.step)
 result['stage']='unbaked form checkpoint';result['passed']=result.get('motion',{}).get('passed',True)
 Path(a.out).write_text(json.dumps(result,indent=2));print('SMG CHECK',result['triangles'],result['bounds_m']['size'],result['passed'],flush=True)
 assert result['passed'],'Clearance violations: see '+a.out
if __name__=='__main__':main()
