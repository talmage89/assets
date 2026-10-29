"""Additive visual schema: rock-in magazines and reciprocating handle sockets."""
def manifest(binding):
 assert binding.VERSION=='1.6.0' and binding.FPS==60
 c=binding.CAPABILITIES
 assert c['detachable_magazine'] and c['magazine_rocks_in']
 assert c['charging_handle_reciprocates'] and not c['last_round_hold_open']
 for name,s in binding.CLIPS.items():
  assert s['start'] in binding.STATES and s['end'] in binding.STATES,name
  assert s['frames']>0 and isinstance(s['required'],bool)
  assert all(0<=f<=s['frames'] for f in s['events'].values())
 for n in ('Reload','ReloadEmpty'):
  e=binding.CLIPS[n]['events']
  assert e['magazine_out']<e['replacement']<e['front_hook']<e['magazine_in']<e['catch_engaged']
 assert binding.CLIPS['FireLast']['end']=='empty_closed'
 assert binding.CLIPS['ReloadEmpty']['start']=='empty_closed'
 return dict(version=binding.VERSION,clips=len(binding.CLIPS))
