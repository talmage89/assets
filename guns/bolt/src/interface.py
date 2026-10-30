"""B24 additive binding: base interface 1.0.0, bolt/optic supplement 1.2.0."""
VERSION='1.0.0'
SUPPLEMENT_VERSION='1.2.0'
FPS=60
CAPABILITIES=dict(bolt_action=True,detachable_magazine=True,last_round_hold_open=False,
    bipod=True,magnified_optic=True,whole_weapon_motion='external only',magazine_capacity=5,
    visible_cartridge_feed=True,feed_type='push',case_handoff_bone='CycleCase')
STATES={name:dict(action=action,magazine=mag,chamber=rounds) for name,action,mag,rounds in [
    ('ready','locked','loaded',1),('last_ready','locked','empty',1),('empty_closed','locked','empty',0),
    ('empty_open','open','empty',0),('cycling','moving','loaded',0),('last_cycling','moving','empty',0),
    ('live_mag_out','locked','absent',1),('empty_mag_out','open','absent',0),
    ('empty_reloaded_open','open','loaded',0)]}
CLIPS={
 'Idle':dict(required=True,frames=1,start='ready',end='ready',events={}),
 'IdleEmpty':dict(required=False,frames=60,start='empty_closed',end='empty_closed',events={}),
 'Fire':dict(required=True,frames=132,start='ready',end='ready',events={'shot':3,'unlock':42,'eject':64,'chamber':104,'lock':122,'reset':132}),
 'FireLast':dict(required=True,frames=132,start='last_ready',end='empty_closed',events={'shot':3,'unlock':42,'eject':64,'lock':122,'reset':132}),
 'Reload':dict(required=True,frames=180,start='ready',end='ready',events={'magazine_out':48,'replacement':78,'magazine_in':142}),
 'ReloadEmpty':dict(required=True,frames=252,start='empty_closed',end='ready',events={'unlock':25,'open':48,'magazine_out':86,'replacement':116,'magazine_in':180,'chamber':219,'lock':242}),
 'Inspect':dict(required=False,frames=180,start='ready',end='ready',events={'safe':25,'power':80,'reset':170}),
 'BipodDeploy':dict(required=True,frames=78,start='ready',end='ready',events={'unfolded':42,'extended':72}),
 'BipodFold':dict(required=True,frames=78,start='ready',end='ready',events={'retracted':32,'folded':72}),
}
def state_at(clip,frame):
 s=CLIPS[clip]
 if frame>=s['frames']:return s['end']
 if clip=='Fire' and 3<=frame<104:return 'cycling'
 if clip=='FireLast' and 3<=frame:return 'last_cycling' if frame<122 else 'empty_closed'
 if clip=='Reload' and 48<=frame<142:return 'live_mag_out'
 if clip=='ReloadEmpty':
  if 86<=frame<180:return 'empty_mag_out'
  if 180<=frame<219:return 'empty_reloaded_open'
  if 48<=frame<86:return 'empty_open'
 return s['start']
def transition(state,clip):
 s=CLIPS[clip]
 if state!=s['start']:raise ValueError((state,clip))
 return s['end']
def interrupt(clip,frame):
 if not 0<=frame<=CLIPS[clip]['frames']:raise ValueError(frame)
 return dict(version=SUPPLEMENT_VERSION,clip=clip,frame=frame,state=state_at(clip,frame),resume='same clip and frame')
