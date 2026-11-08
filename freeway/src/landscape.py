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
 median=np.median(rgb.reshape(-1,3),axis=0)
 rng=np.random.default_rng(381);size=rgb.shape[0]
 def noise(n):
  a=rng.random((n,n),dtype=np.float32)
  # Wrapped padding keeps the original repeat seamless after interpolation.
  a=np.pad(a,2,mode='wrap');im=Image.fromarray(a).resize((size+4*size//n,)*2,Image.Resampling.BICUBIC)
  return np.asarray(im,np.float32)[2*size//n:2*size//n+size,2*size//n:2*size//n+size]-.5
 clump=.42*noise(11)+.35*noise(31)+.21*noise(79)
 rgb=np.clip(rgb/median*np.array([.175,.190,.060])*(1+clump[:,:,None]*1.7),0,1)
 path.parent.mkdir(parents=True,exist_ok=True);write_png(path,linear_to_srgb(rgb),bits=8)
 receipt.write_text(json.dumps(dict(inputs=sig,output_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),scope='Seasonal derivative of original Ground manufacture; same canonical normal/ORM and 2048 allocation'),indent=2));return path

def install():
 import bpy,geom as Q
 path=field();ma=Q.M['Lawn'].copy();ma.name='Freeway summer turf / Ground lawn relief'
 bs=ma.node_tree.nodes.get('Principled BSDF');base=next(n for n in ma.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and 'BaseColor' in n.image.name)
 base.image=bpy.data.images.load(str(path.resolve()),check_existing=True)
 ma.use_backface_culling=False # Rooted blades share the turf images.
 Q.M['Lawn']=ma

def lawn_tint(x,y,kind='verge',seed=0,height=0,lateral=None):
 # Changes are slow in station, and connected to dry high shoulders or yard
 # irrigation/root competition. Texture grain supplies the small variation.
 phase=.5+.26*math.sin(y*.061+math.sin(x*.11)+seed)+.17*math.sin(y*.19+x*.087)
 dry=max(0,min(1,.06+.36*phase if kind=='yard' else .12+.40*phase))
 if kind in ('verge','unmown'):dry=min(1,dry+.16*max(0,min(1,height/7)))
 if kind=='ditch':dry*=.15
 if kind=='unmown':dry=max(.50,dry)
 rootshade=.94+.04*math.sin(x*.18+math.sin(y*.16))+.02*math.sin(y*.73+x*.31)
 # Put straw pigment in the image so the desired red multiplier stays <=1.
 # glTF's normalized color attributes clamp a >1 tint during serialization.
 red_scale=.155/.175
 if kind=='yard':return ((.80+.18*dry)*red_scale*rootshade,(.93-.26*dry)*rootshade,(.94-.37*dry)*rootshade,1)
 stripe=1 if kind=='unmown' else .95+.05*math.cos((x if lateral is None else lateral)*math.pi/1.8)
 return ((.84+.20*dry)*red_scale*rootshade*stripe,(.98-.16*dry)*rootshade*stripe,(.96-.27*dry)*rootshade*stripe,1)

def verges(p,parent):
 """Exported instanced clumps share a guarded chart in the existing atlas."""
 from turf_cards import plant
 return plant(p,parent)

def surface(b,p,points):
 """Small color stations on graded turf; geometry remains on its support."""
 from mathutils import Vector
 aa,bb,cc,dd=map(Vector,points)
 near=max(abs(v.y) for v in (aa,bb,cc,dd))<240 and min(abs(v.x) for v in (aa,bb,cc,dd))<100
 nx=min(64,max(1,math.ceil((bb-aa).length/1.8))) if near else 1
 ny=max(1,math.ceil((dd-aa).length/3)) if near else 1
 def at(x,y):return aa.lerp(bb,x).lerp(dd.lerp(cc,x),y)
 for j in range(ny):
  for i in range(nx):
   start=len(b.colors);b.surface([at(i/nx,j/ny),at((i+1)/nx,j/ny),at((i+1)/nx,(j+1)/ny),at(i/nx,(j+1)/ny)],'Lawn')
   for k in range(start,len(b.colors)):
    x,y,z=b.v[k];u=p.radius-math.hypot(p.radius-x,y) if p.radius else x
    kind='unmown' if abs(u)>(43 if p.kind=='diamond' else 28) else 'verge'
    b.colors[k]=lawn_tint(x,y,kind,p.seed,z,lateral=u)

def smooth(ob):
 """Average matching earth corners; retain the physical ditch/crest shape."""
 from mathutils import Vector
 me=ob.data;groups={}
 for face in me.polygons:
  if 'turf' not in me.materials[face.material_index].name.lower():continue
  for index in face.vertices:
   v=me.vertices[index];key=tuple(round(c,4) for c in v.co)
   groups.setdefault(key,[]).append(face.normal.copy())
 normals=[]
 for loop in me.loops:
  key=tuple(round(c,4) for c in me.vertices[loop.vertex_index].co)
  normals.append(sum(groups[key],Vector()).normalized() if key in groups else me.corner_normals[loop.index].vector)
 me.normals_split_custom_set(normals)

if __name__=='__main__':print(field())
