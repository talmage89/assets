"""Original fictional silkscreen, gauge and grill scale, generated with Pillow."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
import math, random
from settings import KNOB_GRAPHICS
from PIL import Image, ImageDraw, ImageFont
FONT=find_font('Noto Sans', 'Regular')
BOLD=find_font('Noto Sans', 'Bold')


def generate(out,wear=.35):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    def font(size,b=False):return ImageFont.truetype(BOLD if b else FONT,size)
    im=Image.new('RGBA',(2400,600));d=ImageDraw.Draw(im)
    ink=(29,34,32,255)
    d.text((76,32),'CINDER WORKS',font=font(34,True),fill=ink)
    d.text((2310,32),'FIELD 3   /   LP',font=font(28),fill=ink,anchor='ra')
    for x in (430,1200,1970):
        # Knobs occupy the lower circles; the printed arcs stay readable around them.
        spec=KNOB_GRAPHICS
        def dial(degrees,r):
            a=math.radians(degrees)
            return x+math.sin(a)*r,300-math.cos(a)*r*1.2
        # Negative local-Y is counterclockwise in the front view: OFF -> HI -> LO.
        points=[dial(a,142) for a in range(spec['low'],spec['off']+1)]
        d.line(points,fill=ink,width=4)
        for a in range(spec['low'],spec['off']+1,spec['tick_step']):d.line((*dial(a,148),*dial(a,160)),fill=ink,width=4)
        for name,key in [('OFF','off'),('HI','high'),('LO','low')]:
            d.text(dial(spec[key],182),name,font=font(24,True),fill=ink,anchor='mm')
        d.text((x,535),'PUSH • TURN',font=font(20),fill=ink,anchor='mm')
    im.save(out/'panel.png')
    im=Image.new('RGBA',(1024,256),(20,27,30,255));d=ImageDraw.Draw(im)
    d.rounded_rectangle((8,8,1016,248),radius=35,outline=(165,166,156),width=6)
    d.text((512,106),'CINDER WORKS',font=font(86,True),fill=(223,224,210),anchor='mm')
    d.text((512,200),'O U T D O O R   C O O K I N G',font=font(26),fill=(177,181,174),anchor='mm')
    im.save(out/'badge.png')
    im=Image.new('RGBA',(768,768),(216,218,201,255));d=ImageDraw.Draw(im)
    c=384
    for v in range(0,601,20):
        a=math.radians(145+v/600*250)
        r0=270 if v%100==0 else 292
        d.line((c+r0*math.cos(a),c+r0*math.sin(a),c+324*math.cos(a),c+324*math.sin(a)),fill=(32,38,35),width=5)
        if v%100==0:
            d.text((c+228*math.cos(a),c+228*math.sin(a)),str(v),font=font(42),fill=(28,34,30),anchor='mm')
    d.arc((99,99,669,669),290,360,fill=(147,54,25),width=15)
    d.text((384,510),'°F',font=font(46),fill=(30,34,31),anchor='mm')
    d.text((384,580),'CINDER',font=font(25,True),fill=(45,49,43),anchor='mm')
    im.save(out/'gauge.png')
    im=Image.new('RGBA',(300,1050),(17,22,19,255));d=ImageDraw.Draw(im)
    for j in range(5):
        y=65+j*192
        d.rounded_rectangle((90,y+28,210,y+142),radius=18,outline=(225,215,70),width=10)
        d.rectangle((130,y,170,y+28),fill=(225,215,70))
        if j<4:d.rectangle((101,y+134-(j+1)*22,199,y+134),fill=(225,215,70))
    d.text((150,1010),'FUEL',font=font(29,True),fill=(224,223,206),anchor='mm')
    im.save(out/'scale.png')

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('out');parser.add_argument('--wear',type=float,default=.35)
    args=parser.parse_args();generate(args.out,args.wear)
