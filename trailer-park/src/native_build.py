"""Build absent native library modules locally, without altering their families.

Executed in a separate Blender process per family to isolate generic imports.
All geometry comes from the current native scripts. Quick finishes are explicit.
"""
from pathlib import Path
import argparse,sys,runpy
import bpy
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('kind');args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
folder=ROOT/args.kind/'src';sys.path[:0]=[str(folder),str(ROOT)]
target=Path('build/native');target.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)

if args.kind=='shed':
    d=runpy.run_path(str(folder/'build.py'))
    from types import SimpleNamespace
    s=d['Shed'](SimpleNamespace(quality='game',wear=.55))
    for part in ('floor','walls','doors','roof'):d[part](s)
    # Source procedural finishes are replaced by measured palette constants
    # for this form gate; none is advertised as a new or baked texture set.
    for ma in bpy.data.materials:
        if not ma.use_nodes:continue
        bs=next((n for n in ma.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if not bs:continue
        for key in ('Base Color','Normal','Roughness','Metallic'):
            for link in list(bs.inputs[key].links):ma.node_tree.links.remove(link)
        name=ma.name.lower();color=(.21,.27,.21) if 'sage' in name else (.55,.53,.45) if 'white' in name else (.055,.055,.048) if 'shingle' in name or 'felt' in name else (.20,.16,.09)
        bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.78
elif args.kind=='utility':
    import surfaces
    surfaces.material=lambda:None
    surfaces.uv_object=lambda *args:None
    d=runpy.run_path(str(folder/'build.py'))
    d['palette']();spec=d['pole_spec'](length_ft=35,phases=1,framing='armless',comm=True,kind='transformer',seed=22)
    spec.update(light=True,bank=1,comm_count=1)
    d['pole']('ParkPole',spec)
elif args.kind=='playground':
    import geometry as F,parts as P
    F.init(False);r=F.root('ParkSwings');P.swing_frame(r)
    # Native two-bay frame with four native molded belt seats.
    for x in (-2.26,-1.09,1.09,2.26):
        s=F.root('Belt');P.swing(s);s.parent=r;s.location=(x,0,2.4384)
    F.finish(r)
    t=F.root('SpringToy');P.spring(t);t.location=(5.5,0,0);F.finish(t)
else:raise ValueError(args.kind)

from kit import model as G
for ob in list(bpy.context.scene.objects):
    if ob.type!='MESH':continue
    G.apply(ob)
    if not ob.data.uv_layers:
        uv=ob.data.uv_layers.new(name='UVMap')
        for f in ob.data.polygons:
            axes=sorted(range(3),key=lambda k:abs(f.normal[k]))[:2]
            for li in f.loop_indices:
                v=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]],v[axes[1]])
bpy.ops.export_scene.gltf(filepath=str((target/(args.kind+'.gltf')).resolve()),export_format='GLTF_SEPARATE',export_texture_dir='images',export_extras=True,export_animations=False,export_tangents=False)
