"""Bake the original forging's ground planes through the game's Mikk basis.

Cycles supplies the compound roof, recess and all other normal detail. Its
selected-to-active pass introduced visible directional noise on these almost
flat surfaces. For the accepted ground sides only, recover the dense source's
plane by SVD and project that exact geometric normal at each 4096 UV texel.
Padding extends into unoccupied gutter only. No photo, authored pixel mask or
material change enters this projection. The kit filters and exports the result.
"""
import bpy,sys,json,shutil
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root));from kit.image_io import read_png,write_png
import hashlib
base=Path(__file__).resolve().parents[1];out=base/'build/baked/precise4k';out.mkdir(parents=True,exist_ok=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ground(f,points):
 return abs(f.normal.x)>.99999 and all(abs(abs(p.x)-.02595)<.000015 for p in points)
# Recover the two source planes from actual dense vertices, not a reported
# nominal normal. The source is our original measured forging.
bpy.ops.wm.open_mainfile(filepath=str(base/'build/delivery/high.blend'))
high=bpy.data.objects['Action_Body'];planes={};fits={}
for sign in (-1,1):
 ids={i for f in high.data.polygons if f.normal.x*sign>0 and ground(f,[high.data.vertices[j].co for j in f.vertices]) for i in f.vertices}
 points=np.array([high.data.vertices[i].co[:] for i in sorted(ids)],dtype=np.float64);center=points.mean(axis=0)
 _,_,vectors=np.linalg.svd(points-center,full_matrices=False);n=vectors[-1];n*=np.sign(n[0])*sign;distances=(points-center)@n
 planes[sign]=n;fits[str(sign)]=dict(vertices=len(points),normal=n.tolist(),center_m=center.tolist(),rms_mm=float(np.sqrt(np.mean(distances**2))*1000),maximum_residual_mm=float(np.max(abs(distances))*1000))
 assert fits[str(sign)]['maximum_residual_mm']<.03, fits

bpy.ops.wm.open_mainfile(filepath=str(base/'build/delivery/finalized.blend'))
size=4096;normal=read_png(base/'build/baked/4k/T_Covey26_Normal.png');flat=np.zeros((size,size),bool)
occupied=Image.new('1',(size,size));draw=ImageDraw.Draw(occupied)
for ob in bpy.context.scene.objects:
 if ob.type!='MESH' or 'asset_set' not in ob:continue
 m=ob.data;m.calc_loop_triangles();uv=m.uv_layers['BakeUV']
 for tr in m.loop_triangles:
  draw.polygon([(uv.data[j].uv.x*size,(1-uv.data[j].uv.y)*size) for j in tr.loops],fill=1)
o=bpy.data.objects['Action_Body'];m=o.data;m.calc_tangents(uvmap='BakeUV');m.calc_loop_triangles();uv=m.uv_layers['BakeUV'];triangles=0
for tr in m.loop_triangles:
 ps=[m.vertices[j].co for j in tr.vertices];f=m.polygons[tr.polygon_index]
 if not ground(f,ps):continue
 q=np.array([(uv.data[j].uv.x*size-.5,(1-uv.data[j].uv.y)*size-.5) for j in tr.loops],dtype=np.float64)
 xmin,ymin=np.maximum(0,np.floor(q.min(axis=0)).astype(int));xmax,ymax=np.minimum(size-1,np.ceil(q.max(axis=0)).astype(int))
 if xmax<xmin or ymax<ymin:continue
 yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1];v0=q[1]-q[0];v1=q[2]-q[0];det=v0[0]*v1[1]-v1[0]*v0[1]
 if abs(det)<1e-10:continue
 dx=xx-q[0,0];dy=yy-q[0,1];b=(dx*v1[1]-v1[0]*dy)/det;c=(v0[0]*dy-dx*v0[1])/det;a=1-b-c;mask=(a>=-1e-8)&(b>=-1e-8)&(c>=-1e-8)
 if not mask.any():continue
 weights=np.stack((a[mask],b[mask],c[mask]),axis=1)
 ns=np.array([m.corner_normals[j].vector[:] for j in tr.loops]);ts=np.array([m.loops[j].tangent[:] for j in tr.loops]);signs=np.array([m.loops[j].bitangent_sign for j in tr.loops])
 n=weights@ns;n/=np.linalg.norm(n,axis=1)[:,None]
 t=weights@ts;t-=n*np.sum(t*n,axis=1)[:,None];t/=np.linalg.norm(t,axis=1)[:,None]
 bit=np.cross(n,t)*np.sign(weights@signs)[:,None]
 axis=planes[int(np.sign(f.normal.x))];baked=np.stack((t@axis,bit@axis,n@axis),axis=1);baked/=np.linalg.norm(baked,axis=1)[:,None]
 patch=normal[ymin:ymax+1,xmin:xmax+1];patch[mask]=baked*.5+.5;flat[ymin:ymax+1,xmin:xmax+1]|=mask;triangles+=1
# Extend only into unoccupied atlas gutter, preserving every other surface.
ys,xs=np.nonzero(flat);x0=max(0,xs.min()-12);x1=min(size,xs.max()+13);y0=max(0,ys.min()-12);y1=min(size,ys.max()+13)
f=normal[y0:y1,x0:x1].copy();valid=flat[y0:y1,x0:x1].copy();block=np.asarray(occupied)[y0:y1,x0:x1]&~valid
for step in range(12):
 new=valid.copy()
 for dy,dx in ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)):
  candidate=np.roll(valid,(dy,dx),axis=(0,1))&~new&~block
  f[candidate]=np.roll(f,(dy,dx),axis=(0,1))[candidate];new|=candidate
 valid=new
normal[y0:y1,x0:x1][valid]=f[valid]
write_png(out/'T_Covey26_Normal.png',normal,16)
for channel in ('BaseColor','ORM'):
 shutil.copy2(base/('build/baked/4k/T_Covey26_'+channel+'.png'),out/('T_Covey26_'+channel+'.png'))
report=dict(triangles=triangles,interior_texels=int(flat.sum()),gutter_texels=int(valid.sum()-flat.sum()),
 method='Exact tangent projection of fitted original ground planes; curved head retains the GPU Cycles bake',
 source_planes=fits,source_sha256={name:digest(base/'build/delivery'/name) for name in ('finalized.blend','high.blend')},
 gpu_normal_sha256=digest(base/'build/baked/4k/T_Covey26_Normal.png'),
 output_normal_sha256=digest(out/'T_Covey26_Normal.png'),size=size)
(out/'projection-report.json').write_text(json.dumps(report,indent=2));print('GROUND PLANE PROJECTION',report)
