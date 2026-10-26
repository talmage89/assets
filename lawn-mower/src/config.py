"""Meadow 21 delivery policy; camera coordinates include footprint centering."""
BUDGETS={'Mower':15000}
BOUNDS={'Mower':dict(size=(.6088,1.5509,1.0565),tolerance=(.002,.004,.002))}
DELIVERY_BOUNDS=BOUNDS['Mower']
REQUIRED_NODES=('Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR','OperatorBail','HandleFold')
BAKE_DROP_MESHES=()
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR','HandleFold','OperatorBail'],cage_m=.0008,ray_distance_m=.008,ao_distance_m=.018)
UV_PRIORITY={'Deep drawn':1.6,'Pressed engine':1.4,'Recoil':1.5,'Sewn grass':1.3,'Molded bag top':1.2,'Tire':1.2,'Wheel dish':1.1,'Engine identification':2.5,'Deck warning backing':2.5}
UV_DEFAULT_PRIORITY=.85
UV_DENSITY_BANDS=dict(reference_size=2048,p5_min=200,median_min=450,median_max=1100,p95_max=2100)
TITLE='Cinder Works / Meadow 21'
SHOTS={
'hero_closed':dict(location=(1.95,-2.90,1.77),target=(0,-.02,.51),lens=65,aspect=1.20),
'front':dict(location=(0,-4,.53),target=(0,0,.53),ortho=1.80,aspect=1.2),
'side':dict(location=(4,0,.53),target=(0,0,.53),ortho=1.85,aspect=1.2),
'back':dict(location=(0,4,.53),target=(0,0,.53),ortho=1.80,aspect=1.2,studio_yaw=180),
'top':dict(location=(0,0,4),target=(0,0,0),ortho=2.02,aspect=1.2),
'engine':dict(location=(.68,-1.36,.84),target=(0,-.43,.32),lens=66,aspect=1.3),
'bag':dict(location=(.93,.80,1.50),target=(0,.24,.44),lens=60,aspect=1.3,studio_yaw=120),
'underside':dict(location=(.65,1.30,1.10),target=(0,.25,.58),lens=65,aspect=1.3,studio_yaw=180,parts={'LawnMower':dict(rotation_degrees=(140,0,0),translation=(0,0,.9))}),
'folded':dict(location=(1.60,-2.1,1.55),target=(0,-.13,.44),lens=65,aspect=1.25,lid=135,hide=['ServiceSpans']),
'bail_held':dict(location=(.65,1.45,1.60),target=(0,.67,.99),lens=64,aspect=1.3,studio_yaw=90,parts={'OperatorBail':dict(rotation_degrees=(-64.5,0,0))}),
'scale':dict(location=(2.6,-4.2,2.0),target=(-.40,0,.80),lens=60,aspect=1.25,human=True),
}
CONTACTS=[('Cast crankcase sump','Engine raised mounting pad 0',.001),('Lower handle tube','Lower handle deck bracket',.001),('Bag mouth hook','Rear bag retaining cross pin',.0035),('Bag top support rod','Bag mouth hook',.001),('Wheel outrigger shelf FL','Deep drawn 2mm deck with rolled hem',.0005),('Wheel outrigger return FL','Axle height carrier FL',.0005)]
CONTACTS += [('Blade upturned sail L','21 inch mulching blade',.0005),('Blade upturned sail R','21 inch mulching blade',.0005)]
MOTIONS=[]
for k in ('FL','FR','RL','RR'):
 MOTIONS.append(dict(node='Wheel_'+k,axis='X',range=[0,360],step=30,tolerance_m=.0005,allow=[dict(moving='Wheel dish '+k,fixed='Wheel axle '+k,reason='Axle is supported in molded hub bore')]))
MOTIONS += [dict(node='OperatorBail',axis='X',range=[-64.5,0],step=2,tolerance_m=.0005,allow=[dict(moving='Operator presence',fixed='Bail pivot rivet',reason='Bail pivot hooked around rivet'),dict(moving='Operator presence',fixed='Bail pivot boss',reason='Rod seats in molded pivot bearing')]),dict(node='HandleFold',axis='X',range=[0,135],step=3,tolerance_m=.0005,exclude_fixed=['Lower brake cable service loop','Lower handle brake sheath'],allow=[dict(moving='Upper folding',fixed='Lower handle tube',reason='Clamped tube lap at the loosened folding hinge'),dict(moving='Upper folding',fixed='Fold joint bolt',reason='Fold bolt is transverse pivot pin')])]
# Common kit preview names expose the same source cameras.
SHOTS['hero_open']=SHOTS['folded']
SHOTS['controls']=SHOTS['engine']

CONTACTS += [('Brake cable wrap clip 0','Upper brake cable sheath',.0005),('Brake cable wrap clip 1','Upper brake cable sheath',.0005),('Brake cable lower wrap clip','Lower handle brake sheath',.0005),('Engine brake cable bracket','Cast crankcase sump',.0005),('Brake sheath ferrule','Engine brake cable bracket',.0005)]
