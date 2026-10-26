"""One reusable family atlas; module budgets are enforced independently."""
BUDGETS={'Table':4000,'Chair':3000,'Chaise':4000,'Umbrella_Open':4000,'Umbrella_Closed':4000}
ATLAS_SETS=tuple(BUDGETS)
BOUNDS={
 'Table':dict(size=(1.524,.9652,.763),tolerance=(.002,.002,.002)),
 'Chair':dict(size=(.652,.72,.959),tolerance=(.005,.015,.005)),
 'Chaise':dict(size=(.72,2.108,.423),tolerance=(.01,.02,.01)),
 'Umbrella_Open':dict(size=(2.756,2.756,2.565),tolerance=(.015,.015,.001)),
 'Umbrella_Closed':dict(size=(.5,.5,2.565),tolerance=(.001,.001,.001)),
}
UV_DENSITY_BANDS=dict(reference_size=2048,p5_min=160,median_min=220,median_max=440,p95_max=1100)
UV_PRIORITY={'Chair continuous':1.3,'Chaise fixed sling':1.15,'Chaise hinged sling':1.15,'Open eight-panel':1.1,'Closed gathered':1.1}
UV_DEFAULT_PRIORITY=.85
UV_MIN_COVERAGE=.35
UV_SMART_ASPECT=False
UV_SMART_ANGLE=40
REQUIRED_NODES=('Table','Chair','Chaise','Chaise_Backrest','Chaise_Lock_L','Chaise_Lock_R','Umbrella_Open','Umbrella_Closed','Open_Crank','Closed_Crank')
BAKE_POLICY=dict(isolate_moving=True,moving_roots=list(REQUIRED_NODES),cage_m=.0035,ray_distance_m=.014,ao_distance_m=.025)
MOTIONS=[dict(node='Chaise_Backrest',axis='X',range=[0,65],step=2,tolerance_m=.0005,allow=[
 dict(moving='Chaise rotating hinge boss',fixed='Chaise hinge chassis bracket',reason='Clampable hinge axle joint'),
 dict(moving='Chaise rotating hinge boss',fixed='Chaise fixed hinge quadrant',reason='Intended coaxial hinge faces')]),
 dict(node='Open_Crank',axis='Y',range=[0,360],step=10,tolerance_m=.0005,allow=[dict(moving='Open crank',fixed='Open crank cast case',reason='Shaft rotates in crankcase bearing')]),
 dict(node='Closed_Crank',axis='Y',range=[0,360],step=10,tolerance_m=.0005,allow=[dict(moving='Closed crank',fixed='Closed crank cast case',reason='Shaft rotates in crankcase bearing')])]
STUDIO=dict(scale=2.0,light_center=(.4,0,0),backdrop_half_width=18)
# Original library chair plus three linked mesh copies gives four seats in the catalog.
DINING=dict(parts={'Chair':dict(translation=(1.02,-.97,0),rotation_degrees=(0,0,180)),
                   'Chaise_Backrest':dict(rotation_degrees=(45,0,0))},
 instances=[dict(source='Chair',name='Dining_Chair_2',location=(.43,-.97,0),rotation_degrees=(0,0,180)),
            dict(source='Chair',name='Dining_Chair_3',location=(-.43,.97,0)),
            dict(source='Chair',name='Dining_Chair_4',location=(.43,.97,0))],
 hide_assemblies=['Umbrella_Closed'])
ALL=['Table','Chair','Chaise','Umbrella_Open','Umbrella_Closed']
def solo(root):return dict(hide_assemblies=[x for x in ALL if x!=root])
SHOTS={
 'hero_closed':dict(location=(5,-7,4.4),target=(.55,0,1.08),lens=51,aspect=1.33,**DINING),
 'hero_open':dict(location=(3.5,-4.5,2.7),target=(.35,0,.51),lens=55,aspect=1.4,**{**DINING,'hide_assemblies':['Umbrella_Closed','Umbrella_Open']}),
 'front':dict(location=(.6,-8,1.3),target=(.6,0,1.3),ortho=4.65,aspect=1.35,**DINING),
 'side':dict(location=(8,0,1.3),target=(.6,0,1.3),ortho=3.6,aspect=1.1,**DINING),
 'back':dict(location=(.6,8,1.3),target=(.6,0,1.3),ortho=4.65,aspect=1.35,studio_yaw=180,**DINING),
 'top':dict(location=(.6,0,9),target=(.6,0,0),ortho=4.65,aspect=1.35,**DINING),
 'controls':dict(location=(-.36,-1.55,1.05),target=(-1.45,.02,.58),lens=58,aspect=1.2,**solo('Chair')),
 'casting':dict(location=(2.65,-.55,.9),target=(2.08,.48,.42),lens=65,aspect=1.25,parts={'Chaise_Backrest':dict(rotation_degrees=(45,0,0))},**solo('Chaise')),
 'canopy':dict(location=(1.7,-2.8,2.35),target=(0,0,2.15),lens=56,aspect=1.25,**solo('Umbrella_Open')),
 'closed':dict(location=(-1.3,-2.5,1.85),target=(-2.5,1,1.5),lens=65,aspect=.75,**solo('Umbrella_Closed')),
 'scale':dict(location=(5,-8,3.7),target=(.6,0,1.1),lens=51,aspect=1.33,human=True,**DINING),
}
TITLE='Larkspur / Terrace patio family'
EXTRA_SHOTS=['hero_open','canopy','closed']
MOTIONS += [dict(node='Chaise_Lock_'+side,axis='X',range=[0,360],step=15,tolerance_m=.0005) for side in ('L','R')]
