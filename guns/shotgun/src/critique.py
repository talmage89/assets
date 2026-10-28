"""Freeze an actual delivery-format GLB and its source before each critique."""
from pathlib import Path
import argparse,subprocess,shutil,json,hashlib,sys,math
from PIL import Image,ImageDraw,ImageOps
from value_review import measure
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]

def main():
 p=argparse.ArgumentParser();p.add_argument('--pass',dest='name',required=True)
 p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=32)
 p.add_argument('--resume',action='store_true');a=p.parse_args()
 snapshot=BASE/'build/review'/a.name;out=BASE/'renders/lookdev'/a.name
 snapshot.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
 if not a.resume:
  for f in (BASE/'export').glob('*.glb'):shutil.copy2(f,snapshot/f.name)
  shutil.copytree(BASE/'src',snapshot/'sources',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
  if (BASE/'build/delivery/high-sources').exists():shutil.copytree(BASE/'build/delivery/high-sources',snapshot/'baked-sources',dirs_exist_ok=True)
  shutil.copy2(BASE/'build/baked/4k/bake-report.json',snapshot/'bake-report.json')
 def call(cmd):subprocess.run(cmd,check=True,cwd=BASE)
 cmd=[str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python','src/render.py','--',
  '--source',str(snapshot/'shotgun.glb'),'--out',str(out),'--width',str(a.width),'--samples',str(a.samples),
  '--shots','hero,hero_left,receiver,wrist,forend,aimed,aimed_socket,open,pad,used_photo,wood_photo,right_photo,left_photo,open_photo','--camera-file','build/cameras.json']
 if not a.resume:call(cmd)
 for name,shots in [('shell','shell,shell_crimp'),('hull','hull,hull_primer')]:
  target=out/name
  if not a.resume or not (target/'shots.json').exists():
   extra=cmd.copy();extra[extra.index('--source')+1]=str(snapshot/(name+'.glb'))
   extra[extra.index('--out')+1]=str(target);extra[extra.index('--shots')+1]=shots;call(extra)
 for folder in [out,out/'shell',out/'hull']:
  for s in json.loads((folder/'shots.json').read_text()).values():
   assert s['sha256']==hashlib.sha256(Path(s['source']).read_bytes()).hexdigest()
 call(['python3',str(ROOT/'kit/photo_match.py'),'compose','--calibration','build/cameras.json','--renders',str(out),'--out',str(out/'pairs')])
 values=measure(out)
 names=['hero','hero_left','receiver','wrist','forend','aimed','aimed_socket','open','pad']
 images=[(n,out/(n+'.png')) for n in names]+[(n,out/n/(n+'.png')) for n in ('shell','hull')]
 canvas=Image.new('RGB',(1800,math.ceil(len(images)/3)*380),(225,226,222));draw=ImageDraw.Draw(canvas)
 for i,(label,path) in enumerate(images):
  im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(59,62,66,255));bg.alpha_composite(im)
  im=ImageOps.contain(bg.convert('RGB'),(600,345));x=i%3*600;y=i//3*380
  canvas.paste(im,(x+(600-im.width)//2,y+30));draw.text((x+12,y+8),a.name+' / '+label,fill=(20,30,25))
 canvas.save(out/'contact-sheet.jpg',quality=92,optimize=True)
 print('FROZEN DELIVERY CRITIQUE',a.name,hashlib.sha256((snapshot/'shotgun.glb').read_bytes()).hexdigest(),flush=True)
 for name,row in values['patches'].items():print(name,row)
if __name__=='__main__':main()
