"""Current exported-game evidence, full-frame tonal range and native crops."""
import argparse,sys,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit.contact import contact,review_sheet
from deliver import bundle

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('renders/checkpoint'));a=p.parse_args()
 order=['202/hero','202/dusk','201/hero','201/above','201/driver','202/above','202/driver','203/above','203/driver','204/above','204/driver','201/head_lit','201/head_dark','201/lens_detail','201/pavement','201/connection','201/base','201/pedestrian','201/button','201/cabinet','201/cabinet_open','204/span_hanger','201/dusk','optics/30m','optics/100m']
 recipe=hashlib.sha256(b''.join((Path('src')/n).read_bytes() for n in ('render.py','setting.py','plan.py'))).hexdigest()
 for rel in order:
  path=a.out/(rel+'.png');meta=json.loads(path.with_suffix('.json').read_text())
  assert meta['bundle_sha256']==bundle(meta['source']),('Stale export/map image',rel)
  if not rel.startswith('optics/'):
   assert meta['recipe_sha256']==recipe,('Stale presentation image',rel)
  assert meta['engine']=='CYCLES'
 contact([a.out/(s+'.png') for s in order],a.out/'contact.jpg',width=2100,title='Signals / exported shared-map parts / Cycles',captions={str(a.out/(s+'.png')):s.replace('/',' / ').replace('_',' ') for s in order})
 contact([a.out/(s+'.png') for s in order if s.endswith(('above','driver'))],a.out/'four-towns.jpg',width=2000,title='Four road plans / four municipal equipment choices')
 contact([a.out/(s+'.png') for s in order if s not in ('201/hero','201/dusk') and not s.endswith(('above','driver')) and not s.startswith('optics/')],a.out/'construction.jpg',width=2100,title='Construction / hardware / service age / lens states')
 photos=sorted(Path('renders/matches').glob('*-pair.jpg'));assert len(photos)>=4
 review_sheet([[p] for p in photos],a.out/'photo-pairs.jpg',width=2200,title='Measured photo framing / matched procedural sun and sky')
 contact([a.out/'optics/30m.png',a.out/'optics/100m.png'],a.out/'optics/contact.jpg',width=2000,title='Left red lit / right dark / true 30 m and 100 m camera distances')
 im=np.asarray(Image.open(a.out/'202/hero.png').convert('RGB'))/255;y=im@np.array([.2126,.7152,.0722])
 ranges=dict(hero='202/hero',display_Y_quantiles=dict(zip(('p1','p5','p50','p95','p99'),map(float,np.quantile(y,[.01,.05,.5,.95,.99])))),white_fraction=float((im.min(axis=2)>.99).mean()),scope='Full hero including sky/context, display-domain value; not an albedo estimate')
 Path('build/hero-range.json').write_text(json.dumps(ranges,indent=2))
 from measure import run
 run()
 if Path('../build/signals-before/checkpoint').exists():
  from compare_fixes import run
  run()
 print('REVIEW',len(order),'current Cycles views;',len(photos),'photo pairs; range',ranges)
if __name__=='__main__':main()
