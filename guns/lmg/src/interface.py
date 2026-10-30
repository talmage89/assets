"""Visual consumer binding; additive 1.8.0, no firearm simulation."""
VERSION='1.0.0'
SUPPLEMENT_VERSION='1.8.0'
FPS=60
CAPABILITIES=dict(belt_feed=True,detachable_box=True,open_bolt=True,full_automatic=True,
 semi_automatic=False,select_fire=False,last_round_hold_open=False,
 charging_handle_reciprocates=False,bipod=True,box_capacity=200,
 whole_weapon_motion='external only',visual_feed='count-aware rigid display chain',
 material_binding='retain imported PBR material indices')
STATES={
 'belt_ready':dict(action='rear',box='loaded',chamber=0,cover='latched',trigger='reset'),
 'belt_auto_held':dict(action='rear',box='loaded',chamber=0,cover='latched',trigger='held'),
 'belt_tail_ready':dict(action='rear',box='tail_3',chamber=0,cover='latched',trigger='reset'),
 'belt_last_ready':dict(action='rear',box='last',chamber=0,cover='latched',trigger='reset'),
 'empty_closed':dict(action='forward',box='empty',chamber=0,cover='latched',trigger='reset'),
 'belt_safe_ready':dict(action='rear',box='loaded',chamber=0,cover='latched',trigger='reset',safety='on')}
def spec(frames,start='belt_ready',end='belt_ready',events=None,required=True):return dict(frames=frames,start=start,end=end,events=events or {},required=required)
CLIPS={
 'Idle':spec(1),'IdleEmpty':spec(60,'empty_closed','empty_closed'),
 'IdleSafe':spec(1,'belt_safe_ready','belt_safe_ready'),
 'Fire':spec(12,events=dict(shot=3,eject=5,advance=8,caught_rear=10,reset=12)),
 'Burst':spec(24,events=dict(shot=3,shot_2=11,shot_3=19,reset=24)),
 'CeaseFire':spec(8,'belt_auto_held','belt_ready',dict(caught_rear=6,reset=8)),
 'FireLast':spec(12,'belt_last_ready','empty_closed',dict(shot=3,eject=5,empty_forward=8,reset=12)),
 'Reload':spec(360,events=dict(latch_release=18,cover_open=60,belt_lift=88,magazine_out=140,replacement=172,magazine_in=215,belt_laid=264,cover_closed=324,latched=340)),
 'ReloadEmpty':spec(420,'empty_closed','belt_ready',dict(latch_release=18,cover_open=60,magazine_out=140,replacement=172,magazine_in=215,belt_laid=264,cover_closed=324,latched=340,handle_draw=380,caught_rear=380,handle_forward=410)),
 'Charge':spec(66,'empty_closed','belt_ready',dict(handle_draw=30,caught_rear=30,handle_forward=60)),
 'BipodDeploy':spec(84,events=dict(unfolded=48,extended=78)),
 'BipodFold':spec(84,events=dict(retracted=30,folded=78)),
 'SafetyOn':spec(18,'belt_ready','belt_safe_ready',dict(safe=14)),
 'SafetyOff':spec(18,'belt_safe_ready','belt_ready',dict(fire=14)),
 'CarryRaise':spec(30,events=dict(raised=26)),
 'CarryFold':spec(30,events=dict(folded=26)),
 'BoxOpen':spec(60,'empty_closed','empty_closed',events=dict(lid_open=54)),
 'Inspect':spec(180,events=dict(safe=18,cover_open=65,shoulder_rest_raised=65,cover_closed=142,shoulder_rest_folded=142,fire=172)),
 'BeltEnd':spec(42,'belt_tail_ready','empty_closed',dict(shot=4,shot_2=14,shot_3=24,empty_forward=30))}
def interrupt(clip,frame,remaining=200,phase=0):
 if not 0<=frame<=CLIPS[clip]['frames']:raise ValueError(frame)
 return dict(version=SUPPLEMENT_VERSION,clip=clip,frame=frame,remaining=remaining,phase=phase,resume='same clip and time')
