"""Whole-visible-part histograms, highlighted masks and photographic pairs.

Measurements use balanced native photographs and masks inverse-mapped from the
review coordinates. Every rendered sample is selected by an independent part-ID
render of the same exported GLB, camera and pose. No finish-selective grading.
"""
import argparse,json,hashlib,sys,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path[:0]=[str(ROOT),str(BASE/'src')]
from look_matches import PHOTOS,FINISHES
from kit.fonts import find_font
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),22)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),16)
LUMA=np.array((.2126,.7152,.0722))

def mask(row,size):
 im=Image.new('L',size);d=ImageDraw.Draw(im)
 for poly in row['polygons']:d.polygon(poly,fill=255)
 for poly in row.get('holes',[]):d.polygon(poly,fill=0)
 return im

def native_mask(im,name,native_size):
 row=PHOTOS[name]
 if not row['angle']:return im.resize(native_size,Image.Resampling.NEAREST)
 # Reverse the exact centering/expansion used by white_balance.py. The source
 # thumbnail never exceeds 1707 px; native metrics retain original RGB pixels.
 w,h=native_size;s=min(1,1707/w);thumb=(round(w*s),round(h*s))
 rotated=Image.new('L',thumb).rotate(row['angle'],expand=True).size
 im=im.resize(rotated,Image.Resampling.NEAREST).rotate(-row['angle'],expand=False,resample=Image.Resampling.NEAREST)
 x=(im.width-thumb[0])//2;y=(im.height-thumb[1])//2
 return im.crop((x,y,x+thumb[0],y+thumb[1])).resize(native_size,Image.Resampling.NEAREST)

def stats(rgb):
 assert len(rgb)>0,'No visible part pixels'
 lum=rgb@LUMA;high=rgb[lum>=np.percentile(lum,95)]
 return dict(pixels=len(rgb),p10=float(np.percentile(lum,10)),median=float(np.median(lum)),p90=float(np.percentile(lum,90)),
  highlight_value=float(np.mean(high@LUMA)),highlight_rgb=np.mean(high,axis=0).tolist(),median_rgb=np.median(rgb,axis=0).tolist())

def panel(im,box,size,bg=(82,85,89)):
 im=im.crop(box).convert('RGBA');scale=min(size[0]/im.width,size[1]/im.height)
 im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS)
 out=Image.new('RGBA',size,(*bg,255));out.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2));return out.convert('RGB')

def main():
 p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,required=True);p.add_argument('--out',type=Path);a=p.parse_args()
 folder=a.folder;out=a.out or folder/'look-review';out.mkdir(parents=True,exist_ok=True)
 ids=json.loads((BASE/'build/look-part-ids.json').read_text());ids={name:int(i) for i,name in ids.items()}
 cameras=json.loads((BASE/'build/look-cameras.json').read_text());balance=json.loads((BASE/'build/look-photos/white-balance.json').read_text())
 meta=json.loads((folder/'photos/shots.json').read_text());mask_meta=json.loads((folder/'cpu-masks/shots.json').read_text())
 results={}
 for name,row in FINISHES.items():
  shot=row['shot'];assert meta[shot]['sha256']==mask_meta[shot]['sha256']
  ref=Image.open(BASE/'build/look-photos'/(row['photo']+'.png')).convert('RGB')
  photo_mask=mask(row,ref.size)
  native=Image.open(BASE/'build/look-photos'/(row['photo']+'-native.png')).convert('RGB')
  original_mask=native_mask(photo_mask,row['photo'],native.size)
  rgb=np.array(native,dtype=float)[np.asarray(original_mask)>0];photo=stats(rgb)
  render=Image.open(folder/'photos'/(shot+'.png')).convert('RGBA')
  labels=np.asarray(Image.open(folder/'cpu-masks'/(shot+'.png')).convert('RGBA'))
  wanted=[ids[n] for n in row['parts']];selected=np.isin(labels[:,:,0],wanted)&(labels[:,:,3]>250)
  selected=np.asarray(Image.fromarray(np.uint8(selected)*255).filter(ImageFilter.MinFilter(3)))>0
  assert selected.any(),(name,'no visible part pixels in the comparison camera')
  actual=stats(np.asarray(render,dtype=float)[:,:,:3][selected])
  errors={k:actual[k]/max(photo[k],1e-5)-1 for k in ('p10','median','p90','highlight_value')}
  color=np.array(actual['highlight_rgb'])/np.maximum(photo['highlight_rgb'],1e-5)-1
  passed=abs(errors['median'])<=.10 and max(abs(errors['p10']),abs(errors['p90']))<=.15 and abs(errors['highlight_value'])<=.10 and max(abs(color))<=.10
  result=dict(photo=photo,ours=actual,relative_errors=errors,highlight_rgb_relative_errors=color.tolist(),passed=bool(passed),
   photo_source=PHOTOS[row['photo']]['file'],white_balance=balance[row['photo']],parts=row['parts'],
   model_sha256=meta[shot]['sha256'],camera=meta[shot],
   note='Whole visible part masks. Disclosed original designs differ; light is an estimate, not photometric recovery.')
  results[name]=result
  # Context and two unobscured surface crops, with separate binary masks.
  w=1800;h=900;sheet=Image.new('RGB',(w,h),(230,231,227));d=ImageDraw.Draw(sheet)
  d.text((18,12),name+' / baked export (left), white-balanced used photograph (right)',font=FONT,fill='black')
  x,y=np.nonzero(selected)[1],np.nonzero(selected)[0];rb=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1))
  refbox=row['crop']
  sheet.paste(panel(render,rb,(880,420)),(10,52));sheet.paste(panel(ref,refbox,(880,420)),(910,52))
  rm=Image.fromarray(np.uint8(selected)*255).convert('RGB');pm=photo_mask.convert('RGB')
  sheet.paste(panel(rm,rb,(880,200),(0,0,0)),(10,482));sheet.paste(panel(pm,refbox,(880,200),(0,0,0)),(910,482))
  y=695
  d.text((18,y),'Whole visible part; median within 10%; P10/P90 within 15%; brightest 5% value and RGB within 10%.',font=SMALL,fill='black')
  for i,(label,key) in enumerate([('P10','p10'),('Median','median'),('P90','p90'),('Highlight','highlight_value')]):
   d.text((18+i*320,y+30),f'{label}: {actual[key]:.1f} / {photo[key]:.1f} ({errors[key]*100:+.1f}%)',font=SMALL,fill='black')
  d.text((18,y+61),'Highlight RGB ours / photo: '+str(np.round(actual['highlight_rgb'],1).tolist())+' / '+str(np.round(photo['highlight_rgb'],1).tolist()),font=SMALL,fill='black')
  d.text((18,y+91),'Neutral: '+balance[row['photo']]['neutral'],font=SMALL,fill='black')
  d.text((18,y+121),('PASS' if passed else 'MISS: see measured errors; no finish acceptance claimed')+'; gray-paper light is estimated; different makers\' geometry is retained.',font=SMALL,fill='black')
  sheet.save(out/(name+'-pair.jpg'),quality=94,optimize=True)
  original_mask.save(out/(name+'-photo-mask.png'));Image.fromarray(np.uint8(selected)*255).save(out/(name+'-render-mask.png'))
 (out/'values.json').write_text(json.dumps(dict(method='Native balanced photograph; independent same-export ID masks; luma Rec.709 on sRGB display values; highlight brightest 5% mean; no exposure scaling of measurements',finishes=results),indent=2))
 print(json.dumps({n:dict(ours=[round(r['ours'][k],1) for k in ('p10','median','p90','highlight_value')],photo=[round(r['photo'][k],1) for k in ('p10','median','p90','highlight_value')],passed=r['passed']) for n,r in results.items()},indent=2))
if __name__=='__main__':main()
