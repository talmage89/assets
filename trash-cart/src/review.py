"""Compose final exported-GLB evidence and at most three bounded docs JPGs."""
import argparse,json,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet

def jpg(source,target):
 im=Image.open(source).convert('RGB');im.thumbnail((1600,10000),Image.Resampling.LANCZOS)
 target.parent.mkdir(parents=True,exist_ok=True)
 for quality in range(88,40,-3):
  im.save(target,quality=quality,optimize=True)
  if target.stat().st_size<=200000:return
 raise RuntimeError('Documentation size limit exceeded')

def main():
 p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');p.add_argument('--renders',required=True);a=p.parse_args();folder=Path(a.renders)
 if not a.final:
  contact(sorted(folder.glob('*.png')),folder/'contact.jpg',width=1800,title='Trash cart / source review');return
 blue=folder.parent/'recycling';eevee=folder.parent/'final-eevee'
 for d in [folder,blue,eevee]:
  for shot in json.loads((d/'shots.json').read_text()).values():
   if shot['stage']!='final' or not shot['source'].endswith('.glb'):raise RuntimeError('Final evidence requires GLB renders')
 names=['hero_closed','hero_open','front','side','back','top','controls','hinge','wheel','scale']
 paths=[folder/(n+'.png') for n in names]+[blue/'hero_closed.png',blue/'top.png',eevee/'hero_closed.png']
 contact(paths,folder/'contact.jpg',width=2400,title='Alder Creek / 96 gallon cart / exported GLBs / Eevee last',captions={str(blue/'hero_closed.png'):'recycling variant / shared atlas',str(blue/'top.png'):'molded recycling relief',str(eevee/'hero_closed.png'):'Eevee / trash variant'})
 review_sheet([[folder/'hero_closed.png',blue/'hero_closed.png']],folder/'variants-contact.jpg',width=2400,title='Trash / recycling / one shared 1024 atlas')
 review_sheet([[folder/'front.png',folder/'side.png'],[folder/'back.png',folder/'top.png']],folder/'turnaround-contact.jpg',width=2400,title='Exported GLB / front, side, back, top')
 review_sheet([[folder/'hero_open.png',folder/'controls.png'],[folder/'hinge.png',folder/'wheel.png'],[blue/'top.png',folder/'scale.png']],folder/'details-contact.jpg',width=2400,title='Hollow body / truck interface / hinge / wheels / relief / scale')
 docs=ROOT/'trash-cart/docs'
 for name in ['variants','turnaround','details']:jpg(folder/(name+'-contact.jpg'),docs/(name+'.jpg'))

if __name__=='__main__':main()
