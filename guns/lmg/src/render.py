import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
import shots,interface
from guns.common.render import main
if __name__=='__main__':main(shots,interface)
