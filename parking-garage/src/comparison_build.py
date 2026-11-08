"""Photo comparison specimens built by the same bounded garage generator.

Town proof seeds retain their accepted programs. Harmon shows a taller
column stack; the precast photograph uses deeper haunches at the same seat.
"""
import json,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
import geometry as G
from plan import garage,FLOOR
from build import make_garage,members,export
from form import upgrade


def main():
    folder=Path('textures/lookdev');layout=json.loads((folder/'layout.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(Path('build/ParkingGarage.blend').resolve()))
    templates={o.name:o for o in bpy.context.scene.objects if o.parent is None}
    for rr in templates.values():rr.location=(0,0,0)
    G.palette(folder)
    p=garage(202,system='pt',levels=5,tee_count=16);rt=make_garage(p,templates,layout);upgrade(rt,p,layout)
    keep=set(members(rt))
    for ob in list(bpy.context.scene.objects):
        if ob not in keep:bpy.data.objects.remove(ob,do_unlink=True)
    export('export/form/comparison-harmon.gltf',[o for o in members(rt) if o.type!='CURVE'],folder.glob('*.png'))
    Path('build/lookdev/comparison-harmon.json').write_text(json.dumps(p,indent=2)+'\n')
    bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/lookdev/comparison-harmon.blend').resolve()))
    bpy.ops.wm.open_mainfile(filepath=str(Path('build/lookdev/form-101.blend').resolve()))
    rt=bpy.data.objects['Garage_101']
    for ob in rt.children_recursive:
        if ob.type!='MESH' or not ob.name.startswith('BearingCorbels_'):continue
        ob.data=ob.data.copy()
        for v in ob.data.vertices:
            if abs(v.co.z-(FLOOR-1.6))<.00001:v.co.z-=(FLOOR-1.6)*.15
        ob.data.update()
    rt['comparison_variant']='Haunch lower apex at 1.48988m; bearing ledges and tee sections unchanged'
    export('export/form/comparison-precast.gltf',[o for o in members(rt) if o.type!='CURVE'],folder.glob('*.png'))
    bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/lookdev/comparison-precast.blend').resolve()))


if __name__=='__main__':main()
