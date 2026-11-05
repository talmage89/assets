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
    # Freeze the actual game diagonals before testing its hidden back.
    # A BVH's implicit quad tessellation need not match the delivered triangles.
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    from mathutils.bvhtree import BVHTree
    points=[ob.matrix_world@v.co for v in ob.data.vertices]
    tree=BVHTree.FromPolygons(points,[tuple(f.vertices) for f in ob.data.polygons if f.material_index==0])
    fascia=ob.get('part_category')=='fascia'
    hinge_space=[(y-.22,y+.24,.49,.69) for y in [S.DOOR_FRONT,S.DOOR_SPLIT]]
    hinge_space.extend([(y-.08,y+.08,.82,.92) for y in [S.DOOR_FRONT,S.DOOR_SPLIT]])
    if ob.name=='Hood outer':
        # Keep the actual strut/bracket lands at X=+/-660 mm, with 40 mm
        # clearance each way. The former 300 mm bands locked unrelated back
        # tessellation; the exposed hood is held by optimize_backs throughout.
        hinge_space.extend([(x0,x1,-1.90,-1.05,.70,1.10) for x0,x1 in [(-.70,-.62),(.62,.70)]])
    simplify_inner_gauge(ob,tree,.00025 if fascia else .00008,5000,96,max_edge_length=.35 if fascia else .25,
                         protected_regions=hinge_space)
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
    if not all(e.is_manifold for e in bm.edges):raise ValueError(('Sheet cleanup changed solid topology',ob.name))
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bm.to_mesh(ob.data);bm.free();ob['submicron_slivers_retessellated']=retessellated
    seat_inner_sheet(ob)
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


def seat_inner_sheet(ob):
    """Keep reduced back triangles beneath the actual triangulated game skin."""
    from mathutils.bvhtree import BVHTree
    from mathutils.geometry import intersect_ray_tri
    matrix=ob.matrix_world;inverse=matrix.inverted().to_3x3();mesh=ob.data
    outer=[f for f in mesh.polygons if f.material_index==0]
    tree=BVHTree.FromPolygons([matrix@v.co for v in mesh.vertices],[tuple(f.vertices) for f in outer],all_triangles=True)
    backs=[f for f in mesh.polygons if f.material_index==1];target=.00008;before=None;total=0.;first_crossings=None
    def crossings():
        world=[matrix@v.co for v in mesh.vertices]
        back_tree=BVHTree.FromPolygons(world,[tuple(f.vertices) for f in backs],all_triangles=True)
        result=[]
        for oi,bi in tree.overlap(back_tree):
            a=[world[i] for i in outer[oi].vertices];c=[world[i] for i in backs[bi].vertices];crosses=False
            for source,dest in [(a,c),(c,a)]:
                for p,q in zip(source,source[1:]+source[:1]):
                    direction=q-p;length=direction.length
                    if length<1e-12:continue
                    hit=intersect_ray_tri(*dest,direction/length,p,True)
                    if hit is not None and (hit-p).length<length-1e-8 and (hit-p).length>1e-8:crosses=True;break
                if crosses:break
            if crosses:result.append((oi,bi))
        return result,world
    for iteration in range(24):
        minimum=1.;corrections={}
        for face in backs:
            ids=list(face.vertices);ps=[matrix@mesh.vertices[i].co for i in ids]
            probes=ps+[sum(ps,Vector())/3]+[(p+q)/2 for p,q in zip(ps,ps[1:]+ps[:1])]
            for q in probes:
                hit,n,_,_=tree.find_nearest(q);depth=-(q-hit).dot(n);minimum=min(minimum,depth)
                if depth>=target:continue
                correction=-n*(target-depth+.00002)
                for i in ids:
                    if i not in corrections or corrections[i].length_squared<correction.length_squared:corrections[i]=correction
        intersections,world=crossings()
        if first_crossings is None:first_crossings=len(intersections)
        for oi,bi in intersections:
            face=outer[oi];a,c,d=[world[i] for i in face.vertices];n=(c-a).cross(d-a).normalized()
            ids=list(backs[bi].vertices);height=max((world[i]-a).dot(n) for i in ids)
            correction=-n*(max(0,height)+target+.00002)
            for i in ids:
                if i not in corrections or corrections[i].length_squared<correction.length_squared:corrections[i]=correction
        if before is None:before=minimum
        if not corrections:break
        for i,correction in corrections.items():mesh.vertices[i].co+=inverse@correction;total=max(total,correction.length)
        mesh.update()
    else:raise ValueError(('Inner sheet does not clear actual game skin',ob.name,minimum))
    ob['actual_game_back_minimum_depth_m']=minimum;ob['actual_game_back_before_m']=before
    ob['actual_game_back_maximum_step_m']=total;ob['actual_game_back_iterations']=iteration
    ob['actual_game_back_intersections_before']=first_crossings;ob['actual_game_back_intersections_after']=len(intersections)


def conform_liners():
    """Seat front liner edges behind the actual tucked painted outer skin.

    A fixed 880 mm outer X protrudes through the lower fascia, whose real
    section tucks to 840–875 mm. That occlusion is the long apparent arch spike.
    """
    from mathutils.bvhtree import BVHTree
    ps=[];faces=[]
    for panel in bpy.context.scene.objects:
        if panel.type!='MESH' or panel.get('part_category') not in ['body','doors','fascia']:continue
        roles=panel.data.attributes.get('sheet_role');start=len(ps)
        ps.extend(panel.matrix_world@v.co for v in panel.data.vertices)
        faces.extend(tuple(start+i for i in face.vertices) for face in panel.data.polygons if roles and roles.data[face.index].value==0)
    tree=BVHTree.FromPolygons(ps,faces)
    for side,sign in [('L',-1),('R',1)]:
        ob=bpy.data.objects['Wheelwell_F'+side];inverse=ob.matrix_world.inverted();samples=[]
        for v in ob.data.vertices:
            p=ob.matrix_world@v.co
            if abs(p.x)<.80:continue
            hit=tree.ray_cast(Vector((sign*2,p.y,p.z)),Vector((-sign,0,0)),4)[0]
            limit=abs(hit.x)-.006 if hit is not None else .82
            p.x=sign*min(abs(p.x),limit);v.co=inverse@p
            samples.append([p.x,p.y,p.z])
        ob.data.update();G.smooth(ob,35);ob['liner_edge_source']='Actual painted-skin side ray, 6 mm inward'


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
        if not b.high and ob.get('part_category') in ['body','doors','fascia','pillars'] and not ob.get('s240_game_allocated'):
            from sedan_surface_allocation import reduce
            reduce(ob)
            optimize_backs(ob)
    # The rear plastic liner ends inboard of the door's stamped return.
    for name in ['Wheelwell_RL','Wheelwell_RR']:
        ob=bpy.data.objects[name]
        for v in ob.data.vertices:
            p=ob.matrix_world@v.co
            if abs(p.x)>.83:
                p.x*=.795/.875;v.co=ob.matrix_world.inverted()@p
    conform_liners()
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
    if not b.high:
        # Seven section rings retain both beads, both maximum-width shoulders
        # and the crown. Their saved triangles fund a round 56-chord silhouette.
        from kit.vehicle import loaded_tire
        for code in ['FL','FR','RL','RR']:
            old=bpy.data.objects['Tire_'+code];parent=old.parent
            center=parent.matrix_world.translation.copy();material=old.data.materials[0]
            bpy.data.objects.remove(old,do_unlink=True)
            tire=loaded_tire('Tire_'+code,center,S.TIRE_WIDTH,S.TIRE_ASPECT,S.RIM_INCHES,
                material,S.TIRE_DELIVERY_SEGMENTS,S.HUB_HEIGHT,profile_indices=[0,3,5,7,9,11,14],rolling_radius=S.HUB_HEIGHT)
            b.add(tire,parent,'tires')
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
    sedan_hardware.tire_normals(b)
    sedan_exterior.build(b);sedan_interior.build(b);sedan_underbody.build(b);sedan_hardware.door_hinges(b)
    bpy.context.view_layer.update()
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('asset_set')!='Sedan':continue
        weight=ob.data.attributes.new('S240UVWeight','FLOAT','FACE')
        roles=ob.data.attributes.get('sheet_role');outer=ob.get('lens_outer_faces')
        if roles is None and outer is not None:
            roles=ob.data.attributes.new('sheet_role','INT','FACE')
            for face in ob.data.polygons:roles.data[face.index].value=0 if face.index<outer else 1 if face.index<2*outer else 2
        for face in ob.data.polygons:
            role=roles.data[face.index].value if roles else (0 if outer is None or face.index<outer else 1)
            priority=1.0 if role==0 else .35 if role==2 else .25
            if ob.name.startswith('Tire_'):
                sign=-1 if ob.name.endswith('L') else 1
                center=sum((ob.data.vertices[i].co for i in face.vertices),Vector())/len(face.vertices)
                priority=1.7 if sign*center.x>.105 else .70 if (center.y*center.y+center.z*center.z)**.5>.312 else .30
            weight.data[face.index].value=priority
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
    from sedan_surface_normals import coalesce
    for ob in bpy.context.scene.objects:
        if ob.type=='MESH' and ob.get('part_category') in ['body','doors','fascia','pillars','glass']:coalesce(ob)
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
