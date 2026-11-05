"""Four-year reference pair; wheel-only calibration, original body held fixed."""
from pathlib import Path
import runpy
S=runpy.run_path(str(Path(__file__).with_name('hatch_spec.py')))
ROOT=Path(__file__).resolve().parents[1]
F,R,H=S['FRONT_AXLE'],S['REAR_AXLE'],S['HUB_HEIGHT']
MATCHES={}
for view,picks,size,location in [
 ('front',[(620,510),(1116,440),(623,611),(1114,533)],(3354,1830),(5,-7,1.8)),
 ('rear',[(78,390),(586,500),(80,486),(591,608)],(3423,1884),(5,7,1.8))]:
 width,height=size;factor=width/1200;sign=1
 MATCHES['used_'+view]=dict(title='H120 / four-year hatchback '+view+' (MY2018 photographed 2022)',photo=str(ROOT/('refs/hatch-used-'+view+'.jpg')),
  crop=(-120,-80,width+120,height+80),location=location,target=(0,0,.75),lens=62,camera_height_m=(1.50,.15),lens_bounds_mm=(30,120),background='transparent',exposure=-.8,
  landmarks=[dict(world=p,pixel=[v*factor for v in xy],weight=1) for p,xy in zip([(sign*.865,F,H),(sign*.870,R,H),(sign*.855,F,0),(sign*.860,R,0)],picks)])
