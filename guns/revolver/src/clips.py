"""Complete-pose visual animation schedules with explicit holds and STEP states."""
from kit.weapon import action,hold
from interface import CLIPS,STATES,ORDER
from parameters import OPEN
def vis(v):return dict(scale=(int(v),)*3)
def stop(retracted=True):return {'CylinderStop':dict(rot_deg=(-22 if retracted else 0,0,0))}
def occupancy(chambers):
 return {**{'Live'+str(i):vis(v=='loaded') for i,v in enumerate(chambers)},
         **{'Case'+str(i):vis(v=='fired') for i,v in enumerate(chambers)}}
def rest(name):
 s=STATES[name]
 return {**occupancy(s['chambers']),'Cylinder':dict(rot_deg=(0,s['index']*60,0)),
  'Hammer':dict(rot_deg=(35 if s['hammer']=='cocked' else 0,0,0)),
  'Trigger':dict(rot_deg=(-10 if s['hammer']=='cocked' else 0,0,0)),
  'LoaderBody':vis(False),'LoaderRelease':vis(False),'InsertRound':vis(False),
  **{'LoaderRound'+str(i):vis(False) for i in range(6)}}
def open_pose(v=True):
 return {'Crane':dict(rot_deg=(0,OPEN if v else 0,0)),
  **stop()}
def latch(v=True):
 return {'Latch':dict(loc=(0,.002 if v else 0,0)),
         'LatchPin':dict(loc=(0,-.0025 if v else 0,0))}
def firing(n,dry=False):
 start='empty' if dry else 'ready' if n==1 else 'after'+str(n-1)
 change={} if dry else {'Live'+str(ORDER[n-1]):vis(False),'Case'+str(ORDER[n-1]):vis(True)}
 return [(0,rest(start)),hold(2),(5,{**stop(),
  'Trigger':dict(rot_deg=(-4,0,0))}),
  (21,{'Cylinder':dict(rot_deg=(0,n*60,0)),'Hammer':dict(rot_deg=(35,0,0)),
       'Trigger':dict(rot_deg=(-20,0,0))}),
  (24,stop(False)),hold(25),
  (27,{'Hammer':dict(rot_deg=(0,0,0)),**change}),hold(31),
  (38,{'Trigger':dict(rot_deg=(0,0,0))}),hold(42)]
def build_clips(arm):
 for clip,s in CLIPS.items():
  if clip.startswith('Idle'):action(arm,clip,[(0,rest(s['start'])),hold(s['frames'])])
 for n in range(1,7):action(arm,'Fire' if n==1 else 'FireLast' if n==6 else 'Fire'+str(n),firing(n))
 action(arm,'DryFire',firing(1,True))
 action(arm,'CockHammer',[(0,rest('ready')),hold(2),
  (5,stop()),
  (29,{'Cylinder':dict(rot_deg=(0,60,0)),'Hammer':dict(rot_deg=(35,0,0)),
       'Trigger':dict(rot_deg=(-10,0,0))}),
  (32,stop(False)),hold(36),hold(42)])
 action(arm,'FireSingle',[(0,rest('cocked')),hold(1),
  (3,{'Trigger':dict(rot_deg=(-15,0,0))}),
  (4,{'Hammer':dict(rot_deg=(0,0,0)),'Live1':vis(False),'Case1':vis(True)}),
  hold(12),(20,{'Trigger':dict(rot_deg=(0,0,0))}),hold(24)])
 begin=lambda state:[(0,rest(state)),hold(4),(12,{**latch(),**stop()}),hold(16),(40,open_pose())]
 keys=begin('after6')+[hold(48),
  (58,{'Extractor':dict(loc=(0,-.026,0)),
       **{'Case'+str(i):dict(loc=(0,-.026,0)) for i in range(6)}}),hold(59),
  (60,{}),(64,{**{'Case'+str(i):dict(loc=(0,-.062,0)) for i in range(6)}}),
  (78,{**{'Case'+str(i):dict(loc=(-.045,-.09,.040)) for i in range(6)}}),
  (80,{**{'Case'+str(i):vis(False) for i in range(6)}}),
  (88,{'Extractor':dict(loc=(0,0,0))}),hold(100),
  (104,{'LoaderGuide':dict(loc=(0,-.075,0)),'LoaderBody':vis(True),'LoaderRelease':vis(True),
        **{'LoaderRound'+str(i):vis(True) for i in range(6)}}),
  (142,{'LoaderGuide':dict(loc=(0,0,0))}),hold(143),
  (144,{**occupancy(['loaded']*6),'LoaderRelease':dict(loc=(0,.002,0)),**{'LoaderRound'+str(i):vis(False) for i in range(6)}}),
  (150,{'LoaderRelease':dict(loc=(0,0,0))}),
  (172,{'LoaderGuide':dict(loc=(0,-.085,0))}),
  (174,{'LoaderBody':vis(False),'LoaderRelease':vis(False)}),hold(180),(200,open_pose(False)),
  (204,stop(False)),(208,latch(False)),hold(216)]
 action(arm,'Reload',keys)
 keys=begin('one_empty')+[hold(72),
  (76,{'InsertRound':vis(True),'RoundGuide':dict(loc=(0,-.065,0))}),
  (116,{'RoundGuide':dict(loc=(0,0,0))}),hold(117),
  (118,{'InsertRound':vis(False),'Live0':vis(True)}),hold(140),
  (164,open_pose(False)),(168,stop(False)),(172,latch(False)),hold(180)]
 action(arm,'ReloadSingle',keys)
 action(arm,'Inspect',begin('ready')+[hold(100),(128,open_pose(False)),(132,stop(False)),(136,latch(False)),hold(144)])
 assert {t.name for t in arm.animation_data.nla_tracks}==set(CLIPS)
