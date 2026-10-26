"""A short corner and gate proof assembled exclusively from the shipped GLB."""
import argparse,json,sys,hashlib,math
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from dimensions import *
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
src=Path(a.source).resolve();bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(src));obs=bpy.context.scene.objects
# The left corner replaces the staged end post. Keep the standalone right-end
# terminal at the far end of a true terminal-to-terminal transverse section.
for name in ('Chain_Terminal','Chain_Section'):
 root=obs[name]
 for ob in list(root.children_recursive)+[root]:bpy.data.objects.remove(ob,do_unlink=True)
corner=obs['Chain_Corner'];corner.location=(-PITCH,0,0);corner.rotation_mode='XYZ';corner.rotation_euler.z=-math.pi/2
turn=obs['Chain_BetweenTerminals'];turn.location=(-PITCH,PITCH/2,0);turn.rotation_mode='XYZ';turn.rotation_euler.z=math.pi/2
end=obs['Chain_Terminal_End'];end.location=(-PITCH,PITCH,0);end.rotation_mode='XYZ';end.rotation_euler.z=math.pi/2
obs['Chain_GateBay'].location=(PITCH+GATE_PITCH/2,0,0)
bpy.context.view_layer.update()
pairs=[('Chain_Start__L','Chain_Corner'),('Chain_Start__R','Chain_Line'),('Chain_EndSection__L','Chain_Line'),('Chain_EndSection__R','Chain_GateBay__L'),('Chain_BetweenTerminals__L','Chain_Corner'),('Chain_BetweenTerminals__R','Chain_Terminal_End')]
errors={a+' -> '+b:(obs[a].matrix_world.translation-obs[b].matrix_world.translation).length for a,b in pairs};assert max(errors.values())<2e-5,errors
out=Path(a.out).resolve();out.parent.mkdir(exist_ok=True,parents=True);bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',use_selection=True,export_yup=True,export_extras=True,export_animations=False,export_tangents=True)
report=dict(passed=True,source=str(src),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),output=str(out),snap_errors_m=errors)
out.with_suffix('.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
