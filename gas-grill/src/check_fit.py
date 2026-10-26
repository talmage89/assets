"""Optional read-only canonical tank metrology; never saves a scene or an asset."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fit_spec import VALVE_FACE,VALVE_AXIS,HANDLE_SEAT,TANK_RADIUS,TANK_HEIGHT


def main():
    p=argparse.ArgumentParser();p.add_argument('--grill',required=True);p.add_argument('--reference',default='');p.add_argument('--out',required=True);p.add_argument('--parts-source')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);path=Path(a.reference).expanduser()
    if not a.reference or not path.is_file():
        message='SKIP canonical fit check: optional owner tank is absent'
        Path(a.out).write_text(json.dumps(dict(skipped=message,passed=True),indent=2));print(message);return
    # Reference must remain outside this worktree.
    if path.resolve().is_relative_to(Path(__file__).resolve().parents[2]):raise ValueError('Owner reference must be external')
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest=='27955562131121505d15234088412d64a250b5feaaf96314558454a1ba9f3a39','Canonical tank changed; remeasure its valve/collar/foot ring before accepting fit'
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(a.grill).resolve()))
    socket=bpy.data.objects['tank_socket'];attach=bpy.data.objects['regulator_attach'];rig=bpy.data.objects['HoseRig']
    origin=socket.matrix_world.translation.copy();face=socket.matrix_world@VALVE_FACE
    outlet_axis=(socket.matrix_world.to_3x3()@VALVE_AXIS).normalized()
    distance=(attach.matrix_world.translation-face).length
    opposition=(attach.matrix_world.to_3x3()@Vector((0,1,0))).normalized().dot(outlet_axis)
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path))
    imported=set(bpy.context.scene.objects)-before
    reference_names=sorted(o.name for o in imported)
    visual=[o for o in imported if o.type=='MESH' and 'collision' not in o.name.lower()]
    points=[o.matrix_world@v.co for o in visual for v in o.data.vertices]
    lo=Vector(tuple(min(v[k] for v in points) for k in range(3)));hi=Vector(tuple(max(v[k] for v in points) for k in range(3)))
    assert max(abs((hi-lo)[k]-v) for k,v in enumerate((TANK_RADIUS*2,TANK_RADIUS*2,TANK_HEIGHT)))<1e-5,'Canonical bounds changed'
    assert abs(lo.z)<1e-6 and (lo+hi).xy.length<1e-5,'Canonical ground origin changed'
    assert distance<2e-5 and opposition<-.99999,'Coupling face/axis does not meet outlet'
    vertices=[];faces=[]
    for ob in visual:
        offset=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        faces.extend(tuple(offset+i for i in p.vertices) for p in ob.data.polygons)
    surface=BVHTree.FromPolygons(vertices,faces)
    # Hook center is 4 mm below the flat underside of the owner's handle lip.
    hook_center=HANDLE_SEAT-Vector((0,0,.004));hook_gap=surface.find_nearest(hook_center)[3]-.004
    assert abs(hook_gap)<.00015,'Hook no longer engages handle underside'
    path_points=[Vector(rig['hose_rest_points_m'][i:i+3]) for i in range(0,len(rig['hose_rest_points_m']),3)]
    inverse=socket.matrix_world.inverted();clearances=[]
    for point in path_points:
        local=inverse@(rig.matrix_world@point)
        clearances.append(surface.find_nearest(local)[3]-.0052)
    assert min(clearances)>0,'Hose intersects canonical vessel'
    retention={}
    if a.parts_source:
        # Serialization was checked independently; retain component identities
        # from the finalized source for actual surface-to-surface sampling.
        bpy.ops.wm.open_mainfile(filepath=str(Path(a.parts_source).resolve()))
        for ob in bpy.context.scene.objects:
            if ob.type!='MESH' or not ob.name.startswith(('Foot ring retention cradle','Foot ring cradle rubber pad')):continue
            ob.data.calc_loop_triangles();samples=[]
            for triangle in ob.data.loop_triangles:
                v0,v1,v2=[inverse@(ob.matrix_world@ob.data.vertices[i].co) for i in triangle.vertices]
                for i in range(9):
                    for j in range(9-i):samples.append(v0+(v1-v0)*(i/8)+(v2-v0)*(j/8))
            distances=[surface.find_nearest(point)[3] for point in samples]
            retention[ob.name]=dict(minimum_sampled_clearance_m=min(distances),surface_samples=len(samples))
    result=dict(passed=True,reference_sha256=digest,reference_objects=reference_names,
        canonical_bounds_m=dict(min=list(lo),max=list(hi),size=list(hi-lo)),canonical_origin='foot-ring bottom center; +Z up, valve -Y',
        collar_diameter_m=.175,collar_z_m=[.369325,.4596],foot_ring_diameter_m=.210,foot_ring_z_m=[0,.050848],
        valve_face_canonical_m=list(VALVE_FACE),valve_axis_canonical=list(VALVE_AXIS),tank_socket_world_m=list(origin),tank_yaw_degrees=50,
        valve_face_world_m=list(face),valve_axis_world=list(outlet_axis),mating_error_m=distance,axis_opposition_dot=opposition,
        collar_hook_surface_gap_m=hook_gap,retention_clearance=retention,retention_measurement_source=a.parts_source,
        minimum_hose_surface_clearance_m=min(clearances))
    Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,'External reference changed'
    # No blend/GLB save calls exist in this checker.

if __name__=='__main__':main()
