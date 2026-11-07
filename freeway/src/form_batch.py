"""Serial identical-camera form evidence; one GPU-lock acquisition for the set."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render import render
for seed,names in [(101,['hero','above','terminal','pier_girders','sign_structure','gore']),(202,['hero','above','sound_wall'])]:
 names=[n for n in names if not (Path('renders/form-corrected')/str(seed)/(n+'.png')).exists()]
 if not names:continue
 render(f'export/Freeway-{seed}.gltf',f'renders/form-corrected/{seed}',1200,20,'CYCLES',names=names,seed=seed)
