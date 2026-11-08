"""Independent form revision and complete town exports, leaving baseline bytes.

Run plain Blender serially after make's accepted checkpoint construction.
This stage does no Cycles work and does not hold the GPU lock.
"""
import argparse,json,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
import geometry as G
from graphics import generate
from build import export,members
from form import upgrade
from setting import town


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seeds',default='101,202');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    folder=Path('textures/lookdev');layout=generate(folder,extra=True);receipts=[]
    for seed in map(int,args.seeds.split(',')):
        bpy.ops.wm.open_mainfile(filepath=str(Path(f'build/garage-{seed}.blend').resolve()))
        rt=bpy.data.objects['Garage_'+str(seed)];keep=set(members(rt))
        for ob in list(bpy.context.scene.objects):
            if ob not in keep:bpy.data.objects.remove(ob,do_unlink=True)
        p=json.loads(Path(f'build/garage-{seed}.json').read_text());G.palette(folder);upgrade(rt,p,layout)
        for key in ('Glass',):
            bs=G.M[key].node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.035
        p['delivery']=export(f'export/form/ParkingGarageForm-{seed}.gltf',[o for o in members(rt) if o.type!='CURVE'],folder.glob('*.png'))
        Path(f'build/lookdev/garage-{seed}.json').write_text(json.dumps(p,indent=2)+'\n')
        bpy.ops.wm.save_as_mainfile(filepath=str(Path(f'build/lookdev/form-{seed}.blend').resolve()))
        ctx=town(p,rt)
        from town_detail import refine
        refine(ctx['root'],p,layout)
        report={k:v for k,v in ctx.items() if k!='root'}
        report['context_triangles']=G.triangles(members(ctx['root']))
        Path(f'build/lookdev/actors-{seed}.json').write_text(json.dumps(report,indent=2)+'\n')
        path=Path(f'export/form/sites/ParkingGarageFormSite-{seed}.gltf')
        delivery=export(path,list(bpy.context.scene.objects),folder.glob('*.png'))
        bpy.ops.wm.save_as_mainfile(filepath=str(Path(f'build/lookdev/form-site-{seed}.blend').resolve()))
        receipts.append(dict(seed=seed,garage_triangles=p['garage_triangles'],**report,delivery=delivery))
        Path('build/lookdev/form-sites.json').write_text(json.dumps(receipts,indent=2)+'\n')
        print('REFINED FORM',seed,p['garage_triangles'],flush=True)


if __name__=='__main__':main()
