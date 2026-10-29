"""Additive break-action/double-trigger manifest validation; no old meanings change."""
def manifest(binding):
 assert binding.VERSION=='1.7.0' and binding.FPS==60
 cap=binding.CAPABILITIES
 assert cap['break_action'] and cap['double_triggers'] and cap['automatic_safety']
 assert cap['barrel_count']==2 and cap['magazine'] is False and cap['extractors']
 assert cap['chamber_states']==('loaded','fired','empty')
 for name,state in binding.STATES.items():
  assert len(state['chambers'])==2 and set(state['chambers'])<={'loaded','fired','empty'},name
  assert len(state['hammers'])==2 and set(state['hammers'])<={'cocked','rest'},name
  assert state['action'] in ('closed','moving','open') and state['safety'] in ('safe','fire')
 for name,s in binding.CLIPS.items():
  assert s['frames']>0 and s['start'] in binding.STATES and s['end'] in binding.STATES,name
  assert all(0<=v<=s['frames'] for v in s['events'].values()),name
  assert binding.snapshot(name,0)==binding.STATES[s['start']],name
  assert binding.snapshot(name,s['frames'])==binding.STATES[s['end']],name
 return dict(version=binding.VERSION,clips=len(binding.CLIPS),stable_chambers=['right','left'])
