"""Before/after at identical camera, light, resolution and exposure.

The baseline is rebuilt from the accepted git revision when its ignored
snapshot is absent. All work is contained in minigolf/build/baseline.
"""
import argparse,importlib.util,json,sys,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
from render import scene,views,render_one

def main(args):
 import context
 baseline=Path('build/baseline/export');assert (baseline/'Minigolf-92.gltf').exists(),'Run make baseline to reconstruct accepted revision'
 shots={
 'classic-above':dict(location=(-45,-55,61),target=(0,-2,0),lens=43,aspect=1.5),
 'adventure-above':dict(location=(-58,-66,71),target=(0,-2,0),lens=43,aspect=1.5),
 'hero':dict(location=(-1.7,15.4,3.13),target=(1,2,.9),lens=35,aspect=1.6),
 'clubhouse':dict(location=(0,-11.85,1.65),target=(0,-20.15,1.55),lens=42,aspect=1.6)}
 # Wide fixed views keep relocated forms visible in both versions.
 shots.update(terrain=dict(location=(-10,15,3.0),target=(1,4,1.0),lens=40,aspect=1.7),planting=dict(location=(2,-8,1.65),target=(5.2,-1,.7),lens=45,aspect=1.6),road=dict(location=(-67,-27,1.65),target=(-42,-55,3.5),lens=24,aspect=1.8))
 # A fixed wider view contains both the original and relocated waterfall.
 p=json.loads(Path('export/Minigolf-92.json').read_text())['plan'];shots['waterfall']=dict(location=(-2,4.5,3.2),target=(2.75,9.1,1.25),lens=32,aspect=1.6,sun=(-.65,-.65,.48))
 shots.pop('fixture',None);shots.pop('lighthouse',None);shots.pop('castle',None)
 wanted=set(args.keys.split(',')) if args.keys else None
 if wanted:shots={key:value for key,value in shots.items() if key in wanted}
 recipe={};args.out='renders/comparison';fingerprint=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();versions=('before','after') if args.version=='both' else (args.version,)
 for version in versions:
  for seed in (71,92):
   if not any((seed==71)==(key=='classic-above') for key in shots):continue
   if version=='after':source,p,ctx=scene(seed)
   else:
    bpy.ops.wm.read_factory_settings(use_empty=True);source=baseline/f'Minigolf-{seed}.gltf';p=json.loads(source.with_suffix('.json').read_text())['plan'];bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    spec=importlib.util.spec_from_file_location('_baseline_context',Path('build/baseline/src/context.py'));old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old);old.REPO=HERE.parents[1];ctx=old.make(p)
   ctx['comparison_recipe_sha256']=fingerprint
   for key,shot in shots.items():
    if (seed==71)!=(key=='classic-above'):continue
    render_one(version+'-'+key,dict(shot),source,p,ctx,args);recipe[key]=shot
 for kind,key in (('windmill','fixture'),('lighthouse','lighthouse'),('castle','castle')):
  if wanted and key not in wanted:continue
  for version in versions:
   source,p,ctx=scene(92);shot=views(p)[key];root=next(o for o in bpy.context.scene.objects if o.get('fixture_kind')==kind);xf=root.matrix_world.copy()
   if version=='before':
    for ob in [*root.children_recursive,root]:bpy.data.objects.remove(ob,do_unlink=True)
    prior=set(bpy.context.scene.objects);old_source=baseline/'Minigolf-92.gltf';bpy.ops.import_scene.gltf(filepath=str(old_source.resolve()));added=set(bpy.context.scene.objects)-prior
    old_root=next(o for o in added if o.get('fixture_kind')==kind);keep={old_root,*old_root.children_recursive}
    old_root.parent=None;old_root.matrix_world=xf
    for ob in added-keep:bpy.data.objects.remove(ob,do_unlink=True)
    ctx['comparison_scope']='Accepted fixture geometry staged at revised course placement; surrounding revised course identical in both views.'
    ctx['baseline_source']=str(old_source)
   ctx['comparison_recipe_sha256']=fingerprint
   render_one(version+'-'+key,dict(shot),source,p,ctx,args);recipe[key]=shot
 receipt=Path(args.out,'cameras.json');prior=json.loads(receipt.read_text()) if receipt.exists() else {};prior.update(recipe);receipt.write_text(json.dumps(prior,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);p.add_argument('--keys');p.add_argument('--version',choices=('before','after','both'),default='both');args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);main(args)
