"""Source construction plus standard glTF PBR/tint serialization, without bake.

The diagnostic GLB is deliberately not a finished delivery. Texture resolution
and compressed GPU estimates are separate from PNG/file size measurements.
"""
import hashlib
import json
from pathlib import Path
import sys
import bpy
from mathutils.kdtree import KDTree
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit import tiling,gltf
from check_mesh import source_check
from glb_budget import compact


def main():
    source=Path('build/lookdev.blend');report=dict(source=source_check(source))
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];colors=[];material_names=set()
    for ob in meshes:
        assert len(ob.data.uv_layers)==1
        a=ob.data.color_attributes['Tint'];assert a.domain=='POINT'
        colors.extend(tuple(c.color[:3]) for c in a.data)
        for p in ob.data.polygons:material_names.add(ob.data.materials[p.material_index].name)
    assert len(material_names)==6
    assert all(0<=c<=1 for row in colors for c in row)
    source_points=[(tuple(ob.matrix_world@v.co),tuple(ob.data.color_attributes['Tint'].data[v.index].color[:3]))
        for ob in meshes for v in ob.data.vertices]
    tree=KDTree(len(source_points))
    for i,(p,c) in enumerate(source_points):tree.insert(p,i)
    tree.balance()
    pivots={name:tuple(bpy.data.objects[name].matrix_world.translation) for name in ('FrontDoor','PatioDoor','ServiceDoor')}
    moving={bpy.data.objects[name] for name in ('FrontDoor','PatioDoor','ServiceDoor')}
    static=[o for o in meshes if o.parent not in moving]
    bpy.ops.object.select_all(action='DESELECT')
    for ob in static:ob.select_set(True)
    bpy.context.view_layer.objects.active=static[0];bpy.ops.object.join();static[0].name='House_Static'
    path=Path('build/lookdev-proof.glb');tiling.export(path);size=compact(path)
    raw=gltf.GLB(path);doc=raw.json;error=0;count=0;semantics=set();position_error=0
    import numpy as np
    for ni,node in enumerate(doc['nodes']):
        if 'mesh' not in node:continue
        mesh=doc['meshes'][node['mesh']];matrix=raw.world(ni)
        for primitive in mesh['primitives']:
            attrs=primitive['attributes'];semantics.update(attrs)
            for ai in attrs.values():
                a=doc['accessors'][ai];v=doc['bufferViews'][a['bufferView']]
                components={'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
                size={5121:1,5123:2,5126:4}[a['componentType']]*components
                assert a.get('byteOffset',0)%4==0 and v.get('byteStride',size)%4==0
            count+=len(raw.accessor(primitive['indices']))//3
            positions=raw.accessor(attrs['POSITION']);tints=raw.accessor(attrs['COLOR_0'])[:,:3]
            for p,rgb in zip(positions,tints):
                q=matrix@np.r_[p,1];point=(q[0],-q[2],q[1]);nearest=tree.find(point)
                position_error=max(position_error,nearest[2]);matches=tree.find_range(point,2e-5)
                assert matches,'Export vertex has no source surface point'
                delta=min(max(abs(source_points[i][1][k]-rgb[k]) for k in range(3)) for _,i,_ in matches)
                error=max(error,delta)
    assert error<.5/255+1e-5 and position_error<2e-5
    assert count==report['source']['triangles'] and len(doc['meshes'])==4
    assert len(doc['materials'])==6 and len(doc['images'])==15
    assert semantics=={'POSITION','NORMAL','TEXCOORD_0','COLOR_0'}
    report.update(passed=True,glb=dict(file_bytes=path.stat().st_size,triangles=count,meshes=4,
        materials=6,images=15,source_to_export_tint_per_channel_error=error,source_to_export_position_error_m=position_error,
        attributes=sorted(semantics),extensions=doc.get('extensionsUsed',[]),size=size,
        scope='Standard PBR images/POINT vertex tint serialized, no custom shader; not a final bake/look comparison'),
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    import math
    report['glb']['reimport_pivot_error_m']=max(math.dist(bpy.data.objects[n].matrix_world.translation,p) for n,p in pivots.items())
    assert report['glb']['reimport_pivot_error_m']<2e-5
    Path('build/lookdev-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))


if __name__=='__main__':main()
