"""Chain-link unique frame UVs and deliberate shared alpha-tile policy."""
BUDGETS={'ChainLink':10000}
BOUNDS={'ChainLink':dict(size=(7.769812,3.571254,1.303),tolerance=(.001,.001,.001))}
TILED_MESHES={'*_Fabric':dict(rect=(16/1024,16/1024,272/1024,320/1024),alpha_cutoff=.5,double_sided=True,density_min=800,density_max=880)}
UV_ATLAS_RECT=(.01,.34,.99,.99)
UV_MIN_COVERAGE=.20
UV_DENSITY_BANDS=dict(reference_size=1024,p5_min=100,median_min=140,median_max=600,p95_max=1400)
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['Chain_Start','Chain_EndSection','Chain_Section','Chain_BetweenTerminals','Chain_Terminal_End','Chain_Line','Chain_Terminal','Chain_Corner','Chain_GateBay','Chain_GatePost_Hinge','Chain_GatePost_Latch','Chain_Gate','Chain_ForkLatch'],cage_m=.001,ray_distance_m=.006,ao_distance_m=.03)
REQUIRED_NODES=tuple(['Chain_Start','Chain_EndSection','Chain_Section','Chain_BetweenTerminals','Chain_Terminal_End','Chain_Line','Chain_Terminal','Chain_Corner','Chain_GateBay','Chain_Gate','Chain_ForkLatch']+[n+'__'+s for n in ('Chain_Start','Chain_EndSection','Chain_Section','Chain_GateBay') for s in ('L','R')])
MOTIONS=[dict(node='Chain_ForkLatch',axis='Y',range=[-95,0],step=1,tolerance_m=.0003)]
from pathlib import Path
import runpy
v=runpy.run_path(str(Path(__file__).with_name('views.py')));SHOTS=v['SHOTS'];STUDIO=v['STUDIO']

# Long subpixel bottom wire must not determine the scale of the whole atlas.
UV_PRIORITY={n+" bottom tension wire":.20 for n in ("Chain_Start","Chain_EndSection","Chain_Section","Chain_BetweenTerminals")}
UV_PRIORITY.update({n+" top rail":.70 for n in ("Chain_Start","Chain_EndSection","Chain_Section","Chain_BetweenTerminals")})
UV_PRIORITY.update({"Chain gate welded frame":.85})
