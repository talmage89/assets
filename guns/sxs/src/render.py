import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]));sys.path.insert(0,str(Path(__file__).parent))
import shots,interface
from guns.common.render import main
if '--wide' in sys.argv:
 sys.argv.remove('--wide')
 shots.STRIP_SHOT=dict(location=(1.50,-.74,.73),target=(0,.20,-.07),lens=55,aspect=1.6)
elif '--strip' in sys.argv:
 clip=sys.argv[sys.argv.index('--strip')+1]
 if clip in ('Fire','FireLeft'):
  shots.STRIP_SHOT={k:v for k,v in shots.SHOTS['triggers'].items() if k in ('location','target','lens','aspect')}
 elif clip in ('Safety','SafetyOn'):
  shots.STRIP_SHOT=dict(location=(.075,-.08,.13),target=(0,.005,.024),lens=60,aspect=1.5)
main(shots,interface)
