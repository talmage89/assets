"""Local checkpoint contact sheets; no documentation image is committed."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.contact import contact,review_sheet
from PIL import Image
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--matches',action='store_true');a=p.parse_args()
folder=Path('renders/checkpoint');images=list(folder.glob('*.png'))
if images:contact(sorted(images),folder/'contact.jpg',width=1600,title='Miniature golf / form and construction checkpoint / imported glTF')
hero=folder/'hero.png'
if hero.exists():
 im=np.asarray(Image.open(hero).convert('RGB'))/255;y=im@np.array([.2126,.7152,.0722]);(folder/'tonal-range.json').write_text(json.dumps(dict(display_y_percentiles={str(p):float(np.percentile(y,p)) for p in (1,5,50,95,99)},white_clip_share=float(np.mean(np.max(im,axis=2)>.995)),scope='Whole frame display RGB, includes procedural sky and context; not albedo'),indent=2))
pairs=sorted(Path('renders/matches').glob('*-pair.jpg'))
if pairs:review_sheet([[p] for p in pairs],folder/'matched-pairs.jpg',width=2000,title='Three period photographs / calibrated original construction comparisons')
