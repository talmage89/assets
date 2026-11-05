"""Pane-local mold derivatives, independent of adjacent stamped bodywork.

The original nearest-parent normals turn into the adjacent roof/A-pillar at
the upper corners. Their 18-degree local swing reflects a triangular softbox
shard despite coherent glazing geometry and a disabled normal map. Fit the
pane's smooth compound height field and use its derivative only in that small
header transition. Positions, cut outline, frit, tint and IOR remain held.
"""
import math
import bpy,numpy as np
from mathutils import Vector
from hatch_body import smoothstep


def apply():
    ob=bpy.data.objects['Windshield'];me=ob.data;matrix=ob.matrix_world
    count=ob['outer_skin_faces'];ids=sorted({i for f in me.polygons[:count] for i in f.vertices})
    ps=np.array([list(matrix@me.vertices[i].co) for i in ids]);terms=[(i,j) for i in range(5) for j in range(5-i)]
    x=ps[:,0];y=ps[:,1]+.65;rows=np.array([x**i*y**j for i,j in terms]).T
    coeff=np.linalg.lstsq(rows,ps[:,2],rcond=None)[0];residual=rows@coeff-ps[:,2]
    def normal(p):
        x=p.x;y=p.y+.65
        dx=sum(v*i*x**(i-1)*y**j for v,(i,j) in zip(coeff,terms) if i)
        dy=sum(v*j*x**i*y**(j-1) for v,(i,j) in zip(coeff,terms) if j)
        return Vector((-dx,-dy,1)).normalized()
    custom=[n.vector.copy() for n in me.corner_normals];nm=matrix.to_3x3().transposed();changed=0;maximum=0
    for f in me.polygons:
        if f.index>=2*count:continue
        for li in f.loop_indices:
            p=matrix@me.vertices[me.loops[li].vertex_index].co
            if not (-.50<p.y<-.20 and p.z>1.15 and abs(p.x)<.74):continue
            w=smoothstep(.46,.58,abs(p.x))*smoothstep(-.48,-.30,p.y)
            if not w:continue
            target=nm@normal(p);old=custom[li]
            if target.dot(old)<0:target.negate()
            angle=old.angle(target)
            if angle>math.radians(25):w*=math.radians(25)/angle
            target=old.lerp(target,w).normalized();maximum=max(maximum,math.degrees(target.angle(old)))
            custom[li]=target;changed+=1
    me.normals_split_custom_set(custom)
    ob['header_mold_normal_corners']=changed;ob['header_mold_normal_max_deg']=maximum
    ob['header_mold_height_fit_residual_max_m']=float(abs(residual).max())
    print('H120_HEADER_NORMALS',changed,'corners; maximum correction',maximum,'degrees; diagnostic fit residual',float(abs(residual).max()),flush=True)
    backlight()


def backlight():
    """Bridge the lower backlight's inherited saddle with a convex mold field.

    Fit the pane's own lower positions, with a gently convex 25 m longitudinal
    radius and a fitted transverse crown/rake. This supplies a normal
    approximation; positions, gauge, outline and accepted material values
    remain held. A fit to the entire pane would include its near-horizontal
    header return and is unsuitable for this lower physical chart.
    """
    ob=bpy.data.objects['Backlight'];me=ob.data;matrix=ob.matrix_world
    count=ob['outer_skin_faces'];ids=sorted({i for f in me.polygons[:count] for i in f.vertices})
    points=np.array([list(matrix@me.vertices[i].co) for i in ids])
    points=points[(points[:,1]>1.7)&(points[:,2]<1.35)]
    x=points[:,0]/.7;z=(points[:,2]-1.2)/.2
    terms=[(0,0),(0,1),(2,0)];rows=np.array([x**i*z**j for i,j in terms]).T
    longitudinal=-.5/25*.2**2
    coefficients=np.linalg.lstsq(rows,points[:,1]-longitudinal*z*z,rcond=None)[0]
    terms.append((0,2));coefficients=np.append(coefficients,longitudinal)
    residual=np.array([x**i*z**j for i,j in terms]).T@coefficients-points[:,1]
    if coefficients[2]>=0:raise ValueError('Backlight transverse mold is not convex')
    nm=matrix.to_3x3().transposed();custom=[n.vector.copy() for n in me.corner_normals];changed=0;maximum=0
    for face in me.polygons:
        if face.index>=2*count:continue
        for li in face.loop_indices:
            p=matrix@me.vertices[me.loops[li].vertex_index].co
            w=(1-smoothstep(1.23,1.34,p.z))*smoothstep(1.67,1.74,p.y)
            if not w:continue
            x=p.x/.7;z=(p.z-1.2)/.2
            dx=sum(c*i*x**(i-1)*z**j/.7 for c,(i,j) in zip(coefficients,terms) if i)
            dz=sum(c*j*x**i*z**(j-1)/.2 for c,(i,j) in zip(coefficients,terms) if j)
            target=nm@Vector((-dx,1,-dz)).normalized();old=custom[li]
            if target.dot(old)<0:target.negate()
            angle=old.angle(target)
            if angle>math.radians(25):w*=math.radians(25)/angle
            custom[li]=old.lerp(target,w).normalized();maximum=max(maximum,math.degrees(old.angle(custom[li])));changed+=1
    me.normals_split_custom_set(custom)
    ob['lower_mold_normal_corners']=changed;ob['lower_mold_normal_max_deg']=maximum
    ob['lower_mold_position_fit_p95_m']=float(np.percentile(abs(residual),95))
    ob['lower_mold_position_fit_max_m']=float(abs(residual).max())
    print('H120_BACKLIGHT_NORMALS',changed,'corners; maximum correction',maximum,'degrees; diagnostic position residual',float(abs(residual).max()),flush=True)
