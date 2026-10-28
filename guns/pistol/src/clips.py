"""Visual-only mechanical schedule. Holds and state changes implement INTERFACE.md."""
from kit.weapon import action,hold
from interface import FPS
TRAVEL=.036
LOCK=.034

def mechanism(s):
 # Estimated visible path, not a tolerance/cam design. Short press checks stay
 # locked; full cycling gives the hood a modest photographic drop.
 return {'Slide':dict(loc=(0,-s,0)),
         'Barrel':dict(loc=(0,-min(s,.003),0),rot_deg=(min(1,max(0,(s-.003)/.006))*3,0,0)),
         'RecoilGuide':dict(loc=(0,-s*.5,0))}
def pull():return {'Trigger':dict(rot_deg=(-10,0,0)),'TriggerSafety':dict(rot_deg=(-9,0,0))}
def reset():return {'Trigger':dict(rot_deg=(0,0,0)),'TriggerSafety':dict(rot_deg=(0,0,0))}
def empty_mag():return {'TopRound':dict(scale=(0,0,0)),'ReserveRound':dict(scale=(0,0,0)),
                       'Follower':dict(loc=(0,.00404,.010))}
def empty_open():return {**empty_mag(),**mechanism(LOCK),'SlideStop':dict(rot_deg=(-7,0,0)),
                         'ChamberRound':dict(scale=(0,0,0))}
def magpose(d):return dict(loc=(0,-.404026*d,-d),rot_deg=(0,0,0))
def swap(empty=False):
 keys=[hold(10),(12,{'MagRelease':dict(loc=(.002,0,0))}),hold(15),
  (17,{'Magazine':magpose(.006)}),(28,{'Magazine':magpose(.075)}),
  (40,{'Magazine':dict(loc=(0,-.087,-.21),rot_deg=(8,0,0)),'MagRelease':dict(loc=(0,0,0))}),
  hold(46),(47,{}),(55,{'Magazine':dict(loc=(0,-.083,-.20),rot_deg=(-6,0,0))}),
  (73,{'Magazine':magpose(.055)}),(87,{'Magazine':magpose(.004)}),(91,{'Magazine':magpose(0)})]
 if empty:
  keys[7]=(47,{'TopRound':dict(scale=(1,1,1)),'ReserveRound':dict(scale=(1,1,1)),'Follower':dict(loc=(0,0,0))})
 return keys

def build_clips(arm):
 action(arm,'Idle',[(0,{}),(1,{})],fps=FPS)
 fire=[(0,{}),(2,{**pull(),**mechanism(0),'ChamberRound':dict(scale=(0,0,0))}),
  (3,mechanism(.006)),(4,mechanism(.026)),(5,mechanism(TRAVEL)),hold(6),
  (7,mechanism(.006)),(8,{**mechanism(0),'ChamberRound':dict(scale=(1,1,1))}),hold(10),(12,reset())]
 action(arm,'Fire',fire);action(arm,'FireSemi',fire)
 action(arm,'FireLast',[(0,empty_mag()),(2,{**pull(),**mechanism(0),'ChamberRound':dict(scale=(0,0,0))}),
  (3,mechanism(.006)),(4,mechanism(.026)),(5,mechanism(TRAVEL)),
  (6,{'SlideStop':dict(rot_deg=(-7,0,0))}),(7,mechanism(LOCK)),hold(10),(12,reset()),hold(15)])
 action(arm,'Reload',[(0,{})]+swap()+[hold(120)])
 action(arm,'ReloadEmpty',[(0,empty_open())]+swap(True)+[hold(110),
  (112,{'SlideStop':dict(rot_deg=(4,0,0))}),hold(113),(115,mechanism(.020)),
  (117,mechanism(.006)),(118,{**mechanism(0),'ChamberRound':dict(scale=(1,1,1))}),
  (124,{'SlideStop':dict(rot_deg=(0,0,0))}),hold(144)])
 action(arm,'Inspect',[(0,{}),hold(18),(30,mechanism(.002)),hold(54),(65,mechanism(0)),hold(90)])
 action(arm,'Charge',[(0,{**empty_mag(),'ChamberRound':dict(scale=(0,0,0))}),hold(6),
  (14,mechanism(.002)),(15,mechanism(.0054)),(16,mechanism(.009)),(24,mechanism(TRAVEL)),hold(28),
  (30,{**mechanism(LOCK),'SlideStop':dict(rot_deg=(-7,0,0))}),hold(36)])
 action(arm,'IdleOpen',[(0,empty_open()),hold(60)])
 action(arm,'IdleEmpty',[(0,{**empty_mag(),'ChamberRound':dict(scale=(0,0,0))}),hold(60)])
