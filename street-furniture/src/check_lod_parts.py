"""Actual imported placement and permitted motion; original opaque-solid policy."""
import argparse
import json
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from kit.lod import configuration
from kit.lod_io import Document, digest
from kit.motion import owned, sweep
from kit.lod_scene import construction_components


def shelter_supports(meshes, opaque_name, intact):
    """Separate actual construction shells, then ray-test every pad and column."""
    vertices, faces, all_vertices, all_faces = [], [], [], []
    for ob in meshes:
        points = [ob.matrix_world@v.co for v in ob.data.vertices]
        offset = len(all_vertices)
        all_vertices.extend(points)
        all_faces.extend(tuple(offset+i for i in p.vertices) for p in ob.data.polygons)
        offset = len(vertices)
        vertices.extend(points)
        faces.extend(tuple(offset+i for i in p.vertices) for p in ob.data.polygons
                     if ob.material_slots[p.material_index].material.name == opaque_name)
    xyz, triangles = np.array(vertices), np.array(faces)
    parts = []
    for ids in construction_components({'POSITION': xyz}, triangles):
        tris = xyz[triangles[ids]]
        points = tris.reshape(-1, 3)
        normal = np.cross(tris[:, 1]-tris[:, 0], tris[:, 2]-tris[:, 0])
        normal /= np.maximum(np.linalg.norm(normal, axis=1, keepdims=True), 1e-20)
        parts.append(dict(lo=points.min(0), hi=points.max(0), tris=tris,
            bottom=tris[normal[:, 2]<-.99].reshape(-1, 3),
            tree=BVHTree.FromPolygons(points, np.arange(len(points)).reshape(-1, 3), all_triangles=True)))
    slabs = [p for p in parts if (p['hi']-p['lo'])[0]>4 and (p['hi']-p['lo'])[1]>1.7]
    assert len(slabs) == 1
    slab = slabs[0]
    pads = [p for p in parts if np.all(np.abs((p['hi']-p['lo'])-np.array((.16,.16,.02)))<.006)]
    columns = [p for p in parts if 2.29<(p['hi']-p['lo'])[2]<2.31
               and np.all(np.abs((p['hi']-p['lo'])[:2]-.0635)<.006)]
    assert len(pads) == len(columns) == 6, ('Lost support shells', len(pads), len(columns))
    rows = []
    for column in columns:
        center = (column['lo']+column['hi'])/2
        pad = min(pads, key=lambda p: np.linalg.norm(((p['lo']+p['hi'])/2-center)[:2]))
        gaps, insertion = [], []
        assert len(pad['bottom']) and len(column['bottom'])
        for point in pad['bottom']:
            hit = slab['tree'].ray_cast(Vector(point)+Vector((0,0,1)), Vector((0,0,-1)), 2)[0]
            assert hit is not None
            gaps.append(float(point[2]-hit.z))
        for point in column['bottom']:
            hit = pad['tree'].ray_cast(Vector(point)+Vector((0,0,1)), Vector((0,0,-1)), 2)[0]
            assert hit is not None
            insertion.append(float(hit.z-point[2]))
        gap = max(map(abs, gaps))
        depth = float(pad['hi'][2]-pad['lo'][2])
        rows.append(dict(center_xy_m=center[:2].tolist(), pad_samples=len(gaps),
            max_pad_slab_gap_m=gap, column_samples=len(insertion),
            column_insertion_range_m=[min(insertion),max(insertion)],
            passed=gap<=.0005 and min(insertion)>=-.0005 and max(insertion)<=depth+.0005))
    tree = BVHTree.FromPolygons(all_vertices, all_faces, all_triangles=True)
    hit = tree.ray_cast(Vector((1.2,.3,1.31)),Vector((0,1,0)),.6)[0]
    pane_ok = (hit is not None) == intact
    return dict(passed=pane_ok and all(r['passed'] for r in rows), supports=rows,
        tolerance_m=.0005, pane_passed=pane_ok, rear_right_pane_hit_m=list(hit) if hit else None)

parser = argparse.ArgumentParser()
parser.add_argument('--config', required=True)
parser.add_argument('--source-only', action='store_true')
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
cfg, family, source, output = configuration(Path(args.config))
opaque_name = Document(source).data['materials'][0]['name']
paths = [source]
if not args.source_only:
    manifest = json.loads((output/'manifest.json').read_text())
    assert Document(source).dependencies() == manifest['baseline']
    paths += [output/r['path'] for r in manifest['levels'][1:]]
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
    supports = (shelter_supports(meshes, opaque_name, cfg['name']=='Shelter')
                if cfg['name'].startswith('Shelter') else None)

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
    if supports:
        result['passed'] &= supports['passed']
    result.update(level=level, sha256=digest(path), path=str(path.relative_to(ROOT)),
        placement_error_m=error, ground_minimum_m=minimum, physical_meshes=physical,
        non_solid_graphics_excluded=excluded, shelter_supports=supports)
    rows.append(result)
report = dict(passed=all(r['passed'] for r in rows), levels=rows,
    source_only=args.source_only,
    config_sha256=digest(Path(args.config)), script_sha256=digest(Path(__file__)),
    policy='Hold LOD0 while any coin door differs from rest; no moving/fixed pair exemptions',
    scope='All imported meshes for placement/ground; opaque actual surfaces for meter motion, matching original solid tags')
suffix = '-source-parts.json' if args.source_only else '-parts.json'
dest = family/'build'/('lod-'+cfg['readme_key']+suffix)
dest.write_text(json.dumps(report, indent=2)+'\n')
assert report['passed'], str(dest)
