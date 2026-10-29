"""Standalone texture policy; changing it never invalidates the gun bake."""
from pathlib import Path
import runpy
_settings=runpy.run_path(str(Path(__file__).with_name("config.py")))
globals().update({k:v for k,v in _settings.items() if k.isupper()})
DETACHABLES=[dict(spec,texture_size=1024,texture_clusters=spec['filename']=='magazine_loaded.glb') for spec in DETACHABLES]

# Branch-point MikkTSpace rounding anchors; exact source signatures are guarded.
EXPORT_TANGENT_ROUNDING=[{'mesh': 0,
  'primitive': 0,
  'vertex': 9340,
  'position': [0.01083889789879322, 0.04090924188494682, -0.1359890252351761],
  'normal': [0.3984968662261963, -0.5943953394889832, -0.6984944939613342],
  'uv': [0.1512778103351593, 0.9532109498977661],
  'tangent': [0.8323000073432922, 0.5543000102043152, 0.0031999999191612005, 1.0]},
 {'mesh': 0,
  'primitive': 0,
  'vertex': 31352,
  'position': [-0.006550000514835119, 0.03920000419020653, -0.013729550875723362],
  'normal': [0.9545689225196838, -0.2979903221130371, 0.0],
  'uv': [0.8557839393615723, 0.800248920917511],
  'tangent': [0.12030000239610672, 0.38519999384880066, 0.914900004863739, 1.0]}]
