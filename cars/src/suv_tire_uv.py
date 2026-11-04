"""One shared, original carcass tile for the four identical ISO-size tires.

The canonical FR carcass is unwrapped by angle and measured profile arc length.
Left tires reflect the angular coordinate to retain outward-readable lettering.
Their tread handedness follows that reflection. Mesh positions never change.
"""
import math
import bpy
from mathutils import Vector
import suv_spec as S

RECT=(.005,.005,.995,.255)


def prepare():
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or not ob.name.startswith('Tire_'):continue
        me=ob.data;n=S.TIRE_SEGMENTS_GAME;rows=len(me.vertices)//n
        if rows*n!=len(me.vertices):raise ValueError('Unexpected carcass topology')
        profile=[Vector((me.vertices[j*n].co.x,math.hypot(me.vertices[j*n].co.y,me.vertices[j*n].co.z))) for j in range(rows)]
        distances=[0.]
        for a,b in zip(profile,profile[1:]):distances.append(distances[-1]+(b-a).length)
        perimeter=distances[-1]+(profile[-1]-profile[0]).length
        layer=me.uv_layers.get('BakeUV') or me.uv_layers.new(name='BakeUV')
        for face in me.polygons:
            coords=[]
            for vi in face.vertices:
                j,i=divmod(vi,n);u=i/n
                if ob.name.endswith('L'):u=(.5-u)%1
                coords.append([u,distances[j]/perimeter])
            for axis in [0,1]:
                values=[p[axis] for p in coords]
                if max(values)-min(values)>.5:
                    for p in coords:
                        if p[axis]<.5:p[axis]+=1
            for li,(u,v) in zip(face.loop_indices,coords):layer.data[li].uv=(RECT[0]+u*(RECT[2]-RECT[0]),RECT[1]+v*(RECT[3]-RECT[1]))
        ob['export_part']=ob.name
        ob['atlas_reuse']='Shared canonical FR carcass tile; left angular UV reflection preserves readable letters'
