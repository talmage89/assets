"""Authored continuous paths for the fictional pump action, in millimeters.

The game owns counts and physics. Clips retain their event frames; these paths
make the existing events visible on the shipped mesh instead of substituting
an occupied chamber while the bolt is still open.
"""
import math

PITCH=57.5
BREECH=186.1
LIFT=16.
BONES={'Carrier','CarrierGuide','CarrierShell','ChamberShell','FiredGuide','FiredHull',
       'ShellGuide','InsertShell',
       'Follower','TubeFeedGuide',*[f'Tube{i}' for i in range(1,5)]}

def lerp(x,knots):
    if x<=knots[0][0]:return knots[0][1]
    for (a,b),(c,d) in zip(knots,knots[1:]):
        if x<=c:return b+(d-b)*(x-a)/(c-a)
    return knots[-1][1]

def carried(angle):
    a=math.radians(angle)
    return (0,30+74*math.cos(a)-9*math.sin(a),20+74*math.sin(a)+9*math.cos(a))

PICKUP=carried(LIFT)[1]-11.2*math.sin(math.radians(LIFT))
TIP_OFFSET=carried(LIFT)[2]+PITCH*math.sin(math.radians(LIFT))-65
PIVOT_BEGIN=14+(BREECH-96-27)/(65/8)

def guide(head,angle=0):
    return dict(loc=(head[0]*.001,(head[1]-104)*.001,(head[2]-29)*.001),rot_deg=(angle,0,0))

def pushed(face):
    t=max(0,min(1,(face-PICKUP)/(145-PICKUP)))
    angle=LIFT*(1-t);a=math.radians(angle)
    head=(0,face+11.2*math.sin(a),65-PITCH*math.sin(a)+TIP_OFFSET*(1-t)**2)
    # Until the rim leaves the front of the tray, solve its supporting angle
    # from the actual authored low floor and circular rim. Mesh audits judge
    # the polygonal result and chamber clearance independently.
    def support(alpha):
        ca=math.radians(alpha)
        y=head[1]+11.2*math.sin(a)
        return 20+(y-30)*math.tan(ca)-2.2/math.cos(ca)+11.2*math.cos(a)
    lo,hi=0.,LIFT
    for _ in range(24):
        mid=(lo+hi)/2
        if support(mid)<head[2]:lo=mid
        else:hi=mid
    carrier=hi
    carrier=max(0,carrier-2*min(1,max(0,(face-PICKUP)/10)))
    if face>132:carrier*=max(0,(155-face)/23)
    return guide(head,angle),carrier

def draw(f,empty=False):
    begin,end=(46,50) if empty else (40,44)
    return lerp(f,[(0,0),(10 if not empty else 8,0),
        (14,27 if not empty else 96*6/18),(22,92 if not empty else 96*14/18),
        (24,96 if not empty else 96*16/18),
        (26,96),(36 if empty else 30,96),(begin,BREECH-PICKUP),(end,0)])

def ejection(f):
    d=draw(f)
    if f<=20:return dict(loc=(0,-d*.001,0),rot_deg=(0,0,0))
    if f<=23.2:
        t=max(0,(f-PIVOT_BEGIN)/(23.2-PIVOT_BEGIN))
        roll_degrees=lerp(f,[(20,0),(PIVOT_BEGIN,-3),(23.2,-8)])
        yaw=math.radians(70*t);roll=math.radians(roll_degrees)
        x=11.2*math.cos(roll);y=1.4;z=-11.2*math.sin(roll)
        rx=x*math.cos(yaw)+y*math.sin(yaw)
        ry=-x*math.sin(yaw)+y*math.cos(yaw)
        return dict(loc=((11.2-rx)*.001,(-d+1.4-ry)*.001,-z*.001),rot_deg=(0,roll_degrees,-70*t))
    start=ejection(23.2);t=(f-23.2)/60
    return dict(loc=(start['loc'][0]+1.4*t,start['loc'][1]+.8*t,start['loc'][2]-4.905*t*t),
                rot_deg=(80*t,-8,-70-300*t))

def count_delta(clip,f):
    if clip.startswith('Fire') and clip!='FireLast':return -int(f>=30)
    if clip=='ReloadEmpty':return sum(f>=144+72*i for i in range(4))
    if clip.startswith('Reload'):return int(f>=60)
    return 0

def animate(arm):
    import bpy
    from kit import weapon as W
    from interface import CLIPS,STATES
    for clip,spec in CLIPS.items():
        if not clip.startswith(('Fire','Reload')) and clip!='Inspect':continue
        frames={i/4 for i in range(spec['frames']*4+1)}
        if clip.startswith('Fire'):frames.update((PIVOT_BEGIN,23.2,*[PIVOT_BEGIN+i/20 for i in range(50)]))
        frames=sorted(f for f in frames if 0<=f<=spec['frames'])
        snapshots=[]
        start_n=STATES[spec['start']]['tube']
        for f in frames:
            W.pose(arm,clip,f)
            values={}
            if clip.startswith('Fire') or (clip=='ReloadEmpty' and f<84):
                empty=clip=='ReloadEmpty';feeding=clip!='FireLast'
                d=draw(f,empty)
                values.update(Bolt=dict(loc=(0,-d*.001,0)),Forend=dict(loc=(0,-d*.001,0)))
                begin,end=(46,50) if empty else (40,44)
                lift_begin,lift_end=(36,44) if empty else (30,40)
                ca=lerp(f,[(0,0),(lift_begin,0),(lift_end,LIFT),(begin,LIFT)])
                if f>begin:
                    live,ca=pushed(BREECH-d)
                elif empty and f<36:
                    live=guide((lerp(f,[(0,90),(28,60),(32,0)]),
                        lerp(f,[(0,-100),(20,-100),(24,40),(28,104)]),
                        lerp(f,[(0,63),(32,63),(36,29)])))
                elif not empty and f<=30:
                    live=guide((0,lerp(f,[(0,200),(26,200),(30,104)]),29))
                else:live=guide(carried(ca),ca)
                if f>=end:ca=0
                if not feeding:
                    ca=lerp(f,[(0,0),(30,0),(40,LIFT),(41,LIFT),(44,0)])
                values['Carrier']=dict(rot_deg=(ca,0,0))
                values['CarrierGuide']=live
                values['CarrierShell']=dict(scale=(int(feeding and (20<=f<end if empty else f<end)),)*3)
                values['ChamberShell']=dict(scale=(int(f>=end or (not empty and f<2)),)*3 if feeding else (int(f<2),)*3)
                values['FiredGuide']=ejection(f) if not empty else dict(loc=(0,0,0),rot_deg=(0,0,0))
                values['FiredHull']=dict(scale=(int(not empty and 2<=f<32),)*3)
                # Left latch releases the first shell. The right interceptor
                # keeps the next one at its forward station until return.
                left=lerp(f,[(0,0),(25,0),(26,-2),(31,-2),(32,0)])
                right=lerp(f,[(0,2),(24,2),(25,0),(41,0),(42,2)])
                values['ShellStopL']=dict(loc=(left*.001,0,0))
                values['ShellStopR']=dict(loc=(right*.001,0,0))
                if not empty and feeding:
                    n=start_n-int(f>=30)
                    advance=lerp(f,[(0,0),(26,0),(30,-PITCH+3.4)]) if f<30 else lerp(f,[(30,3.4),(42,3.4),(43,0)])
                    for i in range(1,5):
                        on=2<=i<=start_n if f<30 else i<=n
                        values[f'Tube{i}']=dict(loc=(0,advance*.001,0),scale=(int(on),)*3)
                    follower=(start_n-4)*PITCH+advance if f<30 else (n-4)*PITCH+advance
                else:
                    for i in range(1,5):values[f'Tube{i}']=dict(loc=(0,0,0),scale=(0,0,0))
                    # Empty follower is pressed forward before interception;
                    # its rim is then returned to the left retaining land.
                    follower=-4*PITCH+lerp(f,[(0,0),(23,0),(24,3.4),(42,3.4),(43,0)])
                values['Follower']=dict(loc=(0,follower*.001,0))
            if clip=='Inspect':
                values['ChamberShell']=dict(loc=(0,arm.pose.bones['Bolt'].location.y,0))
            # The same visible insertion pushes the complete existing stack.
            starts=[84+72*i for i in range(4)] if clip=='ReloadEmpty' else ([0] if clip.startswith('Reload') else [])
            for index,offset in enumerate(starts):
                sf=f-offset
                if not 0<=sf<=72:continue
                n=index if clip=='ReloadEmpty' else start_n
                y=lerp(sf,[(0,94),(12,94),(26,94),(28,95),(44,142.5),(59,200),(72,200)])
                z=lerp(sf,[(0,-36),(12,-36),(26,29)])
                angle=lerp(sf,[(0,20),(12,20),(26,0)])
                values['ShellGuide']=dict(loc=(0,(y-130)*.001,(z-29)*.001),rot_deg=(angle,0,0))
                advance=max(0,min(PITCH,y+PITCH*math.cos(math.radians(angle))-200))
                commit=sf>=60
                for i in range(1,5):
                    values[f'Tube{i}']=dict(loc=(0,0 if commit else advance*.001,0),scale=(int(i<=n+int(commit)),)*3)
                values['Follower']=dict(loc=(0,((n-4)*PITCH+advance if not commit else (n-3)*PITCH)*.001,0))
                values['InsertShell']=dict(scale=(int(12<=sf<60),)*3)
                values['ShellStopL']=dict(loc=(lerp(sf,[(0,0),(42,0),(43,-.002),(60,-.002),(62,0)]),0,0))
                values['ShellStopR']=dict(loc=(.002,0,0))
            snapshots.append((f,values))
        act=bpy.data.actions[clip];W.pose(arm,clip,0)
        for f,values in snapshots:
            for name,value in values.items():
                bone=arm.pose.bones[name]
                for prop,key in [('location','loc'),('rotation_euler','rot_deg'),('scale','scale')]:
                    if key not in value:continue
                    setattr(bone,prop,tuple(math.radians(v) for v in value[key]) if key=='rot_deg' else value[key])
                    bone.keyframe_insert(prop,frame=f,group=name)
        for fc in W.fcurves(act):
            if any(fc.data_path.startswith('pose.bones["'+n+'"]') for n in BONES|{'Bolt','Forend','ShellStopL','ShellStopR','ShellGuide','InsertShell'}):
                for key in fc.keyframe_points:key.interpolation='CONSTANT' if fc.data_path.endswith('scale') else 'LINEAR'
    retarget_tube(arm)
    W.pose(arm,None,0)

def retarget_tube(arm):
    """Continuous parent travel and STEP child slot indexing, without blanks."""
    import bpy
    from kit import weapon as W
    from interface import CLIPS
    for clip in CLIPS:
        act=bpy.data.actions[clip]
        frames=sorted({float(k.co.x) for fc in W.fcurves(act) for k in fc.keyframe_points})
        samples=[]
        for f in frames:
            W.pose(arm,clip,f);diff=count_delta(clip,f)
            samples.append((f,arm.pose.bones['Tube1'].location.y+diff*PITCH*.001,-diff*PITCH*.001))
        W.pose(arm,clip,0)
        for f,advance,index in samples:
            g=arm.pose.bones['TubeFeedGuide'];g.location=(0,advance,0);g.keyframe_insert('location',frame=f,group=g.name)
            for i in range(1,5):
                b=arm.pose.bones[f'Tube{i}'];b.location=(0,index,0);b.keyframe_insert('location',frame=f,group=b.name)
        for fc in W.fcurves(act):
            if any(fc.data_path==f'pose.bones["Tube{i}"].location' for i in range(1,5)):
                for key in fc.keyframe_points:key.interpolation='CONSTANT'
            elif fc.data_path=='pose.bones["TubeFeedGuide"].location':
                for key in fc.keyframe_points:key.interpolation='LINEAR'
