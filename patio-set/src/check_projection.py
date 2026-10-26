"""Detect missed atlas projections inside meaningful-sized delivered UV faces.

Every authored substrate in this family has positive RGB; exact black is a
missed ray, not an intended marking. Outside-atlas pixels are never sampled.
"""
import sys,json,argparse,io,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.gltf import GLB
from PIL import Image
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from kit.motion import inside
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
g=GLB(Path(a.source));i=next(i for i,v in enumerate(g.json['images']) if 'BaseColor' in v['name']);pixels=np.array(Image.open(io.BytesIO(g.image(i))).convert('RGB'));h,w=pixels.shape[:2]
normal_i=next(i for i,v in enumerate(g.json['images']) if 'Normal' in v['name']);normal=np.array(Image.open(io.BytesIO(g.image(normal_i))).convert('RGB'))
orm_i=next(i for i,v in enumerate(g.json['images']) if 'ORM' in v['name']);orm=np.array(Image.open(io.BytesIO(g.image(orm_i))).convert('RGB'))
weights=np.array([[1/3]*3,[.6,.2,.2],[.2,.6,.2],[.2,.2,.6]])
rows=[]
for mesh in g.json['meshes']:
 checked=black=hidden=occluded=inverted=0
 for primitive in mesh['primitives']:
  u=g.accessor(primitive['attributes']['TEXCOORD_0']);idx=g.accessor(primitive['indices']).reshape(-1,3);tri=u[idx]
  area=np.abs((tri[:,1,0]-tri[:,0,0])*(tri[:,2,1]-tri[:,0,1])-(tri[:,1,1]-tri[:,0,1])*(tri[:,2,0]-tri[:,0,0]))*w*h/2
  vertices=g.accessor(primitive['attributes']['POSITION']);tree=BVHTree.FromPolygons([Vector(v) for v in vertices],idx.tolist(),all_triangles=True)
  positions=vertices[idx][area>=4]
  tri=tri[area>=4];samples=np.einsum('kj,tjc->tkc',weights,tri);x=np.clip((samples[:,:,0]*w).astype(int),0,w-1);y=np.clip((samples[:,:,1]*h).astype(int),0,h-1)
  values=pixels[y,x];miss=np.max(values,axis=2)<4;black+=int(miss.sum());checked+=values.shape[0]*values.shape[1]
  if miss.any():
   # Reconstruct closed components across glTF's UV/normal vertex splits.
   parent=list(range(len(idx)));edges={}
   def find(k):
    while parent[k]!=k:parent[k]=parent[parent[k]];k=parent[k]
    return k
   for fi,ids in enumerate(idx):
    keys=[tuple(round(float(x),5) for x in vertices[j]) for j in ids]
    for aa,bb in zip(keys,keys[1:]+keys[:1]):
     edge=tuple(sorted((aa,bb)))
     if edge in edges:parent[find(fi)]=find(edges[edge])
     else:edges[edge]=fi
   groups={}
   for fi in range(len(idx)):groups.setdefault(find(fi),[]).append(idx[fi].tolist())
   vector_vertices=[Vector(v) for v in vertices]
   solids=[BVHTree.FromPolygons(vector_vertices,fs,all_triangles=True) for fs in groups.values()]
   for face,sample in np.argwhere(miss):
    point=Vector(weights[sample]@positions[face]);vs=[Vector(v) for v in positions[face]];direction=(vs[1]-vs[0]).cross(vs[2]-vs[0]).normalized()
    point+=direction*.00001
    for solid in solids:
     near=solid.find_nearest(point)
     if near[0] is not None and (point-near[0]).dot(near[1])<0 and inside(solid,point):
      hidden+=1;break
  occluded+=int(np.sum(orm[y,x,0]<4));inverted+=int(np.sum(normal[y,x,2]<100))
 rows.append(dict(mesh=mesh['name'],samples=checked,black_samples=black,encased_black_samples=hidden,exposed_black_samples=black-hidden,fraction=(black-hidden)/max(1,checked),occluded_samples=occluded,occlusion_fraction=occluded/max(1,checked),inverted_normals=inverted,inverted_fraction=inverted/max(1,checked)))
# A few samples at grazing intersected seams can miss; broad striped areas cannot.
errors=[row['mesh'] for row in rows if row['fraction']>.001 or (row['mesh'] in ('Umbrella_OpenMesh','Umbrella_ClosedMesh') and row['inverted_fraction']>.015)]
r=dict(passed=not errors,errors=errors,source=a.source,source_sha256=hashlib.sha256(Path(a.source).read_bytes()).hexdigest(),threshold_rgb_byte=4,max_fraction=.001,minimum_uv_face_area_texels=4,umbrella_max_inverted_fraction=.015,meshes=rows)
Path(a.out).write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
if errors:raise RuntimeError('Missed texture projections')
