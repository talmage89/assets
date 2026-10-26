"""Measurements of the owner's read-only canonical GLB; no model data is copied.

Blender import is meters, +Z up, front/outlet -Y, origin at foot-ring bottom.
The optional fit check reads the external file. Modeling/export never import it.
"""
import math
from mathutils import Vector,Matrix
TANK_POSITION=Vector((.507,.013,.198))
TANK_YAW=math.radians(50)
TANK_RADIUS=.1561
TANK_HEIGHT=.468000263
COLLAR_RADIUS=.0875
FOOT_RING_RADIUS=.105
VALVE_FACE=Vector((0,-.0419,.4235))
VALVE_AXIS=Vector((0,-1,0))
HANDLE_SEAT=Vector((-.094,0,.436))

def tank_point(point):
    return TANK_POSITION+Matrix.Rotation(TANK_YAW,3,'Z')@Vector(point)
