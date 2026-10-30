"""Observed display values, with explicit photo patches and projected surface loci.

Comparisons allow different light/white balance. They are not recovered albedos.
Only this review process reads reference pixels; the asset generator never does.
"""
from pathlib import Path
import json,math,sys,argparse
import numpy as np
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.photo_match import project

def stats(image,polygon):
 mask=Image.new('L',image.size);ImageDraw.Draw(mask).polygon(polygon,fill=255)
 a=np.asarray(image.convert('RGB'),dtype=float)[np.asarray(mask)>0]
 assert len(a)>0
 rgb=np.median(a,axis=0);luma=a@np.array((.2126,.7152,.0722))
 return dict(pixels=len(a),median_rgb_255=rgb.tolist(),median_luma_255=round(float(np.median(luma)),2),
  luma_p20_p80_255=np.percentile(luma,[20,80]).round(2).tolist(),rgb_ratios_g1=(rgb/max(rgb[1],1)).round(4).tolist())

def neutral_photo(photo):
 # Unclipped white painted wall below the trigger guard, above the wood box.
 # Coordinates were observed on the 2048-wide reference preview. Its aging and
 # reflected light make this an estimated neutral, rather than a gray card.
 rect=[700,240,900,255];scale=photo.width/2048
 box=tuple(round(v*scale) for v in rect)
 rgb=np.asarray(photo,dtype=float)/255
 linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
 x0,y0,x1,y1=box;sample=linear[y0:y1,x0:x1]
 original=np.median(sample,axis=(0,1));target=float(original@np.array((.2126,.7152,.0722)))
 gains=target/original;adapted=linear*gains
 display=np.where(adapted<=.0031308,adapted*12.92,1.055*np.maximum(adapted,0)**(1/2.4)-.055)
 balanced=Image.fromarray(np.uint8(np.clip(display*255+.5,0,255)))
 neutral=np.median(np.asarray(balanced)[y0:y1,x0:x1],axis=(0,1))
 assert max(neutral)-min(neutral)<=1,neutral
 return balanced,dict(neutral='white painted wall below trigger guard; aging/reflections limit neutrality',
  preview_width=2048,preview_rectangle=rect,native_rectangle=box,
  native_median_rgb_255=np.median(np.asarray(photo)[y0:y1,x0:x1],axis=(0,1)).tolist(),
  linear_channel_gains=gains.tolist(),balanced_neutral_rgb_255=neutral.tolist(),
  method='linear sRGB diagonal adaptation preserving neutral-patch luminance; review only')

def measure(folder):
 folder=Path(folder);cal=json.loads((BASE/'build/cameras.json').read_text())['used_photo']
 photo=Image.open(BASE/'refs/daylight-used.jpg').convert('RGB')
 rendered=Image.open(folder/'used_photo.png').convert('RGBA')
 # Picks are expressed on the 2048-wide inspection preview, scaled to original.
 patches={'steel':[(753,99),(860,100),(860,140),(753,139)],
          'stock':[(120,151),(325,145),(325,191),(120,219)],
          'forend':[(1225,181),(1450,194),(1450,215),(1225,202)]}
 loci={
  'steel':[(.01775,y,z) for y,z in [(.085,.040),(.125,.040),(.125,.046),(.085,.046)]],
  'stock':[(.0215,y,z) for y,z in [(-.210,-.028),(-.135,-.028),(-.135,-.018),(-.210,-.018)]],
  'forend':[(.0195,y,z) for y,z in [(.400,.006),(.500,.006),(.500,.018),(.400,.018)]]}
 shot=cal['shot'];loc=np.array(shot['location']);direction=np.array(shot['target'])-loc
 params=[math.atan2(direction[1],direction[0]),math.atan2(direction[2],np.linalg.norm(direction[:2])),*loc,math.log(shot['lens']),shot['roll']]
 rows={};marked=rendered.convert('RGB');annotated=photo.copy();colors=[(240,90,50),(60,180,90),(80,130,240)]
 balanced,balance=neutral_photo(photo);balanced_marked=balanced.copy();neutral_rows={}
 for (name,points),color in zip(patches.items(),colors):
  original=[(x*photo.width/2048,y*photo.width/2048) for x,y in points]
  projected=project(params,np.array(loci[name]),rendered.width,rendered.height)[0].tolist()
  rows[name]=dict(photo=stats(photo,original),render=stats(rendered,projected),photo_polygon=original,render_polygon=projected)
  neutral_rows[name]=dict(photo=stats(balanced,original),render=rows[name]['render'])
  ImageDraw.Draw(annotated).line(original+[original[0]],fill=color,width=6)
  ImageDraw.Draw(balanced_marked).line(original+[original[0]],fill=color,width=6)
  ImageDraw.Draw(marked).line(projected+[projected[0]],fill=color,width=3)
 ImageDraw.Draw(balanced_marked).rectangle(balance['native_rectangle'],outline=(245,190,30),width=6)
 canvas=Image.new('RGB',(1600,650),(225,226,222))
 for i,im in enumerate((marked,annotated.crop(cal['crop']))):
  im.thumbnail((1580,290),Image.Resampling.LANCZOS);canvas.paste(im,((1600-im.width)//2,40+i*310))
 ImageDraw.Draw(canvas).text((12,10),'Used daylight comparison / orange steel, green stock, blue forend / display values, not recovered albedo',fill=(20,30,25))
 canvas.save(folder/'value-patches.jpg',quality=92,optimize=True)
 neutral_canvas=Image.new('RGB',(1600,650),(225,226,222))
 for i,im in enumerate((marked,balanced_marked.crop(cal['crop']))):
  im=im.copy();im.thumbnail((1580,290),Image.Resampling.LANCZOS);neutral_canvas.paste(im,((1600-im.width)//2,40+i*310))
 ImageDraw.Draw(neutral_canvas).text((12,10),'Export / photo balanced on white painted wall below trigger guard; estimated neutral, different light',fill=(20,30,25))
 neutral_canvas.save(folder/'value-patches-neutral.jpg',quality=92,optimize=True)
 tonal={}
 for name in ('hero','hero_left','receiver','wrist','forend','open','aimed'):
  path=folder/(name+'.png')
  if not path.exists():continue
  a=np.asarray(Image.open(path).convert('RGBA'));rgb=a[:,:,:3][a[:,:,3]>128].astype(float)
  luma=rgb@np.array((.2126,.7152,.0722))
  tonal[name]=dict(luma_p1_p50_p99=np.percentile(luma,[1,50,99]).round(2).tolist(),
   deep_shadow_fraction=float(np.mean(luma<24)),clipped_fraction=float(np.mean(np.all(rgb>=254,axis=1))))
 result=dict(scope='display-view medians and G-normalized hue; no photometric recovery',
  primary_reference='daylight-used.jpg: steel, stock and forend are the same photographed gun',
  patches=rows,white_balance=balance,balanced_patches=neutral_rows,tonal_ranges=tonal)
 secondary=Image.open(BASE/'refs/right.jpg').convert('RGB')
 secondary_picks={'steel':[(462,805),(514,849),(500,875),(446,829)],
                  'stock':[(712,1010),(885,1118),(835,1174),(671,1052)]}
 result['secondary_daylight']={name:stats(secondary,[(x*secondary.width/1926,y*secondary.width/1926) for x,y in polygon])
  for name,polygon in secondary_picks.items()}
 result['secondary_scope']='US DoD foreground pump gun outdoors; reflected sky makes steel brighter. Separate view/light, hue/value range cross-check only.'
 (folder/'values.json').write_text(json.dumps(result,indent=2));return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--renders',required=True);a=p.parse_args();measure(a.renders)
