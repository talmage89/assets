"""Reuse the car's connected-chart packing and explicit subpixel chart repair."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'cars/src'),str(ROOT)]
from sedan_finalize import main
def normalize(out,report):
    import bpy,json
    fixed=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or 'asset_set' not in ob:continue
        fallback=next((m for m in ob.data.materials if m),None)
        if fallback is None:raise ValueError('Unassigned bus surface '+ob.name)
        for index,m in enumerate(ob.data.materials):
            if m is None:ob.data.materials[index]=fallback;fixed.append(dict(mesh=ob.name,slot=index,material=fallback.name))
    data=json.loads(Path(report).read_text());data['boolean_cut_materials']=fixed;Path(report).write_text(json.dumps(data,indent=2))
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(out).resolve()));print('BUS_CUT_MATERIALS',fixed,flush=True)
if __name__=='__main__':
    import argparse,bpy
    p=argparse.ArgumentParser(add_help=False);p.add_argument('--out');p.add_argument('--report');p.add_argument('--repair-only',action='store_true');a,_=p.parse_known_args(sys.argv[sys.argv.index('--')+1:])
    if a.repair_only:bpy.ops.wm.open_mainfile(filepath=str(Path(a.out).resolve()))
    else:main()
    normalize(a.out,a.report)
