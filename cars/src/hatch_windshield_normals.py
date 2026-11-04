"""A windshield's own mold derivatives at the header, independent of its frame.

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
