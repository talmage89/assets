"""Independent external glTF UV density, image allocation and package receipts.

Intentional tile/chart reuse is reported explicitly; this is not a lightmap
unwrap or a claim of globally disjoint tiling UVs.
"""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image


def accessor(d,b,index):
    a=d['accessors'][index];v=d['bufferViews'][a['bufferView']]
    dtype=np.dtype({5121:'u1',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']]);n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
    return np.ndarray((a['count'],n),dtype=dtype,buffer=b,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',dtype.itemsize*n),dtype.itemsize))


def percentiles(values,weights):
    ids=np.argsort(values);q=np.cumsum(weights[ids]);q=q/q[-1]
    return np.interp((.05,.50,.95),q,values[ids]).tolist()


def main():
    report={};unique={};root=Path('..').resolve()
    shared_folders=[root/p for p in ('ground/textures/ship','commercial/textures/ship','houses/textures/ranch-ship','trees/textures/ship','trees/textures/oak/ship','fences/chain-link/textures/ship')]
    for seed in (101,102,103):
        for kind in ('School','Campus'):
            path=Path('export')/f'{kind}-{seed}.gltf';d=json.loads(path.read_text());binary=(path.parent/d['buffers'][0]['uri']).read_bytes();stats={}
            images=[]
            for row in d.get('images',[]):
                f=(path.parent/row['uri']).resolve();im=Image.open(f)
                native_shrub=f.parent==Path('textures/checkpoint').resolve() and f.name.startswith('T_Shrubs_')
                school_light=f==Path('textures/ship/T_School_Light_Emission.png').resolve()
                assert f.parent in shared_folders or native_shrub or school_light,(path,'unexpected school-owned image',row['uri'])
                r=dict(uri=row['uri'],pixels=im.size,bytes=f.stat().st_size,gpu_mib_8bpp_mips=im.width*im.height*4/3/1048576,sha256=hashlib.sha256(f.read_bytes()).hexdigest())
                images.append(r);unique[str(f)]=r
            for mesh in d['meshes']:
                for prim in mesh['primitives']:
                    if 'TEXCOORD_0' not in prim['attributes']:continue
                    mat=d['materials'][prim['material']];name=mat['name'];ids=accessor(d,binary,prim['indices']).astype(int).ravel().reshape(-1,3)
                    xyz=accessor(d,binary,prim['attributes']['POSITION']).astype(float)[ids];uv=accessor(d,binary,prim['attributes']['TEXCOORD_0']).astype(float)[ids]
                    area=np.linalg.norm(np.cross(xyz[:,1]-xyz[:,0],xyz[:,2]-xyz[:,0]),axis=1)/2
                    ab,ac=uv[:,1]-uv[:,0],uv[:,2]-uv[:,0];ua=abs(ab[:,0]*ac[:,1]-ab[:,1]*ac[:,0])/2
                    entry=stats.setdefault(name,dict(density=[],area=[],triangles=0,degenerate_uv=0,outside_unit_square=0))
                    entry['triangles']+=len(ids);entry['degenerate_uv']+=int((ua<1e-14).sum());entry['outside_unit_square']+=int(((uv<0)|(uv>1)).any(axis=(1,2)).sum())
                    tx=mat.get('normalTexture') or mat.get('pbrMetallicRoughness',{}).get('baseColorTexture')
                    if tx:
                        image=images[d['textures'][tx['index']]['source']];pixels=image['pixels'][0]*image['pixels'][1];mask=(area>1e-12)&(ua>1e-14)
                        entry['density']+=np.sqrt(ua[mask]*pixels/area[mask]).tolist();entry['area']+=area[mask].tolist()
            for ma,row in stats.items():
                values=np.asarray(row.pop('density'));weights=np.asarray(row.pop('area'))
                row['area_weighted_density_p5_p50_p95_px_m']=percentiles(values,weights) if len(values) else None
                if kind=='School':assert row['degenerate_uv']==0,(path,ma,row['degenerate_uv'])
            files=[path]+[path.parent/r['uri'] for k in ('buffers','images') for r in d.get(k,[])]
            digest=hashlib.sha256(b''.join(hashlib.sha256(p.read_bytes()).digest() for p in files)).hexdigest()
            report[path.stem]=dict(materials=len(d['materials']),images=images,shared_gpu_mib=sum(r['gpu_mib_8bpp_mips'] for r in images),gltf_bin_bytes=path.stat().st_size+len(binary),surfaces=stats,package_sha256=digest)
    report['all_schools_shared_images']=dict(images=len(unique),gpu_mib=sum(r['gpu_mib_8bpp_mips'] for r in unique.values()),bytes=sum(r['bytes'] for r in unique.values()),files=list(unique.values()),new_school_sets=0)
    report['uv_scope']='Meter-scaled manufacture tiles and guarded Equipment swatches intentionally overlap/repeat; no unique bake or lightmap packing is claimed. Densities use exported float positions/UVs and image dimensions, weighted by actual surface area.'
    Path('build/delivery-audit.json').write_text(json.dumps(report,indent=2));print('SCHOOL SHARED-PBR AUDIT PASS',report['all_schools_shared_images']['images'],'unique images')

if __name__=='__main__':main()
