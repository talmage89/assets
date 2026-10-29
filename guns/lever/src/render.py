import sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from guns.common.render import main
import shots,interface
if os.environ.get('PD_LEVER_FINAL')=='1':import final_shots as shots
if __name__=='__main__':main(shots,interface)
