"""Real-duration 15-Hz inspection strips/playback from the exported checkpoint."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
import interface
from guns.common.strips import main
if __name__=='__main__':main(Path(__file__).resolve().parents[1],interface,source='build/lmg.glb')
