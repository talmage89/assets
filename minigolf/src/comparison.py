"""Before/after at identical camera, light, resolution and exposure.

The baseline is rebuilt from the accepted git revision when its ignored
snapshot is absent. All work is contained in minigolf/build/baseline.
"""
import argparse,importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
from render import scene,views,render_one

def main(args):
 import context
 baseline=Path('build/baseline/export');assert (baseline/'Minigolf-92.gltf').exists(),'Run make baseline to reconstruct accepted revision'
 shots={key:json.loads(Path('renders/before',key+'.json').read_text())['camera'] for key in ('adventure-above','classic-above','hero','fixture','waterfall','clubhouse') if Path('renders/before',key+'.json').exists()}
 # Wide fixed views keep relocated forms visible in both versions.
 shots.update(terrain=dict(location=(-10,15,3.0),target=(1,4,1.0),lens=40,aspect=1.7),lighthouse=dict(location=(-14,-18,1.65),target=(-8,-5,2.2),lens=40,aspect=1.5),castle=dict(location=(-12,-22,1.65),target=(-4,-3,2.2),lens=36,aspect=1.6),planting=dict(location=(2,-8,1.65),target=(5.2,-1,.7),lens=45,aspect=1.6),road=dict(location=(-22,-16,1.65),target=(0,-48,2.4),lens=40,aspect=1.8))
 # Use the current waterfall framing on both versions: it stays outside the
 # rebuilt bridge rather than looking through its supporting wall.
 _,p,_=scene(92);shots['waterfall']=views(p)['waterfall']
 shots.pop('fixture',None);shots.pop('lighthouse',None);shots.pop('castle',None)
 recipe={};args.out='renders/comparison'
 for version in ('before','after'):
  for seed in (71,92):
   if version=='after':source,p,ctx=scene(seed)
   else:
    bpy.ops.wm.read_factory_settings(use_empty=True);source=baseline/f'Minigolf-{seed}.gltf';p=json.loads(source.with_suffix('.json').read_text())['plan'];bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    spec=importlib.util.spec_from_file_location('_baseline_context',Path('build/baseline/src/context.py'));old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old);ctx=old.make(p)
   for key,shot in shots.items():
    if (seed==71)!=(key=='classic-above'):continue
    render_one(version+'-'+key,dict(shot),source,p,ctx,args);recipe[key]=shot
 for kind,key in (('windmill','fixture'),('lighthouse','lighthouse'),('castle','castle')):
  for version in ('before','after'):
   source,p,ctx=scene(92);shot=views(p)[key];root=next(o for o in bpy.context.scene.objects if o.get('fixture_kind')==kind);xf=root.matrix_world.copy()
   if version=='before':
    for ob in [*root.children_recursive,root]:bpy.data.objects.remove(ob,do_unlink=True)
    prior=set(bpy.context.scene.objects);old_source=baseline/'Minigolf-92.gltf';bpy.ops.import_scene.gltf(filepath=str(old_source.resolve()));added=set(bpy.context.scene.objects)-prior
    old_root=next(o for o in added if o.get('fixture_kind')==kind);keep={old_root,*old_root.children_recursive}
    old_root.parent=None;old_root.matrix_world=xf
    for ob in added-keep:bpy.data.objects.remove(ob,do_unlink=True)
    ctx['comparison_scope']='Accepted fixture geometry staged at revised course placement; surrounding revised course identical in both views.'
    ctx['baseline_source']=str(old_source)
   render_one(version+'-'+key,dict(shot),source,p,ctx,args);recipe[key]=shot
 Path(args.out,'cameras.json').write_text(json.dumps(recipe,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);main(args)
