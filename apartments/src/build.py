"""Build the complete form checkpoint, exporting stock external-image glTF."""
import argparse
import json
from pathlib import Path
import sys
import bpy
import bmesh
import numpy as np
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from geometry import Assembly
from plans import garden,row,complex_plan,COMPLEX_SEEDS,ROW_SEEDS
from buildings import garden_building,townhouse
from siteworks import make_complex,row_site
from context import clear_templates,CACHE,parent_chain


def counts(root=None):
    bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and (root is None or root in parent_chain(o))]
    tris=0;materials=set();lo=Vector((1e10,)*3);hi=-lo
    for ob in obs:
        ob.data.calc_loop_triangles();tris+=len(ob.data.loop_triangles)
        for f in ob.data.polygons:materials.add(ob.data.materials[f.material_index].name)
        xyz=np.empty(len(ob.data.vertices)*3,dtype='float64');ob.data.vertices.foreach_get('co',xyz)
        xyz=xyz.reshape(-1,3);xf=np.array(ob.matrix_world);xyz=xyz@xf[:3,:3].T+xf[:3,3]
        if len(xyz):lo=Vector(np.minimum(lo,xyz.min(0)));hi=Vector(np.maximum(hi,xyz.max(0)))
    return dict(triangles=tris,materials=len(materials),bounds_min=list(lo),bounds_max=list(hi),size_m=list(hi-lo),meshes=len(obs))


def consolidate():
    """One mesh per static assembly or true moving pivot, preserve sockets."""
    bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH':continue
        if ob.modifiers:
            ob.data=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg,preserve_all_data_layers=True);ob.modifiers.clear()
        if not ob.data.uv_layers:
            uv=ob.data.uv_layers.new(name='UVMap')
            for f in ob.data.polygons:
                axes=sorted(range(3),key=lambda k:abs(f.normal[k]))[:2]
                for li in f.loop_indices:
                    v=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]],v[axes[1]])
    processed=set()
    parents=sorted({o.parent for o in bpy.context.scene.objects if o.type=='MESH'},key=lambda p:p.name if p else '')
    for parent in parents:
        obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==parent]
        if not obs:continue
        bpy.ops.object.select_all(action='DESELECT')
        for ob in obs:ob.select_set(True)
        bpy.context.view_layer.objects.active=obs[0]
        if len(obs)>1:bpy.ops.object.join()
        ob=bpy.context.object;ob.name=(parent.name if parent else 'Site')+'__Mesh'
        xf=ob.matrix_basis.copy()
        if max(abs(xf[i][j]-(1 if i==j else 0)) for i in range(4) for j in range(4))>1e-8:
            if ob.data.users>1:ob.data=ob.data.copy()
            ob.data.transform(xf)
        ob.matrix_basis=Matrix.Identity(4)
        if ob.data not in processed:
            bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update();processed.add(ob.data)


def publish(stem,plan,root):
    clear_templates();bpy.context.view_layer.update()
    source=Path('build')/(stem+'.blend');source.parent.mkdir(parents=True,exist_ok=True)
    summary=counts();summary['plan']=plan;summary['stage']='FORM CHECKPOINT / quick materials, not baked delivery'
    source.with_suffix('.json').write_text(json.dumps(summary,indent=2))
    bpy.ops.wm.save_as_mainfile(filepath=str(source.resolve()))
    consolidate();path=Path('export')/(stem+'.gltf');path.parent.mkdir(exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',export_texture_dir='shared',
        use_selection=True,export_yup=True,export_extras=True,export_animations=False,export_tangents=True,
        export_attributes=True,export_all_vertex_colors=False,export_image_format='AUTO')
    d=json.loads(path.read_text());summary.update(gltf_bytes=path.stat().st_size,bin_bytes=sum((path.parent/b['uri']).stat().st_size for b in d['buffers']),
        images=[dict(uri=i['uri'],bytes=(path.parent/i['uri']).stat().st_size) for i in d.get('images',[])],
        pivots=sum('pivot_axis' in o or 'slide_axis' in o or 'motion_kind' in o for o in bpy.context.scene.objects),sockets=sum('socket_kind' in o for o in bpy.context.scene.objects))
    summary['serialized_triangles']=sum(sum(d['accessors'][prim['indices']]['count']//3 for prim in d['meshes'][node['mesh']]['primitives']) for node in d['nodes'] if 'mesh' in node)
    assert summary['serialized_triangles']==summary['triangles'],(stem,summary['triangles'],summary['serialized_triangles'])
    path.with_suffix('.json').write_text(json.dumps(summary,indent=2));print('PUBLISHED',stem,summary['triangles'],flush=True)
    return summary


def reset():
    CACHE.clear();bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.unit_settings.system='METRIC'


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/family.blend'));p.add_argument('--only',default='all');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);report={}
    garden_seeds=(int(a.only.rsplit('-',1)[1]),) if a.only.startswith(('Building-','Complex-')) else COMPLEX_SEEDS
    row_seeds=(int(a.only.rsplit('-',1)[1]),) if a.only.startswith('Row-') else ROW_SEEDS
    for seed in garden_seeds:
        for mode in ('building','complex'):
            stem=f'{mode.title()}-{seed}'
            if a.only!='all' and a.only!=stem:continue
            reset();plan=garden(seed) if mode=='building' else complex_plan(seed)
            obj=garden_building(plan) if mode=='building' else make_complex(plan)
            report[stem]=publish(stem,plan,obj.root)
    for seed in row_seeds:
        stem='Row-'+str(seed)
        if a.only!='all' and a.only!=stem:continue
        reset();plan=row(seed);obj=townhouse(plan);architecture=counts(obj.root);row_site(plan,obj);report[stem]=publish(stem,plan,obj.root)
        report[stem]['architecture']=architecture
        Path('export',stem+'.json').write_text(json.dumps(report[stem],indent=2))
    a.out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()))
    if a.only=='all':Path('build/family.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':main()
