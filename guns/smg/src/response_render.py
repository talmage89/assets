"""Supplementary exported-GLB crown profile under the unchanged studio lights."""
import sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[3]),str(Path(__file__).parent)]
from guns.common.render import main
import final_shots,interface
final_shots.SHOTS={**final_shots.SHOTS,'paint_response':dict(
    location=(.001,.04,.46),target=(0,.04,.116),lens=85,aspect=1.7,
    action='Idle',frame=0,exposure=-.15)}
if __name__=='__main__':main(final_shots,interface)
