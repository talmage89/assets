"""H120-only checkpoint motion, atlas and export settings."""
import json,runpy
from pathlib import Path
family=runpy.run_path(str(Path(__file__).with_name('config.py')))
for key in ['DELIVERY_SURFACES','SOURCE_MATERIAL_SURFACES','MAX_MATERIALS','BAKE_BASECOLOR_ALPHA_CHANNEL','UV_SMART_ASPECT','UV_DENSITY_BANDS']:
    globals()[key]=family[key].copy() if isinstance(family[key],dict) else family[key]
colors=runpy.run_path(str(Path(__file__).with_name('hatch_colors.py')))
DELIVERY_SURFACES['Paint']=dict(DELIVERY_SURFACES['Paint'])
DELIVERY_SURFACES['Paint']['extras']=dict(DELIVERY_SURFACES['Paint']['extras'],paint_colors=json.dumps(colors['COLORS']),paint_metallic=json.dumps(colors['PAINT_METAL']))
# Family's documented North-American five-color selection, normalized only here.
COLOR_WEIGHTS=dict(Porcelain=31/89,Carbon=19/89,Graphite=21/89,Aluminum=8/89,Atlantic=10/89)
DELIVERY_SURFACES['Paint']['extras']['factory_spawn_weights']=json.dumps(COLOR_WEIGHTS)
BUDGETS={'Hatch':60000}
BOUNDS={'Hatch':dict(size=(2.0393,4.3630,1.5050),tolerance=(.004,.004,.004))}
DELIVERY_BOUNDS=BOUNDS['Hatch']
SOURCE_MATERIAL_SURFACES.update({
 'H120 cast alloy':'Opaque','H120 dealer insert':'Opaque','H120 grille lattice':'Opaque','H120 gloss black grille':'Opaque','H120 original model':'Opaque',
 'H120 red lamp cover':'Glass','H120 windshield':'Glass','H120 front door glass':'Glass','H120 rear door glass':'Glass','H120 backlight':'Glass',
 'H120 lettered tire L':'Opaque','H120 lettered tire R':'Opaque',
})
REQUIRED_NODES=['AlderH120','Door_FL','Door_FR','Door_RL','Door_RR','Hood','Liftgate','Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR','Steer_FL','Steer_FR']
MOTIONS=[]
for code in ['FL','FR','RL','RR']:
    limit=62 if code.startswith('F') else 66
    MOTIONS.append(dict(node='Door_'+code,axis=[-.10 if code.endswith('L') else .10,0,1],range=[0,limit] if code.endswith('L') else [-limit,0],step=2,tolerance_m=.0005))
for name,limits,label in [('Hood',[-62,0],'hood'),('Liftgate',[0,82],'gate')]:
    MOTIONS.append(dict(node=name,axis='X',range=limits,step=2,tolerance_m=.0005,
        allow=[dict(moving='H120 '+label+' support '+side+' telescoping rod',fixed='H120 '+label+' support '+side+' telescoping sleeve',reason='Chrome rod telescopes inside the hollow gas spring cylinder') for side in ['L','R']]))
for code in ['FL','FR','RL','RR']:
    MOTIONS.append(dict(node='Wheel_'+code,axis='X',range=[0,360],step=10,tolerance_m=.0005))
for code in ['FL','FR']:
    sign=-1 if code.endswith('L') else 1
    MOTIONS.append(dict(node='Steer_'+code,axis='Z',range=[-35,35],step=1,tolerance_m=.0005,
        allow=[dict(moving='H120 bearing front'+str(sign),fixed=other+str(sign),reason=reason) for other,reason in [
            ('H120 halfshaft ','Articulated CV ball inside the rotating knuckle bearing'),
            ('H120 front lower arm ','Ball joint centered on the authored kingpin axis'),
            ('H120 front damper ','Strut and knuckle clamp on the kingpin axis')]]))
UV_DEFAULT_PRIORITY=.50
UV_PRIORITY={'Door ':1.5,'Hood outer':1.5,'Front fender':1.4,'Rear quarter':1.4,'Front molded fascia':1.5,'Rear molded fascia':1.3,
 'Roof':1.2,'Liftgate':1.4,'Headlamp':1.8,'Taillamp':1.8,'H120 upper light':2.5,'H120 lower light':2.5,
 'Tire_':2.5,'Cast spoke':1.6,'Wheel center':1.8,'H120 original':4.0,'H120 dealer':5.0,'Alder center cap':5.0,
 'H120 headliner':.25,'H120 stamped floor':.25,'H120 cargo':.6}
UV_SMART_ANGLE=35
UV_PACK_SHAPE='CONCAVE'
UV_NORMALIZE_ISLAND_SCALE=True
counts=Path(__file__).resolve().parents[1]/'build/hatch-detail/game.counts.json'
BAKE_POLICY=dict(isolate_moving=True,moving_roots=sorted(json.loads(counts.read_text())['meshes']) if counts.exists() else REQUIRED_NODES[1:],
 cage_m=.014,ray_distance_m=.040,ao_distance_m=.030,consolidate_attribute_sources=True)
