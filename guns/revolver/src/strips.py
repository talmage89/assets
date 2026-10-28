import sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]));sys.path.insert(0,str(BASE/'src'))
import interface
from guns.common.strips import main
main(BASE,interface,source='build/revolver.glb',output='renders/checkpoint/strips')
