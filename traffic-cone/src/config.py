TITLE='Waymark / 28-inch traffic cone'
BUDGETS={'TrafficCone':1000}
BOUNDS={'TrafficCone':dict(size=(.3556,.3556,.7112),tolerance=(.0001,.0001,.0001))}
# Reach the high base surface beyond the inset coarse corner chords.
BAKE_CAGE=.005
BAKE_RAY=.012
UV_SMART_ASPECT=False
UV_DENSITY_BANDS=dict(p5_min=150,median_min=300,median_max=900,p95_max=1400)
CONTACTS=[('Hollow orange cone and grip','Weighted black base with stacking bore',.0005)]
SHOTS={
'hero_closed':dict(location=(1.0,-1.5,1.02),target=(0,0,.34),lens=63,aspect=1),
'front':dict(location=(0,-3,.3556),target=(0,0,.3556),ortho=.95,aspect=1),
'side':dict(location=(3,0,.3556),target=(0,0,.3556),ortho=.95,aspect=1),
'back':dict(location=(0,3,.3556),target=(0,0,.3556),ortho=.95,aspect=1),
'top':dict(location=(0,0,3),target=(0,0,.35),ortho=.48,aspect=1),
'controls':dict(location=(.24,-.40,.84),target=(0,0,.60),lens=65,aspect=1.2),
'casting':dict(location=(.38,-.58,.28),target=(0,0,.09),lens=68,aspect=1.2),
'scale':dict(location=(1.6,-3.5,1.75),target=(-.38,0,.86),lens=60,aspect=1,human=True),
}
SHOTS['hero_open']=SHOTS['hero_closed']
