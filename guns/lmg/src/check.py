"""Checkpoint geometry/state measurements. Serialization is tested separately."""
import argparse,json,sys,math
from pathlib import Path
import bpy,bmesh,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit import weapon as W,weapon_verify as V,assembly,motion
import interface
from belt import COUNT,PITCH,solve

ALLOW=[dict(a='Bipod_Hinge_'+side,b='Bipod_Channel_'+side,reason='Finite visual splay shoe seating in hinge sleeve',max_penetration_m=.0004) for side in ('L','R')]

def meshes(arm):return [o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==arm and not o.get('bake_only')]
def bounds(o):
 dg=bpy.context.evaluated_depsgraph_get();e=o.evaluated_get(dg);m=e.to_mesh()
 q=np.array([tuple(e.matrix_world@v.co) for v in m.vertices]);e.to_mesh_clear()
 return q.min(axis=0),q.max(axis=0)
def geometry(arm):
 W.pose(arm,'Idle',0);obs=meshes(arm);n=0;bad=[]
 for o in obs:
  bm=bmesh.new();bm.from_mesh(o.data)
  if any(not e.is_manifold for e in bm.edges):bad.append(o.name)
  bm.free();n+=sum(len(f.vertices)-2 for f in o.data.polygons)
 lo=np.min([bounds(o)[0] for o in obs if not o.name.startswith(('ChamberRound','Ejected'))],axis=0)
 hi=np.max([bounds(o)[1] for o in obs if not o.name.startswith(('ChamberRound','Ejected'))],axis=0)
 return dict(triangles=n,nonmanifold=bad,dimensions_mm=((hi-lo)*1000).tolist(),bounds_mm=[(lo*1000).tolist(),(hi*1000).tolist()])
def semantics(arm):
 rows=[]
 for name,s in interface.CLIPS.items():
  for f in sorted({0,s['frames'],*s['events'].values(),*[i+.5 for i in range(s['frames'])]}):
   W.pose(arm,name,f)
   root=arm.pose.bones['Root'];delta=root.matrix@root.bone.matrix_local.inverted()
   assert max(abs(delta[i][j]-(i==j)) for i in range(4) for j in range(4))<1e-6
   if name in ('Fire','Burst','FireLast'):
    handle=arm.pose.bones['ChargingHandle'];assert handle.location.length<1e-8
  W.pose(arm,name,s['frames'])
  # Explicit intended open/closed result, independent of serialized equality.
  if name=='FireLast' or name=='IdleEmpty':assert abs(arm.pose.bones['Bolt'].location.y)<1e-6
  elif name in ('Idle','Fire','Burst','CeaseFire','ReloadEmpty','Charge'):assert abs(arm.pose.bones['Bolt'].location.y+.08)<1e-6
  rows.append(dict(clip=name,root_identity=True,nonreciprocating_handle=True))
 return rows

def belt_audit(arm):
 rows=[]
 for name in ('Idle','Fire','Burst','FireLast','Reload','ReloadEmpty','BeltEnd'):
  for f in np.arange(0,interface.CLIPS[name]['frames']+.01,.5):
   W.pose(arm,name,float(f));pts=[];axes=[]
   for i in range(COUNT):
    b=arm.pose.bones[f'BeltLink{i:02d}'];p=b.matrix.translation
    if min(abs(v) for v in b.matrix.to_scale())>.001:
     pts.append(p);axes.append((b.matrix.to_3x3()@Vector((0,1,0))).normalized())
   errors=[abs((b-a).length-PITCH*.001) for a,b in zip(pts,pts[1:])]
   axis=max([abs(a.dot(Vector((0,1,0)))-1) for a in axes] or [0])
   # glTF samples Euler curves at 60 Hz. Half-frame linear interpolation is
   # measured, not confused with exact chord solves at authored integer keys.
   rows.append(dict(clip=name,frame=float(f),visible=len(pts),max_center_spacing_error_mm=max(errors or [0])*1000,axis_error=axis))
 return dict(max_spacing_error_mm=max(r['max_center_spacing_error_mm'] for r in rows),max_axis_error=max(r['axis_error'] for r in rows),samples=rows)

def surface_gap(a,b):
 # The shared contact helper samples vertices/edges. Parallel touching lands
 # can miss those samples after float export when their corners lie outside
 # each other. Add actual triangle centroids, retaining an upper-bound claim.
 gap,method=assembly.distance(a,b)
 if gap<.00001:return gap,method
 from mathutils.bvhtree import BVHTree
 data=[];dg=bpy.context.evaluated_depsgraph_get()
 for o in (a,b):
  ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles()
  vs=[ev.matrix_world@v.co for v in me.vertices];fs=[tuple(t.vertices) for t in me.loop_triangles]
  samples=[(vs[i]+vs[j]+vs[k])/3 for i,j,k in fs]
  data.append((samples,BVHTree.FromPolygons(vs,fs,all_triangles=True)));ev.to_mesh_clear()
 measured=min(tree.find_nearest(point)[3] for samples,tree in [(data[0][0],data[1][1]),(data[1][0],data[0][1])] for point in samples)
 return (measured,'sampled triangle-centroid-to-surface upper bound') if measured<gap else (gap,method)

def contacts(arm):
 rows=[]
 for clip,frame,a,b,limit in [('Idle',0,'Bolt_ReadyWitness','Sear_VisualWitness',.00005),*[('Idle',0,'Sear_VisualWitness','Receiver_InnerGuide_'+str(side),.00005) for side in (-1,1)],('Idle',0,'CoverLatch_Tongue','CoverLatch_Seat',.0003),('Idle',0,'Box_Latch','Box_LatchSeat',.0003),('Idle',0,'Box_Suspension','Box_LatchSeat',.0004),*[('BipodDeploy',84,'Bipod_Detent_'+x,'Bipod_Extension_'+x,.00025) for x in ('L','R')],('Idle',0,'FeedTray_VisualStop','Belt_Round_00',.0003),*[('Idle',0,'FeedPawl_Display_'+str(y),'Belt_Round_01',.0003) for y in (149,182)]]:
  W.pose(arm,clip,frame);gap,method=surface_gap(bpy.data.objects[a],bpy.data.objects[b])
  rows.append(dict(clip=clip,frame=frame,parts=[a,b],surface_gap_mm=gap*1000,method=method,limit_mm=limit*1000,passed=gap<=limit))
 # Every ready clip endpoint seats the inert visual witness on its stop.
 for clip,spec in interface.CLIPS.items():
  if interface.STATES[spec['end']]['action']!='rear':continue
  frame=spec['frames'];W.pose(arm,clip,frame)
  gap,method=surface_gap(bpy.data.objects['Bolt_ReadyWitness'],bpy.data.objects['Sear_VisualWitness'])
  rows.append(dict(clip=clip,frame=frame,parts=['Bolt_ReadyWitness','Sear_VisualWitness'],surface_gap_mm=gap*1000,method=method,limit_mm=.05,passed=gap<=.00005))
 W.pose(arm,'FireLast',interface.CLIPS['FireLast']['frames'])
 gap,_=surface_gap(bpy.data.objects['Bolt_ReadyWitness'],bpy.data.objects['Sear_VisualWitness'])
 assert gap>.075,('Forward empty pose must leave the ready witness',gap)
 rows.append(dict(clip='FireLast',frame=interface.CLIPS['FireLast']['frames'],parts=['Bolt_ReadyWitness','Sear_VisualWitness'],surface_gap_mm=gap*1000,required_separation_mm=75,comparison='>',kind='forward-empty negative seating check',passed=gap>.075))
 # Two old marks were left below the shortened leg. Check their real support,
 # independently of the serialization/clearance tests and operator offsets.
 W.pose(arm,'BipodDeploy',84)
 for label in ('L','R'):
  a='Bipod_DetentWitness_'+label+'259';b='Bipod_Extension_'+label
  gap,method=surface_gap(bpy.data.objects[a],bpy.data.objects[b])
  rows.append(dict(clip='BipodDeploy',frame=84,parts=[a,b],surface_gap_mm=gap*1000,method=method,limit_mm=.02,passed=gap<=.00002))
 return rows

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/lmg.blend');p.add_argument('--out',default='build/check.json');p.add_argument('--motion',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));arm=bpy.data.objects['HarrowArmature']
 from guns.common.interface_v1_8 import manifest
 schema=manifest(interface)
 g=geometry(arm);s=semantics(arm);b=belt_audit(arm);c=contacts(arm)
 out=dict(manifest=schema,geometry=g,semantics=s,belt=b,contacts=c,scope='visual assembly and animation only; no operative firing mechanism',passed=38000<=g['triangles']<=48000 and not g['nonmanifold'] and b['max_spacing_error_mm']<.10 and all(x['passed'] for x in c))
 if a.motion:
  # No wildcard waivers. Bounded visual sleeves and intended seats only.
  allow=ALLOW
  out['motion']=motion.sweep_clips(arm,list(interface.CLIPS),step_frames=1,tolerance_m=.0002,allow=allow)
  out['passed'] &= out['motion']['passed']
 Path(a.out).write_text(json.dumps(out,indent=2));print('CHECK',g,b['max_spacing_error_mm'],c,out['passed'])
 assert out['passed'],'See '+a.out
if __name__=='__main__':main()
