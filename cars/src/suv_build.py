"""Independent SUV entry point; pickup and sedan generators are untouched."""
import argparse,json,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from build import Build
import suv_spec as S
import suv_body,wheels

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--quality',choices=['game','high'],default='game')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.read_factory_settings(use_empty=True)
 b=Build(a.quality=='high',detail=False);b.root.name=S.NAME;b.asset_set=S.ASSET_SET;b.root['asset_set']=S.ASSET_SET
 suv_body.build(b);wheels.build(b,S)
 for m in list(bpy.data.materials):
  if not m.users:bpy.data.materials.remove(m)
 sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc['asset']=S.NAME;sc['quality']=a.quality;sc['stage']='SUV source form checkpoint'
 bpy.context.view_layer.update();out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(out))
 counts={}
 for ob in sc.objects:
  if ob.type=='MESH':
   ob.data.calc_loop_triangles();k=ob['part_category'];counts[k]=counts.get(k,0)+len(ob.data.loop_triangles)
 print('SUV_TRIANGLES',json.dumps(counts),sum(counts.values()),flush=True)
if __name__=='__main__':main()
