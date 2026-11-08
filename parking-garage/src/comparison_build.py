"""Photo comparison specimens built by the same bounded garage generator.

Town proof seeds retain their accepted programs. Harmon shows a taller
column stack; the precast photograph uses deeper haunches at the same seat.
"""
import json,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
import geometry as G
import pieces
from plan import garage,FLOOR
from build import make_garage,members,export
from form import upgrade


def main():
    folder=Path('textures/lookdev');layout=json.loads((folder/'layout.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(Path('build/ParkingGarage.blend').resolve()))
    templates={o.name:o for o in bpy.context.scene.objects if o.parent is None}
    for rr in templates.values():rr.location=(0,0,0)
    G.palette(folder)
    tower=G.root('Tower6',module_kind='Tower6');pieces.tower(tower,6);templates['Tower6']=tower
    p=garage(202,system='pt',levels=6,tee_count=24,comparison=True);rt=make_garage(p,templates,layout);upgrade(rt,p,layout)
    keep=set(members(rt))
    for ob in list(bpy.context.scene.objects):
        if ob not in keep:bpy.data.objects.remove(ob,do_unlink=True)
    export('export/form/comparison-harmon.gltf',[o for o in members(rt) if o.type!='CURVE'],folder.glob('*.png'))
    Path('build/lookdev/comparison-harmon.json').write_text(json.dumps(p,indent=2)+'\n')
    bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/lookdev/comparison-harmon.blend').resolve()))
    from precast_specimen import build
    rt,p=build(layout)
    export('export/form/comparison-precast.gltf',[o for o in bpy.context.scene.objects if o.type!='CURVE'],folder.glob('*.png'))
    from tangent_rounding import stabilize
    stabilize(Path('export/form/comparison-precast.gltf'))
    bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/lookdev/comparison-precast.blend').resolve()))


if __name__=='__main__':main()
