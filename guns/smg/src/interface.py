"""Relay 9 binding: 60 Hz visual animation, additive Guns Interface 1.3.0."""
VERSION='1.3.0'
FPS=60
CAPABILITIES=dict(closed_bolt=True,select_fire=True,semi_automatic=True,full_automatic=True,
 detachable_magazine=True,last_round_hold_open=False,manual_handle_lock=True,
 charging_handle_reciprocates=False,magazine_capacity=30,whole_weapon_motion='external only',
 material_binding='retain imported PBR material indices',visual_feed='discrete display ownership',
 charge_state='empty closed to manually locked empty open')
STATES={
 'ready':dict(action='closed',magazine='loaded',chamber=1,handle='forward',selector='semi',trigger='reset'),
 'last_ready':dict(action='closed',magazine='empty',chamber=1,handle='forward',selector='semi',trigger='reset'),
 'empty_closed':dict(action='closed',magazine='empty',chamber=0,handle='forward',selector='semi',trigger='reset'),
 'empty_open':dict(action='open',magazine='empty',chamber=0,handle='locked',selector='semi',trigger='reset'),
 'safe_ready':dict(action='closed',magazine='loaded',chamber=1,handle='forward',selector='safe',trigger='reset'),
 'auto_ready':dict(action='closed',magazine='loaded',chamber=1,handle='forward',selector='auto',trigger='reset'),
 'auto_held':dict(action='closed',magazine='loaded',chamber=1,handle='forward',selector='auto',trigger='held'),
}
def spec(frames,start,end,events=None,required=False,**kw):
 return dict(frames=frames,start=start,end=end,events=events or {},required=required,**kw)
CLIPS={
 'Idle':spec(1,'ready','ready',required=True),
 'Fire':spec(12,'ready','ready',dict(shot=2,eject=4,chamber=7,reset=12),True,alias='FireSemi'),
 'FireSemi':spec(12,'ready','ready',dict(shot=2,eject=4,chamber=7,reset=12),True),
 'FireAuto':spec(5,'auto_held','auto_held',dict(shot=0,eject=2,chamber=5),True),
 'FireLast':spec(12,'last_ready','empty_closed',dict(shot=2,eject=4,closed=7,reset=12),True),
 'Reload':spec(132,'ready','ready',dict(release=14,magazine_out=34,replacement=56,magazine_in=104,catch_engaged=110),True),
 'ReloadEmpty':spec(210,'empty_closed','ready',dict(handle_draw=30,handle_lock=42,release=58,
  magazine_out=78,replacement=100,magazine_in=148,catch_engaged=154,handle_slap=171,handle_release=175,chamber=181),True),
 'Charge':spec(60,'empty_closed','empty_open',dict(handle_draw=30,handle_lock=42),True),
 'Inspect':spec(120,'ready','ready',dict(safe=18,semi=54,partial_open=82,closed=104),True),
 'Selector':spec(20,'safe_ready','auto_ready',dict(safe=0,semi=10,auto=20),True),
 'SelectorSafe':spec(12,'ready','safe_ready',dict(safe=10)),
 'SelectorSemi':spec(12,'safe_ready','ready',dict(semi=10)),
 'SelectorAuto':spec(12,'ready','auto_ready',dict(auto=10)),
 'SelectorAutoSemi':spec(12,'auto_ready','ready',dict(semi=10)),
 'AutoStart':spec(2,'auto_ready','auto_held',dict(trigger_held=2)),
 'AutoStop':spec(6,'auto_held','auto_ready',dict(reset=6)),
 'IdleAuto':spec(1,'auto_held','auto_held'),
 'IdleAutoReady':spec(1,'auto_ready','auto_ready'),
 'IdleSafe':spec(1,'safe_ready','safe_ready'),
 'IdleEmpty':spec(60,'empty_closed','empty_closed'),
 'IdleOpen':spec(60,'empty_open','empty_open'),
}
def event_seconds(clip):return {k:f/FPS for k,f in CLIPS[clip]['events'].items()}
def transition(state,clip):
 s=CLIPS[clip]
 if s['start']!=state:raise ValueError(f'{clip} requires {s["start"]}; got {state}')
 return s['end']
def interrupt(clip,frame):
 if not 0<=frame<=CLIPS[clip]['frames']:raise ValueError('Outside clip')
 return dict(version=VERSION,clip=clip,frame=frame,resume='same clip and frame')
