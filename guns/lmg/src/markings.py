"""Fictional originals, prepared for later normal-map stamping; never references."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from PIL import Image,ImageDraw,ImageFont
from kit.fonts import find_font

def main():
 out=Path(__file__).resolve().parents[1]/'build/markings';out.mkdir(parents=True,exist_ok=True)
 font=find_font('Noto Sans','Regular')
 for name,size,lines in [('receiver',(1024,256),['PROPANE DEFENSE','HARROW 56   •   PD-H56-029014']),('headstamp',(512,512),['PD','56','29'])]:
  im=Image.new('L',size,0);d=ImageDraw.Draw(im)
  if name=='receiver':
   for y,t in zip((35,145),lines):d.text((32,y),t,font=ImageFont.truetype(font,50),fill=255)
  else:
   for (x,y),t in zip(((205,100),(205,320),(80,210)),lines):d.text((x,y),t,font=ImageFont.truetype(font,58),fill=255)
  im.save(out/(name+'.png'))
 print('Prepared fictional marking masks; unbaked checkpoint does not embed them')
if __name__=='__main__':main()
