import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
sys.path.insert(0,str(Path(__file__).parent))
import shots,interface
from guns.common.render import main
main(shots,interface)
