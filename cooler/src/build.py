"""Rill C48: original insulated rotomolded cooler, measured in meters."""
import sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
import bpy,bmesh
from mathutils import Matrix
from kit import model as G,materials as M
from kit.prop import arguments,Build
from finishes import polyethylene

a=arguments();b=Build('Cooler',a.quality,a.wear);hi=b.high;n=6 if hi else 3
bodymat=polyethylene('Rill teal molded polyethylene',a.wear,brand='build/markings/mold.png')
lidmat=polyethylene('Rill flax insulated lid',a.wear,lid=True)
rubber=M.surface('Charcoal silicone elastomer','rubber',a.wear,color=(.013,.017,.016),roughness=.73,grime=.2)
steel=M.surface('Satin stainless hinge pins','stainless',a.wear,roughness=.48)

def rect(w,d,r,z):return [(x,y,z) for x,y in G.rounded_rectangle(w,d,r,n)]
def box(name,c,s,mat,parent=None,r=.003):
 # Matching bevel topology preserves smooth small mount normals through the bake.
 segments=2 if name.startswith(('Latch mounting','Body latch reaction','Molded base runner')) else (3 if hi else 1)
 return b.add(G.box(name,c,s,mat,r,segments),parent)
def pivot(name,p,axis,limits,parent=None):
 o=G.pivot(name,p,axis,limits);o.parent=parent or b.root;bpy.context.view_layer.update();o.matrix_world=Matrix.Translation(p);return o
# A closed vessel: outer floor, tapered outside, rounded shoulder, rim and inner cavity.
loops=[rect(.592,.340,.038,.020),rect(.612,.360,.043,.032),rect(.616,.364,.043,.055),rect(.658,.404,.046,.335),rect(.658,.404,.046,.350),rect(.648,.394,.041,.360),rect(.555,.305,.027,.360),rect(.550,.300,.026,.349),rect(.520,.270,.025,.075),rect(.510,.260,.025,.065)]
body=G.loft('Insulated hollow rotomolded body',loops,bodymat,caps=True)
# Actual side hand recesses leave about 26 mm of inner insulation behind the grip.
for s in (-1,1):
 points=[(y,z+.283) for y,z in G.rounded_rectangle(.198,.050,.018,5 if hi else 3)]
 cutter=G.profile('Grip recess cutter',points,min(s*.350,s*.301),max(s*.350,s*.301),bodymat,axis='X')
 G.boolean(body,cutter)
# One real drain bore connects the low cavity to the right end.
G.boolean(body,G.cylinder('Drain drilling',(.245,.10,.079),(.36,.10,.079),.009,bodymat,24 if hi else 12))
G.smooth(body,45);b.add(body)
# Rubber feet are solid pads overlapping the lower shell, with true ground contact.
for sx in (-1,1):
 for sy in (-1,1):box(f'Rubber foot {sx} {sy}',(sx*.263,sy*.135,.014),(.075,.058,.028),rubber,r=.008)
# Continuous molded insulation lid, with rolled outside crown and recessed top panel.
lid=pivot('Lid',(0,.225,.365),'X',(-108,0))
loops=[rect(.6531,.3991,.037,.365),rect(.6731,.4191,.042,.375),rect(.6731,.4191,.042,.406),rect(.6591,.4051,.038,.4191),rect(.595,.341,.030,.4191),rect(.583,.329,.027,.414)]
b.add(G.smooth(G.loft('Insulated stepped lid crown',loops,lidmat,caps=True),42),lid)
# Inner plug has clearance from the cavity; gasket rests on the actual mouth plane.
box('Lid interior insulation plug',(0,0,.361),(.534,.284,.012),lidmat,lid,r=.012)
gasket=[rect(.611,.361,.032,.360),rect(.611,.361,.032,.365),rect(.581,.331,.027,.365),rect(.581,.331,.027,.360)]
b.add(G.ring_loft('Continuous freezer gasket',gasket,rubber),lid)
# Alternating bored sleeves and secured pins on the outboard rear axis.
for s in (-1,1):
 x=s*.215
 ob=G.box('Body hinge bridge '+str(s),(x,.208,.345),(.045,.036,.036),bodymat,.006,3 if hi else 1)
 G.boolean(ob,G.cylinder('Fixed bridge axle bore',(x-.04,.225,.365),(x+.04,.225,.365),.0065,steel,24 if hi else 12));b.add(ob)
 ob=G.box('Lid hinge bridge '+str(s),(x-s*.040,.208,.378),(.032,.038,.025),lidmat,.004,3 if hi else 1)
 G.boolean(ob,G.cylinder('Moving bridge axle bore',(x-s*.040-.03,.225,.365),(x-s*.040+.03,.225,.365),.0065,steel,24 if hi else 12));b.add(ob,lid)
 for name,cx,length,parent in [('Body bearing',x,.042,b.root),('Lid bearing',x-s*.040,.032,lid)]:
  b.add(G.lathe(name+' '+str(s),[(cx-length/2,.0064),(cx-length/2,.012),(cx+length/2,.012),(cx+length/2,.0064)],lidmat if parent==lid else bodymat,24 if hi else 12,axis='X',center=(.225,.365),closed=True),parent)
 b.add(G.cylinder('Secured hinge pin '+str(s),(s*.145,.225,.365),(s*.242,.225,.365),.006,steel,16 if hi else 8))
# Two lid-mounted T-latches. Both are released before the lid sweep.
for s in (-1,1):
 x=s*.218;hinge=(x,-.224,.388)
 for e in (-1,1):box('Latch mounting ear '+str(s)+' '+str(e),(x+e*.023,-.213,.388),(.014,.028,.028),lidmat,lid,r=.004)
 b.add(G.cylinder('Latch captive pin '+str(s),(x-.026,-.224,.388),(x+.026,-.224,.388),.004,steel,16 if hi else 8),lid)
 latch=pivot('Latch_'+('L' if s<0 else 'R'),hinge,'X',(-90,0),lid)
 b.add(G.lathe('Rubber latch eye '+str(s),[(x-.014,.0044),(x-.014,.009),(x+.014,.009),(x+.014,.0044)],rubber,20 if hi else 10,axis='X',center=(-.224,.388),closed=True),latch)
 # Thick molded dog-bone strap, not a flat rectangular plate.
 outline=[(-.014,.384),(.014,.384),(.012,.356),(.010,.338),(.016,.320),(.012,.306),(.012,.286),(.035,.286),(.039,.278),(.033,.267),(-.033,.267),(-.039,.278),(-.035,.286),(-.012,.286),(-.012,.306),(-.016,.320),(-.010,.338),(-.012,.356)]
 outline=[(xx+x,z) for xx,z in outline]
 ob=G.profile('Rubber T latch '+str(s),outline,-.235,-.222,rubber,axis='Y',radius=.002,segments=3 if hi else 1);G.smooth(ob,42);b.add(ob,latch)
 box('Body latch reaction lug '+str(s),(x,-.207,.304),(.034,.032,.027),bodymat,r=.005)
# Drain seat extends through the wall; cap has its own removable-axis origin.
seat=[(.260,.009),(.260,.012),(.325,.012),(.330,.018),(.335,.018),(.335,.009)]
b.add(G.lathe('Threaded drain seat',seat,rubber,32 if hi else 16,axis='X',center=(.10,.079),closed=True))
plug=pivot('Drain_Plug',(.336,.10,.079),'X',(0,360))
b.add(G.lathe('Drain plug cap',[(.329,0),(.329,.0084),(.337,.0084),(.337,.024),(.349,.024),(.352,.021),(.352,0)],rubber,32 if hi else 16,axis='X',center=(.10,.079)),plug)
for j in range(6):
 ang=j*math.tau/6;y=.10+.018*math.cos(ang);z=.079+.018*math.sin(ang)
 ob=G.box('Drain cap finger scallop',(.348,y,z),(.009,.010,.007),rubber,.001,2 if hi else 1);ob.rotation_euler.x=ang;b.add(ob,plug)
# Low molded plinth ribs strengthen the corners and carry the feet.
for s in (-1,1):
 for y in (-.147,.147):box('Molded base runner',(s*.263,y,.034),(.09,.045,.029),bodymat,r=.006)
# Fine source-only parting line and lid grip emboss go into the normal map.
if hi:
 for s in (-1,1):
  b.add(G.tube('Mold parting witness',[(s*(w/2-r+r/math.sqrt(2)),-d/2+r-r/math.sqrt(2),z) for z,w,d,r in [(.055,.616,.364,.043),(.335,.658,.404,.046)]],.00018,bodymat,5))
b.save(a.out,a.quality)
