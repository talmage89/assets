"""Native-size aaf099e versus current exports, plus labeled framing change.

Local frozen handoff resources are evidence only. Missing baselines rebuild
from tracked source into build/, against the same read-only native inputs.
"""
import hashlib,io,json,os,subprocess,sys,tarfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ASSET=HERE.parent;ROOT=ASSET.parent
sys.path[:0]=[str(ROOT),str(HERE)]
from kit.fonts import find_font
BEFORE=Path('build/round4-before/freeway');OUT=Path('renders/round4-crops')
VIEWS={'grass-101':(101,'hero_previous','hero',(0,.28,1,1)),
       'grass-202':(202,'hero','hero',(0,.36,1,1)),
       'columns':(101,'pier_girders','pier_girders',(0,0,1,1)),
       'barrier':(101,'barrier','barrier',(0,0,1,1)),
       'lanes-101':(101,'hero_previous','hero',(0,.48,1,.74)),
       'lanes-202':(202,'hero','hero',(0,.46,1,1))}

def prepare():
 if (BEFORE/'export/Freeway-101.gltf').exists():return
 BEFORE.parent.mkdir(parents=True,exist_ok=True)
 raw=subprocess.check_output(['git','archive','aaf099e','freeway'],cwd=ROOT)
 with tarfile.open(fileobj=io.BytesIO(raw)) as ar:ar.extractall(BEFORE.parent,filter='data')
 for family in ROOT.iterdir():
  if not family.is_dir() or family.name in ('freeway','build','.git'):continue
  link=BEFORE.parent/family.name
  if not link.exists():link.symlink_to(family,target_is_directory=True)
 (BEFORE/'refs').mkdir(exist_ok=True)
 for photo in Path('refs').iterdir():
  if photo.suffix.lower() not in ('.jpg','.png','.pdf'):continue
  link=BEFORE/'refs'/photo.name
  if not link.exists():link.symlink_to(photo.resolve())
 with (BEFORE.parent/'rebuild.log').open('w') as log:
  subprocess.run(['make','model'],cwd=BEFORE,stdout=log,stderr=subprocess.STDOUT,check=True)

def jobs():
 prepare();out=[]
 for seed,new,old,roi in VIEWS.values():
  target=BEFORE/'renders/final'/str(seed)/(old+'.png')
  if not target.exists():
   camera=json.loads(Path(f'renders/final/{seed}/{new}.json').read_text())['camera']
   if not any(row['out']==str(target) for row in out):out.append(dict(source=str(BEFORE/f'export/Freeway-{seed}.gltf'),out=str(target),camera=camera))
 return out

def panel(label,before,after,roi,same=True):
 a,b=[Image.open(p).convert('RGB') for p in (before,after)]
 records=[json.loads(p.with_suffix('.json').read_text()) for p in (before,after)]
 if same:assert all(records[0]['camera'].get(k)==records[1]['camera'].get(k) for k in ('location','target','lens','aspect')),(label,'Camera differs')
 boxes=[tuple(round(v*(im.width if k%2==0 else im.height)) for k,v in enumerate(roi)) for im in (a,b)]
 a,b=[im.crop(box) for im,box in zip((a,b),boxes)];assert min(a.width,b.width)>=800
 w=max(a.width,b.width);im=Image.new('RGB',(w*2,max(a.height,b.height)+50),(24,29,26));d=ImageDraw.Draw(im)
 font=ImageFont.truetype(find_font('DejaVu Sans','Book'),24)
 im.paste(a,(0,50));im.paste(b,(w,50));d.text((16,10),label+' / aaf099e',font=font,fill=(232,236,226));d.text((w+16,10),'CURRENT EXPORT / '+('same camera' if same else 'new composition'),font=font,fill=(232,236,226))
 im.save(OUT/(label+'.jpg'),quality=96)
 return dict(before=str(before),after=str(after),native_widths=[a.width,b.width],crop_boxes=boxes,identical_camera=same,cameras=[r['camera'] for r in records],before_sha256=hashlib.sha256(before.read_bytes()).hexdigest(),after_sha256=hashlib.sha256(after.read_bytes()).hexdigest())

def main():
 OUT.mkdir(parents=True,exist_ok=True);pending=jobs()
 if pending:
  path=Path('build/round4-before/jobs.json');path.write_text(json.dumps(pending,indent=2))
  with Path('build/round4-before/render.log').open('w') as log:
   subprocess.run([str(ROOT/'kit/with_gpu.sh'),'blender','-t','2','-b','--factory-startup','--python-exit-code','1','--python',str(HERE/'round4_evidence.py'),'--','--render',str(path)],stdout=log,stderr=subprocess.STDOUT,check=True)
 rows={}
 for label,(seed,new,old,roi) in VIEWS.items():
  rows[label]=panel(label,BEFORE/f'renders/final/{seed}/{old}.png',Path(f'renders/final/{seed}/{new}.png'),roi)
 rows['framing-101']=panel('framing-101',BEFORE/'renders/final/101/hero.png',Path('renders/final/101/hero.png'),(0,0,1,1),False)
 (OUT/'evidence.json').write_text(json.dumps(rows,indent=2));print('ROUND 4 EVIDENCE',len(rows),'native comparisons')

if __name__=='__main__':
 if '--render' in sys.argv:
  from render import render
  for row in json.loads(Path(sys.argv[-1]).read_text()):
   path=Path(row['out']);render(row['source'],path.parent,1400,32,'CYCLES',custom={path.stem:row['camera']})
 else:main()
