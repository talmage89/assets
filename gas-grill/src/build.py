"""Original Field 3 grill, clean-scene deterministic Blender 5.2 construction.

Separate manufacturing modules keep the asset parameterized and reviewable.
`game` tessellation is an honest pre-bake source audit, not an exported asset.
"""
import argparse,json,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G
from parts import Build
from cart import build_cart,build_shelves
from cookbox import build_firebox
from hood import build_hood
from controls import build_controls
from fuel import build_fuel


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    parser.add_argument('--quality',choices=['high','game'],default='high')
    parser.add_argument('--wear',type=float,default=.35)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if not 0<=args.wear<=2:raise ValueError('wear must be in [0,2]')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    b=Build(args.quality=='high',args.wear,ROOT/'gas-grill/build/markings')
    build_cart(b)
    build_shelves(b)
    build_firebox(b)
    build_controls(b)
    build_hood(b)
    build_fuel(b)
    # Top-level origin is centered on the actual load-bearing ground footprint.
    asset=G.pivot('GasGrill',(0,0,0));b.root.parent=asset
    b.root.location.x=-.0555
    scene=bpy.context.scene
    scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
    scene['asset']='GasGrill';scene['quality']=args.quality;scene['wear']=args.wear
    scene['reference_dimensions']=json.dumps({'width':1.3208,'height':1.1303,'depth':.6858})
    scene['stage']='lookdev';scene['checkpoint']=3;scene['seed']=41
    bpy.context.view_layer.update()
    bpy.ops.file.pack_all()
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(args.out).resolve()))
    counts={}
    for ob in scene.objects:
        if ob.type=='MESH':
            ob.data.calc_loop_triangles();key=ob.get('asset_set','Grill')
            counts[key]=counts.get(key,0)+len(ob.data.loop_triangles)
    print('BUILD_COUNTS',json.dumps(counts),flush=True)

if __name__=='__main__':main()
