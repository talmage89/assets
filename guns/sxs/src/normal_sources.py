"""Keep the source's genuinely ground side faces flat in the normal bake."""
import math
from mathutils import Vector

def is_ground(face, points):
    """The accepted constant-X lands, including their micron edge break."""
    return (abs(face.normal.x)>.99999 and
            all(abs(abs(p[0])-.02595)<.000015 for p in points))

def ground_sides(ob):
    def angle(a,b):
        # atan2 does not turn a float32 unit-length roundoff into a false
        # 0.02-degree error, as acos(dot) does for almost parallel vectors.
        return math.degrees(math.atan2(a.cross(b).length,a.dot(b)))
    normals=[n.vector.copy() for n in ob.data.corner_normals];before=[];measured=[]
    for face in ob.data.polygons:
        points=[ob.data.vertices[i].co for i in face.vertices]
        # Match the model's existing 0.015 mm ground-side classification.
        # Reduced triangles can end on the microscopic breech edge break,
        # 1.3 microns inside the plane; a 0.3-micron bound omitted them.
        # No longitudinal bound: the same plane continues into the hinge cheek.
        if is_ground(face,points):
            expected=Vector((math.copysign(1,face.normal.x),0,0))
            # Isolate the ground plane's loop-normal space from its curved
            # neighbors. Merely assigning +/-X left as much as 0.307 degrees
            # after Blender's custom-normal encoding in the old smooth fan.
            face.use_smooth=False
            for i in face.loop_indices:
                before.append(angle(normals[i],expected))
                measured.append((i,expected))
                normals[i]=expected
    ob.data.normals_split_custom_set(normals)
    assert before
    after=[angle(ob.data.corner_normals[i].vector,expected) for i,expected in measured]
    return dict(corners=len(before),maximum_before_degrees=max(before),maximum_after_degrees=max(after),
        policy='Flat loop-normal fans on actual constant-X ground faces; preserve turned roof, lip and end-face normals')


def separate_ground_uv(objects,rect,margin=.002):
    """Separate flat lands from unresolved edge-break normals, then repack.

    Smart projection groups these nearly coplanar triangles together even
    though their custom normal fans differ sharply. A subpixel edge break
    then filters its tangent correction onto the ground land. Separate UV
    charts give each surface its own padding without changing any vertex.
    Existing relative island scales (including priorities) are retained.
    """
    import hashlib
    import bpy
    import numpy as np
    from kit import uv
    def identity(ob):
        vertices=np.array([v.co[:] for v in ob.data.vertices],dtype='<f4')
        loops=np.array([p.vertex_index for p in ob.data.loops],dtype='<u4')
        return hashlib.sha256(vertices.tobytes()+loops.tobytes()).hexdigest()
    before={o.name:identity(o) for o in objects}
    normals={o.name:[n.vector[:] for n in o.data.corner_normals] for o in objects}
    action=next(o for o in objects if o.name=='Action_Body')
    mesh=action.data;flat={p.index for p in mesh.polygons
        if is_ground(p,[mesh.vertices[i].co for i in p.vertices])}
    assert flat
    def joined_boundaries():
        edges={};joined=0;layer=mesh.uv_layers['BakeUV']
        for face in mesh.polygons:
            rows=list(face.loop_indices)
            for a,b in zip(rows,rows[1:]+rows[:1]):
                edge=tuple(sorted((mesh.loops[a].vertex_index,mesh.loops[b].vertex_index)))
                coords={mesh.loops[i].vertex_index:tuple(layer.data[i].uv) for i in (a,b)}
                if edge in edges:
                    other,old=edges[edge]
                    if (other in flat)!=(face.index in flat) and all(
                        max(abs(x-y) for x,y in zip(coords[i],old[i]))<1e-7 for i in edge):joined+=1
                else:edges[edge]=(face.index,coords)
        return joined
    joined_before=joined_boundaries();x0,y0,x1,y1=rect
    for ob in objects:
        for point in ob.data.uv_layers['BakeUV'].data:
            point.uv=((point.uv.x-x0)/(x1-x0),(point.uv.y-y0)/(y1-y0))
    for index in flat:
        face=mesh.polygons[index]
        for i in face.loop_indices:
            mesh.uv_layers['BakeUV'].data[i].uv.x+=3+math.copysign(1,face.normal.x)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=action
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.pack_islands(udim_source='CLOSEST_UDIM',rotate=True,rotate_method='ANY',scale=True,
        merge_overlap=False,margin_method='FRACTION',margin=margin,pin=False,shape_method='AABB')
    bpy.ops.object.mode_set(mode='OBJECT')
    for ob in objects:
        for point in ob.data.uv_layers['BakeUV'].data:
            point.uv=(x0+point.uv.x*(x1-x0),y0+point.uv.y*(y1-y0))
        ob.data.normals_split_custom_set(normals[ob.name])
    after={o.name:identity(o) for o in objects};joined_after=joined_boundaries()
    assert before==after and joined_after==0
    return dict(method='Separate original ground-side UV charts; repack existing priority-scaled islands',
        ground_faces=len(flat),joined_ground_boundaries_before=joined_before,
        joined_ground_boundaries_after=joined_after,geometry_identical=before==after,
        geometry_sha256=after,uv=uv.report(objects,size=2048))
