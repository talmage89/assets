"""Privacy family delivery policy and views; +X along bays, −Y good side."""
BUDGETS={'WoodPrivacy':3000}  # Independent per-module 2k limits: check_construction.py.
BOUNDS={'WoodPrivacy':dict(size=(7.02895,.106,1.8808),tolerance=(.004,.008,.004))}
UV_DENSITY_BANDS=dict(reference_size=2048,p5_min=180,median_min=190,median_max=290,p95_max=650)
UV_PRIORITY={'Gate hinge':2.1,'Latch':2.1,'Gate latch':2.1,'Gate picket':1.25,'Gate compression':1.15}
UV_DEFAULT_PRIORITY=1.0
REQUIRED_NODES=('Section_A','Section_B','Post_End','Post_Line','Post_Corner','Gate_Bay','Gate','Latch',
                'Section_A__L','Section_A__R','Section_B__L','Section_B__R','Gate_Bay__L','Gate_Bay__R',
                'Post_End__connect_0','Post_Line__connect_0','Post_Line__connect_180',
                'Post_Corner__connect_90','Post_Corner__connect_180','Gate__free_edge')
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['Section_A','Section_B','Post_End','Post_Line','Post_Corner','Gate_Bay','Gate','Latch'],cage_m=.002,ray_distance_m=.009,ao_distance_m=.04)
# Latch rotates about local Y in the negative direction to lift its free end.
MOTIONS=[dict(node='Latch',axis='Y',range=[-65,0],step=2,tolerance_m=.0003)]

from pathlib import Path
import runpy
_view_config=runpy.run_path(str(Path(__file__).with_name('views.py')))
SHOTS=_view_config['SHOTS']
STUDIO=_view_config['STUDIO']
