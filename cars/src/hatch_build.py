"""Build only the H120 form checkpoint from a factory-empty scene."""
import argparse,json,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from build import Build
import hatch_body,hatch_spec as S,wheels

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--quality',choices=['game','high'],default='game')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 bpy.ops.wm.read_factory_settings(use_empty=True)
 b=Build(a.quality=='high',detail=False);b.root.name=S.NAME;b.asset_set=S.ASSET_SET;b.root['asset_set']=S.ASSET_SET
 hatch_body.build(b);wheels.build(b,S)
 for m in list(bpy.data.materials):
  if m.users==0:bpy.data.materials.remove(m)
 sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
 sc['asset']=S.NAME;sc['quality']=a.quality;sc['stage']='source form checkpoint';sc['seed']=120
 bpy.context.view_layer.update();Path(a.out).parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
 counts={}
 for ob in sc.objects:
  if ob.type=='MESH':
   ob.data.calc_loop_triangles();cat=ob['part_category'];counts[cat]=counts.get(cat,0)+len(ob.data.loop_triangles)
 print('CHECKPOINT_TRIANGLES',json.dumps(counts),sum(counts.values()),flush=True)
if __name__=='__main__':main()
