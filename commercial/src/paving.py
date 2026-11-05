"""Station-only traffic, slab and oxidized-edge fields on stock glTF COLOR_0.

The ground delivery stays immutable. Its repeated low-frequency asphalt field
is measured and compensated here before causal traffic/edge variation is added.
Fine aggregate and normal detail remain the exact original ground images.
"""
import math,random
from pathlib import Path
import bpy,bmesh,numpy as np
from PIL import Image,ImageFilter
from mathutils import Vector
from plan import rotate

_CACHE=None

def ground_field():
 global _CACHE
 if _CACHE is None:
  p=Path(__file__).resolve().parents[2]/'ground/textures/ship/T_Asphalt_BaseColor.png'
  a=np.asarray(Image.open(p).convert('RGB').filter(ImageFilter.GaussianBlur(100)).resize((128,128)),dtype=float)/255
  a=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
  _CACHE=(a,a.mean(axis=(0,1)))
 return _CACHE


def cut(ob,step):
 bm=bmesh.new();bm.from_mesh(ob.data)
 for axis in (0,1):
  lo=min(v.co[axis] for v in bm.verts);hi=max(v.co[axis] for v in bm.verts)
  for i in range(math.floor(lo/step)+1,math.ceil(hi/step)):
   co=[0,0,0];co[axis]=i*step;no=[0,0,0];no[axis]=1
   bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],dist=1e-7,plane_co=co,plane_no=no)
 bm.to_mesh(ob.data);bm.free();ob.data.update()


def bands(meta):
 c=meta['canopy'];points=[]
 for island in meta['islands']:
  for side in (-1,1):
   x,y=rotate((side*2.10,-.90),c['angle']);points.append((island['center'][0]+x,island['center'][1]+y))
 return points


def traffic_distance(x,y,meta):
 distance=100
 for d in meta['driveways']:
  dx,dy=d['center']
  for i in range(22):
   t=i/21
   xx,yy=(dx-2.2*t*t,dy+.3+t*7) if d['edge']=='south' else (dx+.3+t*8.5,dy-2*t*t)
   distance=min(distance,math.hypot(x-xx,y-yy))
 # Through circulation around the exposed pad edges. Vehicles reach every
 # fueling lane and the store rather than stopping seven meters past a cut.
 c=meta['canopy'];u,v=rotate((x-c['center'][0],y-c['center'][1]),-c['angle'])
 left=-c['width']/2-2.0;right=c['width']/2+4.2;front=-c['depth']/2-2.0;rear=c['depth']/2+2.8
 for a,b in (((left,front),(right,front)),((left,front),(left,rear)),((right,front),(right,rear))):
  ax,ay=a;bx,by=b;dx=bx-ax;dy=by-ay;t=max(0,min(1,((u-ax)*dx+(v-ay)*dy)/(dx*dx+dy*dy)))
  distance=min(distance,math.hypot(u-ax-dx*t,v-ay-dy*t))
 return distance


def tint(ob,meta,role):
 me=ob.data;old=me.color_attributes.get('Tint')
 if old:me.color_attributes.remove(old)
 attr=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=attr
 W,D=meta['lot'];c=meta['canopy'];b=meta['building'];a,mean=ground_field();fuel=bands(meta)
 for poly in me.polygons:
  center=ob.matrix_world@poly.center
  local=ob.matrix_world.inverted()@center
  slab=1
  if role=='Concrete':
   # Independent pours, never a tiled variation field in the shared map.
   sx=math.floor((local.x+c['width']/2)/3.048);sy=math.floor(local.y/3.048)
   slab=random.Random(meta['seed']*971+sx*101+sy*73).uniform(.94,1.035)
  for li in poly.loop_indices:
   q=ob.matrix_world@me.vertices[me.loops[li].vertex_index].co;x,y,z=q
   if role=='Asphalt':
    sample=a[int((1-y/6.096%1)*127)%128,int((x/6.096%1)*128)%128]
    compensate=np.clip(mean/np.maximum(sample,.001),.74,1.36)
    edge=min(W/2-abs(x),D/2-abs(y));factor=.72+.10*math.exp(-max(0,edge)/1.3)
    travel=traffic_distance(x,y,meta);factor*=1-.34*math.exp(-(travel/1.10)**2)
    for i in range(meta['stalls']):
     px=b['center_x']-b['width']/2+.15+(i+.5)*2.7432;py=b['front']-meta['walk']-1.8
     factor*=1-.27*math.exp(-((x-px)/.9)**2-((y-py)/1.65)**2)
    if ob.get('repair'):factor*=.52
    rgb=compensate*factor
   else:
    factor=slab
    for fx,fy in fuel:
     u,v=rotate((x-fx,y-fy),-c['angle'])
     standing=math.exp(-((u/.82)**4+((v+.1)/2.35)**4))
     engine=math.exp(-((u/.64)**2+((v-.9)/.70)**2))
     factor*=1-.08*standing-.06*engine
    # Retained damp grit beside actual joints, narrow and irregular.
    u,v=rotate((x-c['center'][0],y-c['center'][1]),-c['angle'])
    if 'Fuel apron' in ob.name:
     joint=min(abs((u+c['width']/2+1.524)%3.048-1.524),abs((v+1.524)%3.048-1.524))
     factor*=1-.14*math.exp(-(joint/.075)**2)
    rgb=(factor,factor*.996,factor*.977)
   attr.data[li].color=(*np.minimum(rgb,1),1)


def context_road(ob,kind):
 """Copy-only presentation tint; canonical ground meshes/images never change."""
 if ob.type!='MESH' or not any(m and m.name.startswith('Asphalt') for m in ob.data.materials):return
 ob.data=ob.data.copy();cut(ob,.50);me=ob.data;uv=me.uv_layers[0]
 a,mean=ground_field()
 material=next(m for m in me.materials if m and m.name.startswith('Asphalt'))
 names={n.layer_name or 'Color' for n in material.node_tree.nodes if n.type=='VERTEX_COLOR'}
 for name in names:
  old=me.color_attributes.get(name)
  if old:me.color_attributes.remove(old)
  attr=me.color_attributes.new(name=name,type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=attr
  for loop in me.loops:
   u,v=uv.data[loop.index].uv;sample=a[int((1-v%1)*127)%128,int(u%1*128)%128]
   p=me.vertices[loop.vertex_index].co
   wheel=min(abs(p.x-q) for q in (-2.65,-1.05,1.05,2.65))
   traffic=0 if 'Intersection' in kind else .08*math.exp(-(wheel/.5)**2)
   value=(.46-traffic)*np.clip(mean/np.maximum(sample,.001),.74,1.36)
   attr.data[loop.index].color=(*np.minimum(value,1),1)
