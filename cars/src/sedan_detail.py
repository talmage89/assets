"""Add S240 detail to the deterministic one-sheet form stage, from scripts."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G
from build import Build
from sedan_check import mesh_tree
import sedan_spec as S


def optimize_backs(ob):
    """Spend on visible construction by reducing only protected inner skins."""
    from sedan_body import simplify_inner_gauge
    roles=ob.data.attributes.get('sheet_role')
    if roles is None:return
    original={}
    for face in ob.data.polygons:
        if roles.data[face.index].value!=0:continue
        for li in face.loop_indices:
            point=ob.data.vertices[ob.data.loops[li].vertex_index].co
            original[tuple(round(c,7) for c in point)]=ob.data.corner_normals[li].vector.copy()
    # The reducer reads role indices, restored only for this isolated step.
    mat=ob.data.materials[0]
    while len(ob.data.materials)<3:ob.data.materials.append(mat)
    for f in ob.data.polygons:f.material_index=roles.data[f.index].value
    from mathutils.bvhtree import BVHTree
    points=[ob.matrix_world@v.co for v in ob.data.vertices]
    tree=BVHTree.FromPolygons(points,[tuple(f.vertices) for f in ob.data.polygons if f.material_index==0])
    fascia=ob.get('part_category')=='fascia'
    simplify_inner_gauge(ob,tree,.00025 if fascia else .00008,2500,32)
    # Remove submicron collinear back slivers: their geometry is valid but
    # cannot retain nonzero area in a float32 packed UV chart. Visible skin
    # and rim edges remain excluded and are checked against the saved map.
    bm=bmesh.new();bm.from_mesh(ob.data)
    edges=[e for e in bm.edges if e.link_faces and all(f.material_index==1 for f in e.link_faces)]
    bmesh.ops.dissolve_degenerate(bm,edges=edges,dist=1e-6)
    # Choose the nondegenerate diagonal of almost-collinear skin quads now.
    # The generic triangulator can pick their zero-width corner later.
    retessellated=0
    for face in list(bm.faces):
        if len(face.verts)!=4:continue
        ps=[v.co for v in face.verts]
        def area(a,c,d):return (ps[c]-ps[a]).cross(ps[d]-ps[a]).length*.5
        ac=min(area(0,1,2),area(0,2,3));bd=min(area(0,1,3),area(1,2,3))
        longest=max(e.calc_length() for e in face.edges)
        if 2*min(ac,bd)/max(longest,1e-9)>1e-6 or max(ac,bd)<20*min(ac,bd):continue
        bmesh.ops.triangulate(bm,faces=[face],quad_method='FIXED' if ac>bd else 'ALTERNATE')
        retessellated+=1
    if not all(e.is_manifold for e in bm.edges):raise ValueError('Sheet cleanup changed solid topology')
    bm.to_mesh(ob.data);bm.free();ob['submicron_slivers_retessellated']=retessellated
    roles=ob.data.attributes['sheet_role'];custom=[]
    for face in ob.data.polygons:
        role=roles.data[face.index].value;face.use_smooth=role==0
        for li in face.loop_indices:
            point=ob.data.vertices[ob.data.loops[li].vertex_index].co
            key=tuple(round(c,7) for c in point)
            if role==0 and key not in original:raise ValueError('Visible skin changed during hidden-back reduction')
            custom.append(original[key] if role==0 else (0,0,0))
        face.material_index=0
    ob.data.materials.clear();ob.data.materials.append(mat);ob.data.normals_split_custom_set(custom)


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--wear',type=float,default=.65)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
    bpy.ops.wm.open_mainfile(filepath=str(source))
    b=Build.__new__(Build);b.root=bpy.data.objects[S.NAME];b.asset_set='Sedan';b.high=bpy.context.scene['quality']=='high';b.detail=True;b.wear=a.wear
    import sedan_finishes
    b.m=sedan_finishes.build(a.wear)
    old_to_new={'Clay body':'body','Clay glass':'glass','Clay rubber':'rubber','Clay wheel':'wheel','Clay bumper':'bumper'}
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH':continue
        if ob.get('part_category') in ['tires','wheels','brakes','closure']:
            bpy.data.objects.remove(ob,do_unlink=True);continue
        for i,mat in enumerate(ob.data.materials):
            if mat and mat.name in old_to_new:ob.data.materials[i]=b.m[old_to_new[mat.name]]
        if not b.high and ob.get('part_category') in ['body','doors','fascia']:
            optimize_backs(ob)
    # The rear plastic liner ends inboard of the door's stamped return.
    for name in ['Wheelwell_RL','Wheelwell_RR']:
        ob=bpy.data.objects[name]
        for v in ob.data.vertices:
            p=ob.matrix_world@v.co
            if abs(p.x)>.83:
                p.x*=.795/.875;v.co=ob.matrix_world.inverted()@p
    for ob in bpy.context.scene.objects:
        if ob.name.startswith('Wheelwell'):
            ob.data.materials.clear();ob.data.materials.append(b.m['frame'])
    for ob in list(bpy.context.scene.objects):
        if ob.name.startswith(('Wheel_','Steer_')):bpy.data.objects.remove(ob,do_unlink=True)
    import wheels,sedan_exterior,sedan_interior,sedan_underbody,sedan_hardware
    from types import SimpleNamespace
    wheel_spec=SimpleNamespace(**{k:getattr(S,k) for k in dir(S) if not k.startswith("__")})
    wheel_spec.WHEEL_AXIAL_SCALE=1.0
    wheels.build(b,wheel_spec)
    # The sedan shoulder blocks follow its narrower tread, while the existing
    # family carcass already has the correct ISO section width.
    for ob in bpy.context.scene.objects:
        if ob.name.startswith('Shoulder tread_'):
            for v in ob.data.vertices:
                v.co.x*=S.WHEEL_AXIAL_SCALE
                radius=(v.co.y*v.co.y+v.co.z*v.co.z)**.5
                if radius>0:
                    factor=(radius-.0015)/radius;v.co.y*=factor;v.co.z*=factor
    for ob in list(bpy.context.scene.objects):
        if not ob.name.startswith('Shoulder tread_'):continue
        if b.high:
            # Fine road-tire lugs belong in the tire's projection group.
            world=ob.matrix_world.copy();ob.parent=bpy.data.objects['Tire_'+ob.name.split('_')[-1]];ob.matrix_world=world
        else:bpy.data.objects.remove(ob,do_unlink=True)
    sedan_hardware.passenger_wheels(b)
    sedan_exterior.build(b);sedan_interior.build(b);sedan_underbody.build(b);sedan_hardware.door_hinges(b)
    bpy.context.view_layer.update()
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('asset_set')!='Sedan':continue
        weight=ob.data.attributes.new('S240UVWeight','FLOAT','FACE')
        roles=ob.data.attributes.get('sheet_role');outer=ob.get('lens_outer_faces')
        for face in ob.data.polygons:
            role=roles.data[face.index].value if roles else (0 if outer is None or face.index<outer else 1)
            weight.data[face.index].value=1.0 if role==0 else .35 if role==2 else .25
        rest=ob.data.attributes.get('VehicleRest') or ob.data.attributes.new('VehicleRest','FLOAT_VECTOR','POINT')
        rest.data.foreach_set('vector',[q for v in ob.data.vertices for q in ob.matrix_world@v.co])
    if b.high:
        # One projection source prevents a nested mesh root from inheriting
        # the tire's exploded bake translation twice. Both source meshes use
        # the same original wheel-local coordinate frame.
        for code in ['FL','FR','RL','RR']:
            tire=bpy.data.objects['Tire_'+code];lug=bpy.data.objects['Shoulder tread_'+code]
            bpy.ops.object.select_all(action='DESELECT');tire.select_set(True);lug.select_set(True)
            bpy.context.view_layer.objects.active=tire;bpy.ops.object.join()
    for mat in list(bpy.data.materials):
        if mat.users==0:bpy.data.materials.remove(mat)
    sc=bpy.context.scene;sc['stage']='S240 detail and procedural look-dev';sc['form_source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest();sc['wear']=a.wear
    categories={};parents={};parts={}
    for ob in sc.objects:
        if ob.type=='MESH' and ob.get('asset_set')=='Sedan':
            ob.data.calc_loop_triangles();num=len(ob.data.loop_triangles);parts[ob.name]=num
            category=ob['part_category'];categories[category]=categories.get(category,0)+num
            parents[ob.parent.name]=parents.get(ob.parent.name,0)+num
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
    report=dict(triangles=sum(parts.values()),categories=categories,parents=parents,meshes=parts)
    Path(a.out).with_suffix('.counts.json').write_text(json.dumps(report,indent=2));print('SEDAN_DETAIL',json.dumps(categories),sum(parts.values()),flush=True)
if __name__=='__main__':main()
