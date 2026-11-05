"""Read the native ground construction profile; extend only the clear run.

Loading the existing local script does not build an asset. Scoped module names
avoid borrowing another family's textures/dimensions module in later stages.
"""
import importlib.util,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
_saved_path=list(sys.path);_saved={k:sys.modules.pop(k,None) for k in ('dimensions','textures')}
try:
 sys.path.insert(0,str(ROOT/'ground/src'))
 spec=importlib.util.spec_from_file_location('_commercial_native_ground',ROOT/'ground/src/build.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 PROFILE=tuple(module.PROFILE)
 TRANSITION=module.transition_stations
finally:
 sys.path[:]=_saved_path
 for name,value in _saved.items():
  sys.modules.pop(name,None)
  if value is not None:sys.modules[name]=value

FLOW=-.1524-.01524  # Lot asphalt meets the outer edge of the 1%-fall public walk.
CURB_TOP=-.01524
STRIP=1.8288
CORNER_ANGLES=tuple(180+90*i/24 for i in range(25))


def depression(s,width,wing=1.524):
 t=max(0,min(1,(abs(s)-width/2)/wing));t=t*t*(3-2*t)
 return .17+.83*t


def cut_top(s,width):return FLOW+.1524*depression(s,width)


def walk_z(v):return CURB_TOP+(v+1.3716)*.01
