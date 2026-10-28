import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]));sys.path.insert(0,str(BASE/'src'))
import interface
from guns.common.strips import main
checkpoint='--checkpoint' in sys.argv
main(BASE,interface,source='build/revolver.glb' if checkpoint else 'export/revolver.glb',
 output='renders/checkpoint/strips' if checkpoint else 'renders/final/strips',
 engine='BLENDER_WORKBENCH' if checkpoint else 'BLENDER_EEVEE',samples=16)
