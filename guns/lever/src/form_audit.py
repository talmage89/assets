"""Independent round-two surface evidence, also run on a fresh GLB import."""
import math
import json
import bpy
import numpy as np
from mathutils import Vector
from kit import motion, weapon as W
from sections import extract


def hull(points):
    points=sorted(set(map(tuple,points)))
    def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    low=[];high=[]
    for target,sequence in ((low,points),(high,reversed(points))):
        for p in sequence:
            while len(target)>1 and cross(target[-2],target[-1],p)<=0:target.pop()
            target.append(p)
    return low[:-1]+high[:-1]


def measure(arm):
    W.pose(arm,'Idle',0)
    wood=bpy.data.objects['Stock'];tongues=[]
    original=json.loads(wood['uninletted_sections_mm'])
    for y in (-35,-5,25):
        boundary=hull([p for line in original[str(y)] for p in line])
        for name in ('Upper_Tang','Lower_Tang'):
            points=[p for line in extract(bpy.data.objects[name],y*.001) for p in line]
            assert points
            # Actual wood sections recorded BEFORE machining. Bridging the
            # current inlet with a chord would falsely reject a flush crowned
            # tongue: that chord lies below the original rounded comb.
            outside=max(max(-((b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]))/
                                math.dist(a,b) for a,b in zip(boundary,boundary[1:]+boundary[:1])) for p in points)
            assert outside<.12,(name,y,'metal proud of wood envelope',outside)
            tongues.append(dict(part=name,station_mm=y,maximum_outside_wood_mm=outside))
    tree=motion.surface(bpy.data.objects['Lever_FingerLoop'])['tree']
    a=math.radians(12);long=Vector((0,math.cos(a),math.sin(a)))
    short=Vector((0,-math.sin(a),math.cos(a)));center=Vector((0,-.006,-.0305))
    def hit(direction,origin=center):
        p=tree.ray_cast(origin,direction,.3)[0]
        assert p is not None,(origin,direction)
        return p
    ends=[hit(s*long) for s in (-1,1)];sides=[hit(s*short) for s in (-1,1)]
    outside=hit(short,center-short*.030)
    length=(ends[1]-ends[0]).length;width=(sides[1]-sides[0]).length
    bar=(outside-sides[0]).length
    assert .101<length<.106 and .027<width<.031 and .0030<bar<.0036,(length,width,bar)
    bow_outer=tree.ray_cast(Vector((0,.085,-.10)),Vector((0,0,1)),.10)[0]
    bow_inner=tree.ray_cast(Vector((0,.085,-.020)),Vector((0,0,-1)),.10)[0]
    assert bow_outer is not None and bow_inner is not None
    bow_depth=bow_inner.z-bow_outer.z
    assert .012<bow_depth<.016,('Full side-depth forging at the bow',bow_depth)
    rear=motion.surface(bpy.data.objects['Rear_Buckhorn'])
    notch_origin=Vector((0,.283,.066))
    notch=[rear['tree'].ray_cast(notch_origin,Vector((s,0,0)),.02)[0] for s in (-1,1)]
    floor=rear['tree'].ray_cast(notch_origin,Vector((0,0,-1)),.02)[0]
    shoulder=rear['tree'].ray_cast(Vector((.0025,.283,.080)),Vector((0,0,-1)),.03)[0]
    assert all(p is not None for p in notch+[floor,shoulder])
    sight=dict(height_mm=(rear['hi'].z-rear['lo'].z)*1000,thickness_mm=(rear['hi'].y-rear['lo'].y)*1000,
      ear_rise_mm=(rear['hi'].z-shoulder.z)*1000,notch_width_mm=(notch[1].x-notch[0].x)*1000,
      notch_depth_mm=(shoulder.z-floor.z)*1000)
    assert 8.8<sight['height_mm']<9.2 and 1<sight['thickness_mm']<1.2
    assert 1.9<sight['ear_rise_mm']<2.4 and 1.95<sight['notch_width_mm']<2.10
    samples=[]
    for frame in (0,13.2258064516,36):
        W.pose(arm,'Cycle',frame)
        delta=arm.pose.bones['Lever'].matrix@arm.data.bones['Lever'].matrix_local.inverted()
        # Recover dimensions from actual evaluated surfaces in the moving
        # local frame, rather than reporting the authored opening constants.
        points=motion.surface(bpy.data.objects['Lever_FingerLoop'])['points']
        actual=motion.surface(bpy.data.objects['Lever_FingerLoop'])['tree']
        c=delta@center;l=delta.to_3x3()@long;s=delta.to_3x3()@short
        ends=[actual.ray_cast(c,d*l,.3)[0] for d in (-1,1)]
        sides=[actual.ray_cast(c,d*s,.3)[0] for d in (-1,1)]
        assert all(p is not None for p in ends+sides)
        ll=(ends[1]-ends[0]).length;ww=(sides[1]-sides[0]).length
        assert abs(ll-length)<2e-6 and abs(ww-width)<2e-6
        center_x=(min(p.x for p in points)+max(p.x for p in points))/2
        assert abs(center_x)<2e-6
        samples.append(dict(frame=frame,global_angle_deg=math.degrees(math.atan2(delta[2][1],delta[1][1])),
            inside_length_mm=ll*1000,inside_width_mm=ww*1000,plane_center_x_mm=center_x*1000))
    W.pose(arm,'Idle',0)
    table_points=np.asarray([tuple(p)[1:] for p in motion.surface(bpy.data.objects['Hammer_ThumbPad'])['points']])
    values,vectors=np.linalg.eigh(np.cov(table_points.T));axis=vectors[:,-1]
    if axis[0]<0:axis=-axis
    table_angle=math.degrees(math.atan2(axis[1],axis[0]))
    assert 10<table_angle<16,('Photo-class cocked thumb table angle',table_angle)
    stem=motion.surface(bpy.data.objects['Stock_TangScrewShank'])
    middle=(stem['lo'].z+stem['hi'].z)/2
    origin=Vector((0,-.015,middle))
    a=stem['tree'].ray_cast(origin,Vector((1,0,0)),.02)[0]
    b=motion.surface(wood)['tree'].ray_cast(origin,Vector((1,0,0)),.02)[0]
    assert a is not None and b is not None
    screw_gap=b.x-a.x
    assert .000025<screw_gap<.000075,('Actual through-wrist screw bore',screw_gap)
    wood_tree=motion.surface(wood)['tree'];plate_tree=motion.surface(bpy.data.objects['Butt_Plate'])['tree'];cover=[]
    for x in (-.010,0,.010):
        for z in (-.095,-.070,-.050,-.030,0):
            origin=Vector((x,-.30,z));direction=Vector((0,1,0))
            metal=plate_tree.ray_cast(origin,direction,.1)[0];walnut=wood_tree.ray_cast(origin,direction,.1)[0]
            assert metal is not None and walnut is not None,(x,z)
            thickness=walnut.y-metal.y
            assert .0015<thickness<.005,(x,z,'Wood must remain behind curved steel',thickness)
            cover.append(dict(x_mm=x*1000,z_mm=z*1000,steel_before_wood_mm=thickness*1000))
    return dict(passed=True,rear_sight=sight,tangs=tongues,tang_screw_radial_wood_clearance_mm=screw_gap*1000,
        butt_plate_cover=cover,hammer_cocked_table_angle_degrees=table_angle,
        lever_inside_length_mm=length*1000,
        lever_inside_width_mm=width*1000,lever_bar_depth_mm=bar*1000,
        lever_bow_depth_mm=bow_depth*1000,
        lever_transverse_section_mm=(max(p.x for p in points)-min(p.x for p in points))*1000,
        lever_stroke=samples)


def plane(arm):
    """Called at every existing clearance pose, including imported subframes."""
    delta=arm.pose.bones['Lever'].matrix@arm.data.bones['Lever'].matrix_local.inverted()
    normal=delta.to_3x3()@Vector((1,0,0))
    error=(normal-Vector((1,0,0))).length
    assert error<2e-5 and abs(delta.translation.x)<2e-6,('Lever leaves gun mid-plane',error,list(delta.translation))
    return error
