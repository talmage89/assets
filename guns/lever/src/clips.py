"""Complete-pose authored schedules; STEP occupancy and a fixed internal Root."""
import math
from kit.weapon import action as weapon_action, hold, fcurves
from dimensions import TUBE_PITCH
from interface import CLIPS


def action(arm,name,keys):
    # A zero-scale display loses its decomposed rotation during glTF sampling.
    # Keep motion on a nonscaling guide; occupancy belongs to its child alone.
    routed=[]
    for frame,pose in keys:
        pose={bone:dict(channels) for bone,channels in pose.items()}
        for display,guide in [('CarrierRound','CarrierGuide'),('FiredCase','FiredGuide')]:
            if display not in pose:continue
            channels=pose[display]
            motion={key:value for key,value in channels.items() if key!='scale'}
            if motion:pose[guide]={**pose.get(guide,{}),**motion}
            pose[display]={key:value for key,value in channels.items() if key=='scale'}
        routed.append((frame,pose))
    return weapon_action(arm,name,routed)


def vis(on):return dict(scale=(int(on),)*3)
def tube(n):
    return {**{'Tube'+str(i):vis(i<=n) for i in range(1,7)},
            'Follower':dict(loc=(0,(n-6)*TUBE_PITCH*.001,0))}
def rest(n=6,live=True,case=False,hammer=44):
    return {**tube(n),'ChamberRound':vis(live),'FiredCase':vis(case),
            'CarrierRound':vis(False),'InsertRound':vis(False),
            'Hammer':dict(rot_deg=(hammer,0,0))}
def action_pose(lever=0,draw=0,lock=0,carrier=0,link=0):
    return {'Lever':dict(rot_deg=(lever-link,0,0)), 'Bolt':dict(loc=(0,-draw,0)),
            'LockingBlock':dict(loc=(0,0,-lock)), 'Carrier':dict(rot_deg=(carrier,0,0)),
            'Link':dict(rot_deg=(link,0,0))}


def cycle(n,last=False,empty=False):
    keys=[(0,rest(n,False,not empty,44 if empty else 0)),(2,{'Sear':dict(rot_deg=(-3,0,0))}),
      (6,{**action_pose(12,0,.030,0,6),'Hammer':dict(rot_deg=(90,0,0))}),
      (14,{**action_pose(43,.036,.030,0,20),'Hammer':dict(rot_deg=(90,0,0))}),
      (22,action_pose(80,.090,.030,0,20)),hold(23),
      (24,{'FiredCase':dict(loc=(0,.004,.020))}),
      (27,{'FiredCase':dict(loc=(0,.009,.060)),**{'Tube'+str(i):vis(False) for i in range(1,7)}}),
      (28,{'FiredCase':dict(loc=(-.008,.016,.090),rot_deg=(-18,0,0))}),
      (32,{'FiredCase':dict(loc=(-.022,.025,.155),rot_deg=(-48,0,0))}),
      (34,{'FiredCase':vis(False)})]
    if n and not last:
        # Start the lift only once the ejected case is above the opening.
        keys[8]=(28,{**keys[8][1],**tube(n-1),'CarrierRound':vis(True)})
        keys += [(36,{'Carrier':dict(rot_deg=(20,0,0)),'CarrierRound':dict(rot_deg=(20,0,0))}),hold(37),
                 (38,{'Bolt':dict(loc=(0,-.075,0)),'Carrier':dict(rot_deg=(6,0,0))}),
                 (44,{'Carrier':dict(rot_deg=(0,0,0)),'Bolt':dict(loc=(0,-.03409,0)),
                      'CarrierRound':dict(loc=(0,.04091,0))}),
                 (49,{'Bolt':dict(loc=(0,0,0)),'CarrierRound':dict(loc=(0,.075,0))}),
                 (50,{'CarrierRound':vis(False),'ChamberRound':vis(True),'Hammer':dict(rot_deg=(90,0,0))}),
                 (54,{'Carrier':dict(rot_deg=(0,0,0)),'Lever':dict(rot_deg=(4,0,0)),
                      'Link':dict(rot_deg=(4,0,0))})]
    else:
        # The linkage drives the empty carrier through the same cam stroke;
        # ammunition occupancy cannot switch mechanical travel off.
        keys += [(36,{'Carrier':dict(rot_deg=(20,0,0))}),hold(37),
                 (38,{'Carrier':dict(rot_deg=(6,0,0)),'Bolt':dict(loc=(0,-.075,0))}),
                 (44,{'Carrier':dict(rot_deg=(0,0,0)),'Bolt':dict(loc=(0,-.03409,0))}),
                 (49,{'Bolt':dict(loc=(0,0,0))}),
                 (50,{'Bolt':dict(loc=(0,0,0)),'Hammer':dict(rot_deg=(90,0,0))}),
                 (54,{'Lever':dict(rot_deg=(4,0,0)),'Link':dict(rot_deg=(4,0,0))})]
    keys[-1][1]['Sear']=dict(rot_deg=(-3,0,0))
    keys += [(57,{'Hammer':dict(rot_deg=(44,0,0))}),
             (58,{**action_pose(),'Sear':dict(rot_deg=(0,0,0))}),hold(60)]
    return keys


def insertion(n,offset=0,live=True):
    keys=[(0,rest(n,live)),hold(4),(8,{'Carrier':dict(rot_deg=(20,0,0))}),
          (10,{'LoadingGate':dict(rot_deg=(0,0,28))}),hold(11),
          (12,{'InsertRound':vis(True),'InsertGuide':dict(loc=(.002,.002,0),rot_deg=(0,0,30))}),
          (28,{'InsertGuide':dict(loc=(-.002,.009,0),rot_deg=(0,0,24)),
               'LoadingGate':dict(rot_deg=(0,0,24))}),
          (42,{'InsertGuide':dict(loc=(-.014,.038,0),rot_deg=(0,0,11.5))}),
          (48,{'InsertGuide':dict(loc=(-.022,.067,0),rot_deg=(0,0,3))}),
          (57,{'InsertGuide':dict(loc=(-.025,.097,0),rot_deg=(0,0,0)),
               **{'Tube'+str(i):dict(loc=(0,.06477,0)) for i in range(1,7)},
               'Follower':dict(loc=(0,(n-5)*TUBE_PITCH*.001,0))}),
          (58,{'InsertRound':vis(False),**tube(n+1)}),
          (62,{'LoadingGate':dict(rot_deg=(0,0,0))}),
          (66,{'Carrier':dict(rot_deg=(0,0,0))}),hold(72)]
    # Hold the old stack until the entering nose reaches it, then push it as
    # a contiguous train. The count event reindexes those same occluded slots.
    for f,pose in keys:
        if f<=42:
            for i in range(1,7):pose.setdefault('Tube'+str(i),{}).setdefault('loc',(0,0,0))
            pose.setdefault('Follower',{}).setdefault('loc',(0,(n-6)*TUBE_PITCH*.001,0))
        if f==58:
            for i in range(1,7):pose['Tube'+str(i)]['loc']=(0,0,0)
        if f==57:
            for i in range(1,7):pose['Tube'+str(i)]['scale']=(0,0,0)
    keyed={f:p for f,p in keys}
    path=[(12,.002,.002,30),(28,-.002,.009,24),(32,-.002,.019,24),(42,-.014,.038,11.5),
          (48,-.022,.067,3),(57,-.025,.097,0)]
    for f in range(12,58):
        a,b=next((a,b) for a,b in zip(path,path[1:]) if a[0]<=f<=b[0])
        t=(f-a[0])/(b[0]-a[0]);x=a[1]+(b[1]-a[1])*t;y=a[2]+(b[2]-a[2])*t;angle=a[3]+(b[3]-a[3])*t
        advance=max(0,min(.06477,.113+y+.06477*math.cos(math.radians(angle))+.00223*abs(math.sin(math.radians(angle)))-.210))
        pose=keyed.setdefault(f,{})
        pose['InsertGuide']=dict(loc=(x,y,0),rot_deg=(0,0,angle))
        if f<=28:pose['LoadingGate']=dict(rot_deg=(0,0,28-4*(f-12)/16))
        for i in range(1,7):
            bone='Tube'+str(i);pose[bone]={**pose.get(bone,{}),'loc':(0,advance,0)}
        pose['Follower']=dict(loc=(0,(n-6)*TUBE_PITCH*.001+advance,0))
    return [(f+offset,p) for f,p in sorted(keyed.items())]


def build_clips(arm):
    action(arm,'Idle',[(0,rest()),hold(1)])
    for n in range(7):
        name='Fire' if n==6 else ('FireLast' if n==0 else 'Fire'+str(n))
        action(arm,name,[(0,rest(n)),hold(1),(2,{'Trigger':dict(rot_deg=(-12,0,0))}),
               (3,{'Hammer':dict(rot_deg=(0,0,0)),'ChamberRound':vis(False),'FiredCase':vis(True)}),
               hold(9),(15,{'Trigger':dict(rot_deg=(0,0,0))}),hold(18)])
        name='Cycle' if n==6 else ('CycleLast' if n==0 else 'Cycle'+str(n))
        action(arm,name,cycle(n,n==0))
    action(arm,'CycleEmpty',cycle(0,True,True))
    action(arm,'Chamber',cycle(1,False,True))
    for n in range(6):
        action(arm,'IdleTube'+str(n),[(0,rest(n)),hold(60)])
        action(arm,'Reload' if n==5 else 'Reload'+str(n+1),insertion(n))
    keys=insertion(3)
    for n in (4,5): keys += insertion(n,72*(n-3))[1:]
    action(arm,'ReloadSeveral',keys)
    action(arm,'HammerSafe',[(0,rest()),(8,{'Sear':dict(rot_deg=(-3,0,0))}),(10,{'Hammer':dict(rot_deg=(46,0,0))}),
           (14,{'Trigger':dict(rot_deg=(-12,0,0))}),hold(16),
           (20,{'Hammer':dict(rot_deg=(36,0,0)),'Trigger':dict(rot_deg=(0,0,0))}),
           (42,{'Hammer':dict(rot_deg=(12,0,0)),'Sear':dict(rot_deg=(0,0,0))}),hold(48)])
    action(arm,'HammerCock',[(0,rest(hammer=12)),(6,{'Sear':dict(rot_deg=(-3,0,0))}),
           (24,{'Hammer':dict(rot_deg=(44,0,0))}),(30,{'Sear':dict(rot_deg=(0,0,0))})])
    action(arm,'Inspect',[(0,rest()),hold(24),(36,{'Hammer':dict(rot_deg=(46,0,0))}),
           hold(50),(64,{'Hammer':dict(rot_deg=(44,0,0))}),hold(120)])
    action(arm,'IdleEmpty',[(0,rest(0,False)),hold(60)])
    action(arm,'IdleUnchambered1',[(0,rest(1,False)),hold(60)])
    action(arm,'IdleOpen',[(0,{**rest(0,False,hammer=90),**action_pose(80,.090,.030,20,20)}),hold(60)])
    keys=insertion(0,live=False)
    keys += [(f+72,p) for f,p in cycle(1,False,True)[1:]]
    for n in range(6):keys+=insertion(n,132+72*n)[1:]
    action(arm,'ReloadEmpty',keys)
    # All changes in the hidden tube representation, including the follower,
    # commit as one discrete state. There is no half-frame follower collision.
    for act in __import__('bpy').data.actions:
        for fc in fcurves(act):
            if fc.data_path=='pose.bones["Follower"].location' and (act.name.startswith('Cycle') or act.name=='Chamber'):
                for k in fc.keyframe_points:k.interpolation='CONSTANT'
    assert set(t.name for t in arm.animation_data.nla_tracks)==set(CLIPS)
