"""Read raw external glTF buffers/maps, plus containment and chart measurements.

UV manufacture-chart reuse is deliberate. This measures density and degenerate
UVs; it does not pretend repeated charts are a unique zero-overlap atlas.
"""
import json,hashlib,struct,math,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.image_io import read_png


def accessor(d,bs,i):
    a=d['accessors'][i];b=d['bufferViews'][a['bufferView']];typ={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']];n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']];t=np.dtype(typ)
    return np.ndarray((a['count'],n),dtype=t,buffer=bs[b['buffer']],offset=b.get('byteOffset',0)+a.get('byteOffset',0),strides=(b.get('byteStride',t.itemsize*n),t.itemsize))

def inside(p,poly):
    x,y=p;hit=False
    for i,a in enumerate(poly):
        b=poly[(i+1)%len(poly)]
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:hit=not hit
    return hit

def heights(tris,point):
    p=np.asarray(point);a=tris[:,0,:2];b=tris[:,1,:2];c=tris[:,2,:2];u=b-a;v=c-a;q=p-a;det=u[:,0]*v[:,1]-u[:,1]*v[:,0];valid=np.abs(det)>1e-12;safe=np.where(valid,det,1)
    s=(q[:,0]*v[:,1]-q[:,1]*v[:,0])/safe;t=(u[:,0]*q[:,1]-u[:,1]*q[:,0])/safe
    hit=valid&(s>=-1e-6)&(t>=-1e-6)&(s+t<=1+1e-6)
    return (tris[:,0,2]+s*(tris[:,1,2]-tris[:,0,2])+t*(tris[:,2,2]-tris[:,0,2]))[hit]

def terrain(doc,path,material):
    bs=[(path.parent/x['uri']).read_bytes() for x in doc['buffers']];out=[]
    for mesh in doc.get('meshes',[]):
        for pr in mesh['primitives']:
            if doc['materials'][pr['material']]['name']!=material:continue
            pos=accessor(doc,bs,pr['attributes']['POSITION']);idx=accessor(doc,bs,pr['indices']).ravel().reshape(-1,3);p=pos[idx]
            # Siteworks has identity root transforms. Convert glTF +Y-up to
            # the authored Blender footprint before sampling actual triangles.
            q=np.stack((p[:,:,0],-p[:,:,2],p[:,:,1]),axis=-1);n=np.cross(q[:,1]-q[:,0],q[:,2]-q[:,0]);valid=(n[:,2]>1e-8)&(q[:,:,2].max(axis=1)<.03)&(q[:,:,2].min(axis=1)>-.3)
            out.extend(q[valid])
    return np.asarray(out)

def main():
    report=dict(passed=True,sets={},sites={},pieces={});memory=0
    for name,n in [('PlayMetal',1024),('PlayPlastic',1024),('PlaySurface',2048)]:
        maps={}
        for c in ('BaseColor','Normal','ORM'):
            p=Path('textures/ship')/f'T_{name}_{c}.png';im=Image.open(p);assert im.size==(n,n),(p,im.size)
            maps[c]=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size=list(im.size))
            if c=='Normal':
                a=read_png(p)[:,:,:3]*2-1;error=np.abs(np.linalg.norm(a,axis=-1)-1);assert error.max()<.012,(p,float(error.max()));maps[c]['max_unit_length_error']=float(error.max())
        mem=3*n*n*4/3/1024**2;memory+=mem;report['sets'][name]=dict(maps=maps,compressed_full_mips_MiB=mem)
        bake=json.loads(Path(f'textures/bake/{name}-bake.json').read_text());assert bake['channels']['BaseColor']['size']==4096;report['sets'][name]['bake']=bake
    assert memory==24;report['family_MiB']=memory
    manifest=json.loads(Path('build/manifest.json').read_text())
    for name in manifest['pieces']:
        p=Path('export')/(name+'.gltf');d=json.loads(p.read_text());bs=[(p.parent/x['uri']).read_bytes() for x in d['buffers']];dens=[];zero=0;triangles=0;tiles=set()
        for mesh in d.get('meshes',[]):
            for primitive in mesh['primitives']:
                m=d['materials'][primitive['material']];attrs=primitive['attributes'];pos=accessor(d,bs,attrs['POSITION']);uv=accessor(d,bs,attrs['TEXCOORD_0']);ix=accessor(d,bs,primitive['indices']).ravel().reshape(-1,3)
                assert np.isfinite(uv).all();assert uv.min()>-1e-6 and uv.max()<1+1e-6,(name,float(uv.min()),float(uv.max()))
                pp=pos[ix];vv=uv[ix];area=np.linalg.norm(np.cross(pp[:,1]-pp[:,0],pp[:,2]-pp[:,0]),axis=1)/2
                a=vv[:,1]-vv[:,0];b=vv[:,2]-vv[:,0];ua=np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0])/2
                valid=area>1e-10;bad=(ua<1e-12)&valid;zero+=int(bad.sum());triangles+=len(ix)
                dens.extend(np.sqrt(ua[valid]/area[valid])*1024)
                if 'baseColorTexture' in m.get('pbrMetallicRoughness',{}):
                    ti=m['pbrMetallicRoughness']['baseColorTexture']['index'];im=d['images'][d['textures'][ti]['source']]['uri'];tiles.add(im)
                    assert Path(p.parent/im).exists()
        # Tiny closed-cylinder caps can be below a delivered texel. Their count
        # remains explicit; a meaningful surface with collapsed UVs fails.
        report['pieces'][name]=dict(triangles=triangles,degenerate_uv_triangles=zero,density_px_m_p5_median_p95=np.percentile(dens,[5,50,95]).tolist(),images=sorted(tiles))
        assert zero==0,(name,zero)
    for s in manifest['sites']:
        poly=s['containment_boundary_m'];corners=[]
        for z in s['zones']:
            a,b,c,d=z['rect']
            for p in ((a,b),(c,b),(c,d),(a,d)):assert inside(p,poly),(s['seed'],'zone beyond containment',z['group'],p);corners.append(p)
        p=Path('export')/f'Playground-{s["seed"]}.gltf';d=json.loads(p.read_text());imgs=[]
        floor=terrain(d,p,'Playground_Site');concrete=terrain(d,p,'Concrete');measured_corners=[]
        for point in corners:
            values=heights(floor,point);assert len(values),(s['seed'],'no actual protective surface',point);measured_corners.append(float(values.min()))
        entry=[];y0=s['surface'][1]
        for x in (-.8,0,.8):
            point=(x,y0+.299);a=heights(floor,point);b=heights(concrete,point);assert len(a) and len(b),(s['seed'],'entry surface absent',point)
            difference=float(min(abs(v-w) for v in a for w in b));assert difference<.012,(s['seed'],'entry lip',difference);entry.append(difference)
        for im in d.get('images',[]):
            ip=(p.parent/im['uri']).resolve();assert ip.exists();assert 'data:' not in im['uri'];imgs.append(dict(uri=im['uri'],sha256=hashlib.sha256(ip.read_bytes()).hexdigest()))
        report['sites'][str(s['seed'])]=dict(triangles=s['total_triangles'],materials=s['materials'],files_bytes=p.stat().st_size+p.with_suffix('.bin').stat().st_size,zone_corners_inside=len(corners),actual_floor_samples_m=measured_corners,entry_floor_max_difference_m=max(entry),containment_area_m2=s['protected_surface_area_m2'],images=imgs)
        assert s['total_triangles']<120000
    protected=ROOT/'build/playground-protected.json'
    if protected.exists():
        data=json.loads(protected.read_text());bad=[k for k,v in data.items() if not (ROOT/k).exists() or hashlib.sha256((ROOT/k).read_bytes()).hexdigest()!=v];assert not bad,bad;report['protected_delivery_files']=len(data)
    Path('build/lookdev-check.json').write_text(json.dumps(report,indent=2));print('LOOKDEV CHECK PASS',len(report['pieces']),'pieces;',report['family_MiB'],'MiB')
if __name__=='__main__':main()
