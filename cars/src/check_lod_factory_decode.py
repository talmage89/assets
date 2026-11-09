"""Fresh-import execution of the delivered decoder on each LOD and preset.

Run in Blender with --source, --manifest and --out. This checks routing and
shader state; native renders separately prove appearance and optical transfer.
"""
import argparse
import json
import sys
from pathlib import Path
import bpy

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from kit.lod_io import Document,digest
import delivery_materials as decoder


def surface(material):
    return next(n for n in material.node_tree.nodes if n.type=='BSDF_PRINCIPLED')


def state(material):
    bs=surface(material)
    def record(key):
        s=bs.inputs[key]
        if s.is_linked:
            return [(link.from_node.name,link.from_socket.name) for link in s.links]
        v=s.default_value
        return list(v) if hasattr(v,'__len__') else v
    return {key:record(key) for key in ('Base Color','Metallic','Roughness','Transmission Weight')}


def check(source,paths,out):
    reference=next(m['extras'] for m in Document(source).data['materials']
                   if m.get('extras',{}).get('paint_decode')=='reference_plus_coverage_delta')
    colors=json.loads(reference['paint_colors']);metals=json.loads(reference['paint_metallic'])
    results=[];errors=[]
    for path in paths:
        doc=Document(path)
        paints=[m for m in doc.data['materials'] if m.get('extras',{}).get('paint_decode')==reference['paint_decode']]
        if len(paints)!=1:
            errors.append(f'{path.name}: expected one paint contract');continue
        for key in ('paint_colors','paint_metallic','paint_reference_color'):
            if paints[0]['extras'].get(key)!=reference[key]:errors.append(f'{path.name}: changed {key}')
        for preset,tint in colors.items():
            bpy.ops.wm.read_factory_settings(use_empty=True)
            bpy.ops.import_scene.gltf(filepath=str(path.resolve()),import_pack_images=False)
            paint=decoder.paint_material()
            ordinary={m.name:state(m) for m in bpy.data.materials if m.use_nodes and m!=paint}
            try:
                decoder.apply(preset,lights=False)
                delta=[s.default_value for s in paint.node_tree.nodes['Factory delta'].inputs]
                expected=[v-r for v,r in zip(tint,reference['paint_reference_color'])]
                assert max(abs(a-b) for a,b in zip(delta,expected))<1e-6
                assert abs(paint.node_tree.nodes['Factory metallic'].inputs[1].default_value-metals[preset])<1e-6
                assert surface(paint).inputs['Base Color'].is_linked
                assert surface(paint).inputs['Metallic'].is_linked
                for name,prior in ordinary.items():assert state(bpy.data.materials[name])==prior
                lamps=[m for m in bpy.data.materials if m.get('lamp_strength')]
                assert lamps,'Missing lamp-state routing'
                for lights in (False,True):
                    decoder.apply(preset,lights=lights)
                    for lamp in lamps:
                        power=lamp.node_tree.nodes.get('Lamp power')
                        value=power.inputs[1].default_value if power else surface(lamp).inputs['Emission Strength'].default_value
                        assert abs(value-(lamp['lamp_strength'] if lights else 0))<1e-4
                results.append(dict(path=str(path),sha256=digest(path),preset=preset,
                                    metallic=metals[preset],lights=[False,True],passed=True))
            except (AssertionError,StopIteration,KeyError) as exc:
                errors.append(f'{path.name}/{preset}: {type(exc).__name__}: {exc}')
    report=dict(passed=not errors,errors=errors,results=results,decoder_sha256=digest(Path(decoder.__file__)),
                scope='Actual delivered decoder execution and shader-routing proof; appearance checked separately')
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=report['passed'],imports=len(results),errors=errors)))
    if errors:raise SystemExit(1)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    manifest=json.loads(a.manifest.read_text())
    paths=[a.source]+[a.manifest.parent/r['path'] for r in manifest['levels'] if r['level']]
    check(a.source,paths,a.out)
