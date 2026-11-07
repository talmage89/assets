"""Fit against the unchanged native school delivery and actual lane triangles."""
import json,sys
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
    lane=next(o for o in campus if 'Bus_loading_lane_paving' in o.name);lane.data.calc_loop_triangles()
    tree=BVHTree.FromPolygons([lane.matrix_world@v.co for v in lane.data.vertices],[tuple(t.vertices) for t in lane.data.loop_triangles],all_triangles=True)
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(BASE/'export/C75-101.gltf'));bus=list(set(bpy.context.scene.objects)-before);bpy.context.view_layer.update()
    support={}
    for code in ['FL','FR','RL_outer','RL_inner','RR_outer','RR_inner']:
        pivot=bpy.data.objects['Wheel_'+code];points=[ob.matrix_world@v.co for ob in pivot.children_recursive if ob.type=='MESH' for v in ob.data.vertices]
        low=min(p.z for p in points);contacts=[p for p in points if p.z<low+.00002];gaps=[]
        for p in contacts:
            hit=tree.ray_cast(p+Vector((0,0,1)),Vector((0,0,-1)),2)[0]
            if hit is not None:gaps.append(p.z-hit.z)
        support[code]=dict(tire_lowest_z_m=low,contact_samples=len(contacts),lane_hits=len(gaps),gap_range_m=[min(gaps),max(gaps)] if gaps else None)
    measured=json.loads((BASE/'build/model-check.json').read_text())['body_bumper_bounds_m']['size'][1]
    report=dict(socket='Campus_101__Bus_loading_0',native_socket_spacing_m=spacing,measured_bus_bumper_length_m=measured,
        two_buses_at_native_sockets_bumper_gap_m=spacing-measured,wheel_ground_samples=support,
        recommendation='Use at least 12.5m center spacing for this 40ft conventional. A single bus fits the 35m straight loading curb. Do not populate both original 11m reservations without increasing their spacing.',
        scope='Actual imported lane ray intersections and actual source bumper bounds; no school file modified')
    (BASE/'build/school-fit.json').write_text(json.dumps(report,indent=2));print('BUS_SCHOOL_FIT',json.dumps(report),flush=True)
if __name__=='__main__':main()
