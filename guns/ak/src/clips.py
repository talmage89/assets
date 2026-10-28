"""Authored visual motion, explicit holds and discrete round visibility.

No mechanically operative feed, lock, fire-control or gas simulation.
"""
from kit.weapon import action,hold
from interface import CLIPS
SAFE=0;AUTO=-16;SEMI=-26;STROKE=.100
def visibility(value):return dict(scale=(int(value),)*3)
def selector(angle):return {'Selector':dict(rot_deg=(angle,0,0))}
def trigger(pulled):return {'Trigger':dict(rot_deg=(-12 if pulled else 0,0,0))}
def cycle(d,rotation=0):return {'BoltCarrier':dict(loc=(0,-d,0)),
 'Bolt':dict(rot_deg=(0,rotation,0))}
def ready():return {**selector(SEMI),'EjectedCase':visibility(False),'Hammer':dict(rot_deg=(-35,0,0))}
def empty_mag():return {**{n:visibility(False) for n in ('TopRound','SecondRound','ThirdRound')},
 'Follower':dict(loc=(0,0,.014))}
def empty():return {**ready(),**empty_mag(),'ChamberRound':visibility(False)}
def rock(angle,loc=(0,0,0)):return {'Magazine':dict(rot_deg=(angle,0,0),loc=loc)}
def swap(reload_empty=False):
 p=[hold(10),(16,{'MagRelease':dict(rot_deg=(-14,0,0)),'MagCatch':dict(loc=(0,-.012,0))}),hold(20),
  (34,rock(28)),hold(38),(40,rock(28,(0,-.005,-.020))),
  (56,rock(35,(0,-.030,-.22))),hold(71),
  (72,{**rock(35,(0,-.030,-.22)),**({**{n:visibility(True) for n in ('TopRound','SecondRound','ThirdRound')},'Follower':dict(loc=(0,0,0))} if reload_empty else {})}),
  (92,rock(30,(0,-.005,-.040))),
  (112,rock(28)),hold(114),(132,rock(0)),hold(134),
  (138,{'MagRelease':dict(rot_deg=(0,0,0)),'MagCatch':dict(loc=(0,0,0))})]
 return p
def build_clips(arm):
 for n,p,f in [('Idle',ready(),1),('IdleEmpty',empty(),60),
  ('IdleSafe',{**ready(),**selector(SAFE)},1),
  ('IdleAutoReady',{**ready(),**selector(AUTO)},1),
  ('IdleAuto',{**ready(),**selector(AUTO),**trigger(True)},1)]:
  action(arm,n,[(0,p),hold(f)])
 fire=[(0,ready()),hold(1),(2,{**trigger(True),'ChamberRound':visibility(False),'Hammer':dict(rot_deg=(0,0,0))}),
  (3,{**cycle(.035,22),'Hammer':dict(rot_deg=(-35,0,0))}),
  (4,{**cycle(STROKE,22),'EjectedCase':visibility(True),'CaseTravel':dict(loc=(.026,0,.012))}),
  (5,{**cycle(.075,22),'CaseTravel':dict(loc=(.060,0,.035),rot_deg=(0,0,50))}),
  (6,{'EjectedCase':visibility(False)}),(8,{**cycle(0),'ChamberRound':visibility(True)}),hold(10),(12,trigger(False))]
 for n in ('Fire','FireSemi'):action(arm,n,fire)
 last=[(f,{**p,**(empty_mag() if f==0 else {}),**({'ChamberRound':visibility(False)} if f==8 else {})}) for f,p in fire]
 action(arm,'FireLast',last)
 action(arm,'FireAuto',[(0,{**ready(),**selector(AUTO),**trigger(True),'ChamberRound':visibility(False),'Hammer':dict(rot_deg=(0,0,0))}),
  (1,{**cycle(.035,22),'Hammer':dict(rot_deg=(-35,0,0))}),
  (2,{**cycle(STROKE,22),'EjectedCase':visibility(True),'CaseTravel':dict(loc=(.026,0,.012))}),
  (3,{**cycle(.075,22),'CaseTravel':dict(loc=(.060,0,.035),rot_deg=(0,0,50))}),
  (4,{'EjectedCase':visibility(False)}),(6,{**cycle(0),'ChamberRound':visibility(True)})])
 action(arm,'Reload',[(0,ready()),*swap(),hold(150)])
 action(arm,'ReloadEmpty',[(0,empty()),*swap(True),hold(154),
  (174,cycle(STROKE,22)),hold(178),(188,{**cycle(0),'ChamberRound':visibility(True)}),hold(210)])
 action(arm,'Charge',[(0,empty()),hold(8),(30,cycle(STROKE,22)),hold(34),(44,cycle(0)),hold(60)])
 action(arm,'Selector',[(0,{**ready(),**selector(SAFE)}),hold(6),(18,selector(AUTO)),hold(24),(36,selector(SEMI))])
 for name,a,b in [('SelectorSafe',SEMI,SAFE),('SelectorSemi',SAFE,SEMI),
  ('SelectorAuto',SEMI,AUTO),('SelectorAutoSemi',AUTO,SEMI)]:
  action(arm,name,[(0,{**ready(),**selector(a)}),hold(2),(10,selector(b)),hold(12)])
 action(arm,'AutoStart',[(0,{**ready(),**selector(AUTO)}),(2,trigger(True))])
 action(arm,'AutoStop',[(0,{**ready(),**selector(AUTO),**trigger(True)}),(6,trigger(False))])
 action(arm,'Inspect',[(0,ready()),hold(8),(22,selector(SAFE)),hold(49),(65,selector(SEMI)),hold(85),
  (100,cycle(.018,16)),hold(110),(125,cycle(0)),hold(150)])
 assert set(t.name for t in arm.animation_data.nla_tracks)==set(CLIPS)
