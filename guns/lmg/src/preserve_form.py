"""Bound the delivery-only cover cleanup against the accepted source surfaces."""
import json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W

def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path));arm=bpy.data.objects['HarrowArmature'];W.pose(arm,None,0);data={}
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or ob.parent!=arm or ob.get('bake_only'):continue
  ob.data.calc_loop_triangles()
  data[ob.name]=dict(vertices=[tuple(ob.matrix_world@v.co) for v in ob.data.vertices],faces=[tuple(t.vertices) for t in ob.data.loop_triangles])
 return data
old=snapshot(BASE/'build/lmg.blend');new=snapshot(BASE/'build/delivery/finalized.blend');assert old.keys()==new.keys()
rows={}
for name,a in old.items():
 b=new[name]
 if name!='FeedCover_Shell':
  assert a['faces']==b['faces'],name
  delta=float(np.max(abs(np.asarray(a['vertices'])-np.asarray(b['vertices']))));assert delta<1e-8,(name,delta)
  rows[name]=dict(triangles=len(a['faces']),maximum_vertex_delta_m=delta,topology_identical=True)
 else:
  def directed(left,right):
   # Double-precision triangle distances. Blender's float BVH loses its own
   # submicron faces and even reports nonzero distances to identical meshes.
   lv=np.asarray(left['vertices']);rv=np.asarray(right['vertices'])
   triangles=rv[np.asarray(right['faces'])];aa,bb,cc=triangles.transpose(1,0,2)
   ab=bb-aa;ac=cc-aa;normal=np.cross(ab,ac);nn=np.sum(normal*normal,axis=1)
   d00=np.sum(ab*ab,axis=1);d01=np.sum(ab*ac,axis=1);d11=np.sum(ac*ac,axis=1)
   den=d00*d11-d01*d01
   source=lv[np.asarray(left['faces'])]
   points=np.concatenate((source.reshape(-1,3),source.mean(axis=1),(source[:,0]+source[:,1])/2,(source[:,1]+source[:,2])/2,(source[:,2]+source[:,0])/2))
   largest=0.
   for p in points:
    delta=p-aa;plane=np.sum(delta*normal,axis=1)/np.maximum(nn,1e-40)
    projected=delta-normal*plane[:,None]
    d20=np.sum(projected*ab,axis=1);d21=np.sum(projected*ac,axis=1)
    vv=(d11*d20-d01*d21)/np.maximum(den,1e-40)
    ww=(d00*d21-d01*d20)/np.maximum(den,1e-40)
    inside=(vv>=-1e-8)&(ww>=-1e-8)&(vv+ww<=1+1e-8)&(den>1e-35)
    distances=np.where(inside,plane*plane*nn,np.inf)
    for start,end in ((aa,bb),(bb,cc),(cc,aa)):
     edge=end-start;t=np.clip(np.sum((p-start)*edge,axis=1)/np.maximum(np.sum(edge*edge,axis=1),1e-40),0,1)
     dd=p-start-edge*t[:,None];distances=np.minimum(distances,np.sum(dd*dd,axis=1))
    largest=max(largest,float(np.sqrt(distances.min())))
   return largest
  delta=max(directed(a,b),directed(b,a));assert delta<.000005,delta
  rows[name]=dict(accepted_triangles=len(a['faces']),delivery_triangles=len(b['faces']),sampled_bidirectional_surface_delta_m=delta,scope='vertices, triangle centroids and edge midpoints; sampled surface bound')
result=dict(passed=True,source_triangles=sum(len(r['faces']) for r in old.values()),delivery_triangles=sum(len(r['faces']) for r in new.values()),parts=rows)
(BASE/'build/delivery/form-preservation.json').write_text(json.dumps(result,indent=2));print('FORM PRESERVATION',result['source_triangles'],result['delivery_triangles'],rows['FeedCover_Shell'])
