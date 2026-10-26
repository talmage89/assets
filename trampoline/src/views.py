TITLE='Alder Play / Orbit 14'
STUDIO=dict(scale=4,light_center=(0,0,.6),backdrop_height=15,backdrop_half_width=22)
SHOTS={
 'hero_closed':dict(location=(7,-9,4.6),target=(0,0,1.3),lens=51,aspect=1.25),
 'front':dict(location=(0,-9,1.4),target=(0,0,1.4),ortho=5.0,aspect=1.4),
 'side':dict(location=(9,0,1.4),target=(0,0,1.4),ortho=5.0,aspect=1.4),
 'back':dict(location=(0,9,1.4),target=(0,0,1.4),ortho=5,aspect=1.4,studio_yaw=180),
 'top':dict(location=(0,0,9),target=(0,0,0),ortho=4.9,aspect=1),
 'controls':dict(location=(.8,-4.6,2),target=(0,-1.9,1.5),lens=65,aspect=1.2),
 'casting':dict(location=(3,-3.4,1.05),target=(1.55,-1.25,.75),lens=65,aspect=1.2),
 'fabric':dict(location=(1.8,-3,2.1),target=(.85,-1.25,1.05),lens=62,aspect=1.2),
 'underpad':dict(location=(.32,-1.20,1.14),target=(0,-1.98,.90),lens=65,aspect=1.4),
 'scale':dict(location=(7,-10,4.8),target=(-.25,0,1.2),lens=51,aspect=1.3,human=True,human_offset=(-1.8,-1.4,0)),
 'underside':dict(location=(4,-5,.22),target=(0,0,.7),lens=43,aspect=1.3),
}
EXTRA_SHOTS=['fabric','underpad','underside']
