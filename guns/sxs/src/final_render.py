"""Common renderer entry point for look development and baked-export finals."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
import final_shots,interface
from guns.common.render import main
if '--source-diagnostic' in sys.argv:
 sys.argv.remove('--source-diagnostic');final_shots.FINAL_STAGE=False
if '--mask' in sys.argv:
 sys.argv.remove('--mask');final_shots.MASK=True
if '--look' in sys.argv:
 sys.argv.remove('--look')
 from look_matches import SHOTS
 final_shots.SHOTS.update(SHOTS)
if __name__=='__main__':main(final_shots,interface)
