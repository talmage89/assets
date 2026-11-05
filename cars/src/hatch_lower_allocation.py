"""Retile nearly coplanar lower fascia faces to fund the gate's tight draw.

Every retained vertex stays fixed. Aperture/gauge edges and the upper painted
panels remain held. Probe the changed chords against the original triangles;
reject any candidate exceeding 0.75 mm. This is game allocation only.
"""
import math
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def apply(b):
    if b.high:return
    for name in ['Front molded fascia','Rear molded fascia']:
        ob=bpy.data.objects[name];me=ob.data;me.calc_loop_triangles()
        tree=BVHTree.FromPolygons([v.co.copy() for v in me.vertices],
            [tuple(t.vertices) for t in me.loop_triangles],all_triangles=True)
        saved=me.attributes.new('H120 lower held corners','FLOAT_VECTOR','CORNER')
        for row,n in zip(saved.data,me.corner_normals):row.vector=n.vector
        bm=bmesh.new();bm.from_mesh(me);bm.normal_update()
        region={f for f in bm.faces if (ob.matrix_world@f.calc_center_median()).z<.60}
        vertices=[v for v in bm.verts if v.link_faces and all(f in region for f in v.link_faces)]
        edges=[e for e in bm.edges if len(e.link_faces)==2 and all(f in region for f in e.link_faces)]
        before=sum(len(f.verts)-2 for f in bm.faces)
        bmesh.ops.dissolve_limit(bm,angle_limit=math.radians(1),use_dissolve_boundaries=False,
            verts=vertices,edges=edges,delimit={'MATERIAL'})
        bmesh.ops.triangulate(bm,faces=[f for f in bm.faces if len(f.verts)>3]);bm.normal_update()
        maximum=0
        for f in bm.faces:
            if (ob.matrix_world@f.calc_center_median()).z>=.60:continue
            points=[v.co for v in f.verts]
            for q in [sum(points,Vector())/len(points)]+[(a+c)/2 for a,c in zip(points,points[1:]+points[:1])]:
                maximum=max(maximum,tree.find_nearest(q)[3])
        retired=before-sum(len(f.verts)-2 for f in bm.faces)
        if maximum>.00075:
            bm.free();me.attributes.remove(saved)
            raise ValueError('Lower fascia allocation exceeded its chord tolerance: '+name)
        bm.to_mesh(me);bm.free();saved=me.attributes['H120 lower held corners']
        me.normals_split_custom_set([r.vector for r in saved.data]);me.attributes.remove(saved)
        ob['lower_allocation_retired_triangles']=retired
        ob['lower_allocation_probe_max_m']=maximum
        print('H120_LOWER_ALLOCATION',name,retired,'triangles retired; maximum probe',maximum,flush=True)
