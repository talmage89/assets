"""Repair Mikk's float32 zero-angle corner on long, thin bevel triangles.

Only zero tangents are touched. UV and geometric area must both be valid.
The derivative and corner-angle weighting use float64 and atan2, avoiding
acos(dot)==0 at the very acute corner of a metre-long millimetre bevel.
"""
import json,struct
from pathlib import Path
import numpy as np

def repair(path):
 path=Path(path);packed=path.suffix=='.glb'
 if packed:
  raw=path.read_bytes();size=struct.unpack_from('<I',raw,12)[0]
  doc=json.loads(raw[20:20+size]);binary=bytearray(raw[28+size:])
 else:
  doc=json.loads(path.read_text());binpath=path.parent/doc['buffers'][0]['uri'];binary=bytearray(binpath.read_bytes())
 def array(index):
  a=doc['accessors'][index];v=doc['bufferViews'][a['bufferView']]
  dtype={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]
  dim={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']];item=np.dtype(dtype).itemsize
  return np.ndarray((a['count'],dim),dtype=dtype,buffer=binary,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',dim*item),item))
 rows=[]
 for mesh in doc['meshes']:
  for prim in mesh['primitives']:
   attr=prim['attributes']
   if 'TANGENT' not in attr:continue
   tangent=array(attr['TANGENT']);bad=np.where(np.linalg.norm(tangent[:,:3],axis=1)<.5)[0]
   if not len(bad):continue
   pos=array(attr['POSITION']).astype(float);uv=array(attr['TEXCOORD_0']).astype(float);normal=array(attr['NORMAL']).astype(float);faces=array(prim['indices']).reshape(-1,3)
   for vertex in bad:
    total=np.zeros(3);btotal=np.zeros(3)
    for ids in faces[np.any(faces==vertex,axis=1)]:
     p=pos[ids];t=uv[ids];e=p[1]-p[0];f=p[2]-p[0];du=t[1]-t[0];dv=t[2]-t[0];det=du[0]*dv[1]-du[1]*dv[0]
     assert abs(det)>1e-14 and np.linalg.norm(np.cross(e,f))>1e-12,('Invalid UV or geometry',mesh['name'],int(vertex))
     k=list(ids).index(vertex);a=p[(k+1)%3]-p[k];b=p[(k+2)%3]-p[k];angle=np.arctan2(np.linalg.norm(np.cross(a,b)),np.dot(a,b))
     total+=(e*dv[1]-f*du[1])/det*angle;btotal+=(f*du[0]-e*dv[0])/det*angle
    n=normal[vertex];total-=n*np.dot(n,total);length=np.linalg.norm(total);assert length>1e-8
    total/=length;tangent[vertex,:3]=total;tangent[vertex,3]=-1 if np.dot(np.cross(n,total),btotal)<0 else 1
   rows.append(dict(mesh=mesh['name'],material=doc['materials'][prim['material']]['name'],repaired_vertices=len(bad)))
 if packed:
  header=raw[:20+size];path.write_bytes(header+raw[20+size:28+size]+binary)
 else:binpath.write_bytes(binary)
 return rows
