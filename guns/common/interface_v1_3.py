"""Additive 1.3 schema: manually locking, nonreciprocating charging handles.

Existing 1.0/1.1 bindings are untouched; a member owns its timings and states.
"""
def manifest(binding):
    assert binding.VERSION == '1.3.0' and binding.FPS == 60
    caps = binding.CAPABILITIES
    for flag in ('closed_bolt', 'select_fire', 'detachable_magazine', 'manual_handle_lock'):
        assert caps[flag] is True, flag
    assert caps['last_round_hold_open'] is False
    assert caps['charging_handle_reciprocates'] is False
    assert {'Idle', 'Fire', 'FireSemi', 'FireAuto', 'FireLast', 'Reload',
            'ReloadEmpty', 'Charge', 'Inspect', 'Selector'} <= set(binding.CLIPS)
    for name, spec in binding.CLIPS.items():
        assert spec['start'] in binding.STATES and spec['end'] in binding.STATES, name
        assert spec['frames'] > 0 and isinstance(spec['required'], bool), name
        assert all(0 <= f <= spec['frames'] for f in spec['events'].values()), name
    assert binding.CLIPS['FireLast']['end'] == 'empty_closed'
    assert binding.CLIPS['ReloadEmpty']['start'] == 'empty_closed'
    return dict(version=binding.VERSION, clips=len(binding.CLIPS))
