"""Observed photo/display values; independent of asset/material generation."""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.photo_match import project
from kit.fonts import find_font

def projection(shot,points,size):
 loc=np.asarray(shot['location']);delta=np.asarray(shot['target'])-loc
 params=[math.atan2(delta[1],delta[0]),math.atan2(delta[2],np.linalg.norm(delta[:2])),*loc,math.log(shot['lens']),shot.get('roll',0)]
 return project(params,np.asarray(points),*size)[0]

def stats(im,polygon):
 mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon([tuple(p) for p in polygon],fill=255)
 rgb=np.asarray(im.convert('RGB'),dtype=float)[np.asarray(mask)>0]
 assert len(rgb)
 median=np.median(rgb,axis=0);luma=rgb@np.array((.2126,.7152,.0722))
 return dict(pixels=len(rgb),median_rgb=median.tolist(),median_luma=float(np.median(luma)),
             luma_p20_p80=np.percentile(luma,[20,80]).tolist(),ratios_g1=(median/max(median[1],1)).tolist())

PATCHES={
 'receiver':('used_photo',[(435,213),(605,207),(607,233),(433,242)],[(.01575,y,z) for y,z in [(.10,.028),(.17,.028),(.17,.040),(.10,.040)]]),
 'wrist':('used_photo',[(118,267),(231,248),(236,268),(121,291)],[(.014,y,z) for y,z in [(-.018,.010),(.025,.010),(.025,.020),(-.018,.020)]]),
 'forend':('used_photo',[(783,228),(972,221),(972,242),(784,248)],[(.018,y,z) for y,z in [(.244,.012),(.320,.012),(.320,.025),(.244,.025)]]),
 'stock':('right_photo',[(400,407),(605,380),(610,415),(405,457)],[(.020,y,z) for y,z in [(-.22,-.055),(-.135,-.03),(-.135,-.012),(-.22,-.025)]]),
}

def measure(folder):
 folder=Path(folder);meta=json.loads((folder/'shots.json').read_text());cameras=json.loads((BASE/'build/cameras.json').read_text())
 rows={};panels=[]
 for name,(shot,polygon,points) in PATCHES.items():
  if shot not in meta:continue
  cal=cameras[shot];photo=Image.open(cal['photo']).convert('RGB');render=Image.open(folder/(shot+'.png')).convert('RGB')
  projected=projection(meta[shot],points,render.size).tolist()
  rows[name]=dict(photo=stats(photo,polygon),render=stats(render,projected),photo_polygon=polygon,render_polygon=projected,
                 reference=Path(cal['photo']).name)
  for im,poly in ((photo,polygon),(render,projected)):
   ImageDraw.Draw(im).polygon([tuple(p) for p in poly],outline=(255,95,40),width=3)
  photo=photo.crop(cal['crop']);panels.append((name,render,photo))
 if panels:
  sheet=Image.new('RGB',(1600,len(panels)*300),(230,230,225));d=ImageDraw.Draw(sheet)
  font=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
  for i,(name,render,photo) in enumerate(panels):
   d.text((12,i*300+8),name+' / rendered and white-balanced photograph / orange sampling polygons',font=font,fill='black')
   for j,im in enumerate((render,photo)):
    im.thumbnail((790,255),Image.Resampling.LANCZOS);sheet.paste(im,(j*800+(800-im.width)//2,i*300+40))
  sheet.save(folder/'value-patches.jpg',quality=93,optimize=True)
 result=dict(scope='Observed display values under estimated comparable views; not recovered albedos. Reflected light and estimated neutrals remain limitations.',patches=rows)
 (folder/'values.json').write_text(json.dumps(result,indent=2));return result

def tonal(folder):
 rows={}
 for name in ('hero','hero_left','receiver','wrist','forend','open'):
  path=Path(folder)/(name+'.png')
  if not path.exists():continue
  rgba=np.asarray(Image.open(path).convert('RGBA'));rgb=rgba[:,:,:3][rgba[:,:,3]>128].astype(float)
  luma=rgb@np.array((.2126,.7152,.0722))
  rows[name]=dict(luma_p1_p50_p99=np.percentile(luma,[1,50,99]).tolist(),deep_shadow_fraction=float(np.mean(luma<24)),clipped_fraction=float(np.mean(np.all(rgb>=254,axis=1))))
 return rows
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--renders',required=True);a=p.parse_args();print(json.dumps(measure(a.renders),indent=2))
