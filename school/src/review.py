"""Contact sheets and objective exposure facts; no final docs at this gate."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font


def sheet(paths,out,columns=3,thumb=480):
    if not paths:return
    h=350;rows=math.ceil(len(paths)/columns);im=Image.new('RGB',(columns*thumb,rows*h),(25,29,26));d=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),15)
    for i,p in enumerate(paths):
        src=Image.open(p).convert('RGB');src.thumbnail((thumb,h-28));x=(i%columns)*thumb;y=(i//columns)*h
        im.paste(src,(x+(thumb-src.width)//2,y+26));d.text((x+8,y+5),p.parent.name+' / '+p.stem,font=font,fill=(224,224,213))
    out.parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=91,optimize=True)


def main():
    folder=Path('renders/checkpoint');paths=sorted(folder.glob('*/*.png'));sheet(paths,folder/'contact.jpg')
    stats={}
    for p in folder.glob('*/hero.png'):
        a=np.array(Image.open(p).convert('RGB'))/255;y=a@np.array([.2126,.7152,.0722]);stats[p.parent.name]=dict(display_luma_p1_p50_p99=np.percentile(y,[1,50,99]).tolist(),all_channel_clipped_fraction=float((a.min(2)>.99).mean()),camera=json.loads((p.parent/'provenance.json').read_text())['hero']['camera'])
    Path('build/tonal-check.json').write_text(json.dumps(stats,indent=2))
    sheet(sorted(Path('renders/matches').glob('*-pair.jpg')),Path('renders/matches/contact.jpg'),columns=1,thumb=1600)
    print('REVIEW SHEETS',folder/'contact.jpg')

if __name__=='__main__':main()
