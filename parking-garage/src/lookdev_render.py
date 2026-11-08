"""Cycles review of the revised external glTFs, with source/image receipts."""
import argparse,json,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from render import render_shot,shots,overlays
from light_review import lighting,views


def main():
    a=argparse.ArgumentParser();a.add_argument('--stage',default='form');a.add_argument('--out',type=Path,default=Path('renders/form-pass1'));a.add_argument('--seeds',default='101,202');a.add_argument('--shots',default='hero,retained_hero,above,aisle,tower');a.add_argument('--width',type=int,default=1200);a.add_argument('--samples',type=int,default=24);a.add_argument('--source-finish',action='store_true');args=a.parse_args(sys.argv[sys.argv.index('--')+1:]);receipts=[]
    for seed in map(int,args.seeds.split(',')):
        p=json.loads(Path(f'build/lookdev/garage-{seed}.json').read_text())
        bpy.ops.wm.read_factory_settings(use_empty=True)
        prefix='ParkingGarageFormSite' if args.stage=='form' else 'ParkingGarageLookSite'
        path=Path(f'export/{args.stage}/sites/{prefix}-{seed}.gltf');bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
        if args.source_finish:
            from atlas_binding import source_finish
            source_finish()
        cache=Path(f'build/lookdev/render-{args.stage}-{seed}.blend').resolve();bpy.ops.wm.save_as_mainfile(filepath=str(cache))
        shotdefs=views(p,shots)
        for name in args.shots.split(','):
            if name=='plan_path' and seed!=101:continue
            shot=shotdefs[name];bpy.ops.wm.open_mainfile(filepath=str(cache))
            if shot.get('paths'):overlays(p)
            lighting(interior=shot.get('interior',False))
            r=render_shot(args.out/str(seed)/(name+'.png'),shot,args.width,args.samples,shot.get('engine','CYCLES'),path)
            from hashlib import sha256
            d=json.loads(path.read_text());r['images']={im['uri']:sha256((path.parent/im['uri']).read_bytes()).hexdigest() for im in d.get('images',[])}
            r.update(seed=seed,name=name,stage=args.stage,source_finish=args.source_finish)
            receipts.append(r);(args.out/'views.json').write_text(json.dumps(receipts,indent=2)+'\n')
    print('EXPORTED REVIEW COMPLETE',args.out,len(receipts),flush=True)


if __name__=='__main__':main()
