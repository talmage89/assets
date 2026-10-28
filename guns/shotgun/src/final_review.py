"""Current-GLB provenance, full review sheets, playback audit and final JPGs."""
from pathlib import Path
import sys,json,hashlib,argparse,math
from PIL import Image,ImageDraw,ImageFont,ImageOps
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from value_review import measure
OUT=BASE/'renders/final';font=ImageFont.truetype(find_font('Noto Sans','Regular'),21)
BEAUTY=OUT/'beauty'

def panel(path,size,bg=(59,62,66)):
 im=Image.open(path).convert('RGBA');im.thumbnail(size,Image.Resampling.LANCZOS)
 result=Image.new('RGBA',size,(*bg,255));result.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2))
 return result.convert('RGB')
def sheet(items,path,columns=2,width=1600,height=440):
 rows=math.ceil(len(items)/columns);cell=width//columns
 im=Image.new('RGB',(width,rows*height),(225,226,222));d=ImageDraw.Draw(im)
 for i,(title,p) in enumerate(items):
  x=i%columns*cell;y=i//columns*height
  im.paste(panel(p,(cell-16,height-46)),(x+8,y+38));d.text((x+12,y+7),title,font=font,fill=(20,28,24))
 path.parent.mkdir(parents=True,exist_ok=True);im.save(path,quality=92,optimize=True)
 return im
def doc(im,path):
 im=im.copy();im.thumbnail((1600,10000),Image.Resampling.LANCZOS)
 for quality in (90,86,82,78,74,70,65):
  im.save(path,quality=quality,optimize=True)
  if path.stat().st_size<=200000:break
 assert path.stat().st_size<=200000

def main():
 p=argparse.ArgumentParser();p.add_argument('--docs',action='store_true');a=p.parse_args()
 records=[]
 for meta in OUT.rglob('shots.json'):
  for name,row in json.loads(meta.read_text()).items():
   source=Path(row['source'])
   if source.suffix!='.glb':continue # source comparisons have separate metadata.
   canonical=BASE/'export'/source.name
   assert row['sha256']==hashlib.sha256(canonical.read_bytes()).hexdigest(),(meta,name,'stale image')
   assert (meta.parent/(name+'.png')).exists()
   records.append(dict(folder=str(meta.parent.relative_to(OUT)),shot=name,sha256=row['sha256'],engine=row['engine']))
 timing=json.loads((OUT/'strips/timing.json').read_text());playback={}
 for name,row in timing.items():
  with Image.open(OUT/'strips'/(name+'.webp')) as im:
   total=0
   for i in range(im.n_frames):im.seek(i);im.load();total+=im.info.get('duration',0)
   assert total==row['duration_ms'],(name,total,row['duration_ms'])
   playback[name]=dict(frames=im.n_frames,decoded_duration_ms=total,expected_ms=row['duration_ms'])
 (BASE/'build/final-provenance.json').write_text(json.dumps(dict(passed=True,image_records=len(records),images=records,playback=playback),indent=2))
 values=measure(OUT/'photos')
 # Copy hero tonal evidence into the final value report as well.
 import numpy as np
 for name in ('hero','hero_left','receiver','wrist','forend','open','aimed'):
  pixels=np.asarray(Image.open(BEAUTY/(name+'.png')).convert('RGBA'));rgb=pixels[:,:,:3][pixels[:,:,3]>128].astype(float)
  luma=rgb@np.array((.2126,.7152,.0722))
  values['tonal_ranges'][name]=dict(luma_p1_p50_p99=np.percentile(luma,[1,50,99]).round(2).tolist(),
   deep_shadow_fraction=float(np.mean(luma<24)),clipped_fraction=float(np.mean(np.all(rgb>=254,axis=1))))
 (OUT/'photos/values.json').write_text(json.dumps(values,indent=2))
 names=['hero','hero_left','front','side','back','top','receiver','wrist','forend','aimed','open','scale','muzzle','stock','guard','underside','pad','aimed_socket','muzzle_under','trigger_right','trigger_quarter','trigger_pulled']
 items=[(n,BEAUTY/(n+'.png')) for n in names]
 items += [('Eevee hero',OUT/'eevee/hero.png'),('Loaded shell',OUT/'shell/shell.png'),
  ('Fold crimp',OUT/'shell/shell_crimp.png'),('Fired hull',OUT/'hull/hull.png'),('Struck primer',OUT/'hull/hull_primer.png')]
 sheet(items,OUT/'contact-sheet.jpg',columns=3,width=1800,height=350)
 turn=sheet([(n,BEAUTY/(n+'.png')) for n in ('front','side','back','top')],OUT/'turnaround.jpg',height=470)
 details=sheet([(n,BEAUTY/(n+'.png')) for n in ('receiver','wrist','forend','pad','trigger_right','trigger_quarter')],OUT/'details.jpg',columns=1,height=560)
 action=sheet([('Shell on the raised carrier',BEAUTY/'open.png'),('Exact Socket_Eye / 70 degrees horizontal',BEAUTY/'aimed.png'),
  ('Loaded shell / fictional headstamp',OUT/'shell/shell.png'),('Fired hull / sooted mouth',OUT/'hull/hull.png')],OUT/'action.jpg',height=480)
 sheet([(n,OUT/'pairs'/(n+'_photo-pair.jpg')) for n in ('right','left','open','used','wood','hero-wear')],OUT/'photo-pairs.jpg',columns=1,height=400)
 sheet([(n,OUT/'strips'/(n+'.jpg')) for n in ('Fire','FireLast','Reload','ReloadEmpty','Inspect')],OUT/'clips.jpg',columns=1,height=550)
 # Full-frame inspection panels contain every rendered strip sample, not only keys.
 samples=[]
 for name in timing:
  folder=OUT/'strips'/name
  for frame,row in json.loads((folder/'shots.json').read_text()).items():
   samples.append((f'{name} / {row["time_s"]:.3f} s',folder/(frame+'.png')))
 for index in range(0,len(samples),24):
  sheet(samples[index:index+24],BASE/'build/inspection'/f'clips-{index//24:02d}.jpg',columns=4,width=1600,height=310)
 if a.docs:
  docs=BASE/'docs';docs.mkdir(exist_ok=True)
  doc(panel(BEAUTY/'hero.png',(1600,600)),docs/'hero.jpg')
  doc(turn,docs/'turnaround.jpg');doc(details,docs/'details.jpg');doc(action,docs/'action.jpg')
  doc(panel(OUT/'eevee/hero.png',(1600,600)),docs/'eevee.jpg')
 print('FINAL PROVENANCE',len(records),'images;',len(playback),'real-duration clips;',OUT/'contact-sheet.jpg',flush=True)
if __name__=='__main__':main()
