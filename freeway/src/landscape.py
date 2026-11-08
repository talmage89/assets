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
 # Keep the fine authored blade values, but compress the native soil/weed
 # contrast. Independent channel normalization turned soil into yellow camo.
 luminance=rgb@np.array([.2126,.7152,.0722],np.float32)
 fine=np.clip((luminance/np.median(luminance))**.80,.55,1.55)
 rng=np.random.default_rng(381);size=rgb.shape[0]
 def noise(n):
  a=rng.random((n,n),dtype=np.float32)
  # Wrapped padding keeps the original repeat seamless after interpolation.
  a=np.pad(a,2,mode='wrap');im=Image.fromarray(a).resize((size+4*size//n,)*2,Image.Resampling.BICUBIC)
  return np.asarray(im,np.float32)[2*size//n:2*size//n+size,2*size//n:2*size//n+size]-.5
 clump=.42*noise(11)+.35*noise(31)+.21*noise(79)
 # A 1.524m mowing swath remains in the textured base when blades are below
 # a pixel. Near cards carry the corresponding alternating orientation.
 stripe=1+.035*np.sin(np.arange(size,dtype=np.float32)*math.tau/size)
 value=fine*(1+clump*.65)*stripe[None,:]
 rgb=np.clip(value[:,:,None]*np.array([.145,.170,.055]),0,1)
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
 red_scale=.125/.145
 # Keep the accepted irrigated-yard mean when changing the ROW's pigment.
 if kind=='yard':return ((.80+.18*dry)*(.125/.145)*rootshade,(.93-.26*dry)*(.155/.170)*rootshade,(.94-.37*dry)*rootshade,1)
 # Mowing contrast belongs to the dense card tiles. Sampling its short
 # period on the sparse earth corners would alias into large triangles.
 # Aggregate short turf includes under-blade shadow. Matching that value
 # reduces the near-card/distant-base discontinuity in the exported asset.
 return tuple(v*.78 for v in ((.84+.20*dry)*red_scale*rootshade,(.98-.16*dry)*rootshade,(.96-.27*dry)*rootshade))+(1,)

def verges(p,parent):
 """Exported instanced clumps share a guarded chart in the existing atlas."""
 from turf_cards import plant
 return plant(p,parent)

def surface(b,p,points):
 """Retain the accepted physical earth triangles; shade them smoothly later.

 Bilinear quad resampling changed the heights of the old triangulated slopes
 and moved seats/flumes. Manufacture grain and instanced cards provide local
 detail without adding a dense terrain grid or altering those supports.
 """
 start=len(b.colors);b.surface(points,'Lawn');uv=[]
 for k in range(start,len(b.colors)):
  x,y,z=b.v[k];u=p.radius-math.hypot(p.radius-x,y) if p.radius else x
  kind='unmown' if abs(u)>(43 if p.kind=='diamond' else 28) else 'verge'
  b.colors[k]=lawn_tint(x,y,kind,p.seed,z,lateral=u)
  station=math.atan2(y,p.radius-x)*p.radius if p.radius else y
  uv.append((u/3.048,station/3.048))
 b.uv[-1]=uv

def smooth(ob):
 """Average matching earth corners; retain the physical ditch/crest shape."""
 from mathutils import Vector
 me=ob.data;groups={};grass_loops=set()
 for face in me.polygons:
  if 'turf' not in me.materials[face.material_index].name.lower():continue
  grass_loops.update(face.loop_indices)
  for index in face.vertices:
   v=me.vertices[index];key=tuple(round(c,4) for c in v.co)
   groups.setdefault(key,[]).append(face.normal.copy())
 normals=[]
 for loop in me.loops:
  key=tuple(round(c,4) for c in me.vertices[loop.vertex_index].co)
  normals.append(sum(groups[key],Vector()).normalized() if loop.index in grass_loops else me.corner_normals[loop.index].vector)
 me.normals_split_custom_set(normals)

if __name__=='__main__':print(field())
