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
from form_gauges import section

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
 line=[top(0,y) for y in np.arange(102,114.81,.25)]
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
  for label,ys in [('fence to head',np.arange(96.5,102.01,.25)),('head to strap',np.arange(92,94.01,.1))]:
   points=[top(side*12.6 if label=='fence to head' else side*10.0,y,('Action_Body','Top_Strap')) for y in ys]
   center,r,error=circle(np.array(points)[:,[1,2]]*1000)
   transitions.append(dict(name=label,side=side,radius_mm=r,max_fit_error_mm=error,interval_mm=[float(ys[0]),float(ys[-1])]))
 endpoints=[]
 for side in (-1,1):
  pair=[]
  for label,x in [('outer',23.0),('inner',7.5)]:
   baseline_y=96 if label=='outer' else 94
   baseline=top(side*x,baseline_y).z*1000
   samples=[top(side*x,y) for y in np.arange(baseline_y,114.91,.1)]
   point=next(p for p in samples if p.z*1000>baseline+.10)
   record=dict(side=side,end=label,point_mm=[c*1000 for c in point],baseline_z_mm=baseline,baseline_y_mm=baseline_y,threshold_mm=.10)
   endpoints.append(record);pair.append(record)
  pair[0]['inner_behind_outer_mm']=pair[0]['point_mm'][1]-pair[1]['point_mm'][1]
 radial=[]
 for angle in range(30,151,15):
  t=math.radians(angle);direction=Vector((math.cos(t),math.sin(t),0))
  center=Vector((0,.094,.049))
  head=_TREES['Action_Body'].ray_cast(center+direction*.00565,direction,.03)[0]
  if 'Top_LeverSpindle' not in _TREES:_TREES['Top_LeverSpindle']=tree('Top_LeverSpindle')
  boss=_TREES['Top_LeverSpindle'].ray_cast(center,direction,.02)[0]
  assert head is not None and boss is not None
  radial.append(dict(angle_deg=angle,gap_mm=(head-boss).length*1000,head_radius_mm=(head-center).length*1000,boss_radius_mm=(boss-center).length*1000))
 roof=top(0,103).z*1000
 wall=_TREES['Action_Body'].ray_cast(Vector((0,.099,.053)),Vector((0,1,0)),.02)[0].y*1000
 p=section('Action_Body',0,.0000005)*1000
 arc=p[(p[:,1]>wall+.02)&(p[:,1]<wall+.9)&(p[:,2]>roof-.9)&(p[:,2]<roof-.02)]
 assert len(arc)>=6,('Recess lip section',len(arc),wall,roof)
 lc,lr,le=circle(arc[:,[1,2]])
 rolls=[]
 for side in (-1,1):
  base=top(side*12.6,95.5).z*1000
  ys=np.arange(97,106.76,.25);ds=115-ys;values=np.array([top(side*12.6,y).z*1000-base for y in ys])
  candidates=[]
  for end in np.arange(14,24.001,.01):
   t=np.clip((ds-8)/(end-8),0,1);u=1-t
   basis=np.c_[u**5,5*t*u**4,10*t*t*u**3]
   coefficients=np.linalg.lstsq(basis,values,rcond=None)[0]
   error=float(np.sqrt(np.mean((basis@coefficients-values)**2)))
   if coefficients[0]>=coefficients[1]>=coefficients[2]>=0:candidates.append((error,float(end)))
  error,end=min(candidates);rolls.append(dict(side=side,fitted_length_mm=end,rms_profile_error_mm=error,scope='fit to degree-5 rear return; zero height/slope/curvature endpoint inferred from triangles'))
 assert min(p.z*1000 for p in line)>=rib-.01
 assert all(abs(r['drop_from_crown_mm']-r['photo_drop_mm'])<=r['photo_uncertainty_mm'] for r in rows),rows
 assert .35<lr<.85,(lr,le)
 assert all(8.5<=r['inner_behind_outer_mm']<=14.5 for r in endpoints if 'inner_behind_outer_mm' in r),endpoints
 assert all(2<r['radius_mm']<10 for r in transitions),transitions
 return dict(crown_mm=crown,height_stations=rows,
  centerline=dict(points_mm=[[c*1000 for c in p] for p in line],minimum_mm=min(p.z*1000 for p in line),maximum_mm=max(p.z*1000 for p in line),
   front_action_valley_mm=front,actual_rib_floor_mm=rib,scope='Y102–114.8 mm: uninterrupted head; rounded fore lip and boss recess lie behind this interval'),
  side_return_radii=radii,transition_profile_fits=transitions,return_endpoints=endpoints,
  crown_roll_profile_fits=rolls,boss_radial_clearance=radial,recess_lip=dict(radius_mm=lr,max_fit_error_mm=le,section_x_mm=.0005,points=len(arc)),
  plan_scope='Rear return at x=23/7.5 mm, first 0.10 mm rise above the measured adjacent head (Y96 outer/Y94 inner); not a hard seam')
