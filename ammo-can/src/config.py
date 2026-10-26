TITLE='Alder Creek / .50 caliber steel ammo can'
STUDIO=dict(backdrop_half_width=30)
BUDGETS={'AmmoCan':3000}
BOUNDS={'AmmoCan':{'size':(.1548,.3056,.1905),'tolerance':(.002,.002,.003)}}
DELIVERY_BOUNDS={'size':(.1548,.3056,.1905),'tolerance':(.002,.002,.003)}
REQUIRED_NODES=('AmmoCan','Lid','Latch','Handle')
UV_DENSITY_BANDS=dict(reference_size=1024,p5_min=350,median_min=550,median_max=1400,p95_max=1800)
UV_PRIORITY={'Hollow stamped':1.1,'Hemmed cover':1.05,'Continuous retained':.7,'Secured rear':.65}
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['Lid','Latch','Handle'],cage_m=.0002,ray_distance_m=.004,ao_distance_m=.015)
# Lid clearance requires the cam to be released first; check_sequence.py stages it.
MOTIONS=[dict(node='Latch',axis='X',range=[0,-105],step=2,tolerance_m=.00025,allow=[dict(moving='Cam lever hinge sleeve',fixed='Cam latch retained pivot pin',reason='Pin inside working lever sleeve')]),dict(node='Handle',axis='Y',range=[0,-90],step=2,tolerance_m=.00025,allow=[dict(moving='Folding carrying handle wire',fixed='Handle retaining sleeve',reason='Coaxial wire stubs retained in rolled sleeve bores')])]
SHOTS={
'hero_closed':dict(location=(.70,-.82,.52),target=(0,0,.095),lens=78,aspect=1.2),
'hero_open':dict(location=(.75,-.95,.72),target=(0,.05,.305),lens=45,aspect=1.15,lid=-100,parts={'Latch':{'rotation_degrees':(-105,0,0)}}),
'front':dict(location=(0,-1,.095),target=(0,0,.095),ortho=.24,aspect=1),
'side':dict(location=(1,0,.095),target=(0,0,.095),ortho=.36,aspect=1.25),
'back':dict(location=(0,1,.095),target=(0,0,.095),ortho=.24,aspect=1),
'top':dict(location=(0,0,1),target=(0,0,.095),ortho=.35,aspect=1),
'controls':dict(location=(.27,-.48,.29),target=(0,-.143,.128),lens=85,aspect=1.25),
'casting':dict(location=(.32,.40,.31),target=(.02,.145,.176),lens=85,aspect=1.25),
'handle':dict(location=(.36,-.38,.46),target=(0,0,.19),lens=85,aspect=1.25,parts={'Handle':{'rotation_degrees':(0,-75,0)}}),
'scale':dict(location=(2.2,-4.0,1.85),target=(-.4,0,.82),lens=67,aspect=1.25,human=True),
}
EXTRA_SHOTS=['hero_open','handle']
CONTACTS=[
('Continuous retained rubber gasket','Hollow stamped casing and folded mouth',.00015),
('Continuous retained rubber gasket','Stamped gasket retainer and inner lip',.00015),
('Stamped gasket retainer and inner lip','Hemmed cover pan with relieved rear skirt',.00015),
('Stamped cam latch plate with inspection hole','Body welded hasp reaction seat',.00015),
('Stamped cam latch plate with inspection hole','Cam hinge folded neck',.00015),
('Cam hinge folded neck','Cam lever hinge sleeve',.0003),
('Cam pull bail','Stamped cam latch plate with inspection hole',.00015),
('Cam lever hinge sleeve','Cam latch retained pivot pin',.0004),
]
for s in (-1,1):
 CONTACTS.extend([('Rear body hinge mounting leaf '+str(s),'Hollow stamped casing and folded mouth',.0002),('Body rear hinge sleeve '+str(s),'Rear body hinge mounting leaf '+str(s),.0002),('Cover rear hinge hook '+str(s),'Cover rear hinge leaf '+str(s),.0002),('Cover rear hinge hook '+str(s),'Secured rear hinge pin',.0004)])
for y in (-.061,.061):
 CONTACTS.extend([('Handle mounting foot '+str(y),'Hemmed cover pan with relieved rear skirt',.00015),('Handle retaining sleeve '+str(y),'Handle mounting foot '+str(y),.00015),('Folding carrying handle wire','Handle retaining sleeve '+str(y),.0004)])
