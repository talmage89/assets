"""Fit against the unchanged native school delivery and actual lane triangles."""
import json,sys,math
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'school-bus'

def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(ROOT/'school/export/Campus-101.gltf'))
    campus=list(bpy.context.scene.objects);socket=bpy.data.objects['Campus_101__Bus_loading_0'];other=bpy.data.objects['Campus_101__Bus_loading_1']
    bpy.context.view_layer.update();spacing=(socket.matrix_world.translation-other.matrix_world.translation).length;xf=socket.matrix_world.inverted()
    for ob in campus:
        if ob.parent is None:ob.matrix_world=xf@ob.matrix_world
    bpy.context.view_layer.update()
    # Native static site geometry is consolidated. Select its actual asphalt
    # triangles by material, then independently test the published bus corridor.
    verts=[];faces=[];native=[]
    for ob in campus:
        if ob.type!='MESH':continue
        slots={i for i,m in enumerate(ob.data.materials) if m and m.name.startswith('SchoolGround_Asphalt')}
        if not slots:continue
        ob.data.calc_loop_triangles();offset=len(verts);verts.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        chosen=[tuple(offset+i for i in t.vertices) for t in ob.data.loop_triangles if t.material_index in slots]
        faces.extend(chosen);native.append(dict(mesh=ob.name,asphalt_triangles=len(chosen)))
    if not faces:raise ValueError('No native school asphalt triangles')
    tree=BVHTree.FromPolygons(verts,faces,all_triangles=True)
    site=bpy.data.objects['Campus_101'];to_plan=site.matrix_world.inverted()
    plan=json.loads((ROOT/'school/export/Campus-101.json').read_text())['plan'];route=[np.array(p,dtype=float) for p in plan['bus_route']]
    def route_distance(x,y):
        p=np.array(to_plan@Vector((x,y,0)))[:2];values=[]
        for a,b in zip(route,route[1:]):
            d=b-a;t=np.clip(np.dot(p-a,d)/np.dot(d,d),0,1);values.append(float(np.linalg.norm(p-(a+t*d))))
        return min(values)
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(BASE/'export/C75-101.gltf'));bus=list(set(bpy.context.scene.objects)-before);bpy.context.view_layer.update()
    support={}
    for code in ['FL','FR','RL_outer','RL_inner','RR_outer','RR_inner']:
        pivot=bpy.data.objects['Wheel_'+code];points=[ob.matrix_world@v.co for ob in pivot.children_recursive if ob.type=='MESH' for v in ob.data.vertices]
        low=min(p.z for p in points);contacts=[p for p in points if p.z<low+.00002];gaps=[]
        for p in contacts:
            hit=tree.ray_cast(p+Vector((0,0,1)),Vector((0,0,-1)),2)[0]
            if hit is not None:gaps.append(p.z-hit.z)
        support[code]=dict(tire_lowest_z_m=low,contact_samples=len(contacts),lane_hits=len(gaps),gap_range_m=[min(gaps),max(gaps)] if gaps else None)
    model=json.loads((BASE/'build/model-check.json').read_text());measured_bounds=model['body_bumper_bounds_m']
    measured=measured_bounds['size'][1];footprint=[]
    deployed_front=-measured/2-model['measured_deployed_crossing_extension_m']
    active_spacing=model['full_rest_bounds_m']['max'][1]-deployed_front+.2
    for x in [measured_bounds['min'][0],0,measured_bounds['max'][0]]:
        for y in [measured_bounds['min'][1],0,measured_bounds['max'][1]]:
            hit=tree.ray_cast(Vector((x,y,1)),Vector((0,0,-1)),2)[0]
            footprint.append(dict(x_m=x,y_m=y,lane_z_m=hit.z if hit is not None else None,distance_to_bus_route_m=route_distance(x,y)))
    errors=[]
    if any(r['lane_hits']!=r['contact_samples'] or r['lane_hits']==0 or max(abs(v) for v in r['gap_range_m'])>.005 for r in support.values()):errors.append('Wheel contact with actual lane')
    if any(p['lane_z_m'] is None or p['distance_to_bus_route_m']>7.3152/2 for p in footprint):errors.append('Body footprint outside lane')
    report=dict(passed=not errors,errors=errors,socket='Campus_101__Bus_loading_0',native_socket_spacing_m=spacing,measured_bus_bumper_length_m=measured,
        two_buses_at_native_sockets_bumper_gap_m=spacing-measured,wheel_ground_samples=support,
        active_crossing_gate_spacing_for_0_2m_scene_gap_m=math.ceil(active_spacing*20)/20,
        footprint_lane_rays=footprint,native_asphalt_meshes=native,bus_corridor_width_m=7.3152,
        recommendation='Use 12.5m center spacing for parked buses, or the computed active-gate spacing when the crossing loop is deployed. The 0.2m gap is a game-scene allowance, not a real-world operating rule. A single bus fits the 35m straight loading curb. Do not populate both original 11m reservations without increasing their spacing.',
        scope='Actual imported school asphalt intersections, published bus-route corridor and actual source bumper bounds; no school file modified')
    (BASE/'build/school-fit.json').write_text(json.dumps(report,indent=2));print('BUS_SCHOOL_FIT',json.dumps(report),flush=True)
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
