TITLE='Alder / size-1 curbside mailbox'
BUDGETS={'Mailbox':1800}
BOUNDS={'Mailbox':dict(size=(.1806,.5383,1.26965),tolerance=(.0005,.0005,.0005))}
# Shell is 165.1 x 482.6 x 215.9 mm; attachments and arm extend assembly bounds.
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['Door','Flag'],cage_m=.00045,ray_distance_m=.004,ao_distance_m=.025)
UV_SMART_ASPECT=False
UV_DENSITY_BANDS=dict(p5_min=220,median_min=350,median_max=950,p95_max=1500)
UV_PRIORITY={'Wood':.8,'Door stamped':1.35,'Flag':1.1}
REQUIRED_NODES=['Mailbox','Door','Flag']
CONTACTS=[('Wood notched 4x4 post','Wood half-lap arm',.0008),('Wood half-lap arm','Wood mounting board',.0008),('Wood mounting board','Pressed metal floor',.0008),('Bent galvanized shell','Pressed metal floor',.0005),('Bent galvanized shell','Seamed rear panel',.0005)]
MOTIONS=[dict(node='Door',axis='X',range=[0,105],step=1,tolerance_m=.00005,allow=[dict(moving='Door hinge ear',fixed='Fixed hinge pin',reason='Door ear captures coaxial end pin'),dict(moving='Door pull',fixed='Roof spring catch',reason='Elastic spring catch releases when pulled')]),dict(node='Flag',axis='X',range=[0,90],step=1,tolerance_m=.00005,allow=[dict(moving='Flag pivot cap',fixed='Flag nylon stand-off',reason='Coaxial pivot clamp surfaces')])]
SHOTS={
'hero_closed':dict(location=(1.2,-1.8,1.6),target=(0,0,.83),lens=65,aspect=1),
'hero_open':dict(location=(.85,-1.5,1.45),target=(0,-.02,1.12),lens=67,aspect=1.2,parts={'Door':dict(rotation_degrees=(105,0,0)),'Flag':dict(rotation_degrees=(90,0,0))}),
'front':dict(location=(0,-4,.66),target=(0,0,.66),ortho=1.55,aspect=1),
'side':dict(location=(4,0,.66),target=(0,0,.66),ortho=1.55,aspect=1),
'back':dict(location=(0,4,.66),target=(0,0,.66),ortho=1.55,aspect=1),
'top':dict(location=(0,0,4),target=(0,0,.8),ortho=.68,aspect=1),
'controls':dict(location=(.48,-.75,1.48),target=(0,-.10,1.16),lens=67,aspect=1.2),
'casting':dict(location=(.50,-.60,1.20),target=(0,.09,.98),lens=67,aspect=1.2),
'scale':dict(location=(2,-4,1.9),target=(-.35,0,.87),lens=60,aspect=1,human=True)}
EXTRA_SHOTS=['hero_open']

for shot in SHOTS.values():
    for key in ['location','target']:
        x,y,z=shot[key];shot[key]=(x,y-.20,z)
