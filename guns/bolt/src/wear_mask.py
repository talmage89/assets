"""Count causal wear on finalized UVs and read its actual shipping texels.

This diagnostic evaluates the original analytic wear on the finalized surfaces;
shipping RGB/ORM below are read from the delivered maps, never inferred from
shader constants. Dense projection and surface-normal differences are explicit.
"""
import sys,json,argparse
from pathlib import Path
import bpy,numpy as np
from PIL import Image
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import gpu
import lookdev
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
lookdev.assign(float((BASE/'build/wear-parameters.txt').read_text().split('=')[1]))
sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=4
sc.render.bake.margin=0;sc.render.bake.use_selected_to_active=False
base=np.array(Image.open(BASE/'textures/T_VesperB24_BaseColor.png'))[:,:,:3]
orm=np.array(Image.open(BASE/'textures/T_VesperB24_ORM.png'))[:,:,:3];records={}
for name in ('Stock_Mold','Bolt_Body','Scope_Body','Turret_Elevation','Bipod_Sleeve'):
 ob=bpy.data.objects[name]
 for o in sc.objects:o.select_set(False)
 ob.hide_set(False);ob.select_set(True);bpy.context.view_layer.objects.active=ob
 for m in ob.modifiers:m.show_render=False;m.show_viewport=False
 ob.data.uv_layers.active=ob.data.uv_layers['BakeUV']
 im=bpy.data.images.new('Wear diagnostic '+name,2048,2048,float_buffer=True,alpha=True);im.colorspace_settings.name='Non-Color';im.generated_color=(0,0,0,0)
 for mat in ob.data.materials:
  nt=mat.node_tree;em=nt.nodes.new('ShaderNodeEmission');nt.links.new(nt.nodes['OUT_wear'].outputs[0],em.inputs['Color']);nt.links.new(em.outputs[0],nt.nodes['OUT'].inputs['Surface'])
  tex=nt.nodes.new('ShaderNodeTexImage');tex.image=im;nt.nodes.active=tex
 bpy.ops.object.bake(type='EMIT')
 pixels=np.array(im.pixels[:],dtype=np.float32).reshape(2048,2048,4)[::-1].copy();mask=pixels[:,:,0]
 # Alpha is opaque outside a self bake in Blender 5.2. Rasterize actual UV
 # centers independently so coverage is measured rather than assumed.
 inside=np.zeros((2048,2048),bool);ob.data.calc_loop_triangles();uv=ob.data.uv_layers['BakeUV']
 for t in ob.data.loop_triangles:
  points=np.array([(uv.data[i].uv.x*2048,(1-uv.data[i].uv.y)*2048) for i in t.loops])
  lo=np.maximum(np.floor(points.min(0)).astype(int),0);hi=np.minimum(np.ceil(points.max(0)).astype(int),2048)
  if np.any(hi<=lo):continue
  xx,yy=np.meshgrid(np.arange(lo[0],hi[0])+.5,np.arange(lo[1],hi[1])+.5)
  v=points[1]-points[0];w=points[2]-points[0];det=v[0]*w[1]-v[1]*w[0]
  if abs(det)<1e-12:continue
  u=((xx-points[0,0])*w[1]-(yy-points[0,1])*w[0])/det
  v2=(v[0]*(yy-points[0,1])-v[1]*(xx-points[0,0]))/det
  inside[lo[1]:hi[1],lo[0]:hi[0]]|=(u>=0)&(v2>=0)&(u+v2<=1)
 Image.fromarray(np.uint8(np.clip(mask,0,1)*255)).save(a.out/(name+'-mask.png'))
 thresholds={}
 for t in (.1,.5,.8,.95):
  m=inside&(mask>t)
  thresholds[str(t)]=dict(texels=int(m.sum()),fraction=float(m.sum()/max(1,inside.sum())),
   shipping_rgb_median=np.median(base[m],axis=0).tolist() if m.any() else [],shipping_orm_median=np.median(orm[m],axis=0).tolist() if m.any() else [])
 profiles={}
 if name in ('Scope_Body','Turret_Elevation'):
  triangles=list(ob.data.loop_triangles)
  tree=BVHTree.FromPolygons([v.co for v in ob.data.vertices],[t.vertices for t in triangles],all_triangles=True)
  rows=[]
  for station in (np.arange(-.126,-.121,.00005) if name=='Scope_Body' else np.arange(.148,.1515,.00005)):
   origin=Vector((.05,station,.128)) if name=='Scope_Body' else Vector((.05,.062,station))
   hit,normal,index,distance=tree.ray_cast(origin,Vector((-1,0,0)))
   if index is None:continue
   t=triangles[index];v=[ob.data.vertices[i].co for i in t.vertices]
   tex=[Vector((*uv.data[i].uv,0)) for i in t.loops];coord=barycentric_transform(hit,*v,*tex)
   xx=min(2047,max(0,int(coord.x*2048)));yy=min(2047,max(0,int((1-coord.y)*2048)))
   rows.append(dict(station_m=float(station),mask=float(mask[yy,xx]),texel=[xx,yy],shipping_rgb=base[yy,xx].tolist(),shipping_orm=orm[yy,xx].tolist()))
  high=[r for r in rows if r['mask']>.5]
  profiles=dict(sample_step_mm=.05,unique_contact_texels=len({tuple(r['texel']) for r in high}),
   half_strength_span_mm=(max(r['station_m'] for r in high)-min(r['station_m'] for r in high)) *1000+.05 if high else 0,samples=rows)
 records[name]=dict(interior_texels=int(inside.sum()),maximum=float(mask.max()),thresholds=thresholds,profile=profiles)

(a.out/'mask-stats.json').write_text(json.dumps(dict(scope=__doc__,parts=records),indent=2));print('B24 WEAR AUDIT',json.dumps({k:dict(interior_texels=v['interior_texels'],core=v['thresholds']['0.95'],profile_texels=v['profile'].get('unique_contact_texels')) for k,v in records.items()}),flush=True)
