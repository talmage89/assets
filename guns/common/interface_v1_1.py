"""Additive 1.1 schema for tube-fed members; 1.0 checker is left unchanged."""
def manifest(binding):
 assert binding.VERSION=='1.1.0' and binding.FPS==60
 assert {'Idle','Fire','FireLast','Reload','ReloadEmpty','Inspect'}<=set(binding.CLIPS)
 assert binding.CAPABILITIES['pump_action'] and binding.CAPABILITIES['tube_magazine']
 for name,s in binding.CLIPS.items():
  assert s['start'] in binding.STATES and s['end'] in binding.STATES,name
  assert s['frames']>0 and isinstance(s['required'],bool)
  assert all(0<=f<=s['frames'] for f in s['events'].values())
  for p in s.get('interruptible',[]):
   assert 0<=p['begin']<=p['end']<=s['frames'] and p['state'] in binding.STATES
 return dict(version=binding.VERSION,clips=len(binding.CLIPS))
