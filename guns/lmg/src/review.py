"""Rebuild checkpoint contact pages without writing final docs JPGs."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1]
def main():
 out=BASE/'renders/checkpoint';out.mkdir(parents=True,exist_ok=True)
 paths=[p for p in sorted(out.glob('*.png')) if not p.stem.endswith('-dimensions')]+list(sorted((out/'pairs').glob('*-pair.jpg')))
 paths+=list(sorted((out/'detachables').glob('*/*.png')))
 for name in ('sections.jpg','link-interleaving-section.jpg','photo-measurements.jpg','eye-weld.jpg'):
  if (out/name).exists():paths.append(out/name)
 if (out/'belt-advance.jpg').exists():paths.append(out/'belt-advance.jpg')
 if (out/'orthographic-dimensions.jpg').exists():paths.append(out/'orthographic-dimensions.jpg')
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
 pages=[]
 for k in range(0,len(paths),12):
  group=paths[k:k+12];im=Image.new('RGB',(1600,320*((len(group)+3)//4)),(230,233,229));d=ImageDraw.Draw(im)
  for j,p in enumerate(group):
   tile=Image.open(p).convert('RGB');tile.thumbnail((390,282));x=j%4*400;y=j//4*320
   im.paste(tile,(x+(400-tile.width)//2,y+28+(282-tile.height)//2));d.text((x+10,y+5),p.stem,font=font,fill=(20,35,25))
  dest=out/f'review-page-{len(pages)+1}.jpg';im.save(dest,quality=92);pages.append(dest)
 if pages:
  ims=[Image.open(p) for p in pages];sheet=Image.new('RGB',(1600,sum(i.height for i in ims)),(230,233,229));y=0
  for im in ims:sheet.paste(im,(0,y));y+=im.height
  sheet.save(out/'contact-sheet.jpg',quality=90)
 print('REVIEW',len(paths),'images,',len(pages),'pages')
if __name__=='__main__':main()
