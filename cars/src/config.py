"""Delivery budget, bake/surface policy, measured motion and archived cameras."""
BUDGETS={'Pickup':60000}
BOUNDS={'Pickup':dict(size=(2.45872,5.89026,1.96088),tolerance=(.025,.002,.002))}
SHOTS={
 'front_three_quarter':dict(location=(8,-10,3.6),target=(0,-.10,.98),lens=57,aspect=1.6),
 'rear_three_quarter':dict(location=(-8,10,3.6),target=(0,.15,.96),lens=57,aspect=1.6,studio_yaw=180),
 'side':dict(location=(12,0,1),target=(0,0,1),ortho=6.7,aspect=2.0),
 'front':dict(location=(0,-12,1),target=(0,0,1),ortho=3.0,aspect=1.0),
 'top':dict(location=(0,0,12),target=(0,0,0),ortho=6.7,aspect=1.2,roll=1.5707963267948966),
 'stripes_front':dict(location=(7.5,-9.5,4.6),target=(0,-.1,1),lens=57,aspect=1.6),
 'stripes_side':dict(location=(-10,-2.0,3.7),target=(0,0,1),lens=57,aspect=1.8),
}
STUDIO=dict(scale=3,light_center=(0,0,0),backdrop_half_width=12)
# Full mechanical ranges; source BVH sweeps and imported articulation are checked.
MOTIONS=[]
for code in ['FL','FR','RL','RR']:
    MOTIONS.append(dict(node='Door_'+code,axis='Z',range=[0,72] if code.endswith('L') else [-72,0],step=2,tolerance_m=.0005))
MOTIONS += [dict(node='Hood',axis='X',range=[-62,0],step=2,tolerance_m=.0005),
            dict(node='Tailgate',axis='X',range=[-90,0],step=2,tolerance_m=.0005)]
for code in ['FL','FR','RL','RR']:
    MOTIONS.append(dict(node='Wheel_'+code,axis='X',range=[0,360],step=15,tolerance_m=.0005))
for code in ['FL','FR']:
    MOTIONS.append(dict(node='Steer_'+code,axis='Z',range=[-35,35],step=1,tolerance_m=.0005))

LOOKDEV_SHOTS={
 'front_three_quarter':dict(location=(8,-10,3.05),target=(0,-.12,.98),lens=57,aspect=1.6,studio_yaw=-35),
 'rear_three_quarter':dict(location=(-8,10,3.05),target=(0,.15,.96),lens=57,aspect=1.6,studio_yaw=145),
 'side':dict(location=(12,0,1.10),target=(0,0,1.10),ortho=6.65,aspect=2.0,studio_yaw=-25,exposure=-2.8),
 'front_detail':dict(location=(3.4,-6.8,2.25),target=(.12,-2.43,1.01),lens=77,aspect=1.45,studio_yaw=-35,paint='Graphite'),
 'wheel_detail':dict(location=(3.2,-3.55,1.05),target=(.87,-1.985,.51),lens=90,aspect=1.2,studio_yaw=-50),
 'lamps_lit':dict(location=(3.4,-6.8,2.25),target=(.12,-2.43,1.01),lens=77,aspect=1.45,studio_yaw=-35,lights=True,paint='Graphite'),
 'interior':dict(location=(1.9,-2.7,1.88),target=(-.06,-.24,1.13),lens=70,aspect=1.45,studio_yaw=-35),
 'face_plan':dict(location=(0,-2.40,7),target=(0,-2.40,0),ortho=2.50,aspect=1.45,paint='Graphite',studio_yaw=-35),
 'face_side':dict(location=(6,-2.52,1.05),target=(0,-2.52,1.05),ortho=1.45,aspect=1.45,paint='Graphite',studio_yaw=-35),
 'face_above':dict(location=(4.4,-3.8,2.8),target=(.18,-2.50,1.03),lens=85,aspect=1.45,paint='Graphite',studio_yaw=-35,exposure=-3.0),
}

# Intended rotating bearing and articulated suspension interfaces. These are
# local joints; neither tire/liner nor rotor/caliper interference is exempted.
for motion in MOTIONS:
    name=motion['node']
    if name.startswith('Wheel_'):
        code=name.removeprefix('Wheel_');sign=-1 if code.endswith('L') else 1
        motion['allow']=[dict(moving='Wheel center_'+code,fixed='Hub bearing spindle_'+code[0]+str(sign),reason='Rotating hub surrounds its fixed bearing spindle')]
    if name.startswith('Steer_'):
        code=name.removeprefix('Steer_');sign=-1 if code.endswith('L') else 1
        motion['allow']=[dict(moving=moving,fixed=fixed,reason='Articulated ball/CV joint at steering knuckle')
          for moving in ['Hub bearing spindle_F'+str(sign),'Steering knuckle_'+str(sign)]
          for fixed in ['Front wishbone_'+str(sign),'Steering tie rod_'+str(sign),'Front halfshaft '+str(sign)]]

# One shared three-map set. RGB is a correct Atlantic glTF fallback; paint
# alpha is neutral coverage. Runtime colors add coverage*(tint-reference) in
# linear light, preserving the source contamination instead of tinting it.
import json as _json
from pathlib import Path as _Path
import runpy as _runpy
_PAINT=_runpy.run_path(str(_Path(__file__).with_name('pickup_spec.py')))
MAX_MATERIALS=4
BAKE_BASECOLOR_ALPHA_CHANNEL='paint_coverage'
DELIVERY_SURFACES={
 'Paint':dict(principled={'Coat Weight':1,'Coat Roughness':.035},factors={'Metallic':.12},
    extras=dict(paint_decode='reference_plus_coverage_delta',paint_reference_color=list(_PAINT['COLORS']['Atlantic']),
                paint_colors=_json.dumps(_PAINT['COLORS']),paint_metallic=_json.dumps(_PAINT['PAINT_METAL']))),
 'Opaque':{},
 'Glass':dict(principled={'Transmission Weight':1,'IOR':1.5}),
 'Lamps':dict(emission_strength=80,extras=dict(lamp_strength=80,lamp_alpha_semantic='emission_strength_over_80')),
}
SOURCE_MATERIAL_SURFACES={
 'Alder '+name:'Opaque' for name in ['rubber','plastic','wheel','chrome','dark_chrome','bed','bumper','frame','brake','caliper','cloth','seat_side','interior','headliner','interior_light','turned rotor friction ring','tire left','tire right','red prismatic lens','mirror silver','original plate','original badge','original model','original grille','original display']}
SOURCE_MATERIAL_SURFACES['Alder factory paint']='Paint'
SOURCE_MATERIAL_SURFACES.update({'Alder '+name:'Glass' for name in ['clear windshield','front side glass','factory privacy glass','rear privacy glass','headlamp polycarbonate']})
SOURCE_MATERIAL_SURFACES.update({'Alder '+name:'Lamps' for name in ['white running signature','projector phosphor','red brake emitter','amber reflector']})
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['Door_FL','Door_FR','Door_RL','Door_RR','Hood','Tailgate',
  'Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR','Steer_FL','Steer_FR','Fuel_Door','Wiper_0','Wiper_1'],
  cage_m=.012,ray_distance_m=.035,ao_distance_m=.040,consolidate_attribute_sources=True)
# Nested transparent optics and thin relief prints cannot share projection
# rays with adjacent parts. The kit accepts exact mesh names as isolation
# roots too; only the bake moves them. Their exported geometry is untouched.
BAKE_POLICY['moving_roots'] += ['Windshield','Rear glass','Fictional plate_F','Fictional plate_R','Alder grille field']
for _side in ['L','R']:
    BAKE_POLICY['moving_roots'] += ['Headlamp envelope_'+str(-1 if _side=='L' else 1),
       'Projector optic_'+_side,'Projector emitter_'+_side,'Alder running signature_'+_side,
       'Headlamp reflector_'+_side,'Headlamp lateral reflector_'+_side]
    for _end in ['F','R']:
        BAKE_POLICY['moving_roots'] += ['Tire_'+_end+_side,'Wheel barrel_'+_end+_side,'Side glass_'+_end+_side]
UV_SMART_ASPECT=False
UV_DEFAULT_PRIORITY=.60
UV_PRIORITY={
 'Door skin':1.5,'Hood outer':1.5,'Front fender':1.4,'Fender shoulder':1.4,'Bed outer':1.4,'Tailgate outer':1.4,
 'Roof crown':1.2,'Fascia body':1.5,'Fascia shared':1.7,'Front bumper':1.4,'Rear bumper':1.3,
 'Headlamp':1.9,'Projector':1.7,'Alder running':1.9,'Alder grille':1.7,'Grille cavity':1.4,
 'Tire_':1.2,'Cast spoke':1.5,'Wheel center':1.5,'Wheel barrel':1.2,'Brake':1.2,
 'Fictional plate':2.5,'Alder front badge':2.5,'C150 fictional':2.5,'Tailgate Alder name':2.5,'Alder center':2.5,
 'Boxed frame':.30,'Frame ': .30,'Wheelwell':.50,'Cab floor':.45,'Pickup bed floor':.85,
 'Front seat':.9,'Front backrest':.9,'Dashboard':.9,'Steering ':1.1,'Inner door':.8,
}
UV_DENSITY_BANDS=dict(reference_size=2048,p5_min=35,median_min=100,median_max=400,p95_max=1200)
REQUIRED_NODES=['AlderC150','Hood','Tailgate','Door_FL','Door_FR','Door_RL','Door_RR',
 'Steer_FL','Steer_FR','Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR']
DELIVERY_BOUNDS=BOUNDS['Pickup']

UV_SMART_ANGLE=35
MOTIONS += [dict(node='Mirror_L',axis='Z',range=[-50,0],step=2,tolerance_m=.0005),
            dict(node='Mirror_R',axis='Z',range=[0,50],step=2,tolerance_m=.0005),
            dict(node='Fuel_Door',axis='Z',range=[0,95],step=2,tolerance_m=.0005),
            dict(node='Wiper_0',axis='Z',range=[-80,0],step=2,tolerance_m=.0005),
            dict(node='Wiper_1',axis='Z',range=[-80,0],step=2,tolerance_m=.0005)]

for _m in MOTIONS:
    if _m['node'].startswith('Mirror_'):
        _side=_m['node'][-1]
        _m['allow']=[dict(moving=prefix+_side,fixed='Mirror fixed base_'+_side,reason='Stationary hinge base enters the rotating mirror bearing') for prefix in ['Molded mirror shell_','Mirror support arm_']]
