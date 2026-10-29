"""R39 visual binding. Additive supplement 1.6.0; 60-Hz clip times."""
VERSION='1.6.0';FPS=60
CAPABILITIES=dict(closed_bolt=True,select_fire=True,semi_automatic=True,
 full_automatic=True,detachable_magazine=True,magazine_rocks_in=True,
 charging_handle_reciprocates=True,last_round_hold_open=False,
 magazine_capacity=30,whole_weapon_motion='external only',
 visual_feed='discrete display ownership',material_binding='retain imported PBR indices')
STATES={}
for n,mode,mag,ch,trig in [('ready','semi','loaded',1,'reset'),
 ('last_ready','semi','empty',1,'reset'),('empty_closed','semi','empty',0,'reset'),
 ('safe_ready','safe','loaded',1,'reset'),('auto_ready','auto','loaded',1,'reset'),
 ('auto_held','auto','loaded',1,'held')]:
 STATES[n]=dict(action='closed',selector=mode,magazine=mag,chamber=ch,trigger=trig)
def spec(f,start,end,events=None,required=False):
 return dict(frames=f,start=start,end=end,events=events or {},required=required)
CLIPS={
 'Idle':spec(1,'ready','ready',required=True),
 'IdleEmpty':spec(60,'empty_closed','empty_closed'),
 'IdleSafe':spec(1,'safe_ready','safe_ready'),
 'IdleAutoReady':spec(1,'auto_ready','auto_ready'),
 'IdleAuto':spec(1,'auto_held','auto_held'),
 'Fire':spec(12,'ready','ready',dict(shot=2,eject=4,chamber=8,reset=12),True),
 'FireSemi':spec(12,'ready','ready',dict(shot=2,eject=4,chamber=8,reset=12),True),
 'FireAuto':spec(6,'auto_held','auto_held',dict(shot=0,eject=2,chamber=6),True),
 'FireLast':spec(12,'last_ready','empty_closed',dict(shot=2,eject=4,closed=8,reset=12),True),
 'Reload':spec(150,'ready','ready',dict(release=16,unhook=40,magazine_out=56,
  replacement=72,front_hook=112,magazine_in=132,catch_engaged=138),True),
 'ReloadEmpty':spec(210,'empty_closed','ready',dict(release=16,unhook=40,
  magazine_out=56,replacement=72,front_hook=112,magazine_in=132,
  catch_engaged=138,handle_draw=174,chamber=188),True),
 'Charge':spec(60,'empty_closed','empty_closed',dict(handle_draw=30,closed=44),True),
 'Inspect':spec(150,'ready','ready',dict(safe=22,semi=65,partial_open=100,closed=125),True),
 'Selector':spec(36,'safe_ready','ready',dict(safe=0,auto=18,semi=36),True),
 'SelectorSafe':spec(12,'ready','safe_ready',dict(safe=10)),
 'SelectorSemi':spec(12,'safe_ready','ready',dict(semi=10)),
 'SelectorAuto':spec(12,'ready','auto_ready',dict(auto=10)),
 'SelectorAutoSemi':spec(12,'auto_ready','ready',dict(semi=10)),
 'AutoStart':spec(2,'auto_ready','auto_held',dict(trigger_held=2)),
 'AutoStop':spec(6,'auto_held','auto_ready',dict(reset=6)),
}
def transition(state,clip):
 s=CLIPS[clip]
 if s['start']!=state:raise ValueError((state,clip))
 return s['end']
def interrupt(clip,frame):
 if not 0<=frame<=CLIPS[clip]['frames']:raise ValueError(frame)
 return dict(version=VERSION,clip=clip,frame=frame,resume='same clip and frame')
