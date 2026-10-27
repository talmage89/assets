"""Pin oak atlas, source and exported-GLB delivery policy."""
from pathlib import Path
import runpy
globals().update({k:v for k,v in runpy.run_path(str(Path(__file__).with_name("config.py"))).items() if k.isupper()})
BUDGETS={'PinOak':25000}
BOUNDS={'PinOak':dict(size=(10.,10.,16.7),tolerance=(1.4,1.4,1.))}
DELIVERY_BOUNDS=BOUNDS['PinOak']
TILED_MESHES={'Summer leaf cards':dict(rect=(0,0,1,.5),alpha_cutoff=.45,double_sided=True,preserve_normals=True,density_min=580,density_max=800)}

MATERIAL_OVERRIDES={'Trunk and branches':dict(ior=1.45,specular=.06)}
# More of the unchanged atlas is assigned to chest-height bark for ridge grain.
UV_DENSITY_BANDS=dict(UV_DENSITY_BANDS,median_max=750)
