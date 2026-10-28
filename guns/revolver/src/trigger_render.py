import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]));sys.path.insert(0,str(BASE/'src'))
import shots,interface
from guns.common.trigger_review import run
run(BASE,shots,interface)
