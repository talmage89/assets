"""Protect the accepted civil construction separately from weather and context.

Compare oriented exported civil triangles (position, normal, UV), omitting the
maintenance material and obsolete large mowing skins. The local handoff
snapshot is never an input to generation. Actual support audits are independent.
"""
import hashlib,json,subprocess,os,shlex
from pathlib import Path
import numpy as np
from look_audit import raw

def geometry(path):
 path=Path(path);doc=json.loads(path.read_text());buffers=[(path.parent/b['uri']).read_bytes() for b in doc['buffers']]
 def read(i):
  a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']];dt=np.dtype({5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]);n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
  return np.ndarray((a['count'],n),dtype=dt,buffer=buffers[v['buffer']],offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',n*dt.itemsize),dt.itemsize))
 out={}
 for mesh in doc['meshes']:
  fields=[]
  for prim in mesh['primitives']:
   mat=doc['materials'][prim['material']]['name']
   if mat.startswith('FreewayMaintenance'):continue
   if mesh['name'].startswith('Repairs sealants ghosts tire contacts') and mat in ('Concrete','Freeway_Form_Joint'):continue
   if mesh['name'].startswith(('Cut slopes and drainage','WideMedian')) and 'summer turf' in mat.lower():continue
   attr=prim['attributes'];idx=read(prim['indices']).ravel()
   values=np.concatenate([read(attr[k]).astype('<f4') for k in ('POSITION','NORMAL','TEXCOORD_0')],axis=1)[idx].reshape(-1,3,8)
   if mesh['name'].startswith('Mowing drainage') and ('lawn' in mat.lower() or 'summer turf' in mat.lower()):
    # Remove only the old cosmetic skins. Small volunteer leaves remain in
    # the strict comparison, as do every drain/flume and supporting surface.
    area=np.linalg.norm(np.cross(values[:,1,:3]-values[:,0,:3],values[:,2,:3]-values[:,0,:3]),axis=1)*.5
    values=values[area<.1]
   # Correct the inherited ROW fence across the arterial. Only its 22 m
   # opening and adjoining end segments change; the accepted civil works do
   # not. glTF Z is minus Blender station Y in this untransformed batch.
   if mesh['name'].startswith('ROW posts and fabric') and 'Freeway-101' in path.name:
    values=values[np.all(np.abs(values[:,:,2])>=24.5,axis=1)]
   # Only the cyclic corner starting point is arbitrary. Winding is retained.
   tris=[]
   for tri in values:
    tris.append(min(np.roll(tri,j,axis=0).tobytes() for j in range(3)))
   fields.extend(tris)
  out[mesh['name']]=hashlib.sha256(b''.join(sorted(fields))).hexdigest()
 return out

def main():
 baseline=Path('build/freeway-final-baseline/export');rows={};jobs=[]
 for name in ('Freeway-101','Freeway-202','modules/Overpass','modules/PrestressedGirder24','modules/PierBent'):
  path=Path('export')/(name+'.gltf');current=geometry(path)
  if (baseline/(name+'.gltf')).exists():
   old=geometry(baseline/(name+'.gltf'));changed=[n for n in current if current.get(n)!=old.get(n)]
   allowed=('Road_','MedianF__Mesh','PierBent__Mesh','Overpass__PierBent__Mesh')
   assert current.keys()==old.keys(),(name,'Civil mesh list changed')
   assert all(n.startswith(allowed) for n in changed),(name,changed)
   if changed:jobs.append(dict(old=str(baseline/(name+'.gltf')),new=str(path),names=changed))
   rows[name]=dict(meshes=len(current),unchanged_meshes=len(current)-len(changed),retessellated_meshes=changed,omitted='Maintenance decals, replacement-slab skins and sealant spread, revised turf shading/color stations, obsolete large mowing skins; all supporting paving, drains and flumes retained',exception='ROW fence opened at arterial; comparison excludes only fence triangles within 24.5 m of station zero' if name=='Freeway-101' else None)
  else:rows[name]=dict(meshes=len(current),scope='Handoff snapshot absent; independent construction audits apply')
 if jobs:
  source=Path('build/retessellation-jobs.json');source.write_text(json.dumps(jobs,indent=2))
  subprocess.run(shlex.split(os.environ.get('BLENDER_BINARY','blender'))+['-t','2','-b','--factory-startup','--python-exit-code','1','--python','src/retessellation.py','--',str(source)],check=True)
 Path('build/accepted-construction.json').write_text(json.dumps(rows,indent=2));print('ACCEPTED CONSTRUCTION',[(n,r.get('unchanged_meshes'),len(r.get('retessellated_meshes',[]))) for n,r in rows.items()])
if __name__=='__main__':main()
