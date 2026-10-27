"""Original fictional labels; installed open-license fonts only."""
import argparse
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from PIL import Image,ImageDraw,ImageFont
B=find_font('Noto Sans', 'Bold');F=find_font('Noto Sans', 'Regular')
def main(out,wear):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for name,size,bg,rows in [('badge',(1024,512),(24,32,29),[('CINDER WORKS',85),('MEADOW 21',100),('140 cc  /  OHV',43)]),('warning',(1024,512),(222,192,76),[('CAUTION',100),('ROTATING BLADE',65),('KEEP HANDS & FEET CLEAR',47),('STOP ENGINE BEFORE SERVICE',37)]),('bag',(1024,320),(45,52,44),[('CINDER WORKS',110),('MEADOW  /  21',58)])]:
        im=Image.new('RGBA',size,(0,0,0,0) if name=='bag' else (*bg,255));d=ImageDraw.Draw(im)
        for i,(s,fs) in enumerate(rows):d.text((size[0]/2,size[1]*(i+.52)/len(rows)),s,font=ImageFont.truetype(B if i==0 else F,fs),anchor='mm',fill=(203,206,181) if name!='warning' else (27,33,25))
        im.save(out/(name+'.png'))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--wear',type=float,default=.35);a=p.parse_args();main(a.out,a.wear)
