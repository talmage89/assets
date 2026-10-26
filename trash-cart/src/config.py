"""Studio views, primary delivery envelope, and explicit atlas staging envelope."""
BUDGETS={'TrashCart':6000}
SOURCE_BUDGETS={'TrashCart':7600} # Includes both lids; each export contains one.
DELIVERY_BOUNDS={'size':(.75565,.9017,1.09855),'tolerance':(.003,.003,.003)}
# The second lid occupies atlas staging space, never delivery space.
BOUNDS={'TrashCart':{'size':(2.00565,.9017,1.09855),'tolerance':(.004,.004,.004)}}
REQUIRED_NODES=('TrashCart','Lid','Wheel_Left','Wheel_Right')
BAKE_DROP_MESHES=()
UV_PRIORITY={'Rotomolded':1.1,'trash crowned':1.1,'recycling crowned':1.1,'Wheel':.75,'Steel axle':.6,'Molded axle':.65}
UV_DEFAULT_PRIORITY=1
SHOTS={
 'hero_closed':dict(location=(2.1,-3.2,1.95),target=(0,0,.56),lens=78,aspect=1.05),
 'hero_open':dict(location=(2.2,-3.6,2.5),target=(0,.08,.85),lens=68,aspect=1.05,lid=-100),
 'front':dict(location=(0,-4,.55),target=(0,0,.55),ortho=1.25,aspect=1),
 'side':dict(location=(4,0,.55),target=(0,0,.55),ortho=1.25,aspect=1),
 'back':dict(location=(0,4,.55),target=(0,0,.55),ortho=1.25,aspect=1),
 'top':dict(location=(0,0,4),target=(0,0,.5),ortho=1.25,aspect=1),
 'controls':dict(location=(.8,-1.65,.98),target=(0,-.33,.60),lens=80,aspect=1.2),
 'hinge':dict(location=(.78,1.35,1.51),target=(.10,.33,1.01),lens=85,aspect=1.4),
 'wheel':dict(location=(1.12,.94,.48),target=(.27,.25,.18),lens=85,aspect=1.3),
 'scale':dict(location=(2.6,-4.8,2.1),target=(-.35,0,.88),lens=67,aspect=1.25,human=True),
}
for shot in SHOTS.values():shot['hide_assemblies']=['AtlasBlueLid']
