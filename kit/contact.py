"""Captioned contact sheets; source renders remain untouched. No generated assets."""
import argparse, math
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
FONT='/usr/share/fonts/noto/NotoSans-Regular.ttf'


def contact(paths,out,width=1600,title='Modeling / look-dev review',captions=None):
    paths=list(map(Path,paths));w=width//2;h=round(w*.8)+58
    canvas=Image.new('RGB',(width,70+math.ceil(len(paths)/2)*h),(232,233,229));d=ImageDraw.Draw(canvas)
    d.text((24,19),title,font=ImageFont.truetype(FONT,25),fill=(29,37,34))
    for i,p in enumerate(paths):
        src=Image.open(p).convert('RGBA');bg=Image.new('RGBA',src.size,(232,233,229,255));bg.alpha_composite(src)
        im=ImageOps.contain(bg.convert('RGB'),(w-16,h-62))
        x=(i%2)*w+(w-im.width)//2;y=70+(i//2)*h
        canvas.paste(im,(x,y));d.text(((i%2)*w+14,y+h-49),(captions or {}).get(str(p),p.stem.replace('_',' ')),font=ImageFont.truetype(FONT,19),fill=(37,45,40))
    Path(out).parent.mkdir(parents=True,exist_ok=True);canvas.save(out,quality=90,optimize=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--title',default='Modeling / look-dev review');p.add_argument('images',nargs='+');a=p.parse_args();contact(a.images,a.out,title=a.title)


def review_sheet(rows,out,width=2400,title='Photo-directed look-dev review'):
    """Variable-height rows of one or more images, preserving comparison scale.

    A full-width photo pair stays readable; hero/detail images can share a row.
    Callers supply rows of paths. No source images are modified or committed.
    """
    margin,gap=20,16
    prepared=[]
    for row in rows:
        cell=(width-2*margin-gap*(len(row)-1))//len(row)
        images=[]
        for path in row:
            path=Path(path);src=Image.open(path).convert('RGBA')
            bg=Image.new('RGBA',src.size,(232,233,229,255));bg.alpha_composite(src)
            height=round(src.height*cell/src.width)
            images.append((bg.convert('RGB').resize((cell,height),Image.Resampling.LANCZOS),path.stem.replace('_',' ')))
        prepared.append((images,max(im.height for im,_ in images)+42))
    canvas=Image.new('RGB',(width,90+sum(h+gap for _,h in prepared)),(232,233,229))
    draw=ImageDraw.Draw(canvas)
    draw.text((margin,24),title,font=ImageFont.truetype(FONT,30),fill=(29,37,34))
    y=90
    for images,height in prepared:
        x=margin
        for im,label in images:
            canvas.paste(im,(x,y))
            draw.text((x,y+height-32),label,font=ImageFont.truetype(FONT,20),fill=(37,45,40))
            x+=im.width+gap
        y+=height+gap
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    canvas.save(out,quality=92,optimize=True)
