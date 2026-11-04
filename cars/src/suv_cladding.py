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
   count=64 if b.high else 32
   angles=[-.115+(math.pi+.230)*i/count for i in range(count+1)];nu=len(angles);verts=[]
   for width,proud in [(0,.010),(.008,.0225),(.045,.0205),(.060,.004)]:
    for a in angles:
     y,z=arch_point(a,axle,width);p=tree.ray_cast(Vector((sgn*2,y,z)),Vector((-sgn,0,0)),3)[0]
     x=abs(p.x) if p else .896
     verts.append((sgn*(x+proud),y,z))
   fs=[(j*nu+i,j*nu+i+1,(j+1)*nu+i+1,(j+1)*nu+i) for j in range(3) for i in range(nu-1)]
   ob=G.mesh('Arch cladding_'+end+label,verts,fs,b.m['rubber']);sol=ob.modifiers.new('Injection molded gauge','SOLIDIFY');sol.thickness=.003;sol.offset=-1;G.apply(ob);b.add(ob,category='cladding')
   # Inner flange is visibly turned into each opening, with a 22 mm return.
   ring=verts[:nu];inner=[(x-sgn*.022,y,z) for x,y,z in ring]
   ob=G.mesh('Arch flange_'+end+label,ring+inner,[(i,i+1,nu+i+1,nu+i) for i in range(nu-1)],b.m['rubber']);sol=ob.modifiers.new('Flange gauge','SOLIDIFY');sol.thickness=.002;G.apply(ob);b.add(ob,category='cladding')
  for end,ya,yb in [('F',S.DOOR_FRONT+.004,S.DOOR_SPLIT-.004),('R',S.DOOR_SPLIT+.004,S.DOOR_REAR-.004)]:
   verts=[];n=16
   for z,d in [(.285,.003),(.304,.006),(.415,.007),(.440,.003)]:
    for i in range(n+1):
     y=ya+(yb-ya)*i/n;p=tree.ray_cast(Vector((sgn*2,y,z)),Vector((-sgn,0,0)),3)[0]
     x=abs(p.x) if p else .81;verts.append((sgn*(x+d),y,z))
   ob=G.mesh('Lower door cladding_'+end+label,verts,[(j*(n+1)+i,j*(n+1)+i+1,(j+1)*(n+1)+i+1,(j+1)*(n+1)+i) for j in range(3) for i in range(n)],b.m['rubber'])
   for axle in [S.FRONT_AXLE,S.REAR_AXLE]:trim_arch(ob,axle,96 if b.high else 64)
   closeable_sheet(ob)
   sol=ob.modifiers.new('Door molding gauge','SOLIDIFY');sol.thickness=.003;sol.offset=-1;G.apply(ob);b.add(ob,bpy.data.objects['Door_'+end+label],category='cladding')
  # Low longitudinal rails have real feet seated on the roof, no floating bars.
  rail=[]
  for i in range(13):
   y=-.10+1.63*i/12;p=tree.ray_cast(Vector((sgn*.680,y,3)),Vector((0,0,-1)),3)[0]
   if p:rail.append((sgn*.680,y,1.687-.007*((y-.7)/.85)**2))
  b.add(G.tube('Roof rail_'+label,rail,.013,b.m['bumper'],8),category='rails')
  for i in [1,6,11]:
   x,y,z=rail[i];b.add(G.box('Rail foot_'+label+str(i),(x,y,z-.025),(.036,.085,.055),b.m['rubber'],.008,1),category='rails')
 # A separate small satin skid finish follows the chin's actual crown.
 from suv_body import form_blank,locator_y_guess
 rows=[]
 for j in range(4):
  z=.335+.052*j/3
  rows.append([(x,locator_y_guess(x,z,True),z) for x in [-.45+i*.90/12 for i in range(13)]])
 skid=form_blank('Chin skid finish',rows,b.m['bumper'],tree,True);b.add(skid,category='cladding')
 # Original low spoiler extends aft from the top of the gate, gently crowned.
 verts=[]
 for y,z in [(1.81,1.625),(1.88,1.651),(1.97,1.641),(1.99,1.625)]:
  for i in range(17):
   x=(i/8-1)*.70;verts.append((x,y-.06*(abs(x)/.7)**3,z-.018*(x/.7)**2))
 ob=G.mesh('Liftgate spoiler',verts,[(j*17+i,j*17+i+1,(j+1)*17+i+1,(j+1)*17+i) for j in range(3) for i in range(16)],b.m['body']);sol=ob.modifiers.new('Spoiler gauge','SOLIDIFY');sol.thickness=.009;sol.offset=-1;G.apply(ob);b.add(ob,bpy.data.objects['Liftgate'],category='spoiler')
