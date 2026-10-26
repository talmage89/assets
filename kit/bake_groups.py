"""Optional projection isolation, preserving object-space procedural coordinates."""
from mathutils import Vector


def owner(ob,roots):
    while ob:
        if ob.name in roots:return ob.name
        ob=ob.parent
    return 'stationary'


def offsets(objects,roots,padding=.1):
    points=[ob.matrix_world@Vector(c) for ob in objects for c in ob.bound_box]
    span=max(p.x for p in points)-min(p.x for p in points)+padding
    return {'stationary':Vector((0,0,0)),**{name:Vector((span*(i+1),0,0)) for i,name in enumerate(roots)}}
