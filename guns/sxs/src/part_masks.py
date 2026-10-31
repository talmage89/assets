"""Independent visible-part masks from exported triangles and saved cameras.

A CPU perspective-correct z-buffer avoids color management, dithering, temporal
AA and shader-based classification. It uses actual evaluated GLB triangles,
including animation visibility. No source modeling surface is substituted.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path[:0]=[str(ROOT),str(BASE/'src')]
from kit import weapon as W,weapon_verify as V
from PIL import Image

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--photos',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 p.add_argument('--shots',default='')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);arm=V.import_glb(a.source.resolve())
 parts=sorted([o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o],key=lambda o:o.get('part_name',o.name))
 ids={str(i):o.get('part_name',o.name) for i,o in enumerate(parts,1)}
 (BASE/'build/look-part-ids.json').write_text(json.dumps(ids,indent=2));a.out.mkdir(parents=True,exist_ok=True)
 cameras=json.loads((a.photos/'shots.json').read_text());records={}
 for name,s in cameras.items():
  if a.shots and name not in a.shots.split(','):continue
  assert s['sha256']==hashlib.sha256(a.source.read_bytes()).hexdigest()
  width,height=Image.open(a.photos/(name+'.png')).size
  camera=bpy.data.objects.new('Mask Camera',bpy.data.cameras.new('Mask Camera'));bpy.context.collection.objects.link(camera)
  camera.location=s['location'];camera.rotation_euler=(Vector(s['target'])-camera.location).to_track_quat('-Z','Y').to_euler()
  camera.rotation_euler.rotate_axis('Z',s.get('roll',0));bpy.context.view_layer.update()
  if s.get('aimed'):
   from kit.weapon_presentation import aimed_camera
   W.pose(arm,s.get('action','Idle'),s.get('frame',0));aimed_camera(camera,bpy.data.objects['Socket_Eye']);bpy.context.view_layer.update()
  else:W.pose(arm,s.get('action','Idle'),s.get('frame',0))
  inverse=camera.matrix_world.inverted();depth=np.full((height,width),np.inf);labels=np.zeros((height,width),np.uint8)
  tested=0
  for owner,ob in enumerate(parts,1):
   if min(abs(v) for v in arm.pose.bones[ob['bone']].matrix.to_scale())<.001:continue
   mesh=ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh();mesh.calc_loop_triangles()
   transform=inverse@ob.matrix_world
   vertices=np.array([tuple(transform@v.co) for v in mesh.vertices]);z=-vertices[:,2]
   if 'ortho' in s:
    pixels=np.stack((width/2+vertices[:,0]*width/s['ortho'],height/2-vertices[:,1]*width/s['ortho']),axis=1)
   else:
    focal=width*s.get('lens',70)/36
    pixels=np.stack((width/2+focal*vertices[:,0]/np.maximum(z,1e-8),height/2-focal*vertices[:,1]/np.maximum(z,1e-8)),axis=1)
   pixels[:,0]-=s.get('shift_x',0)*width
   pixels[:,1]+=s.get('shift_y',0)*width
   for triangle in mesh.loop_triangles:
    indices=list(triangle.vertices);q=pixels[indices];zz=z[indices]
    if min(zz)<=.001:continue
    lo=np.maximum(0,np.floor(q.min(axis=0)).astype(int));hi=np.minimum((width-1,height-1),np.ceil(q.max(axis=0)).astype(int))
    if np.any(hi<lo):continue
    yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];xx=xx+.5;yy=yy+.5
    d0=q[1]-q[0];d1=q[2]-q[0];det=d0[0]*d1[1]-d0[1]*d1[0]
    if abs(det)<1e-10:continue
    b=((xx-q[0,0])*d1[1]-(yy-q[0,1])*d1[0])/det
    c=(d0[0]*(yy-q[0,1])-d0[1]*(xx-q[0,0]))/det;aa=1-b-c
    inside=(aa>=0)&(b>=0)&(c>=0)
    distance=aa*zz[0]+b*zz[1]+c*zz[2] if 'ortho' in s else 1/np.maximum(aa/zz[0]+b/zz[1]+c/zz[2],1e-15)
    region=depth[lo[1]:hi[1]+1,lo[0]:hi[0]+1];visible=inside&(distance<region)
    region[visible]=distance[visible];labels[lo[1]:hi[1]+1,lo[0]:hi[0]+1][visible]=owner;tested+=1
   ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh_clear()
  rgba=np.zeros((height,width,4),np.uint8);rgba[:,:,0]=labels;rgba[:,:,3]=(labels>0)*255
  Image.fromarray(rgba).save(a.out/(name+'.png'))
  records[name]={**s,'mask_method':'Independent CPU triangle z-buffer; perspective-correct depth; actual evaluated GLB', 'triangles_rasterized':tested}
  bpy.data.objects.remove(camera,do_unlink=True)
 (a.out/'shots.json').write_text(json.dumps(records,indent=2));print('PART MASKS',len(records))
if __name__=='__main__':main()
