"""Read-only native library adapters. All products live in this family's build."""
import argparse
from pathlib import Path
import runpy
import sys
import os
import struct
import bpy
ROOT=Path(__file__).resolve().parents[2]
a=argparse.ArgumentParser();a.add_argument('--kind');a.add_argument('--out',type=Path);a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
sys.path.insert(0,str(ROOT))
bpy.ops.wm.read_factory_settings(use_empty=True)
if a.kind=='downtown':
    sys.path.insert(0,str(ROOT/'downtown/src'))
    from plan import generate
    from geometry import palette
    from graphics import generate as graphics
    from building import Building
    # The existing original source fallback is deliberately quick form PBR.
    plan=generate(411,'midwest',7);sheet,layout=graphics(Path('build/context/downtown-signs'));mats=palette(sheet)
    for lot in plan['lots']:
        rr,obs,doors=Building(lot,mats,layout).build();rr.location=(lot['x'],lot['y'],0)
elif a.kind=='commercial':
    sys.path.insert(0,str(ROOT/'commercial/src'))
    import strip_build,strip_graphics
    strip_graphics.generate(Path('build/strip/signs'))
    strip_build.build(201,Path('build/context/commercial-native'),plants=False,look=False)
    # Retain the building only; the garage has its own native-ground setting.
    for o in list(bpy.context.scene.objects):
        if o.type!='MESH':continue
        ancestors=[];p=o.parent
        while p:ancestors.append(p.name);p=p.parent
        if not any(s.startswith(('Bay_','EndCap_','Tower_','RoofLadder','MeterBank')) for s in ancestors):bpy.data.objects.remove(o,do_unlink=True)
else:
    # Original car generators and their section geometry; no invented proxies.
    sys.argv=['context_build.py','--','--kind',a.kind,'--out',str(a.out.with_suffix('.blend'))]
    runpy.run_path(str(ROOT/'downtown/src/context_build.py'),run_name='__main__')
    # Simple uniform checkpoint finishes survive stock glTF; the original
    # geometry is kept, with no source procedural shader claimed as baked.
    for m in bpy.data.materials:
        if not m.use_nodes:continue
        bs=m.node_tree.nodes.get('Principled BSDF')
        if not bs:continue
        if 'paint' in m.name.lower():
            tint=next((n for n in m.node_tree.nodes if n.name=='Paint tint'),None)
            color=tuple(tint.outputs[0].default_value) if tint else (.18,.24,.26,1)
        elif 'glass' in m.name.lower() or 'windshield' in m.name.lower():color=(.16,.23,.25,1)
        elif 'alloy' in m.name.lower() or 'chrome' in m.name.lower():color=(.45,.46,.44,1)
        else:color=(.025,.028,.027,1)
        for link in list(bs.inputs['Base Color'].links):m.node_tree.links.remove(link)
        bs.inputs['Base Color'].default_value=color
        for link in list(bs.inputs['Roughness'].links):m.node_tree.links.remove(link)
        bs.inputs['Roughness'].default_value=.28 if 'paint' in m.name.lower() else .55
        for key in ('Normal','Metallic'):
            for link in list(bs.inputs[key].links):m.node_tree.links.remove(link)
a.out.parent.mkdir(parents=True,exist_ok=True)
bpy.context.view_layer.update()
bpy.ops.export_scene.gltf(filepath=str(a.out.resolve()),export_format='GLB',export_yup=True,export_extras=True,export_animations=False,export_apply=True,export_tangents=False)
print('LOCAL NATIVE CONTEXT',a.kind,a.out,flush=True)
# Native vehicle graphs trigger a Blender 5.2 teardown crash on this platform.
# The synchronous exporter has already closed its output. Validate its complete
# container before ending the worker directly; fresh imports are checked later.
if a.kind in ('hatchback','crossover'):
    raw=a.out.read_bytes();assert raw[:4]==b'glTF' and struct.unpack_from('<I',raw,8)[0]==len(raw)
    sys.stdout.flush();sys.stderr.flush();os._exit(0)
