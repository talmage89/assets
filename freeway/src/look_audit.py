"""Raw external glTF PBR/UV/geometry audit; no Blender import required."""
import hashlib,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image


def raw(path):
    path=Path(path);doc=json.loads(path.read_text());buffers=[(path.parent/b['uri']).read_bytes() for b in doc['buffers']]
    def accessor(i):
        a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']];dt=np.dtype({5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]);n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
        return np.ndarray((a['count'],n),dtype=dt,buffer=buffers[v['buffer']],offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',n*dt.itemsize),dt.itemsize))
    geometry={};densities=[];degenerate=0;textured_degenerate=0
    for material in doc.get('materials',[]):
        pbr=material.get('pbrMetallicRoughness',{})
        for key in ('metallicFactor','roughnessFactor'):
            assert 0<=pbr.get(key,1)<=1,(path,material['name'],key,pbr.get(key))
    for i,mesh in enumerate(doc.get('meshes',[])):
        count=0
        for p in mesh['primitives']:
            a=p['attributes'];v=accessor(a['POSITION']);idx=accessor(p['indices']).ravel().reshape(-1,3);n=accessor(a['NORMAL']);uv=accessor(a['TEXCOORD_0'])
            assert np.isfinite(v).all() and np.isfinite(uv).all();assert abs(np.linalg.norm(n,axis=1)-1).max()<.003;assert idx.max()<len(v)
            tri=v[idx];area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2;assert area.min()>1e-12,(path,mesh['name'])
            tuv=uv[idx];duv=tuv[:,1]-tuv[:,0];euv=tuv[:,2]-tuv[:,0];ua=abs(duv[:,0]*euv[:,1]-duv[:,1]*euv[:,0])/2;degenerate+=int((ua<1e-14).sum())
            mat=doc['materials'][p['material']]
            if mat.get('extras',{}).get('tiling_vertex_tint') is True:assert 'COLOR_0' in a,(path,mesh['name'],'Native tint dropped')
            base=mat.get('pbrMetallicRoughness',{}).get('baseColorTexture')
            if base:
                textured_degenerate+=int((ua<1e-14).sum())
                im=doc['images'][doc['textures'][base['index']]['source']];size=Image.open(path.parent/im['uri']).size
                values=np.sqrt(ua/area*size[0]*size[1]);densities.extend(values[ua>1e-14].tolist())
            count+=len(idx)
        geometry[i]=count
    assert textured_degenerate==0,(path,'Collapsed textured UVs',textured_degenerate)
    # Instance-expanded count, not just unique mesh triangles.
    count=sum(geometry[node['mesh']] for node in doc.get('nodes',[]) if 'mesh' in node)
    rows=[]
    for im in doc.get('images',[]):
        assert 'uri' in im and not im['uri'].startswith(('http:','https:','data:','/'));p=path.parent/im['uri'];assert p.is_file(),p
        with Image.open(p) as image:w,h=image.size
        rows.append(dict(uri=im['uri'],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size=[w,h],bytes=p.stat().st_size,bc_full_mips_mib=w*h*4/3/2**20))
    unique={r['sha256']:r for r in rows}
    return dict(triangles=count,unique_mesh_triangles=sum(geometry.values()),mesh_instances=sum('mesh' in n for n in doc.get('nodes',[])),unique_meshes=len(geometry),materials=len(doc.get('materials',[])),primitives=sum(len(m['primitives']) for m in doc.get('meshes',[])),gltf_bytes=path.stat().st_size,bin_bytes=sum(len(b) for b in buffers),images=list(unique.values()),image_bytes=sum(r['bytes'] for r in unique.values()),bc_full_mips_mib=sum(r['bc_full_mips_mib'] for r in unique.values()),degenerate_uv_triangles=degenerate,textured_degenerate_uv_triangles=textured_degenerate,uv_density_px_m_percentiles=np.quantile(densities,[.05,.5,.95]).tolist() if densities else None,uv_scope='Meter-scaled tiling and guarded chart reuse deliberately overlap. Collapsed UVs only on untextured native scalar materials are counted but unused. Density percentiles are unweighted per triangle, not a unique lightmap atlas certificate.')


def main():
    from context_colors import audit_exports
    audit_exports()
    result=dict(modules={},scenes={},texture_sets={},preservation={},scope='Raw serialized geometry/PBR/image/UV data; geometry contact and fresh-import checks are separate.')
    for path in sorted(Path('export/modules').glob('*.gltf')):
        row=raw(path);cap=50000 if path.stem=='Overpass' else 8000 if path.stem in ('SignTruss','Cantilever') else 2000
        assert row['triangles']<=cap,(path,row['triangles']);result['modules'][path.stem]=row
    union={}
    for seed in (101,202):
        rows={k:raw(f'export/{k}-{seed}.gltf') for k in ('Freeway','Town','Traffic')};assert rows['Freeway']['triangles']<400000
        for k,row in rows.items():
            source=json.loads(Path(f'build/scene-{seed}.json').read_text());expected=source['triangles'] if k=='Freeway' else source[k.lower() if k=='Traffic' else 'context']['triangles'];assert row['triangles']==expected,(k,row['triangles'],expected)
            for im in row['images']:union[im['sha256']]=im
        result['scenes'][str(seed)]=rows
    from textures import SETS
    for name,spec in SETS.items():
        files=[Path('textures/ship')/f'T_{name}_{c}.png' for c in ('BaseColor','Normal','ORM')]
        assert all(Image.open(f).size==(spec['size'],)*2 for f in files)
        for f in files:assert f.exists()
        normal=np.asarray(Image.open(files[1]).convert('RGB'),np.float32)/127.5-1
        error=float(abs(np.linalg.norm(normal,axis=2)-1).max());assert error<.008,(name,error)
        result['texture_sets'][name]=dict(**spec,png_bytes=sum(f.stat().st_size for f in files),bc_full_mips_mib=3*spec['size']**2*4/3/2**20,normal_max_length_error=error,bake=json.loads((Path('textures/bake')/(name+'-bake.json')).read_text()))
    root=Path(__file__).resolve().parents[2]
    p=Path('build/session-preservation.json')
    if p.exists():
        preserved=json.loads(p.read_text())
        for name,h in preserved.items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h,('Existing delivery changed',name)
        result['preservation']=dict(files=len(preserved),passed=True)
    final=Path('build/final-preservation.json')
    if final.exists():
        preserved=json.loads(final.read_text())
        for name,h in preserved.items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h,('Existing delivery changed',name)
        result['preservation']['final_session_files']=len(preserved)
    result['shared_image_union']=dict(unique_images=len(union),bc_full_mips_mib=sum(r['bc_full_mips_mib'] for r in union.values()),png_bytes=sum(r['bytes'] for r in union.values()))
    Path('build/look-audit.json').write_text(json.dumps(result,indent=2));print('LOOK AUDIT PASSED',[(k,{n:r['triangles'] for n,r in v.items()}) for k,v in result['scenes'].items()])
if __name__=='__main__':main()
