import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
sys.path.insert(0,str(Path(__file__).parent))
import interface
source=Path(sys.argv[sys.argv.index('--source')+1])
if 'export' in source.parts:import final_shots as shots
else:import shots
from guns.common.render import main
main(shots,interface)

from presentation import stamp
stamp(sys.argv[sys.argv.index("--out")+1])
