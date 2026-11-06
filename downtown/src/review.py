"""Ignored checkpoint sheets; no final docs are committed before approval."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font

def sheet(paths,out,columns=3,cell=520):
 paths=list(paths)
 if not paths:raise ValueError('No rendered images found')
 rows=(len(paths)+columns-1)//columns;im=Image.new('RGB',(cell*columns,round(cell*.72)*rows),(232,230,220));d=ImageDraw.Draw(im);font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),15)
 for i,p in enumerate(paths):
  a=Image.open(p).convert('RGB');a.thumbnail((cell-16,round(cell*.72)-38));x=(i%columns)*cell;y=(i//columns)*round(cell*.72)
  im.paste(a,(x+(cell-a.width)//2,y+29));d.text((x+10,y+7),str(p).replace('renders/',''),font=font,fill=(30,35,30))
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=90,optimize=True);print('SHEET',out,len(paths));return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--folder',default='renders/checkpoint');p.add_argument('--out');a=p.parse_args()
 files=sorted(Path(a.folder).glob('*/*.png'));sheet(files,a.out or a.folder+'/contact.jpg')
 if Path('renders/matches').exists():
  pairs=sorted(Path('renders/matches').glob('*-pair.jpg'))
  if pairs:sheet(pairs,'renders/matches/contact.jpg',1,1600)
