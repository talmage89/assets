"""Delivery, surface, motion and studio policy for the Evening 89."""
BUDGETS={'Heater':15000}
BOUNDS={'Heater':dict(size=(.8382,.8382,2.2606),tolerance=(.001,.001,.001))}
DELIVERY_BOUNDS=BOUNDS['Heater']
REQUIRED_NODES=('tank_socket','regulator_attach','TankDoor','ControlKnob','TransportWheel_L','TransportWheel_R')
EXCLUDED_NODES=('Tank','TankCollision','Cylinder welded steel vessel','OPD forged brass valve body')
BAKE_DROP_MESHES=('Control legends print','Maker badge print')
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['TankDoor','ControlKnob','TransportWheel_L','TransportWheel_R'],cage_m=.0005,ray_distance_m=.003,ao_distance_m=.025)
MATERIAL_OVERRIDES={'Emitter perforated':dict(emission_strength=7,emission_tint=(1,.12,.008))}
UV_PRIORITY={'Control graphic':2.7,'Maker badge':2.5,'Emitter perforated':1.8,'Reflector':1.0,'Curved tank':1.3,'Hollow 3':1.2,'Static LPG':1.4}
UV_DEFAULT_PRIORITY=.8
UV_DENSITY_BANDS=dict(reference_size=2048,p5_min=200,median_min=450,median_max=1000,p95_max=1900)
STUDIO=dict(scale=1.7,backdrop_height=14)
TITLE='Cinder Works / Evening 89'
SHOTS={
 'hero_closed':dict(location=(1.95,-3.4,2.5),target=(0,0,1.13),lens=66,aspect=.80),
 'hero_open':dict(location=(1.7,-3,1.25),target=(0,0,.43),lens=70,aspect=1.15,lid=-105),
 'front':dict(location=(0,-5,1.13),target=(0,0,1.13),ortho=2.65,aspect=1.0),
 'side':dict(location=(5,0,1.13),target=(0,0,1.13),ortho=2.65,aspect=1.0),
 'back':dict(location=(0,5,1.13),target=(0,0,1.13),ortho=2.65,aspect=1.0,studio_yaw=180),
 'top':dict(location=(0,0,5),target=(0,0,0),ortho=1.05,aspect=1),
 'controls':dict(location=(.32,-.8,1.88),target=(0,-.02,1.735),lens=72,aspect=1.3),
 'burner':dict(location=(.72,-1.16,2.13),target=(0,0,2.035),lens=68,aspect=1.3),
 'casting':dict(location=(.64,-.94,2.65),target=(0,0,2.21),lens=62,aspect=1.3),
 'scale':dict(location=(3.5,-7,3),target=(-.40,0,1.1),lens=68,aspect=1.1,human=True),
 'fit_check':dict(location=(.95,-1.5,.92),target=(0,-.01,.40),lens=66,aspect=1.25,lid=-105,fit_reference=True),
 'lit':dict(location=(.72,-1.16,1.98),target=(0,0,2.035),lens=68,aspect=1.3,emission_scale=1,exposure=-1.0),
}
for n,s in SHOTS.items():s.setdefault('emission_scale',0)
EXTRA_SHOTS=['hero_open','burner','lit','fit_check']
MOTIONS=[dict(node='TankDoor',axis='Z',range=[-105,0],step=3,tolerance_m=.0005,allow=[
 dict(moving='Door hinge sleeve',fixed='Fixed hinge pin',reason='Hinge pin inside the bored sleeve'),
 dict(moving='Door hinge leaf',fixed='Fixed hinge pin',reason='Leaf welded to sleeve at pin axis'),
]) ,dict(node='ControlKnob',axis='Y',range=[-135,0],step=5,tolerance_m=.0004,allow=[])]
for side in ('L','R'):
    MOTIONS.append(dict(node='TransportWheel_'+side,axis='X',range=[0,360],step=15,tolerance_m=.0005,allow=[dict(moving='Transport wheel',fixed='Wheel axle',reason='Axle in wheel bore'),dict(moving='Wheel molded',fixed='Wheel axle',reason='Axle in molded hub bore')]))
CONTACTS=[('Hollow 3 inch post','Pole lower flange',.0002),('Control sleeve','Post upper socket',.0002),('Burner air mixing bowl','Control sleeve',.0002),('Reflector support stud 0','Burner top closure',.0002)]

CONTACTS += [('Reflector support stud 0','Reflector shallow crown cap',.0002),
 ('Reflector stand off washer 0','Reflector shallow crown cap',.0003),
 ('Guard radial mount 0 0','Rolled emitter retaining band',.0002),
 ('Guard radial mount 1 0','Burner top closure',.0002),
 ('Wheel mounting ear','Stamped weighted base pan',.0002),
 ('Internal stanchion 0','Tank support floor',.0002),
 ('Internal stanchion 1','Tank support floor',.0002),
 ('Internal stanchion 2','Tank support floor',.0002)]
