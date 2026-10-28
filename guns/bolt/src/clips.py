"""60 Hz visual schedules. Explicit holds, discrete ammunition, fixed Root."""
from kit.weapon import action,hold
from interface import FPS
TRAVEL=.104
def bolt(lift=0,draw=0):
 return {'BoltTravel':dict(loc=(0,-draw,0)),'Bolt':dict(rot_deg=(0,-lift,0))}
def empty_mag():
 return {'TopRound':dict(scale=(0,0,0)),'ReserveRound':dict(scale=(0,0,0)),
         'Follower':dict(loc=(0,0,.018))}
def chamber(visible):return {'ChamberRound':dict(scale=(int(visible),)*3)}
def swap(offset,empty=False):
 keys=[hold(offset),(offset+3,{'MagRelease':dict(rot_deg=(-12,0,0),loc=(0,-.0012,0))}),hold(offset+7),
  (offset+14,{'Magazine':dict(loc=(0,0,-.045))}),
  (offset+28,{'Magazine':dict(loc=(0,-.04,-.19),rot_deg=(12,0,0)),'MagRelease':dict(rot_deg=(0,0,0),loc=(0,0,0))}),
  hold(offset+43),(offset+44,{}),(offset+70,{'Magazine':dict(loc=(0,0,-.09),rot_deg=(0,0,0))}),
  (offset+108,{'Magazine':dict(loc=(0,0,0))})]
 if empty:keys[6]=(offset+44,{'TopRound':dict(scale=(1,1,1)),'ReserveRound':dict(scale=(1,1,1)),
                            'Follower':dict(loc=(0,0,0))})
 return keys
def bipod(deployed=False,extension=0):
 return {**{('Bipod'+s):dict(rot_deg=(-90,0,0) if deployed else (0,0,0)) for s in ('L','R')},
         **{('BipodSplay'+s):dict(rot_deg=(0,0,sign*15) if deployed else (0,0,0)) for s,sign in [('L',1),('R',-1)]},
         **{('BipodExtend'+s):dict(loc=(0,extension,0)) for s in ('L','R')}}
def build_clips(arm):
 action(arm,'Idle',[(0,{}),hold(1)],fps=FPS)
 action(arm,'IdleEmpty',[(0,{**empty_mag(),**chamber(False)}),hold(60)])
 for last in (False,True):
  start=empty_mag() if last else {}
  schedule=[(0,start),(3,{'Trigger':dict(rot_deg=(-12,0,0)),'CockingPiece':dict(loc=(0,.004,0))}),hold(12),
   (18,{'Trigger':dict(rot_deg=(0,0,0))}),hold(25),(42,{**bolt(90), 'CockingPiece':dict(loc=(0,0,0))}),hold(46),
   (64,{**bolt(90,TRAVEL),**chamber(False)}),hold(76),(104,{**bolt(90,0),**chamber(not last)}),hold(108),
   (122,bolt()),hold(132)]
  action(arm,'FireLast' if last else 'Fire',schedule)
 action(arm,'Reload',[(0,{})]+swap(34)+[hold(180)])
 action(arm,'ReloadEmpty',[(0,{**empty_mag(),**chamber(False)}),hold(8),(25,bolt(90)),hold(28),
  (48,bolt(90,TRAVEL))]+swap(72,True)+[hold(195),(219,{**bolt(90),**chamber(True)}),hold(224),(242,bolt()),hold(252)])
 action(arm,'Inspect',[(0,{}),hold(12),(25,{'Safety':dict(rot_deg=(25,0,0))}),hold(44),
  (80,{'PowerRing':dict(rot_deg=(0,55,0)),'Elevation':dict(rot_deg=(0,0,24)),
       'Windage':dict(rot_deg=(18,0,0)),'Parallax':dict(rot_deg=(30,0,0))}),hold(92),
  (100,{'BoltRelease':dict(rot_deg=(5,0,0))}),hold(108),(112,{'BoltRelease':dict(rot_deg=(0,0,0))}),
  (145,{'PowerRing':dict(rot_deg=(0,0,0)),'Elevation':dict(rot_deg=(0,0,0)),
        'Windage':dict(rot_deg=(0,0,0)),'Parallax':dict(rot_deg=(0,0,0))}),hold(158),
  (170,{'Safety':dict(rot_deg=(0,0,0))}),hold(180)])
 action(arm,'BipodDeploy',[(0,{}),hold(8),(42,bipod(True)),hold(48),(72,bipod(True,.0762)),hold(78)])
 action(arm,'BipodFold',[(0,bipod(True,.0762)),hold(8),(32,bipod(True)),hold(40),(72,bipod()),hold(78)])
