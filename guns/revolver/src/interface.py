"""Additive Guns 1.4.0 visual revolver binding. Stable physical chamber IDs.

All timing is authored animation, not functional mechanical simulation.
"""
import copy
VERSION='1.4.0'
FPS=60
CAPABILITIES=dict(revolver=True,detachable_magazine=False,magazine=False,
 cylinder_capacity=6,double_action=True,single_action=True,swing_out_cylinder=True,
 manual_reload=True,speedloader=True,last_round_hold_open=False,
 chamber_states=('loaded','fired','empty'),whole_weapon_motion='external only',
 material_binding='retain imported PBR materials')
def state(chambers,index=0,action='closed',hammer='rest'):
 return dict(chambers=list(chambers),index=index,action=action,hammer=hammer,magazine='none')
STATES={'ready':state(['loaded']*6),'empty':state(['empty']*6),
 'dry_indexed':state(['empty']*6,1),
 'one_empty':state(['empty']+['loaded']*5),
 'cocked':state(['loaded']*6,1,hammer='cocked')}
ORDER=(1,2,3,4,5,0)
for n in range(1,7):
 chambers=['loaded']*6
 for i in ORDER[:n]:chambers[i]='fired'
 STATES['after'+str(n)]=state(chambers,n)
def spec(frames,start,end,events=None,required=False):
 return dict(frames=frames,start=start,end=end,events=events or {},required=required)
CLIPS={'Idle':spec(1,'ready','ready',required=True),
 'CockHammer':spec(42,'ready','cocked',dict(index=29,stop_seated=32,cocked=36)),
 'FireSingle':spec(24,'cocked','after1',dict(shot=4,reset=20)),
 'DryFire':spec(42,'empty','dry_indexed',dict(index=21,stop_seated=24,hammer_fall=27,reset=38)),
 'Reload':spec(216,'after6','ready',dict(latch_release=12,open=40,eject_stroke=58,cases_release=60,
  cases_clear=80,star_return=88,loader_enter=104,rounds_seated=142,loader_release=144,
  loader_clear=172,close=200,latch_engaged=208),True),
 'ReloadSingle':spec(180,'one_empty','ready',dict(latch_release=12,open=40,
  round_enter=76,round_seated=116,round_commit=118,hand_clear=140,close=164,latch_engaged=172),True),
 'Inspect':spec(144,'ready','ready',dict(latch_release=12,open=40,close=128,latch_engaged=136)),
 'IdleEmpty':spec(1,'empty','empty'),
 'IdleDryIndexed':spec(1,'dry_indexed','dry_indexed'),
 'IdleCocked':spec(1,'cocked','cocked')}
for n in range(1,7):
 name='Fire' if n==1 else 'FireLast' if n==6 else 'Fire'+str(n)
 CLIPS[name]=spec(42,'ready' if n==1 else 'after'+str(n-1),'after'+str(n),
  dict(index=21,stop_seated=24,shot=27,reset=38),n in (1,6))
 CLIPS['IdleAfter'+str(n)]=spec(1,'after'+str(n),'after'+str(n))
def snapshot(clip,frame):
 s=CLIPS[clip]
 if not 0<=frame<=s['frames']:raise ValueError('Outside clip')
 r=copy.deepcopy(STATES[s['start']]);e=s['events']
 if clip.startswith('Fire') and clip!='FireSingle':
  n=6 if clip=='FireLast' else 1 if clip=='Fire' else int(clip[4:])
  if frame>=e['index']:r['index']=n
  if frame>=e['shot']:r['chambers'][ORDER[n-1]]='fired'
 elif clip=='FireSingle':
  if frame>=4:r['chambers'][1]='fired';r['hammer']='rest'
 elif clip=='DryFire':
  if frame>=21:r['index']=1
 elif clip=='CockHammer':
  if frame>=29:r['index']=1
  if frame>=36:r['hammer']='cocked'
 elif clip in ('Reload','ReloadSingle','Inspect'):
  r['action']='closed' if frame<12 or frame>=e['latch_engaged'] else 'moving'
  if 40<=frame<e['close']:r['action']='open'
  if clip=='Reload':
   if frame>=60:r['chambers']=['empty']*6
   if frame>=144:r['chambers']=['loaded']*6
   if frame>=88:r['index']=0
  elif clip=='ReloadSingle' and frame>=118:r['chambers'][0]='loaded'
 if frame==s['frames']:r=copy.deepcopy(STATES[s['end']])
 return r
def interrupt(clip,frame):
 return dict(version=VERSION,clip=clip,frame=frame,state=snapshot(clip,frame),resume='same clip and frame; hold pose')
def transition(current,clip):
 if current!=CLIPS[clip]['start']:raise ValueError('Wrong start state')
 return CLIPS[clip]['end']
