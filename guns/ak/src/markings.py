"""Original stamps; installed OFL font, no reference pixels or traced glyphs."""
from pathlib import Path
import sys
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
OUT=BASE/'build/markings';OUT.mkdir(parents=True,exist_ok=True)
font=find_font('Noto Sans','Regular')
def label(name,lines,size=(2048,512)):
 im=Image.new('L',size,0);d=ImageDraw.Draw(im);f=ImageFont.truetype(font,100)
 for i,line in enumerate(lines):d.text((size[0]/2,30+160*i),line,font=f,anchor='mt',fill=255,stroke_width=0)
 im.save(OUT/(name+'.png'))
label('receiver',['PROPANE DEFENSE','RILL 39   •   7.62 × 39','PD  039184'],(2048,512))
# Keep the primer's center clear. These original short legends sit on the
# head's outer annulus, above and below the separate primer/seal treatment.
im=Image.new('L',(1024,1024),0);d=ImageDraw.Draw(im);f=ImageFont.truetype(font,120)
d.text((512,150),'PD 39',font=f,anchor='mm',fill=255)
d.text((512,870),'RILL',font=f,anchor='mm',fill=255)
im.save(OUT/'headstamp.png')
# Two staggered columns on a 13.4 x 60 mm leaf; our typography and layout.
w,h=1024,4096;im=Image.new('L',(w,h),0);d=ImageDraw.Draw(im);f=ImageFont.truetype(font,175)
for i in range(10):
 x=(-3.65 if i%2==0 else 3.65);y=211+i*3.6
 px=(x+6.7)/13.4*w;py=(251-y)/63*h
 d.text((px,py),str(i+1),font=f,anchor='mm',fill=255)
im.save(OUT/'leaf.png')
