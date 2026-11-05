"""Checkpoint contact sheets and current-source/provenance assertions; no docs commit."""
import argparse,sys,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('renders/checkpoint'));a=p.parse_args()
 order=['201/hero','201/above','201/driver','202/above','202/driver','203/above','203/driver','204/above','204/driver','201/head_lit','201/head_dark','201/connection','201/base','201/pedestrian','201/button','201/cabinet','201/cabinet_open','204/span_hanger','201/dusk']
 recipe=hashlib.sha256(b''.join((Path('src')/n).read_bytes() for n in ('render.py','setting.py','plan.py'))).hexdigest()
 for rel in order:
  path=a.out/(rel+'.png');meta=json.loads(path.with_suffix('.json').read_text())
  assert meta['sha256']==hashlib.sha256(Path(meta['source']).read_bytes()).hexdigest(),('Stale geometry image',rel)
  assert meta['recipe_sha256']==recipe,('Stale presentation image',rel)
 contact([a.out/(s+'.png') for s in order],a.out/'contact.jpg',width=1800,title='Signals / construction checkpoint / imported GLBs',captions={str(a.out/(s+'.png')):s.replace('/',' / ').replace('_',' ') for s in order})
 contact([a.out/(s+'.png') for s in order if s.endswith(('above','driver'))],a.out/'four-towns.jpg',width=1800,title='Four towns / same family of original signal hardware')
 contact([a.out/(s+'.png') for s in order if s not in ('201/hero','201/dusk') and not s.endswith(('above','driver'))],a.out/'construction.jpg',width=1800,title='Construction and states / quick checkpoint materials')
 photos=[Path('renders/matches/trenton-pair.jpg'),Path('renders/matches/maryland-pair.jpg')]
 for photo in photos:assert photo.exists()
 review_sheet([[p] for p in photos],a.out/'photo-pairs.jpg',width=2200,title='Period photographs / calibrated framing / form comparison')
 # Display range is evidence about the current picture, not a claim of albedo.
 im=np.asarray(Image.open(a.out/'201/hero.png').convert('RGB'))/255
 y=im@np.array([.2126,.7152,.0722])
 ranges=dict(display_Y_quantiles=dict(zip(('p1','p5','p50','p95','p99'),map(float,np.quantile(y,[.01,.05,.5,.95,.99])))),white_fraction=float((im.min(axis=2)>.99).mean()),scope='Entire hero, including sky/context; not inverse albedo or an asset-only mask')
 Path('build/hero-range.json').write_text(json.dumps(ranges,indent=2))
 print('REVIEW',len(order),'current Cycles images, two period-photo pairs; four review sheets')
if __name__=='__main__':main()
