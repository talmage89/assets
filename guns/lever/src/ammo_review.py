"""White-balanced reference metals beside the actual exported cartridge."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from value_review import stats,projection
from kit.fonts import find_font

def main():
 folder=BASE/'renders/final/cartridge';photo=Image.open(BASE/'build/white-balanced/ammo.png').convert('RGB')
 render=Image.open(folder/'cartridge.png').convert('RGB');shot=json.loads((folder/'shots.json').read_text())['cartridge']
 regions={
  'brass':([(367,560),(419,560),(419,820),(367,820)],[(.0044,y,z) for y,z in [(.012,.0025),(.033,.0025),(.033,.0037),(.012,.0037)]]),
  'copper':([(373,192),(418,192),(418,274),(373,274)],[(.0029,y,z) for y,z in [(.0558,.0019),(.059,.0019),(.059,.0025),(.0558,.0025)]]),
  'lead':([(374,149),(410,149),(410,161),(374,161)],[(.0009,y,z) for y,z in [(.0645,.0009),(.0647,.0009),(.0647,.0015),(.0645,.0015)]]),
 }
 rows={}
 for name,(poly,points) in regions.items():
  xy=projection(shot,points,render.size).tolist();rows[name]=dict(photo=stats(photo,poly),export=stats(render,xy),photo_polygon=poly,export_polygon=xy)
  for im,polygon in ((photo,poly),(render,xy)):ImageDraw.Draw(im).polygon([tuple(p) for p in polygon],outline=(255,80,30),width=2)
 out=BASE/'renders/final/pairs';out.mkdir(exist_ok=True);canvas=Image.new('RGB',(1600,820),(230,230,225));draw=ImageDraw.Draw(canvas)
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),19)
 draw.text((12,10),'Exported live cartridge / white-balanced photo / orange value patches',font=font,fill='black')
 for j,im in enumerate((render,photo.crop((316,130,480,975)))):
  im.thumbnail((780,720),Image.Resampling.LANCZOS);canvas.paste(im,(j*800+(800-im.width)//2,55))
 draw.text((12,786),'Gray exposed lead is an estimated neutral; different light and original flat nose. Display values, not recovered albedo.',font=font,fill='black')
 canvas.save(out/'ammunition-values-pair.jpg',quality=94,optimize=True)
 (out/'ammunition-values.json').write_text(json.dumps(dict(neutral='Exposed gray lead cap, native (374,149)-(410,161); estimated, not a gray card.',scope='Observed display colors, different geometry/light; no albedo inversion',regions=rows),indent=2))
 print('AMMUNITION VALUES',[(n,round(r['photo']['median_luma'],2),round(r['export']['median_luma'],2)) for n,r in rows.items()],flush=True)
if __name__=='__main__':main()
