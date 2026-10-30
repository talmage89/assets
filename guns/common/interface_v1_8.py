"""Additive cosmetic belt/open-bolt binding checks; base meanings are untouched."""
from guns.common.interface_checks import manifest as base_manifest

def manifest(binding):
 base=base_manifest(binding)
 assert binding.SUPPLEMENT_VERSION=='1.8.0'
 caps=binding.CAPABILITIES
 for name in ('belt_feed','detachable_box','open_bolt','full_automatic','bipod'):assert caps[name] is True,name
 for name in ('semi_automatic','select_fire','last_round_hold_open','charging_handle_reciprocates'):assert caps[name] is False,name
 assert caps['box_capacity']==200
 # Separate new state names keep the existing closed-bolt ready meanings intact.
 assert not {'ready','last_ready'} & set(binding.STATES)
 for name in ('belt_ready','belt_last_ready','belt_safe_ready','belt_auto_held','belt_tail_ready'):
  state=binding.STATES[name];assert state['chamber']==0 and state['action']=='rear',name
 assert binding.CLIPS['Idle']['start']=='belt_ready'
 assert binding.CLIPS['FireLast']['end']=='empty_closed'
 assert binding.CLIPS['CeaseFire']['end']=='belt_ready'
 assert {'Reload','ReloadEmpty','Burst','BeltEnd','BipodDeploy','BipodFold','SafetyOn','SafetyOff'}<=set(binding.CLIPS)
 return dict(base_version=base['version'],supplement='1.8.0',clips=base['clips'],new_states=sorted(set(binding.STATES)-{'empty_closed'}))
