"""Shared Ground turf grain with locally authored summer color and rooted verge.

As in school's lawn, broad physical color stations follow drainage, exposure
and root shade. Blade relief/ORM remain the unmodified baked Ground resources.
"""
import math,json,hashlib,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.image_io import srgb_to_linear,linear_to_srgb,write_png

def field():
 source=ROOT/'ground/textures/ship/T_Lawn_BaseColor.png';path=Path('textures/context/T_FreewaySummerGrass_BaseColor.png');receipt=path.with_suffix('.json')
 sig=dict(native_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),recipe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 if path.exists() and receipt.exists() and json.loads(receipt.read_text()).get('inputs')==sig:return path
 rgb=srgb_to_linear(np.asarray(Image.open(source).convert('RGB'),np.float32)/255)
 # This derivative changes the original scripted lawn's seasonal pigment,
 # retaining the original fine blade/grain pattern. It contains no macro age.
 median=np.median(rgb.reshape(-1,3),axis=0);rgb=np.clip(rgb/median*np.array([.125,.155,.055]),0,1)
 path.parent.mkdir(parents=True,exist_ok=True);write_png(path,linear_to_srgb(rgb),bits=8)
 receipt.write_text(json.dumps(dict(inputs=sig,output_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),scope='Seasonal derivative of original Ground manufacture; same canonical normal/ORM and 2048 allocation'),indent=2));return path

def install():
 import bpy,geom as Q
 path=field();ma=Q.M['Lawn'].copy();ma.name='Freeway summer turf / Ground lawn relief'
 bs=ma.node_tree.nodes.get('Principled BSDF');base=next(n for n in ma.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and 'BaseColor' in n.image.name)
 base.image=bpy.data.images.load(str(path.resolve()),check_existing=True)
 ma.use_backface_culling=False # Rooted blades share the turf images.
 Q.M['Lawn']=ma

def lawn_tint(x,y,kind='verge',seed=0,height=0):
 # Changes are slow in station, and connected to dry high shoulders or yard
 # irrigation/root competition. Texture grain supplies the small variation.
 phase=.5+.26*math.sin(y*.061+math.sin(x*.11)+seed)+.17*math.sin(y*.19+x*.087)
 dry=max(0,min(1,.20+.64*phase if kind=='verge' else .06+.36*phase))
 if kind=='verge':dry=min(1,dry+.16*max(0,min(1,height/7)))
 if kind=='ditch':dry*=.15
 if kind=='unmown':dry=max(.50,dry)
 rootshade=.94+.04*math.sin(x*.18+math.sin(y*.16))+.02*math.sin(y*.73+x*.31)
 return ((.80+.18*dry)*rootshade,(.93-.26*dry)*rootshade,(.94-.37*dry)*rootshade,1)

def verges(p,parent):
 """Small rooted blades/seed stems in the separately counted context package."""
 import random
 import geom as Q
 from roadside import soil_tree
 from mathutils import Vector
 from mathutils.bvhtree import BVHTree
 import bpy
 # Reject a root beneath an actual pavement face. Ramps climb above the
 # earth BVH, so a terrain-only sample otherwise grows grass through asphalt.
 vertices=[];faces=[]
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH':continue
  root=ob
  while root.parent:root=root.parent
  if root.get('module_kind') not in ('roadway','ramp','arterial'):continue
  if root.name in ('RoadStraight','RoadCurve','RoadBankTransition','RampBranch'):continue
  offset=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices)
  ob.data.calc_loop_triangles()
  for face in ob.data.loop_triangles:
   if ob.data.materials[face.material_index] not in (Q.M['Asphalt'],Q.M['Concrete'],Q.M.get('WheelPolish')):continue
   pts=[vertices[offset+i] for i in face.vertices]
   if (pts[1]-pts[0]).cross(pts[2]-pts[0]).z>0:faces.append(tuple(offset+i for i in face.vertices))
 paving=BVHTree.FromPolygons(vertices,faces,all_triangles=True)
 soil=soil_tree();rng=random.Random(p.seed+919);b=Q.Batch('Rooted summer verge and unmown seed stems',parent)
 for side in (-1,1):
  for j in range(round(p.length/.8)):
   s=-p.length/2+(j+.5)*.8
   limit=43 if p.kind=='diamond' else 28
   u=side*(p.edge+rng.uniform(.6,1.35) if j%3==0 else limit+rng.uniform(-1.3,3.4))
   x,y,_=p.xyz(s,u);q=soil.ray_cast(Vector((x,y,30)),Vector((0,0,-1)),60)[0]
   if q is None:continue
   if any(paving.ray_cast(Vector((x+dx,y+dy,30)),Vector((0,0,-1)),60)[0] is not None for dx,dy in ((0,0),(.20,0),(-.20,0),(0,.20),(0,-.20))):continue
   q.z+=.005;tall=abs(u)>limit-1.5
   tint=lawn_tint(x,y,'unmown' if tall else 'verge',p.seed)
   for k in range(14):
    angle=rng.uniform(0,math.tau);h=rng.uniform(.28,.72) if tall else rng.uniform(.05,.18);w=rng.uniform(.006,.014)
    center=q+Vector((rng.uniform(-.16,.16),rng.uniform(-.12,.12),0));d=Vector((math.cos(angle),math.sin(angle),0));tip=center+d*h*.30+Vector((0,0,h))
    b.face([center-d*w,center+d*w,tip], 'Lawn',tint=tint)
    if tall and k%4==0:
     # A few genuine seed heads, not a wire curtain along the mowing line.
     b.face([tip-d*.018,tip+d*.018,tip+Vector((0,0,.09))],'Lawn',tint=(.88,.69,.37,1))
 return b.finish()

if __name__=='__main__':print(field())
