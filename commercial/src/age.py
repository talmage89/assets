"""Explicit fifteen-year service sites, using guarded shared-atlas overlays.

Drip patches sit under vehicle engines at each fueling face and parking stall.
Tracks follow the entries and swept turns; repairs follow a buried-service
trench. Vertical deposits start at actual folded joints and exposed steel.
"""
import math,random
import bmesh
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
   u,v=rotate((side*2.10,-1.60),c['angle']);yaw=c['angle']+rng.uniform(-9,9)
   decal('Fueling engine drips',(x+u,y+v,.014),3.0,9.0,'Oil'+str(rng.randrange(4)),r,yaw)
   causes.append(dict(cause='engine drips at fueling position',center=(x+u,y+v,.014)))
  # Dirt at each plinth and where shoes work around both operating faces.
  for side in (-1,1):
   u,v=rotate((side*.45,-.96),c['angle'])
   decal('Dispenser base grime',(x+u,y+v,.164),.78,1.25,'Oil'+str(rng.randrange(4)),r,c['angle'])
 # Repeated wheel contacts continue through each fueling lane, including
 # its exposed approach beyond the canopy. They cross the absorbed drops.
 for island in meta['islands']:
  for side in (-1,1):
   for wheel in (-1,1):
    lateral=side*2.10+wheel*.78;points=[]
    for i in range(20):
     along=-c['depth']/2-3+i*(c['depth']+5)/19
     u,v=rotate((lateral+.09*math.sin(i*.40+island['index']*1.13+wheel*.67),along),c['angle'])
     points.append((island['center'][0]+u,island['center'][1]+v))
    ob=ribbon('Fuel lane repeated wheel contact',points,.27,r,mat='White',z=.014);ob['wear_cell']='Tire';ob['swept_wear']=True
    for i in range(20):
     along=-c['depth']/2-3+i*(c['depth']+5)/19
     level=.014 if -c['depth']/2-.8<along<c['depth']/2+.8 else .0035
     for vertex in ob.data.vertices[2*i:2*i+2]:vertex.co.z=level
 # Parking engine positions, including the accessible vehicle bay, without
 # painting over its clear aisle. Lightly worn markings are vertex-filtered.
 for i in range(meta['stalls']):
  xx=b['center_x']-b['width']/2+.15+(i+.5)*9*FT
  if abs(xx-meta['access']['center_x'])<1.3:continue
  yy=b['front']-meta['walk']-1.8
  decal('Parked engine drips',(xx,yy,.003),1.80,3.7,'Oil'+str(i%4),r,rng.uniform(-8,8))
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
   ob=ribbon('Driveway turning tire contact',points,.32,r,mat='White',z=.0035)
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
 # Wash from the canopy's folded sheet joints, on all four outer faces.
 # The ink is only deposited below an actual panel division, not over logos.
 can=bpy.data.objects['Canopy']
 for axis,length,fixed in ((0,c['width'],c['depth']/2+.052),(1,c['depth'],c['width']/2+.052)):
  for i in range(1,math.ceil(length/2.4384)):
   along=-length/2+i*2.4384
   flow=random.Random(meta['seed']*887+axis*71+i);height=flow.uniform(.48,.83)
   for side in (-1,1):
    pos=(along,side*fixed,c['clear']+c['fascia']-height/2-.028) if axis==0 else (side*fixed,along,c['clear']+c['fascia']-height/2-.028)
    ob=decal('Fascia joint runoff',pos,flow.uniform(.31,.48),height,'Grime',can,(0 if side<0 else 180) if axis==0 else (90 if side>0 else -90),True)
    ob['wear_flip']=flow.random()>.5
 for i in range(int(w/2.4384)+1):
  x=-w/2+.20+i*2.4384
  for side in (-1,1):
   flow=random.Random(meta['seed']*701+i*31+side);length=flow.uniform(.54,.94)
   ob=decal('Coping seam runoff',(x,side*(d/2+.004),b['parapet']-.065-length/2),flow.uniform(.24,.36),length,'Grime',store,0 if side<0 else 180,True)
   ob['wear_flip']=flow.random()>.5
   if side>0:
    # A deposit must not bridge the open drainage sleeve. Cut its actual
    # aperture out of the non-solid overlay, retaining the full chart below.
    bm=bmesh.new();bm.from_mesh(ob.data)
    for sx in (-w*.35,w*.35):
     lx=x-sx # rear overlay is rotated through 180 degrees
     if abs(lx)>.31:continue
     lo,hi=lx-.145,lx+.145;bottom=b['roof']+.017-ob.location.z;top=b['roof']+.163-ob.location.z
     for axis,value in ((0,lo),(0,hi),(2,bottom),(2,top)):
      point=[0,0,0];normal=[0,0,0];point[axis]=value;normal[axis]=1
      bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],dist=1e-7,plane_co=point,plane_no=normal)
     gone=[f for f in bm.faces if lo<f.calc_center_median().x<hi and bottom<f.calc_center_median().z<top]
     bmesh.ops.delete(bm,geom=gone,context='FACES')
    bm.to_mesh(ob.data);bm.free()
 for side in (-1,1):
  for j in range(9):
   y=-d/2+.7+j*(d-1.4)/8
   decal('Low masonry salt from moisture',(side*(w/2+.043),y,.34),.46,.40,'Salt',store,90 if side>0 else -90,True)
 # Paint loss follows scraped arcs, conforming to the real pipe surface.
 # Rust is restricted to those exposed chips and to water at the base collar.
 for ob in list(bpy.context.scene.objects):
  if ob.type!='MESH' or not ob.name.startswith('Pipe bollard'):continue
  parent=ob.parent
  for scar,(height,span) in enumerate(((.052,1.4),(.39,.70))):
   vertices=[]
   for i in range(10):
    theta=-math.pi/2-span/2+span*i/9;z=height+.007*math.sin(i*2.7+meta['seed'])
    thickness=(.025 if scar==0 else .010)*max(.10,math.sin(math.pi*i/9))
    for dz in (-thickness,thickness):vertices.append((.0846*math.cos(theta),.0846*math.sin(theta),z+dz))
   chip=mesh('Impact exposed paint chip',vertices,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(9)],'Metal',parent,False)
   if scar==0:
    # Small irregular oxide fragments border only the actual chipped ring.
    chip['rust_finish']=True
 meta['wear_causes']=dict(age_years=15,maintained=True,fueling_positions=causes,methods='Generated guarded footprints, swept contact paths, physical repair/seal ribbons, coping runoff, contact wear and broad COLOR_0')
 return r
