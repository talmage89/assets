"""Bake and count the actual receiver contact mask on unchanged shipping UVs.

Inspection only: neither reference pixels nor this image enter the asset. Run
through kit/with_gpu.sh after export; --out selects an ignored evidence folder.
"""
import sys,json,argparse
from pathlib import Path
import bpy,numpy as np
from PIL import Image
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parents[1]))
from kit import gpu
parser=argparse.ArgumentParser();parser.add_argument('--out',required=True,type=Path)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);out=args.out;out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/high.blend'))
sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=4
sc.render.bake.margin=0;sc.render.bake.use_selected_to_active=False
ob=bpy.data.objects['Receiver']
for o in sc.objects:o.select_set(False)
ob.hide_set(False);ob.select_set(True);bpy.context.view_layer.objects.active=ob
for m in ob.modifiers:m.show_render=False;m.show_viewport=False
ob.data.uv_layers.active=ob.data.uv_layers['BakeUV']
mat=ob.data.materials[0];nt=mat.node_tree
rub=nt.nodes['OUT_wear'].outputs[0]
em=nt.nodes.new('ShaderNodeEmission');nt.links.new(rub,em.inputs['Color']);nt.links.new(em.outputs[0],nt.nodes['OUT'].inputs['Surface'])
im=bpy.data.images.new('Actual contact mask',2048,2048,float_buffer=True);im.colorspace_settings.name='Non-Color'
tex=nt.nodes.new('ShaderNodeTexImage');tex.image=im;nt.nodes.active=tex
bpy.ops.object.bake(type='EMIT')
a=np.array(im.pixels[:],dtype=np.float32).reshape(2048,2048,4)[::-1,:,0].copy();np.save(out/'mask.npy',a)
Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(out/'mask.png')
# Raster center coverage with the exact UV triangles; no padded island texels.
ob.data.calc_loop_triangles();uv=ob.data.uv_layers['BakeUV'];inside=np.zeros((2048,2048),bool)
for t in ob.data.loop_triangles:
 p=np.array([(uv.data[i].uv.x*2048,(1-uv.data[i].uv.y)*2048) for i in t.loops]);lo=np.maximum(np.floor(p.min(0)).astype(int),0);hi=np.minimum(np.ceil(p.max(0)).astype(int),2048)
 if np.any(hi<=lo):continue
 x,y=np.meshgrid(np.arange(lo[0],hi[0])+.5,np.arange(lo[1],hi[1])+.5);v=p[1]-p[0];w=p[2]-p[0];det=v[0]*w[1]-v[1]*w[0]
 if abs(det)<1e-10:continue
 u=((x-p[0,0])*w[1]-(y-p[0,1])*w[0])/det;v2=(v[0]*(y-p[0,1])-v[1]*(x-p[0,0]))/det
 inside[lo[1]:hi[1],lo[0]:hi[0]]|=(u>=0)&(v2>=0)&(u+v2<=1)
Image.fromarray(np.uint8(inside)*255).save(out/'receiver-islands.png')
base=np.array(Image.open(BASE/'textures/T_Hearth12_BaseColor.png'))[:,:,:3];rough=np.array(Image.open(BASE/'textures/T_Hearth12_ORM.png'))[:,:,:3]
rows={}
for threshold in (.01,.1,.5,.8,.95):
 m=inside&(a>threshold)
 rows[str(threshold)]=dict(texels=int(m.sum()),fraction=float(m.sum()/inside.sum()),rgb_median=np.median(base[m],axis=0).tolist() if m.any() else [],orm_median=np.median(rough[m],axis=0).tolist() if m.any() else [])
tree=BVHTree.FromPolygons([v.co for v in ob.data.vertices],[t.vertices for t in ob.data.loop_triangles],all_triangles=True)
triangles=list(ob.data.loop_triangles)
def profile(points,axis):
 samples=[];surface_points=[]
 for origin in points:
  hit,normal,index,distance=tree.ray_cast(Vector(origin),Vector((-1,0,0)))
  if index is None:continue
  t=triangles[index];verts=[ob.data.vertices[i].co for i in t.vertices]
  tex=[Vector((*uv.data[i].uv,0)) for i in t.loops];coord=barycentric_transform(hit,*verts,*tex)
  xx=min(2047,max(0,int(coord.x*2048)));yy=min(2047,max(0,int((1-coord.y)*2048)))
  samples.append((float(origin[axis]),float(a[yy,xx]),xx,yy))
  if a[yy,xx]>.5:surface_points.append(hit.copy())
 high=[r for r in samples if r[1]>.5]
 return dict(unique_contact_texels=len({(r[2],r[3]) for r in high}),
  half_strength_span_mm=round((max(r[0] for r in high)-min(r[0] for r in high)) *1000+.1,2) if high else 0,
  surface_span_mm=round(sum((q-p).length for p,q in zip(surface_points,surface_points[1:]))*1000,2),
  profile_sample_step_mm=.1,
  samples=samples)
sys.path.insert(0,str(BASE/'src'));from build import receiver_shape,GRIP
profiles={}
for y in (.08,.15,.21):
 (_,bottom,_),_=receiver_shape(y*1000+GRIP.y);bottom=(bottom-GRIP.z)*.001
 profiles['lower_y_'+str(y)]=profile([(.04,y,z) for z in np.arange(bottom,bottom+.006,.0001)],2)
profiles['port_lower']=profile([(.04,.180,z) for z in np.arange(.032,.038,.0001)],2)
profiles['port_rear']=profile([(.04,y,.047) for y in np.arange(.133,.143,.0001)],1)
profiles['port_front']=profile([(.04,y,.047) for y in np.arange(.232,.242,.0001)],1)
result=dict(receiver_texels=int(inside.sum()),mask_max=float(a[inside].max()),thresholds=rows,profiles=profiles)
(out/'mask-stats.json').write_text(json.dumps(result,indent=2));print('RECEIVER MASK',result['receiver_texels'],'texels;',rows,'profiles in',out/'mask-stats.json',flush=True)
