"""Same-camera comparison panels, native 1440 pixels each; no docs output."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import review_sheet
from PIL import Image
out=Path('renders/form-fixes')
for name in ('side','hero','tail_plies','truck','truck_inner','wheel_bearing','section_stance','section_truck','section_kick'):
    a=out/'before'/(name+'.png');b=out/'after'/(name+'.png')
    assert Image.open(a).width>=800 and Image.open(b).width>=800
    review_sheet([[a,b]],out/(name+'-before-after.jpg'),width=2880,title=name.replace('_',' ')+' / before (left) / after (right) / same camera')
review_sheet([[out/'after'/(n+'.png') for n in ('section_stance','section_truck','section_kick')]],out/'three-sections.jpg',width=3600,title='Actual exported deck / stance, mounting station, kick / ray-derived veneer caps')
