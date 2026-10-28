"""Dense-source photographic comparisons, separately labeled from delivery."""
import sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[3]),str(Path(__file__).parent)]
from guns.common.render import main
import final_shots as shots,interface
shots.FINAL_STAGE=False
shots.RENDER_STAGE='dense source, original procedural finishes; comparison only'
if __name__=='__main__':main(shots,interface)
