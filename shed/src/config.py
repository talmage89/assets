from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from dimensions import *
TITLE='Hearthfield / 810 garden shed'
BUDGETS={'Shed':10000}
BOUNDS={'Shed':dict(size=(2*(RX+.007),2*(RY+.012),RIDGE+.043),tolerance=(.005,.005,.005))}
DELIVERY_BOUNDS=BOUNDS['Shed']
REQUIRED_NODES=('Door_L','Door_R')
UV_TARGET_DENSITY=170
UV_DENSITY_BANDS=dict(reference_size=2048,p5_min=65,median_min=110,median_max=310,p95_max=520)
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['Door_L','Door_R'],cage_m=.0006,ray_distance_m=.002,ao_distance_m=.08)
MATERIAL_OVERRIDES={'Window glass':dict(transmission=.72,ior=1.46)}
STUDIO=dict(scale=3.4,light_center=(0,0,.7),backdrop_height=15,backdrop_half_width=22)
SHOTS={
 'hero_closed':dict(location=(6,-8,4.7),target=(0,0,1.45),lens=52,aspect=1.2),
 'hero_open':dict(location=(4,-7,3.5),target=(0,-.15,1.42),lens=49,aspect=1.25,parts={'Door_L':dict(rotation_degrees=(0,0,-105)),'Door_R':dict(rotation_degrees=(0,0,105))}),
 'front':dict(location=(0,-8,1.5),target=(0,0,1.5),ortho=3.8,aspect=1),
 'side':dict(location=(8,0,1.5),target=(0,0,1.5),ortho=4.1,aspect=1.15),
 'back':dict(location=(0,8,1.5),target=(0,0,1.5),ortho=3.8,aspect=1,studio_yaw=180),
 'top':dict(location=(0,0,9),target=(0,0,0),ortho=4,aspect=1),
 'controls':dict(location=(2,-3.7,1.15),target=(.65,-1.5,.75),lens=65,aspect=1.2),
 'casting':dict(location=(3.1,-2.4,3.8),target=(.88,-.25,2.62),lens=65,aspect=1.3),
 'interior':dict(exposure=1.25,location=(.05,-2.7,1.6),target=(.1,.6,1.7),lens=26,aspect=1.2,parts={'Door_L':dict(rotation_degrees=(0,0,-105)),'Door_R':dict(rotation_degrees=(0,0,105))}),
 'scale':dict(location=(6,-9,4.3),target=(-.3,0,1.4),lens=52,aspect=1.3,human=True,human_offset=(-1.35,-1.4,0)),
}
EXTRA_SHOTS=['hero_open','interior']
MOTIONS=[dict(node='Door_'+k,axis='Z',range=r,step=5,tolerance_m=.0004,allow=[dict(moving='Door hinge sleeve',fixed='Fixed hinge pin',reason='Pin inside the sleeve bore')]) for k,r in [('L',[-110,0]),('R',[0,110])]]
CONTACTS=[('PT 4x4 skid','PT floor joist 00',.0001),('Door jack stud','Double 2x6 door header',.0001),('Rafter 0 1','Roof plywood sheathing 1',.0001)]
