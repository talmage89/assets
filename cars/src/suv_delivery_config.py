"""X220 atlas and delivery policy, retaining the family's four shared surfaces."""
import copy,json,runpy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from suv_finishes import COLORS,PAINT_METAL,FLEET_WEIGHTS

_family=runpy.run_path(str(Path(__file__).with_name('config.py')))
for _name in ['DELIVERY_SURFACES','MAX_MATERIALS','BAKE_BASECOLOR_ALPHA_CHANNEL','UV_SMART_ASPECT','UV_DENSITY_BANDS']:
    globals()[_name]=copy.deepcopy(_family[_name])
DELIVERY_SURFACES['Paint']['extras'].update(paint_reference_color=list(COLORS['Atlantic']),paint_colors=json.dumps(COLORS),paint_metallic=json.dumps(PAINT_METAL),factory_spawn_weights=json.dumps(FLEET_WEIGHTS))
DELIVERY_SURFACES['Glass']['principled']['IOR']=1.52
DELIVERY_SURFACES['Lamps']['extras']['emission_color_override']=json.dumps(dict(alpha_min=.45,alpha_max=.68,linear_rgb=[1,.92,.80]))
BUDGETS={'SUV':65000}
BOUNDS={'SUV':dict(size=(2.117,4.59883,1.735),tolerance=(.002,.002,.002))}
# Generic verification measures transformed local boxes of the canted wheel
# nodes. Their conservative X corners overstate the real vertex envelope.
# suv_delivery_check independently gates actual raw-accessor bounds at 2 mm.
DELIVERY_BOUNDS=dict(size=(2.117,4.59883,1.735),tolerance=(.09,.002,.002))
SOURCE_MATERIAL_SURFACES={'X220 '+n:'Opaque' for n in ['rubber','plastic','bumper','wheel','chrome','dark_chrome','frame','caliper','cloth','seat_side','interior','headliner','interior_light','turned rotor','gloss black','prismatic red reflector','mirror','touring tire L','touring tire R','original badge','original model','original plate','original display','original cluster','weathered molded cladding']}
SOURCE_MATERIAL_SURFACES['X220 factory paint']='Paint'
SOURCE_MATERIAL_SURFACES.update({'X220 '+n:'Glass' for n in ['windshield','front side glass','privacy glass','backlight','clear optical cover','red optic']})
SOURCE_MATERIAL_SURFACES.update({'X220 '+n:'Lamps' for n in ['running guide','projector emitter','brake guide','amber marker']})
REQUIRED_NODES=['AlderX220','Door_FL','Door_FR','Door_RL','Door_RR','Hood','Liftgate','FuelDoor','Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR','Steer_FL','Steer_FR']
UV_DEFAULT_PRIORITY=.40
UV_PRIORITY={'Door ':2.0,'Hood outer':2.1,'Front fender':2.0,'Rear quarter':2.0,'Front fascia':2.1,'Rear bumper':2.0,'Liftgate outer':2.0,'Roof fixed':1.8,
 'Headlamp':1.2,'Taillamp':1.1,'Tire_':2.0,'Wheel ':1.1,'Cast spoke':1.5,'Rear plate face':6.0,'Front ALDER badge':6.0,'Rear ALDER badge':6.0,'X220 AWD model badge':5.0,'Alder center cap':6.0,'Front badge':2.5,'Rear badge':2.5,'Fictional plate':2.5,'Alder':2.0,
 'Lower door cladding':1.2,'Arch cladding':1.2,'Front side glazing':.85,'Rear side glazing':.85,'Backlight':.85,'Windshield':.85}
UV_SMART_ANGLE=66
UV_PACK_SHAPE='CONVEX'
UV_NORMALIZE_ISLAND_SCALE=True
UV_PRIORITY_ATTRIBUTE='X220UVWeight'
from suv_tire_uv import RECT
TILED_MESHES={'Tire_*':dict(rect=RECT,density_min=600,density_max=1800)}
UV_ATLAS_RECT=(0,.28,1,1)
UV_MIN_COVERAGE=.30
