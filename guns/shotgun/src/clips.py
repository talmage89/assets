"""Authored visual timing, explicit holds, STEP occupancy, no Root movement.

Feeding uses a discrete chamber handoff, as in the pistol. Occluded tube slots
are reindexed at count events. No claim of continuous internal ammunition paths.
"""
from kit.weapon import action as kit_action,hold,fcurves
from interface import FPS,CLIPS
STROKE=.096
def action(arm,name,keys,**kw):
 # Keep the shell spawn frame nonsingular while its display mesh is hidden.
 # This separates a hand-held frame from STEP mesh occupancy, additively.
 normalized=[]
 for f,over in keys:
  over={b:dict(v) for b,v in over.items()}
  if 'InsertShell' in over:
   d=over['InsertShell'];movement={k:d.pop(k) for k in ('loc','rot_deg') if k in d}
   if movement:over['ShellGuide']=movement
  normalized.append((f,over))
 return kit_action(arm,name,normalized,**kw)
def vis(v):return dict(scale=(int(v),)*3)
def tube(n,hide=False):
 return {**{'Tube'+str(i):vis(i<=n and not hide) for i in range(1,5)},
         'Follower':dict(loc=(0,(n-4)*.059,0))}
def rest(n=4,chamber=True):
 return {**tube(n),'ChamberShell':vis(chamber),'CarrierShell':vis(False),'InsertShell':vis(False)}
def pump(d):return {'Forend':dict(loc=(0,-d,0)),'Bolt':dict(loc=(0,-d,0))}
def unlock(v=True):return {'BoltLock':dict(rot_deg=(-9 if v else 0,0,0))}
def carrier(v,angle=15):return {'Carrier':dict(rot_deg=(angle if v else 0,0,0))}
def fire_keys(n,last=False):
 keys=[(0,rest(n)),hold(1),(2,{'Trigger':dict(rot_deg=(-12,0,0))}),hold(8),
  (10,unlock()),(14,{'Trigger':dict(rot_deg=(0,0,0)),**pump(.027)}),
  (24,pump(.080)),(26,pump(STROKE)),hold(29)]
 # The fired chamber representation disappears at the ejection event. A game
 # spawns the separate fired hull from Ejection, not the loaded-shell mesh.
 keys[6]=(24,{**pump(.080),'ChamberShell':vis(False)})
 if not last:
  keys += [(30,{**tube(n-1),'CarrierShell':vis(True),
   'ShellStopL':dict(loc=(-.002,0,0)),'ShellStopR':dict(loc=(.002,0,0))}),
   (34,{'ShellStopL':dict(loc=(0,0,0)),'ShellStopR':dict(loc=(0,0,0))}),
   (40,carrier(True)),hold(43),
   (44,{'CarrierShell':vis(False),'ChamberShell':vis(True)})]
 else:keys += [hold(44)]
 keys += [(58,{**pump(0),**carrier(False)}),(60,unlock(False)),hold(66)]
 return keys
def insertion(n,offset=0):
 # Loading pushes the carrier above the underside opening. The visible shell
 # passes through that opening, nose first. Slot reindexing is hidden by steel.
 def k(f,p):return f+offset,p
 return [k(0,rest(n)),k(8,carrier(True,20)),k(11,{}),
  k(12,{'InsertShell':{**vis(True),'loc':(0,-.065,-.065),'rot_deg':(20,0,0)}}),
  k(28,{'InsertShell':dict(loc=(0,-.035,0),rot_deg=(0,0,0))}),
  k(40,{'Follower':dict(loc=(0,(n-4)*.059,0))}),
  k(44,{'InsertShell':dict(loc=(0,.015,0),rot_deg=(0,0,0)),
   'ShellStopL':dict(loc=(-.002,0,0)),'ShellStopR':dict(loc=(.002,0,0)),
   **{'Tube'+str(i):vis(False) for i in range(1,5)},'Follower':dict(loc=(0,(n-4)*.059+.006,0))}),
  k(59,{'InsertShell':dict(loc=(0,.069,0),rot_deg=(0,0,0)),'Follower':dict(loc=(0,(n-3)*.059,0))}),
  k(60,{'InsertShell':vis(False),**tube(n+1)}),
  k(62,{'ShellStopL':dict(loc=(0,0,0)),'ShellStopR':dict(loc=(0,0,0))}),k(66,carrier(False)),k(72,{})]
def build_clips(arm):
 action(arm,'Idle',[(0,rest()),hold(1)])
 action(arm,'Fire',fire_keys(4))
 action(arm,'FireLast',fire_keys(0,True))
 action(arm,'Reload',insertion(3))
 # Empty loading is a visible carrier presentation followed by four insertions.
 keys=[(0,rest(0,False)),hold(5),(8,{**unlock(),'ActionRelease':dict(rot_deg=(9,0,0))}),(26,pump(STROKE)),
  (32,{'ActionRelease':dict(rot_deg=(0,0,0))}),hold(35),
  (36,{'CarrierShell':vis(True)}),(44,carrier(True)),hold(49),
  (50,{'CarrierShell':vis(False),'ChamberShell':vis(True)}),
  (68,{**pump(0),**carrier(False)}),(70,unlock(False)),hold(84)]
 for n in range(4):
  seq=insertion(n,84+72*n)
  # Avoid a duplicate boundary; full-pose helper carries previous closed pose.
  keys += seq[1:]
 keys += [hold(378)]
 action(arm,'ReloadEmpty',keys)
 action(arm,'Inspect',[(0,rest()),hold(10),(18,{'Safety':dict(loc=(.003,0,0))}),hold(38),
  (48,{'Safety':dict(loc=(0,0,0))}),hold(64),(78,{'ActionRelease':dict(rot_deg=(9,0,0))}),
  hold(88),(96,unlock()),(106,pump(.005)),hold(116),(128,pump(0)),
  (132,{**unlock(False),'ActionRelease':dict(rot_deg=(0,0,0))}),hold(150)])
 action(arm,'IdleEmpty',[(0,rest(0,False)),hold(60)])
 action(arm,'IdleOpen',[(0,{**rest(0,False),**pump(STROKE),**unlock()}),hold(60)])
 for n in (0,1,2,3):action(arm,'IdleTube'+str(n),[(0,rest(n)),hold(60)])
 for n in (1,2,3):
  action(arm,'Fire'+str(n),fire_keys(n))
  action(arm,'Reload'+str(n),insertion(n-1))
 # Occluded tube-slot reindexing is a discrete count change, including follower.
 # A half-frame interpolated jump would run the follower through the old shell.
 for act in [a for a in __import__('bpy').data.actions if a.name.startswith('Fire')]:
  for fc in fcurves(act):
   if fc.data_path=='pose.bones["Follower"].location':
    for key in fc.keyframe_points:key.interpolation='CONSTANT'
 assert set(a.name for a in arm.animation_data.nla_tracks)==set(CLIPS)
