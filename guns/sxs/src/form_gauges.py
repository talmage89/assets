"""Measured exterior form evidence from evaluated triangles, independent of export.

These are visual-asset gauges, not engineering or manufacturing specifications.
The photographs have no ruler; scale inference and its uncertainty are documented
separately in refs/SOURCES.md. No photo is imported here.
"""
import numpy as np
from mathutils import Vector
from kit import motion,weapon as W
from contacts import part,ray

def section(name,axis,station):
 ob=part(name);ev=ob.evaluated_get(__import__('bpy').context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();points=[]
 for tri in me.loop_triangles:
  ps=[ev.matrix_world@me.vertices[i].co for i in tri.vertices]
  for a,b in zip(ps,ps[1:]+ps[:1]):
   if (a[axis]-station)*(b[axis]-station)<0:points.append(a+(b-a)*(station-a[axis])/(b[axis]-a[axis]))
 ev.to_mesh_clear();assert points,(name,station);return np.array(points)
def width(name,y):
 p=section(name,1,y);return float(np.ptp(p[:,0])*1000)
def measure(arm):
 W.pose(arm,'Idle',0)
 lever=motion.surface(part('Top_Lever'))['points'];lever=np.array(lever)
 boss=np.array(motion.surface(part('Top_LeverSpindle'))['points'])
 rows=dict(lever_boss_diameter_mm=float(np.ptp(boss[:,0])*1000),lever_length_mm=float(np.ptp(lever[:,1])*1000),lever_overall_width_mm=float(np.ptp(lever[:,0])*1000),
  lever_thumb_width_mm=width('Top_Lever',.030),lever_sections=[])
 for y in (.030,.050,.072):
  x=.0006 if y<.07 else 0
  hi=ray('Top_Lever',(x,y,.09),(0,0,-1));lo=ray('Top_Lever',(x,y,0),(0,0,1));seat=ray('Top_Strap',(x,y,.09),(0,0,-1))
  rows['lever_sections'].append(dict(y_mm=y*1000,vertical_thickness_mm=(hi.z-lo.z)*1000,strap_gap_mm=(lo.z-seat.z)*1000))
 p=section('Trigger_Guard',1,.072);p=p[p[:,2]<-.028]
 rows['guard_band_width_mm']=float(np.ptp(p[:,0])*1000);rows['guard_band_thickness_mm']=float(np.ptp(p[:,2])*1000)
 # Broad flat side samples. SVD fits a plane to actual ray hits, with no
 # generator slope or expected normal fed into the measurement.
 planes={}
 for side in (-1,1):
  points=[ray('Action_Body',(side*.08,y,z),(-side,0,0)) for y in (.095,.100,.105,.110) for z in (.014,.020,.026)]
  p=np.array(points);c=p.mean(0);_,_,vh=np.linalg.svd(p-c);distance=abs((p-c)@vh[-1])
  planes['right' if side>0 else 'left']=dict(samples=len(p),max_deviation_mm=float(max(distance)*1000),normal=vh[-1].tolist())
 for side in (-1,1):
  points=[ray('Action_Body',(side*.08,y,z),(-side,0,0)) for y in (.125,.135,.145) for z in (.017,.021,.024)]
  p=np.array(points);c=p.mean(0);_,_,vh=np.linalg.svd(p-c);distance=abs((p-c)@vh[-1])
  planes[('right' if side>0 else 'left')+' bar']=dict(samples=len(p),max_deviation_mm=float(max(distance)*1000),normal=vh[-1].tolist())
 rows['ground_side_planes']=planes
 eye=__import__('bpy').data.objects['Socket_Eye'].matrix_world.translation
 a=ray('Solid_TopRib',(0,.116,.09),(0,0,-1));b=ray('Solid_TopRib',(0,.774,.09),(0,0,-1))
 datum=lambda y:a.z+(y-a.y)*(b.z-a.z)/(b.y-a.y)
 rib=ray('Solid_TopRib',(0,.315,.09),(0,0,-1));comb=ray('Stock_Walnut',eye,(0,0,-1))
 eye_line=eye.z+(.0547-eye.z)*(.315-eye.y)/(.766-eye.y)
 rows['eye_fit']=dict(eye_mm=[v*1000 for v in eye],comb_z_mm=comb.z*1000,
  height_above_comb_mm=(eye.z-comb.z)*1000,height_above_extended_rib_mm=(eye.z-datum(eye.y))*1000,
  drop_at_cheek_mm=(datum(eye.y)-comb.z)*1000,coin_station_mm=315,actual_rib_z_mm=rib.z*1000,
  ray_above_coin_station_rib_mm=(eye_line-rib.z)*1000,rule_coin_mm=3.15,
  rule_error_mm=abs(eye_line-rib.z-.00315)*1000)
 assert max(v['max_deviation_mm'] for v in planes.values())<.02,planes
 assert rows['eye_fit']['rule_error_mm']<.02
 assert 12.0<rows['guard_band_width_mm']<12.8 and 1.4<rows['guard_band_thickness_mm']<1.9
 assert 75<rows['lever_length_mm']<81
 return rows
