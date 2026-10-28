"""Real-speed 15-Hz playback of the actual baked delivery."""
import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(Path(__file__).parent)]
from guns.common.strips import main
import interface
if __name__=='__main__':main(BASE,interface,source='export/bolt.glb',output='renders/final/strips',engine='BLENDER_EEVEE',samples=16)
