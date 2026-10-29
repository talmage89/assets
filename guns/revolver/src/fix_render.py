"""Use identical final lighting/cameras for the preserved and current GLBs."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parents[2]),str(HERE)]
import final_shots,interface
from guns.common.render import main
from presentation import stamp
main(final_shots,interface)
stamp(sys.argv[sys.argv.index('--out')+1])
