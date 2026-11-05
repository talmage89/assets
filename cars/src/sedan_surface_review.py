"""Identical full-size studio crops; every sampled box is recorded, never warped."""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font

REGIONS=[
 ('windshield','front_three_quarter',(460,250,1260,700)),
 ('roof-sail','front_three_quarter',(600,240,1400,620)),
 ('backlight-sail-deck','rear_three_quarter',(160,260,960,700)),
 ('hood-lamp-corner','front_three_quarter',(120,390,920,820)),
 ('lamp-cut','face',(0,0,1600,650)),
 ('grille','face',(0,250,1600,950)),
]

def main():
 p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True);font=ImageFont.truetype(find_font('Noto Sans','Regular'),20);records=[]
 metadata=[json.loads((Path(folder)/'shots.json').read_text()) for folder in [a.before,a.after]]
 for label,name,box in REGIONS:
  paths=[Path(a.before)/(name+'.png'),Path(a.after)/(name+'.png')]
  if not all(f.exists() for f in paths):raise ValueError('Missing full-size comparison: '+name)
  for key in ['location','target','lens','roll','ortho','studio_yaw','exposure','width','height','paint']:
   if metadata[0][name].get(key)!=metadata[1][name].get(key):raise ValueError('Before/after camera or value recipe differs: '+name+' / '+key)
  if any(m[name]['stage']!='final exported GLB' for m in metadata):raise ValueError('Comparison must judge both exported deliveries')
  ims=[Image.open(f).convert('RGB') for f in paths]
  if ims[0].size!=ims[1].size:raise ValueError('Before/after framing resolution differs: '+name)
  crops=[im.crop(box) for im in ims];w,h=crops[0].size
  if w<800:raise ValueError('A native comparison crop must be at least 800 px wide')
  pair=Image.new('RGB',(2*w,h+40),(230,232,230));d=ImageDraw.Draw(pair)
  for i,(im,text) in enumerate(zip(crops,['Before','After GLB'])):
   pair.paste(im,(i*w,40));d.text((i*w+8,8),text,font=font,fill=(25,35,40))
  pair.save(out/(label+'.jpg'),quality=96,optimize=True)
  records.append(dict(region=label,view=name,box=list(box),native_crop_size=[w,h],sources=[str(f) for f in paths],sha256=[hashlib.sha256(f.read_bytes()).hexdigest() for f in paths]))
 (out/'crops.json').write_text(json.dumps(records,indent=2));print('SURFACE_BEFORE_AFTER',len(records),out)
 from sedan_detail_review import sheet
 sheet([out/(r['region']+'.jpg') for r in records],out/'contact.jpg',2,1600)
if __name__=='__main__':main()
