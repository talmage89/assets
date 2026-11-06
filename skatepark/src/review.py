"""Ignored contact sheets and measured display tone for the form gate."""
import json,sys,argparse
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.fonts import find_font

def sheet(files,path,columns=3,width=600):
    if not files:return
    tileheight=round(width*.72);out=Image.new('RGB',(columns*width,((len(files)+columns-1)//columns)*tileheight),(29,32,30));d=ImageDraw.Draw(out);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),18)
    for i,p in enumerate(files):
        im=Image.open(p).convert('RGB');im.thumbnail((width-12,tileheight-35));x=i%columns*width;y=i//columns*tileheight
        out.paste(im,(x+(width-im.width)//2,y+28));d.text((x+9,y+5),str(p.parent.name)+' / '+p.stem,font=font,fill=(230,230,222))
    path.parent.mkdir(parents=True,exist_ok=True);out.save(path,quality=91,optimize=True)

def comparison_sheet(files,path,width=1600):
    if not files:return
    images=[]
    for p in files:
        im=Image.open(p).convert('RGB')
        images.append(im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS))
    out=Image.new('RGB',(width,sum(im.height for im in images)+12*(len(images)-1)),(29,32,30));y=0
    for im in images:out.paste(im,(0,y));y+=im.height+12
    path.parent.mkdir(parents=True,exist_ok=True);out.save(path,quality=91,optimize=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,default=Path('renders/checkpoint'));a=p.parse_args()
    files=sorted(a.folder.glob('*/*.png'));sheet(files,a.folder/'contact.jpg')
    pairs=sorted(Path('renders/matches').glob('*-pair.jpg'));comparison_sheet(pairs,a.folder/'matched-contact.jpg')
    values={}
    for f in files:
        rgb=np.asarray(Image.open(f).convert('RGB'),float)/255;y=rgb@np.array([.2126,.7152,.0722])
        values[str(f.relative_to(a.folder))]=dict(display_Y_percentiles=dict(zip(('p1','p5','p50','p95','p99'),np.percentile(y,[1,5,50,95,99]).tolist())),white_clipped_fraction=float((rgb.min(axis=2)>.995).mean()),scope='Whole image, including sky/context; not an architectural mask or albedo measurement')
    (a.folder/'tone.json').write_text(json.dumps(values,indent=2));print('FORM SHEET',a.folder/'contact.jpg',len(files),'images')

if __name__=='__main__':main()
