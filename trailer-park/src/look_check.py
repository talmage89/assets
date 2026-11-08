"""Independent shipped UV-cell, PBR resource, density and instance audit."""
import hashlib,json,sys,math
from pathlib import Path
import numpy as np
from PIL import Image
sys.path[:0]=[str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parents[2])]
from kit.gltf import GLB
from textures import RECTS


def raw(path):
    g=GLB.__new__(GLB);g.json=json.loads(path.read_text());g.binary=(path.parent/g.json['buffers'][0]['uri']).read_bytes()
    g.parents={c:i for i,n in enumerate(g.json['nodes']) for c in n.get('children',[])};return g


def audit():
    result={};all_images={}
    for path in sorted(Path('export').glob('*.gltf')):
        g=raw(path);d=g.json;unique=0;placed=0;draws=0;densities={};areas={};cells=0
        for mesh in d['meshes']:
            for pr in mesh['primitives']:
                idx=g.accessor(pr['indices']).ravel().reshape(-1,3);unique+=len(idx)
                ma=d['materials'][pr['material']];name=ma['name'];uv=g.accessor(pr['attributes']['TEXCOORD_0'])
                if name.startswith('ManufacturedSoilFringe'):
                    assert ma.get('alphaMode')=='BLEND' and ma.get('doubleSided')
                    color=g.accessor(pr['attributes']['COLOR_0'])
                    assert color.shape[1]==4 and color[:,3].min()<.001 and color[:,3].max()>.8,(path,'Lost soil edge opacity')
                v=g.accessor(pr['attributes']['POSITION']);uv=uv[idx];v=v[idx]
                a=np.linalg.norm(np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]),axis=1)/2
                delta0=uv[:,1]-uv[:,0];delta1=uv[:,2]-uv[:,0];ua=abs(delta0[:,0]*delta1[:,1]-delta0[:,1]*delta1[:,0])/2
                assert np.all(ua>1e-13),(path.name,name,'collapsed UV')
                if name.startswith(('ManufacturedPBR','ManufacturedPatina','ManufacturedGrassBlades')):
                    pbr=ma['pbrMetallicRoughness'];assert all(k in pbr for k in ('baseColorTexture','metallicRoughnessTexture')) and 'normalTexture' in ma
                    if name=='ManufacturedPBR_Metal':
                        assert 'COLOR_0' in pr['attributes'],(path,'Lost authored finish tint')
                        color=g.accessor(pr['attributes']['COLOR_0'])
                        assert np.min(color[:,:3])<.95,(path,mesh['name'],'White replacement of authored finish tint')
                    if name=='ManufacturedPBR_Grass':
                        assert 'COLOR_0' in pr['attributes'],(path,'Lost blade tint')
                        color=g.accessor(pr['attributes']['COLOR_0'])
                        assert color[:,1].mean()>color[:,0].mean() and color[:,:3].max()<.5,(path,'Invalid July blade hue/value')
                    if name=='ManufacturedPatina':
                        assert ma.get('alphaMode')=='BLEND' and not ma.get('doubleSided',False)
                        rgba=g.accessor(pr['attributes']['COLOR_0'])
                        # glTF may omit an all-one alpha component. Full
                        # severity stays VEC3 white; weaker skins need VEC4.
                        assert rgba.shape[1] in (3,4) and np.all(rgba[:,:3]==1),(path,'Changed neutral weather tint')
                        if rgba.shape[1]==4:assert np.all((rgba[:,3]>0)&(rgba[:,3]<=1)),(path,'Lost seeded weather coverage')
                    if name=='ManufacturedGrassBlades':
                        assert ma.get('alphaMode')=='MASK' and ma.get('doubleSided')
                    tex=d['textures'][pbr['baseColorTexture']['index']];im=d['images'][tex['source']];w,h=Image.open(path.parent/im['uri']).size
                    density=np.sqrt(ua*w*h/np.maximum(a,1e-20));densities.setdefault(name,[]).extend(density.tolist());areas.setdefault(name,[]).extend(a.tolist())
                    if name in ('ManufacturedPBR_Metal','ManufacturedPatina','ManufacturedGrassBlades'):
                        uv=uv.copy();uv[:,:,1]=1-uv[:,:,1]
                        inside=np.zeros(len(uv),bool)
                        charts=[RECTS['Plain']] if name=='ManufacturedPBR_Grass' else RECTS.values()
                        for u0,v0,u1,v1 in charts:inside|=((uv[:,:,0]>=u0-1e-5)&(uv[:,:,0]<=u1+1e-5)&(uv[:,:,1]>=v0-1e-5)&(uv[:,:,1]<=v1+1e-5)).all(axis=1)
                        assert inside.all(),(path.name,'chart crosses shared-cell boundary',int((~inside).sum()))
                        cells+=len(uv)
        for node in d['nodes']:
            if 'mesh' in node:
                for pr in d['meshes'][node['mesh']]['primitives']:placed+=d['accessors'][pr['indices']]['count']//3;draws+=1
        images={}
        for im in d.get('images',[]):
            p=(path.parent/im['uri']).resolve();sha=hashlib.sha256(p.read_bytes()).hexdigest();w,h=Image.open(p).size
            images[sha]=dict(uri=im['uri'],bytes=p.stat().st_size,size=[w,h],mipped_8bpp_mib=w*h*4/3/1048576);all_images[sha]=images[sha]
        stats={}
        for name,values in densities.items():
            order=np.argsort(values);v=np.asarray(values)[order];weights=np.asarray(areas[name])[order];cdf=np.cumsum(weights)/sum(weights)
            stats[name]=dict(area_weighted_p5_median_p95_px_m=np.interp((.05,.5,.95),cdf,v).tolist(),area_m2=float(sum(weights)))
        meta=json.loads(path.with_suffix('.json').read_text());assert placed==meta['triangles'] and unique==meta['unique_export_triangles']
        if path.stem.startswith('Park'):
            assert unique<placed*.60,(path,'lost mesh sharing',unique,placed)
            density=meta['homes_per_acre'];assert 8<=density<=10 if meta['plan']['kind']=='old' else 5.5<=density<=6.5
        result[path.stem]=dict(placed_triangles=placed,unique_triangles=unique,materials=len(d['materials']),unbatched_primitives=draws,
                              geometry_bytes=meta['geometry_bytes'],shared_cell_triangles=cells,density=stats,images=list(images.values()),gpu_mib=sum(im['mipped_8bpp_mib'] for im in images.values()))
    new=[]
    for channel in ('BaseColor','Normal','ORM'):
        p=Path('textures/ship')/f'T_Manufactured_{channel}.png';im=Image.open(p);assert im.size==(2048,2048);new.append(dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
        if channel=='Normal':
            vectors=np.asarray(im,dtype=float)/255*2-1;error=float(abs(np.linalg.norm(vectors,axis=-1)-1).max())
            assert error<.007,('Shipped tangent normal length',error)
            new[-1]['max_unit_length_error']=error
    report=dict(passed=True,scope='Metric repeat UVs intentionally overlap; triangle containment in declared atlas cells, not a unique lightmap pack',exports=result,new_set=dict(size=2048,gpu_mib=16,images=new),union_gpu_mib=sum(im['mipped_8bpp_mib'] for im in all_images.values()))
    assert report['union_gpu_mib']<=176.05,('Accepted static image budget exceeded',report['union_gpu_mib'])
    Path('build/look-check.json').write_text(json.dumps(report,indent=2));print('LOOK CHECK PASS',len(result),'exports; new set 16 MiB')


if __name__=='__main__':audit()
