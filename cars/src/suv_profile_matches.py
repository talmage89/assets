"""Profile photographs retain perspective; four chassis picks, fixed estimated lens.

These cameras supplement, never replace, the raw orthographic overlays. The
85 mm estimate is not EXIF. No body outline is part of the calibration.
"""
from pathlib import Path
import runpy
S=runpy.run_path(str(Path(__file__).with_name('suv_spec.py')))
ROOT=Path(__file__).resolve().parents[1];MATCHES={}
for make,pixels in [('rav4',[(244,574),(938,575),(244,665),(938,665)]),('crv',[(246,574),(937,574),(246,665),(937,665)])]:
 world=[(.894,S['FRONT_AXLE'],S['HUB_HEIGHT']),(.899,S['REAR_AXLE'],S['HUB_HEIGHT']),(.880,S['FRONT_AXLE'],0),(.885,S['REAR_AXLE'],0)]
 MATCHES[make+'_profile']=dict(title='X220 / '+make+' / perspective profile, chassis only',photo=str(ROOT/('refs/suv-'+make+'-side.jpg')),crop=(-100,-60,2200,1635),location=(11.5,0,.85),target=(0,0,.85),lens=85,lens_bounds_mm=(85,85),background='transparent',landmarks=[dict(world=w,pixel=[1.75*v for v in p]) for w,p in zip(world,pixels)])
