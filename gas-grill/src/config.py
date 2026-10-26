"""Asset-specific studio shots and checkpoint tolerances; meters, −Y front."""
BUDGETS={'Grill':20000}
BOUNDS={'Grill':{'size':(1.3208,.7158,1.1303),'tolerance':(.001,.001,.001)}}
SHOTS={
 'hero_closed':dict(location=(2.05,-3.20,1.95),target=(.08,0,.64),lens=72,aspect=1.25),
 'hero_open':dict(location=(2.27,-3.74,2.48),target=(.06,.05,.80),lens=72,aspect=1.25,lid=-104),
 'controls':dict(location=(.52,-1.46,1.065),target=(-.0495,-.25,.80),lens=72,aspect=1.6),
 'front':dict(location=(0,-4,.56515),target=(0,0,.56515),ortho=1.55,aspect=1.25),
 'side':dict(location=(4,0,.56515),target=(0,0,.56515),ortho=1.55,aspect=1.25),
 'back':dict(location=(0,4,.56515),target=(0,0,.56515),ortho=1.55,aspect=1.25),
 'top':dict(location=(0,0,4),target=(0,0,.65),ortho=1.55,aspect=1.25),
 'construction':dict(location=(.95,-1.4,2.1),target=(0,.03,.83),lens=72,aspect=1.4,lid=-104,hide=['Cooking grate','Grate ','Warming rack','CookGrates','WarmingRack']),
 'combustion':dict(location=(.45,-.70,1.85),target=(-.04,.03,.79),lens=72,aspect=1.4,lid=-104,hide=['Cooking grate','Grate ','Warming rack','Heat tent 1','Heat tent 3','Heat tent 5','CookGrates','WarmingRack','HeatTents'],note='Diagnostic: grates/rack and covering heat tents removed to expose burners; normally tents 1/3/5 sit directly above them.'),
 'interior':dict(location=(.95,-1.4,2.1),target=(0,.03,.88),lens=72,aspect=1.4,lid=-104),
 'regulator':dict(location=(.52,-.90,.40),target=(.14,-.35,.12),lens=75,aspect=1.3,hose='dangling'),
 'fit_check':dict(location=(1.9,-2.7,1.65),target=(.15,0,.62),lens=72,aspect=1.25,fit_reference=True),
 'hose_pose':dict(location=(1.0,-1.45,.80),target=(.25,-.30,.41),lens=75,aspect=1.0,hose='dangling'),
 'scale':dict(location=(2.6,-5.2,2.25),target=(-.38,0,.88),lens=68,aspect=1.25,human=True),
}

# Rest pose is connected to the external tank; catalog views use the free hose.
for name,shot in SHOTS.items():
    if name!='fit_check':shot.setdefault('hose','dangling')

UV_PRIORITY={
 'Fascia stainless':2.8,'Badge':2.7,'Thermometer':2.7,'Original maker':2.7,
 'Molded control knob':1.5,'Knob ':1.5,'Control ':1.3,
 'Pressed porcelain':1.5,'Brushed stainless work':1.7,'Shelf folded apron':1.2,
 'Regulator':2.0,'Type 1':2.0,'Coupling':2.0,'Hose ':2.0,'LP flexible':1.5,
 'Tank scale graduated':2.0,'Cast firebox':.9,'Cooking grate':1.1,
 'Control manifold':.40,'Gas valve':.40,'Gas metering':.40,'Gas manifold':.45,
 'Venturi':.6,'Ignition':.6,'Heat tent':1.0,'Formed cart':.65,'Lower frame':.6,
 'Side frame':.65,'Rear cart':.6,'Pressed lower shelf':.7,'Stamped shelf':.7,
}
UV_DEFAULT_PRIORITY=.9

BAKE_DROP_MESHES=('Fascia original silkscreen','Original maker badge')
REQUIRED_NODES=('tank_socket','regulator_attach','Lid','Knob_1','Knob_2','Knob_3','Wheel_Front','Wheel_Back','GreaseTray')
EXCLUDED_NODES=('Tank','TankCollision','Cylinder welded steel vessel','OPD forged brass valve body')

# Explicit asset policy; generic kit callers can leave these options absent.
from pathlib import Path
import runpy
_SETTINGS=runpy.run_path(str(Path(__file__).with_name('settings.py')))
RIG_POSES={'HoseRig':_SETTINGS['RIG_POSE']}
EXPORT_SKIN_NAMES={'HoseRig':'HoseAssembly'}
BAKE_POLICY={'isolate_moving':True,'moving_roots':['Lid','Knob_1','Knob_2','Knob_3','Wheel_Front','Wheel_Back','GreaseTray','HoseRig'],
             'cage_m':.003,'ray_distance_m':.012,'ao_distance_m':.035,'padding_m':.1}
VERIFY_POLICY={'density_p5_min':200,'density_median_min':450,'density_median_max':900,'density_p95_max':1500,'density_reference_size':2048,
 'tube':{'rest_points_property':'hose_rest_points_m','radius_m':.0052,'radial_tolerance_m':.00012,'plane_tolerance_m':.00015,'minimum_ring_vertices':6,'minimum_rings':40,'minimum_posed_radius_m':.0036,
         'minimum_attachment_travel_m':.15,'root_tolerance_m':1e-5}}
MOTIONS=[]
for node in ['Wheel_Front','Wheel_Back']:
    MOTIONS.append(dict(node=node,axis='Y',range=[0,360],step=5,tolerance_m=.0005,
        allow=[dict(moving='Wheel hub',fixed='Solid wheel axle',reason='Axle passes through hub bore')]))
MOTIONS.append(dict(node='Lid',axis='X',range=[-104,0],step=2,tolerance_m=.0005,allow=[
 dict(moving='Moving cast hinge lug',fixed='Hinge shoulder pin',reason='Pin in hinge bore'),
 dict(moving='Moving cast hinge lug',fixed='Rear fork hinge bracket',reason='Cast lug nested between fork ears'),
]))
for i in range(1,4):
    MOTIONS.append(dict(node=f'Knob_{i}',axis='Y',range=[-140,0],step=5,tolerance_m=.0005,allow=[]))
MOTIONS.append(dict(node='GreaseTray',axis='Y',kind='translation',range=[-.20,0],step=.005,tolerance_m=.0005,allow=[]))
SHOTS['drawer_open']=dict(location=(.70,-1.25,.96),target=(-.05,-.15,.63),lens=75,aspect=1.4,parts={'GreaseTray':{'translation':(0,-.20,0)}},hose='dangling')

SHOTS['grease_support']=dict(location=(.50,-.90,.53),target=(-.0555,-.03,.642),lens=75,aspect=1.4,hose='dangling')
