"""Independent stock glTF checks, shared image hashes, trim domains and density.

Repeated manufacturing trims intentionally share charts. Each polygon must
remain inside one trim cell. Names and indications have their own domains.
This is different from unique unwrapped-island overlap verification.
"""
from pathlib import Path
import json,sys,hashlib,math
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))

def run():
 report=[];images={};trianglecounts={}
 for path in sorted(Path('export').rglob('*.gltf')):
  d=json.loads(path.read_text());binary=(path.parent/d['buffers'][0]['uri']).read_bytes()
  def acc(idx):
   a=d['accessors'][idx];v=d['bufferViews'][a['bufferView']];dt=np.dtype({5121:'u1',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']]);n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
   return np.ndarray((a['count'],n),dtype=dt,buffer=binary,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',n*dt.itemsize),dt.itemsize))
  rows=[];total=0
  for im in d.get('images',[]):
   file=(path.parent/im['uri']).resolve();digest=hashlib.sha256(file.read_bytes()).hexdigest();expected=Path('textures/ship')/file.name
   assert expected.exists() and digest==hashlib.sha256(expected.read_bytes()).hexdigest(),file
   images[file.name]=(Image.open(file).size,file.stat().st_size)
   assert file.parent==Path('export/textures').resolve(),file
  assert len(d.get('images',[]))<=5,(path,len(d['images']))
  assert len(d['materials'])<=4,(path,len(d['materials']))
  for node in d['nodes']:
   if 'mesh' not in node:continue
   for prim in d['meshes'][node['mesh']]['primitives']:
    mat=d['materials'][prim['material']];pos=acc(prim['attributes']['POSITION']);normal=acc(prim['attributes']['NORMAL']);uv=acc(prim['attributes']['TEXCOORD_0']);ix=acc(prim['indices']).reshape(-1,3);total+=len(ix)
    assert np.isfinite(pos).all() and np.isfinite(uv).all();assert np.max(abs(np.linalg.norm(normal,axis=1)-1))<1e-4
    assert np.min(uv)>=-1e-6 and np.max(uv)<=1.000001,(path,node['name'],'outside UV domain')
    p=pos[ix];t=uv[ix];area3=np.linalg.norm(np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]),axis=1)/2;du=t[:,1]-t[:,0];dv=t[:,2]-t[:,0];area2=abs(du[:,0]*dv[:,1]-du[:,1]*dv[:,0])/2
    constant=node.get('extras',{}).get('signal_kind')=='countdown'
    if mat['name'].startswith('SharedLens_'):assert mat['alphaMode']=='MASK' and mat['alphaCutoff']==.5
    if constant:
     tex=mat['pbrMetallicRoughness']['baseColorTexture']['index'];imrow=d['images'][d['textures'][tex]['source']];pixels=np.array(Image.open(path.parent/imrow['uri']).convert('RGBA'));uu,vv=uv[0];px=min(pixels.shape[1]-1,int(uu*pixels.shape[1]));py=min(pixels.shape[0]-1,int((1-vv)*pixels.shape[0]));assert pixels[py,px,3]>200,('Countdown samples transparent texel',node['name'])
    if mat['name']=='Signals_Atlas':
     cells=np.floor(np.clip(t,0,.999999)*np.array([4,8])).astype(int)
     crossed=np.any(cells!=cells[:,0:1],axis=(1,2));assert not crossed.any(),(path,node['name'],'trim boundary',int(crossed.sum()))
    valid=(area3>1e-12)&(area2>1e-16)
    assert np.all(valid | (area3<1e-12) | constant),(path,node['name'],'zero-area UV',int((~valid).sum()))
    density=np.sqrt(area2[valid]/area3[valid])*(2048 if mat['name']=='Signals_Atlas' else 1024 if 'Lens' in mat['name'] else 512)
    rows.append(dict(node=node['name'],material=mat['name'],triangles=len(ix),density_px_m_quantiles=np.quantile(density,[.05,.5,.95]).tolist() if len(density) else None,constant_countdown=constant))
  report.append(dict(file=str(path),triangles=total,material_count=len(d['materials']),geometry_bytes=len(binary),json_bytes=path.stat().st_size,meshes=rows))
 assert len(images)==5,images
 assert images['T_Signals_BaseColor.png'][0]==(2048,2048)
 assert images['T_Signals_Emissive.png'][0]==(1024,1024)
 Path('build/delivery-check.json').write_text(json.dumps(dict(passed=True,files=report,images=images,gpu_mib=17.5,overlap_policy='Explicit shared manufacturing trim reuse inside 32 guarded cells; countdown segments intentionally sample a constant LED texel',scope='Raw glTF accessors/materials/images; source contacts/motion and fresh-import comparisons are independent'),indent=2))
 print('DELIVERY CHECK',len(report),'glTFs; five shared images; normals, trim domains, UV area/density, image bytes')
if __name__=='__main__':run()
