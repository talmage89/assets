"""Freeze and render an actual shipped-format GLB for a numbered critique pass."""
from pathlib import Path
import argparse,subprocess,shutil,json,os,hashlib,math
from PIL import Image,ImageDraw,ImageOps
from value_review import measure
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]

def main():
 p=argparse.ArgumentParser();p.add_argument('--pass',dest='pass_name',required=True)
 p.add_argument('--width',type=int,default=1280);p.add_argument('--samples',type=int,default=32)
 p.add_argument('--resume',action='store_true',help='Compose an already rendered frozen pass without replacing it')
 a=p.parse_args();snapshot=BASE/'build/review'/a.pass_name;out=BASE/'renders/lookdev'/a.pass_name
 snapshot.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
 if not a.resume:
  for f in (BASE/'export').glob('*.glb'):shutil.copy2(f,snapshot/f.name)
  (snapshot/'sources').mkdir(exist_ok=True)
  for f in (BASE/'src').glob('*.py'):shutil.copy2(f,snapshot/'sources'/f.name)
 def call(args):subprocess.run(args,check=True,cwd=BASE)
 cmd=[str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1',
  '--python','src/render.py','--','--source',str(snapshot/'pistol.glb'),'--out',str(out),
  '--width',str(a.width),'--samples',str(a.samples),'--shots',
  'hero,hero_left,grip_texture,port_hood,rear_sights,aimed,right_photo,open_photo,left_photo',
  '--camera-file','build/cameras.json']
 if not a.resume:call(cmd)
 else:
  for shot,s in json.loads((out/'shots.json').read_text()).items():
   assert s['sha256']==hashlib.sha256((snapshot/'pistol.glb').read_bytes()).hexdigest()
 for variant,shots in [('magazine_loaded','mag_standalone,mag_rear'),
                       ('magazine_empty','mag_standalone,mag_rear'),('case','case')]:
  target=out/variant
  if not a.resume or not (target/'shots.json').exists():
   extra=cmd.copy();extra[extra.index('--source')+1]=str(snapshot/(variant+'.glb'))
   extra[extra.index('--out')+1]=str(target);extra[extra.index('--shots')+1]=shots
   call(extra)
 call(['python3',str(ROOT/'kit/photo_match.py'),'compose','--calibration','build/cameras.json','--renders',str(out),'--out',str(out/'pairs')])
 values=measure(out)
 images=['hero','hero_left','grip_texture','port_hood','rear_sights','aimed']
 extra_images=[('Loaded magazine',out/'magazine_loaded/mag_standalone.png'),
               ('Loaded spine',out/'magazine_loaded/mag_rear.png'),
               ('Empty magazine',out/'magazine_empty/mag_standalone.png'),
               ('Empty spine',out/'magazine_empty/mag_rear.png'),('Fired case',out/'case/case.png')]
 items=[(name,out/(name+'.png')) for name in images]+extra_images
 sheet=Image.new('RGB',(1800,math.ceil(len(items)/3)*475),(237,238,234));draw=ImageDraw.Draw(sheet)
 for i,(name,path) in enumerate(items):
  im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(65,68,72,255));bg.alpha_composite(im)
  im=ImageOps.contain(bg.convert('RGB'),(600,435));x=i%3*600;y=i//3*475
  sheet.paste(im,(x+(600-im.width)//2,y+35));draw.text((x+12,y+10),a.pass_name+' / '+name,fill=(20,30,25))
 sheet.save(out/'contact-sheet.jpg',quality=93,optimize=True)
 print('FROZEN GLB CRITIQUE',a.pass_name,hashlib.sha256((snapshot/'pistol.glb').read_bytes()).hexdigest(),flush=True)
 for view,rows in values['patches'].items():
  print(view,{name:(r['photo']['median_luma_255'],r['render']['median_luma_255'],r['render']['rgb_ratios_g1']) for name,r in rows.items()})

if __name__=='__main__':main()
