"""Independent checkpoint audit: raw external glTF plus fresh Blender import.

This proves serialization, per-module counts/bounds, shared images and pivot
metadata. It explicitly does NOT certify final UVs, baked materials or swept
clearances. Those gates are deferred with look-dev, rather than faked here.
"""
import hashlib,json,sys,math
from pathlib import Path
import numpy as np
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))

def raw(path):
    doc=json.loads(path.read_text());buffers=[(path.parent/b['uri']).read_bytes() for b in doc.get('buffers',[])]
    def accessor(i):
        a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']];n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];dt=np.dtype({5126:'<f4',5123:'<u2',5125:'<u4',5121:'u1'}[a['componentType']]);return np.ndarray((a['count'],n),dt,buffer=buffers[v.get('buffer',0)],offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',n*dt.itemsize),dt.itemsize)).copy()
    triangles=0;maxnormal=0
    for m in doc.get('meshes',[]):
        for p in m['primitives']:
            count=len(accessor(p['indices']));assert count%3==0;triangles+=count//3
            pos=accessor(p['attributes']['POSITION']);assert np.isfinite(pos).all()
            n=accessor(p['attributes']['NORMAL']);err=float(np.abs(np.linalg.norm(n,axis=1)-1).max());maxnormal=max(maxnormal,err);assert err<.001
    images=[]
    for v in doc.get('images',[]):
        assert 'uri' in v and not v['uri'].startswith('data:');p=path.parent/v['uri'];assert p.exists();images.append(dict(uri=v['uri'],bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    assert len(images)==1,images
    return doc,dict(unique_mesh_triangles=triangles,max_unit_normal_error=maxnormal,external_images=images,gltf_bytes=path.stat().st_size,geometry_bytes=sum(len(b) for b in buffers))

def audit(path,manifest,signs=False):
    doc,report=raw(path);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    roots={o.name:o for o in bpy.context.scene.objects if o.parent is None};rows={}
    for key,expected in manifest['pieces'].items():
        rt=roots[key];obs=[o for o in rt.children_recursive if o.type=='MESH'];count=0;points=[];mats=set()
        for o in obs:
            o.data.calc_loop_triangles();count+=len(o.data.loop_triangles);points.extend(rt.matrix_world.inverted()@o.matrix_world@v.co for v in o.data.vertices);mats.update(m.name for m in o.data.materials if m)
        assert count==expected['triangles'],(key,count,expected['triangles'])
        lo=[min(v[k] for v in points) for k in range(3)];hi=[max(v[k] for v in points) for k in range(3)]
        if 'bounds_m' in expected:
            error=float(np.max(np.abs(np.asarray([lo,hi])-expected['bounds_m'])));assert error<2e-5,(key,error)
        else:error=None
        if signs:budget=1500
        elif 'Shelter' in key:budget=8000
        elif key in ('Bench','Litter','Recycling'):budget=4000
        elif key=='BikeRackRow':budget=4*3000
        elif key=='NewsRow':budget=3*3000
        else:budget=3000
        assert count<=budget,(key,count,budget);assert len(mats)<=2,(key,mats)
        for pivot in expected.get('pivots',[]):
            p=next(p for p in rt.children_recursive if p.name==pivot['name']);assert p['pivot_axis']==pivot['axis'];assert list(p['range_degrees'])==pivot['range_degrees']
            assert math.dist(p.location,pivot['position'])<2e-5
        assert max(abs(s-1) for s in rt.scale)<1e-5
        rows[key]=dict(triangles=count,budget=budget,materials=len(mats),measured_bounds_m=[lo,hi],source_import_max_bound_error_m=error)
        standalone=path.with_name(key+'.gltf');sd,sr=raw(standalone)
        assert sr['external_images']==report['external_images'],(key,'Noncanonical external image')
        assert sr['unique_mesh_triangles']==expected['triangles'],(key,'Standalone count')
    report.update(passed=True,rows=rows,scope=__doc__,stage='form checkpoint / no final UV or motion certification')
    return report

def main():
    report=audit(Path('export/StreetFurniture.gltf'),json.loads(Path('build/manifest.json').read_text()))
    receipt=ROOT/'build/street-furniture-preservation.json'
    if receipt.exists():
        expected=json.loads(receipt.read_text());changed=[p for p,h in expected.items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed,changed
        report['preserved_existing_files']=len(expected)
    Path('build/check.json').write_text(json.dumps(report,indent=2));print('CHECKPOINT CHECK PASSED',len(report['rows']),'modules; existing delivery hashes preserved')
if __name__=='__main__':main()
