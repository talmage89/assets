"""Authored visual cartridge paths; meters, not manufacturing geometry.

The ramp/mouth envelope supplies the lower support of the visual cartridge.
All schedule times are kept in clips.py. No dynamics or gameplay ammo count.
"""
import math

MAG_SHIFT = 47.0                 # mm, entire box/well and catch
ROUND_SHIFT = MAG_SHIFT - 2.5    # place the head near the rear wall
FEED_RISE = 4.5                  # mm, inner lip/stack, exterior box unchanged
HEAD = (0, 107.5, 50.5)
CHAMBER_HEAD = 209.5
TRAVEL = .104
RAMP = [(181.5,47.0),(194,53.0),(197.65,56.2),
        (197.8,49.8),(205.2,49.8),(205.35,55.35),(209.5,56.2),(214,58.8)]
PROFILE = [(0,6.005),(1.3,6.005),(1.3,5.1),(2.6,5.1),
           (2.6,5.96),(39.5,5.72),(44.5,4.37),(51.18,4.37),(51.18,3.91),
           (55,3.91),(59,3.65),(64,2.8),(68,1.65),(71.12,.1)]

def lerp_knots(x, knots):
    if x <= knots[0][0]: return knots[0][1]
    for (a,b),(c,d) in zip(knots,knots[1:]):
        if x <= c: return b+(d-b)*(x-a)/(c-a)
    return knots[-1][1]

def path(face_y):
    """Head position / pitch at the given bolt-face station, in mm/degrees.

    The tilted rim's rearmost upper corner stays on the bolt plane. Support
    comes from the ramp then the lower chamber mouth. Chamber radius is read
    from our own visual barrel profile, rather than a functional specification.
    """
    if face_y <= HEAD[1]: return HEAD, 0.0
    def support(degrees, face=face_y):
        angle=math.radians(degrees);sn,cs=math.sin(angle),math.cos(angle)
        y=face+6.005*sn;z=-1000
        for (s0,r0),(s1,r1) in zip(PROFILE,PROFILE[1:]):
            # Extrema occur at profile endpoints and where an edge crosses a
            # ramp/chamber station. Include the narrow lug-relief shoulders;
            # uniform axial samples can miss them by more than half a mm.
            yy0=y+s0*cs+r0*sn;dy=(s1-s0)*cs+(r1-r0)*sn
            fractions={0.,1.}
            if abs(dy)>1e-12:
                for station in [*[p[0] for p in RAMP],210,214,249.5,254.5,261,262]:
                    t=(station-yy0)/dy
                    if 0<t<1:fractions.add(t)
            for t in fractions:
                s=s0+(s1-s0)*t;r=r0+(r1-r0)*t
                yy=y+s*cs+r*sn;low=s*sn-r*cs
                if RAMP[0][0] <= yy <= RAMP[-1][0]:z=max(z,lerp_knots(yy,RAMP)-low)
                if yy>=210:
                    radius=lerp_knots(yy,[(210,8.8),(214,6.2),(249.5,6.2),(254.5,4.55),(261,4.55),(262,4.0)])
                    z=max(z,65-radius-low)
        return z
    def initial(face):
        if support(0,face)<=HEAD[2]:return 0.0
        lo,hi=0.,16.
        for _ in range(24):
            mid=(lo+hi)/2
            if support(mid,face)>HEAD[2]:lo=mid
            else:hi=mid
        return hi
    degrees=initial(face_y) if face_y<=139 else initial(139)*max(0,(178-face_y)/39)
    angle=math.radians(degrees);y=face_y+6.005*math.sin(angle)
    z=max(HEAD[2],support(degrees))
    # A small clearance for the polygonal barrel and angled case shoulder,
    # tapered out at the final concentric seat. Independent mesh sweeps check it.
    z+=lerp_knots(face_y,[(107.5,0),(120,0),(145,.08),(178,.08),(209.5,0)])
    # Settle the case concentrically inside the closed chamber.
    if face_y>=178:z=max(z,lerp_knots(face_y,[(178,64.8),(209.5,65)]))
    return (0,y,z),math.degrees(angle)

def feeding(face_y):
    p,angle=path(face_y)
    return dict(loc=tuple((p[i]-HEAD[i])*.001 for i in range(3)),rot_deg=(angle,0,0))

def ejection(frame):
    """Rightward pivot followed by a short ballistic continuation, Fire frames.

    The plunger is already compressed under the case head. It can pivot the
    case only when its mouth clears the receiver's front port bridge.
    """
    draw=TRAVEL*max(0,min(1,(frame-46)/18))
    head=(0,CHAMBER_HEAD*.001-draw,.065)
    if frame <= 61.6: return dict(loc=(0,-draw,0),rot_deg=(0,0,0))
    if frame <= 63:
        angle=math.radians((frame-61.6)/1.4*65)
        # Rim held at the right-side claw while the nose pivots outward.
        x=.006005*(1-math.cos(angle))-.0013*math.sin(angle)
        y=head[1]+.006005*math.sin(angle)+.0013*(1-math.cos(angle))
        return dict(loc=(x,y-CHAMBER_HEAD*.001,0),rot_deg=(0,0,-math.degrees(angle)))
    t=(frame-63)/60
    at=ejection(63)
    return dict(loc=(at['loc'][0]+1.4*t,at['loc'][1]-.65*t,
                     .85*t-4.905*t*t),rot_deg=(140*t,0,-65-450*t))

def animate(arm):
    """Add explicit sampled paths without changing other bone channels."""
    import bpy
    from kit import weapon as W
    from interface import CLIPS
    names=('TopRound','ReserveRound','Follower','ChamberRound','CycleCase')
    for clip,spec in CLIPS.items():
        act=bpy.data.actions[clip]
        for fc in W.fcurves(act):
            if fc.data_path.startswith('pose.bones["CycleCase"]'):
                for k in fc.keyframe_points:k.co.y=0 if fc.data_path.endswith('scale') else 0
        if clip not in ('Fire','FireLast','ReloadEmpty'):continue
        # Capture complete base channels before replacing ammunition alone.
        samples=[]
        frames=sorted({*[float(i) for i in range(spec['frames']+1)],61.6,63.0} if clip.startswith('Fire') else {float(i) for i in range(spec['frames']+1)})
        if clip.startswith('Fire'):frames=sorted({*frames,*[61.6+i/10 for i in range(45)]})
        if clip=='Fire':frames=sorted({*frames,76+2/104*28})
        if clip=='ReloadEmpty':frames=sorted({*frames,195+2/104*24})
        if clip=='Fire':frames=sorted({*frames,*[76+i/4 for i in range(113)]})
        if clip=='ReloadEmpty':frames=sorted({*frames,*[195+i/4 for i in range(97)]})
        for f in frames:
            W.pose(arm,clip,f)
            values={name:dict(loc=tuple(arm.pose.bones[name].location),
                rot_deg=tuple(math.degrees(v) for v in arm.pose.bones[name].rotation_euler),
                scale=tuple(arm.pose.bones[name].scale)) for name in names}
            values['CycleCase']=dict(loc=(0,0,0),rot_deg=(0,0,0),scale=(0,0,0))
            if clip.startswith('Fire'):
                values['ChamberRound']['scale']=(1,1,1) if f<3 or (clip=='Fire' and f>=104) else (0,0,0)
                if 3<=f<=66:values['CycleCase']={**ejection(f), 'scale':(1,1,1) if f<66 else (0,0,0)}
            if clip != 'FireLast':
                begin,end,reset=(76,104,122) if clip=='Fire' else (195,219,242)
                if begin<f<reset:
                    face=CHAMBER_HEAD-TRAVEL*1000*(1-min(1,(f-begin)/(end-begin)))
                    values['TopRound']={**feeding(face),'scale':(1,1,1) if f<end else (0,0,0)}
                    rise=11.8*max(0,min(1,(face-150)/28))
                    values['ReserveRound']=dict(loc=(-.0037*rise/11.8,0,rise*.001),rot_deg=(0,0,0),scale=(1,1,1))
                    values['Follower']=dict(loc=(0,0,rise*.001),rot_deg=(0,0,0),scale=(1,1,1))
            samples.append((f,values))
        W.pose(arm,clip,0)
        for f,values in samples:
            for name,val in values.items():
                b=arm.pose.bones[name];b.location=val['loc'];b.rotation_euler=tuple(math.radians(v) for v in val['rot_deg']);b.scale=val['scale']
                for prop in ('location','rotation_euler','scale'):b.keyframe_insert(prop,frame=f,group=name)
        for fc in W.fcurves(act):
            if any(fc.data_path.startswith('pose.bones["'+n+'"]') for n in names):
                for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path.endswith('scale') else 'LINEAR'
    W.pose(arm,None,0)
