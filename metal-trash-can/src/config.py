BUDGETS={'MetalTrashCan':5000}
BOUNDS={'MetalTrashCan':{'size':(.564,.5334,.75565),'tolerance':(.008,.004,.003)}}
DELIVERY_BOUNDS={'size':(.564,.5334,.75565),'tolerance':(.008,.004,.003)}
REQUIRED_NODES=('MetalTrashCan','Lid','Handle_Left','Handle_Right')
UV_PRIORITY={'Corrugated':1.0,'Pressed removable':1.05}
SHOTS={
'hero_closed':dict(location=(1.5,-2.4,1.3),target=(0,0,.38),lens=80,aspect=1.1),
'hero_open':dict(location=(1.5,-2.4,1.6),target=(0,0,.52),lens=68,aspect=1.1,parts={'Lid':{'translation':(0,0,.25)}}),
'front':dict(location=(0,-3,.38),target=(0,0,.38),ortho=.88,aspect=1),
'side':dict(location=(3,0,.38),target=(0,0,.38),ortho=.88,aspect=1),
'back':dict(location=(0,3,.38),target=(0,0,.38),ortho=.88,aspect=1),
'top':dict(location=(0,0,3),target=(0,0,.3),ortho=.70,aspect=1),
'controls':dict(location=(.6,-1,1.2),target=(0,0,.72),lens=85,aspect=1.3),
'interior':dict(location=(1.15,-1.4,1.8),target=(0,0,.36),lens=80,aspect=1.15,hide_assemblies=['Lid']),
'handle':dict(location=(1.05,-.55,.83),target=(.255,0,.62),lens=85,aspect=1.25),
'scale':dict(location=(2.6,-4.8,2),target=(-.35,0,.85),lens=67,aspect=1.25,human=True),
}
UV_DENSITY_BANDS=dict(reference_size=1024,p5_min=250,median_min=300,median_max=700,p95_max=900)
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['Lid','Handle_Left','Handle_Right'],cage_m=.0002,ray_distance_m=.004,ao_distance_m=.025)
MOTIONS=[dict(node='Lid',kind='translation',axis='Z',range=[0,.6],step=.01,tolerance_m=.0005)]
for label,s in [('Left',1),('Right',-1)]:
 MOTIONS.append(dict(node='Handle_'+label,axis='Y',range=[0,s*95],step=2,tolerance_m=.0004,allow=[dict(moving=label+' folding wire',fixed=label+' rolled bracket eye',reason='Retained wire ends rotate inside the mounting eye bore')]))
