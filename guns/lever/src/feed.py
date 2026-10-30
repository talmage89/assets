"""Continuous authored tube/carrier/bolt paths for the visual game asset.

No gameplay counts or dynamics. Event/state names remain in interface.py.
All positions below describe our fictional mesh in millimeters.
"""
import math

BONES={'Lever','Link','Carrier','CarrierGuide','CarrierRound','FiredGuide','FiredCase','ChamberRound',
       'Follower','TubeFeedGuide',*[f'Tube{i}' for i in range(1,7)]}
HEAD=(0,136,20)
PIVOT=(0,85,7)
LIFT=16.0

def lerp(f,knots):
    if f<=knots[0][0]:return knots[0][1]
    for (a,b),(c,d) in zip(knots,knots[1:]):
        if f<=c:return b+(d-b)*(f-a)/(c-a)
    return knots[-1][1]

def guide(head,angle=0):
    a=math.radians(angle);dy=HEAD[1]-PIVOT[1];dz=HEAD[2]-PIVOT[2]
    rotated=(0,PIVOT[1]+dy*math.cos(a)-dz*math.sin(a),
             PIVOT[2]+dy*math.sin(a)+dz*math.cos(a))
    return dict(loc=tuple((head[i]-rotated[i])*.001 for i in range(3)),rot_deg=(angle,0,0))

def raised(angle=LIFT):
    a=math.radians(angle)
    return (0,85+51*math.cos(a)-13*math.sin(a),7+51*math.sin(a)+13*math.cos(a))

PICKUP=raised()[1]-6.2*math.sin(math.radians(LIFT))
PROFILE=[(0,6.2),(.18,6.425),(1.5,6.425),(1.63,5.35),(2.2,5.05),
         (3.1,5.355),(36.6,5.095),(39.69,4.23),(51.8,4.19),
         (55.5,3.91),(59,3.78),(62.8,2.95),(64,2.4),(64.77,2.23)]
CHAMBER=[(200,6.45),(201.62,6.45),(201.621,5.6),(203.1,5.46),
         (236.6,5.2),(239.7,4.3),(252,4.3),(257,4.5),(266,3.85)]

def supported(face):
    angle=lerp(face,[(PICKUP,LIFT),(180,0),(200,0)])
    a=math.radians(angle);sn,cs=math.sin(a),math.cos(a)
    head_y=face+6.2*sn
    ca=math.radians(lerp(face,[(PICKUP,LIFT),(160,0)]))
    tray_ends=[85+(y-85)*math.cos(ca)-6.70*math.sin(ca) for y in (132,200)]
    z=-1000.
    stations=tray_ends+[p[0] for p in CHAMBER]
    for (s0,r0),(s1,r1) in zip(PROFILE,PROFILE[1:]):
        yy0=head_y+s0*cs+r0*sn;dy=(s1-s0)*cs+(r1-r0)*sn
        ts={0.,1.}
        if abs(dy)>1e-12:
            ts.update((yy-yy0)/dy for yy in stations if 0<(yy-yy0)/dy<1)
        for t in ts:
            s=s0+(s1-s0)*t;r=r0+(r1-r0)*t
            y=head_y+s*cs+r*sn;low=s*sn-r*cs
            if tray_ends[0]<=y<=tray_ends[1]:
                floor=7+(y-85)*math.tan(ca)+6.70/math.cos(ca)
                z=max(z,floor-low-.125/math.cos(ca))
            if y>=200:z=max(z,48-lerp(y,CHAMBER)-low)
    z+=lerp(face,[(PICKUP,0),(140,.025),(180,.025),(200,0)])
    if face>=180:z=max(z,lerp(face,[(180,47.9),(200,48)]))
    return (0,head_y,z),angle

def live(f,face):
    if f<=28:
        return guide((0,lerp(f,[(0,210),(14,210),(28,136)]),20))
    if f<=36:
        angle=lerp(f,[(28,0),(36,LIFT)])
        return guide(raised(angle),angle)
    if face<=PICKUP:return guide(raised(),LIFT)
    head,angle=supported(face)
    return guide(head,angle)

def ejection(f,draw):
    if f<=19:return dict(loc=(0,-draw,0),rot_deg=(0,0,0))
    if f<=22:
        angle=lerp(f,[(19,0),(22,75)]);a=math.radians(angle)
        return dict(loc=(0,-draw+(1.5*(1-math.cos(a))+6.425*math.sin(a))*.001,
                         (6.425*(1-math.cos(a))-1.5*math.sin(a))*.001),rot_deg=(angle,0,0))
    start=ejection(22,.090);t=(f-22)/60
    return dict(loc=(.20*t,start['loc'][1]-.20*t,start['loc'][2]+2.1*t-4.905*t*t),
                rot_deg=(75+260*t,0,80*t))

def animate(arm):
    import bpy
    from kit import weapon as W
    from interface import CLIPS,STATES
    for clip,spec in CLIPS.items():
        cycle=clip.startswith('Cycle') or clip=='Chamber' or clip=='ReloadEmpty'
        if not cycle:continue
        offset=72 if clip=='ReloadEmpty' else 0
        feeding=clip not in ('CycleEmpty','CycleLast')
        n=1 if clip=='ReloadEmpty' else STATES[spec['start']]['tube']
        case=clip.startswith('Cycle') and clip!='CycleEmpty'
        pickup_frame=38+(PICKUP-125)/(.075-.03409)/1000*6
        frames=sorted({0.,float(spec['frames']),offset+pickup_frame,*[offset+i/4 for i in range(241)]})
        snapshots=[]
        for frame in frames:
            W.pose(arm,clip,frame)
            if not offset<=frame<=offset+60:continue
            f=frame-offset
            draw=-arm.pose.bones['Bolt'].location.y
            link=lerp(f,[(0,0),(6,6),(14,20),(36,20),(49,4),(58,0)])
            lever=lerp(f,[(0,0),(6,12),(14,43),(22,72),(36,80),(49,8),(58,0)])
            values=dict(Link=dict(rot_deg=(link,0,0)),Lever=dict(rot_deg=(lever-link,0,0)))
            if feeding:
                carrier_angle=lerp(f,[(0,0),(28,0),(36,LIFT),(pickup_frame,LIFT)]) if f<=pickup_frame else lerp(200-draw*1000,[(PICKUP,LIFT),(160,0)])
                values['Carrier']=dict(rot_deg=(carrier_angle,0,0))
                values['CarrierGuide']=live(f,200-draw*1000)
                values['CarrierRound']=dict(scale=(1,1,1) if f<50 else (0,0,0))
                values['ChamberRound']=dict(scale=(0,0,0) if f<50 else (1,1,1))
                advance=lerp(f,[(0,0),(14,0),(28,-64.77)])*.001
                for i in range(1,7):
                    visible=(2<=i<=n) if f<28 else (i<=n-1)
                    values[f'Tube{i}']=dict(loc=(0,advance if f<28 else 0,0),scale=(int(visible),)*3)
                values['Follower']=dict(loc=(0,(n-6)*.06477+advance,0))
                # The tube's first display is represented by the same high
                # carrier cartridge from its retained pose to chamber seat.
                values['TubeStop']=dict(rot_deg=(0,0,lerp(f,[(0,0),(13,0),(14,-38),(27,-38),(28,0)])))
                values['TubeCutoff']=dict(rot_deg=(0,0,lerp(f,[(0,38),(16,38),(17,0),(29,0),(32,38)])))
            else:
                values['Carrier']=dict(rot_deg=(lerp(f,[(0,0),(28,0),(36,LIFT),(37,LIFT),(44,0)]),0,0))
            values['FiredGuide']=ejection(f,draw) if case else dict(loc=(0,0,0),rot_deg=(0,0,0))
            values['FiredCase']=dict(scale=(int(case and f<30),)*3)
            snapshots.append((frame,values))
        act=bpy.data.actions[clip]
        W.pose(arm,clip,0)
        for frame,values in snapshots:
            for name,value in values.items():
                bone=arm.pose.bones[name]
                for prop,key in [('location','loc'),('rotation_euler','rot_deg'),('scale','scale')]:
                    if key not in value:continue
                    setattr(bone,prop,tuple(math.radians(v) for v in value[key]) if key=='rot_deg' else value[key])
                    bone.keyframe_insert(prop,frame=frame,group=name)
        for fc in W.fcurves(act):
            if any(fc.data_path.startswith('pose.bones["'+n+'"]') for n in BONES|{'TubeStop','TubeCutoff'}):
                for key in fc.keyframe_points:key.interpolation='CONSTANT' if fc.data_path.endswith('scale') else 'LINEAR'
    W.pose(arm,None,0)
    retarget_tube(arm)


def retarget_tube(arm):
    """Continuous stack motion + STEP local slot indexing, with no blank frame.

    glTF cannot mix STEP and LINEAR intervals within one sampler. A nonscaling
    parent supplies the continuous spring/insertion travel; child translations
    supply only the discrete index offset. At each commit the complete set of
    physical occupied positions coincides, including in the diagnostic section.
    """
    import bpy
    from kit import weapon as W
    from interface import CLIPS
    for clip in CLIPS:
        act=bpy.data.actions[clip]
        frames=sorted({float(k.co.x) for fc in W.fcurves(act) for k in fc.keyframe_points})
        samples=[]
        for f in frames:
            W.pose(arm,clip,f)
            if clip=='ReloadEmpty':diff=int(f>=58)-int(f>=100)+sum(f>=190+72*i for i in range(6))
            elif clip=='ReloadSeveral':diff=sum(f>=58+72*i for i in range(3))
            elif clip.startswith('Reload'):diff=int(f>=58)
            elif (clip.startswith('Cycle') and clip not in ('CycleEmpty','CycleLast')) or clip=='Chamber':diff=-int(f>=28)
            else:diff=0
            advance=arm.pose.bones['Tube1'].location.y+diff*.06477
            samples.append((f,advance,-diff*.06477))
        W.pose(arm,clip,0)
        for f,advance,index in samples:
            guide=arm.pose.bones['TubeFeedGuide'];guide.location=(0,advance,0)
            guide.keyframe_insert('location',frame=f,group=guide.name)
            for i in range(1,7):
                bone=arm.pose.bones[f'Tube{i}'];bone.location=(0,index,0)
                bone.keyframe_insert('location',frame=f,group=bone.name)
        for fc in W.fcurves(act):
            if any(fc.data_path==f'pose.bones["Tube{i}"].location' for i in range(1,7)):
                for key in fc.keyframe_points:key.interpolation='CONSTANT'
            elif fc.data_path=='pose.bones["TubeFeedGuide"].location':
                for key in fc.keyframe_points:key.interpolation='LINEAR'
    W.pose(arm,None,0)
