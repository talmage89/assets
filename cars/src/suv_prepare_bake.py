"""Prepare the reviewed SUV for the family atlas without editing that source."""
import argparse,sys
from pathlib import Path
import bpy
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
import prepare_bake
from suv_finishes import COLORS,PAINT_METAL


def main():
    p=argparse.ArgumentParser(add_help=False);p.add_argument('--out',required=True)
    a,_=p.parse_known_args(sys.argv[sys.argv.index('--')+1:]);prepare_bake.main()
    for mat in bpy.data.materials:
        if not mat.get('vehicle_paint'):continue
        nt=mat.node_tree
        nt.nodes['Paint tint'].outputs[0].default_value=(*COLORS['Atlantic'],1)
        nt.nodes['Paint metallic'].outputs[0].default_value=PAINT_METAL['Atlantic']
        nt.links.new(nt.nodes['OUT_paint_coverage'].outputs[0],nt.nodes['OUT_metal'].inputs[0])
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH':continue
        # Retain the original support's own Z-axis frame through consolidation.
        # Runtime re-aims the exported driver using the same measured endpoints.
        if 'support_pivot' in ob:
            driver=bpy.data.objects.new(ob.name+' driver',None);bpy.context.collection.objects.link(driver)
            driver.parent=ob.parent;driver.matrix_world=ob.matrix_world.copy();driver['static_root']=True
            for key in list(ob.keys()):
                if key.startswith('support_'):driver[key]=ob[key];del ob[key]
            ob.parent=driver;ob.matrix_parent_inverse=Matrix.Identity(4);ob.matrix_basis=Matrix.Identity(4)
            ob['export_part']=ob.name
        role=ob.data.attributes.get('skin_face_role');attr=ob.data.attributes.new('X220UVWeight','FLOAT','FACE')
        for f,d in zip(ob.data.polygons,attr.data):
            d.value=1 if role is None or role.data[f.index].value==0 else .18 if role.data[f.index].value==1 else .45
    bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
    from suv_tire_uv import prepare
    prepare();bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))


if __name__=='__main__':main()
