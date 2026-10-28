"""Blade direction, actual bearing contact and triangle-surface guard gap.

For disjoint closed triangle meshes, the minimum is vertex/face or edge/edge.
BVH vertex/face queries plus all AABB-qualified edge pairs measure that minimum
at each declared pose. This is independent of export agreement and is not a
claim of continuous-time collision detection.
"""
import math
import bpy,numpy as np
from mathutils import Vector
from kit import weapon as W,motion,assembly


def edge_array(surface):
    edges={tuple(sorted((a,b))) for f in surface['faces'] for a,b in zip(f,f[1:]+f[:1])}
    return np.array([[tuple(surface['points'][a]),tuple(surface['points'][b])] for a,b in edges])


def gap(a,b):
    # Face/vertex candidates, including both orientations.
    best=min([b['tree'].find_nearest(p)[3] for p in a['points']]+
             [a['tree'].find_nearest(p)[3] for p in b['points']])
    ea,eb=edge_array(a),edge_array(b);blo=eb.min(axis=1);bhi=eb.max(axis=1)
    for edge in ea:
        alo=edge.min(axis=0);ahi=edge.max(axis=0)
        delta=np.maximum(np.maximum(alo-bhi,blo-ahi),0)
        candidates=eb[np.sum(delta*delta,axis=1)<best*best]
        if not len(candidates):continue
        p=edge[0];u=edge[1]-p;q=candidates[:,0];v=candidates[:,1]-q;w=p-q
        aa=float(u@u);bb=v@u;cc=np.sum(v*v,axis=1);dd=w@u;ee=np.sum(v*w,axis=1)
        denom=aa*cc-bb*bb
        valid=denom>1e-24
        s=np.divide(bb*ee-cc*dd,denom,out=np.zeros_like(cc),where=valid)
        t=np.divide(aa*ee-bb*dd,denom,out=np.zeros_like(cc),where=valid)
        interior=valid&(s>=0)&(s<=1)&(t>=0)&(t<=1)
        if interior.any():best=min(best,float(np.linalg.norm(w[interior]+s[interior,None]*u-t[interior,None]*v[interior],axis=1).min()))
        # Endpoint/segment cases (also covers parallel segments).
        for point in edge:
            t=np.clip(np.sum((point-q)*v,axis=1)/np.maximum(cc,1e-30),0,1)
            best=min(best,float(np.linalg.norm(point-q-t[:,None]*v,axis=1).min()))
        for point in (candidates[:,0],candidates[:,1]):
            s=np.clip((point-p)@u/max(aa,1e-30),0,1)
            best=min(best,float(np.linalg.norm(point-p-s[:,None]*u,axis=1).min()))
    return best


def measure(arm):
    W.pose(arm,None,0);shoe=bpy.data.objects['Trigger_Shoe'];guard=bpy.data.objects['Trigger_Guard']
    s=motion.surface(shoe);front=[];back=[]
    for z in (.014,.010,.004,-.003):
        f=s['tree'].ray_cast(Vector((0,.06,z)),Vector((0,-1,0)),.1)
        b=s['tree'].ray_cast(Vector((0,0,z)),Vector((0,1,0)),.1)
        assert f[0] is not None and b[0] is not None
        assert f[1].y>.4 and b[1].y<-.4
        front.append(list(f[0]));back.append(list(b[0]))
    assert front[0][1]>front[2][1]+.002 and front[3][1]>front[2][1]+.002,front
    assert back[0][1]>back[2][1]+.0015 and back[3][1]>back[2][1]+.0015,back
    width=s['hi'].x-s['lo'].x;assert .0062<width<.0065,width
    pivot=list(arm.data.bones['Trigger'].head_local);assert (Vector(pivot)-Vector((0,.02669,.023))).length<1e-7
    fixed=motion.surface(guard);rows=[]
    rest_rotation=arm.pose.bones['Trigger'].matrix.to_quaternion()
    # More densely than the whole-rifle sweep during the brief trigger pull.
    frames=(0,1.5,3) if len(s['faces'])>5000 else [i/4 for i in range(13)]
    for frame in frames:
        W.pose(arm,'Fire',frame);surface=motion.surface(shoe)
        depth,crossings=motion.penetration(surface,fixed,0)
        assert depth==0 and crossings==0,(frame,depth,crossings)
        clearance=gap(surface,fixed);assert clearance>.0002,(frame,clearance)
        bearing,method=assembly.distance(shoe,bpy.data.objects['Trigger_Pin']);assert bearing<1e-7
        delta=arm.pose.bones['Trigger'].matrix.to_quaternion()@rest_rotation.inverted()
        axis,angle_radians=delta.to_axis_angle()
        angle=math.degrees(angle_radians)*(1 if axis.x>=0 else -1)
        rows.append(dict(frame=frame,pull_degrees=angle,guard_clearance_m=clearance,
                         bearing_contact_m=bearing,bearing_method=method))
    # Imported bone local axes differ; measure the evaluated frame's angle.
    W.pose(arm,'Fire',0);rest=arm.pose.bones['Trigger'].matrix.to_quaternion()
    W.pose(arm,'Fire',3);pulled=arm.pose.bones['Trigger'].matrix.to_quaternion()
    angle=math.degrees(rest.rotation_difference(pulled).angle);assert abs(angle-12)<.001,angle
    assert rows[-1]['pull_degrees']< -11.999,rows[-1]
    W.pose(arm,None,0)
    return dict(passed=True,width_m=width,pivot_m=pivot,pull_angle_degrees=angle,
                front_surface_samples_m=front,back_surface_samples_m=back,poses=rows,
                minimum_sampled_guard_clearance_m=min(r['guard_clearance_m'] for r in rows),
                method='actual triangle vertex/face + edge/edge distance; sampled pull poses, no continuous-time claim')
