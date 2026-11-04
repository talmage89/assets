"""Sectional-door track kinematics and sampled solid clearance.

Each rigid section follows the shared vertical / quarter-circle / horizontal
guide. Adjacent endpoints retain the section's actual height as a chord.
"""
import math
from mathutils import Vector,Matrix


def track(distance,door_height,radius=.20):
    vertical=door_height+.01;arc=math.pi*radius/2
    if distance<=vertical:return Vector((0,0,distance))
    if distance<=vertical+arc:
        a=(distance-vertical)/radius
        return Vector((0,radius*(1-math.cos(a)),vertical+radius*math.sin(a)))
    return Vector((0,radius+distance-vertical-arc,vertical+radius))


def pose(progress):
    import bpy
    nodes=sorted([o for o in bpy.context.scene.objects if o.get('motion_kind')=='sectional_track'],key=lambda o:o['section'])
    if not nodes:return []
    h=nodes[0]['section_height_m'];height=h*4;radius=nodes[0]['track_radius_m'];travel=progress*(height+.55)
    bottom0=Vector(nodes[0]['closed_top_m'])-Vector((0,0,h));frames=[]
    top_distance=height+travel
    for node in reversed(nodes):
        top=track(top_distance,height,radius)
        # Find a point behind the top on the guide exactly one rigid section
        # away. The chord, rather than arc length, determines its rotation.
        lo=top_distance-2*h;hi=top_distance
        for _ in range(40):
            mid=(lo+hi)/2
            if (top-track(mid,height,radius)).length>h:lo=mid
            else:hi=mid
        bottom=track((lo+hi)/2,height,radius);delta=(top-bottom).normalized()
        angle=math.atan2(delta.y,delta.z)
        node.location=bottom0+top;node.rotation_mode='XYZ';node.rotation_euler=( -angle,0,0)
        frames.append(dict(node=node.name,top=list(node.location),angle_degrees=-math.degrees(angle),chord_height_m=(top-bottom).length))
        top_distance=(lo+hi)/2
    bpy.context.view_layer.update();return frames


def check(plan=None):
    import bpy
    from kit.motion import surface,penetration,owned
    # Surface BVHs compare each section with static construction. Shared
    # section joints are intentional butt seams, tested for a positive gap
    # separately; they are not named exemptions against fixed structure.
    nodes=[o for o in bpy.context.scene.objects if o.get('motion_kind')=='sectional_track']
    if not nodes:return dict(passed=True,samples=0,scope='No sectional garage door')
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set') and not o.get('allow_boundary',False)]
    moving=[o for o in meshes if any(owned(o,n) for n in nodes)]
    fixed=[o for o in meshes if o not in moving];stationary={o.name:surface(o) for o in fixed}
    saved={o.name:o.matrix_basis.copy() for o in nodes};worst=0;violations=[];chord=0;ceiling_clearance=100.
    try:
        for step in range(41):
            progress=step/40;frames=pose(progress)
            chord=max(chord,max(abs(row['chord_height_m']-nodes[0]['section_height_m']) for row in frames))
            current={o.name:surface(o) for o in moving}
            for o in moving:
                if plan:
                    block=next(b for b in plan['blocks'] if b.name==o['block'])
                    gap=block.floor+plan['spec']['ceiling']-current[o.name]['hi'].z
                    ceiling_clearance=min(ceiling_clearance,gap)
                    if gap<.0005:violations.append(dict(progress=progress,moving=o.name,fixed='Authored clear ceiling plane',penetration_m=-gap))
                for other in fixed:
                    depth,crossings=penetration(current[o.name],stationary[other.name],.0005);worst=max(worst,depth)
                    if depth>.0005:violations.append(dict(progress=progress,moving=o.name,fixed=other.name,penetration_m=depth))
                for other in moving:
                    if other.name<=o.name:continue
                    depth,crossings=penetration(current[o.name],current[other.name],.0005);worst=max(worst,depth)
                    if depth>.0005:violations.append(dict(progress=progress,moving=o.name,fixed=other.name,penetration_m=depth))
    finally:
        for o in nodes:o.matrix_basis=saved[o.name]
        bpy.context.view_layer.update()
    return dict(passed=not violations,samples=41,sections=len(nodes),tolerance_m=.0005,max_penetration_m=worst,chord_height_max_error_m=chord,measured_panel_to_authored_ceiling_min_gap_m=ceiling_clearance if plan else None,violations=violations,allowed_contacts=[],scope='Sampled rigid section surfaces against tagged closed construction/other sections, plus actual panel bounds against the authored clear ceiling plane. Continuous kinematic guide is authored, not a continuous collision guarantee.')
