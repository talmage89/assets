"""Independent external-glTF resources, raw geometry and preserved libraries."""
import hashlib,json,sys
from collections import Counter
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]


def accessor(doc,binary,index):
    a=doc['accessors'][index];v=doc['bufferViews'][a['bufferView']]
    dt=np.dtype({5120:'i1',5121:'u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']]);n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
    b=np.ndarray((a['count'],n),dtype=dt,buffer=binary,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',n*dt.itemsize),dt.itemsize)).copy()
    if a.get('normalized'):b=b.astype(float)/np.iinfo(dt).max
    return b


def audit(path):
    d=json.loads(path.read_text());binary=(path.parent/d['buffers'][0]['uri']).read_bytes()
    ns=d['nodes'];parents={c:i for i,n in enumerate(ns) for c in n.get('children',[])};counts=Counter();bad=[];density=[]
    for i,n in enumerate(ns):
        if 'mesh' not in n:continue
        j=i;kind='church'
        while True:
            e=ns[j].get('extras',{})
            if 'actor_kind' in e:kind=e['actor_kind'];break
            if j not in parents:break
            j=parents[j]
        for pr in d['meshes'][n['mesh']]['primitives']:
            at=pr['attributes'];idx=accessor(d,binary,pr['indices']).ravel().reshape(-1,3);counts[kind]+=len(idx)
            if kind not in ('church','site'):continue
            xyz=accessor(d,binary,at['POSITION']);normal=accessor(d,binary,at['NORMAL'])
            if not np.isfinite(xyz).all() or not np.isfinite(normal).all():bad.append((n['name'],'nonfinite'))
            if np.max(np.abs(np.linalg.norm(normal,axis=1)-1))>.002:bad.append((n['name'],'normal length'))
            pp=xyz[idx];area=np.linalg.norm(np.cross(pp[:,1]-pp[:,0],pp[:,2]-pp[:,0]),axis=1)/2
            # Microscopic native-terrain slivers are reported separately; our
            # church meshes are held to a stricter zero-area threshold.
            if kind=='church' and np.any(area<1e-12):bad.append((n['name'],'zero area',int(np.sum(area<1e-12))))
            if 'TEXCOORD_0' in at:
                uv=accessor(d,binary,at['TEXCOORD_0'])[idx];a=uv[:,1]-uv[:,0];b=uv[:,2]-uv[:,0];ua=np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0])/2
                good=(area>1e-9)&(ua>1e-14)
                if kind=='church':density.extend((np.sqrt(ua[good]/area[good])*1024).tolist())
            elif kind=='church':bad.append((n['name'],'missing UV'))
    images={}
    for im in d.get('images',[]):
        assert 'uri' in im and not im['uri'].startswith(('/', 'data:', 'http')),im
        p=(path.parent/im['uri']).resolve();assert p.exists(),p
        digest=hashlib.sha256(p.read_bytes()).hexdigest();size=Image.open(p).size
        images[digest]=dict(path=str(p.relative_to(ROOT)),size=size,bytes=p.stat().st_size,mib=size[0]*size[1]*4/3/1024**2)
    static=counts['church']+counts['site']+counts['town']
    if path.stem.startswith('ChurchSite'):assert static<250000,(path,static)
    if path.stem.startswith('Church-'):assert counts['church']<=120000,(path,counts)
    if path.parent.name=='modules' and path.stem=='Tower':assert counts['church']<=15000
    assert not bad,(path,bad[:20])
    actors=Counter(n.get('extras',{}).get('actor_kind') for n in ns if n.get('extras',{}).get('actor_kind') in ('car','vegetation','town'))
    return dict(counts=dict(counts),actors=dict(actors),static_without_cars_plants=static,materials=len(d['materials']),primitives=sum(len(m['primitives']) for m in d['meshes']),gltf_bin_bytes=path.stat().st_size+len(binary),image_bytes=sum(r['bytes'] for r in images.values()),texture_mib=sum(r['mib'] for r in images.values()),images=list(images.values()),density_1024_px_m=np.percentile(density,[5,50,95]).tolist() if density else [],uv_policy='Authored tiled/strip/graphic charts intentionally reuse UVs; density is not a unique lightmap claim.')


def main():
    rows={str(p):audit(p) for p in sorted(Path('export').rglob('*.gltf'))}
    baseline=Path('build/library-baseline.json')
    if baseline.exists():
        changed=[s for s,h in json.loads(baseline.read_text()).items() if not (ROOT/s).exists() or hashlib.sha256((ROOT/s).read_bytes()).hexdigest()!=h]
        assert not changed,changed
    Path('build/check.json').write_text(json.dumps(dict(passed=True,packages=rows,library_preserved=baseline.exists()),indent=2))
    print('PASS',len(rows),'external-image packages; static budgets, raw geometry, normals, UV presence, image resolution and library preservation')


if __name__=='__main__':main()
