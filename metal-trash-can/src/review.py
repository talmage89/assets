"""Three bounded documentation images, all from the shipped GLB."""
import argparse,json,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet

def jpg(source,target):
 im=Image.open(source).convert('RGB');im.thumbnail((1600,10000),Image.Resampling.LANCZOS);target.parent.mkdir(parents=True,exist_ok=True)
 for q in range(88,39,-3):
  im.save(target,quality=q,optimize=True)
  if target.stat().st_size<=200000:return
 raise RuntimeError('Docs size')
def main():
 p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');p.add_argument('--renders',required=True);a=p.parse_args();f=Path(a.renders)
 if not a.final:contact(sorted(f.glob('*.png')),f/'contact.jpg',width=1800,title='Galvanized garbage can / source');return
 names=['hero_closed','hero_open','front','side','back','top','controls','handle','interior','scale'];e=f.parent/'final-eevee/hero_closed.png'
 for folder in [f,e.parent]:
  for s in json.loads((folder/'shots.json').read_text()).values():
   assert s['stage']=='final' and s['source'].endswith('.glb')
 contact([f/(n+'.png') for n in names]+[e],f/'contact.jpg',width=2400,title='31 gallon galvanized garbage can / exported GLB / Eevee last')
 review_sheet([[f/'hero_closed.png',e]],f/'hero-contact.jpg',width=2400,title='Cycles / Eevee / one 1024 texture set')
 review_sheet([[f/'front.png',f/'side.png'],[f/'back.png',f/'top.png']],f/'turnaround-contact.jpg',width=2400,title='Front / side / back / top')
 review_sheet([[f/'controls.png',f/'handle.png'],[f/'interior.png',f/'scale.png'],[f/'hero_open.png']],f/'details-contact.jpg',width=2400,title='Pressed lid / carrying eye / hollow interior / 1.8 m scale')
 for n in ['hero','turnaround','details']:jpg(f/(n+'-contact.jpg'),ROOT/'metal-trash-can/docs'/(n+'.jpg'))
if __name__=='__main__':main()
