"""Rasterize fictional checkpoint numbers using an installed open font."""
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--text');p.add_argument('--out');a=p.parse_args()
im=Image.new('RGBA',(256,256),(0,0,0,0));d=ImageDraw.Draw(im)
font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),27)
box=d.multiline_textbbox((0,0),a.text,font=font,align='center',spacing=9)
d.multiline_text(((256-box[2])/2,(256-(box[3]-box[1]))/2),a.text,font=font,fill=(24,20,14,255),align='center',spacing=9)
im.save(a.out)
