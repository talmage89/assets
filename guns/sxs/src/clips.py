"""Complete rigid animation; no firearm lockwork simulation or internal hammers."""
from kit.weapon import action,hold
from interface import CLIPS,STATES
from parameters import OPEN,LIFT
def vis(value):return dict(scale=(int(value),)*3)
def rest(name):
 s=STATES[name];opened=s['action']=='open'
 return {'Barrels':dict(rot_deg=(OPEN if opened else 0,0,0)),
  'TopLever':dict(rot_deg=(0,0,25 if opened else 0)),
  'LockBolt':dict(loc=(0,-.024 if opened else 0,0)),
  'Safety':dict(loc=(0,-.005 if s['safety']=='safe' else 0,0)),
  'Extractor':dict(loc=(0,LIFT*.001 if opened else 0,0)),
  **{name+side:vis(s['chambers'][i]==which) for i,side in enumerate(('R','L')) for name,which in [('Live','loaded'),('Hull','fired')]},
  'InsertR':vis(False),'InsertL':vis(False)}
def opening(state):
 return [(0,rest(state)),hold(4),(12,{'TopLever':dict(rot_deg=(0,0,25)),'LockBolt':dict(loc=(0,-.024,0))}),
  hold(16),(20,{'Safety':dict(loc=(0,-.005,0)),'Barrels':dict(rot_deg=(-4,0,0))}),
  (48,{'Barrels':dict(rot_deg=(-35,0,0))}),
  (56,{'Barrels':dict(rot_deg=(OPEN,0,0)),'Extractor':dict(loc=(0,-.006,0))}),
  (64,{'Extractor':dict(loc=(0,LIFT*.001,0))})]
def closing(start):
 return [hold(start),(start+16,{'Extractor':dict(loc=(0,0,0))}),
  (start+52,{'Barrels':dict(rot_deg=(0,0,0))}),
  (start+60,{'TopLever':dict(rot_deg=(0,0,0)),'LockBolt':dict(loc=(0,0,0))})]
def insert(side,start):
 return [(start,{'Insert'+side:vis(True),'InsertGuide'+side:dict(loc=(0,-.105,0))}),
  (start+32,{'InsertGuide'+side:dict(loc=(0,0,0))}),hold(start+33),
  (start+34,{'Insert'+side:vis(False),'Live'+side:vis(True)}),hold(start+52)]
def build_clips(arm):
 for name,s in CLIPS.items():
  if name.startswith('Idle'):action(arm,name,[(0,rest(s['start'])),hold(s['frames'])])
 for name,side,bone in [('Fire','R','Trigger'),('FireLeft','L','TriggerRear')]:
  action(arm,name,[(0,rest(CLIPS[name]['start'])),hold(1),
   (5,{bone:dict(rot_deg=(-13,0,0)),'Live'+side:vis(False),'Hull'+side:vis(True)}),hold(12),
   (22,{bone:dict(rot_deg=(0,0,0))}),hold(30)])
 for name,state in [('Open','spent'),('OpenLoaded','ready')]:action(arm,name,opening(state)+[hold(72)])
 action(arm,'Unload',[(0,rest('open_spent')),hold(12),
  (50,{**{'Hull'+s:dict(loc=(0,-.083,0)) for s in ('R','L')}}),
  (66,{**{'Hull'+s:dict(loc=(.035,-.12,.035)) for s in ('R','L')}}),
  (68,{'HullR':vis(False),'HullL':vis(False)}),hold(96)])
 action(arm,'Reload',[(0,rest('open_empty')),hold(10)]+insert('R',12)+[hold(74)]+insert('L',76)+[hold(144)])
 action(arm,'ReloadSingle',[(0,rest('open_one')),hold(10)]+insert('R',12)+[hold(84)])
 action(arm,'Close',[(0,rest('open_loaded'))]+closing(4)+[hold(72)])
 for name,target in [('Safety','fire'),('SafetyOn','safe')]:
  action(arm,name,[(0,rest(CLIPS[name]['start'])),hold(4),
   (20,{'Safety':dict(loc=(0,-.005 if target=='safe' else 0,0))}),hold(30)])
 action(arm,'Inspect',opening('ready')+[hold(108)]+closing(112)+[hold(180)])
 assert {t.name for t in arm.animation_data.nla_tracks}==set(CLIPS)
