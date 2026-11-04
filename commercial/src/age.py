"""Explicit fifteen-year service sites, using guarded shared-atlas overlays.

Drip patches sit under vehicle engines at each fueling face and parking stall.
Tracks follow the entries and swept turns; repairs follow a buried-service
trench. Vertical deposits start at actual folded joints and exposed steel.
"""
import math,random
from geometry import *
from plan import rotate,FT


def decal(name,p,w,h,cell,parent,yaw=0,vertical=False):
 x,y,z=p
 vs=[(-w/2,0,-h/2),(w/2,0,-h/2),(w/2,0,h/2),(-w/2,0,h/2)] if vertical else [(-w/2,-h/2,0),(w/2,-h/2,0),(w/2,h/2,0),(-w/2,h/2,0)]
 ob=mesh(name,vs,[(0,1,2,3)],'White',parent,False);ob.location=(x,y,z);ob.rotation_euler.z=math.radians(yaw);ob['wear_cell']=cell;return ob


def ribbon(name,pts,width,parent,mat='Black',z=.003):
 verts=[]
 for i,q in enumerate(pts):
  a=Vector(pts[max(0,i-1)]);b=Vector(pts[min(len(pts)-1,i+1)]);d=b-a;le=math.hypot(d.x,d.y);nx,ny=-d.y/le,d.x/le
  verts.extend(((q[0]+nx*width/2,q[1]+ny*width/2,z),(q[0]-nx*width/2,q[1]-ny*width/2,z)))
 return mesh(name,verts,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(len(pts)-1)],mat,parent,False)


def add(meta):
 rng=random.Random(meta['seed']+991);c=meta['canopy'];b=meta['building'];W,D=meta['lot']
 r=root('ServiceWear',kind='SitePaving');r['reusable_module']=True;causes=[]
 # Narrow sediment halos follow the authored saw cuts. They reuse the
 # sheet's irregular linear contact mask, with the physical cut still visible.
 pad=root('Joint deposits',(*c['center'],.013),c['angle'],parent=r)
 for x in [-c['width']/2+i*3.048 for i in range(int(c['width']/3.048)+1)]:
  decal('Fuel joint retained dirt',(x,0,0),.07,c['depth']+1.6,'Tire',pad)
 for y in (-3.048,0,3.048):decal('Fuel joint retained dirt',(0,y,.0002),.07,c['width']+2,'Tire',pad,90)
 # Every side of every island has a parking/engine footprint. This coordinate
 # is the vehicle center, with the stain forward where its engine rests.
 for island in meta['islands']:
  x,y=island['center']
  for side in (-1,1):
   u,v=rotate((side*2.10,-.90),c['angle']);yaw=c['angle']+rng.uniform(-9,9)
   decal('Fueling engine drips',(x+u,y+v,.014),1.45,2.25,'Oil'+str(rng.randrange(4)),r,yaw)
   causes.append(dict(cause='engine drips at fueling position',center=(x+u,y+v,.014)))
  # Dirt at each plinth and where shoes work around both operating faces.
  for side in (-1,1):
   u,v=rotate((side*.45,-.96),c['angle'])
   decal('Dispenser base grime',(x+u,y+v,.164),.78,1.25,'Oil'+str(rng.randrange(4)),r,c['angle'])
 # Parking engine positions, including the accessible vehicle bay, without
 # painting over its clear aisle. Lightly worn markings are vertex-filtered.
 for i in range(meta['stalls']):
  xx=b['center_x']-b['width']/2+.15+(i+.5)*9*FT
  if abs(xx-meta['access']['center_x'])<1.3:continue
  yy=b['front']-meta['walk']-1.8
  decal('Parked engine drips',(xx,yy,.003),1.30,1.70,'Oil'+str(i%4),r,rng.uniform(-8,8))
 # Tire contact sweeps enter from each opening and turn toward the canopy.
 for drive in meta['driveways']:
  dx,dy=drive['center'];south=drive['edge']=='south'
  for side in (-1,1):
   points=[]
   for i in range(12):
    t=i/11
    if south:
     x=dx+side*.79-2.2*t*t;y=dy+.3+t*7.0;yaw=-math.degrees(math.atan2(-4.4*t,7))
    else:
     x=dx+.3+t*8.5;y=dy+side*.79-2.0*t*t;yaw=90-math.degrees(math.atan2(-4.0*t,8.5))
    points.append((x,y))
   # One continuous swept contact, rather than repeated rectangular stamps.
   ob=ribbon('Driveway turning tire contact',points,.23,r,mat='White',z=.0035)
   for i in range(12):
    center=Vector((*points[i],.0035));factor=max(.06,min(1,i/1.5,(11-i)/1.5))
    for vertex in ob.data.vertices[2*i:2*i+2]:vertex.co=center+(vertex.co-center)*factor
   ob['wear_cell']='Tire';ob['swept_wear']=True
 # Sealed branching shrinkage cracks in the asphalt beyond the pad. A cut
 # trench is visibly a repair, not a random all-over dirty noise field.
 x0=W/2-6.7;x1=W/2-5.9;y0=-D/2+8.7;y1=b['front']-meta['walk']-.5
 repair=mesh('Patched buried-service trench',[(x0,y0,.002),(x1,y0,.002),(x1,y1,.002),(x0,y1,.002)],[(0,1,2,3)],'Asphalt',r,False);repair['repair']=True
 for xx in (x0,x1):ribbon('Trench sawcut seal',[(xx,y0),(xx,y1)],.035,r)
 for i in range(3):
  yy=-D/2+1.8+i*.66;pts=[(-W/2+2+j*1.4,yy+.08*math.sin(j*1.7+i)) for j in range(11)]
  ribbon('Sealed asphalt crack',pts,.028,r)
  branch=pts[4];ribbon('Crack branch',[branch,(branch[0]+.35,branch[1]+.48),(branch[0]+1.2,branch[1]+.63)],.021,r)
 # Gum belongs to foot traffic near thresholds and pump controls.
 for i in range(32):
  x=rng.uniform(-2.1,2.1);y=b['front']-rng.uniform(.25,2.5)
  if abs(x-meta['access']['center_x'])<meta['access']['width']/2:continue
  decal('Entrance gum',(x,y,.1545),rng.uniform(.024,.062),rng.uniform(.024,.055),'Gum',r,rng.uniform(0,360))
 # Runoff decals are parented to the actual architectural module. Each
 # narrow streak starts at a folded seam; salts stay in the wet base course.
 store=bpy.data.objects['Store'];w,d=b['width'],b['depth'];fy=-d/2
 for i in range(int(w/2.4384)+1):
  x=-w/2+.20+i*2.4384
  for side in (-1,1):
   decal('Coping seam runoff',(x,side*(d/2+.004),b['parapet']-.43),.22,.78,'Grime',store,0 if side<0 else 180,True)
 for side in (-1,1):
  for j in range(9):
   y=-d/2+.7+j*(d-1.4)/8
   decal('Low masonry salt from moisture',(side*(w/2+.043),y,.34),.46,.40,'Salt',store,90 if side>0 else -90,True)
 # Paint impact is concentrated near bumper height and the exposed base.
 for ob in list(bpy.context.scene.objects):
  if ob.type!='MESH' or not ('Pipe bollard' in ob.name or 'Column U guard' in ob.name):continue
  parent=ob.parent;xx,yy,_=ob.location
  if 'Pipe bollard' in ob.name:
   decal('Bollard impact scuff',(xx,yy-.0845,.28),.115,.24,'Scuff',parent,0,True)
   decal('Bollard exposed steel corrosion',(xx,yy-.085,.09),.11,.12,'Rust',parent,0,True)
 meta['wear_causes']=dict(age_years=15,maintained=True,fueling_positions=causes,methods='Generated guarded footprints, swept contact paths, physical repair/seal ribbons, coping runoff, contact wear and broad COLOR_0')
 return r
