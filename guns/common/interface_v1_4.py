"""Revolver supplement schema, separate from existing family interfaces."""
def manifest(binding):
 assert binding.VERSION=='1.4.0' and binding.FPS==60
 cap=binding.CAPABILITIES
 assert cap['cylinder_capacity']==6 and cap['magazine'] is False
 assert cap['double_action'] and cap['single_action']
 for name,state in binding.STATES.items():
  assert len(state['chambers'])==6 and set(state['chambers'])<={'loaded','fired','empty'},name
  assert isinstance(state['index'],int) and state['action'] in ('closed','open','moving')
 for name,s in binding.CLIPS.items():
  assert s['frames']>0 and s['start'] in binding.STATES and s['end'] in binding.STATES,name
  assert all(0<=v<=s['frames'] for v in s['events'].values()),name
  assert binding.snapshot(name,0)==binding.STATES[s['start']]
  assert binding.snapshot(name,s['frames'])==binding.STATES[s['end']]
 return dict(version=binding.VERSION,clips=len(binding.CLIPS),stable_chambers=6)
