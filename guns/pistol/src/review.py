"""Final exported-GLB sheets, current-source provenance and bounded docs JPGs."""
from pathlib import Path
import argparse,json,hashlib,math,sys
from PIL import Image,ImageDraw,ImageFont,ImageOps
from value_review import measure
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
OUT=BASE/'renders/final'
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),23)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),17)


def panel(path,size):
 im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(67,70,73,255));bg.alpha_composite(im)
 return ImageOps.contain(bg.convert('RGB'),size,Image.Resampling.LANCZOS)


def sheet(path,items,columns=3,cell=(700,545)):
 w,h=cell;canvas=Image.new('RGB',(w*columns,h*math.ceil(len(items)/columns)),(233,235,232));draw=ImageDraw.Draw(canvas)
 for i,(label,image) in enumerate(items):
  x=i%columns*w;y=i//columns*h;draw.text((x+13,y+11),label,font=FONT,fill=(23,32,29))
  im=panel(image,(w-6,h-48));canvas.paste(im,(x+(w-im.width)//2,y+44+(h-48-im.height)//2))
 canvas.save(path,quality=93,optimize=True)
 return canvas


def provenance():
 rows=[]
 for folder in ('beauty','eevee','photos','loaded','empty','case'):
  metadata=json.loads((OUT/folder/'shots.json').read_text())
  for name,s in metadata.items():
   source=Path(s['source']);assert source.suffix=='.glb' and source.parent==BASE/'export'
   assert s['sha256']==hashlib.sha256(source.read_bytes()).hexdigest(),(folder,name,'stale source')
   assert s['stage']=='final exported GLB with baked 2048 PBR maps'
   im=Image.open(OUT/folder/(name+'.png'));assert im.width>=1000
   rows.append(dict(group=folder,shot=name,source=source.name,sha256=s['sha256'],engine=s['engine']))
 for folder in sorted((OUT/'strips').iterdir()):
  if not folder.is_dir():continue
  for name,s in json.loads((folder/'shots.json').read_text()).items():
   source=Path(s['source']);assert source==BASE/'export/pistol.glb'
   assert s['sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
   assert s['engine']=='BLENDER_EEVEE'
   rows.append(dict(group='strips',shot=name,source=source.name,sha256=s['sha256'],engine=s['engine']))
 timing=json.loads((OUT/'strips/timing.json').read_text())
 for clip,s in timing.items():
  assert sum(s['playback_frame_durations_ms'])==s['duration_ms']
  with Image.open(OUT/'strips'/(clip+'.webp')) as im:
   duration=0
   for i in range(im.n_frames):
    im.seek(i);im.load();duration+=im.info.get('duration',0)
   assert duration==s['duration_ms'],(clip,duration,s['duration_ms'])
 result=dict(passed=True,render_count=len(rows),shots=rows,clip_timing=timing)
 (BASE/'build/final-provenance.json').write_text(json.dumps(result,indent=2))
 return result


def save_doc(image,name):
 folder=BASE/'docs';folder.mkdir(exist_ok=True)
 im=image.copy();im.thumbnail((1600,2000),Image.Resampling.LANCZOS)
 for quality in (92,88,84,80,76,72,68):
  im.save(folder/name,quality=quality,optimize=True)
  if (folder/name).stat().st_size<=200000:break
 assert im.width<=1600 and (folder/name).stat().st_size<=200000
 print('DOC',name,im.size,(folder/name).stat().st_size)


def main():
 p=argparse.ArgumentParser();p.add_argument('--docs',action='store_true');a=p.parse_args()
 proof=provenance();measure(OUT/'photos',OUT/'beauty')
 beauty=[('Cycles / '+name,OUT/'beauty'/(name+'.png')) for name in
  ('hero','hero_left','front','side','back','top','rear_sights','grip_texture','port_hood','markings','aimed','locked','scale','hand_frame')]
 extra=[('Loaded magazine',OUT/'loaded/mag_standalone.png'),('Loaded / spine',OUT/'loaded/mag_rear.png'),
        ('Empty magazine',OUT/'empty/mag_standalone.png'),('Empty / spine',OUT/'empty/mag_rear.png'),
        ('Fired case',OUT/'case/case.png'),('Case / carbon at mouth',OUT/'case/case_mouth.png'),
        ('Eevee / same exported PBR',OUT/'eevee/hero.png')]
 sheet(OUT/'contact-sheet.jpg',beauty+extra)
 turns=sheet(OUT/'turnaround.jpg',[(n.title(),OUT/'beauty'/(n+'.png')) for n in ('front','side','back','top')],2,(800,640))
 details=sheet(OUT/'details.jpg',[(n.replace('_',' ').title(),OUT/'beauty'/(n+'.png')) for n in ('rear_sights','grip_texture','port_hood','markings')],2,(800,650))
 actions=sheet(OUT/'action-magazines.jpg',[('Locked open',OUT/'beauty/locked.png'),extra[0],extra[2],extra[4]],2,(800,650))
 clips=[]
 for folder in sorted((OUT/'strips').iterdir()):
  if not folder.is_dir():continue
  paths=sorted(folder.glob('*.png'));pick=sorted(set(round(i*(len(paths)-1)/4) for i in range(5)))
  clips.append((folder.name,[paths[i] for i in pick]))
 canvas=Image.new('RGB',(1800,len(clips)*340),(233,235,232));draw=ImageDraw.Draw(canvas)
 for row,(name,paths) in enumerate(clips):
  y=row*340;draw.text((12,y+7),name+' / real-time Eevee strip; uniform 15 Hz samples',font=SMALL,fill=(23,32,29))
  for col,f in enumerate(paths):
   im=panel(f,(355,295));canvas.paste(im,(col*360,y+35))
 canvas.save(OUT/'clips.jpg',quality=90,optimize=True)
 if a.docs:
  save_doc(Image.open(OUT/'beauty/hero.png').convert('RGB'),'hero.jpg')
  save_doc(turns,'turnaround.jpg');save_doc(details,'details.jpg');save_doc(actions,'action.jpg')
  save_doc(Image.open(OUT/'eevee/hero.png').convert('RGB'),'eevee.jpg')
 print('FINAL REVIEW',proof['render_count'],'current GLB renders;',OUT/'contact-sheet.jpg',flush=True)

if __name__=='__main__':main()
