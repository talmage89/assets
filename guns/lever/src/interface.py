"""Guns 1.0 binding + additive 1.5 lever/top-ejection capabilities, 60 Hz."""
VERSION='1.0.0'
SUPPLEMENT_VERSION='1.5.0'
FPS=60
CAPABILITIES=dict(lever_action=True,manual_action=True,tube_magazine=True,
    shell_by_shell_loading=True,side_loading_gate=True,exposed_hammer=True,
    top_ejection=True,tube_capacity=6,detachable_magazine=False,
    last_round_hold_open=False,hammer_safe_position='half_cock',
    support_hand_socket='Socket_SupportHand',lever_hand_socket='Socket_LeverHand',
    whole_weapon_motion='external only',material_binding='retain imported PBR materials',
    visual_feed='continuous tube/carrier/bolt path; coincident ownership and tube-slot indexing',
    visible_cartridge_feed=True,feed_type='tube_carrier',case_handoff_bone='FiredGuide',
    case_anchor_blender_m=(0,.200,.048),case_demo_hide_frame=30)


def ready(n):return 'ready' if n==6 else ('last_ready' if n==0 else 'ready'+str(n))
def spent(n):return 'spent'+str(n)
STATES={}
for n in range(7):
    STATES[ready(n)]=dict(action='closed',tube=n,chamber=1,case=0,hammer='cocked')
    STATES[spent(n)]=dict(action='closed',tube=n,chamber=0,case=1,hammer='fired')
STATES.update(empty_closed=dict(action='closed',tube=0,chamber=0,case=0,hammer='cocked'),
              empty_open=dict(action='open',tube=0,chamber=0,case=0,hammer='cocked'),
              empty_tube1=dict(action='closed',tube=1,chamber=0,case=0,hammer='cocked'),
              half_cock=dict(action='closed',tube=6,chamber=1,case=0,hammer='half_cock'))


def spec(frames,start,end,events=None,required=False,**extra):
    return dict(frames=frames,start=start,end=end,events=events or {},required=required,**extra)


CLIPS={
 'Idle':spec(1,'ready','ready',required=True),
 'Fire':spec(18,'ready','spent6',dict(shot=3,reset=15),True),
 'FireLast':spec(18,'last_ready','spent0',dict(shot=3,reset=15),True),
 'Cycle':spec(60,'spent6','ready5',dict(unlock=6,open=22,eject=24,shell_release=28,carrier_up=36,chamber=50,lock=58),True),
 'CycleLast':spec(60,'spent0','empty_closed',dict(unlock=6,open=22,eject=24,lock=58),True),
 'CycleEmpty':spec(60,'empty_closed','empty_closed',dict(unlock=6,open=22,lock=58)),
 'Reload':spec(72,'ready5','ready',dict(insertion_begin=12,tube_entry=42,shell_commit=58,interrupt_safe=66),True,
               interruptible=[dict(begin=66,end=72,state='ready')]),
 'ReloadSeveral':spec(216,'ready3','ready',dict(shell_commit_1=58,shell_commit_2=130,shell_commit_3=202),True,
               interruptible=[dict(begin=66,end=72,state='ready4'),dict(begin=138,end=144,state='ready5'),dict(begin=210,end=216,state='ready')]),
 'HammerSafe':spec(48,'ready','half_cock',dict(thumb_control=10,sear_release=14,half_cock=42),True),
 'HammerCock':spec(30,'half_cock','ready',dict(full_cock=24),True),
 'Inspect':spec(120,'ready','ready',dict(hammer_touch=36,reset=100)),
 'IdleEmpty':spec(60,'empty_closed','empty_closed'),
 'IdleOpen':spec(60,'empty_open','empty_open'),
 'IdleUnchambered1':spec(60,'empty_tube1','empty_tube1'),
 'Chamber':spec(60,'empty_tube1','last_ready',dict(unlock=6,open=22,shell_release=28,carrier_up=36,chamber=50,lock=58)),
 'ReloadEmpty':spec(564,'empty_closed','ready',dict(first_commit=58,unlock=78,chamber=122,
               shell_commit_1=190,shell_commit_2=262,shell_commit_3=334,shell_commit_4=406,shell_commit_5=478,shell_commit_6=550),True,
               interruptible=[dict(begin=66,end=72,state='empty_tube1'),dict(begin=130,end=132,state='last_ready'),
                 *[dict(begin=198+72*i,end=204+72*i,state=ready(i+1)) for i in range(6)]]),
}
for n in range(6):CLIPS['IdleTube'+str(n)]=spec(60,ready(n),ready(n))
for n in range(1,6):
    CLIPS['Fire'+str(n)]=spec(18,ready(n),spent(n),dict(CLIPS['Fire']['events']))
    CLIPS['Cycle'+str(n)]=spec(60,spent(n),ready(n-1),dict(CLIPS['Cycle']['events']))
for n in range(5):
    CLIPS['Reload'+str(n+1)]=spec(72,ready(n),ready(n+1),dict(CLIPS['Reload']['events']),
            interruptible=[dict(begin=66,end=72,state=ready(n+1))])


def transition(current,clip):
    s=CLIPS[clip]
    if current!=s['start']:raise ValueError((current,clip,s['start']))
    return s['end']


def interrupt(clip,frame):
    s=CLIPS[clip]
    if not 0<=frame<=s['frames']:raise ValueError('Outside clip')
    phase=next((p for p in s.get('interruptible',[]) if p['begin']<=frame<=p['end']),None)
    state=phase['state'] if phase else None
    idle=('IdleUnchambered1' if state=='empty_tube1' else 'Idle' if state=='ready' else
          'IdleTube'+str(STATES[state]['tube'])) if state else None
    return dict(version=SUPPLEMENT_VERSION,clip=clip,frame=frame,resume='same clip and frame',exit_state=state,exit_clip=idle)
