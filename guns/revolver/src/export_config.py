"""Standalone texture policy; changing it never invalidates the gun bake."""
from pathlib import Path
import runpy
_settings=runpy.run_path(str(Path(__file__).with_name("config.py")))
globals().update({k:v for k,v in _settings.items() if k.isupper()})
DETACHABLES=[dict(spec,texture_size=(1024 if spec["name"]=="LoadedSpeedloader" else 512)) for spec in DETACHABLES]

# Branch-point MikkTSpace rounding anchors; exact source signatures are guarded.
EXPORT_TANGENT_ROUNDING=[{'mesh': 0,
  'primitive': 0,
  'vertex': 26134,
  'position': [-0.016468632966279984, -0.04541745409369469, 0.02397993952035904],
  'normal': [-0.9904832243919373, -0.08619853854179382, -0.10729818046092987],
  'uv': [0.30672523379325867, 0.81462562084198],
  'tangent': [0.12639999389648438, -0.26100000739097595, -0.9570000171661377, 1.0]},
 {'mesh': 0,
  'primitive': 0,
  'vertex': 40749,
  'position': [0.004033419769257307, 0.0394313670694828, -0.0260030385106802],
  'normal': [-0.7081308960914612, -0.6482282280921936, 0.27991220355033875],
  'uv': [0.9341432452201843, 0.23678886890411377],
  'tangent': [-0.20659999549388885, -0.18880000710487366, -0.9599999785423279, 1.0]}]
