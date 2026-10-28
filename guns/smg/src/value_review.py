"""Reference/render display values and native-scale wear, never asset texels."""
from pathlib import Path
import json,math,sys,argparse
import numpy as np
from PIL import Image,ImageDraw,ImageOps,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.photo_match import project
from white_balance import stats
from kit.fonts import find_font

def measure(folder):
 folder=Path(folder);cal=json.loads((BASE/'build/cameras.json').read_text());loci=json.loads((BASE/'build/value-loci.json').read_text());rows={}
 for name,patches in loci.items():
  im=Image.open(folder/(name+'.png')).convert('RGB');shot=cal[name]['shot'];loc=np.array(shot['location']);direction=np.array(shot['target'])-loc
  params=[math.atan2(direction[1],direction[0]),math.atan2(direction[2],np.linalg.norm(direction[:2])),*loc,math.log(shot['lens']),shot['roll']]
  draw=ImageDraw.Draw(im);rows[name]={}
  for key,row in patches.items():
   if key.startswith('polymer_'):continue # these extra regions are measured in both full heroes
   points=project(params,np.array(row['points_m']),im.width,im.height)[0].tolist()
   rows[name][key]=dict(stats(im,points),surface=row,render_polygon=points)
   draw.line(points+[points[0]],fill=('lime' if key.startswith('polymer') else 'orange' if key.startswith('paint') else 'cyan'),width=2)
  im.save(folder/(name+'-values.jpg'),quality=92)
 photo=json.loads((BASE/'build/white-balanced/measurements.json').read_text())
 result=dict(photo=photo,render=rows,scope='display luma 0-255 and median channel ratios; approximate daylight comparison, not recovered albedo',white_balance=json.loads((BASE/'build/white-balanced/corrections.json').read_text()))
 (folder/'values.json').write_text(json.dumps(result,indent=2));return result

def wear_pair():
 out=BASE/'renders/final/pairs';out.mkdir(parents=True,exist_ok=True)
 # Native 1600-wide hero crop, no enlargement or contrast stretch.
 hero=Image.open(BASE/'renders/final/beauty/hero.png').convert('RGBA');bg=Image.new('RGBA',hero.size,(105,108,110,255));bg.alpha_composite(hero)
 # Project actual receiver-envelope corners into the native hero camera.
 shot=json.loads((BASE/'renders/final/beauty/shots.json').read_text())['hero']
 loc=np.array(shot['location']);direction=np.array(shot['target'])-loc
 params=[math.atan2(direction[1],direction[0]),math.atan2(direction[2],np.linalg.norm(direction[:2])),*loc,math.log(shot['lens']),shot.get('roll',0)]
 corners=np.array([(x,y,z) for x in (-.020,.020) for y in (-.040,.190) for z in (.074,.131)])
 pixels=project(params,corners,hero.width,hero.height)[0]
 lo=np.floor(pixels.min(0)).astype(int)-20;hi=np.ceil(pixels.max(0)).astype(int)+20
 crop=bg.convert('RGB').crop((*lo,*hi))
 baseline=project(params,np.array([(-.0164,-.040,.096),(-.0164,.190,.096)]),hero.width,hero.height)[0]
 receiver_pixels=int(round(np.linalg.norm(baseline[1]-baseline[0])))
 photo=Image.open(BASE/'build/white-balanced/navy2.png').convert('RGB')
 ref=photo.crop((1645,245,2735,450));ref=ref.resize((receiver_pixels,round(receiver_pixels*205/1090)),Image.Resampling.LANCZOS)
 width=max(600,crop.width+40);height=max(360,crop.height+245)
 canvas=Image.new('RGB',(width*2,height),(228,229,225));canvas.paste(crop,((width-crop.width)//2,55));canvas.paste(ref,(width+(width-ref.width)//2,80))
 d=ImageDraw.Draw(canvas);d.text((20,15),'Export hero / native pixels / no contrast stretch',fill=(20,30,25));d.text((width+20,15),'Daylight issued receiver / same 230-mm pixel span',fill=(20,30,25))
 measured=json.loads((out/'wear-2d-values.json').read_text())
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),14)
 for x,label,key in [(20,'SHIPPED upper flat','shipping'),(width+20,'PHOTO upper flat','photo')]:
  row=measured[key];wr=row['worn_regions'];pr=row['paint_islands']
  lines=[label+' / common 0.5-mm 2-D grid',
         f"Worn area {row['worn_share']:.1%}; forward / middle / aft: "+' / '.join(f'{v:.0%}' for v in row['thirds_forward_middle_aft']),
         f"Largest worn region contains {wr['largest_share_of_phase']:.1%} of wear",
         f"Paint regions {pr['count']}; enclosed islands {pr['complete_count']}",
         '2-D masks, profiles and region sizes: wear-2d-pair.jpg']
  for i,line in enumerate(lines):d.text((x,height-138+i*24),line,font=font,fill=(20,30,25))
 (out/'native-wear-values.json').write_text(json.dumps(dict(hero_native_size=list(hero.size),hero_crop_native=[*map(int,lo),*map(int,hi)],receiver_baseline_pixels=receiver_pixels,reference_receiver_crop_native=[1645,245,2735,450],reference_assumed_span_mm=230,photo_statistics=measured['photo'],shipping_statistics=measured['shipping'],scope='Native hero crop; photo resized to common receiver span. Statistics use the independent 2-D upper-flat grid in wear-2d-values.json; no 1-D acceptance.'),indent=2))
 canvas.save(out/'native-wear-pair.jpg',quality=94)

def tonal(folder):
 rows={}
 folder=Path(folder)
 for name in json.loads((folder/'shots.json').read_text()):
  path=folder/(name+'.png')
  a=np.asarray(Image.open(path).convert('RGBA'));pixels=a[:,:,:3][a[:,:,3]>128].astype(float);lum=pixels@np.array((.2126,.7152,.0722))
  rows[path.stem]=dict(luma_p1_p50_p99=np.percentile(lum,[1,50,99]).round(2).tolist(),deep_shadow_fraction=float(np.mean(lum<24)),clipped_fraction=float(np.mean(np.all(pixels>=254,axis=1))))
 return rows
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--folder',default=str(BASE/'renders/final/photos'));a=p.parse_args()
 r=measure(a.folder);r['tonal_ranges']=tonal(Path(a.folder).parent/'beauty');(Path(a.folder)/'values.json').write_text(json.dumps(r,indent=2))
 if (BASE/'renders/final/beauty/hero.png').exists():wear_pair()
 print(json.dumps(r['render'],indent=2))
