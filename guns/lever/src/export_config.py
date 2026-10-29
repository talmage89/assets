"""Export-only delivery policy; source atlas and geometry are unchanged."""
from pathlib import Path
import runpy
_settings=runpy.run_path(str(Path(__file__).with_name("config.py")))
globals().update({k:v for k,v in _settings.items() if k.isupper()})

# Branch-point MikkTSpace rounding anchors; exact source signatures are guarded.
EXPORT_TANGENT_ROUNDING=[{'mesh': 0,
  'primitive': 0,
  'vertex': 44505,
  'position': [-0.003100000089034438, 0.0, -0.0848500058054924],
  'normal': [-1.0, 0.0, 0.0],
  'uv': [0.8080399632453918, 0.7481789588928223],
  'tangent': [0.0, -0.79339998960495, 0.6087999939918518, 1.0]},
 {'mesh': 0,
  'primitive': 0,
  'vertex': 44598,
  'position': [-0.003100000089034438, 0.003670518286526203, -0.0820164903998375],
  'normal': [-1.0, 0.0, 0.0],
  'uv': [0.8068454265594482, 0.7453275918960571],
  'tangent': [0.0, -0.7932999730110168, 0.6087999939918518, 1.0]}]
