import sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[3]),str(Path(__file__).parent)]
import final_shots,interface
from guns.common.render import main
final_shots.FINAL_STAGE=False
final_shots.RENDER_STAGE='dense procedural source / comparison only'
main(final_shots,interface)

from presentation import stamp
stamp(sys.argv[sys.argv.index("--out")+1])
