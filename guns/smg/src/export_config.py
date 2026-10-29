"""Standalone texture policy; changing it never invalidates the gun bake."""
from pathlib import Path
import runpy
_settings=runpy.run_path(str(Path(__file__).with_name("config.py")))
globals().update({k:v for k,v in _settings.items() if k.isupper()})
DETACHABLES=[dict(spec,texture_size=1024) for spec in DETACHABLES]

# Branch-point MikkTSpace rounding anchors; exact source signatures are guarded.
EXPORT_TANGENT_ROUNDING=[{'mesh': 0,
  'primitive': 0,
  'vertex': 10849,
  'position': [0.007338518742471933, 0.1276310533285141, -0.3330000042915344],
  'normal': [0.793351948261261, 0.6087631583213806, 0.0],
  'uv': [0.7561852931976318, 0.9227297306060791],
  'tangent': [0.6087999939918518, -0.7932999730110168, 0.0, 1.0]},
 {'mesh': 0,
  'primitive': 0,
  'vertex': 42396,
  'position': [0.0033667548559606075, 0.08249448239803314, -0.15550000965595245],
  'normal': [-0.29079869389533997, 0.7020968198776245, -0.6499970555305481],
  'uv': [0.8959172964096069, 0.0336918830871582],
  'tangent': [0.609499990940094, 0.659600019454956, 0.4397999942302704, 1.0]}]
