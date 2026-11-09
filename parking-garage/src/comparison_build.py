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
    from graphics import generate
    folder=Path('textures/lookdev/comparison');layout=generate(folder,extra=True,extra_levels=8)
    bpy.ops.wm.open_mainfile(filepath=str(Path('build/ParkingGarage.blend').resolve()))
    templates={o.name:o for o in bpy.context.scene.objects if o.parent is None}
    for rr in templates.values():rr.location=(0,0,0)
    G.palette(folder)
    tower=G.root('Tower8',module_kind='Tower8');pieces.tower(tower,8);templates['Tower8']=tower
    p=garage(202,system='pt',levels=8,tee_count=24,comparison=True)
    p['structural_stations']=sorted({round(x,9) for x in p['structural_stations']})
    rt=make_garage(p,templates,layout);upgrade(rt,p,layout)
    for rr in list(rt.children):
        if not rr.name.startswith('ColumnShaft_'):continue
        height=max(v.co.z for ob in rr.children if ob.type=='MESH' for v in ob.data.vertices)
        for ob in list(rr.children):
            if ob.type=='MESH':bpy.data.objects.remove(ob,do_unlink=True)
        column=G.Mesh(rr.name+'__Round cast form',rr)
        column.tube([(0,0,0),(0,0,height)],.381,'Concrete',64);column.finish();rr['round_column']=True
    # This photograph has a cast edge downstand below the slab. It belongs
    # to this reference variant; the accepted town has its original edge.
    fascia=G.Mesh('Reference cast edge downstand',rt)
    for lev in range(1,p['levels']):
        for a,c in zip(p['structural_stations'],p['structural_stations'][1:]):
            if c-a<.8:continue
            fascia.box(((a+c)/2,-p['width']/2+.07,lev*FLOOR-.49),(c-a-.762,.32,.54))
    fascia.finish();p['reference_edge_downstand_m']=.54
    keep=set(members(rt))
    for ob in list(bpy.context.scene.objects):
        if ob not in keep:bpy.data.objects.remove(ob,do_unlink=True)
    export('export/form/comparison-harmon.gltf',[o for o in members(rt) if o.type!='CURVE'],Path('textures/lookdev').rglob('*.png'))
    Path('build/lookdev/comparison-harmon.json').write_text(json.dumps(p,indent=2)+'\n')
    bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/lookdev/comparison-harmon.blend').resolve()))
    from precast_specimen import build
    rt,p=build(json.loads(Path('textures/lookdev/layout.json').read_text()),tee_count=18,rear_spans=2)
    export('export/form/comparison-precast.gltf',[o for o in bpy.context.scene.objects if o.type!='CURVE'],Path('textures/lookdev').rglob('*.png'))
    from tangent_rounding import stabilize
    stabilize(Path('export/form/comparison-precast.gltf'))
    bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/lookdev/comparison-precast.blend').resolve()))


if __name__=='__main__':main()
