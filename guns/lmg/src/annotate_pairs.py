"""Numbered arrows at measured/photo-projected landmarks, comparison only."""
import json,sys,runpy,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1]

def main():
 out=BASE/'renders/checkpoint/pairs';cal=json.loads((BASE/'build/cameras.json').read_text())
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),19)
 for name,row in cal.items():
  path=out/(name+'-pair.jpg');im=Image.open(path).convert('RGB');d=ImageDraw.Draw(im)
  width=im.width//2;scale=width/(row['crop'][2]-row['crop'][0])
  for side,key in [(0,'projected_pixels'),(1,'measured_pixels')]:
   for i,p in enumerate(row[key]):
    x=side*width+p[0]*scale;y=70+p[1]*scale
    if not (side*width+8<x<(side+1)*width-8 and 80<y<im.height-60):continue
    dx,dy=(-30 if i%2 else 30),(-27 if i%3 else 27)
    tail=(x+dx,y+dy);d.line((tail,(x,y)),fill=(75,201,174),width=2)
    angle=math.atan2(-dy,-dx)
    a=(x-9*math.cos(angle-.45),y-9*math.sin(angle-.45));b=(x-9*math.cos(angle+.45),y-9*math.sin(angle+.45))
    d.polygon([(x,y),a,b],fill=(75,201,174));d.text(tail,str(i+1),font=font,fill=(20,30,26),stroke_width=2,stroke_fill=(234,239,232),anchor='mm')
  if name=='right_photo':
   from kit.photo_match import project
   reference=json.loads((BASE/'build/reference-measurements.json').read_text())
   measured=json.loads((BASE/'build/form-round2.json').read_text())
   photo=reference['stock'];section=measured['stock_sections_mm']
   s=row['shot'];location=np.array(s['location']);direction=np.array(s['target'])-location;direction/=np.linalg.norm(direction)
   parameters=np.r_[math.atan2(direction[1],direction[0]),math.atan2(direction[2],np.linalg.norm(direction[:2])),location,math.log(s['lens']),s['roll']]
   for index,(label,ref) in enumerate(photo.items()):
    y=ref['station_y_mm'];key=min(section,key=lambda k:abs(float(k)-y));q=section[key]
    if label in ('butt upper','butt toe'):
     a,b=measured['butt_bounds_mm'];y=(a[1]+b[1])/2
     z=b[2] if label=='butt upper' else a[2]
    else:z=q['comb'] if label.startswith('comb') else q['bottom']
    uv,_,_=project(parameters,np.array([[0,y*.001,z*.001]]),row['crop'][2]-row['crop'][0],row['crop'][3]-row['crop'][1])
    targets=[uv[0],np.array(ref['pixel'])-np.array(row['crop'][:2])]
    for side,pixel in enumerate(targets):
     x=side*width+pixel[0]*scale;y=70+pixel[1]*scale
     dx,dy=(32,35) if index%2 else (25,-40)
     d.line([(x+dx,y+dy),(x,y)],fill=(239,180,65),width=3)
     d.ellipse((x-4,y-4,x+4,y+4),outline=(239,180,65),width=3)
     d.text((x+dx,y+dy),chr(65+index),font=font,fill=(25,35,28),stroke_fill=(238,241,233),stroke_width=2)
   panel=Image.new('RGB',(im.width,im.height+46),(238,239,236));panel.paste(im,(0,0));d=ImageDraw.Draw(panel)
   d.text((18,im.height+10),'Stock A comb rear · B comb front · C butt upper · D toe · E lower edge at grip (amber)',font=font,fill=(25,45,35));im=panel
  im.save(path,quality=94,optimize=True)
 print('ANNOTATED',len(cal),'pairs; green arrows show geometric/photo landmarks, RMS retained')
if __name__=='__main__':main()
