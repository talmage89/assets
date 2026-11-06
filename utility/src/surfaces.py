"""Stock glTF family PBR and explicit construction UV charts, before joining."""
import math
from pathlib import Path
import bpy
from atlas import point,RECTS

FAMILY=None


def material():
    global FAMILY
    from kit.tiling import material as pbr
    FAMILY=pbr('Utility',Path('textures/ship'))
    FAMILY['age_years']='15–30';FAMILY.use_backface_culling=False
    return FAMILY


def uv_object(ob,seed=1,height=12,spec=None):
    import bmesh
    me=ob.data
    # A transported low-sided tube can have a slightly twisted quad. Choose
    # its chart plane on the actual shipping triangles, not an averaged quad
    # normal that can project one of its triangles onto a line.
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=bm.faces[:]);bm.normal_update();bm.to_mesh(me);bm.free();me.update()
    uv=me.uv_layers.active or me.uv_layers.new(name='UVMap')
    old=[m.name.removeprefix('Utility_') for m in me.materials]
    coords=[v.co for v in me.vertices]
    low=[min(v[k] for v in coords) for k in range(3)];high=[max(v[k] for v in coords) for k in range(3)]
    span=[max(.00001,high[k]-low[k]) for k in range(3)]
    roles=set()
    charts=me.attributes.get('UtilityChart') or me.attributes.new('UtilityChart','INT','FACE')
    for poly in me.polygons:
        source=old[poly.material_index];role=source
        if source in ('Wood','Endgrain'):
            role='PoleA' if seed%2 else 'PoleB'
            if 'crossarm' in ob.name.lower():role='Crossarm'
            elif 'molding' in ob.name.lower():role='Molding'
            if source=='Endgrain' or (role.startswith('Pole') and abs(poly.normal.z)>.9):role='Endgrain'
            if role=='Crossarm' and abs(poly.normal.x)>.9:role='Endgrain'
            if role=='Molding' and abs(poly.normal.z)>.9:role='Endgrain'
        elif source=='Paint':role='Tank'
        elif source in ('Aluminum','Steel'):role='Steel'
        if ob.get('atlas_role'):role=ob['atlas_role']
        roles.add(role)
        charts.data[poly.index].value=list(RECTS).index(role)
        for li in poly.loop_indices:
            if role=='Tag' and ob.get('authored_tag_uv'):continue
            v=coords[me.loops[li].vertex_index]
            if role.startswith('Pole'):
                # Seam on the back of the shaft; local front is U=.25.
                angles=[math.atan2(coords[i].y,coords[i].x)/math.tau+.5 for i in poly.vertices]
                u=math.atan2(v.y,v.x)/math.tau+.5
                if max(angles)-min(angles)>.5 and u>.5:u-=1
                if spec:
                    import numpy as np
                    # Fixed lower metres preserve ground wetting and nail
                    # scars. Upper chart landmarks follow this actual pole's
                    # communications, neutral and arm through-bolts.
                    actual=[-.12,0,2.5,spec['communication'],spec['neutral'],spec['primary']-.38,height]
                    authored=[0,.012,2.5,6.6,7.85,9.0,12]
                    vv=float(np.interp(v.z,actual,authored))/12
                else:vv=max(0,min(1,v.z/height))
            elif role=='Guard' and 'yellow guy guard' in ob.name.lower():
                # Lathe-local +Z runs from anchor to the top of the guard.
                # Dirt and scuffs must follow that axis before object posing.
                if abs(poly.normal.z)>.9:
                    u=(v.x-low[0])/span[0]
                    vv=(.015 if v.z<(low[2]+high[2])/2 else .85)+.02*(v.y-low[1])/span[1]
                else:
                    angles=[math.atan2(coords[i].y,coords[i].x)/math.tau+.5 for i in poly.vertices]
                    u=math.atan2(v.y,v.x)/math.tau+.5
                    if max(angles)-min(angles)>.5 and u>.5:u-=1
                    vv=(v.z-low[2])/span[2]
            elif role=='Guard':
                # The riser also has a yellow formed channel, not a lathe.
                if abs(poly.normal.z)>.9:
                    u=(v.x-low[0])/span[0]
                    vv=(.015 if v.z<(low[2]+high[2])/2 else .85)+.02*(v.y-low[1])/span[1]
                else:
                    k=1 if abs(poly.normal.x)>.5 else 0
                    u=(v[k]-low[k])/span[k];vv=(v.z-low[2])/span[2]
            elif role=='Tank' and 'tank' in ob.name.lower():
                if abs(poly.normal.z)>.8:
                    u=(v.x-low[0])/span[0];vv=(v.y-low[1])/span[1]
                    u=.58+.30*u;vv=.50+.35*vv
                    uv.data[li].uv=point(role,u,vv)
                    continue
                cx=(high[0]+low[0])/2;cy=(high[1]+low[1])/2
                angles=[math.atan2(coords[i].y-cy,coords[i].x-cx)/math.tau+.5 for i in poly.vertices]
                u=math.atan2(v.y-cy,v.x-cx)/math.tau+.5
                if max(angles)-min(angles)>.5 and u>.5:u-=1
                vv=(v.z-low[2])/span[2]
            elif role in ('Tag','Brand','Rating'):
                u=(v.x-low[0])/span[0];vv=(v.z-low[2])/span[2]
            elif role in ('Crossarm','Molding'):
                long_axis=0 if role=='Crossarm' else 2
                others=[k for k in range(3) if k!=long_axis]
                # UV V is vertical grain for the molding, along X for the arm.
                a=others[0] if abs(poly.normal[others[1]])>.5 else others[1]
                u=(v[long_axis]-low[long_axis])/span[long_axis]
                vv=(v[a]-low[a])/span[a]
                if role=='Molding':u,vv=vv,u
            else:
                axes=sorted(range(3),key=lambda k:abs(poly.normal[k]))[:2]
                u=(v[axes[0]]-low[axes[0]])/span[axes[0]]
                vv=(v[axes[1]]-low[axes[1]])/span[axes[1]]
            if role=='Tank' and not ob.name.startswith('Rolled steel transformer tank'):
                # Lids and small painted fittings use chalked paint away from
                # the barrel's vertical runoff and its stained lower seam.
                u=.58+.30*u;vv=.50+.35*vv
            if not (-1e-5<=u<=1.00001 and -1e-5<=vv<=1.00001):
                raise ValueError((ob.name,role,poly.index,tuple(poly.normal),tuple(v),u,vv))
            uv.data[li].uv=point(role,u,vv)
        poly.material_index=0
    me.materials.clear();me.materials.append(FAMILY)
    me.calc_loop_triangles()
    bad=[]
    for tri in me.loop_triangles:
        a,b,c=[uv.data[i].uv for i in tri.loops]
        if abs((b-a).cross(c-a))<1e-13:bad.append(tri.index)
    if bad:raise ValueError(('Degenerate stock UV',ob.name,len(bad),bad[:6]))
    ob['atlas_charts']=','.join(sorted(roles));ob['uv_reuse']='Authored stock charts; repeated role surfaces intentionally overlap'
