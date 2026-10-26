TITLE='Minnow / Petal 60 molded wading pool'
BUDGETS={'KiddiePool':2000}
BOUNDS={'KiddiePool':dict(size=(1.524,1.524,.3048),tolerance=(.001,.001,.001))}
REQUIRED_NODES=('KiddiePool','Water')
UV_DENSITY_BANDS=dict(reference_size=1024,p5_min=90,median_min=130,median_max=500,p95_max=900)
UV_MIN_COVERAGE=.35
UV_PRIORITY={'Thin molded':1.1,'Wet rim grass':1.0,'Water surface':.85}
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['KiddiePool','Water'],cage_m=.0003,ray_distance_m=.0012,ao_distance_m=.018)
MATERIAL_OVERRIDES={'Water surface':dict(transmission=1,ior=1.333)}
MOTIONS=[]
SHOTS={
 'hero_closed':dict(location=(2.1,-2.7,2.4),target=(0,0,.12),lens=63,aspect=1.4),
 'hero_open':dict(location=(2.1,-2.7,2.4),target=(0,0,.12),lens=63,aspect=1.4,hide_assemblies=['Water']),
 'front':dict(location=(0,-3,.16),target=(0,0,.16),ortho=1.76,aspect=2.4),
 'side':dict(location=(3,0,.16),target=(0,0,.16),ortho=1.76,aspect=2.4),
 'back':dict(location=(0,3,.16),target=(0,0,.16),ortho=1.76,aspect=2.4,studio_yaw=180),
 'top':dict(location=(0,0,3),target=(0,0,0),ortho=1.76,aspect=1,hide_assemblies=['Water']),
 'controls':dict(location=(.85,-1.05,.77),target=(.30,-.57,.24),lens=65,aspect=1.3),
 'casting':dict(location=(.7,-.85,1.45),target=(0,0,.01),lens=65,aspect=1.25,hide_assemblies=['Water']),
 'waterline':dict(location=(.82,-1.06,1.0),target=(.18,-.31,.12),lens=65,aspect=1.3),
 'scale':dict(location=(3.0,-4.8,2.5),target=(-.27,0,.78),lens=59,aspect=1.35,human=True),
}
EXTRA_SHOTS=['hero_open','waterline']

EEVEE_SHOT='hero_open'
