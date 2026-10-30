"""Authored exterior-animation timings. No mechanically validated action cycle."""
from kit import weapon as W
from interface import CLIPS
from belt import transforms

def vis(v):return dict(scale=(int(v),)*3)
def bolt(rear=True):return {'Bolt':dict(loc=(0,-.080 if rear else 0,0)), 'OperatingRod':dict(loc=(0,-.080 if rear else 0,0))}
def trigger(held=False):return {'Trigger':dict(rot_deg=(-12 if held else 0,0,0))}
def bipod(deployed=False,extend=False):
 out={}
 for s,label in [(-1,'L'),(1,'R')]:
  out['Bipod'+label]=dict(rot_deg=(85,0,0) if deployed else (0,0,0))
  out['BipodSplay'+label]=dict(rot_deg=(0,0,s*18) if deployed else (0,0,0))
  out['BipodExtend'+label]=dict(loc=(0,-.065 if extend else 0,0))
 return out

def build_clips(arm):
 def add(name,keys):
  # Belt absolute transforms at each frame make interpolation inspectable.
  full=[(0,{**bolt(),**transforms(), 'ChamberRound':vis(False),'EjectedCase':vis(False),'EjectedLink':vis(False)})]
  for f,p in keys:
   if f==0:full[0][1].update(p)
   else:full.append((f,p))
  # Unwrap single-axis rotations before export. Euler interpolation across
  # +180/-180 otherwise spins backwards between sampled glTF quaternions.
  last={}
  for f,row in full:
   for bone,p in row.items():
    if 'rot_deg' not in p:continue
    angles=list(p['rot_deg']);old=last.get(bone,angles)
    for k in range(3):angles[k]=old[k]+(angles[k]-old[k]+180)%360-180
    p['rot_deg']=tuple(angles);last[bone]=angles
  W.action(arm,name,full)
 def firing(last=False,burst=False):
  end=24 if burst else 12;events=[3,11,19] if burst else [3];keys=[(0,{**transforms(0,1 if last else 200)})]
  for i,f in enumerate(events):
   keys += [(f-2,trigger(True)),(f,{**bolt(False),'ChamberRound':vis(True)}),
    (f+1,{'ChamberRound':vis(False),f'BeltRound{i:02d}':vis(False)}),(f+2,{**bolt(not last),'EjectedCase':vis(True),'EjectedLink':vis(True),'FeedPawls':dict(loc=(0,0,.0015)),f'BeltLink{i:02d}':vis(False)})]
   for j in range(3,6):
    phase=i+(j-2)/3
    keys.append((f+j,{**transforms(phase,0 if last else 200,consumed=i+1),'FeedPawls':dict(loc=(.003*(1-(j-2)/3),0,.0015 if j<5 else 0)),
      'EjectedCase':dict(loc=(.020*(j-1),-.010*(j-1),-.015*(j-1))), 'EjectedLink':dict(loc=(.018*(j-1),0,-.012*(j-1)))}))
  keys += [(end, {**trigger(),**bolt(not last),'EjectedCase':vis(False),'EjectedLink':vis(False)})]
  # Multiple boundary events may coincide in a burst; explicit merge per frame.
  merged={}
  for f,p in keys:merged.setdefault(f,{}).update(p)
  return sorted(merged.items())
 add('Idle',[(1,{})]);add('IdleEmpty',[(0,{**bolt(False),**transforms(0,0)}),(60,{})])
 add('IdleSafe',[(0,{'Safety':dict(loc=(.005,0,0))}),(1,{})])
 add('Fire',firing());add('FireLast',firing(True));add('Burst',firing(burst=True))
 add('CeaseFire',[(0,{**trigger(True),**bolt(False)}),(6,bolt()),(8,trigger())])
 for empty,name in [(False,'Reload'),(True,'ReloadEmpty')]:
  keys=[(0,{**bolt(not empty),**transforms(0,0 if empty else 200)}),(10,{}),
   (18,{'CoverLatch':dict(loc=(0,0,.006))}),(24,{}),(60,{'FeedCover':dict(rot_deg=(-96,0,0))}),
   (68,{}),(88,transforms(0,0 if empty else 200,lift=55,withdraw=25)),
   (106,transforms(0,0 if empty else 200,lift=55,withdraw=170)),
   (112,{'MagRelease':dict(loc=(0,0,.006))}),(120,{}),
   (140,{'Magazine':dict(loc=(-.015,0,-.21),rot_deg=(8,0,0))}),(171,{}),
   (172,transforms(0,200,lift=55,withdraw=170)),
   (200,{'Magazine':dict(loc=(0,0,-.04),rot_deg=(0,0,0))}),
   (215,{'Magazine':dict(loc=(0,0,0))}),(224,{'MagRelease':dict(loc=(0,0,0))}),
   (238,transforms(0,200,lift=55,withdraw=25)),(264,transforms()),(285,{}),
   (324,{'FeedCover':dict(rot_deg=(0,0,0))}),(332,{}),(340,{'CoverLatch':dict(loc=(0,0,0))})]
  if empty:keys += [(352,{}),(380,{**bolt(),'ChargingHandle':dict(loc=(0,-.080,0))}),(386,{}),(410,{'ChargingHandle':dict(loc=(0,0,0))})]
  keys.append((CLIPS[name]['frames'],{}));add(name,keys)
 add('Charge',[(0,bolt(False)),(6,{}),(30,{**bolt(),'ChargingHandle':dict(loc=(0,-.080,0))}),(36,{}),(60,{'ChargingHandle':dict(loc=(0,0,0))}),(66,{})])
 add('BipodDeploy',[(8,{}),(48,bipod(True)),(54,{}),(78,bipod(True,True)),(84,{})])
 add('BipodFold',[(0,bipod(True,True)),(6,{}),(30,bipod(True)),(38,{}),(78,bipod()),(84,{})])
 for name,on in [('SafetyOn',True),('SafetyOff',False)]:add(name,[(0,{'Safety':dict(loc=(0 if on else .005,0,0))}),(4,{}),(14,{'Safety':dict(loc=(.005 if on else 0,0,0))}),(18,{})])
 for name,raise_it in [('CarryRaise',True),('CarryFold',False)]:
  add(name,[(0,{'CarryHandle':dict(rot_deg=(0,0 if raise_it else -65,0))}),(4,{}),(26,{'CarryHandle':dict(rot_deg=(0,-65 if raise_it else 0,0))}),(30,{})])
 add('BoxOpen',[(0,{**bolt(False),**transforms(0,0)}),(6,{}),(24,{'Magazine':dict(loc=(.15,0,-.2))}),(30,{}),(54,{'BoxLid':dict(rot_deg=(0,100,0))}),(60,{})])
 add('Inspect',[(12,{}),(18,{'Safety':dict(loc=(.005,0,0)),'CoverLatch':dict(loc=(0,0,.006))}),(28,{}),
  (65,{'FeedCover':dict(rot_deg=(-65,0,0)),'ShoulderRest':dict(rot_deg=(65,0,0))}),(106,{}),(142,{'FeedCover':dict(rot_deg=(0,0,0)),'ShoulderRest':dict(rot_deg=(0,0,0))}),
  (154,{'CoverLatch':dict(loc=(0,0,0))}),(164,{}),(172,{'Safety':dict(loc=(0,0,0))}),(180,{})])
 add('BeltEnd',[(0,transforms(0,3)),(4,transforms(0,2,consumed=1)),(10,transforms(1,2,consumed=1)),
  (14,transforms(1,1,consumed=2)),(20,transforms(2,1,consumed=2)),
  (24,{**transforms(2,0,consumed=3),**bolt(False),**trigger(True)}),(30,transforms(3,0,consumed=3)),(42,trigger())])
 assert set(t.name for t in arm.animation_data.nla_tracks)==set(CLIPS)
