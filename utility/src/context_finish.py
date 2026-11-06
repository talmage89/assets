"""Stage the library's own house surfaces without publishing another asset.

Presentation context uses the original family look-development shaders/fields.
Only utility parts are being delivered and judged as baked exports this round.
"""
import argparse,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'houses/src'),str(ROOT)]
import bpy

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--type',required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    from importlib import import_module
    module=import_module(dict(builder_colonial='lookdev',ranch='ranch_lookdev',cape='cape_lookdev',split='split_lookdev')[a.type])
    module.prepare(a.source,a.out)
    # Presentation never opens house doors. Two retained meshes (roof/shell)
    # keep the real roof-ray audit and avoid cloning hundreds of construction
    # meshes for every far house. Materials, UVs and authored tints survive.
    from kit import model as G
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    groups={roof:[o for o in meshes if ('roof' in o.name.lower())==roof] for roof in (False,True)}
    for roof,group in groups.items():
        if not group:continue
        bpy.ops.object.select_all(action='DESELECT')
        for ob in group:G.apply(ob);ob.select_set(True)
        bpy.context.view_layer.objects.active=group[0];bpy.ops.object.join();group[0].name='Context_Roof' if roof else 'Context_Shell'
    # Context materials retain scripted UV transforms. Save a packed source,
    # then export only the unchanged glTF geometry for the house fit check.
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(a.out.resolve()))
    # Unlike the utility delivery, these source shaders do not all fit stock
    # glTF. Renderer appends this packed scene rather than exporting the look.
