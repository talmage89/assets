"""Asset-owned entry point for trigger close-ups and photographic pairs."""
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parents[1]));sys.path.insert(0,str(BASE/'src'))
from guns.common.trigger_review import run
if __name__=='__main__':
 import final_shots,interface
 run(BASE,final_shots,interface)
