"""Guns 1.7.0 visual break action. Physical chamber IDs: right=0, left=1."""
import copy
VERSION='1.7.0';FPS=60
CAPABILITIES=dict(break_action=True,barrel_count=2,double_triggers=True,
 automatic_safety=True,extractors=True,ejectors=False,magazine=False,
 detachable_magazine=False,last_round_hold_open=False,
 chamber_states=('loaded','fired','empty'),hammer_state_only=True,
 whole_weapon_motion='external only',material_binding='retain imported PBR materials')
def state(chambers=('loaded','loaded'),*,action='closed',safety='fire',hammers=('cocked','cocked')):
 return dict(chambers=list(chambers),action=action,safety=safety,hammers=list(hammers),magazine='none')
STATES={'ready':state(),'after_right':state(('fired','loaded'),hammers=('rest','cocked')),
 'spent':state(('fired','fired'),hammers=('rest','rest')),
 'loaded_safe':state(safety='safe'),
 'open_spent':state(('fired','fired'),action='open',safety='safe'),
 'open_empty':state(('empty','empty'),action='open',safety='safe'),
 'open_one':state(('empty','loaded'),action='open',safety='safe'),
 'open_loaded':state(action='open',safety='safe')}
def spec(frames,start,end,**events):return dict(frames=frames,start=start,end=end,events=events)
CLIPS={'Idle':spec(1,'ready','ready'),
 'Fire':spec(30,'ready','after_right',shot=5,reset=22),
 'FireLeft':spec(30,'after_right','spent',shot=5,reset=22),
 'Open':spec(72,'spent','open_spent',lever_right=12,unlocked=12,safe=20,cocked=48,open=56,extractor_raised=64),
 'OpenLoaded':spec(72,'ready','open_loaded',lever_right=12,unlocked=12,safe=20,cocked=48,open=56,extractor_raised=64),
 'Unload':spec(96,'open_spent','open_empty',hand_grasp=12,hulls_clear=50,hulls_release=68,hand_clear=88),
 'Reload':spec(144,'open_empty','open_loaded',right_enter=12,right_seated=44,right_commit=46,right_hand_clear=64,
  left_enter=76,left_seated=108,left_commit=110,left_hand_clear=132),
 'ReloadSingle':spec(84,'open_one','open_loaded',right_enter=12,right_seated=44,right_commit=46,right_hand_clear=72),
 'Close':spec(72,'open_loaded','loaded_safe',extractor_home=20,closed=56,lever_home=64,locked=64),
 'Safety':spec(30,'loaded_safe','ready',fire_detent=20),
 'SafetyOn':spec(30,'ready','loaded_safe',safe_detent=20),
 'Inspect':spec(180,'ready','loaded_safe',lever_right=12,unlocked=12,safe=20,cocked=48,open=56,
  extractor_raised=64,extractor_home=132,closed=164,lever_home=172,locked=172)}
for clip,s in [('IdleAfterRight','after_right'),('IdleSpent','spent'),('IdleSafe','loaded_safe'),
 ('IdleOpenSpent','open_spent'),('IdleOpenEmpty','open_empty'),('IdleOpenOne','open_one'),('IdleOpenLoaded','open_loaded')]:
 CLIPS[clip]=spec(1,s,s)
def snapshot(clip,frame):
 s=CLIPS[clip]
 if not 0<=frame<=s['frames']:raise ValueError('Outside clip')
 r=copy.deepcopy(STATES[s['start']]);e=s['events']
 if clip in ('Fire','FireLeft') and frame>=e['shot']:
  i=0 if clip=='Fire' else 1;r['chambers'][i]='fired';r['hammers'][i]='rest'
 if clip in ('Open','OpenLoaded','Inspect'):
  if frame>=12:r['action']='moving'
  if frame>=20:r['safety']='safe'
  if frame>=48:r['hammers']=['cocked','cocked']
  if frame>=56:r['action']='open'
  if clip=='Inspect' and frame>=112:r['action']='moving'
  if clip=='Inspect' and frame>=172:r['action']='closed'
 if clip=='Unload' and frame>=68:r['chambers']=['empty','empty']
 if clip in ('Reload','ReloadSingle'):
  if frame>=46:r['chambers'][0]='loaded'
  if clip=='Reload' and frame>=110:r['chambers'][1]='loaded'
 if clip=='Close':
  if frame>4:r['action']='moving'
  if frame>=64:r['action']='closed'
 if clip in ('Safety','SafetyOn') and frame>=20:r['safety']='fire' if clip=='Safety' else 'safe'
 if frame==s['frames']:r=copy.deepcopy(STATES[s['end']])
 return r
def interrupt(clip,frame):
 return dict(version=VERSION,clip=clip,frame=frame,state=snapshot(clip,frame),resume='same clip and frame; hold pose')
def transition(current,clip):
 if current!=CLIPS[clip]['start']:raise ValueError('Wrong start state')
 return CLIPS[clip]['end']
