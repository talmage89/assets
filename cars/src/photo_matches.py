"""Inspected 3D/pixel landmarks for comparison, not traced profiles.

Coordinates are measured at 1500 px and converted to original pixels. Wheel
hub anchors are on the outer face, not the hidden wheel-center plane. Roof
anchors are design estimates; full residuals disclose their uncertainty.
"""
from pathlib import Path
import runpy
S=runpy.run_path(str(Path(__file__).with_name('pickup_spec.py')))
ROOT=Path(__file__).resolve().parents[1]
def anchor(p,xy,scale):return dict(world=p,pixel=tuple(v*scale for v in xy))
MATCHES={
 'match_front':dict(title='Crew 4x4 / front three-quarter clay',photo=str(ROOT/'refs/ford-lariat-front.jpg'),
    crop=(0,0,5130,2528),location=(7,-10,1.4),target=(0,0,1),lens=55,background='transparent',
    landmarks=[anchor((.964,S['FRONT_AXLE'],S['HUB_HEIGHT']),(656,545),5130/1500),
               anchor((.964,S['REAR_AXLE'],S['HUB_HEIGHT']),(1331,499),5130/1500),
               anchor((.95,S['FRONT_AXLE'],0),(656,682),5130/1500),
               anchor((.95,S['REAR_AXLE'],0),(1331,594),5130/1500),
               anchor((.84,-1.02,1.91),(858,55),5130/1500),
               anchor((.84,.875,1.91),(1120,65),5130/1500),
               anchor((.95,1.041,1.44856),(1200,215),5130/1500),
               anchor((.95,2.844,1.44856),(1425,221),5130/1500)]),
 'match_rear':dict(title='Crew short bed / rear three-quarter clay',photo=str(ROOT/'refs/ford-lariat-rear.jpg'),
    crop=(0,0,4886,2699),location=(7,10,1.4),target=(0,0,1),lens=55,background='transparent',
    landmarks=[anchor((.964,S['FRONT_AXLE'],S['HUB_HEIGHT']),(105,553),4886/1500),
               anchor((.964,S['REAR_AXLE'],S['HUB_HEIGHT']),(638,620),4886/1500),
               anchor((.95,S['FRONT_AXLE'],0),(105,655),4886/1500),
               anchor((.95,S['REAR_AXLE'],0),(638,774),4886/1500),
               anchor((.84,-1.02,1.91),(330,159),4886/1500),
               anchor((.84,.875,1.91),(558,92),4886/1500),
               anchor((.95,2.844,1.44856),(907,222),4886/1500),
               anchor((-.95,2.844,1.44856),(1435,245),4886/1500)]),
}
