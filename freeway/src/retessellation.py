"""Measure edited material-sampling meshes against accepted exported surfaces.

Run in Blender, independently of the generator. Weather needs extra vertices
on columns/barriers/lanes; this audits shape instead of triangle-list identity.
The explicitly revised turf is outside this construction comparison.
"""
import json,sys
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))

def fields(path):
 d=json.loads(path.read_text());buffers=[(path.parent/b['uri']).read_bytes() for b in d['buffers']]
 def read(i):
  a=d['accessors'][i];v=d['bufferViews'][a['bufferView']];dt=np.dtype({5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]);n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
  return np.ndarray((a['count'],n),dtype=dt,buffer=buffers[v['buffer']],offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',n*dt.itemsize),dt.itemsize))
 out={}
 for mesh in d['meshes']:
  arrays={};textured={}
  for prim in mesh['primitives']:
   mat=d['materials'][prim['material']];name=mat['name']
   if name.startswith('FreewayMaintenance') or 'summer turf' in name.lower():continue
   key=name.split('.')[0]
   if key.startswith('Freeway Wheel polish / Ground '):key=key.split(' / Ground ')[1]
   attr=prim['attributes'];idx=read(prim['indices']).ravel()
   arrays.setdefault(key,[]).append(np.concatenate([read(attr[k]) for k in ('POSITION','NORMAL','TEXCOORD_0')],axis=1)[idx].reshape(-1,3,8))
   textured[key]=bool(mat.get('pbrMetallicRoughness',{}).get('baseColorTexture') or mat.get('normalTexture'))
  if arrays:out[mesh['name']]={key:dict(triangles=np.concatenate(value),textured=textured[key]) for key,value in arrays.items()}
 return out

def compare(old,new,textured=True):
 tree=BVHTree.FromPolygons([Vector(v) for v in old[:,:,:3].reshape(-1,3)],[(i,i+1,i+2) for i in range(0,len(old)*3,3)],all_triangles=True)
 samples=np.concatenate([new,new.mean(axis=1,keepdims=True)],axis=1)
 worst=0;uv_error=0;normal_error=0;worst_position=None
 for sample_index,row in enumerate(samples.reshape(-1,8)):
  point,n,index,distance=tree.find_nearest(Vector(row[:3]));assert point is not None
  if distance>worst:worst=distance;worst_position=list(map(float,row[:3]))
  if sample_index%4!=3:continue # Corner UV/normal charts have intentional seams.
  # Native texture phase and normals must agree too, using barycentric
  # interpolation at the closest point on the actual old surface.
  def errors(index,point):
   tri=old[index];a,b,c=tri[:,:3];v=np.asarray(point)-a;e0=b-a;e1=c-a
   gram=np.array([[e0@e0,e0@e1],[e0@e1,e1@e1]])
   weights=np.linalg.solve(gram,[v@e0,v@e1]);value=tri[0]+weights[0]*(tri[1]-tri[0])+weights[1]*(tri[2]-tri[0])
   return float(abs(value[6:]-row[6:]).max()) if textured else 0.,float(np.linalg.norm(value[3:6]-row[3:6]))
  uv,norm=errors(index,point)
  if uv>.001 or norm>.005:
   # Closed tube components meet at coincident, oppositely oriented internal
   # caps. A single nearest triangle can select the other cap's UV/normal.
   candidates=[errors(k,q) for q,_,k,d in tree.find_nearest_range(Vector(row[:3]),max(.00005,distance+.00001))]
   if candidates:uv,norm=min(candidates,key=lambda value:value[0]+value[1])
  uv_error=max(uv_error,uv);normal_error=max(normal_error,norm)
 return dict(samples=len(samples)*4,max_surface_distance_m=worst,max_uv_delta=uv_error,max_normal_delta=normal_error,worst_surface_position=worst_position)

def main():
 jobs=json.loads(Path(sys.argv[-1]).read_text());report={}
 for job in jobs:
  old=fields(Path(job['old']));new=fields(Path(job['new']));rows={}
  for name in job['names']:
   assert name in old and name in new,(name,'Missing civil sampling mesh')
   assert old[name].keys()==new[name].keys(),(name,'Supporting material families changed')
   groups={}
   for key in old[name]:
    # Keep the pavement, paint and raised joint layers separate. Nearest
    # geometry alone can select a neighboring layer's unrelated UV chart.
    o=old[name][key];n=new[name][key]
    a=compare(o['triangles'],n['triangles'],o['textured']);b=compare(n['triangles'],o['triangles'],o['textured'])
    for r in (a,b):
     assert r['max_surface_distance_m']<.001,(name,key,r)
     assert r['max_uv_delta']<.001,(name,key,r)
     assert r['max_normal_delta']<.005,(name,key,r)
    groups[key]=dict(old_to_new=b,new_to_old=a)
   rows[name]=groups
  report[job['new']]=rows
 Path('build/retessellation-audit.json').write_text(json.dumps(report,indent=2));print('RETESSELLATION PASSED',sum(len(v) for v in report.values()),'mesh surfaces, bidirectional samples')
if __name__=='__main__':main()
