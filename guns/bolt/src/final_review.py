"""GLB provenance, final sheets, real-duration playback and small docs JPGs."""
from pathlib import Path
import sys,json,hashlib,argparse,math
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
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
 path.parent.mkdir(parents=True,exist_ok=True);im.save(path,quality=92,optimize=True);return im
def doc(im,path):
 im=im.copy();im.thumbnail((1600,10000),Image.Resampling.LANCZOS)
 for quality in (90,86,82,78,74,70,65,60):
  im.save(path,quality=quality,optimize=True)
  if path.stat().st_size<=200000:break
 assert path.stat().st_size<=200000

def main():
 from value_review import measure
 p=argparse.ArgumentParser();p.add_argument('--docs',action='store_true');a=p.parse_args()
 records=[]
 for meta in OUT.rglob('shots.json'):
  for name,row in json.loads(meta.read_text()).items():
   source=Path(row['source'])
   if source.suffix!='.glb':continue
   canonical=BASE/'export'/source.name
   assert row['sha256']==hashlib.sha256(canonical.read_bytes()).hexdigest(),(meta,name,'stale image')
   assert (meta.parent/(name+'.png')).exists()
   records.append(dict(folder=str(meta.parent.relative_to(OUT)),shot=name,sha256=row['sha256'],engine=row['engine']))
 timing=json.loads((OUT/'strips/timing.json').read_text());playback={}
 for name,row in timing.items():
  with Image.open(OUT/'strips'/(name+'.webp')) as im:
   total=0
   for i in range(im.n_frames):im.seek(i);im.load();total+=im.info.get('duration',0)
   assert total==row['duration_ms'];playback[name]=dict(frames=im.n_frames,decoded_duration_ms=total,expected_ms=row['duration_ms'])
 (BASE/'build/final-provenance.json').write_text(json.dumps(dict(passed=True,image_records=len(records),images=records,playback=playback),indent=2))
 measure(OUT/'photos')
 from final_shots import DEFAULT_SHOTS
 names=DEFAULT_SHOTS.split(',')+['crown','bipod_detail','rings','rear_cocked','bottom']
 items=[(n,BEAUTY/(n+'.png')) for n in names]
 items += [('Eevee hero',OUT/'eevee/hero.png'),('Loaded magazine',OUT/'loaded/magazine.png'),('Empty magazine',OUT/'empty/magazine.png'),('Fired case',OUT/'case/case.png'),('Fired mouth',OUT/'case/case_mouth.png')]
 items += [(n,OUT/'details'/(n+'.png')) for n in ('receiver_markings','forend_wear') if (OUT/'details'/(n+'.png')).exists()]
 items += [(n,OUT/'trigger'/(n+'.png')) for n in ('trigger_right','trigger_quarter','trigger_pulled')]
 sheet(items,OUT/'contact-sheet.jpg',columns=3,width=1800,height=370)
 turn=sheet([(n,BEAUTY/(n+'.png')) for n in ('front','side','back','top')],OUT/'turnaround.jpg',height=470)
 details=sheet([(n,BEAUTY/(n+'.png')) for n in ('optic','rear_cocked','grip','wrist')],OUT/'details.jpg',columns=2,height=600)
 action=sheet([('Bolt open / round retained in port',BEAUTY/'bolt_open.png'),('Socket_Eye / integrated 8x / 100 m',BEAUTY/'aimed.png'),('Deployed bipod',BEAUTY/'deployed.png'),('Loaded magazine',OUT/'loaded/magazine.png'),('Empty magazine',OUT/'empty/magazine.png'),('Fired case',OUT/'case/case.png')],OUT/'action.jpg',height=460)
 sheet([(n,OUT/'pairs'/(n+'-pair.jpg')) for n in ('right_photo','profile_right','left_photo','open_photo','wrist_photo','used_open','hero-wear')],OUT/'photo-pairs.jpg',columns=1,height=420)
 sheet([(n,OUT/'trigger-pairs'/(n+'-pair.jpg')) for n in ('trigger_photo_right','trigger_photo_quarter')],OUT/'trigger-pairs.jpg',columns=1,height=650)
 sheet([(n,OUT/'strips'/(n+'.jpg')) for n in timing],OUT/'clips.jpg',columns=1,height=550)
 samples=[]
 for name in timing:
  folder=OUT/'strips'/name
  for frame,row in json.loads((folder/'shots.json').read_text()).items():samples.append((f'{name} / {row["time_s"]:.3f} s',folder/(frame+'.png')))
 for index in range(0,len(samples),24):sheet(samples[index:index+24],BASE/'build/inspection'/f'clips-{index//24:02d}.jpg',columns=4,width=1600,height=310)
 if a.docs:
  docs=BASE/'docs';docs.mkdir(exist_ok=True)
  doc(panel(BEAUTY/'hero.png',(1600,640)),docs/'hero.jpg');doc(turn,docs/'turnaround.jpg')
  doc(details,docs/'details.jpg');doc(action,docs/'action.jpg');doc(panel(OUT/'eevee/hero.png',(1600,640)),docs/'eevee.jpg')
 print('B24 FINAL PROVENANCE',len(records),'images;',len(playback),'real-duration clips;',OUT/'contact-sheet.jpg')
if __name__=='__main__':main()
