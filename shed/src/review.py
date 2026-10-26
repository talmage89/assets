import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.delivery_docs import main
main(ROOT/'shed')
if '--final' in sys.argv:
 from kit.contact import review_sheet
 from kit.delivery_docs import jpg
 d=Path(sys.argv[sys.argv.index('--renders')+1])
 review_sheet([[d/'hero_open.png',d/'interior.png'],[d/'controls.png',d/'casting.png']],d/'details.jpg',width=2000,title='Hearthfield 810 / exported interior, threshold and roof')
 jpg(d/'details.jpg',ROOT/'shed/docs/details.jpg')
