"""All final shots import the GLB; inspection staging matches privacy."""
HIDE=['Picket_B','Picket_Corner','Picket_GateBay']
ONLY_GATE=['Picket_A','Picket_B','Picket_End','Picket_Line','Picket_Corner']
ASSEMBLED=dict(parts={'Picket_GateBay':{'translation':(-1.05995,0,0)}},hide_assemblies=['Picket_Corner'])
SHOTS={
'hero_closed':dict(location=(4.7,-9,2.6),target=(.35,0,.57),lens=52,aspect=1.9,**ASSEMBLED),
'hero_open':dict(location=(4.8,8.5,3.1),target=(.35,0,.58),lens=52,aspect=1.9,studio_yaw=180,hide_assemblies=['Picket_Corner'],parts={'Picket_GateBay':{'translation':(-1.05995,0,0)},'Picket_Gate':{'rotation_degrees':(0,0,-65)},'Picket_Gate_Latch':{'rotation_degrees':(0,-65,0)}}),
'front':dict(location=(-1.2192,-5,.6),target=(-1.2192,0,.6),ortho=2.75,aspect=1.9,hide_assemblies=HIDE),
'back':dict(location=(-1.2192,5,.6),target=(-1.2192,0,.6),ortho=2.75,aspect=1.9,hide_assemblies=HIDE,studio_yaw=180),
'side':dict(location=(3,-.01,.6),target=(-1.2192,0,.6),ortho=1.45,aspect=1.1,hide_assemblies=HIDE),
 'top':dict(location=(-1.2192,0,5),target=(-1.2192,0,.6),ortho=2.75,aspect=2.2,hide_assemblies=HIDE),
'paint':dict(location=(-1.7,-1,.48),target=(-1.55,-.028,.26),lens=70,aspect=1.25,hide_assemblies=['Picket_GateBay']),
'joinery':dict(location=(.45,.85,1.4),target=(0,0,.92),lens=65,aspect=1.25,studio_yaw=180,hide_assemblies=['Picket_GateBay']),
'hardware':dict(location=(3.95,-1.2,1.2),target=(3.59,-.04,.89),lens=70,aspect=1.3,hide_assemblies=ONLY_GATE),
'gate':dict(location=(5.8,-3,1.7),target=(4,0,.60),lens=65,aspect=1.1,hide_assemblies=ONLY_GATE),
'gate_back':dict(location=(5.8,3,1.7),target=(4,0,.60),lens=65,aspect=1.1,studio_yaw=180,hide_assemblies=ONLY_GATE),
'pieces':dict(location=(8,-12,5.5),target=(1,0,.5),lens=55,aspect=2,parts={'Picket_A':{'translation':(-.48,.8,0)},'Picket_B':{'translation':(.48,.8,0)},'Picket_GateBay':{'translation':(.8,.8,0)},'Picket_End':{'translation':(1.4384,-1.2,0)},'Picket_Line':{'translation':(0,-1.2,0)},'Picket_Corner':{'translation':(-1.4384,-1.2,0)}}),
'posts':dict(location=(1.25,-3,1.6),target=(0,0,.6),lens=65,aspect=1.2,hide_assemblies=['Picket_A','Picket_B','Picket_GateBay'],parts={'Picket_End':{'translation':(1.9,0,0)},'Picket_Corner':{'translation':(-1.9,0,0)}}),
'scale':dict(location=(2,-6,2.4),target=(.25,0,.9),lens=55,aspect=1.5,human=True,parts={n:{'translation':(1.9,0,0)} for n in ['Picket_A','Picket_End','Picket_Line']},hide_assemblies=HIDE),
}
for s in SHOTS.values():s.setdefault('exposure',-1.15)
STUDIO=dict(light_scale=2.2,light_center=(.4,0,0),backdrop_half_width=24,backdrop_color=(.16,.18,.17))

SHOTS["corner_good"]=dict(location=(5.8,-9,3.4),target=(.2,.6,.57),lens=55,aspect=1.9,exposure=-1.15)
SHOTS["corner_rails"]=dict(location=(-6.2,8.2,3.2),target=(.2,.6,.45),lens=45,aspect=1.9,studio_yaw=215,exposure=-1.15)
