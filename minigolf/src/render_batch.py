"""Render each checkpoint frame in a fresh, serial Blender process.

Each fresh Blender process owns the shared GPU lock. A completed frame is
reused only when its GLB, recipe, width and sample receipts are current.
"""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
EXTRAS='tee cup border waterfall fixture bridge clubhouse lighthouse castle bank planting road sign'.split()

def gpu_command(command):
 # Standalone and externally locked preview invocations both work. Normal
 # batches release between frames so another worker can use the shared GPU.
 return command if os.environ.get('ASSETS_GPU_HELD')=='1' else [str(HERE.parents[1]/'kit/with_gpu.sh'),*command]

def recipe_hash():
 return hashlib.sha256(b''.join((HERE/f).read_bytes() for f in ('render.py','context.py','fixtures.py','geometry.py','context_variant.py','render_batch.py'))).hexdigest()

def frames():
 return [kind+'-'+name for kind in ('classic','adventure') for name in ('ground','above','hero','dusk')]+EXTRAS

def main(args):
 chosen=args.shots.split(',') if args.shots else frames();recipe=recipe_hash()
 for name in chosen:
  seed=71 if name.startswith('classic-') else 92;source=Path(f'export/Minigolf-{seed}.glb');digest=hashlib.sha256(source.read_bytes()).hexdigest();png=Path(args.out)/(name+'.png');receipt=png.with_suffix('.json')
  if png.exists() and receipt.exists():
   old=json.loads(receipt.read_text())
   if old.get('recipe_sha256')==recipe and old.get('sha256')==digest and old.get('width')==args.width and old.get('samples',0)>=args.samples and old.get('engine')=='CYCLES':
    print('CURRENT FRAME',png,flush=True);continue
  subprocess.run(gpu_command([args.blender,'-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(HERE/'render.py'),'--','--out',args.out,'--width',str(args.width),'--samples',str(args.samples),'--shots',name]),check=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--blender',default='blender');p.add_argument('--out',default='renders/lookdev');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);p.add_argument('--shots');main(p.parse_args())
