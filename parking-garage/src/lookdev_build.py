"""Bind baked shared charts and caused age; preserve every earlier delivery."""
import argparse,json,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
import geometry as G
from build import export,members
from atlas_binding import palette,bind
from service_age import placed
from form import remove_paint,tower_signs
from plan import garage
import pieces


def images():return list(Path('textures/lookdev').rglob('*.png'))


def modules():
    bpy.ops.wm.open_mainfile(filepath=str(Path('build/ParkingGarage.blend').resolve()))
    roots=[o for o in bpy.context.scene.objects if o.parent is None];G.palette(Path('textures/lookdev'))
    layout=json.loads(Path('textures/lookdev/layout.json').read_text());mats=palette();p=garage(101);report={}
    for root in roots:
        root.location=(0,0,0);name=root.name
        if name.startswith('Tower'):
            levels=int(name[-1]) if name[-1].isdigit() else 4
            for o in list(root.children_recursive):bpy.data.objects.remove(o,do_unlink=True)
            pieces.tower(root,levels,refined=True);tower_signs(root,levels,layout,'ALDER QUAY')
        elif name=='DoubleTee':
            for o in list(root.children):
                if o.type=='MESH':bpy.data.objects.remove(o,do_unlink=True)
            from tee_detail import source
            source(root)
        elif name=='Spandrel':
            for o in list(root.children):
                if o.type=='MESH':bpy.data.objects.remove(o,do_unlink=True)
            pieces.spandrel(root,refined=True)
        elif name in ('StructuralBay','EndBay','RampBay'):
            from tee_detail import source
            from plan import FLOOR,TEE
            import bmesh
            rise=FLOOR/(16*TEE) if name=='RampBay' else 0
            for deck in [o for o in root.children if o.get('module_kind')=='DoubleTee']:
                for ob in list(deck.children):
                    if ob.type=='MESH':bpy.data.objects.remove(ob,do_unlink=True)
                ob=source(deck)
                for v in ob.data.vertices:v.co.z+=rise*(deck.location.x+v.co.x)
                bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
        for ob in root.children_recursive:remove_paint(ob)
        bpy.context.view_layer.update();bind(root,p,mats)
        report[name]=export(f'export/lookdev/modules/{name}.gltf',members(root),images())
        report[name]['bounds_m']=G.bounds(members(root))
        assert report[name]['triangles']<=(8000 if name.startswith('Tower') else 2000),(name,report[name]['triangles'])
    Path('build/lookdev/modules.json').write_text(json.dumps(report,indent=2)+'\n')


def sites():
    reports=[]
    for seed in (101,202):
        bpy.ops.wm.open_mainfile(filepath=str(Path(f'build/lookdev/form-site-{seed}.blend').resolve()))
        p=json.loads(Path(f'build/lookdev/garage-{seed}.json').read_text());rt=bpy.data.objects['Garage_'+str(seed)];mats=palette()
        binds=bind(rt,p,mats);age=placed(rt,p,mats);rt['stage']='BAKED LOOK-DEV CHECKPOINT / NO DOCS'
        p['garage_triangles']=G.triangles(members(rt));assert p['garage_triangles']<300000
        for row in p['pieces']:
            ob=bpy.data.objects.get(row['name'])
            if ob:row['triangles']=G.triangles(members(ob))
        p['delivery']=export(f'export/lookdev/ParkingGarageLook-{seed}.gltf',[o for o in members(rt) if o.type!='CURVE'],images())
        Path(f'build/lookdev/look-{seed}.json').write_text(json.dumps(p,indent=2)+'\n')
        delivery=export(f'export/lookdev/sites/ParkingGarageLookSite-{seed}.gltf',[o for o in bpy.context.scene.objects if o.type!='CURVE'],images())
        from tangent_rounding import stabilize
        stabilize(Path(f'export/lookdev/sites/ParkingGarageLookSite-{seed}.gltf'))
        bpy.ops.wm.save_as_mainfile(filepath=str(Path(f'build/lookdev/look-site-{seed}.blend').resolve()))
        context=json.loads(Path(f'build/lookdev/actors-{seed}.json').read_text())
        categories={}
        for actor in context['actors']:
            row=categories.setdefault(actor['category'],dict(count=0,triangles=0))
            row['count']+=1;row['triangles']+=actor['triangles']
        reports.append(dict(seed=seed,garage_triangles=p['garage_triangles'],bound_objects=binds,age=age,delivery=delivery,
            actors=categories,actor_triangles=context['actor_triangles'],context_triangles=context['context_triangles'],
            context_without_actors_triangles=context['context_triangles']-context['actor_triangles']))
        Path('build/lookdev/sites.json').write_text(json.dumps(reports,indent=2)+'\n');print('BAKED LOOK SITE',seed,p['garage_triangles'],flush=True)


def comparisons():
    for name,seed in (('precast',101),('harmon',202)):
        bpy.ops.wm.open_mainfile(filepath=str(Path(f'build/lookdev/comparison-{name}.blend').resolve()))
        p=json.loads(Path(f'build/lookdev/comparison-{name}.json').read_text())
        rt=bpy.data.objects['Garage_'+str(seed)];mats=palette();bind(rt,p,mats);placed(rt,p,mats)
        export(f'export/lookdev/comparison-{name}.gltf',[o for o in bpy.context.scene.objects if o.type!='CURVE'],images())
        if name=='precast':
            from tangent_rounding import stabilize
            stabilize(Path(f'export/lookdev/comparison-{name}.gltf'))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--only',default='all');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.only in ('all','modules'):modules()
    if a.only in ('all','sites'):sites()
    if a.only in ('all','comparisons'):comparisons()
