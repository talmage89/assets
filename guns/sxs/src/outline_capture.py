"""Actual rear-joint and centerline curves for independent photo comparison.

These are recovered from the source triangles after construction. No image
observation or projected curve is consumed by a modeling or bake script.
"""
import hashlib,json,sys
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit import weapon as W

def main():
 source=BASE/'build/sxs.blend';bpy.ops.wm.open_mainfile(filepath=str(source))
 arm=next(o for o in bpy.data.objects if o.type=='ARMATURE');W.pose(arm,'Idle',0)
 ob=bpy.data.objects['HIGH_Action_Body'];me=ob.data;me.calc_loop_triangles();world=[ob.matrix_world@v.co for v in me.vertices]
 owners=me.attributes['head_region'];edge_regions={}
 for face in me.polygons:
  for a,b in face.edge_keys:edge_regions.setdefault(tuple(sorted((a,b))),set()).add(owners.data[face.index].value)
 joint_edges=[edge for edge,regions in edge_regions.items() if 4 in regions and len(regions)>1]
 segments=[[list(world[i]) for i in edge] for edge in joint_edges]
 ids={i for edge,regions in edge_regions.items() if 4 in regions and 1 in regions for i in edge}
 wood=sorted([world[i] for i in ids],key=lambda p:p.x)
 assert len(wood)>400,len(wood)
 tree=BVHTree.FromPolygons(world,[tuple(t.vertices) for t in me.loop_triangles],all_triangles=True)
 center=[]
 for y in np.arange(100.6,115,.1):
  p=tree.ray_cast(Vector((0,y*.001,.080)),Vector((0,0,-1)),.08)[0];assert p is not None
  center.append(p)
 curves={'wood joint':[list(p) for p in wood],'centerline':[list(p) for p in center]}
 # Physical bore-axis meridians, retaining measured slope/curvature. A smooth
 # return has no literal edge; do not relabel a height threshold as its outline.
 for sign in (-1,1):
  points=[]
  for y in np.arange(94,114.91,.1):
   x=sign*(12.6-1.7*(y-115)/660.4)
   p=tree.ray_cast(Vector((x*.001,y*.001,.08)),Vector((0,0,-1)),.08)[0];points.append(list(p))
  curves['left meridian' if sign<0 else 'right meridian']=points
 out=BASE/'build/head-outlines.json';out.write_text(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),curves_world_m=curves,wood_joint_segments_world_m=segments),indent=2))
 print('Actual outline curves', {k:len(v) for k,v in curves.items()})
if __name__=='__main__':main()
