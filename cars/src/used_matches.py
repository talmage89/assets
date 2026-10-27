"""Native-frame calibration of used 4x4 reference photographs; no image tracing.

Four near-side wheel hub/contact picks and one depth/height anchor. Front's
opposite tire is occluded: a low-confidence roof-height anchor discloses this
extra body/configuration uncertainty rather than inventing a ground point.
"""
from pathlib import Path
import runpy
S=runpy.run_path(str(Path(__file__).with_name('pickup_spec.py')))
ROOT=Path(__file__).resolve().parents[1]
F,R,H=S['FRONT_AXLE'],S['REAR_AXLE'],S['HUB_HEIGHT']

def rows(world,pixels,factor,weights=None):
    return [dict(world=p,pixel=[v*factor for v in q],weight=(weights or [1]*len(world))[i]) for i,(p,q) in enumerate(zip(world,pixels))]

MATCHES={
 'used_front':dict(title='Daily-driver black crew 4x4 / front',photo=str(ROOT/'refs/ford-front.jpg'),
    crop=(-250,-150,5103,2709),location=(-6,-8,2.0),target=(0,0,1),lens=44,background='transparent',
    landmarks=rows([(-.964,F,H),(-.964,R,H),(-.920,F,0),(-.920,R,0),(0,.03,S['HEIGHT'])],
      [(767,603),(127,484),(805,760),(145,573),(646,34)],4853/1500,[1,1,1,1,.25])),
 'used_rear':dict(title='Daily-driver black crew 4x4 / rear',photo=str(ROOT/'refs/ford-rear.jpg'),
    crop=(-250,-120,5061,2435),location=(-6,8,2.0),target=(0,0,1),lens=44,background='transparent',
    landmarks=rows([(-.964,F,H),(-.964,R,H),(-.920,F,0),(-.920,R,0),(.858,R,0)],
      [(1414,410),(759,547),(1413,501),(767,682),(320,637)],4811/1500)),
}

# The Ford views are supplemental form/reflection references, photographed in
# their model year. Condition is calibrated against the MY2017 Ram in 2022.
MATCHES['used_front']['title']='Ford street comparison / front (model-year photo)'
MATCHES['used_rear']['title']='Ford street comparison / rear (model-year photo)'
MATCHES.update({
 'aged_front':dict(title='Five-year daily driver / front (MY2017 in September 2022)',photo=str(ROOT/'refs/ram-front.jpg'),
    crop=(-250,-150,4610,2662),location=(12,-16,3),target=(0,0,1),lens=120,background='transparent',paint='Graphite',
    landmarks=rows([(.988,F,H),(.988,R,H),(.920,F,0),(.920,R,0),(-.858,F,0)],
      [(720,637),(1335,598),(715,780),(1324,723),(171,755)],4360/1500),
    lens_status='estimated framing; EXIF reports 27.182 mm physical focal length but cropped sensor framing is uncalibrated',
    calibration_note='Class registration using Alder wheel anchors; Ram wheelbase/tire/trim differ. Body dimensions are not fitted. Picks have roughly 5 px uncertainty at the 1500 px inspection scale.'),
 'aged_rear':dict(title='Five-year daily driver / rear (MY2017 in September 2022)',photo=str(ROOT/'refs/ram-rear.jpg'),
    crop=(-250,-160,5082,2772),location=(12,16,3),target=(0,0,1),lens=110,background='transparent',paint='Graphite',
    landmarks=rows([(.988,F,H),(.988,R,H),(.920,F,0),(.920,R,0),(-.858,R,0)],
      [(104,563),(782,588),(106,680),(794,726),(1180,693)],4832/1500),
    lens_status='estimated framing; EXIF reports 20.796 mm physical focal length but cropped sensor framing is uncalibrated',
    calibration_note='Class registration using Alder wheel anchors; reference wheelbase/tire size differ. No body dimension is refitted; roughly 5 px pick uncertainty at 1500 px.'),
})
