"""Contact sheets of every actual checkpoint export view; no docs this round."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font


def sheet(files,out,title,columns=3):
    files=list(files);w=480;h=352
    im=Image.new('RGB',(columns*w,52+((len(files)+columns-1)//columns)*h),(32,37,34));d=ImageDraw.Draw(im)
    font=ImageFont.truetype(find_font('DejaVu Sans','Book'),15);d.text((14,14),title,font=font,fill=(237,236,224))
    for i,p in enumerate(files):
        pic=Image.open(p).convert('RGB');pic.thumbnail((w-10,h-37),Image.Resampling.LANCZOS)
        x=(i%columns)*w;y=52+(i//columns)*h;im.paste(pic,(x+(w-pic.width)//2,y))
        d.text((x+8,y+h-26),str(p.parent.name)+' / '+p.stem,font=font,fill=(215,218,206))
    out.parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=91,optimize=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--folder',type=Path,default=Path('renders/checkpoint'));a=ap.parse_args()
    files=sorted(a.folder.rglob('*.png'));sheet(files,a.folder/'contact.jpg','River / exported glTF / form and construction checkpoint')
    pairs=sorted(Path('renders/checkpoint-matches').glob('*-pair.jpg'))
    if pairs:sheet(pairs,Path('renders/checkpoint-matches/contact.jpg'),'Photo type comparisons / balanced assumed neutrals',1)
    print('REVIEW_SHEET',len(files),a.folder/'contact.jpg')


if __name__=='__main__':main()
