TITLE='Rill / C48 rotomolded cooler'
BUDGETS={'Cooler':5000}
BOUNDS={'Cooler':dict(size=(.68905,.472,.4191),tolerance=(.001,.001,.001))}
REQUIRED_NODES=('Cooler','Lid','Latch_L','Latch_R','Drain_Plug')
UV_DENSITY_BANDS=dict(reference_size=1024,p5_min=270,median_min=330,median_max=900,p95_max=1500)
UV_MIN_COVERAGE=.35
UV_PRIORITY={'Insulated hollow':1.1,'Insulated stepped':1.1,'Rubber T latch':1.15,'Rubber foot':.7}
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['Cooler','Lid','Latch_L','Latch_R','Drain_Plug'],cage_m=.002,ray_distance_m=.010,ao_distance_m=.02)
MOTIONS=[dict(node='Latch_'+s,axis='X',range=[0,-90],step=3,tolerance_m=.0005,allow=[
 dict(moving='Rubber latch eye',fixed='Latch captive pin',reason='Captive pin in silicone bearing eye'),
 dict(moving='Rubber T latch',fixed='Body latch reaction lug',reason='Silicone cam lip flexes off retaining lug during release')]) for s in ('L','R')]
MOTIONS.append(dict(node='Drain_Plug',axis='X',range=[0,360],step=15,tolerance_m=.0003))
SHOTS={
 'hero_closed':dict(location=(1.12,-1.45,.91),target=(0,0,.21),lens=65,aspect=1.35),
 'hero_open':dict(location=(1.18,-1.55,1.15),target=(0,.03,.43),lens=46,aspect=1.25,lid=-100,parts={'Latch_L':dict(rotation_degrees=(-90,0,0)),'Latch_R':dict(rotation_degrees=(-90,0,0))}),
 'front':dict(location=(0,-2,.21),target=(0,0,.21),ortho=.84,aspect=1.4),
 'side':dict(location=(2,0,.21),target=(0,0,.21),ortho=.61,aspect=1.1),
 'back':dict(location=(0,2,.21),target=(0,0,.21),ortho=.84,aspect=1.4,studio_yaw=180),
 'top':dict(location=(0,0,2),target=(0,0,0),ortho=.84,aspect=1.4),
 'controls':dict(location=(.59,-.77,.55),target=(.19,-.19,.32),lens=78,aspect=1.25),
 'casting':dict(location=(.82,.39,.40),target=(.32,.04,.19),lens=72,aspect=1.25),
 'gasket':dict(location=(.90,-1.15,.95),target=(0,.08,.40),lens=63,aspect=1.25,lid=-100,parts={'Latch_L':dict(rotation_degrees=(-90,0,0)),'Latch_R':dict(rotation_degrees=(-90,0,0))}),
 'scale':dict(location=(2.6,-4.8,2.0),target=(-.37,0,.83),lens=65,aspect=1.25,human=True),
}
EXTRA_SHOTS=['hero_open','gasket']
