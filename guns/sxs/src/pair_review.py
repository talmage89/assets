"""Review-only photo outlines and native-pixel landmark vectors.

No output of this module is imported by modeling, materials, or bake sources.
The plain pairs remain unobscured; arrows and the photo silhouette are on a
separate companion panel in each pair. A similarity diagnostic distinguishes
coherent framing from local residuals; it does not certify form acceptance.
"""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.photo_match import compose
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1]
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),16)
def diagnostic(row):
 p=np.array(row['projected_pixels']);q=np.array(row['measured_pixels']);c=p.mean(0);d=q.mean(0)
 # Least-squares translation/scale/roll correction in the review image only.
 a=p-c;b=q-d;den=(a*a).sum();aa=(a*b).sum()/den;bb=(a[:,0]*b[:,1]-a[:,1]*b[:,0]).sum()/den
 mat=np.array([[aa,-bb],[bb,aa]]);fit=a@mat.T+d
 rms=lambda x:float(np.sqrt(np.mean((x*x).sum(axis=1))))
 total=rms(p-q);local=rms(fit-q);coherent=math.sqrt(max(0,total**2-local**2))
 return dict(rms_native_px=total,after_similarity_px=local,coherent_component_px=coherent,
  translation_native_px=(d-c).tolist(),scale=float(math.hypot(aa,bb)),roll_deg=math.degrees(math.atan2(bb,aa)),
  assessment='framing dominant' if coherent>local*1.4 else 'mixed framing/form' if coherent>local*.7 else 'local form/observation dominant',
  vectors=[dict(name=name,render_pixel=x.tolist(),photo_pixel=y.tolist(),delta_px=(y-x).tolist(),length_px=float(np.linalg.norm(y-x)))
   for name,x,y in zip(row.get('landmark_names',[str(i+1) for i in range(len(p))]),p,q)])
def arrow(d,p,q,color):
 d.ellipse((p[0]-4,p[1]-4,p[0]+4,p[1]+4),outline=(0,235,225),width=2)
 d.line((*p,*q),fill=color,width=2);v=np.array(p)-q;n=np.linalg.norm(v)
 if n>2:
  v/=n;side=np.array([-v[1],v[0]]);q=np.array(q)
  d.polygon([tuple(q),tuple(q+v*10+side*4),tuple(q+v*10-side*4)],fill=color)
 d.ellipse((q[0]-3,q[1]-3,q[0]+3,q[1]+3),outline=color,width=2)
def main():
 p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 calibration=BASE/'build/cameras.json';out=Path(a.out);compose(calibration,Path(a.renders),out)
 rows=json.loads(calibration.read_text());report={}
 for name,row in rows.items():
  data=diagnostic(row);report[name]=data
  photo=Image.open(row['photo']).convert('RGB').crop(row['crop']);raw=Image.open(Path(a.renders)/(name+'.png')).convert('RGBA')
  w=1100;h=round(w*photo.height/photo.width);fac=w/photo.width
  raw=raw.resize((w,h),Image.Resampling.LANCZOS);bg=Image.new('RGBA',(w,h),(82,85,89,255));bg.alpha_composite(raw);panel=bg.convert('RGB')
  # Robust review silhouette on the reference's known plain backdrop. Closing
  # fills single-pixel lighting holes; it never changes an asset mesh/texture.
  rgb=np.array(photo);lum=rgb@np.array([.2126,.7152,.0722]);black=np.median(lum[:max(1,photo.height//12)])<60
  mask=Image.fromarray(np.uint8(lum>(12 if black else 0))*255) if black else Image.fromarray(np.uint8(np.min(rgb,axis=2)<190)*255)
  mask=mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
  edge=ImageOps.autocontrast(ImageChops_subtract(mask.filter(ImageFilter.MaxFilter(3)),mask.filter(ImageFilter.MinFilter(3))))
  edge=edge.resize((w,h),Image.Resampling.LANCZOS)
  overlay=Image.new('RGB',(w,h),(255,185,40));panel.paste(overlay,(0,0),edge)
  draw=ImageDraw.Draw(panel)
  for i,(pp,qq) in enumerate(zip(row['projected_pixels'],row['measured_pixels'])):
   pt=np.array(pp)*fac;qt=np.array(qq)*fac;arrow(draw,tuple(pt),tuple(qt),(255,80,110))
   if 0<=pt[0]<w and 0<=pt[1]<h:draw.text((pt[0]+7,pt[1]+2),str(i+1),font=SMALL,fill=(0,255,240),stroke_width=1,stroke_fill='black')
  panel.save(out/(name+'-outline.jpg'),quality=94,optimize=True)
  plain=Image.open(out/(name+'-pair.jpg'));sheet=Image.new('RGB',(plain.width,plain.height+h+105),(238,239,236));sheet.paste(plain,(0,0));sheet.paste(panel,(0,plain.height+66))
  d=ImageDraw.Draw(sheet);y=plain.height+8
  d.text((18,y),'Review only: amber = photo outline; cyan = rendered landmark; pink arrow = residual to photo',font=FONT,fill=(25,36,31))
  d.text((18,y+27),f"Native RMS {data['rms_native_px']:.1f}px; similarity remainder {data['after_similarity_px']:.1f}px / {data['assessment']}",font=FONT,fill=(25,36,31))
  y=plain.height+82
  for i,v in enumerate(data['vectors']):
   d.text((w+20,y+i*27),f"{i+1}. {v['name']}: {v['length_px']:.1f}px",font=SMALL,fill=(25,36,31))
  d.text((w+20,y+(len(data['vectors'])+1)*27),'EXIF unavailable; macro review lens fixed at 150 mm.',font=SMALL,fill=(25,36,31))
  sheet.save(out/(name+'-pair.jpg'),quality=94,optimize=True)
 (out/'residuals.json').write_text(json.dumps(report,indent=2))
def ImageChops_subtract(a,b):
 from PIL import ImageChops
 return ImageChops.subtract(a,b)
if __name__=='__main__':main()
