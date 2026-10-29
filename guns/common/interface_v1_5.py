"""Additive schema for lever/top-ejection members; existing bindings unchanged."""
from guns.common.interface_checks import manifest as base_manifest


def manifest(binding):
    result=base_manifest(binding)
    assert binding.SUPPLEMENT_VERSION=='1.5.0'
    for key in ('lever_action','manual_action','tube_magazine','shell_by_shell_loading',
                'side_loading_gate','exposed_hammer','top_ejection'):
        assert binding.CAPABILITIES[key],key
    assert binding.CAPABILITIES['tube_capacity']>0
    for s in binding.CLIPS.values():
        for phase in s.get('interruptible',[]):
            assert 0<=phase['begin']<=phase['end']<=s['frames']
            assert phase['state'] in binding.STATES
    return dict(result,supplement=binding.SUPPLEMENT_VERSION)
