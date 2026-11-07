"""Same-camera gate comparisons against fe8acfc, reproducible from git sources.

The isolated baseline writes only inside this worktree's build directory.
Sibling families are read-only symlink inputs; original sources are not changed.
"""
import argparse,io,json,subprocess,sys,tarfile,shutil
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from render_batch import gpu_run
ROOT=HERE.parents[1];ASSET=HERE.parent;BASE=ROOT/'build/minigolf-gate-baseline';REV='fe8acfc'
SHOTS=['classic-hero','adventure-above','waterfall','pond','tee','classic-green']

def prepare(blender):
 source=BASE/'minigolf';source.mkdir(parents=True,exist_ok=True)
 if not (source/'src/build.py').exists():
  data=subprocess.check_output(['git','archive',REV,'minigolf/Makefile','minigolf/src'],cwd=ROOT)
  with tarfile.open(fileobj=io.BytesIO(data)) as archive:archive.extractall(BASE,filter='data')
 for family in ROOT.iterdir():
  if not family.is_dir() or family.name in ('minigolf','build','.git'):continue
  dest=BASE/family.name
  if not dest.exists():dest.symlink_to(family,target_is_directory=True)
 # Archived scripts use the current unchanged kit and native family maps.
 if not (source/'export/Minigolf-92.gltf').exists():
  subprocess.run(['make','model','BLENDER='+blender],cwd=source,check=True)
 context=source/'build/context'
 if not context.exists() and not context.is_symlink():context.symlink_to(ASSET/'build/context',target_is_directory=True)
 # Native landscape placement is unchanged; import it from its real URI root.
 return source

def render(args):
 import bpy
 from render import scene,render_one,views
 chosen=args.shots.split(',') if args.shots else SHOTS
 for seed in (71,92):
  names=[n for n in chosen if (71 if n.startswith('classic-') else 92)==seed]
  if not names:continue
  source,p,ctx=scene(seed,source=args.source.format(seed=seed) if args.source else None)
  for name in names:
   key=name.removeprefix('classic-').removeprefix('adventure-')
   from gate_cameras import CAMERAS
   shot=CAMERAS.get(name,views(p).get(key)) if key!='walks' else dict(location=(0,-2,90),target=(0,-2,0),ortho=70,lens=45,aspect=1.05,sun=(-.65,-.65,1.4))
   if key=='green':
    from photo_matches import LIGHTING
    fit=json.loads((ASSET/'build/photo-calibration.json').read_text())['period_classic_green']
    shot=dict(fit['shot'],**LIGHTING['period_classic_green']);shot['aspect']=(fit['crop'][2]-fit['crop'][0])/(fit['crop'][3]-fit['crop'][1])
   render_one(args.prefix+name,shot,source,p,ctx,args)

def pairs():
 out=ASSET/'renders/finish-fixes';out.mkdir(parents=True,exist_ok=True);rows=[]
 for name in SHOTS:
  a,b=[out/(prefix+name+'.png') for prefix in ('before-','after-')]
  if not a.exists() or not b.exists():continue
  ma,mb=[json.loads(f.with_suffix('.json').read_text()) for f in (a,b)]
  assert ma['camera']==mb['camera'],('Comparison camera changed',name,ma['camera'],mb['camera'])
  x,y=Image.open(a).convert('RGB'),Image.open(b).convert('RGB');assert x.size==y.size and x.width>=800
  z=Image.new('RGB',(x.width*2,x.height+36),(232,231,220));z.paste(x,(0,36));z.paste(y,(x.width,36));d=ImageDraw.Draw(z);d.text((12,10),REV+' / BEFORE',fill='black');d.text((x.width+12,10),'FINISH / EXPORTED glTF',fill='black');z.save(out/(name+'-pair.jpg'),quality=94)
  rows.append(dict(name=name,panel_width=x.width,before=str(a.relative_to(ASSET)),after=str(b.relative_to(ASSET)),camera_scope='Identical camera, lens, lighting and course placements'))
 (ASSET/'build/finish-crops.json').write_text(json.dumps(rows,indent=2))

def main(args):
 base=None if args.after_only else prepare(args.blender)
 # Use the current renderer for both so camera/light/context are identical.
 batches=[('after-',None)] if args.after_only else [('before-',str(base/'export/Minigolf-{seed}.gltf')),('after-',None)]
 for prefix,source in batches:
  chosen=args.shots.split(',') if args.shots else SHOTS
  for name in chosen:
   command=[args.blender,'-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(HERE/'finish_views.py'),'--','--worker','--out','renders/finish-fixes','--prefix',prefix,'--width',str(args.width),'--samples',str(args.samples),'--shots',name]
   if source:command+=['--source',source]
   gpu_run(command,cwd=ASSET)

 if not args.after_only:pairs()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--worker',action='store_true');p.add_argument('--after-only',action='store_true');p.add_argument('--prepare-only',action='store_true');p.add_argument('--source');p.add_argument('--prefix',default='after-');p.add_argument('--shots');p.add_argument('--blender',default='blender');p.add_argument('--out',default='renders/finish-fixes');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
 if a.prepare_only:prepare(a.blender)
 else:render(a) if a.worker else main(a)
