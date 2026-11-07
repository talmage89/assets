"""Keep the game scene separate from retained dense manufacturing sculpts."""
import argparse,sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit import model as G
from mathutils import Matrix
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
for o in list(bpy.context.scene.objects):
    if o.get('source_only'):bpy.data.objects.remove(o,do_unlink=True)
    elif o.type=='MESH':
        fallback=o.data.materials[2] if o.get('part')=='deck' else next(m for m in o.data.materials if m)
        for i,m in enumerate(o.data.materials):
            if m is None:o.data.materials[i]=fallback
bpy.data.objects['Skateboard']['checkpoint']='Game assembly / baked PBR atlas'
# Temporary projection owners are deliberately not moving pivots. The kit
# exporter consolidates their parts and removes these empty helpers.
for o in list(bpy.context.scene.objects):
    if o.type=='MESH' and o.get('asset_set'):
        frame=G.pivot('Projection / '+o.name,(0,0,0));frame.parent=o.parent;frame.matrix_basis=Matrix.Identity(4);G.attach(o,frame,asset_set='Skateboard')
bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
