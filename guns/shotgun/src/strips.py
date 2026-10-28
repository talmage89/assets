from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]));sys.path.insert(0,str(Path(__file__).parent))
from guns.common.strips import main
import interface
if __name__=='__main__':main(Path(__file__).resolve().parents[1],interface,source='export/shotgun.glb',output='renders/final/strips',engine='BLENDER_EEVEE',samples=16)
