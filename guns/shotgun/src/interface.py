"""Guns Interface 1.1 additive tube-magazine binding; 60-Hz visual clips."""
VERSION='1.1.0';FPS=60
CAPABILITIES=dict(pump_action=True,tube_magazine=True,shell_by_shell_loading=True,
 detachable_magazine=False,last_round_hold_open=False,tube_capacity=4,
 support_hand_socket='Socket_SupportHand',whole_weapon_motion='external only',
 material_binding='retain imported PBR materials',visual_feed='discrete chamber/occluded tube slot handoff')
STATES={'ready':dict(action='closed',magazine='loaded',tube=4,chamber=1),
 'last_ready':dict(action='closed',magazine='empty',tube=0,chamber=1),
 'empty_closed':dict(action='closed',magazine='empty',tube=0,chamber=0),
 'empty_open':dict(action='open',magazine='empty',tube=0,chamber=0)}
for i in (1,2,3):STATES['ready'+str(i)]=dict(action='closed',magazine='loaded',tube=i,chamber=1)
def state(n):return 'ready' if n==4 else ('last_ready' if n==0 else 'ready'+str(n))
def spec(frames,start,end,events=None,required=False,**kw):
 return dict(frames=frames,start=start,end=end,events=events or {},required=required,**kw)
CLIPS={
 'Idle':spec(1,'ready','ready',required=True),
 'Fire':spec(66,'ready','ready3',dict(shot=2,unlock=10,eject=24,shell_release=30,carrier_up=40,chamber=44,lock=60,reset=66),True),
 'FireLast':spec(66,'last_ready','empty_closed',dict(shot=2,unlock=10,eject=24,lock=60,reset=66),True),
 'Reload':spec(72,'ready3','ready',dict(insertion_begin=12,tube_entry=44,shell_commit=60,interrupt_safe=66),True,
  interruptible=[dict(begin=66,end=72,state='ready')]),
 'ReloadEmpty':spec(378,'empty_closed','ready',dict(unlock=8,open=26,carrier_load=36,carrier_up=44,chamber=50,lock=70,
  chamber_ready=78,shell_commit_1=144,shell_commit_2=216,shell_commit_3=288,shell_commit_4=360),True,
  interruptible=[dict(begin=78,end=84,state='last_ready'),dict(begin=150,end=156,state='ready1'),
   dict(begin=222,end=228,state='ready2'),dict(begin=294,end=300,state='ready3'),dict(begin=366,end=378,state='ready')]),
 'Inspect':spec(150,'ready','ready',dict(safe=18,unsafe=48,release=78,partial_open=106,closed=132)),
 'IdleEmpty':spec(60,'empty_closed','empty_closed'),
 'IdleOpen':spec(60,'empty_open','empty_open'),
}
for n in (0,1,2,3):CLIPS['IdleTube'+str(n)]=spec(60,state(n),state(n))
for n in (1,2,3):
 CLIPS['Fire'+str(n)]=spec(66,state(n),state(n-1),dict(CLIPS['Fire']['events']))
 CLIPS['Reload'+str(n)]=spec(72,state(n-1),state(n),dict(CLIPS['Reload']['events']),
  interruptible=[dict(begin=66,end=72,state=state(n))])

def event_seconds(clip):return {k:v/FPS for k,v in CLIPS[clip]['events'].items()}
def transition(current,clip):
 s=CLIPS[clip]
 if current!=s['start']:raise ValueError(f'{clip} requires {s["start"]}; got {current}')
 return s['end']
def interrupt(clip,frame):
 s=CLIPS[clip]
 if not 0<=frame<=s['frames']:raise ValueError('Outside clip')
 phase=next((p for p in s.get('interruptible',[]) if p['begin']<=frame<=p['end']),None)
 return dict(version=VERSION,clip=clip,frame=frame,
  resume='same clip and frame',exit_state=phase['state'] if phase else None,
  exit_clip=('Idle' if phase and phase['state']=='ready' else
   'IdleTube'+str(STATES[phase['state']]['tube']) if phase else None))
