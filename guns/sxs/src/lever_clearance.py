"""0–25 degree visual lever sweep: evaluated triangle-surface separation.

Vertex/triangle distances plus interior edge/edge minima are measured. BVH
radius queries conservatively retain edge candidates. Angles are sampled at
0.5 degree intervals; this is not a continuous collision certificate.
"""
import math
import numpy as np
import bpy
from mathutils import Vector,Matrix
from kit import motion,weapon as W
from contacts import part

def gap(a,b):
 best=math.inf
 for source,target in ((a,b),(b,a)):
  for p in source['points']:
   hit=target['tree'].find_nearest(p)
   if hit[0] is not None:best=min(best,hit[3])
 # Vertex/triangle candidates cover edge endpoint cases. Only interior
 # closest points on two nonparallel edges can improve that upper bound.
 fixed=np.array([tuple(p) for p in b['points']]);faces=np.array(b['faces'])
 edges={tuple(sorted((f[i],f[(i+1)%3]))) for f in a['faces'] for i in range(3)}
 for ia,ib in edges:
  p=a['points'][ia];q=a['points'][ib];u=np.array(q-p);aa=u@u
  if aa<1e-18:continue
  candidates=b['tree'].find_nearest_range((p+q)*.5,math.sqrt(aa)*.5+best+1e-8)
  if not candidates:continue
  tri=fixed[faces[[r[2] for r in candidates]]]
  c=tri.reshape(-1,3);d=np.roll(tri,-1,axis=1).reshape(-1,3);v=d-c;w=np.array(p)-c
  bb=v@u;cc=(v*v).sum(1);dd=w@u;ee=(v*w).sum(1);den=aa*cc-bb*bb
  valid=den>1e-22
  t=np.divide(bb*ee-cc*dd,den,out=np.zeros_like(den),where=valid)
  s=np.divide(aa*ee-bb*dd,den,out=np.zeros_like(den),where=valid)
  valid &= (t>=0)&(t<=1)&(s>=0)&(s<=1)
  if valid.any():
   delta=w[valid]+t[valid,None]*u-s[valid,None]*v[valid]
   best=min(best,float(np.sqrt((delta*delta).sum(1)).min()))
 return best

def measure(arm):
 W.pose(arm,'Idle',0)
 original=arm.animation_data.action;basis={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
 arm.animation_data.action=None
 fixed={name:motion.surface(part(name)) for name in ('Action_Body','Top_Strap','Stock_Walnut')}
 bone=arm.pose.bones['TopLever'];rest=bone.matrix.copy();world_rest=arm.matrix_world@rest;pivot=world_rest.translation.copy()
 records=[]
 try:
  for i in range(51):
   angle=i*.5
   bone.matrix=arm.matrix_world.inverted()@Matrix.Translation(pivot)@Matrix.Rotation(math.radians(angle),4,'Z')@Matrix.Translation(-pivot)@world_rest
   bpy.context.view_layer.update()
   for moving in ('Top_Lever','Top_LeverSpindle'):
    surface=motion.surface(part(moving))
    for name,stationary in fixed.items():
     distance=gap(surface,stationary)
     penetration,crossings=motion.penetration(surface,stationary,.00002)
     records.append(dict(angle_deg=angle,moving=moving,fixed=name,gap_mm=distance*1000,
      penetration_mm=penetration*1000,triangle_crossings=crossings))
 finally:
  arm.animation_data.action=original
  for name,value in basis.items():arm.pose.bones[name].matrix_basis=value
  bpy.context.view_layer.update()
 minimum=min(records,key=lambda r:r['gap_mm'])
 return dict(passed=min(r['gap_mm'] for r in records)>.025 and max(r['penetration_mm'] for r in records)<.001,
  range_deg=[0,25],step_deg=.5,angular_samples=51,method='evaluated triangle surfaces; vertex/face and interior edge/edge distances; BVH conservative candidates',
  minimum_gap_mm=minimum['gap_mm'],minimum_at=minimum,maximum_penetration_mm=max(r['penetration_mm'] for r in records),records=records)
