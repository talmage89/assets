"""Delivered frame: meters, +Z up, pumper faces -Y, footprint origin at grade."""
BUDGETS={'Hydrant':6000}
BOUNDS={'Hydrant':{'size':(.415544,.395,.8128),'tolerance':(.003,.001,.0001)}}
SHOTS={
 'hero_closed':dict(location=(1.12,-1.85,1.13),target=(0,-.015,.405),lens=65,aspect=1.0),
 'hero_open':dict(location=(1.12,-1.85,1.13),target=(0,-.015,.405),lens=65,aspect=1.0),
 'controls':dict(location=(.64,-.88,.71),target=(.015,-.04,.50),lens=70,aspect=1.2),
 'casting':dict(location=(-.65,1.13,.66),target=(0,.015,.43),lens=74,aspect=1.2),
 'front':dict(location=(0,-3,.4064),target=(0,0,.4064),ortho=1.04,aspect=1),
 'side':dict(location=(3,0,.4064),target=(0,0,.4064),ortho=1.04,aspect=1),
 'back':dict(location=(0,3,.4064),target=(0,0,.4064),ortho=1.04,aspect=1),
 'top':dict(location=(0,0,3),target=(0,0,.42),ortho=.65,aspect=1),
 'scale':dict(location=(1.65,-4.0,1.80),target=(-.40,0,.87),lens=65,aspect=1.0,human=True),
}
UV_PRIORITY={'Cast upper barrel':1.2,'Pumper cap':1.25,'Cast bonnet':1.1,'Chain':.65}
UV_DEFAULT_PRIORITY=1
# Pixels per meter in the delivered 1024 atlas, not scaled grill defaults.
UV_DENSITY_BANDS=dict(p5_min=280,median_min=550,median_max=900,p95_max=1500)
REQUIRED_NODES=('FireHydrant',)
