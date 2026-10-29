"""Final GLB provenance, inspection sheets and uncommitted docs JPGs."""
import argparse,hashlib,json,math,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.fonts import find_font
from value_review import measure,tonal
from interface import CLIPS
from ammo_review import main as ammo_values
OUT=BASE/'renders/final';FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),20)

def panel(path,size):
 im=Image.open(path).convert('RGBA');im.thumbnail(size,Image.Resampling.LANCZOS)
 result=Image.new('RGBA',size,(65,67,70,255));result.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2))
 return result.convert('RGB')

def sheet(items,path,columns=2,width=1600,height=450):
 rows=math.ceil(len(items)/columns);cell=width//columns
 im=Image.new('RGB',(width,rows*height),(230,230,225));d=ImageDraw.Draw(im)
 for i,(name,file) in enumerate(items):
  x=i%columns*cell;y=i//columns*height
  d.text((x+12,y+7),name,font=FONT,fill=(20,24,28));im.paste(panel(file,(cell-16,height-45)),(x+8,y+37))
 path.parent.mkdir(parents=True,exist_ok=True);im.save(path,quality=92,optimize=True);return im

def doc(im,path):
 im=im.copy();im.thumbnail((1600,10000),Image.Resampling.LANCZOS)
 for q in (92,88,84,80,76,72,68,64,58):
  im.save(path,quality=q,optimize=True)
  if path.stat().st_size<=200000:break
 assert path.stat().st_size<=200000

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--docs',action='store_true');a=parser.parse_args()
 beauty=OUT/'beauty';records=[]
 panel(beauty/'hero.png',(1600,605)).save(OUT/'hero-gray.jpg',quality=94,optimize=True)
 for metadata in OUT.rglob('shots.json'):
  for name,row in json.loads(metadata.read_text()).items():
   if Path(row['source']).suffix!='.glb':continue
   source=BASE/'export'/Path(row['source']).name
   assert row['sha256']==hashlib.sha256(source.read_bytes()).hexdigest(),(metadata,name,'stale GLB render')
   assert (metadata.parent/(name+'.png')).exists()
   records.append(dict(image=str((metadata.parent/(name+'.png')).relative_to(BASE)),source=source.name,sha256=row['sha256'],engine=row['engine']))
 timing=json.loads((OUT/'strips/timing.json').read_text());assert set(timing)==set(CLIPS);playback={};unique={}
 for name,clip in CLIPS.items():
  with Image.open(OUT/'strips'/(name+'.webp')) as im:
   duration=0
   for i in range(im.n_frames):im.seek(i);im.load();duration+=im.info.get('duration',0)
   assert duration==round(clip['frames']/60*1000)==timing[name]['encoded_duration_ms']
   playback[name]=dict(decoded_duration_ms=duration,frames=im.n_frames)
  metadata=json.loads((OUT/'strips'/name/'shots.json').read_text())
  for frame,row in metadata.items():
   file=OUT/'strips'/name/(frame+'.png');raw=Image.open(file).convert('RGBA')
   key=hashlib.sha256(raw.tobytes()).hexdigest();unique.setdefault(key,(name+' / %.3f s'%row['time_s'],file))
 inspection=BASE/'build/final-inspection'
 values=list(unique.values())
 for i in range(0,len(values),24):sheet(values[i:i+24],inspection/('clips-%02d.jpg'%(i//24)),columns=4,width=1600,height=320)
 meta=json.loads((beauty/'shots.json').read_text());items=[(name,beauty/(name+'.png')) for name in meta]
 items += [('Eevee hero',OUT/'eevee/hero.png')]
 items += [(folder+' / '+name,OUT/folder/(name+'.png')) for folder,names in [('cartridge',['cartridge','headstamp']),('case',['case','mouth','headstamp'])] for name in names]
 if (OUT/'wear-details/shots.json').exists():
  items += [(name,OUT/'wear-details'/(name+'.png')) for name in json.loads((OUT/'wear-details/shots.json').read_text())]
 sheet(items,OUT/'contact-sheet.jpg',columns=3,width=1800,height=355)
 turn=sheet([(name,beauty/(name+'.png')) for name in ('front','right','back','top')],OUT/'turnaround.jpg',height=440)
 details=sheet([(name,beauty/(name+'.png')) for name in ('receiver','wrist','forend','sights','butt_plate','muzzle')],OUT/'details.jpg',columns=2,height=480)
 action=sheet([('Lever open / raised carrier',beauty/'open.png'),('Exact Socket_Eye / 70 degrees',beauty/'aimed.png'),('Live cartridge',OUT/'cartridge/cartridge.png'),('Fired case / struck primer',OUT/'case/headstamp.png')],OUT/'action.jpg',height=450)
 sheet([(p.stem,p) for p in sorted((OUT/'pairs').glob('*-pair.jpg'))],OUT/'photo-pairs.jpg',columns=1,width=1800,height=450)
 measure(OUT/'photos');ranges=tonal(beauty)
 ammo_values()
 (OUT/'tonal-values.json').write_text(json.dumps(ranges,indent=2))
 report=dict(passed=True,image_records=len(records),images=records,playback=playback,unique_strip_images=len(unique),inspection_sheets=math.ceil(len(unique)/24))
 (BASE/'build/final-provenance.json').write_text(json.dumps(report,indent=2))
 if a.docs:
  docs=BASE/'docs';docs.mkdir(exist_ok=True)
  doc(panel(beauty/'hero.png',(1600,605)),docs/'hero.jpg');doc(turn,docs/'turnaround.jpg')
  doc(details,docs/'details.jpg');doc(action,docs/'action.jpg');doc(panel(OUT/'eevee/hero.png',(1600,605)),docs/'eevee.jpg')
 print('FINAL PROVENANCE',len(records),'GLB images;',len(playback),'real-duration clips;',len(unique),'unique strip images',flush=True)
if __name__=='__main__':main()
