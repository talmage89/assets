"""Explicit visual holds and discrete ammunition, independent handle/bolt owners.

Distances and angles are authored for the exterior game prop, not a functional
mechanism or manufacturing specification. No whole-instance movement is keyed.
"""
from kit.weapon import action,hold
from interface import CLIPS
STROKE=.084
SEMI=42
AUTO=83
LOCK_ANGLE=35

def vis(v):return dict(scale=(int(v),)*3)
def selector(deg):return {'Selector':dict(rot_deg=(deg,0,0))}
def empty_mag():
 return {**{n:vis(False) for n in ('TopRound','SecondRound','ThirdRound')},
         'Follower':dict(loc=(0,-.002,.017))}
def ready():return selector(SEMI)
def empty():return {**ready(),**empty_mag(),'ChamberRound':vis(False)}
def bolt(d):return {'Bolt':dict(loc=(0,-d,0))}
def handle(d,angle=0):return {'ChargingHandle':dict(loc=(0,-d,0),rot_deg=(0,angle,0))}
def pull(v=True):return {'Trigger':dict(rot_deg=(-12 if v else 0,0,0))}
def mag(d,angle=0):return {'Magazine':dict(loc=(0,d*.14,-d),rot_deg=(angle,0,0))}
def swap(offset=0,empty=False):
 keys=[(10,{}),(14,{'MagRelease':dict(rot_deg=(12,0,0)),'MagCatch':dict(loc=(-.0035,0,0))}),hold(18),
  (23,mag(.008)),(34,mag(.085)),(46,{**mag(.22,9),'MagRelease':dict(rot_deg=(0,0,0))}),
  hold(55),(56,{}),(64,mag(.22,-6)),(84,mag(.065)),(98,mag(.006)),(104,mag(0)),hold(106),(110,{'MagCatch':dict(loc=(0,0,0))})]
 if empty:keys[7]=(56,{**{n:vis(True) for n in ('TopRound','SecondRound','ThirdRound')},'Follower':dict(loc=(0,0,0))})
 return [(f+offset,p) for f,p in keys]
def draw(offset=0):
 return [(6+offset,{}),(12+offset,handle(.003)),(30+offset,{**handle(STROKE),**bolt(STROKE)}),
  hold(34+offset),(42+offset,handle(STROKE,LOCK_ANGLE))]
def build_clips(arm):
 action(arm,'Idle',[(0,ready()),hold(1)])
 fire=[(0,ready()),hold(1),(2,{**pull(),'ChamberRound':vis(False)}),
       (3,bolt(.034)),(4,bolt(STROKE)),(5,bolt(.061)),(7,{**bolt(0),'ChamberRound':vis(True)}),hold(9),(12,pull(False))]
 action(arm,'Fire',fire);action(arm,'FireSemi',fire)
 action(arm,'FireLast',[(0,{**ready(),**empty_mag()}),*fire[1:6],
  (7,bolt(0)),hold(9),(12,pull(False))])
 action(arm,'FireAuto',[(0,{**selector(AUTO),**pull(),'ChamberRound':vis(False)}),
  (1,bolt(.035)),(2,bolt(STROKE)),(3,bolt(.060)),(5,{**bolt(0),'ChamberRound':vis(True)})])
 action(arm,'Reload',[(0,ready()),*swap(),hold(132)])
 action(arm,'ReloadEmpty',[(0,empty()),*draw(),*swap(44,True),hold(169),
  (171,handle(STROKE,18)),(175,handle(STROKE,0)),(178,{**handle(.041),**bolt(.041)}),
  (181,{**handle(0),**bolt(0),'ChamberRound':vis(True)}),hold(210)])
 action(arm,'Charge',[(0,empty()),*draw(),hold(60)])
 action(arm,'Inspect',[(0,ready()),hold(8),(18,selector(0)),hold(42),(54,ready()),
  hold(68),(82,{**handle(.007),**bolt(.004)}),hold(92),(104,{**handle(0),**bolt(0)}),hold(120)])
 action(arm,'Selector',[(0,selector(0)),(10,ready()),(20,selector(AUTO))])
 for name,a,b in [('SelectorSafe',SEMI,0),('SelectorSemi',0,SEMI),('SelectorAuto',SEMI,AUTO),('SelectorAutoSemi',AUTO,SEMI)]:
  action(arm,name,[(0,selector(a)),hold(2),(10,selector(b)),hold(12)])
 action(arm,'AutoStart',[(0,selector(AUTO)),(2,pull())])
 action(arm,'AutoStop',[(0,{**selector(AUTO),**pull()}),(6,pull(False))])
 action(arm,'IdleAuto',[(0,{**selector(AUTO),**pull()}),hold(1)])
 action(arm,'IdleAutoReady',[(0,selector(AUTO)),hold(1)])
 action(arm,'IdleSafe',[(0,selector(0)),hold(1)])
 action(arm,'IdleEmpty',[(0,empty()),hold(60)])
 action(arm,'IdleOpen',[(0,{**empty(),**bolt(STROKE),**handle(STROKE,LOCK_ANGLE)}),hold(60)])
 assert set(t.name for t in arm.animation_data.nla_tracks)==set(CLIPS)
