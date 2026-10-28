"""Native hero receiver versus used daylight photo at equal receiver pixel scale.

Reference pixels are read only here, never by the material or baking pipeline.
The photographed port lip is compared with a projected patch on our actual lip.
Display values include the different lighting; they are not recovered albedos.
"""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.photo_match import project
from kit.fonts import find_font
from value_review import stats

def projection(shot,points,size):
 loc=np.array(shot['location']);direction=np.array(shot['target'])-loc
 params=[math.atan2(direction[1],direction[0]),math.atan2(direction[2],np.linalg.norm(direction[:2])),*loc,math.log(shot['lens']),shot.get('roll',0)]
 return project(params,np.array(points),*size)[0]

def main():
 p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,default=BASE/'renders/final/beauty')
 p.add_argument('--out',type=Path,default=BASE/'renders/final/pairs');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 hero=Image.open(a.renders/'hero.png').convert('RGBA');shot=json.loads((a.renders/'shots.json').read_text())['hero']
 photo=Image.open(BASE/'refs/daylight-used.jpg').convert('RGB')
 # Observed receiver end-to-end extent, excluding furniture and barrel.
 photo_extent=(1588,2518)
 ends=projection(shot,[(.0171,.037,.033),(.0167,.250,.033)],hero.size)
 scale=float(np.linalg.norm(ends[1]-ends[0])/(photo_extent[1]-photo_extent[0]))
 crop=(1540,130,2550,480);pc=photo.crop(crop);pc=pc.resize((round(pc.width*scale),round(pc.height*scale)),Image.Resampling.LANCZOS)
 # Preserve native hero pixels; composite its transparency onto docs gray.
 bounds=(500,135,825,290);hc=Image.new('RGBA',hero.size,(59,62,66,255));hc.alpha_composite(hero);hc=hc.convert('RGB').crop(bounds)
 # Independently observed narrow worn lower lip; avoid the bright bolt face.
 photo_poly=[(2140,295),(2360,317),(2360,322),(2140,300)]
 local=[((x-crop[0])*scale,(y-crop[1])*scale) for x,y in photo_poly]
 points=[(.01775,y,z) for y,z in ((.158,.0344),(.216,.0344),(.216,.0350),(.158,.0350))]
 render_poly=projection(shot,points,hero.size).tolist()
 native_photo=stats(pc,local);render=stats(hero,render_poly)
 rows=dict(scope='display sRGB, same receiver pixel scale; different light and lens; not recovered albedo',
  photo='daylight-used.jpg / Everett Walker / CC BY-SA 4.0',
  photo_receiver_extent_px=photo_extent,hero_projected_receiver_length_px=float(np.linalg.norm(ends[1]-ends[0])),
  photo_resize_scale=scale,photo_polygon_original=photo_poly,hero_polygon=render_poly,
  worn_lower_port_lip=dict(photo_at_hero_scale=native_photo,hero=render),
  band_05_to_2mm_projected_px=(np.linalg.norm(ends[1]-ends[0])/.213*np.array((.0005,.002))).tolist())
 canvas=Image.new('RGB',(760,450),(225,226,222));d=ImageDraw.Draw(canvas);font=ImageFont.truetype(find_font('Noto Sans','Regular'),17)
 d.text((12,8),'Hero crop: native pixels',font=font,fill=(20,28,24));d.text((392,8),'Used daylight: same receiver scale',font=font,fill=(20,28,24))
 canvas.paste(hc,(12,38));canvas.paste(pc,(392,38))
 d.text((12,204),'3x nearest-neighbor inspection (same pixels, no added detail)',font=font,fill=(20,28,24))
 # Center both enlargements on the measured lower lip, not the middle of
 # differently cropped rectangles; each contains the same 120 x 60 pixels.
 centers=(np.mean(render_poly,axis=0)-np.array(bounds[:2]),np.mean(local,axis=0))
 for (x,im),(cx,cy) in zip(((12,hc),(392,pc)),centers):
  cx,cy=round(float(cx)),round(float(cy));center=im.crop((cx-60,cy-30,cx+60,cy+30))
  canvas.paste(center.resize((360,180),Image.Resampling.NEAREST),(x,234))
 d.text((12,424),'Original shorter utility receiver / different field sights in photo; comparison only',font=font,fill=(20,28,24))
 canvas.save(a.out/'hero-wear_photo-pair.jpg',quality=94,optimize=True)
 (a.out/'hero-wear-values.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows),flush=True)

if __name__=='__main__':main()
