"""Head measurements from evaluated triangles; no generator parameters.

Three photo-station drops, transverse R fits and explicit centerline datums.
This is visual-asset evidence, not a working or manufacturing specification.
"""
import math
import numpy as np
from kit import weapon as W
from contacts import tree
from mathutils import Vector
_TREES={}
from action_gauges import circle

def top(x,y,names=('Action_Body',)):
 points=[]
 for name in names:
  if name not in _TREES:_TREES[name]=tree(name)
  hit=_TREES[name].ray_cast(Vector((x*.001,y*.001,.09)),Vector((0,0,-1)),.12)[0]
  if hit is not None:points.append(hit)
 assert points,(x,y,names)
 return max(points,key=lambda p:p.z)

def measure(arm):
 W.pose(arm,'Idle',0);_TREES.clear()
 crown=max(top(x,114.8).z*1000 for x in (-12.6,12.6))
 rows=[]
 for label,x,y,photo,uncertainty in [
  ('behind right return',12.6,95.5,5.6,3),('behind left return',-12.6,95.5,5.6,3),
  ('right side wood line',25.92,95.2,12.5,3),('left side wood line',-25.92,95.2,12.5,3),
  ('center wood line',0,85.2,8.5,3.5)]:
  p=top(x,y,('Action_Body','Top_Strap'));height=p.z*1000
  rows.append(dict(name=label,point_mm=[c*1000 for c in p],top_mm=height,
   drop_from_crown_mm=crown-height,photo_drop_mm=photo,photo_uncertainty_mm=uncertainty))
 line=[top(0,y) for y in np.arange(100.5,114.81,.25)]
 rib=top(0,115.2,('Solid_TopRib',)).z*1000
 front=top(0,114.8).z*1000
 radii=[]
 for side in (-1,1):
  points=[top(side*x,95.2) for x in np.arange(20.1,25.71,.2)]
  center,r,error=circle(np.array(points)[:,[0,2]]*1000)
  radii.append(dict(side=side,section_y_mm=95.2,radius_mm=r,max_fit_error_mm=error,center_mm=center.tolist()))
 # Profile fits expose the local compound radii with their approximation
 # error; no nominal fillet radius is fed to these observations.
 transitions=[]
 for side in (-1,1):
  for label,ys in [('fence to head',np.arange(96.5,102.01,.25)),('head to strap',np.arange(85.2,91.01,.25))]:
   points=[top(side*12.6 if label=='fence to head' else side*8.5,y,('Action_Body','Top_Strap')) for y in ys]
   center,r,error=circle(np.array(points)[:,[1,2]]*1000)
   transitions.append(dict(name=label,side=side,radius_mm=r,max_fit_error_mm=error,interval_mm=[float(ys[0]),float(ys[-1])]))
 endpoints=[]
 for side in (-1,1):
  pair=[]
  for label,x in [('outer',23.0),('inner',6.5)]:
   baseline_y=96 if label=='outer' else 94
   baseline=top(side*x,baseline_y).z*1000
   samples=[top(side*x,y) for y in np.arange(baseline_y,114.91,.1)]
   point=next(p for p in samples if p.z*1000>baseline+.10)
   record=dict(side=side,end=label,point_mm=[c*1000 for c in point],baseline_z_mm=baseline,baseline_y_mm=baseline_y,threshold_mm=.10)
   endpoints.append(record);pair.append(record)
  pair[0]['inner_behind_outer_mm']=pair[0]['point_mm'][1]-pair[1]['point_mm'][1]
 return dict(crown_mm=crown,height_stations=rows,
  centerline=dict(points_mm=[[c*1000 for c in p] for p in line],minimum_mm=min(p.z*1000 for p in line),maximum_mm=max(p.z*1000 for p in line),
   front_action_valley_mm=front,actual_rib_floor_mm=rib,scope='Y100.5–114.8 mm; lever recess at/behind its boss is separate'),
  side_return_radii=radii,transition_profile_fits=transitions,return_endpoints=endpoints,
  plan_scope='Rear return at x=23/6.5 mm, first 0.10 mm rise above the measured adjacent head (Y96 outer/Y94 inner); not a hard seam')
