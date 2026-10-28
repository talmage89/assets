"""Dimensioned, equal-scale section plots from the extracted game triangles."""
from pathlib import Path
import sys,json
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1];rows=json.loads((BASE/'build/sections.json').read_text())
font=ImageFont.truetype(find_font('Noto Sans','Regular'),22);small=ImageFont.truetype(find_font('Noto Sans','Regular'),17)
# The final ring section has four legend entries; retain a complete footer.
im=Image.new('RGB',(1800,100+((len(rows)+2)//3)*510),(239,240,235));d=ImageDraw.Draw(im)
d.text((20,16),'Hearth 12 / sections measured on game triangles / all dimensions mm',font=font,fill=(25,35,30))
for i,row in enumerate(rows):
 x=(i%3)*600;y=60+(i//3)*510
 d.text((x+18,y+12),f"{row['region']} | Y {row['station_mm']:g}",font=font,fill=(25,35,30))
 d.text((x+18,y+45),f"{row['width_mm']:.2f} wide × {row['height_mm']:.2f} high",font=small,fill=(35,55,50))
 points=[p for segs in row['parts'].values() for seg in segs for p in seg];cz=(max(p[1] for p in points)+min(p[1] for p in points))/2
 scale=4.3
 def xy(p):return (round(x+300+p[0]*scale),round(y+265-(p[1]-cz)*scale))
 for mm in range(-60,61,10):
  d.line((x+45,y+265+mm*scale,x+550,y+265+mm*scale),fill=(222,225,217))
  d.line((x+300+mm*scale,y+95,x+300+mm*scale,y+447),fill=(222,225,217))
 for j,(name,segs) in enumerate(row['parts'].items()):
  col=[(56,73,81),(151,88,38),(77,113,91),(145,54,44)][j%4]
  for a,b in segs:d.line((*xy(a),*xy(b)),fill=col,width=3)
  d.text((x+15,y+457+j*17),name,font=small,fill=col)
out=BASE/'renders/checkpoint/sections.jpg';out.parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=92)
