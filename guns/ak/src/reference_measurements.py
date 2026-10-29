"""Sparse photographic form observations, never a mesh/texture input.

The two references differ in perspective and surface depth. Pixel estimates are
reported as uncertain visual comparisons, separately from game-mesh measurements.
"""
import json,math,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1]
OBSERVATIONS=[dict(photo='museum.jpg',crop=(720,230,890,335),
 points=[(772,252),(770,276),(792,301)],scale_mm_per_pixel=255/559,
 baseline='255 mm exterior receiver span / 559 native pixels'),
 dict(photo='trigger-sharp.jpg',crop=(3040,1040,3270,1250),
 points=[(3150,1090),(3153,1150),(3094,1216)],scale_mm_per_pixel=36/210,
 baseline='36 mm receiver-side height / about 210 native pixels')]
def main():
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
 out=BASE/'renders/checkpoint';out.mkdir(parents=True,exist_ok=True)
 sheet=Image.new('RGB',(1600,1050),(238,239,236));draw=ImageDraw.Draw(sheet);rows=[]
 draw.text((20,12),'Trigger observations / balanced reference photos / sparse points only',font=font,fill='black')
 for i,obs in enumerate(OBSERVATIONS):
  points=obs['points'];a,b,c=points;dx,dy=c[0]-a[0],c[1]-a[1]
  bow=abs(dx*(b[1]-a[1])-dy*(b[0]-a[0]))/math.hypot(dx,dy)
  row=dict(obs,projected_height_mm=abs(dy)*obs['scale_mm_per_pixel'],
   three_point_chord_bow_mm=bow*obs['scale_mm_per_pixel'],
   sparse_projected_depth_mm=(max(p[0] for p in points)-min(p[0] for p in points))*obs['scale_mm_per_pixel'],
   relative_uncertainty=.20,limits='blur, perspective and center-plane depth; not orthographic metrology')
  rows.append(row);crop=obs['crop'];im=Image.open(BASE/'build/white-balanced'/obs['photo']).convert('RGB').crop(crop)
  im.thumbnail((740,700));scale=min(740/(crop[2]-crop[0]),700/(crop[3]-crop[1]));im=im.resize((round((crop[2]-crop[0])*scale),round((crop[3]-crop[1])*scale)))
  x=i*800+25;y=60;sheet.paste(im,(x,y))
  for j,p in enumerate(points):
   xx=x+(p[0]-crop[0])*scale;yy=y+(p[1]-crop[1])*scale
   draw.ellipse((xx-5,yy-5,xx+5,yy+5),outline=(210,50,25),width=2);draw.text((xx+8,yy-12),str(j+1),font=font,fill=(230,90,30))
  draw.text((x,790),obs['photo']+' / '+obs['baseline'],font=font,fill='black')
  draw.text((x,825),f"Height {row['projected_height_mm']:.1f} mm; bow {row['three_point_chord_bow_mm']:.1f} mm; ±20%",font=font,fill='black')
  draw.text((x,860),f"Sparse-point projected depth {row['sparse_projected_depth_mm']:.1f} mm; includes perspective",font=font,fill='black')
 model=json.loads((BASE/'build/form-measurements.json').read_text());t=model['trigger'];g=model['guard']
 draw.text((25,900),f"Actual game mesh: blade height {t['envelope_mm'][2]:.2f} mm; side depth {t['envelope_mm'][1]:.2f} mm; section-center bow {t['maximum_chord_bow_mm']:.2f} mm",font=font,fill='black')
 draw.text((25,940),f"Actual guard section at Y30: {g['section_xz_mm'][0]:.2f} × {g['section_xz_mm'][1]:.2f} mm. Oblique references support a broad flat band, not round wire.",font=font,fill='black')
 draw.text((25,985),'Across-band width cannot be separated from gauge in a side photograph alone; both oblique views and the actual section are required.',font=font,fill='black')
 sheet.save(out/'trigger-measurements.jpg',quality=93)
 (BASE/'build/reference-measurements.json').write_text(json.dumps(rows,indent=2))
 print('TRIGGER PHOTOS',[(r['projected_height_mm'],r['three_point_chord_bow_mm']) for r in rows])
if __name__=='__main__':main()
