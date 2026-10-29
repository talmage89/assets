"""Sample real receiver surfaces and shipped UV texels on a physical 2D grid."""
import sys,json
from pathlib import Path
import bpy,numpy as np
from PIL import Image
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W
from forms import RECEIVER_ROWS

def main():
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
 W.pose(bpy.data.objects['LeverArmature'],None,0);ob=bpy.data.objects['Receiver'];mesh=ob.data;mesh.calc_loop_triangles()
 triangles=list(mesh.loop_triangles);tree=BVHTree.FromPolygons([v.co for v in mesh.vertices],[t.vertices for t in triangles],all_triangles=True)
 uv=mesh.uv_layers['BakeUV'];image=np.asarray(Image.open(BASE/'textures/T_BrackenL20_BaseColor.png').convert('RGB'))
 orm=np.asarray(Image.open(BASE/'textures/T_BrackenL20_ORM.png').convert('RGB'))
 ys=np.arange(.075,.190,.0005);hs=np.arange(.00025,.008,.0005)
 points=[];colors=[];packed=[]
 for h in hs:
  row=[];color=[];material=[]
  for y in ys:
   a,b=next((a,b) for a,b in zip(RECEIVER_ROWS,RECEIVER_ROWS[1:]) if a[0]<=y*1000<=b[0]);t=(y*1000-a[0])/(b[0]-a[0]);bottom=(a[2]+t*(b[2]-a[2]))*.001
   hit,normal,index,distance=tree.ray_cast(Vector((-.04,y,bottom+h)),Vector((1,0,0)),.06)
   assert index is not None,(y,h)
   tri=triangles[index];verts=[mesh.vertices[i].co for i in tri.vertices];tex=[Vector((*uv.data[i].uv,0)) for i in tri.loops]
   coord=barycentric_transform(hit,*verts,*tex);xx=min(2047,max(0,int(coord.x*2048)));yy=min(2047,max(0,int((1-coord.y)*2048)))
   row.append(tuple(hit));color.append(image[yy,xx]);material.append(orm[yy,xx])
  points.append(row);colors.append(color);packed.append(material)
 out=BASE/'build/review';out.mkdir(exist_ok=True)
 np.savez_compressed(out/'wear-grid.npz',points=np.asarray(points),base=np.asarray(colors),orm=np.asarray(packed),ys=ys,hs=hs)
 print('ACTUAL SHIPPING WEAR GRID',len(ys),len(hs),'at 0.5 mm',flush=True)
if __name__=='__main__':main()
