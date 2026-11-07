"""Render each course in a fresh serial process, reusing its uploaded scene."""
from external import bundle
import argparse,hashlib,json,os,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
EXTRAS='tee cup border waterfall pond fixture clubhouse eevee'.split()

def gpu_command(command):
 return command if os.environ.get('ASSETS_GPU_HELD')=='1' else [str(HERE.parents[1]/'kit/with_gpu.sh'),*command]

def recipe_hash():
 return hashlib.sha256(b''.join((HERE/f).read_bytes() for f in ('render.py','context.py','fixtures.py','geometry.py','context_variant.py','render_batch.py'))).hexdigest()

def frames():
 return [kind+'-'+name for kind in ('classic','adventure') for name in ('above','hero','dusk','front','side','back','top')]+['classic-tee','classic-cup','classic-border']+EXTRAS

def main(args):
 chosen=args.shots.split(',') if args.shots else frames();recipe=recipe_hash()
 for seed in (71,92):
  needed=[];source=Path(f'export/Minigolf-{seed}.gltf');digest=bundle(source)
  for name in chosen:
   if (71 if name.startswith('classic-') else 92)!=seed:continue
   png=Path(args.out)/(name+'.png');receipt=png.with_suffix('.json')
   if png.exists() and receipt.exists():
    old=json.loads(receipt.read_text())
    if old.get('recipe_sha256')==recipe and old.get('sha256')==digest and old.get('width')==args.width and old.get('samples',0)>=args.samples and old.get('engine')==('BLENDER_EEVEE' if name=='eevee' else 'CYCLES'):
     print('CURRENT FRAME',png,flush=True);continue
   needed.append(name)
  for frame in needed:subprocess.run(gpu_command([args.blender,'-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(HERE/'render.py'),'--','--out',args.out,'--width',str(args.width),'--samples',str(args.samples),'--shots',frame]),check=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--blender',default='blender');p.add_argument('--out',default='renders/final');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);p.add_argument('--shots');main(p.parse_args())
