"""Keep the source's genuinely ground side faces flat in the normal bake."""
import math
from mathutils import Vector

def ground_sides(ob):
    normals=[n.vector.copy() for n in ob.data.corner_normals];before=[];measured=[]
    for face in ob.data.polygons:
        points=[ob.data.vertices[i].co for i in face.vertices]
        if abs(face.normal.x)>.99999 and all(.07<=p.y<=.170001 and abs(abs(p.x)-.02595)<.0000003 for p in points):
            expected=Vector((math.copysign(1,face.normal.x),0,0))
            for i in face.loop_indices:
                before.append(math.degrees(math.acos(max(-1,min(1,normals[i].dot(expected))))))
                measured.append((i,expected))
                normals[i]=expected
    ob.data.normals_split_custom_set(normals)
    assert before
    after=[math.degrees(math.acos(max(-1,min(1,ob.data.corner_normals[i].vector.dot(expected))))) for i,expected in measured]
    return dict(corners=len(before),maximum_before_degrees=max(before),maximum_after_degrees=max(after),
        policy='Actual constant-X ground faces only; preserve the subdivision roof, lip and end-face normals')
