"""Additive arterial checkpoint modules; never opens or overwrites native deliveries.

Uses native Ground GLB material bytes; newly authored crowned skins and simple
marking decals stay in ArterialCheckpoint.glb. Native curb/ramp/walks are placed
unscaled around its wider ports by the signals presentation.
"""
import math,sys,json,argparse
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import model as G
from kit.tiling import world_uv
LANE=3.3528;HALF=LANE*1.5;FACE=HALF+.4572;CORE=FACE+4.572
def road_z(x):return .00635+(HALF-abs(x))/48
def junction_z(x,y):return .00635+min(HALF,max(0,math.hypot(CORE-abs(x),CORE-abs(y))-5.0292))/48
def make():
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.gltf(filepath=str((ROOT/'ground/export/Ground.glb').resolve()))
 asphalt=next(m for m in bpy.data.materials if m.name=='Asphalt')
 for o in list(bpy.context.scene.objects):bpy.data.objects.remove(o,do_unlink=True)
 def mat(name,c):
  m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.85;return m
 white=mat('Arterial_White_Form',(.64,.64,.59));yellow=mat('Arterial_Yellow_Form',(.63,.40,.015));seal=mat('Arterial_Sealant_Form',(.014,.014,.013))
 def rt(name):return G.pivot(name,(0,0,0))
 def mesh(name,v,f,ma,r):
  o=G.mesh(name,v,f,ma);o.parent=r;world_uv(o,6.096)
  # Imported asphalt consumes tint; neutral white leaves canonical maps intact.
  if ma==asphalt:
   ca=o.data.color_attributes.new(name='Color',type='FLOAT_COLOR',domain='POINT')
   for value in ca.data:value.color=(1,1,1,1)
  return o
 def grid(name,xs,ys,fn,ma,r):
  v=[(x,y,fn(x,y)) for y in ys for x in xs];f=[];n=len(xs)
  for j in range(len(ys)-1):
   for i in range(n-1):
    a=j*n+i;f.extend([(a,a+1,a+n+1),(a,a+n+1,a+n)])
  return mesh(name,v,f,ma,r)
 def seq(a,b,n):return [a+(b-a)*i/n for i in range(n+1)]
 road=rt('Road_Arterial_3Lane')
 grid('Three eleven-foot lanes',seq(-HALF,HALF,12),[-3.048,3.048],lambda x,y:road_z(x),asphalt,road)
 junction=rt('Road_Arterial_Intersection')
 grid('Crowned arterial center',seq(-HALF,HALF,12),seq(-HALF,HALF,12),junction_z,asphalt,junction)
 for turn in range(4):
  c,s=math.cos(turn*math.pi/2),math.sin(turn*math.pi/2)
  # Arm rectangle.
  vs=[(x*c-y*s,x*s+y*c,junction_z(x*c-y*s,x*s+y*c)) for y in seq(HALF,CORE,6) for x in seq(-HALF,HALF,12)]
  fs=[]
  for j in range(6):
   for i in range(12):
    a=j*13+i;fs.extend([(a,a+1,a+14),(a,a+14,a+13)])
  mesh('Arterial junction arm',vs,fs,asphalt,junction)
  vs=[(HALF,HALF,junction_z(HALF,HALF))];fs=[]
  for level in range(1,7):
   for a in seq(0,math.pi/2,24):
    x=HALF+(CORE-5.0292*math.cos(a)-HALF)*level/6
    y=HALF+(CORE-5.0292*math.sin(a)-HALF)*level/6
    vs.append((x,y,junction_z(x,y)))
  for i in range(24):fs.append((0,i+2,i+1))
  for j in range(5):
   for i in range(24):
    a=1+j*25+i;fs.extend([(a,a+1,a+26),(a,a+26,a+25)])
  vs=[(x*c-y*s,x*s+y*c,z) for x,y,z in vs]
  mesh('Arterial rounded return',vs,fs,asphalt,junction)
 # Decal cards follow the crown's X break, without volume/wasted undersides.
 def card(r,name,x0,x1,y0,y1,ma):
  return grid(name,sorted(set([x0,x1]+([0] if x0<0<x1 else []))),[y0,y1],lambda x,y:road_z(x)+.002,ma,r)
 lines=rt('Markings_Arterial_Lanes')
 for x in (-LANE/2-.085,-LANE/2+.085):card(lines,'Double yellow',x-.05,x+.05,-3.048,3.048,yellow)
 card(lines,'Inbound lane dash',LANE/2-.05,LANE/2+.05,-1.524,1.524,white)
 stop=rt('Markings_Arterial_Stop')
 card(stop,'Twenty-four-inch stop bar',-LANE/2,HALF,-.3048,.3048,white)
 crossing=rt('Markings_Arterial_Crosswalk')
 for x in seq(-HALF+.2286,HALF-.2286,11):
  card(crossing,'High visibility bar',x-.2286,x+.2286,-.9144,.9144,white)
 for label,left in [('Markings_Arterial_LeftArrow',True),('Markings_Arterial_ThroughArrow',False)]:
  r=rt(label)
  pts=[(-.10,-1.50),(.10,-1.50),(.10,.50),(.48,.50),(0,1.50),(-.48,.50),(-.10,.50)] if not left else [(-.10,-1.50),(.10,-1.50),(.10,.40),(-.10,.70),(-.60,.70),(-.60,1.05),(-1.50,.60),(-.60,.15),(-.60,.50),(-.10,.50)]
  mesh('Original geometric lane arrow',[(x,y,road_z(x)+.003) for x,y in pts],[tuple(range(len(pts)))],white,r)
 loop=rt('Decal_DetectorLoop')
 # 6 foot square, 45 degree clipped corners, 10 mm sealed saw cut.
 path=[(-.9144,-.70),(-.70,-.9144),(.70,-.9144),(.9144,-.70),(.9144,.70),(.70,.9144),(-.70,.9144),(-.9144,.70),(-.9144,-.70)]
 for a,b in zip(path,path[1:]):
  dx,dy=b[0]-a[0],b[1]-a[1];ll=math.hypot(dx,dy);ox,oy=-dy/ll*.005,dx/ll*.005
  vs=[(x,y,road_z(x)+.002) for x,y in [(a[0]+ox,a[1]+oy),(a[0]-ox,a[1]-oy),(b[0]-ox,b[1]-oy),(b[0]+ox,b[1]+oy)]]
  mesh('Sealed saw cut',vs,[(0,1,2,3)],seal,loop)
 card(loop,'Loop lead-in',-.005,.005,-2.20,-.9144,seal)
 roots=[o for o in bpy.context.scene.objects if o.parent is None]
 for i,r in enumerate(roots):
  r['port_width_m']=HALF*2;r['checkpoint']=True;r.location=(i*25,0,0)
  for o in r.children_recursive:
   if o.type=='MESH':G.apply(o);o.data.calc_loop_triangles()
 (ROOT/'ground/export').mkdir(exist_ok=True)
 bpy.ops.export_scene.gltf(filepath=str(ROOT/'ground/export/ArterialCheckpoint.glb'),export_format='GLB',export_extras=True)
 print('ARTERIAL checkpoint modules',len(roots))
if __name__=='__main__':make()
