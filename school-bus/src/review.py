"""Ignored review contact sheets only; checkpoint never writes final docs JPGs."""
from pathlib import Path
import math
from PIL import Image,ImageDraw,ImageFont
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1]
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
def sheet(paths,out,cols=3,w=520,h=370):
    im=Image.new('RGB',(cols*w,math.ceil(len(paths)/cols)*h),(231,232,226));d=ImageDraw.Draw(im)
    for i,p in enumerate(paths):
        tile=Image.open(p).convert('RGB');tile.thumbnail((w-16,h-42));x=(i%cols)*w;y=(i//cols)*h
        im.paste(tile,(x+(w-tile.width)//2,y+29+(h-42-tile.height)//2));d.text((x+10,y+6),p.stem,font=FONT,fill=(25,30,27))
    im.save(out,quality=92,optimize=True)
def main():
    folder=BASE/'renders/checkpoint';paths=[folder/(n+'.png') for n in ['hero','front','side','rear','top','rear_three_quarter','front_detail','entrance','interior','aisle','warning','emergency','roof','scale','fleet']]
    sheet(paths,folder/'contact.jpg');sheet([folder/(n+'.png') for n in ['front','side','rear','top']],folder/'turnaround.jpg',2,w=720,h=480)
    pairs=list((BASE/'renders/matches').glob('*-pair.jpg'))
    if pairs:sheet(pairs,BASE/'renders/matches/contact.jpg',1,w=1500,h=800)
    print('REVIEW_SHEETS',folder/'contact.jpg',folder/'turnaround.jpg')
if __name__=='__main__':main()
