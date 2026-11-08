"""Fresh import, shared-image audit, tile UVs and unchanged floor/path proof.

Geometry construction tests are separate from source/export serialization.
Intentional tile UV reuse is checked against atlas bands, not falsely called
nonoverlapping lightmap islands. No reference pixel enters these checks.
"""
import hashlib,json,math,sys
from pathlib import Path
import bpy
import numpy as np
from PIL import Image
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
import geometry as G
from check import measured_height
from kit.image_io import read_png


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def preservation():
    baseline=json.loads(Path('build/lookdev/baseline.json').read_text());changed=[s for s,h in baseline.items() if sha(ROOT/s)!=h]
    external=json.loads(Path('build/lookdev/preservation-external.json').read_text());changed.extend(s for s,h in external.items() if sha(ROOT/s)!=h)
    assert not changed,changed
    return dict(original_garage_files=len(baseline),other_family_files=len(external),changed=changed)


def modules():
    results=[]
    for name,expected in json.loads(Path('build/lookdev/modules.json').read_text()).items():
        path=Path('export/lookdev/modules')/(name+'.gltf');bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
        meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];count=G.triangles(meshes);bounds=G.bounds(meshes)
        assert count==expected['triangles']<=(8000 if name.startswith('Tower') else 2000),(name,count)
        error=max(abs(bounds[i][j]-expected['bounds_m'][i][j]) for i in range(2) for j in range(3));assert error<.0001,(name,error)
        collapsed=0
        for ob in meshes:
            me=ob.data;me.calc_loop_triangles();uv=me.uv_layers.active;assert uv,name
            for tri in me.loop_triangles:
                c=[Vector(uv.data[i].uv) for i in tri.loops];area=abs((c[1]-c[0]).cross(c[2]-c[0]))/2
                if tri.area>1e-9 and area<1e-15:collapsed+=1
        assert collapsed==0,(name,collapsed)
        results.append(dict(name=name,triangles=count,bounds_max_error_m=error,collapsed_uv_triangles=collapsed))
    return results


def main():
    bake=json.loads(Path('build/lookdev/atlas-bake/ParkingGarage-bake.json').read_text())
    assert all(row['size']==4096 for row in bake['channels'].values())
    for folder,key in (('atlas-source','source_sha256'),('atlas-bake','baked_sha256')):
        assert all(sha(Path('build/lookdev')/folder/name)==digest for name,digest in bake[key].items())
    filtered=json.loads(Path('textures/lookdev/ship/texture-report.json').read_text())
    for channel,row in filtered.items():
        assert row['size']==[2048,2048]
        assert row['bytes']==Path(f'textures/lookdev/ship/T_ParkingGarage_{channel}.png').stat().st_size
    saved=preservation();module_results=modules();rows=[];canonical={};layout=json.loads(Path('build/lookdev/atlas-layout.json').read_text())
    bands=[v['rect'] for v in layout.values()];floor_prefixes=('Flat_','Ramp_','Grade slab','SpeedRamp','North end grade','Inner closure','End expansion','Pour joint','Ramp landing seal','Private entry','Tower_')
    for seed in (101,202):
        p=json.loads(Path(f'build/lookdev/look-{seed}.json').read_text());original=json.loads(Path(f'build/garage-{seed}.json').read_text())
        # The new checkpoint must retain the complete accepted generator plan.
        for key in ('stalls','paths','pedestrian_paths','towers','ramp_limits','floor_to_floor','structural_stations'):assert p[key]==original[key],(seed,key)
        path=Path(f'export/lookdev/ParkingGarageLook-{seed}.gltf');doc=json.loads(path.read_text())
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
        meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];tris=G.triangles(meshes);assert tris==p['garage_triangles']<300000
        raw=path.with_suffix('.bin').read_bytes();normal_error=0
        for mesh in doc['meshes']:
            for primitive in mesh['primitives']:
                acc=doc['accessors'][primitive['attributes']['NORMAL']];view=doc['bufferViews'][acc['bufferView']]
                values=np.ndarray((acc['count'],3),dtype='<f4',buffer=raw,offset=view.get('byteOffset',0)+acc.get('byteOffset',0),strides=(view.get('byteStride',12),4))
                normal_error=max(normal_error,float(np.max(np.abs(np.linalg.norm(values,axis=1)-1))))
        assert normal_error<.0002,(seed,normal_error)
        floor=[];density=[];uv_bad=0;collapsed=0
        for ob in meshes:
            me=ob.data;me.calc_loop_triangles();uv=me.uv_layers.active;assert uv,ob.name
            for t in me.loop_triangles:
                mat=me.materials[t.material_index];pts=[ob.matrix_world@me.vertices[i].co for i in t.vertices];cu=[Vector(uv.data[i].uv) for i in t.loops]
                actual=(pts[1]-pts[0]).cross(pts[2]-pts[0]);area=actual.length/2
                ua=abs((cu[1]-cu[0]).cross(cu[2]-cu[0]))/2
                if ua<1e-15 and area>1e-9:collapsed+=1
                if ob.name.startswith(floor_prefixes) and actual.z>0 and area>1e-10:floor.append([tuple(v) for v in pts])
                if not mat.name.startswith('Garage concrete'):continue
                vv=[v.y for v in cu]
                allowed=any(min(vv)>=b-2e-6 and max(vv)<=d+2e-6 for a,b,c,d in bands)
                uv_bad+=not allowed
                if area>.0001 and ua>0:density.append((2048*math.sqrt(ua/area),area))
        assert uv_bad==0,(seed,uv_bad)
        assert collapsed==0,(seed,'Collapsed UV triangles',collapsed)
        floor=np.asarray(floor,dtype=float);errors=[];unsupported=[]
        for row in original['paths']+original['pedestrian_paths']:
            for point in row['points']:
                actual=measured_height(floor,point)
                if actual is None:unsupported.append((row['name'],point))
                else:errors.append(abs(actual-point[2]))
        assert not unsupported,(seed,unsupported[:5]);assert max(errors)<.0001,(seed,max(errors))
        from headroom import measure
        headroom=measure(meshes,p,floor)
        images=[]
        for im in doc.get('images',[]):
            q=(path.parent/im['uri']).resolve();digest=sha(q);canonical.setdefault(digest,q)
            assert canonical[digest]==q,('Duplicate image path',q)
            with Image.open(q) as image:size=image.size
            images.append(dict(uri=im['uri'],sha256=digest,bytes=q.stat().st_size,size=size,mib=size[0]*size[1]*4/3/2**20))
        values=np.asarray([d[0] for d in density]);weights=np.asarray([d[1] for d in density]);order=np.argsort(values);cdf=np.cumsum(weights[order])/sum(weights)
        percentiles=np.interp([.05,.5,.95],cdf,values[order]).tolist()
        rows.append(dict(seed=seed,triangles=tris,materials=len(doc['materials']),images=images,texture_mib=sum(v['mib'] for v in images),
            gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,route_surface_samples=len(errors),max_route_height_error_m=max(errors),
            uv_band_violations=uv_bad,collapsed_uv_triangles=collapsed,raw_normal_max_unit_error=normal_error,headroom=headroom,area_weighted_density_p5_p50_p95=percentiles))
    for channel in ('BaseColor','Normal','ORM'):
        q=Path(f'textures/lookdev/ship/T_ParkingGarage_{channel}.png');arr=read_png(q);assert arr.shape[:2]==(2048,2048)
        if channel=='Normal':assert np.max(np.abs(np.linalg.norm(arr*2-1,axis=2)-1))<.008
    report=dict(passed=True,bake=bake,preservation=saved,modules=module_results,garages=rows,uv_contract='Manufacture tile reuse; no unique-lightmap overlap claim',shared_family_image_mib=sum(Image.open(p).width*Image.open(p).height*4/3/2**20 for p in canonical.values()))
    Path('build/lookdev/check.json').write_text(json.dumps(report,indent=2)+'\n');print('LOOK-DEV CHECK PASS',[(r['seed'],r['triangles'],r['max_route_height_error_m']) for r in rows],flush=True)


if __name__=='__main__':main()
