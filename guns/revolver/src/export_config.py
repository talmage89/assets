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

# Mip-layout follow-up: one further bounded last-digit MikkTSpace drift.
EXPORT_TANGENT_ROUNDING += [{'mesh': 0,
  'primitive': 0,
  'vertex': 9970,
  'position': [-0.008325641974806786, 0.030723724514245987, -0.0511554554104805],
  'normal': [-0.5879799723625183, -0.5879799723625183, -0.5554810166358948],
  'uv': [0.1091633141040802, 0.178663432598114],
  'tangent': [0.5623999834060669, -0.7907999753952026, 0.241799995303154, 1.0]}]

# Further repeat-export drift, bounded to the same one-digit rounding step.
EXPORT_TANGENT_ROUNDING += [{'mesh': 0,
  'primitive': 0,
  'vertex': 24105,
  'position': [-0.0036384486593306065, 0.0694710910320282, 0.008339623920619488],
  'normal': [-0.4966960847377777, -0.5085960030555725, 0.7032944560050964],
  'uv': [0.26178622245788574, 0.30661290884017944],
  'tangent': [-0.864300012588501, 0.21559999883174896, -0.4544000029563904, 1.0]}]
