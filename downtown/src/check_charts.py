"""Independent raw glTF chart areas, strip guards and physical brick module.

Repetition on different masonry surfaces is intentional. Unique graphics use
explicit atlas rectangles; no automatic unwrap or overlapping unique bake exists.
"""
import json,sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit.gltf import GLB

def load(path):
 g=object.__new__(GLB);g.json=json.loads(path.read_text());g.binary=(path.parent/g.json['buffers'][0]['uri']).read_bytes();return g

rows=[]
for path in sorted(Path('export').glob('*.gltf')):
 g=load(path);densities={};minimum_guard=1.;ntri=0
 for mesh in g.json['meshes']:
  for pr in mesh['primitives']:
   mat=g.json['materials'][pr['material']]['name'];attrs=pr['attributes'];v=g.accessor(attrs['POSITION']);uv=g.accessor(attrs['TEXCOORD_0']);ix=g.accessor(pr['indices']).reshape(-1,3);a=v[ix];t=uv[ix]
   world=np.linalg.norm(np.cross(a[:,1]-a[:,0],a[:,2]-a[:,0]),axis=1)/2;du=t[:,1]-t[:,0];dv=t[:,2]-t[:,0];ua=abs(du[:,0]*dv[:,1]-du[:,1]*dv[:,0])/2
   assert np.all(world>1e-11) and np.all(ua>1e-13),(path,mat,'degenerate chart')
   size=1024 if 'MineralRoof' in mat or 'Interior' in mat else 2048
   density=np.sqrt(ua/world)*size;densities[mat]=np.percentile(density,[5,50,95]).tolist();ntri+=len(ix)
   if any(n in mat for n in ('Masonry','MineralRoof','Finish')):
    count=8 if 'Finish' in mat else 4;low=t[:,:,1].min(axis=1);high=t[:,:,1].max(axis=1);strip=np.floor((low+high)/2*count)
    assert np.all(strip>=0) and np.all(strip<count)
    guards=np.minimum(low-strip/count,(strip+1)/count-high)
    assert np.all(guards>=(8/2048)-2e-6),(path,mat,'unguarded strip',float(guards.min()))
    minimum_guard=min(minimum_guard,float(guards.min()))
   if 'Masonry' in mat:
    # Export is Y-up, so physical height is coordinate 1. Large vertical
    # exterior triangles retain 18 courses across the usable V repeat.
    dz=np.ptp(a[:,:,1],axis=1);dv=np.ptp(t[:,:,1],axis=1);vertical=dz>.15
    ratios=dz[vertical]/dv[vertical];expected=1.2192/(.25-16/2048)
    assert np.all(abs(ratios-expected)<.002),(path,ratios.min(),ratios.max())
 rows.append(dict(id=path.stem,triangles=ntri,density_px_m_p5_p50_p95=densities,minimum_region_guard_uv=minimum_guard))
Path('build/chart-check.json').write_text(json.dumps(dict(passed=True,buildings=rows,brick_module_m=[.2032,.2032/3],scope='Actual raw areas/UVs, nondegenerate charts, guarded strip containment, vertical masonry phase. Repeated tile/trim charts are intentional, not a unique per-building unwrap.'),indent=2)+'\n')
print('CHARTS PASS',len(rows),'building/street deliveries')
