import argparse
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--wear',type=float,default=.4);a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
im=Image.new('RGBA',(1024,1229),(0,0,0,0));d=ImageDraw.Draw(im);f=ImageFont.truetype(find_font('DejaVu Sans', 'Condensed Bold'),190)
d.text((512,938),'1847',font=f,anchor='mm',fill=(220,221,206,255));im.save(out/'address.png')
