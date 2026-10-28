"""PD C9 implementation of Guns Interface 1.0.0. Times are integer 60-Hz frames."""
VERSION='1.0.0'
FPS=60
STATES={
 'ready':dict(action='closed',magazine='loaded',chamber=1),
 'last_ready':dict(action='closed',magazine='empty',chamber=1),
 'empty_open':dict(action='open',magazine='empty',chamber=0),
 'empty_closed':dict(action='closed',magazine='empty',chamber=0),
 'live_mag_out':dict(action='closed',magazine='absent',chamber=1),
 'cycling':dict(action='moving',magazine='loaded',chamber=0),
 'last_cycling':dict(action='moving',magazine='empty',chamber=0),
 'empty_reloaded_open':dict(action='open',magazine='loaded',chamber=0),
 'empty_mag_out':dict(action='open',magazine='absent',chamber=0),
}
CLIPS={
 'Idle':dict(required=True,frames=1,start='ready',end='ready',events={}),
 'Fire':dict(required=True,frames=12,start='ready',end='ready',events={'shot':2,'eject':4,'chamber':8,'reset':12}),
 'FireSemi':dict(required=False,alias='Fire',frames=12,start='ready',end='ready',events={'shot':2,'eject':4,'chamber':8,'reset':12}),
 'FireLast':dict(required=True,frames=15,start='last_ready',end='empty_open',events={'shot':2,'eject':4,'lock':7,'reset':12}),
 'Reload':dict(required=True,frames=120,start='ready',end='ready',events={'magazine_out':28,'magazine_in':91}),
 'ReloadEmpty':dict(required=True,frames=144,start='empty_open',end='ready',events={'magazine_out':28,'magazine_in':91,'slide_release':112,'chamber':118}),
 'Inspect':dict(required=False,frames=90,start='ready',end='ready',events={'press_check_open':30,'press_check_closed':65}),
 'Charge':dict(required=False,frames=36,start='empty_closed',end='empty_open',events={'lock':30}),
 'IdleOpen':dict(required=False,frames=60,start='empty_open',end='empty_open',events={}),
 'IdleEmpty':dict(required=False,frames=60,start='empty_closed',end='empty_closed',events={}),
}
CAPABILITIES=dict(semi_automatic=True,detachable_magazine=True,last_round_hold_open=True,
                  charge_state='empty magazine; ends locked open',whole_weapon_motion='external only',
                  material_binding='retain imported PBR materials; no Rifle-name override')

def event_seconds(clip):return {k:v/FPS for k,v in CLIPS[clip]['events'].items()}

def state_at(clip,frame):
 spec=CLIPS[clip]
 if frame>=spec['frames']:return spec['end']
 if clip in ('Fire','FireSemi') and 2<=frame<8:return 'cycling'
 if clip=='FireLast' and frame>=2:return 'last_cycling' if frame<7 else 'empty_open'
 if clip=='ReloadEmpty' and 91<=frame<118:return 'empty_reloaded_open'
 if clip in ('Reload','ReloadEmpty') and spec['events']['magazine_out']<=frame<spec['events']['magazine_in']:
  return 'live_mag_out' if clip=='Reload' else 'empty_mag_out'
 return spec['start']

def transition(state,clip):
 spec=CLIPS[clip]
 if state!=spec['start']:raise ValueError(f'{clip} requires {spec["start"]}, got {state}')
 return spec['end']

def interrupt(clip,frame):
 # A paused action is resumed at its saved time, never restarted with a new
 # full-pose action while its magazine is absent. Consumers retain this token.
 if not 0<=frame<=CLIPS[clip]['frames']:raise ValueError('Outside clip')
 return dict(version=VERSION,clip=clip,frame=frame,state=state_at(clip,frame),resume='same clip and frame')
