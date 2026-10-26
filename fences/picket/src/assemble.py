"""Build a corner/gate demonstration using ONLY the exported baked library.

No source modeling meshes or materials are loaded. Instances share mesh data
and the library's one atlas material. This GLB is a render/fit proof, not an
additional texture family or a replacement for the independent module library.
"""
import argparse,json,sys,hashlib,math
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from dimensions import *


def clone_tree(root,name):
    members=[root]+list(root.children_recursive);copies={}
    for original in members:
        ob=original.copy();bpy.context.scene.collection.objects.link(ob);copies[original]=ob
    for original,ob in copies.items():
        ob.parent=copies.get(original.parent);ob.matrix_basis=original.matrix_basis.copy()
        ob.name=name if original==root else name+'__'+original.name
    return copies[root]

p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
source=Path(a.source).resolve();bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source))
obs=bpy.context.scene.objects
turn=clone_tree(obs['Picket_A'],'Corner_Section');turn.location=(-PITCH,PITCH/2,0);turn.rotation_mode='XYZ';turn.rotation_euler.z=-math.pi/2
corner=obs['Picket_Corner'];corner.location=(-PITCH,0,0);corner.rotation_mode='XYZ';corner.rotation_euler.z=-math.pi/2
end=obs['Picket_End'];end.location=(-PITCH,PITCH,0);end.rotation_mode='XYZ';end.rotation_euler.z=-math.pi/2
obs['Picket_GateBay'].location=(PITCH+GATE_PITCH/2,0,0)
bpy.context.view_layer.update()
# Measure actual transformed sockets against post centers and one another.
pairs=[('Picket_A__L','Picket_Corner'),('Picket_A__R','Picket_Line'),('Picket_B__L','Picket_Line'),
       ('Picket_B__R','Picket_GateBay__L'),('Corner_Section__Picket_A__R','Picket_Corner'),('Corner_Section__Picket_A__L','Picket_End')]
errors={left+' -> '+right:(obs[left].matrix_world.translation-obs[right].matrix_world.translation).length for left,right in pairs}
assert max(errors.values())<2e-5,errors
out=Path(a.out).resolve();out.parent.mkdir(exist_ok=True,parents=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',use_selection=True,export_yup=True,export_extras=True,export_animations=False,export_tangents=True)
report=dict(source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),output=str(out),snap_errors_m=errors,passed=True)
out.with_suffix('.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
