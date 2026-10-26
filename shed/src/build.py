"""Hearthfield 810: framed, gauged, original procedural backyard shed."""
import sys,math,random
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G
from kit.prop import Build,arguments
from kit.materials import surface,galvanized,weathered_wood
from dimensions import *
from finishes import wood,shingles

class Shed(Build):
 def __init__(self,a):
  super().__init__('Shed',a.quality,a.wear)
  self.timber={k:wood('Sawn framing '+k,a.wear*.35,k) for k in 'XYZ'}
  self.paint=wood('Chalked sage T1-11',a.wear,paint=(.19,.255,.19))
  self.trim=wood('Aged warm white trim',a.wear,paint=(.69,.665,.56),trim=True)
  self.trims={k:wood('Warm white trim grain '+k,a.wear,k,paint=(.69,.665,.56),trim=True) for k in 'XYZ'}
  self.grade=G.pivot('Grade weather frame',(0,0,0));self.grade.parent=self.root
  self.pt=object();self.pt_seed=810
  self.floor=wood('Plywood floor / foot lane',a.wear,'Y',floor=True)
  self.back=wood('Unpainted plywood back',a.wear*.2)
  self.roof=shingles(a.wear)
  self.cap=shingles(a.wear,cap=True)
  self.underlay=surface('Asphalt felt under shingles','rubber',0,color=(.003,.004,.003),roughness=.96)
  self.zinc=galvanized('Drip edge zinc',wear=a.wear)
  self.iron=surface('Blackened strap hardware','paint',a.wear,color=(.023,.026,.025),roughness=.6,grime=.22)
  self.glass=surface('Slightly dusty window glass','plastic',a.wear,color=(.32,.38,.35),roughness=.23,dust=.15)
 def box(self,n,p,s,m=None,pa=None,r=0):
  if m==self.trim:m=self.trims['XYZ'[max(range(3),key=lambda k:s[k])]]
  if m==self.pt:
   # A separate stable source frame follows each timber's actual long axis.
   axis=max(range(3),key=lambda k:s[k]);direction=Vector(tuple(int(k==axis) for k in range(3)))
   frame=G.pivot(n+' grain frame',Vector(p)-direction*s[axis]/2);frame.parent=self.root
   frame.rotation_euler=direction.to_track_quat('Z','Y').to_euler()
   self.pt_seed+=1
   m=weathered_wood(n+' gray-brown treated pine',frame,width=max(s[k] for k in range(3) if k!=axis),length=s[axis],seed=self.pt_seed,wear=self.wear,ground_frame=self.grade)
  return self.add(G.box(n,p,s,m or self.timber['Z'],r if self.high else 0,2),pa)
 def beam(self,n,a,b,width=.0381,depth=.0889,mat=None,pa=None):
  a,b=Vector(a),Vector(b);ob=G.box(n,(a+b)/2,(width,depth,(b-a).length),mat or self.timber['Z'],.0006 if self.high else 0,2)
  ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return self.add(ob,pa)
 def skin(self,n,points,lo,hi,axis='Y',pa=None):
  ob=G.profile(n,points,lo,hi,self.paint,axis=axis)
  ob.data.materials.append(self.back)
  # Interior back gets exposed plywood instead of exterior paint.
  for p in ob.data.polygons:
   v=p.normal[1 if axis=='Y' else 0]
   inner=(v>0 if hi<0 else v<0)
   if inner:p.material_index=1
  return self.add(ob,pa)

def floor(b):
 for x in (-.78,.78):b.box('PT 4x4 skid',(x,0,SKID/2), (SKID,D,SKID),b.pt)
 for x in (-W/2+STUD/2,W/2-STUD/2):b.box('PT rim joist',(x,0,SKID+JOIST/2),(STUD,D,JOIST),b.pt)
 for i,y in enumerate([-D/2+STUD/2]+[-D/2+i*.4064 for i in range(1,8)]+[D/2-STUD/2]):
  if abs(y)>D/2:continue
  b.box('PT floor joist %02d'%i,(0,y,SKID+JOIST/2),(W-2*STUD,STUD,JOIST),b.timber['X'])
 # Three physical deck sheets; seams lie over the joist grid.
 for i,(y0,y1) in enumerate([(-D/2,-.3048),(-.3048,.9144),(.9144,D/2)]):
  b.box('Floor plywood sheet '+str(i),(0,(y0+y1)/2,DECK-FLOOR/2),(W,y1-y0-.001,FLOOR),b.floor)
 b.box('Worn threshold',(0,-D/2-.015,DECK+.003),(DOOR_W,.135,.006),b.floor)

def walls(b):
 z0=DECK;zt=EAVE
 for s in (-1,1):
  x=s*(W/2-WALL/2)
  for z in (z0+STUD/2,zt-STUD/2,zt-1.5*STUD):b.box('Side wall plate',(x,0,z),(WALL,D-2*WALL,STUD),b.timber['Y'])
  for i,y in enumerate([-D/2+WALL]+[-D/2+.4064*i for i in range(1,8)]+[D/2-WALL]):
   if y>D/2-WALL:continue
   if s==1 and abs(y-WIN_Y)<WIN_W/2+STUD:continue
   b.box('Side stud %d %d'%(s,i),(x,y,(z0+STUD+zt-2*STUD)/2),(WALL,STUD,WALL_H-3*STUD))
  # Siding rectangle split physically around the right-hand window opening.
  if s<0:rects=[(-D/2,D/2,z0-.12,zt)]
  else:rects=[(-D/2,WIN_Y-WIN_W/2,z0-.12,zt),(WIN_Y+WIN_W/2,D/2,z0-.12,zt),(WIN_Y-WIN_W/2,WIN_Y+WIN_W/2,z0-.12,WIN_Z-WIN_H/2),(WIN_Y-WIN_W/2,WIN_Y+WIN_W/2,WIN_Z+WIN_H/2,zt)]
  lo,hi=sorted((s*W/2,s*(W/2+SIDING)))
  for j,(a,c,d,e) in enumerate(rects):b.skin('Side T1-11 panel %d %d'%(s,j),[(a,d),(c,d),(c,e),(a,e)],lo,hi,'X')
  # Corner boards wrap the real edge with two legs, no floating corner posts.
  for y in (-D/2,D/2):b.box('Side corner trim',(s*(W/2+SIDING+.0095),y, (z0-.12+zt)/2),(.019,.089,zt-z0+.12),b.trim)
  b.box('Splash dirtied side skirt',(s*(W/2+SIDING+.0095),0,z0-.075),(.019,D,.089),b.trim)
 # End frames and gables. Door cutout is a true opening.
 for s in (-1,1):
  y=s*(D/2-WALL/2)
  for z in (zt-STUD/2,zt-1.5*STUD):b.box('End wall top plate',(0,y,z),(W,WALL,STUD),b.timber['X'])
  ranges=[(-W/2,-DOOR_W/2),(DOOR_W/2,W/2)] if s<0 else [(-W/2,W/2)]
  for lo,hi in ranges:b.box('End bottom plate',((lo+hi)/2,y,z0+STUD/2),(hi-lo,WALL,STUD),b.timber['X'])
  for i,x in enumerate([-W/2+STUD/2]+[-W/2+i*.4064 for i in range(1,6)]+[W/2-STUD/2]):
   if s<0 and abs(x)<DOOR_W/2+STUD:continue
   b.box('End wall stud %d %d'%(s,i),(x,y,(z0+STUD+zt-2*STUD)/2),(STUD,WALL,WALL_H-3*STUD))
  if s<0:
   for x in (-DOOR_W/2-STUD/2,DOOR_W/2+STUD/2):b.box('Door jack stud',(x,y,(z0+DOOR_TOP)/2),(STUD,WALL,DOOR_TOP-z0))
   for x in (-DOOR_W/2-1.5*STUD,DOOR_W/2+1.5*STUD):b.box('Door king stud',(x,y,(z0+zt-2*STUD)/2),(STUD,WALL,zt-2*STUD-z0))
   b.box('Double 2x6 door header',(0,y,DOOR_TOP+.06985),(DOOR_W+2*STUD,WALL,.1397),b.timber['X'])
   for x in (-.60,0,.60):b.box('Header cripple',(x,y,(DOOR_TOP+.1397+zt-2*STUD)/2),(STUD,WALL,zt-2*STUD-DOOR_TOP-.1397))
  lo,hi=sorted((s*D/2,s*(D/2+SIDING)))
  polys=[ [(-W/2,z0-.12),(-DOOR_W/2,z0-.12),(-DOOR_W/2,DOOR_TOP),(-W/2,DOOR_TOP)],[(DOOR_W/2,z0-.12),(W/2,z0-.12),(W/2,DOOR_TOP),(DOOR_W/2,DOOR_TOP)], [(-W/2,DOOR_TOP),(W/2,DOOR_TOP),(W/2,zt),(-W/2,zt)] ] if s<0 else [[(-W/2,z0-.12),(W/2,z0-.12),(W/2,zt),(-W/2,zt)]]
  polys += [[(-W/2,zt),(W/2,zt),(0,RIDGE)]]
  for i,poly in enumerate(polys):b.skin('End siding %d %d'%(s,i),poly,lo,hi)
  for x in (-W/2,W/2):b.box('End corner trim',(x,s*(D/2+SIDING+.0095),(z0-.12+zt)/2),(.089,.019,zt-z0+.12),b.trim)
  for x in (-.8128,-.4064,0,.4064,.8128):
   h=(W/2-abs(x))*PITCH-.0889
   if h>0:b.box('Gable upright',(x,y,zt+h/2),(.0381,.0889,h))
  for a,c in ranges:b.box('Splash dirtied end skirt',((a+c)/2,s*(D/2+SIDING+.010),z0-.075),(c-a,.019,.089),b.trim)
 # Trim the open door jamb without extending across the threshold.
 for x in (-DOOR_W/2-.0445,DOOR_W/2+.0445):b.box('Door casing',(x,-D/2-.031, (DOOR_TOP+DECK)/2),(.089,.03,DOOR_TOP-DECK+.01),b.trim)
 b.box('Door lintel trim',(0,-D/2-.031,DOOR_TOP+.0445),(DOOR_W+.178,.03,.089),b.trim)
 # Side window with sill, king/jack framing, recessed two-pane glazing.
 x=W/2-WALL/2
 for y in (WIN_Y-WIN_W/2-STUD/2,WIN_Y+WIN_W/2+STUD/2):
  b.box('Window king stud',(x,y,(DECK+EAVE)/2),(WALL,STUD,WALL_H-2*STUD))
 for lo,hi in [(DECK+STUD,WIN_Z-WIN_H/2-STUD),(WIN_Z+WIN_H/2+STUD,EAVE-2*STUD)]:
  b.box('Window cripple stud',(x,-D/2+4*.4064,(lo+hi)/2),(WALL,STUD,hi-lo))
 for z in (WIN_Z-WIN_H/2-STUD/2,WIN_Z+WIN_H/2+STUD/2):b.box('Window structural header sill',(x,WIN_Y,z),(WALL,WIN_W,STUD),b.timber['Y'])
 for y in (WIN_Y-WIN_W/2-.025,WIN_Y+WIN_W/2+.025):b.box('Window casing upright',(W/2+.030,y,WIN_Z),(.035,.064,WIN_H+.128),b.trim)
 for z in (WIN_Z-WIN_H/2-.025,WIN_Z+WIN_H/2+.025):b.box('Window casing horizontal',(W/2+.030,WIN_Y,z),(.035,WIN_W+.064,.064),b.trim)
 b.box('Sloped projecting window sill',(W/2+.05,WIN_Y,WIN_Z-WIN_H/2-.051),(.115,WIN_W+.17,.025),b.trim)
 b.box('Window center mullion',(W/2+.022,WIN_Y,WIN_Z),(.026,.025,WIN_H),b.trim)
 for s in (-1,1):b.box('Window glass '+str(s),(W/2+.004,WIN_Y+s*WIN_W/4,WIN_Z),(.003,WIN_W/2-.018,WIN_H-.018),b.glass)

def doors(b):
 original_paint,original_trims=b.paint,b.trims
 for sign,label in ((-1,'L'),(1,'R')):
  hx=sign*(DOOR_W/2-.002);pa=G.pivot('Door_'+label,(hx,HINGE_Y,DOOR_BOTTOM),'Z',(0,110) if sign>0 else (-110,0));pa.parent=b.root
  rest=(hx,HINGE_Y,DOOR_BOTTOM)
  b.paint=wood('Door '+label+' sage / rest exposure',b.wear,paint=(.19,.255,.19),origin=rest)
  b.trims={k:wood('Door '+label+' trim '+k,b.wear,k,paint=(.69,.665,.56),trim=True,origin=rest) for k in 'XYZ'}
  center=sign*(DOOR_W/4);width=DOOR_W/2-.008;y=-D/2-.027
  b.skin('Door plywood '+label,[(center-width/2,DOOR_BOTTOM),(center+width/2,DOOR_BOTTOM),(center+width/2,DOOR_TOP-.006),(center-width/2,DOOR_TOP-.006)],y-.009,y+.009,pa=pa)
  for x in (center-width/2+.038,center+width/2-.038):b.box('Door painted stile '+label,(x,y-.022,(DOOR_BOTTOM+DOOR_TOP)/2),(.076,.026,DOOR_TOP-DOOR_BOTTOM-.006),b.trim,pa)
  for z in (DOOR_BOTTOM+.044,DOOR_TOP-.045):b.box('Door painted rail '+label,(center,y-.022,z),(width-.15,.026,.076),b.trim,pa)
  for z in (DOOR_BOTTOM+.13,DOOR_TOP-.13):b.box('Door back rail '+label,(center,y+.035,z),(width,.045,.089),b.timber['X'],pa)
  b.beam('Door compression brace '+label,(hx-sign*.065,y+.034,DOOR_BOTTOM+.17),(sign*.067,y+.034,DOOR_TOP-.17),.07,.039,b.timber['Z'],pa)
  for j,z in enumerate((DOOR_BOTTOM+.26,DOOR_TOP-.25)):
   # Tapered strap hinge with fixed pin and open bored rotating knuckles.
   b.add(G.profile('Door hinge strap '+label+str(j),[(hx-sign*.018,z-.027),(hx-sign*.28,z-.012),(hx-sign*.28,z+.012),(hx-sign*.018,z+.027)],-D/2-.066,-D/2-.062,b.iron,'Y'),pa)
   b.box('Fixed hinge mounting leaf '+label,(hx+sign*.034,HINGE_Y+.003,z),(.048,.006,.084),b.iron)
   b.box('Fixed hinge mounting return '+label,(hx+sign*.052,HINGE_Y+.022,z),(.004,.038,.06),b.iron)
   for dz in (-.04,.04):
    b.add(G.lathe('Fixed hinge bearing '+label,[(z+dz-.006,.0033),(z+dz-.006,.007),(z+dz+.006,.007),(z+dz+.006,.0033)],b.iron,12,center=(hx,HINGE_Y),closed=True))
    b.box('Fixed bearing neck '+label,(hx+sign*.008,HINGE_Y+.004,z+dz),(.016,.004,.012),b.iron)
   b.box('Door hinge bent neck '+label,(hx-sign*.012,HINGE_Y+.008,z),(.012,.014,.040),b.iron,pa)
   b.add(G.cylinder('Fixed hinge pin '+label,(hx,HINGE_Y,z-.046),(hx,HINGE_Y,z+.046),.003,b.zinc,8))
   b.add(G.lathe('Door hinge sleeve '+label,[(z-.032,.0035),(z-.032,.007),(z+.032,.007),(z+.032,.0035)],b.iron,12,center=(hx,HINGE_Y),closed=True),pa)
   for xx in (hx-sign*.065,hx-sign*.22):
    b.add(G.cylinder('Hinge carriage bolt '+label,(xx,-D/2-.069,z),(xx,-D/2-.065,z),.0045,b.zinc,8),pa)
  # Fixed iron pull on each leaf; no separate moving object for a welded handle.
  x=sign*.075;z=DECK+1.03
  b.box('Door pull plate '+label,(x,y-.041,z),(.031,.005,.16),b.iron,pa)
  b.add(G.tube('Door pull grip '+label,[(x,y-.043,z-.05),(x,y-.080,z-.04),(x,y-.080,z+.04),(x,y-.043,z+.05)],.006,b.iron,8),pa)
 b.paint,b.trims=original_paint,original_trims

def roof(b):
 # Structural rafters at 24 inch centers, touching sheathing at actual surfaces.
 for j in range(6):
  y=-D/2+STUD/2+j*(D-STUD)/5
  b.box('Truss tie '+str(j),(0,y,EAVE-.04445),(W,.0381,.0889),b.timber['X'])
  for sign in (-1,1):
   pts=[(0,RIDGE),(sign*RX,EAVE-(RX-W/2)*PITCH),(sign*RX,EAVE-(RX-W/2)*PITCH-.0889),(0,RIDGE-.0889)]
   b.add(G.profile('Rafter %d %d'%(j,sign),pts,y-STUD/2,y+STUD/2,b.timber['X'],'Y'))
  b.add(G.profile('Plywood ridge gusset '+str(j),[(-.21,RIDGE-.14),(.21,RIDGE-.14),(0,RIDGE)],y+.0191,y+.0318,b.back,'Y'))
 for sign in (-1,1):
  # Sheathing full gauged plywood underside.
  pts=[(0,RIDGE),(sign*RX,RIDGE-RX*PITCH),(sign*RX,RIDGE-RX*PITCH+.0127),(0,RIDGE+.0127)]
  sheathing=G.profile('Roof plywood sheathing '+str(sign),pts,-RY,RY,b.back,'Y')
  # The visible slot bottoms are black felt/headlap, never pale roof plywood.
  # Reuse the upper deck face; its underside and cut edges stay raw plywood.
  sheathing.data.materials.append(b.underlay)
  for face in sheathing.data.polygons:
   if face.normal.z>.5:face.material_index=1
  b.add(sheathing)
  # Eave fascia and drip edge, with an outward hem.
  z=RIDGE-RX*PITCH
  b.box('Eave fascia '+str(sign),(sign*(RX-.013),0,z-.052),(.026,RY*2,.104),b.trim)
  b.box('Galvanized eave drip '+str(sign),(sign*(RX+.002),0,z+.003),(.010,RY*2,.029),b.zinc)
  for y in (-RY,RY):
   b.add(G.profile('Rake fascia',[(0,RIDGE),(sign*RX,z),(sign*RX,z-.108),(0,RIDGE-.108)],y-.012,y+.012,b.trim,'Y'))
  # Three-tab courses: exposed tabs are real gauged slabs; sparse ends lift.
  rng=random.Random(810+sign)
  rows=12;step=RX/rows
  for row in range(rows):
   xa=RX-row*step;xb=max(0,xa-step-.016)
   cuts=[-RY]+[v for v in [-RY+(.1524 if row%2 else .3048)+i*.3048 for i in range(12)] if -RY<v<RY]+[RY]
   for k,(ya,yb) in enumerate(zip(cuts,cuts[1:])):
    ya+=.003;yb-=.003
    if yb<=ya:continue
    lift=(.008+rng.random()*.014) if rng.random()<.065 and row<6 else .0008*rng.random()
    # Top/end five-point section introduces an actual curled exposed lip.
    base=.017+row*.001
    points=[(sign*xb,RIDGE-xb*PITCH+base),(sign*(xa-.018),RIDGE-(xa-.018)*PITCH+base),(sign*xa,RIDGE-xa*PITCH+base+lift),(sign*xa,RIDGE-xa*PITCH+base+lift-.003),(sign*(xa-.018),RIDGE-(xa-.018)*PITCH+base-.003),(sign*xb,RIDGE-xb*PITCH+base-.003)]
    b.add(G.profile('Shingle tab %d %02d %02d'%(sign,row,k),points,ya,yb,b.roof,'Y'))
 # Lapped ridge cap sections, original profile.
 for j in range(12):
  ya=-RY+j*(RY*2/12);yb=ya+RY*2/12-.001
  b.add(G.profile('Folded ridge cap '+str(j),[(-.13,RIDGE-.065+.04),(0,RIDGE+.043),(.13,RIDGE-.065+.04),(.13,RIDGE-.065+.036),(0,RIDGE+.039),(-.13,RIDGE-.065+.036)],ya,yb,b.cap,'Y'))

def main():
 a=arguments();b=Shed(a);floor(b);walls(b);doors(b);roof(b);b.save(a.out,a.quality)
if __name__=='__main__':main()
