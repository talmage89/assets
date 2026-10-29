"""Sparse round-three photo observations, independent of generated mesh data.

The absolute baselines below are explicit visual-scale assumptions. These are
uncertain exterior estimates, not caliper measurements or fabrication data.
No photograph or measured polyline enters the geometry/texture generators.
"""
import json, math, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from kit.fonts import find_font
BASE = Path(__file__).resolve().parents[1]
OBS = [
 dict(photo='museum.jpg', crop=(1050,50,1250,190), title='Installed rear saddle / side',
      segments=[('shoulder', (1125,89), (1125,128.5)),
                ('hinge', (1190,71), (1190,128.5))],
      scale=255/559, uncertainty=.22,
      baseline='255 mm accepted receiver span / 559 native px',
      limit='Barrel upper line is occluded: inferred from accepted barrel/receiver datum; ±4–6 mm.'),
 dict(photo='rear-sight.jpg', crop=(1600,1250,2280,1800), title='Leaf and notch / Commons macro',
      segments=[('leaf', (1870,1510), (2020,1370)),
                ('notch crosspiece', (1900,1660), (2225,1370)),
                ('saddle baseline', (1730,1665), (2135,1330))],
      scale=33/math.hypot(405,335), uncertainty=.16,
      baseline='33 mm saddle baseline assumption, inset within accepted 35 mm receiver',
      limit='Different surface heights/perspective; widths are conditional estimates, not independent scale proof.'),
 dict(photo='front-behind.jpg', crop=(560,140,1080,520), title='Hood sheet edge / sharp rear',
      segments=[('sheet edge', (638,218), (664,218))],
      scale=23/451, uncertainty=.40,
      baseline='23 mm accepted exterior collar scale / 451 native px',
      limit='Sheet edge is tilted and paint/wear obscure its boundary; approximately ±0.5 mm.'),
 dict(photo='front-side.jpg', crop=(750,130,1220,840), title='Broad hood ear / sharp side',
      segments=[('band depth', (793,385), (1167,385)),
                ('drum baseline', (813,650), (1080,650))],
      scale=9/267, uncertainty=.16,
      baseline='9 mm visual drum baseline assumption / 267 native px',
      limit='Near-side drum and hood have different depth; approximately ±2 mm.'),
]

def main():
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),21)
 small=ImageFont.truetype(find_font('Noto Sans','Regular'),16)
 sheet=Image.new('RGB',(1800,1650),(238,239,236));draw=ImageDraw.Draw(sheet)
 draw.text((20,12),'Round 3 / sparse photo observations / uncertain visual scale',font=font,fill='black')
 rows=[]
 for i,obs in enumerate(OBS):
  x=(i%2)*900+20;y=(i//2)*800+55;crop=obs['crop']
  im=Image.open(BASE/'build/white-balanced'/obs['photo']).convert('RGB').crop(crop)
  scale=min(850/im.width,535/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)))
  sheet.paste(im,(x,y+30));draw.text((x,y),obs['title'],font=font,fill='black')
  values=[]
  for j,(label,a,b) in enumerate(obs['segments']):
   color=[(240,70,25),(20,130,190),(180,40,180)][j]
   q=[(x+(p[0]-crop[0])*scale,y+30+(p[1]-crop[1])*scale) for p in (a,b)]
   draw.line(q,fill=color,width=3)
   for xx,yy in q:draw.ellipse((xx-4,yy-4,xx+4,yy+4),fill=color)
   px=math.dist(a,b);mm=px*obs['scale']
   values.append(dict(label=label,endpoints_native_px=[a,b],pixels=px,estimated_mm=mm))
   draw.text((x,y+580+j*25),f'{label}: {px:.1f} px / {mm:.1f} mm (±{obs["uncertainty"]*100:.0f}%)',font=small,fill=color)
  draw.text((x,y+670),obs['photo']+' / '+obs['baseline'],font=small,fill='black')
  # Two lines keep the qualification readable on the observation sheet.
  words=obs['limit'].split();line='';yy=y+698
  for word in words:
   if len(line)+len(word)>94:draw.text((x,yy),line,font=small,fill='black');yy+=24;line=''
   line+=word+' '
  draw.text((x,yy),line,font=small,fill='black')
  rows.append(dict(obs,measurements=values))
 (BASE/'build/round3-photo-observations.json').write_text(json.dumps(rows,indent=2))
 sheet.save(BASE/'renders/checkpoint/form-observations.jpg',quality=93)
 print('ROUND 3 PHOTO ESTIMATES',[(r['photo'],[(m['label'],round(m['estimated_mm'],2)) for m in r['measurements']]) for r in rows])

if __name__=='__main__': main()
