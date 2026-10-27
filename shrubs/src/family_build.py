"""Assemble independently reviewable shrubs into one shared-atlas source library."""
import argparse,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--wear',type=float);p.add_argument('--quality');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for species in ('boxwood','hydrangea'):
        path=Path('build')/species/'lookdev.blend'
        with bpy.data.libraries.load(str(path.resolve()),link=False) as (src,dst):dst.objects=list(src.objects)
        for ob in dst.objects:
            if ob:bpy.context.scene.collection.objects.link(ob)
    # Both specimens use precisely the same node definition and image files.
    mats={}
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        for slot in ob.material_slots:
            key=slot.material.name.split('.00')[0]
            if key in mats:slot.material=mats[key]
            else:mats[key]=slot.material
    bpy.context.scene.unit_settings.system='METRIC';bpy.context.view_layer.update()
    a.out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()))
if __name__=='__main__':main()
