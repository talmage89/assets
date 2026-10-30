"""30 Hz port/section presentation of an exported, textured gun GLB.

Only source triangle attribution is used for the optional diagnostic section.
Rendered vertices, UVs, materials, skin and animation always come from the GLB.
"""
import argparse
import hashlib
import sys
from pathlib import Path
from types import SimpleNamespace

import bpy
from mathutils import Vector
from mathutils.kdtree import KDTree


def section(reference, names):
    import bmesh
    with bpy.data.libraries.load(str(Path(reference).resolve()), link=False) as (src, dst):
        dst.objects = [n for n in src.objects if any(n.startswith(p) for p in names)]
    triangles = []
    for ob in dst.objects:
        ob.data.calc_loop_triangles()
        triangles.extend([[ob.matrix_world @ ob.data.vertices[i].co for i in t.vertices]
                          for t in ob.data.loop_triangles])
    tree = KDTree(len(triangles))
    for i, points in enumerate(triangles):
        tree.insert(sum(points, Vector()) / 3, i)
    tree.balance()
    removed = 0
    for ob in [o for o in bpy.context.scene.objects if o.type == 'MESH']:
        mesh = ob.data
        selected = []
        for face in mesh.polygons:
            points = [ob.matrix_world @ mesh.vertices[i].co for i in face.vertices]
            center = sum(points, Vector()) / len(points)
            if center.x <= 0:
                continue
            for _, i, _ in tree.find_range(center, 2e-7):
                if max(min((p-q).length for q in triangles[i]) for p in points) < 2e-7:
                    selected.append(face.index)
                    break
        if selected:
            attr = mesh.attributes.new('SectionNormal', 'FLOAT_VECTOR', 'CORNER')
            attr.data.foreach_set('vector', [v for n in mesh.corner_normals for v in n.vector])
            bm = bmesh.new(); bm.from_mesh(mesh); bm.faces.ensure_lookup_table()
            bmesh.ops.delete(bm, geom=[bm.faces[i] for i in selected], context='FACES')
            bm.to_mesh(mesh); bm.free()
            mesh.normals_split_custom_set([r.vector[:] for r in mesh.attributes['SectionNormal'].data])
            mesh.attributes.remove(mesh.attributes['SectionNormal'])
            removed += len(selected)
    for ob in dst.objects:
        bpy.data.objects.remove(ob, do_unlink=True)
    assert removed, 'Section must identify actual imported triangles'
    return removed


def main(base, manifest, presentation, view, section_parts):
    from guns.common.render import main as render
    p = argparse.ArgumentParser()
    p.add_argument('--clip', required=True)
    p.add_argument('--start', type=int, default=0)
    p.add_argument('--end', type=int)
    p.add_argument('--cutaway', action='store_true')
    p.add_argument('--reference', default=str(base/'build/delivery/finalized.blend'))
    args, remaining = p.parse_known_args(sys.argv[sys.argv.index('--')+1:])
    end = args.end if args.end is not None else manifest.CLIPS[args.clip]['frames']
    frames = list(range(args.start, end+1, 2))
    if frames[-1] != end:
        frames.append(end)
    shots = {f'f{f:04d}': dict(view, action=args.clip, frame=f, time_s=f/60,
                              background='transparent', section=args.cutaway,
                              renderer_sha256=signature(base)) for f in frames}
    def configure(scene, source):
        removed = section(args.reference, section_parts) if args.cutaway else 0
        presentation.configure_scene(scene, source)
        for shot in shots.values():
            shot['removed_triangles'] = removed
            shot['section_parts'] = section_parts if args.cutaway else []
    config = SimpleNamespace(FINAL_STAGE=True, RENDER_STAGE='exported GLB / diagnostic right-half section' if args.cutaway else 'exported GLB / port',
        DEFAULT_SHOTS=','.join(shots), SHOTS=shots, PHOTO_POSES={},
        floor_height=presentation.floor_height, configure_scene=configure,
        prepare_shot=presentation.prepare_shot)
    sys.argv = [sys.argv[0], '--', *remaining]
    render(config, manifest)


def signature(base):
    return hashlib.sha256(Path(__file__).read_bytes()+(base/'src/cycle_views.py').read_bytes()).hexdigest()
