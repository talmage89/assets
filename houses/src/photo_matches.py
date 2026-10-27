"""Three house comparisons: facade, room-over-garage and summer age.

These are type comparisons, not surveys or copies. The room-over-garage
reference has a split entry and projecting bay; the 1991 facade reference
has a lower garage and a side-gable main roof.
Fit construction anchors in the areas shared by our authored design. The
reported residuals retain the photographic design/proportion differences.
"""
from pathlib import Path
import sys
import os
sys.path.insert(0,str(Path(__file__).resolve().parent))
from plan import load
p=load(int(os.environ.get('HOUSE_SEED','27')),Path(os.environ['HOUSE_PLAN']) if os.environ.get('HOUSE_PLAN') else None);m,g=p['blocks']

MATCHES=dict(
    colonial_2003_nh=dict(title='2003 colonial / 23 years old, summer daylight and window depth',
        photo='refs/colonial-2003-nh.jpg',crop=(35,110,628,542),
        location=(m.cx,-24,1.8),target=(m.cx,m.y0,3.5),lens=45,
        camera_height_m=(1.8,1.0),lens_bounds_mm=(28,100),background='transparent',
        landmarks=[
            dict(world=(m.x0,m.y0,.508),pixel=(61,501)),
            dict(world=(m.x1,m.y0,.508),pixel=(600,500)),
            dict(world=(m.x0,m.y0,5.9944),pixel=(61,246)),
            dict(world=(m.x1,m.y0,5.9944),pixel=(600,256)),
            dict(world=(m.cx,m.y0,.508),pixel=(326,501)),
        ]),
    colonial_rog_ri=dict(title='Room-over-garage / gable, opening scale and trim',
        photo='refs/colonial-rog-ri.jpg',crop=(285,45,576,353),
        location=(g.cx+1,g.y0-16,1.8),target=(g.cx,g.y0,3.7),lens=42,
        camera_height_m=(1.8,1.0),lens_bounds_mm=(28,100),background='transparent',
        landmarks=[
            dict(world=(g.x0,g.y0,.1016),pixel=(321,331)),
            dict(world=(g.x1,g.y0,.1016),pixel=(539,321)),
            dict(world=(g.x0,g.y0,5.588),pixel=(321,130)),
            dict(world=(g.x1,g.y0,5.588),pixel=(539,132)),
            dict(world=(g.cx,g.y0,g.height(g.cx,g.y0)),pixel=(434,68)),
        ]),
    colonial_1991_oh=dict(title='1991 colonial / two floors, entry and window rhythm',
        photo='refs/colonial-1991-oh.jpg',crop=(0,165,525,565),
        location=(m.cx,-24,2.0),target=(m.cx,m.y0,3.3),lens=42,
        camera_height_m=(1.8,1.0),lens_bounds_mm=(28,100),background='transparent',
        landmarks=[
            dict(world=(m.x0,m.y0,.508),pixel=(27,500)),
            dict(world=(m.cx+m.width*.25,m.y0,.508),pixel=(454,500)),
            dict(world=(m.x0,m.y0,5.9944),pixel=(24,253)),
            dict(world=(m.cx+m.width*.25,m.y0,5.9944),pixel=(454,255)),
            dict(world=(m.cx,m.y0,.508),pixel=(316,495)),
            dict(world=(m.cx,m.y0,2.54),pixel=(316,402)),
        ]),
)
