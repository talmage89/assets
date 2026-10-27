"""Fictional original graphics, generated with installed OFL Noto fonts."""
import argparse,math
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from PIL import Image,ImageDraw,ImageFont
F=find_font('Noto Sans', 'Regular');B=find_font('Noto Sans', 'Bold')
def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    im=Image.new('RGBA',(768,1536),(91,100,99,255));d=ImageDraw.Draw(im)
    def text(x,y,s,size=45,bold=False,fill=(226,228,212,255)):
        d.text((x,y),s,font=ImageFont.truetype(B if bold else F,size),fill=fill,anchor='mm')
    d.rounded_rectangle((12,12,756,1524),radius=32,outline=(168,172,160),width=6)
    text(384,98,'CINDER WORKS',62,True);text(384,173,'EVENING 89  /  LP',37)
    # knob center at print y=570; pivot/axis ticks based on the actual dimensions.
    cx,cy=384,518
    def dial(a,r):
        t=math.radians(a);return (cx+math.sin(t)*r,cy-math.cos(t)*r)
    d.line([dial(a,211) for a in range(-135,1)],fill=(226,228,212),width=5)
    for a in range(-135,1,15):d.line((*dial(a,213),*dial(a,232)),fill=(226,228,212),width=5)
    for a,s in [(0,'OFF'),(-55,'HI'),(-135,'LO')]:
        x,y=dial(a,274);text(x,y,s,39,True)
    text(384,910,'PUSH  •  TURN',36)
    text(384,1220,'PIEZO',35,True);text(384,1375,'OUTDOOR USE ONLY',34)
    im.save(out/'controls.png')
    im=Image.new('RGBA',(1024,384),(27,36,33,255));d=ImageDraw.Draw(im)
    d.rounded_rectangle((8,8,1016,376),radius=22,outline=(185,186,163),width=6)
    text(512,110,'CINDER WORKS',92,True);text(512,230,'E V E N I N G   8 9',56);text(512,315,'RADIANT PATIO HEATER',36)
    im.save(out/'badge.png')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--wear',type=float);main(p.parse_args().out)
