TITLE='Rill / residential LED cobra-head street light'
STUDIO_SCALE=3
STUDIO_BACKDROP_HEIGHT=45
BUDGETS={'StreetLight':3200}
BOUNDS={'StreetLight':dict(size=(.38,2.44,7.9561),tolerance=(.003,.03,.003))}
MATERIAL_OVERRIDES={'LED phosphor emitter':dict(emission_strength=16),'Tempered optical glass':dict(transmission=1,ior=1.5)}
REQUIRED_NODES=['StreetLight','LightEmitter']
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['HandholeModule'],cage_m=.0015,ray_distance_m=.006,ao_distance_m=.018)
UV_SMART_ASPECT=False
UV_PRIORITY={'Die-cast':2.0,'Driver':1.7,'Folded':2.2,'LED':2.2,'Tempered':2.2,'Cast heat':1.7,'Photocell':1.5,'Tapered':.35,'Curved':.7}
UV_DENSITY_BANDS=dict(p5_min=90,median_min=120,median_max=700,p95_max=1700)
CONTACTS=[('Anchor base plate','Concrete ground plinth',.001),('Tapered steel shaft','Anchor base plate',.001),('Reinforced handhole cover','Tapered steel shaft',.002),('Pole cap','Tapered steel shaft',.001),('Welded pole arm pad','Tapered steel shaft',.002),('Welded pole arm pad','Mast arm flange',.001),('Curved tapered mast arm','Mast arm flange',.001),('Curved tapered mast arm','Die-cast cobra housing',.001),('Driver gear tray','Die-cast cobra housing',.001),('Internal slipfitter clamp jaw','Curved tapered mast arm',.0003),('Internal slipfitter clamp jaw','Die-cast cobra housing',.0003),('Tempered optical glass','Compressed optics gasket',.0002),('Compressed optics gasket','Die-cast cobra housing',.0003),('Folded optical reflector','Optics retaining rail',.0005),('Folded optical reflector.001','Optics retaining rail.001',.0005),('LED phosphor emitter','Ceramic LED support',.0002),('LED phosphor emitter.001','Ceramic LED support.001',.0002),('Ceramic LED support','Die-cast cobra housing',.0003),('Ceramic LED support.001','Die-cast cobra housing',.0003)]
SHOTS={
'hero_closed':dict(location=(8,-12,7.8),target=(0,-.65,4.15),lens=60,aspect=.8,emission_scale=0),
'front':dict(location=(0,-20,4),target=(0,-.8,4),ortho=8,aspect=.8,emission_scale=0),
'side':dict(location=(20,0,4),target=(0,-.8,4),ortho=8,aspect=.8,emission_scale=0),
'back':dict(location=(0,20,4),target=(0,-.8,4),ortho=8,aspect=.8,emission_scale=0),
'top':dict(location=(0,-1,20),target=(0,-1,4),ortho=3,aspect=1,emission_scale=0),
'controls':dict(location=(.66,-2.95,7.30),target=(0,-2.08,7.80),lens=65,aspect=1.2,emission_scale=0),
'casting':dict(location=(.70,-1.05,.82),target=(0,0,.32),lens=65,aspect=1.2,emission_scale=0),
'lit':dict(location=(.40,-2.75,7.30),target=(0,-2.10,7.78),lens=60,aspect=1.2,emission_scale=1,exposure=-1.5),
'scale':dict(location=(8.7,-13,8.2),target=(-.35,-.65,3.9),lens=60,aspect=.8,human=True,emission_scale=0)}
SHOTS['hero_open']=SHOTS['hero_closed']
EXTRA_SHOTS=['lit']
