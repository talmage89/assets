"""Optional before/after review of the two walnut pairs and identical hero view.

The --before directory is a local review snapshot, never a build dependency.
Both sets retain their original GLB attribution; no pixels feed the materials.
"""
import argparse,hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),24)

def main():
 p=argparse.ArgumentParser();p.add_argument('--before',type=Path,required=True)
 p.add_argument('--out',type=Path,default=BASE/'renders/walnut/comparison');a=p.parse_args()
 a.out.mkdir(parents=True,exist_ok=True);final=BASE/'renders/final'
 old=json.loads((a.before/'look-review/values.json').read_text())['finishes']
 new=json.loads((final/'look-review/values.json').read_text())['finishes']
 digest=hashlib.sha256((BASE/'export/sxs.glb').read_bytes()).hexdigest()
 results={}
 for name in ['walnut_stock','walnut_forend']:
  assert new[name]['model_sha256']==digest and new[name]['passed'],name
  images=[Image.open(folder/'look-review'/(name+'-pair.jpg')).convert('RGB') for folder in [a.before,final]]
  sheet=Image.new('RGB',(1800,2*(images[0].height+40)),(225,226,222));d=ImageDraw.Draw(sheet)
  for i,im in enumerate(images):
   y=i*(im.height+40);d.text((12,y+5),'BEFORE / accepted handoff' if i==0 else 'AFTER / final exported GLB',font=FONT,fill='black');sheet.paste(im,(0,y+40))
  sheet.save(a.out/(name+'-before-after.jpg'),quality=94,optimize=True)
  results[name]=dict(before=old[name]['ours'],after=new[name]['ours'],photo=new[name]['photo'],passed=new[name]['passed'])
 oldmeta=json.loads((a.before/'beauty/shots.json').read_text())['hero']
 newmeta=json.loads((final/'beauty/shots.json').read_text())['hero']
 for key in ['location','target','lens','aspect','exposure','action','frame']:assert oldmeta.get(key)==newmeta.get(key),key
 sheet=Image.new('RGB',(1600,2*(571+45)),(108,111,114));d=ImageDraw.Draw(sheet)
 for i,folder in enumerate([a.before,final]):
  im=Image.open(folder/'beauty/hero.png').convert('RGBA');bg=Image.new('RGBA',im.size,(108,111,114,255));bg.alpha_composite(im)
  bg=bg.convert('RGB');bg.thumbnail((1600,571),Image.Resampling.LANCZOS);y=i*616
  d.text((16,y+8),'BEFORE' if i==0 else 'AFTER / baked export',font=FONT,fill=(235,235,231));sheet.paste(bg,((1600-bg.width)//2,y+45))
 sheet.save(a.out/'hero-before-after.jpg',quality=95,optimize=True)
 (a.out/'values.json').write_text(json.dumps(dict(before_sha256=oldmeta['sha256'],after_sha256=digest,finishes=results),indent=2)+'\n')
 print('WALNUT BEFORE/AFTER',a.out)
if __name__=='__main__':main()
