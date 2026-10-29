"""Reproducible visual gauges; no reference pixels enter the asset pipeline.

Scale is estimated locally from the existing class-envelope camera fit, not
claimed as a manufacturer measurement. Pixel placement and perspective/class
uncertainty are explicit in REFERENCE.md. The model is independently ray-gauged.
"""
import hashlib,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.photo_match import project
from kit.fonts import find_font

def main():
 camera=json.loads((BASE/'build/photo-cameras.json').read_text())['open_photo']
 shot=camera['shot'];c=np.array(shot['location']);forward=np.array(shot['target'])-c;forward/=np.linalg.norm(forward)
 params=np.r_[math.atan2(forward[1],forward[0]),math.atan2(forward[2],np.linalg.norm(forward[:2])),c,math.log(shot['lens']),shot.get('roll',0)]
 w,h=camera['crop'][2]-camera['crop'][0],camera['crop'][3]-camera['crop'][1]
 def scale(point):
  uv,_,_=project(params,np.array([point,np.array(point)+[0,0,.001]]),w,h)
  return float(np.linalg.norm(uv[1]-uv[0]))
 rows={
  'shaft':dict(points=[[1000,874],[1000,969]],local_point_m=[-.03438,.106,.0327],uncertainty_mm=.6),
  'head':dict(points=[[770,865],[770,961]],local_point_m=[-.03438,.123,.0327],uncertainty_mm=.7),
  'spur_near_tip':dict(points=[[2840,455],[2880,539]],local_point_m=[0,-.0075,.072],uncertainty_mm=1.0),
 }
 im=Image.open(BASE/'build/references/open.png').convert('RGB');font=ImageFont.truetype(find_font('Noto Sans','Regular'),23)
 out=BASE/'renders/final/fixes';out.mkdir(parents=True,exist_ok=True)
 for name,row in rows.items():
  row['native_pixel_span']=math.dist(*row['points']);row['local_px_per_mm']=scale(row['local_point_m'])
  row['estimated_mm']=row['native_pixel_span']/row['local_px_per_mm']
  panel=im.copy();d=ImageDraw.Draw(panel);a,b=[tuple(p) for p in row['points']]
  d.line([a,b],fill=(255,60,20),width=3)
  for x,y in (a,b):d.ellipse((x-5,y-5,x+5,y+5),outline=(255,230,20),width=2)
  crop=(680,800,1220,1040) if name!='spur_near_tip' else (2680,420,2970,660)
  panel=panel.crop(crop);panel.thumbnail((1000,650));canvas=Image.new('RGB',(1000,panel.height+90),(235,237,233))
  canvas.paste(panel,(0,60));d=ImageDraw.Draw(canvas)
  d.text((10,8),f"{name}: {row['native_pixel_span']:.1f} native px / {row['local_px_per_mm']:.2f} px/mm = {row['estimated_mm']:.2f} +/- {row['uncertainty_mm']:.1f} mm",font=font,fill=(25,35,30))
  canvas.save(out/(name+'-photo-gauge.jpg'),quality=94,optimize=True)
 result=dict(reference='open.jpg',photo_sha256=hashlib.sha256((BASE/'refs/open.jpg').read_bytes()).hexdigest(),
  camera_landmark_rms_pixels=camera['residual_rms_pixels'],gauges=rows,
  note='Oblique photographic estimates from a class-envelope camera, with substantial systematic uncertainty; not shop dimensions. Red segments are manual visual gauge placements. The spur segment includes its roof/rounded end thickness, rather than the old terminal sliver.')
 (out/'photo-gauges.json').write_text(json.dumps(result,indent=2));print(json.dumps(rows,indent=2))

if __name__=='__main__':main()
