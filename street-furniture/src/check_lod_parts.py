"""Actual imported placement and permitted motion; original opaque-solid policy."""
import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from kit.lod import configuration
from kit.lod_io import Document, digest
from kit.motion import owned, sweep

parser = argparse.ArgumentParser()
parser.add_argument('--config', required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
cfg, family, source, output = configuration(Path(args.config))
manifest = json.loads((output/'manifest.json').read_text())
assert Document(source).dependencies() == manifest['baseline']
opaque_name = Document(source).data['materials'][0]['name']
paths = [source]+[output/r['path'] for r in manifest['levels'][1:]]
rows = []
for level, path in enumerate(paths):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path))
    meshes = [ob for ob in bpy.context.scene.objects if ob.type == 'MESH']
    root = bpy.data.objects[cfg['include_nodes'][0]]
    assert all(owned(ob, root) for ob in meshes)
    before = [ob.matrix_world@v.co for ob in meshes for v in ob.data.vertices]
    minimum = min(v.z for v in before)
    assert abs(minimum) < .0005, ('Lost ground contact', minimum)
    rest = root.matrix_world.copy()
    root.matrix_world = Matrix.Translation(Vector((1, 0, 0)))@rest
    bpy.context.view_layer.update()
    after = [ob.matrix_world@v.co for ob in meshes for v in ob.data.vertices]
    error = max((b-a-Vector((1, 0, 0))).length for a, b in zip(before, after))
    assert error < 1e-6, 'A mesh no longer follows its module root'
    root.matrix_world = rest
    bpy.context.view_layer.update()

    pivots = [ob for ob in root.children_recursive if 'pivot_axis' in ob]
    specs, physical, excluded = [], [], []
    for ob in meshes:
        if 'asset_set' in ob:
            del ob['asset_set']
        if not pivots:
            continue
        # Inspect actual opaque surfaces. The original meter graphics/lens are
        # explicitly non-solid open sheets. Keep that policy after static
        # consolidation puts them beside opaque faces in a multi-material mesh.
        faces = [tuple(p.vertices) for p in ob.data.polygons
                 if ob.material_slots[p.material_index].material.name == opaque_name]
        if not faces:
            excluded.append(ob.name)
            continue
        used = sorted({v for face in faces for v in face})
        remap = {v: i for i, v in enumerate(used)}
        mesh = bpy.data.meshes.new('Physical audit: opaque faces')
        mesh.from_pydata([ob.data.vertices[i].co for i in used], [],
                         [[remap[i] for i in face] for face in faces])
        ob.data = mesh
        ob['asset_set'] = 'StreetFurniture'
        ob['allow_boundary'] = False
        physical.append(dict(mesh=ob.name, faces=len(faces)))
    for pivot in pivots:
        axis = pivot['pivot_axis']
        assert axis == 'Z' and abs((pivot.matrix_world.to_3x3()@Vector((0, 0, 1))).z) > .999
        assert sum(owned(ob, pivot) for ob in meshes if 'asset_set' in ob) == 1
        specs.append(dict(node=pivot.name, axis=axis, step=5,
            range=[0, 0] if level else list(pivot['range_degrees']),
            tolerance_m=.0005, allow=[]))
    result = sweep(dict(MOTIONS=specs)) if specs else dict(passed=True, motions=[])
    result.update(level=level, sha256=digest(path), path=str(path.relative_to(ROOT)),
        placement_error_m=error, ground_minimum_m=minimum, physical_meshes=physical,
        non_solid_graphics_excluded=excluded)
    rows.append(result)
report = dict(passed=all(r['passed'] for r in rows), levels=rows,
    config_sha256=digest(Path(args.config)), script_sha256=digest(Path(__file__)),
    policy='Hold LOD0 while any coin door differs from rest; no moving/fixed pair exemptions',
    scope='All imported meshes for placement/ground; opaque actual surfaces for meter motion, matching original solid tags')
dest = family/'build'/('lod-'+cfg['readme_key']+'-parts.json')
dest.write_text(json.dumps(report, indent=2)+'\n')
assert report['passed'], str(dest)
