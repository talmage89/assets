"""Export-only subsets; never invalidate the canonical rifle bake."""
from pathlib import Path
import runpy

_settings = runpy.run_path(str(Path(__file__).with_name('config.py')))
globals().update({k: v for k, v in _settings.items() if k.isupper()})
DETACHABLES = [dict(spec, texture_size=1024, texture_clusters=True)
               for spec in DETACHABLES]

# Preserve main's branch-point MikkTSpace rounding, guarded by exact signatures.
EXPORT_TANGENT_ROUNDING = [{'mesh': 0,
  'primitive': 0,
  'vertex': 41116,
  'position': [-0.005687868222594261, 0.07539501041173935, -0.1767502725124359],
  'normal': [0.6868268847465515, 0.19730772078037262, -0.699527382850647],
  'uv': [0.7522528767585754, 0.8693001866340637],
  'tangent': [0.7208999991416931, -0.30720001459121704, 0.6212000250816345, 1.0]},
 {'mesh': 0,
  'primitive': 0,
  'vertex': 10441,
  'position': [0.004587456583976746, 0.03838341683149338, -0.23635943233966827],
  'normal': [0.40090781450271606, -0.9161179065704346, -0.0010000194888561964],
  'uv': [0.4743030071258545, 0.6118791699409485],
  'tangent': [0.9157999753952026, 0.4007999897003174, 0.024399999529123306, 1.0]},
 {'mesh': 0,
  'primitive': 0,
  'vertex': 12724,
  'position': [-0.01146525889635086, 0.011232291348278522, -0.002896255813539028],
  'normal': [-0.5533081889152527, -0.3030044436454773, -0.7759113907814026],
  'uv': [0.1701437532901764, 0.30278080701828003],
  'tangent': [0.8330000042915344, -0.20559999346733093, -0.513700008392334, 1.0]}]
