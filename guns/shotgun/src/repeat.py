"""Compare rebuilds by named geometry/rig/animation, ignoring buffer order."""
import argparse,json,sys,hashlib
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from kit.gltf import GLB
def canonical(data):
 j=data.json;nodes=j['nodes'];materials=j['materials'];out={}
 for m in j['meshes']:
  for prim in m['primitives']:
   p=data.accessor(prim['attributes']['POSITION']);n=data.accessor(prim['attributes']['NORMAL'])
   corners=np.c_[p,n];triangles=[]
   for tri in data.accessor(prim['indices']).reshape(-1,3):
    v=[tuple(float(x) for x in corners[i]) for i in tri]
    rotations=[tuple(v),tuple(v[1:]+v[:1]),tuple(v[2:]+v[:2])]
    # Match topology by position. Smooth-normal summation can vary at a pole
    # by tiny floating error; using that normal as a sort key permutes faces.
    position_key=lambda tri:tuple(round(x,9) for corner in tri for x in corner[:3])
    triangles.append(min(rotations,key=position_key))
   out['mesh:'+m['name']+':'+materials[prim['material']]['name']]=np.asarray(sorted(triangles,key=position_key))
 for a in j.get('animations',[]):
  for channel in a['channels']:
   s=a['samplers'][channel['sampler']];t=channel['target']
   key='clip:'+a['name']+':'+nodes[t['node']]['name']+':'+t['path']+':'+s['interpolation']
   values=data.accessor(s['output']).copy()
   if t['path']=='rotation':values*=np.where(values[:,3:]<0,-1,1)
   out[key+':times']=data.accessor(s['input']);out[key+':values']=values
 for node in nodes:
  name=node['name'];parent=next((p['name'] for p in nodes if nodes.index(node) in p.get('children',[])),None)
  out['parent:'+name+':'+str(parent)]=np.array([1.])
  for key in ('translation','rotation','scale','matrix'):
   if key in node:out['rest:'+name+':'+key]=np.asarray(node[key])
 for skin in j.get('skins',[]):
  for i,mat in zip(skin['joints'],data.accessor(skin['inverseBindMatrices'])):out['bind:'+nodes[i]['name']]=mat
 for material in materials:
  pbr=material['pbrMetallicRoughness']
  out['material:'+material['name']]=np.array([*pbr.get('baseColorFactor',[1,1,1,1]),pbr.get('metallicFactor',1),pbr.get('roughnessFactor',1)])
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--reference',required=True);p.add_argument('--repeat',required=True);p.add_argument('--out',required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);left=GLB(Path(a.reference));right=GLB(Path(a.repeat))
 x,y=canonical(left),canonical(right);assert set(x)==set(y),(set(x)-set(y),set(y)-set(x))
 maximum=0.;worst=None;position_delta=0.;normal_angle=0.;normal_component=0.
 for key in x:
  assert x[key].shape==y[key].shape,(key,x[key].shape,y[key].shape)
  error=float(np.max(np.abs(x[key]-y[key]))) if x[key].size else 0
  if key.startswith('mesh:'):
   position=float(np.max(np.abs(x[key][...,:3]-y[key][...,:3])))
   difference=x[key][...,3:]-y[key][...,3:]
   component=float(np.max(np.abs(difference)))
   angle=float(np.max(np.degrees(2*np.arcsin(np.minimum(np.linalg.norm(difference,axis=-1)/2,1)))))
   position_delta=max(position_delta,position);normal_component=max(normal_component,component);normal_angle=max(normal_angle,angle)
   assert position<1e-9,(key,'position',position)
   # Blender encodes custom normals in per-loop normal spaces. Their decoded
   # values can differ by a few quantization steps despite identical geometry.
   # Bound/report this shader-normal angle separately; never relax positions.
   assert angle<.03,(key,'normal angle',angle)
  else:
   if error>maximum:maximum=error;worst=key
   assert error<1e-7,(key,error)
 same=Path(a.reference).read_bytes()==Path(a.repeat).read_bytes()
 result=dict(passed=True,scope='named triangle positions/normals, rest hierarchy, bind matrices, PBR factors and clip channels; buffer order ignored',
  entries=len(x),maximum_position_delta_m=position_delta,maximum_normal_component_delta=normal_component,
  maximum_normal_angle_degrees=normal_angle,normal_angle_limit_degrees=.03,
  maximum_other_numeric_delta=maximum,worst=worst,glb_byte_identical=same)
 Path(a.out).write_text(json.dumps(result,indent=2));print('REPEAT',result)
if __name__=='__main__':main()
