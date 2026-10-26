import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.delivery_docs import main,jpg
from kit.contact import review_sheet
main(ROOT/'trampoline')
if '--final' in sys.argv:
 d=Path(sys.argv[sys.argv.index('--renders')+1]);review_sheet([[d/'controls.png',d/'underpad.png'],[d/'fabric.png',d/'underside.png']],d/'details.jpg',width=2000,title='Orbit 14 / exported entry, springs, fabric and underside');jpg(d/'details.jpg',ROOT/'trampoline/docs/details.jpg')
