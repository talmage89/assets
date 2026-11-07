"""Serial, resumable same-camera comparisons, one Blender scene per frame."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from render_batch import recipe_hash,HERE,gpu_command
KEYS='classic-above adventure-above hero clubhouse terrain planting road waterfall fixture lighthouse castle'.split()
def main(args):
 fingerprint=hashlib.sha256((HERE/'comparison.py').read_bytes()).hexdigest();recipe=recipe_hash()
 for key in KEYS:
  for version in ('before','after'):
   seed=71 if key=='classic-above' else 92;staged=key in ('fixture','lighthouse','castle')
   source=Path('export')/f'Minigolf-{seed}.glb' if version=='after' or staged else Path('build/baseline/export')/f'Minigolf-{seed}.gltf'
   digest=hashlib.sha256(source.read_bytes()).hexdigest();png=Path('renders/comparison')/f'{version}-{key}.png';receipt=png.with_suffix('.json')
   if png.exists() and receipt.exists():
    old=json.loads(receipt.read_text())
    if old.get('recipe_sha256')==recipe and old.get('sha256')==digest and old.get('width')==args.width and old.get('samples',0)>=args.samples and old.get('context',{}).get('comparison_recipe_sha256')==fingerprint:
     print('CURRENT COMPARISON',png,flush=True);continue
   subprocess.run(gpu_command([args.blender,'-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(HERE/'comparison.py'),'--','--width',str(args.width),'--samples',str(args.samples),'--keys',key,'--version',version]),check=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--blender',default='blender');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);main(p.parse_args())
