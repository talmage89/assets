"""Round-four exterior measurements from actual evaluated surfaces, in meters.

No geometry-generator dimensions enter the fits. Circular transverse/edge
profiles and the longitudinal roll are least-squares observations of triangles.
They describe a visual asset, not a manufacturing or working firearm model.
"""
import math,numpy as np
from mathutils import Vector
from kit import weapon as W,motion
from contacts import part,ray
from form_gauges import section

def circle(points):
 p=np.array(points);c=np.linalg.lstsq(np.c_[2*p,np.ones(len(p))],(p*p).sum(1),rcond=None)[0]
 center=c[:2];r=math.sqrt(c[2]+center@center)
 return center,r,float(np.max(abs(np.linalg.norm(p-center,axis=1)-r)))
def measure(arm):
 W.pose(arm,'Idle',0);rows={};body=np.array(motion.surface(part('Action_Body'))['points'])
 barrels=np.r_[np.array(motion.surface(part('Barrel_R'))['points']),np.array(motion.surface(part('Barrel_L'))['points'])]
 barrels=barrels[abs(barrels[:,1]-.115)<1e-7]
 top=float(barrels[:,2].max());barrel_width=float(np.ptp(barrels[:,0]))
 fences=[]
 for side,name in [(1,'right'),(-1,'left')]:
  upper=body[(side*body[:,0]>.0065)&(body[:,1]>.095)&(body[:,2]>.044)]
  bore=[]
  for by in (.125,.145):
   points=[]
   for angle in range(0,360,10):
    t=math.radians(angle)
    points.append(ray('Barrel_'+('R' if side>0 else 'L'),(side*.0126,by,.044),(math.cos(t),0,math.sin(t))))
   bc,br,be=circle(np.array(points)[:,[0,2]]);bore.append((by,bc))
  bore_axis=lambda y:bore[0][1]+(bore[1][1]-bore[0][1])*(y-bore[0][0])/(bore[1][0]-bore[0][0])
  fits=[]
  for y in (.108,.110,.112,.114):
   pts=[]
   for angle in range(35,101,5):
    t=math.radians(angle);d=(side*math.cos(t),0,math.sin(t))
    origin=Vector((side*.0126,float(y),.044))+Vector(d)*.006
    pts.append(ray('Action_Body',origin,d))
   center,r,error=circle(np.array(pts)[:,[0,2]])
   fits.append(dict(y_m=float(y),center_m=center.tolist(),radius_m=r,max_error_m=error))
  # r(y)^2 is quadratic for an axial elliptical roll, fitted without supplying
  # a radius or longitudinal length from the model generator.
  # The exposed front circles retain the accepted crown curvature.
  # The remaining 10.5 mm joins the head with a degree-5 return; its
  # physical rear extent is measured separately in head_gauges.py.
  crown=[(f['y_m'],f['radius_m']) for f in fits]
  y=np.array([p[0] for p in crown]);r2=np.array([p[1]**2 for p in crown])
  a,b,c=np.polyfit(y,r2,2);yc=-b/(2*a);rr=c-b*b/(4*a);length=math.sqrt(-rr/a)
  centers=np.array([f['center_m'] for f in fits]);delta=centers-np.array([bore_axis(f['y_m']) for f in fits])
  fences.append(dict(side=name,highest_mm=float(upper[:,2].max()*1000),barrel_top_mm=top*1000,
   height_difference_mm=float((upper[:,2].max()-top)*1000),arc_fits=fits,
   exposed_arc_scope="first 8 mm behind breech; remaining rear surface joins the head",crown_roll_samples=crown,
   bore_axis_at_breech_mm=(bore_axis(.115)*1000).tolist(),maximum_center_offset_mm=float(np.linalg.norm(delta,axis=1).max()*1000),
   fitted_front_radius_mm=math.sqrt(rr)*1000,fitted_rounding_length_mm=length*1000,
   fitted_roll_front_y_mm=yc*1000,photo_rounding_estimate_mm=[18,20]))
 rows['fences']=fences
 p=section('Action_Body',1,.1149);p=p[p[:,2]>.0439]
 rows['fence_pair_section_width_mm']=float(np.ptp(p[:,0])*1000)
 crowns=body[(body[:,1]>.095)&(body[:,1]<.11501)&(body[:,2]>.04399)]
 rows['fence_pair_width_mm']=float(np.ptp(crowns[:,0])*1000);rows['barrel_breech_width_mm']=barrel_width*1000
 steps=[]
 for side in (-1,1):
  for z in (.016,.020,.024,.0255):
   a=ray('Action_Body',(side*.08,.1148,z),(-side,0,0));b=ray('Action_Body',(side*.08,.1152,z),(-side,0,0))
   steps.append(abs(a.x-b.x)*1000)
 rows['maximum_head_bar_side_step_mm']=max(steps)
 bottom=[]
 for y in (.120,.135,.150):
  p=section('Action_Body',1,y);bottom_z=p[:,2].min()
  for side in (-1,1):
   arc=p[(side*p[:,0]>.0183)&(abs(p[:,0])<.0258)&(p[:,2]<bottom_z+.007)]
   center,r,error=circle(arc[:,[0,2]])
   bottom.append(dict(y_mm=y*1000,side=side,radius_mm=r*1000,max_fit_error_mm=error*1000))
 rows['bottom_edge_radius']=bottom;rows['photo_bottom_radius_estimate_mm']=[7,9]
 seams=[]
 for x in (.0005,.005,.010,.015,.020,.024):
  p=section('Trigger_Plate',0,x);end=float(p[:,1].max());d=.00022
  def z(name,y):return ray(name,(x,y,-.035),(0,0,1)).z
  # Extrapolate both immediately adjacent skins to the same seam station;
  # otherwise the rising belly slope would be incorrectly counted as a step.
  plate_z=2*z('Trigger_Plate',end-d)-z('Trigger_Plate',end-2*d)
  body_z=2*z('Action_Body',end+d)-z('Action_Body',end+2*d)
  seams.append(dict(x_mm=x*1000,y_mm=end*1000,step_mm=abs(body_z-plate_z)*1000))
 rows['plate_seam']=seams;rows['maximum_bar_plate_step_mm']=max(r['step_mm'] for r in seams)
 slots=[]
 for name,x,y in [('Front_Trigger',.0026,.064),('Rear_Trigger',-.0026,.031)]:
  p=(x,y+(.003 if name=='Rear_Trigger' else 0),.0028 if name=='Rear_Trigger' else .0065)
  a=ray('Trigger_Plate',p,(-1,0,0));b=ray('Trigger_Plate',p,(1,0,0))
  blade_points=np.array(motion.surface(part(name))['points']);blade_width=float(np.ptp(blade_points[:,0]))
  slots.append(dict(blade=name,slot_width_mm=(b.x-a.x)*1000,blade_width_mm=blade_width*1000,
   clearance_each_side_mm=((b.x-a.x)-blade_width)*500))
 rows['trigger_slots']=slots
 assert max(r['height_difference_mm'] for r in fences)<.015,fences
 assert rows['fence_pair_width_mm']<=rows['barrel_breech_width_mm']+.02,(rows['fence_pair_width_mm'],rows['barrel_breech_width_mm'])
 assert max(r['maximum_center_offset_mm'] for r in fences)<.06,fences
 assert all(17<r['fitted_rounding_length_mm']<21 for r in fences),fences
 assert rows['maximum_head_bar_side_step_mm']<.02,rows['maximum_head_bar_side_step_mm']
 assert rows['maximum_bar_plate_step_mm']<.15,seams
 assert all(7.7<r['radius_mm']<8.3 for r in bottom),bottom
 assert all(.20<r['clearance_each_side_mm']<.40 for r in slots),slots
 return rows
