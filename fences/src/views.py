"""Render-only framing and lighting; camera edits do not invalidate the atlas."""
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
 'posts':dict(parts={'Post_End':{'translation':(1.9,0,0)},'Post_Corner':{'translation':(-1.9,0,0)}},location=(1.6,-3.5,1.9),target=(0,0,.93),lens=60,aspect=1.1,hide_assemblies=['Section_A','Section_B','Gate_Bay']),
 'scale':dict(location=(2,-7,2.5),target=(.25,0,.94),lens=55,aspect=1.5,human=True,parts={n:{'translation':(1.9,0,0)} for n in ('Section_A','Post_End','Post_Line')},
              hide_assemblies=['Section_B','Post_Corner','Gate_Bay']),
}

STUDIO=dict(light_scale=2.2,light_center=(.4,0,0),backdrop_half_width=24)
for shot in SHOTS.values():shot.setdefault('exposure',-1.15)
SHOTS['corner_good']=dict(location=(5.8,-10,4.4),target=(.25,.62,.95),lens=55,aspect=1.8,exposure=-1.15)
SHOTS['corner_rails']=dict(studio_yaw=180,location=(-6.2,8.2,4.1),target=(.25,.62,.55),lens=45,aspect=1.8,exposure=-1.15)
SHOTS['pieces'].update(parts={
 'Section_A':{'translation':(-.4808,.8,0)},'Section_B':{'translation':(.4808,.8,0)},
 'Post_End':{'translation':(1.4384,-1.2,0)},'Post_Line':{'translation':(0,-1.2,0)},
 'Post_Corner':{'translation':(-1.4384,-1.2,0)},'Gate_Bay':{'translation':(.8,.8,0)}},
 location=(8.8,-13,6.8),target=(1.3,0,.9),lens=55)
