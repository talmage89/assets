"""Picket atlas policy; cameras live in views.py to avoid needless rebakes."""
BUDGETS={'WhitePicket':4200}
BOUNDS={'WhitePicket':dict(size=(7.05405,.1175,1.205),tolerance=(.001,.001,.001))}
UV_DENSITY_BANDS=dict(reference_size=1024,p5_min=100,median_min=110,median_max=240,p95_max=500)
UV_PRIORITY={'Picket_Gate hinge':1.5,'Picket_Gate lifting':1.5}
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['Picket_A','Picket_B','Picket_End','Picket_Line','Picket_Corner','Picket_GateBay','Picket_Gate','Picket_Gate_Latch'],cage_m=.0015,ray_distance_m=.007,ao_distance_m=.035)
REQUIRED_NODES=tuple(['Picket_A','Picket_B','Picket_End','Picket_Line','Picket_Corner','Picket_GateBay','Picket_Gate','Picket_Gate_Latch']+[n+'__'+s for n in ('Picket_A','Picket_B','Picket_GateBay') for s in ('L','R')])
MOTIONS=[dict(node='Picket_Gate_Latch',axis='Y',range=[-65,0],step=2,tolerance_m=.0003)]
from pathlib import Path
import runpy
v=runpy.run_path(str(Path(__file__).with_name('views.py')));SHOTS=v['SHOTS'];STUDIO=v['STUDIO']
