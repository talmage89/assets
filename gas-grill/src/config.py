"""Asset-specific studio shots and checkpoint tolerances; meters, −Y front."""
BUDGETS={'Grill':20000}
BOUNDS={'Grill':{'size':(1.3208,.6858,1.1303),'tolerance':(.001,.001,.001)}}
SHOTS={
 'hero_closed':dict(location=(2.05,-3.20,1.95),target=(.08,0,.64),lens=72,aspect=1.25),
 'hero_open':dict(location=(2.1,-3.45,2.35),target=(.06,.05,.77),lens=72,aspect=1.25,lid=-104),
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
