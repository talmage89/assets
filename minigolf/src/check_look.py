"""Raw delivered texture / UV / memory audit, distinct from visual acceptance.

Reused trim tiles intentionally overlap. This is a tiled family, not a unique
atlas: UV overlap is legal only within an authored material rectangle.
"""
import sys,json,hashlib,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import numpy as np
from kit.gltf import GLB
from kit.image_io import read_png
from textures import RECTS

def main():
 report=[]
 for seed in (71,92):
  path=Path(f'export/Minigolf-{seed}.glb');g=GLB(path);counts=0;density=[];colors=[];uv_bad=0
  for mesh in g.json['meshes']:
   for prim in mesh['primitives']:
    attr=prim['attributes'];p=g.accessor(attr['POSITION']);uv=g.accessor(attr['TEXCOORD_0']);idx=g.accessor(prim['indices']).reshape(-1,3);n=g.accessor(attr['NORMAL']);counts+=len(idx)
    assert np.isfinite(uv).all() and np.isfinite(p).all()
    assert np.max(np.abs(np.linalg.norm(n,axis=1)-1))<1e-4
    if 'TANGENT' in attr:
     tangent=g.accessor(attr['TANGENT']);assert np.max(np.abs(np.linalg.norm(tangent[:,:3],axis=1)-1))<.001
    if 'COLOR_0' in attr:colors.append(g.accessor(attr['COLOR_0'])[:,:3])
    mat=g.json['materials'][prim['material']];name=mat.get('name','')
    if name.startswith('Minigolf') and 'Graphics' not in name:
     lo=uv[idx].min(axis=1);hi=uv[idx].max(axis=1);valid=np.zeros(len(idx),bool)
     for u0,v0,u1,v1 in RECTS.values():valid |= (lo[:,0]>=u0-1e-6)&(hi[:,0]<=u1+1e-6)&(lo[:,1]>=v0-1e-6)&(hi[:,1]<=v1+1e-6)
     uv_bad+=np.count_nonzero(~valid)
     v=p[idx];t=uv[idx];world=np.linalg.norm(np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]),axis=1)/2
     ua=np.abs(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]))/2
     useful=(world>1e-6)&(ua>1e-12);density.extend((2048*np.sqrt(ua[useful]/world[useful])).tolist())
  assert uv_bad==0,(seed,uv_bad)
  assert len(colors)>0,'Causal macro masks lost from export'
  meta=json.loads(path.with_suffix('.json').read_text());assert counts==meta['triangles']
  images=[];allocation=0
  for im in g.json.get('images',[]):
   view=g.json['bufferViews'][im['bufferView']];off=view.get('byteOffset',0);raw=g.binary[off:off+view['byteLength']];a=read_png(raw);h,w,c=a.shape
   allocation+=w*h*4/3 # one 8-bpp map plus mips
   images.append(dict(name=im.get('name'),size=[w,h],channels=c,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
  report.append(dict(seed=seed,triangles=counts,materials=len(g.json['materials']),images=images,compressed_gpu_mib=allocation/1024**2,glb_bytes=path.stat().st_size,uv_escaped_triangles=int(uv_bad),course_uv_density_px_m_p5_p50_p95=np.percentile(density,[5,50,95]).tolist(),tint_minmax=[np.min(np.concatenate(colors),axis=0).tolist(),np.max(np.concatenate(colors),axis=0).tolist()]))
 normal=read_png('textures/ship/T_Minigolf_Normal.png')*2-1;error=np.abs(np.linalg.norm(normal,axis=-1)-1);assert error.max()<.012
 out=dict(passed=True,scope=__doc__,normal_max_unit_error=float(error.max()),courses=report)
 Path('build/look-check.json').write_text(json.dumps(out,indent=2));print('LOOK CHECK PASS',[(r['seed'],r['triangles'],r['materials'],r['compressed_gpu_mib']) for r in report])
if __name__=='__main__':main()
