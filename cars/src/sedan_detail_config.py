"""S240 detail delivery policy; the pickup configuration is read without edits."""
import runpy
from pathlib import Path
_family=runpy.run_path(str(Path(__file__).with_name('config.py')))
for _key in ['DELIVERY_SURFACES','SOURCE_MATERIAL_SURFACES','MAX_MATERIALS','BAKE_BASECOLOR_ALPHA_CHANNEL','UV_SMART_ASPECT','UV_SMART_ANGLE','UV_DENSITY_BANDS']:
    globals()[_key]=_family[_key].copy() if isinstance(_family[_key],dict) else _family[_key]
_colors=runpy.run_path(str(Path(__file__).with_name('sedan_colors.py')))
DELIVERY_SURFACES['Paint']['extras']=dict(DELIVERY_SURFACES['Paint']['extras'],paint_colors=__import__('json').dumps(_colors['COLORS']),paint_metallic=__import__('json').dumps(_colors['PAINT_METAL']))
# Axalta 2025 North America: white31, gray21, black19, blue10, silver8.
# Normalize these five choices only; not a claim about used-car fleet shares.
COLOR_WEIGHTS={name:value/89 for name,value in [('Porcelain',31),('Carbon',19),('Graphite',21),('Aluminum',8),('Atlantic',10)]}
DELIVERY_SURFACES['Paint']['extras']['factory_spawn_weights']=__import__('json').dumps(COLOR_WEIGHTS)
BUDGETS={'Sedan':62000}
BOUNDS={'Sedan':dict(size=(2.105,4.885,1.482),tolerance=(.006,.010,.003))}
DELIVERY_BOUNDS=BOUNDS['Sedan']
SOURCE_MATERIAL_SURFACES.update({
 'S240 cast alloy':'Opaque',
 'S240 dealer insert':'Opaque','S240 grille lattice':'Opaque','S240 gloss black grille':'Opaque',
 'S240 original model':'Opaque',
 'S240 red lamp cover':'Glass',
 'S240 windshield':'Glass','S240 front door glass':'Glass','S240 rear door glass':'Glass','S240 backlight':'Glass',
 'S240 lettered tire L':'Opaque','S240 lettered tire R':'Opaque','S240 tire L':'Opaque','S240 tire R':'Opaque',
})
UV_DEFAULT_PRIORITY=.32
UV_PRIORITY={'Door ':1.5,'Hood outer':1.5,'Front fender':1.4,'Rear quarter':1.4,'Front molded fascia':1.5,'Rear molded fascia':1.3,
 'Roof':1.2,'Trunk':1.4,'Headlamp':1.8,'Taillamp':1.8,'S240 optical':1.0,'S240 low ':1.7,'S240 high ':1.7,'S240 upper light':1.8,'S240 lower light':1.8,
 'Tire_':1.2,'Cast spoke':1.4,'Wheel center':1.5,'Wheel barrel':1.0,'S240 original':2.0,
 'S240 headliner':.25,'S240 stamped floor':.25,'S240 trunk tub':.25,'S240 engine':.4,'S240 seat':.6}
REQUIRED_NODES=['AlderS240','Door_FL','Door_FR','Door_RL','Door_RR','Hood','Trunk','Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR','Steer_FL','Steer_FR']
MOTIONS=[]
for _code in ['FL','FR','RL','RR']:
    MOTIONS.append(dict(node='Door_'+_code,axis=[-.14 if _code.endswith('L') else .14,0,1],range=[0,60 if _code.startswith('F') else 68] if _code.endswith('L') else [-60 if _code.startswith('F') else -68,0],step=2,tolerance_m=.0005))
MOTIONS.extend([dict(node='Hood',axis='X',range=[-62,0],step=2,tolerance_m=.0005,
    allow=[dict(moving='S240 telescoping rod',fixed='S240 telescoping sleeve',reason='Telescoping rod inside the gas-strut sleeve')]),
    dict(node='Trunk',axis='X',range=[0,72],step=2,tolerance_m=.0005,
    allow=[dict(moving='S240 trunk gooseneck',fixed='S240 trunk hinge bearing',reason='Gooseneck rotates in its bearing at the common axis')])])
for _code in ['FL','FR','RL','RR']:
    MOTIONS.append(dict(node='Wheel_'+_code,axis='X',range=[0,360],step=10,tolerance_m=.0005))
for _code in ['FL','FR']:
    _sign=-1 if _code.endswith('L') else 1
    MOTIONS.append(dict(node='Steer_'+_code,axis='Z',range=[-35,35],step=1,tolerance_m=.0005,
        allow=[dict(moving='S240 bearing front'+str(_sign),fixed='S240 halfshaft '+str(_sign),reason='Articulated CV joint inside the hub bearing'),
               dict(moving='S240 bearing front'+str(_sign),fixed='S240 front lower arm '+str(_sign),reason='Lower ball joint centered on the measured kingpin axis, represented by the composite knuckle housing'),
               dict(moving='S240 bearing front'+str(_sign),fixed='S240 front damper '+str(_sign),reason='Coaxial strut / knuckle clamp at the steering axis; composite bearing housing')]))
BAKE_POLICY=dict(isolate_moving=True,moving_roots=REQUIRED_NODES[1:]+[
 'Windshield','Backlight','Headlamp opening-1','Headlamp opening1','Tire_FL','Tire_FR','Tire_RL','Tire_RR'],
 cage_m=.008,ray_distance_m=.022,ao_distance_m=.030,consolidate_attribute_sources=True)
for _sign in [-1,1]:
    _cover='Headlamp opening'+str(_sign)
    BAKE_POLICY['moving_roots'] += ['S240 low '+_part+' '+_cover for _part in ['reflector','optic','phosphor']]
    for _lamp in [_cover,'Taillamp opening'+str(_sign)+' lid','Taillamp opening'+str(_sign)+' quarter']:
        BAKE_POLICY['moving_roots'] += ['S240 '+_row+' light guide '+_lamp for _row in ['upper','lower']]

# Convex packing prevents concave-packer sliver collisions between thin skins.
UV_SMART_ANGLE=45
UV_PACK_SHAPE='CONVEX'
# The sedan finalizer normalizes the connected outer charts after unwrapping.
# Preliminary SmartUV slivers can have zero projected area before that repair.
UV_NORMALIZE_ISLAND_SCALE=False

# Project each named manufactured part independently. Thin optical returns and
# skin backs must not receive a neighboring source's material or reverse normal.
import json as _json
_counts=Path(__file__).resolve().parents[1]/'build/sedan/detail-game.counts.json'
if _counts.exists():BAKE_POLICY['moving_roots']=sorted(_json.loads(_counts.read_text())['meshes'])
BAKE_POLICY.update(cage_m=.014,ray_distance_m=.040)
UV_PRIORITY['S240 upper light']=2.5
UV_PRIORITY['S240 lower light']=2.5

# Dense image sampling belongs to the visible sheet, not its hidden gauge back.
UV_PRIORITY_ATTRIBUTE='S240UVWeight'
UV_PRIORITY['Alder center cap']=3.0
UV_PRIORITY['Tire_']=1.6

UV_PRIORITY['Plate blank']=3.0
UV_PRIORITY['S240 model badge']=3.0


UV_PRIORITY.update({"Greenhouse":1.4,"Low wide grille":2.2,"Tire_":1.6})
