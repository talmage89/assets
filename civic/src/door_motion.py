"""Chord-length sectional-door travel on a vertical / quarter-circle / roof track."""
import math
from mathutils import Vector


def guide(distance,height,radius):
    start=height+.10;arc=radius*math.pi/2
    if distance<=start:return Vector((0,0,distance))
    if distance<start+arc:
        t=(distance-start)/radius
        return Vector((0,radius*(1-math.cos(t)),start+radius*math.sin(t)))
    return Vector((0,radius+distance-start-arc,start+radius))


def pose(objects,progress,rest=None):
    """Position each panel by its two hinge points, keeping real panel length.

    Return original local matrices so the identical sweep can reset/repeat.
    Positive progress raises the lower panel through the bend; the upper
    sections travel farther into the roof, preserving their original order.
    """
    groups={}
    for ob in objects:
        name=ob.get('overhead_door')
        if name:groups.setdefault((ob.parent.name,name),[]).append(ob)
    rest=rest or {o.name:o.matrix_basis.copy() for rows in groups.values() for o in rows}
    for rows in groups.values():
        rows.sort(key=lambda o:o['section_index']);h=rows[0]['door_height_m'];r=rows[0]['track_radius_m'];pitch=rows[0]['panel_pitch_m']
        base=rest[rows[0].name].translation;s=progress*(h+.10+r*math.pi/2)
        for ob in rows:
            a=guide(s,h,r);lo=s;hi=s+pitch*1.8
            for _ in range(36):
                mid=(lo+hi)/2
                if (guide(mid,h,r)-a).length<pitch:lo=mid
                else:hi=mid
            end=(lo+hi)/2;b=guide(end,h,r);delta=b-a
            ob.rotation_mode='XYZ';ob.matrix_basis=rest[ob.name];ob.location=base+a;ob.rotation_euler.x=-math.atan2(delta.y,delta.z);s=end
    return rest
