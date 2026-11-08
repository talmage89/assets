"""Independent raw-accessor and fresh-import form/construction checks.

Intentional tiling UV reuse is allowed; no unique lightmap/atlas overlap or
final baked-detail certification is claimed at this form checkpoint.
"""
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import numpy as np
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from preserve import check as preserved
from package import bundle


def accessor(d,bin,index):
    a=d['accessors'][index];v=d['bufferViews'][a['bufferView']]
    typ={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]
    n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
    offset=v.get('byteOffset',0)+a.get('byteOffset',0);stride=v.get('byteStride',np.dtype(typ).itemsize*n)
    return np.ndarray((a['count'],n),dtype=typ,buffer=bin,offset=offset,strides=(stride,np.dtype(typ).itemsize)).copy()


def raw(path):
    d=json.loads(path.read_text());binary=(path.parent/d['buffers'][0]['uri']).read_bytes();tris=0;norm=[];uv=[];flows=[]
    for me in d['meshes']:
        for pr in me['primitives']:
            inds=accessor(d,binary,pr['indices']).ravel();tris+=len(inds)//3
            v=accessor(d,binary,pr['attributes']['POSITION']);assert np.isfinite(v).all()
            n=accessor(d,binary,pr['attributes']['NORMAL']);norm.extend(np.linalg.norm(n,axis=1))
            if 'TEXCOORD_0' in pr['attributes']:
                u=accessor(d,binary,pr['attributes']['TEXCOORD_0']);assert np.isfinite(u).all()
                tv=v[inds.reshape(-1,3)];tu=u[inds.reshape(-1,3)]
                area=np.linalg.norm(np.cross(tv[:,1]-tv[:,0],tv[:,2]-tv[:,0]),axis=1)/2
                ua=abs(np.cross(tu[:,1]-tu[:,0],tu[:,2]-tu[:,0]))/2
                valid=(area>1e-9)&(ua>1e-12)
                if valid.any():uv.extend(np.sqrt(ua[valid]/area[valid])*1024)
            if '_FLOW' in pr['attributes']:flows.extend(accessor(d,binary,pr['attributes']['_FLOW']))
    norm=np.array(norm);assert abs(norm-1).max()<.002
    flow=np.array(flows);assert len(flow)>1000,(path,'No exported flow')
    assert (flow[:,1]>.005).all() and flow[:,2].max()>1
    assert all((path.parent/im['uri']).is_file() for im in d.get('images',[]))
    # Expanded triangles count mesh reuse through nodes, not only stored meshes.
    expanded=sum(sum(d['accessors'][pr['indices']]['count']//3 for pr in d['meshes'][n['mesh']]['primitives']) for n in d['nodes'] if 'mesh' in n)
    return dict(stored_triangles=tris,placed_triangles=expanded,materials=len(d['materials']),images=len(d.get('images',[])),
        normal_length_error=float(abs(norm-1).max()),density_at_1024_px_m=np.percentile(uv,[5,50,95]).tolist(),
        flow_vertices=len(flow),flow_speed_m_s=np.percentile(np.linalg.norm(flow[:,:2],axis=1),[0,50,100]).tolist(),
        max_flow_depth_m=float(flow[:,2].max()),bytes_gltf=path.stat().st_size,bytes_bin=len(binary),bundle_sha256=bundle(path))


def bvh(ob):
    verts=[ob.matrix_world@v.co for v in ob.data.vertices];faces=[list(f.vertices) for f in ob.data.polygons]
    return BVHTree.FromPolygons(verts,faces,all_triangles=True)


def construction(seed):
    path=Path('export')/f'RiverCrossing-{seed}.gltf';bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
    obs=list(bpy.context.scene.objects);meta=json.loads(Path(f'build/RiverCrossing-{seed}.json').read_text())
    counts={}
    for ob in obs:
        if ob.type!='MESH':continue
        ob.data.calc_loop_triangles();key=ob.get('river_category','context');counts[key]=counts.get(key,0)+len(ob.data.loop_triangles)
    assert counts==meta['triangles'],(counts,meta['triangles'])
    assert counts['bridge']<80000 and counts['reach']<150000
    pads=[bvh(o) for o in obs if o.type=='MESH' and o.name.startswith('BearingStation')]
    gaps=[];lengths=[]
    for ob in obs:
        if ob.type!='MESH' or not ob.name.startswith('Girder_'):continue
        ps=[ob.matrix_world@v.co for v in ob.data.vertices];xmin=min(p.x for p in ps);xmax=max(p.x for p in ps);y=(min(p.y for p in ps)+max(p.y for p in ps))/2;z=min(p.z for p in ps)
        lengths.append(xmax-xmin)
        for x in (xmin+.26,xmax-.26):
            origin=Vector((x,y,z+.001));hits=[tree.ray_cast(origin,Vector((0,0,-1)),.6)[0] for tree in pads]
            hit=[h for h in hits if h is not None];assert hit,('Unsupported girder',ob.name,x)
            gaps.append(min(abs(z-h.z) for h in hit))
    assert max(gaps)<.002,('Girder/pad gap',max(gaps))
    # Sample actual imported reach cross-sections, not declared width constants.
    bed=next(o for o in obs if o.name=='BedBanksFloodplain');tree=bvh(bed);water=next(o for o in obs if o.name=='WaterSurface')
    samples=[]
    for y in (-80,0,40,75):
        row=[v.co for v in water.data.vertices if abs(v.co.y-y)<.02]
        if not row:continue
        world=[water.matrix_world@v for v in row];samples.append(dict(y_m=y,width_m=max(v.x for v in world)-min(v.x for v in world)))
    return dict(categories=counts,bearing_surface_samples=len(gaps),max_girder_pad_gap_m=max(gaps),girder_lengths_m=sorted(set(round(x,5) for x in lengths)),water_width_samples=samples)


def main():
    results={}
    for seed in (101,202):results[str(seed)]=dict(raw=raw(Path(f'export/RiverCrossing-{seed}.gltf')),construction=construction(seed))
    modules=json.loads(Path('build/manifest.json').read_text())['modules']
    for m in modules:assert m['triangles']<=m['limit']
    report=dict(passed=True,crossings=results,modules=modules,preserved_files=preserved(),
        scope='form, raw normals/finite tiling UV/density, flow, actual bearing contacts and serialization')
    Path('build/check.json').write_text(json.dumps(report,indent=2)+'\n');print('RIVER_CHECK_PASS')


if __name__=='__main__':main()
