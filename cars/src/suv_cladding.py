"""Separate molded arch extensions, door cladding, lower fascias and roof rails."""
import math
import bpy
from mathutils import Vector
from kit import model as G
import suv_spec as S

def build(b,tree):
 from suv_body import arch_point,trim_arch,closeable_sheet
 for label,sgn in [('L',-1),('R',1)]:
  for end,axle in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
   count=64 if b.high else 24
   angles=[-.115+(math.pi+.230)*i/count for i in range(count+1)];nu=len(angles);verts=[]
   for width,proud in [(0,.010),(.008,.0225),(.045,.0205),(.060,.004)]:
    for a in angles:
     y,z=arch_point(a,axle,width);p=tree.ray_cast(Vector((sgn*2,y,z)),Vector((-sgn,0,0)),3)[0]
     x=abs(p.x) if p else .896
     verts.append((sgn*(x+proud-(.007 if end=='F' and width in [.008,.045] else .003 if end=='F' and width==0 else .0019 if end=='R' and width in [.008,.045] else 0)),y,z))
   fs=[(j*nu+i,j*nu+i+1,(j+1)*nu+i+1,(j+1)*nu+i) for j in range(3) for i in range(nu-1)]
   ob=G.mesh('Arch cladding_'+end+label,verts,fs,b.m['rubber']);sol=ob.modifiers.new('Injection molded gauge','SOLIDIFY');sol.thickness=.003;sol.offset=-1;G.apply(ob);b.add(ob,category='cladding')
   # Inner flange is visibly turned into each opening, with a 22 mm return.
   ring=verts[:nu];inner=[(x-sgn*.022,y,z) for x,y,z in ring]
   ob=G.mesh('Arch flange_'+end+label,ring+inner,[(i,i+1,nu+i+1,nu+i) for i in range(nu-1)],b.m['rubber']);sol=ob.modifiers.new('Flange gauge','SOLIDIFY');sol.thickness=.002;G.apply(ob);b.add(ob,category='cladding')
  for end,ya,yb in [('F',S.DOOR_FRONT+.004,S.DOOR_SPLIT-.004),('R',S.DOOR_SPLIT+.004,S.DOOR_REAR-.004)]:
   verts=[];n=16 if b.high else 8
   for z,d in [(.285,.003),(.304,.006),(.415,.007),(.440,.003)]:
    for i in range(n+1):
     y=ya+(yb-ya)*i/n;p=tree.ray_cast(Vector((sgn*2,y,z)),Vector((-sgn,0,0)),3)[0]
     x=abs(p.x) if p else .81;verts.append((sgn*(x+d),y,z))
   ob=G.mesh('Lower door cladding_'+end+label,verts,[(j*(n+1)+i,j*(n+1)+i+1,(j+1)*(n+1)+i+1,(j+1)*(n+1)+i) for j in range(3) for i in range(n)],b.m['rubber'])
   for axle in [S.FRONT_AXLE,S.REAR_AXLE]:trim_arch(ob,axle,96 if b.high else 64)
   closeable_sheet(ob)
   sol=ob.modifiers.new('Door molding gauge','SOLIDIFY');sol.thickness=.003;sol.offset=-1;G.apply(ob);b.add(ob,bpy.data.objects['Door_'+end+label],category='cladding')
  # Low capped rails follow the roof and sit on broad molded end feet.
  rail=[]
  for i in range(17):
   t=i/16;y=.04+1.47*t;p=tree.ray_cast(Vector((sgn*.620,y,3)),Vector((0,0,-1)),3)[0]
   from suv_body import smoothstep
   height=.032*min(smoothstep(0,.18,t),smoothstep(0,.18,1-t))+.009
   rail.append((sgn*.620,y,min(1.689,p.z+height)))
  b.add(G.tube('Roof rail_'+label,rail,.011,b.m['bumper'],8),category='rails')
  for end in [0,1]:
   loops=[]
   for i in range(7):
    y=.035+.235*i/6 if end==0 else 1.285+.235*i/6
    p=tree.ray_cast(Vector((sgn*.620,y,3)),Vector((0,0,-1)),3)[0]
    z=min(rail,key=lambda q:abs(q[1]-y))[2]
    loops.append([(sgn*.620+dx,y,p.z+dz) for dx,dz in [(-.024,0),(.024,0),(.016,z-p.z+.006),(-.016,z-p.z+.006)]])
   b.add(G.loft('Rail foot_'+label+str(end),loops,b.m['rubber']),category='rails')
 # Small skid finishes follow both chins rather than hang as flat plates.
 from suv_body import form_blank,locator_y_guess
 for front in [True,False]:
  rows=[]
  for j in range(4):
   z=(.306 if front else .368)+.055*j/3
   rows.append([(x,locator_y_guess(x,z,front),z) for x in [-.46+i*.92/16 for i in range(17)]])
  skid=form_blank(('Chin' if front else 'Rear')+' skid finish',rows,b.m['bumper'],tree,front);b.add(skid,category='cladding')
 # Molded upper/lower skin with downward end caps: seated across the roof end.
 # It is a closed section, not a thin board suspended over the backlight.
 rings=[];count=25
 for i in range(count):
  u=2*i/(count-1)-1;x=.755*u;end=abs(u)**8
  crown=.018*u*u;front=1.755-.075*end;rear=2.025-.115*abs(u)**4
  p=tree.ray_cast(Vector((x,front,3)),Vector((0,0,-1)),3)[0]
  root=p.z if p else 1.620-crown
  top=1.644-crown-.052*end
  rings.append([(x,front,root-.004),(x,front+.045,root+.009),
    (x,rear-.035,top+.009),(x,rear,top-.004),(x,rear-.012,top-.023),
    (x,front+.115,root-.015)])
 spoiler=G.loft('Liftgate spoiler',rings,b.m['body']);b.add(spoiler,bpy.data.objects['Liftgate'],category='spoiler')
 # The stop-light blank is integrated into the aft molded section.
 rings=[]
 for i in range(17):
  x=-.25+.5*i/16;y=2.025-.115*(abs(x)/.755)**4;z=1.644-.018*(x/.755)**2
  rings.append([(x,y-.008,z-.015),(x,y+.001,z-.015),(x,y+.001,z-.003),(x,y-.008,z-.003)])
 b.add(G.loft('Spoiler brake lamp',rings,b.m['glass']),bpy.data.objects['Liftgate'],category='spoiler')
