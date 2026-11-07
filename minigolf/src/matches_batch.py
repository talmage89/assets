from external import bundle
"""Fresh serial Blender processes for the three complete-course photo pairs."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
from render_batch import recipe_hash,HERE,gpu_run
sys.path.insert(0,str(HERE.parents[1]))
from kit.photo_match import compose
from photo_matches import SELECTION,LIGHTING
def main(args):
 out='renders/source-matches' if args.source_fields else 'renders/look-matches';fits=json.loads(Path('build/photo-calibration.json').read_text());recipe=recipe_hash();fingerprint=hashlib.sha256((HERE/'matches.py').read_bytes()).hexdigest()
 fields={ch:Path('build/procedural' if ch!='Normal' else 'textures/bake')/f'T_Minigolf_{ch}.png' for ch in ('BaseColor','ORM','Normal')};field_hashes={ch:hashlib.sha256(path.read_bytes()).hexdigest() for ch,path in fields.items()}
 for key,fit in fits.items():
  seed,_=SELECTION[key];source=Path(f'export/Minigolf-{seed}.gltf');digest=bundle(source);png=Path(out)/(key+'.png');receipt=png.with_suffix('.json');shot=dict(fit['shot'],**LIGHTING[key]);shot['aspect']=(fit['crop'][2]-fit['crop'][0])/(fit['crop'][3]-fit['crop'][1]);shot=json.loads(json.dumps(shot))
  if png.exists() and receipt.exists():
   old=json.loads(receipt.read_text());ctx=old.get('context',{})
   if old.get('recipe_sha256')==recipe and old.get('sha256')==digest and old.get('width')==args.width and old.get('samples',0)>=args.samples and old.get('requested_camera')==shot and ctx.get('match_recipe_sha256')==fingerprint and (not args.source_fields or ctx.get('source_fields')==field_hashes):
    print('CURRENT PHOTO FRAME',png,flush=True);continue
  command=[args.blender,'-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(HERE/'matches.py'),'--','render','--key',key,'--no-compose','--width',str(args.width),'--samples',str(args.samples)]
  if args.source_fields:command.append('--source-fields')
  gpu_run(command)
 compose('build/photo-calibration.json',out,out)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--blender',default='blender');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);p.add_argument('--source-fields',action='store_true');main(p.parse_args())
