"""Keep the source's genuinely ground side faces flat in the normal bake."""
import math
from mathutils import Vector

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
        if abs(face.normal.x)>.99999 and all(abs(abs(p.x)-.02595)<.000015 for p in points):
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
        policy='Flat loop-normal fans on actual constant-X ground faces; preserve subdivision roof, lip and end-face normals')
