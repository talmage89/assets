"""Median display value and hue in manually picked used-pistol photo regions.

The patches avoid markings, boundaries and specular extremes. These are image
values under different lights, not recovered physical albedos. No image is used
by modeling, look-dev, baking or export.
"""
from pathlib import Path
import argparse,json,math,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parents[1]))
from kit.photo_match import project

RIGHT={
 'slide':[(322,123),(353,123),(353,151),(322,151)],
 'frame':[(520,186),(628,184),(628,207),(520,210)],
 'grip':[(207,328),(238,342),(214,395),(183,379)]}
OPEN={
 'slide':[(276,123),(315,123),(315,146),(276,146)],
 'frame':[(528,195),(630,194),(629,214),(526,216)],
 'grip':[(253,328),(283,341),(259,391),(228,376)]}
LEFT_ORIGINAL={
 'slide':[(493,342),(645,254),(658,278),(507,369)],
 'frame':[(732,341),(800,305),(815,338),(756,367)],
 'grip':[(936,425),(1011,467),(975,532),(894,480)]}

def stats(image,polygon):
 im=np.asarray(image.convert('RGB'),dtype=np.float64)
 mask=Image.new('L',image.size,0);ImageDraw.Draw(mask).polygon(polygon,fill=255)
 pixels=im[np.asarray(mask)>0];med=np.median(pixels,axis=0)
 luma=pixels@np.array((.2126,.7152,.0722))
 return dict(pixels=len(pixels),median_rgb_255=med.round(2).tolist(),
  median_luma_255=round(float(np.median(luma)),2),
  luma_p20_p80_255=np.percentile(luma,[20,80]).round(2).tolist(),
  rgb_ratios_g1=(med/max(med[1],1)).round(4).tolist())

def measure(folder,tonal_folder=None):
 folder=Path(folder);results={};patch_panels=[]
 original=Image.open(BASE/'refs/daylight-side.jpg')
 leveled=Image.open(BASE/'build/left-leveled.jpg')
 def rotate(p):
  x,y=p;x-=original.width/2;y-=original.height/2;t=math.radians(-30)
  return (math.cos(t)*x+math.sin(t)*y+leveled.width/2,-math.sin(t)*x+math.cos(t)*y+leveled.height/2)
 left={k:[rotate(p) for p in points] for k,points in LEFT_ORIGINAL.items()}
 calibration=json.loads((BASE/'build/cameras.json').read_text())
 cases=[('right_photo',BASE/'refs/round2-right.jpg',(60,55,760,535),RIGHT),
        ('open_photo',BASE/'refs/round2-open.jpg',(40,55,755,520),OPEN),
        ('left_photo',BASE/'build/left-leveled.jpg',(135,360,1410,1250),left)]
 colors={'slide':(180,45,20),'frame':(20,140,80),'grip':(40,90,220)}
 for name,path,crop,polygons in cases:
  photo=Image.open(path).convert('RGB');render=Image.open(folder/(name+'.png')).convert('RGB')
  scale=render.width/(crop[2]-crop[0]);rows={}
  annotated=photo.copy();ad=ImageDraw.Draw(annotated)
  marked=render.copy();md=ImageDraw.Draw(marked)
  for surface,points in polygons.items():
   projected=[((x-crop[0])*scale,(y-crop[1])*scale) for x,y in points]
   if surface=='slide':
    # Original markings occupy different positions on the C9. Use an unmarked
    # flat steel patch, projected from an authored station, rather than sampling
    # our lettering or port simply because it shares the photo's screen pixels.
    sign=-1 if name=='left_photo' else 1;shift=-.034 if name=='open_photo' else 0
    y0,y1=(.008,.084) if sign<0 else (.006,.028)
    world=np.array([(sign*.01275,y+shift,z) for y,z in
       [(y0,.0614),(y1,.0614),(y1,.0635),(y0,.0635)]])
    shot=calibration[name]['shot'];loc=np.array(shot['location']);direction=np.array(shot['target'])-loc
    az=math.atan2(direction[1],direction[0]);el=math.atan2(direction[2],np.linalg.norm(direction[:2]))
    params=[az,el,*loc,math.log(shot['lens']),shot['roll']]
    projected=project(params,world,render.width,render.height)[0].tolist()
   rows[surface]=dict(photo=stats(photo,points),render=stats(render,projected))
   ad.line(points+[points[0]],fill=colors[surface],width=3)
   md.line(projected+[projected[0]],fill=colors[surface],width=3)
  results[name]=rows
  pair=Image.new('RGB',(1400,520),(238,239,236))
  for i,im in enumerate((marked,annotated.crop(crop))):
   im.thumbnail((700,480),Image.Resampling.LANCZOS);pair.paste(im,(i*700+(700-im.width)//2,35))
  ImageDraw.Draw(pair).text((12,12),name+' / red: slide, green: frame, blue: textured grip / median RGB and G-normalized ratios in values.json',fill=(20,30,25))
  patch_panels.append(pair)
 tonal={}
 for name in ('hero','hero_left','grip_texture','port_hood'):
  f=Path(tonal_folder or folder)/(name+'.png')
  if not f.exists():continue
  im=np.asarray(Image.open(f).convert('RGB'),dtype=float);luma=im@np.array((.2126,.7152,.0722))
  tonal[name]=dict(full_image_luma_percentiles_255=np.percentile(luma,[0,1,5,50,95,99,100]).round(2).tolist(),
   pixels_all_channels_255=int(np.all(im==255,axis=2).sum()))
 result=dict(scope='display-view values and hue; not recovered albedos',
  method='manual photo polygons; unmarked slide render patch projected from an authored flat station; median channels, median Rec.709 luma, G=1 ratios',
  patches=results,tonal_ranges=tonal)
 (folder/'values.json').write_text(json.dumps(result,indent=2))
 sheet=Image.new('RGB',(1400,520*len(patch_panels)),(238,239,236))
 for i,p in enumerate(patch_panels):sheet.paste(p,(0,i*520))
 sheet.save(folder/'value-patches.jpg',quality=93,optimize=True)
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--renders',required=True);a=p.parse_args();measure(a.renders)
