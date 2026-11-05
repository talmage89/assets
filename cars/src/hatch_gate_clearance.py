"""Keep buried gate chords behind the independently refined outer draw.

The game reverse sheet is an economical occlusion surface. Its coarse chords
must not cross the sub-millimeter outer gauge at a concavity. Preserve every
outer vertex and cut rim; retreat only wholly buried reverse vertices. The
separate molded card is seated by its whole surface, rather than locator rows.
"""
import math
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def triangle_probes(face,points,spacing=.006):
    a,c,d=[points[i] for i in face.vertices]
    n=max(2,math.ceil(max((a-c).length,(c-d).length,(a-d).length)/spacing))
    for i in range(n+1):
        for j in range(n+1-i):
            weights=(i/n,j/n,1-(i+j)/n)
            yield sum((p*w for p,w in zip([a,c,d],weights)),Vector()),weights


def apply():
    ob=bpy.data.objects['Liftgate outer'];me=ob.data;matrix=ob.matrix_world
    inverse=matrix.inverted();role=me.attributes['hatch_outer_skin']
    points=[matrix@v.co for v in me.vertices];initial=[p.copy() for p in points]
    outer=[f for f in me.polygons if role.data[f.index].value]
    tree=BVHTree.FromPolygons(points,[tuple(f.vertices) for f in outer])
    held={v for f in outer for v in f.vertices}
    selected={f.index for f in me.polygons if not role.data[f.index].value
        and (matrix.to_3x3()@f.normal).y<-.4
        and any(abs(points[v].x)<.636 and .650<points[v].z<.99 for v in f.vertices)}
    me.calc_loop_triangles()
    faces=[f for f in me.loop_triangles if f.polygon_index in selected]
    movable={i for f in faces for i in f.vertices if i not in held}
    def skin(q):
        return tree.ray_cast(Vector((q.x,3,q.z)),Vector((0,-1,0)),3)[0]
    for iteration in range(40):
        shifts={}
        for face in faces:
            for q,weights in triangle_probes(face,points):
                p=skin(q)
                if p is None:continue
                deficit=q.y-p.y+.001
                active=sum(w for i,w in zip(face.vertices,weights) if i in movable)
                if deficit<.000001 or active<.0001:continue
                for i in face.vertices:
                    if i in movable:shifts[i]=max(shifts.get(i,0),deficit/active)
        if not shifts:break
        for i,distance in shifts.items():points[i].y-=distance
    else:raise ValueError('Gate reverse clearance did not converge')
    for i in movable:me.vertices[i].co=inverse@points[i]
    me.update()
    ob['buried_reverse_retreat_max_m']=max(((points[i]-initial[i]).length for i in movable),default=0)
    ob['buried_reverse_probe_spacing_m']=.006
    ob['buried_reverse_target_y_gap_m']=.001
    # The original card spans the hollow with only two longitudinal bands.
    # Its largest face bulge, rather than a corner, determines its seating.
    trim=bpy.data.objects['H120 liftgate inner trim']
    tp=[trim.matrix_world@v.co for v in trim.data.vertices]
    trim.data.calc_loop_triangles();worst=-1
    for face in trim.data.loop_triangles:
        for q,_ in triangle_probes(face,tp):
            p=skin(q)
            if p is not None:worst=max(worst,q.y-p.y)
    if worst==-1:raise ValueError('Gate card has no outer-skin overlap')
    retreat=max(0,worst+.018);ti=trim.matrix_world.inverted()
    for vertex in trim.data.vertices:
        p=trim.matrix_world@vertex.co;p.y-=retreat;vertex.co=ti@p
    trim.data.update();trim['seating_retreat_m']=retreat
    trim['whole_surface_target_y_gap_m']=.018
    print('H120_GATE_BURIED_CLEARANCE',ob['buried_reverse_retreat_max_m'],retreat,flush=True)
