"""Privacy family delivery policy and views; +X along bays, −Y good side."""
BUDGETS={'WoodPrivacy':3000}  # Independent per-module 2k limits: check_construction.py.
BOUNDS={'WoodPrivacy':dict(size=(7.02895,.106,1.8808),tolerance=(.004,.008,.004))}
UV_DENSITY_BANDS=dict(reference_size=2048,p5_min=180,median_min=190,median_max=290,p95_max=650)
UV_PRIORITY={'Gate hinge':2.1,'Latch':2.1,'Gate latch':2.1,'Gate picket':1.25,'Gate compression':1.15}
UV_DEFAULT_PRIORITY=1.0
REQUIRED_NODES=('Section_A','Section_B','Post_End','Post_Line','Post_Corner','Gate_Bay','Gate','Latch',
                'Section_A__L','Section_A__R','Section_B__L','Section_B__R','Gate_Bay__L','Gate_Bay__R',
                'Post_End__connect_0','Post_Line__connect_0','Post_Line__connect_180',
                'Post_Corner__connect_90','Post_Corner__connect_180','Gate__free_edge')
BAKE_POLICY=dict(isolate_moving=False,moving_roots=[],cage_m=.002,ray_distance_m=.009,ao_distance_m=.04)
# Latch rotates about local Y in the negative direction to lift its free end.
MOTIONS=[dict(node='Latch',axis='Y',range=[-65,0],step=2,tolerance_m=.0003)]
ASSEMBLED=dict(parts={'Gate_Bay':{'translation':(-1.05995,0,0)}},hide_assemblies=['Post_Corner'])
SHOTS={
 'hero_closed':dict(location=(4.8,-10,3.4),target=(.37,0,.94),lens=52,aspect=1.85,**ASSEMBLED),
 'hero_open':dict(studio_yaw=180,location=(5.6,9,3.5),target=(.35,0,.95),lens=52,aspect=1.85,
                  parts={'Gate_Bay':{'translation':(-1.05995,0,0)},'Gate':{'rotation_degrees':(0,0,-72)},'Latch':{'rotation_degrees':(0,-65,0)}},hide_assemblies=['Post_Corner']),
 'front':dict(location=(-1.2192,-6,.96),target=(-1.2192,0,.96),ortho=2.75,aspect=1.35,hide_assemblies=['Section_B','Post_Corner','Gate_Bay']),
 'back':dict(location=(-1.2192,6,.96),target=(-1.2192,0,.96),ortho=2.75,aspect=1.35,hide_assemblies=['Section_B','Post_Corner','Gate_Bay']),
 'side':dict(location=(4,-.005,.96),target=(-1.2192,0,.96),ortho=2.3,aspect=1.1,hide_assemblies=['Section_B','Post_Corner','Gate_Bay']),
 'top':dict(location=(-1.2192,0,6),target=(-1.2192,0,.94),ortho=2.75,aspect=2.4,hide_assemblies=['Section_B','Post_Corner','Gate_Bay']),
 'grain':dict(location=(-.43,-.88,1.69),target=(-.63,-.028,1.57),lens=72,aspect=1.35,hide_assemblies=['Gate_Bay']),
 'joinery':dict(location=(.42,.77,1.91),target=(0,0,1.68),lens=70,aspect=1.35,hide_assemblies=['Gate_Bay']),
 'hardware':dict(location=(4.3,-1.05,1.58),target=(3.59,-.04,1.69),lens=65,aspect=1.35,hide_assemblies=['Section_A','Section_B','Post_End','Post_Line','Post_Corner']),
 'gate':dict(location=(5.9,-3.3,2.03),target=(4,0,.98),lens=60,aspect=1.1,hide_assemblies=['Section_A','Section_B','Post_End','Post_Line','Post_Corner']),
 'gate_back':dict(studio_yaw=180,location=(5.9,3.3,2.13),target=(4,0,.98),lens=60,aspect=1.1,hide_assemblies=['Section_A','Section_B','Post_End','Post_Line','Post_Corner']),
 'pieces':dict(location=(2.8,-11,4.4),target=(.95,0,.89),lens=52,aspect=2),
 'posts':dict(parts={'Post_End':{'translation':(1.9,0,0)},'Post_Corner':{'translation':(-1.9,0,0)}},location=(1.6,-3.5,1.9),target=(0,0,.93),lens=60,aspect=1.8,hide_assemblies=['Section_A','Section_B','Gate_Bay']),
 'scale':dict(location=(2,-7,2.5),target=(.25,0,.94),lens=55,aspect=1.5,human=True,parts={n:{'translation':(1.9,0,0)} for n in ('Section_A','Post_End','Post_Line')},
              hide_assemblies=['Section_B','Post_Corner','Gate_Bay']),
}

STUDIO=dict(light_scale=2.2,light_center=(.4,0,0))
for shot in SHOTS.values():shot.setdefault('exposure',-1.15)
SHOTS['corner_good']=dict(location=(5.8,-10,4.4),target=(.25,.62,.95),lens=55,aspect=1.8,exposure=-1.15)
SHOTS['corner_rails']=dict(studio_yaw=180,location=(-6.2,8.2,4.1),target=(.25,.62,.95),lens=55,aspect=1.8,exposure=-1.15)
SHOTS['pieces'].update(parts={
 'Section_A':{'translation':(-.4808,.8,0)},'Section_B':{'translation':(.4808,.8,0)},
 'Post_End':{'translation':(1.4384,-1.2,0)},'Post_Line':{'translation':(0,-1.2,0)},
 'Post_Corner':{'translation':(-1.4384,-1.2,0)},'Gate_Bay':{'translation':(.8,.8,0)}},
 location=(8.8,-13,6.8),target=(1.3,0,.9),lens=55)
