"""Detail the accepted H120 form without rebuilding or refitting its exterior."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from build import Build
import hatch_spec as S


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    p.add_argument('--wear',type=float,default=.65)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
    bpy.ops.wm.open_mainfile(filepath=str(source))
    b=Build.__new__(Build);b.root=bpy.data.objects[S.NAME];b.asset_set=S.ASSET_SET
    b.high=bpy.context.scene['quality']=='high';b.detail=True;b.wear=a.wear
    import hatch_finishes,hatch_exterior,hatch_interior,hatch_underbody,hatch_hardware,hatch_mechanisms,wheels
    b.m=hatch_finishes.build(a.wear)
    mapping={'Clay body':'body','Clay glass':'glass','Clay rubber':'rubber','Clay wheel':'wheel','Clay bumper':'bumper'}
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH':continue
        if ob.get('part_category') in ['wheels','tires','brakes','closure']:
            bpy.data.objects.remove(ob,do_unlink=True);continue
        for i,mat in enumerate(ob.data.materials):
            if mat and mat.name in mapping:ob.data.materials[i]=b.m[mapping[mat.name]]
    for ob in list(bpy.context.scene.objects):
        if ob.name.startswith(('Wheel_','Steer_')):bpy.data.objects.remove(ob,do_unlink=True)
    from types import SimpleNamespace
    spec=SimpleNamespace(**{k:getattr(S,k) for k in dir(S) if not k.startswith('__')})
    spec.WHEEL_AXIAL_SCALE=1.0
    wheels.build(b,spec)
    # Original FWD geometry: 15 degree SAI, 6.5 degree caster and negative
    # 20 mm scrub. Keep every wheel/rest surface while setting the kingpin.
    from mathutils import Matrix,Vector
    import math
    for code in ['FL','FR']:
        ob=bpy.data.objects['Steer_'+code];sign=-1 if code.endswith('L') else 1
        bpy.context.view_layer.update();children={c:c.matrix_world.copy() for c in ob.children}
        axis=Vector((-sign*math.tan(math.radians(15)),math.tan(math.radians(6.5)),1)).normalized()
        ground=Vector((sign*(S.FRONT_TRACK/2+.020),S.FRONT_AXLE-.045,0))
        position=ground+axis*(S.HUB_HEIGHT/axis.z)
        ob.matrix_world=Matrix.Translation(position)@axis.to_track_quat('Z','Y').to_matrix().to_4x4()
        ob['kingpin_ground_point']=list(ground);ob['kingpin_axis_vehicle']=list(axis)
        ob['kingpin_status']='15 degree SAI / 6.5 degree caster, negative 20 mm scrub'
        bpy.context.view_layer.update()
        for child,xf in children.items():child.matrix_world=xf
    for ob in list(bpy.context.scene.objects):
        if ob.name.startswith('Shoulder tread_'):
            if not b.high:
                bpy.data.objects.remove(ob,do_unlink=True);continue
            else:
                for v in ob.data.vertices:v.co.x*=S.TIRE_WIDTH/.275
        if ob.name.startswith('Wheelwell'):
            ob.data.materials.clear();ob.data.materials.append(b.m['frame'])
            inverse=ob.matrix_world.inverted()
            for v in ob.data.vertices:
                p=ob.matrix_world@v.co
                if ob.name.startswith('Wheelwell inboard_F'):p.x*=.485/.56
                elif ob.name.startswith('Wheelwell_R') and abs(p.x)>.83:p.x*=.76/.88
                elif ob.name.startswith('Wheelwell_F') and abs(p.x)>.83:p.x*=.795/.88
                if ob.name.startswith('Wheelwell_F'):
                    r=((p.y-S.FRONT_AXLE)**2+(p.z-S.HUB_HEIGHT)**2)**.5
                    p.y=S.FRONT_AXLE+(p.y-S.FRONT_AXLE)*(r+.007)/r;p.z=S.HUB_HEIGHT+(p.z-S.HUB_HEIGHT)*(r+.007)/r
                v.co=inverse@p
    for ob in bpy.context.scene.objects:
        if not ob.name.startswith('Arch flange_F'):continue
        inverse=ob.matrix_world.inverted()
        ps=[ob.matrix_world@v.co for v in ob.data.vertices];outer=max(abs(p.x) for p in ps)
        for v,p in zip(ob.data.vertices,ps):
            if abs(p.x)<outer-.008:
                r=((p.y-S.FRONT_AXLE)**2+(p.z-S.HUB_HEIGHT)**2)**.5
                p.y=S.FRONT_AXLE+(p.y-S.FRONT_AXLE)*(r+.006)/r;p.z=S.HUB_HEIGHT+(p.z-S.HUB_HEIGHT)*(r+.006)/r
                v.co=inverse@p
    hatch_hardware.passenger_wheels(b);hatch_hardware.game_wheel_allocation(b)
    import hatch_running_surfaces
    hatch_running_surfaces.tires(b)
    # The spoiler's mounting underside seats above the roof skin; its held outer
    # contour is unchanged. The former locator buried its foot 7 mm in the roof.
    from hatch_check import mesh_tree
    fixed=mesh_tree([o for o in bpy.context.scene.objects if o.type=='MESH' and (o.name=='Roof' or o.name.startswith(('Greenhouse','Rear quarter')))])
    spoiler=bpy.data.objects['Roof spoiler'];inverse=spoiler.matrix_world.inverted()
    for v in spoiler.data.vertices:
        p=spoiler.matrix_world@v.co
        if p.y>1.57:continue
        hit=fixed.ray_cast(__import__('mathutils').Vector((p.x,p.y,2)),__import__('mathutils').Vector((0,0,-1)),3)[0]
        if hit is not None and p.z<hit.z+.008:p.z=hit.z+.008;v.co=inverse@p
    import hatch_surface_detail
    hatch_surface_detail.refine(b)
    import hatch_surface_normals
    hatch_surface_normals.sample_reflections(b)
    hatch_surface_normals.apply()
    import hatch_shoulder_surface
    hatch_shoulder_surface.apply(b)
    hatch_running_surfaces.arches(b)
    hatch_running_surfaces.liners(b)
    hatch_exterior.build(b);hatch_interior.build(b);hatch_underbody.build(b);hatch_mechanisms.build(b)
    if not b.high:
        for ob in list(bpy.context.scene.objects):
            if 'bolster piping' in ob.name or ob.name=='Lower intake opening blade 2':bpy.data.objects.remove(ob,do_unlink=True)
    import hatch_reference_surface
    hatch_reference_surface.cleanup()
    import hatch_hidden_allocation
    hatch_hidden_allocation.reduce(b)
    hatch_hidden_allocation.covered_door_backs(b)
    bpy.context.view_layer.update()
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('asset_set')!=S.ASSET_SET:continue
        rest=ob.data.attributes.get('VehicleRest') or ob.data.attributes.new('VehicleRest','FLOAT_VECTOR','POINT')
        rest.data.foreach_set('vector',[q for v in ob.data.vertices for q in ob.matrix_world@v.co])
        if ob.type=='MESH' and ob.name.startswith('H120 original'):ob['allow_boundary']=True
    if b.high:
        for code in ['FL','FR','RL','RR']:
            tire=bpy.data.objects['Tire_'+code];lug=bpy.data.objects['Shoulder tread_'+code]
            bpy.ops.object.select_all(action='DESELECT');tire.select_set(True);lug.select_set(True)
            bpy.context.view_layer.objects.active=tire;bpy.ops.object.join()
    categories={};parts={};parents={}
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('asset_set')!=S.ASSET_SET:continue
        ob.data.calc_loop_triangles();num=len(ob.data.loop_triangles);parts[ob.name]=num
        category=ob['part_category'];categories[category]=categories.get(category,0)+num
        parents[ob.parent.name]=parents.get(ob.parent.name,0)+num
    for mat in list(bpy.data.materials):
        if mat.users==0:bpy.data.materials.remove(mat)
    sc=bpy.context.scene;sc['stage']='H120 detail and look development checkpoint';sc['wear']=a.wear
    sc['form_source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
    report=dict(triangles=sum(parts.values()),categories=categories,parents=parents,meshes=parts)
    out.with_suffix('.counts.json').write_text(json.dumps(report,indent=2))
    print('H120_DETAIL',json.dumps(categories),sum(parts.values()),flush=True)
if __name__=='__main__':main()
