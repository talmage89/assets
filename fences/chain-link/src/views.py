"""Library stages a terminal-line-terminal run and an independent reusable bay."""
ASSEMBLED=dict(parts={'Chain_GateBay':{'translation':(-.5170125,0,0)}},hide_assemblies=['Chain_Corner','Chain_Section'])
HIDE=['Chain_EndSection','Chain_Corner','Chain_GateBay','Chain_Section']
GATE=['Chain_Start','Chain_EndSection','Chain_Terminal','Chain_Line','Chain_Corner','Chain_Section']
SHOTS={
'hero_closed':dict(location=(5.4,-11,3),target=(.4,0,.65),lens=52,aspect=2,**ASSEMBLED),
'hero_open':dict(location=(5.4,10,3.4),target=(.4,0,.65),lens=52,aspect=2,studio_yaw=180,parts={'Chain_GateBay':{'translation':(-.5170125,0,0)},'Chain_Gate':{'rotation_degrees':(0,0,-65)},'Chain_ForkLatch':{'rotation_degrees':(0,-95,0)}},hide_assemblies=['Chain_Corner','Chain_Section']),
'front':dict(location=(-1.524,-6,.67),target=(-1.524,0,.67),ortho=3.4,aspect=2.2,hide_assemblies=HIDE),
'back':dict(location=(-1.524,6,.67),target=(-1.524,0,.67),ortho=3.4,aspect=2.2,hide_assemblies=HIDE,studio_yaw=180),
'side':dict(location=(4,-.01,.67),target=(-1.524,0,.67),ortho=1.6,aspect=1.1,hide_assemblies=HIDE),
 'top':dict(location=(-1.524,0,6),target=(-1.524,0,.6),ortho=3.4,aspect=2.4,hide_assemblies=HIDE),
'mesh':dict(location=(-1.05,-.90,1.0),target=(-1.33,-.034,.82),lens=65,aspect=1.3,hide_assemblies=['Chain_GateBay','Chain_Section']),
'hardware':dict(location=(3.77,-1.05,1.4),target=(3.62,-.04,1.06),lens=70,aspect=1.25,hide_assemblies=GATE),
'joinery':dict(location=(-2.62,-1.0,1.5),target=(-3.048,-.025,1.12),lens=65,aspect=1.3,hide_assemblies=['Chain_GateBay','Chain_Section']),
'gate':dict(location=(5.9,-3.4,1.9),target=(4.1,0,.66),lens=65,aspect=1.1,hide_assemblies=GATE),
'gate_back':dict(location=(5.9,3.4,1.9),target=(4.1,0,.66),lens=65,aspect=1.1,studio_yaw=180,hide_assemblies=GATE),
'pieces':dict(location=(10,-15,6),target=(1,0,.6),lens=55,aspect=2.1,parts={'Chain_Start':{'translation':(-.4,.6,0)},'Chain_EndSection':{'translation':(.4,.6,0)},'Chain_Section':{'translation':(0,1.5,0)},'Chain_Terminal':{'translation':(2.0,-1,0)},'Chain_Line':{'translation':(0,-1,0)},'Chain_Corner':{'translation':(-2,-1,0)},'Chain_GateBay':{'translation':(1,.6,0)}}),
'posts':dict(location=(1.3,-3,1.7),target=(0,0,.65),lens=65,aspect=1.2,hide_assemblies=['Chain_Start','Chain_EndSection','Chain_Section','Chain_GateBay'],parts={'Chain_Terminal':{'translation':(2.5,0,0)},'Chain_Corner':{'translation':(-2.5,0,0)}}),
'scale':dict(location=(2,-6,2.6),target=(.3,0,.9),lens=52,aspect=1.65,human=True,parts={n:{'translation':(2.15,0,0)} for n in ('Chain_Start','Chain_Terminal','Chain_Line')},hide_assemblies=HIDE),
}
for s in SHOTS.values():s.setdefault('exposure',-.9)
STUDIO=dict(light_scale=2.4,light_center=(.4,0,0),backdrop_half_width=26,backdrop_color=(.065,.080,.075))

# Inspection-only modules are hidden in the assembled and detail views.
for name,shot in SHOTS.items():
 if name not in ('pieces','posts'):
  shot.setdefault('hide_assemblies',[]).extend(['Chain_BetweenTerminals','Chain_Terminal_End'])
SHOTS['pieces']['parts']['Chain_BetweenTerminals']={'translation':(0,1,0)}
SHOTS['posts']['parts']['Chain_Terminal_End']={'translation':(-1.75,-2,0)}
SHOTS['posts']['hide_assemblies'].append('Chain_BetweenTerminals')
SHOTS['corner_good']=dict(location=(6.4,-10,3.8),target=(.3,.7,.65),lens=52,aspect=1.9,exposure=-.9)
SHOTS['corner_rails']=dict(location=(-6.8,9.5,3.7),target=(.3,.6,.55),lens=44,aspect=1.9,studio_yaw=215,exposure=-.9)
