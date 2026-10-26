"""Three bounded documentation JPGs, with exported-GLB provenance checks."""
import argparse,hashlib,json,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet
from kit.delivery_docs import jpg

def main():
 p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--final',action='store_true');a=p.parse_args();f=Path(a.renders)
 if not a.final:
  contact(sorted(f.glob('*.png')),f/'contact.jpg',title='Ammo can / source review');return
 asset=ROOT/'ammo-can';digest=hashlib.sha256((asset/'export/AmmoCan.glb').read_bytes()).hexdigest()
 labels={'hero_closed':'Closed cover','hero_open':'Released cam and opened cover','front':'Front','side':'Side','back':'Rear','top':'Top','controls':'Cam latch and pull bail','casting':'Rear hinge and cover hooks','handle':'Raised carrying handle','scale':'Scale beside a 1.8 m human'}
 names=list(labels);e=f.parent/'final-eevee/hero_closed.png'
 for folder in (f,e.parent):
  for s in json.loads((folder/'shots.json').read_text()).values():
   assert s['stage']=='final' and s['source'].endswith('.glb') and s['source_sha256']==digest
 inputs=asset/'build/docs-input';inputs.mkdir(parents=True,exist_ok=True)
 paths={}
 for n,label in labels.items():
  paths[n]=inputs/(label+'.png');shutil.copyfile(f/(n+'.png'),paths[n])
 eevee=inputs/'Eevee.png';shutil.copyfile(e,eevee)
 contact([paths[n] for n in names]+[eevee],f/'contact.jpg',width=2400,title='M2A1-style ammo can / exported GLB / Eevee last')
 review_sheet([[paths['hero_closed'],eevee]],f/'hero-contact.jpg',width=2400,title='Cycles / Eevee / one 1024 texture set')
 review_sheet([[paths['front'],paths['side']],[paths['back'],paths['top']]],f/'turnaround-contact.jpg',width=2400,title='Front / side / rear / top')
 review_sheet([[paths['controls'],paths['casting']],[paths['handle'],paths['scale']],[paths['hero_open']]],f/'details-contact.jpg',width=2400,title='Cam / hinge / carrying handle / scale / open cover')
 for n in ('hero','turnaround','details'):jpg(f/(n+'-contact.jpg'),asset/'docs'/(n+'.jpg'))
if __name__=='__main__':main()
