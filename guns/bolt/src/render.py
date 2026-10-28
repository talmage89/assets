"""Final presentation accepts only the exported baked GLB."""
import sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[3]),str(Path(__file__).parent)]
from guns.common.render import main
import final_shots as shots,interface
if __name__=='__main__':main(shots,interface)
