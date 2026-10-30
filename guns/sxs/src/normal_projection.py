"""Bake original dense forging normals through the game mesh's Mikk basis.

The GPU bake supplies all material channels and other parts' normals. Its
selected-to-active pass introduced directional noise beside the ground sides.
Re-evaluate the forging at each 4096 UV texel from its original dense geometry.
Construction ownership prevents projection across roof/lip/floor/end boundaries.
The actual ground planes are fitted by SVD. No painted or photo-derived pixels.
"""
import hashlib
import argparse
import json
import shutil
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils.bvhtree import BVHTree
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from kit.image_io import read_png, write_png

BASE = Path(__file__).resolve().parents[1]
SIZE = 4096
OUT = BASE / 'build/baked/precise4k'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ground(face, points):
    return (abs(face.normal.x) > .99999
            and all(abs(abs(p[0]) - .02595) < .000015 for p in points))


def dot(a, b):
    return np.einsum('ij,ij->i', a, b)


def unit(v):
    return v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-15)


def dense_sources(high):
    bpy.ops.wm.open_mainfile(filepath=str(high))
    mesh = bpy.data.objects['Action_Body'].data
    mesh.calc_loop_triangles()
    points = [v.co.copy() for v in mesh.vertices]
    positions = np.array([tuple(p) for p in points])
    normals = np.array([tuple(n.vector) for n in mesh.corner_normals])
    planes, fits, regions = {}, {}, {}
    for sign in (-1, 1):
        ids = sorted({i for f in mesh.polygons if f.normal.x * sign > 0
                      and ground(f, [points[j] for j in f.vertices]) for i in f.vertices})
        p = positions[ids]
        center = p.mean(axis=0)
        _, _, vectors = np.linalg.svd(p - center, full_matrices=False)
        n = vectors[-1] * np.sign(vectors[-1, 0]) * sign
        distances = (p - center) @ n
        planes[sign] = n
        fits[str(sign)] = dict(
            vertices=len(p), normal=n.tolist(), center_m=center.tolist(),
            rms_mm=float(np.sqrt(np.mean(distances**2)) * 1000),
            maximum_residual_mm=float(np.max(abs(distances)) * 1000))
        assert fits[str(sign)]['maximum_residual_mm'] < .03
    ownership = mesh.attributes['head_region']
    for region in range(5):
        triangles = [t for t in mesh.loop_triangles if ownership.data[t.polygon_index].value == region]
        assert triangles, region
        indices = np.array([tuple(t.vertices) for t in triangles])
        loops = np.array([tuple(t.loops) for t in triangles])
        regions[region] = (BVHTree.FromPolygons(points, indices.tolist(), all_triangles=True),
                           positions[indices], normals[loops])
    return planes, fits, regions


def source_normals(points, region):
    tree, positions, normals = region
    hits = [tree.find_nearest(tuple(p)) for p in points]
    assert all(h[2] is not None for h in hits)
    indices = np.array([h[2] for h in hits])
    p = np.array([tuple(h[0]) for h in hits])
    vertices, normals = positions[indices], normals[indices]
    e0, e1 = vertices[:, 1] - vertices[:, 0], vertices[:, 2] - vertices[:, 0]
    d = p - vertices[:, 0]
    d00, d01, d11 = dot(e0, e0), dot(e0, e1), dot(e1, e1)
    d20, d21 = dot(d, e0), dot(d, e1)
    denominator = d00 * d11 - d01 * d01
    b = (d11 * d20 - d01 * d21) / denominator
    c = (d00 * d21 - d01 * d20) / denominator
    n = normals[:, 0] * (1-b-c)[:, None] + normals[:, 1] * b[:, None] + normals[:, 2] * c[:, None]
    return unit(n), max(h[3] for h in hits) * 1000


def main():
    global OUT
    parser=argparse.ArgumentParser()
    parser.add_argument('--high',type=Path,default=BASE/'build/delivery/high.blend')
    parser.add_argument('--baked',type=Path,default=BASE/'build/baked/4k')
    parser.add_argument('--out',type=Path,default=OUT)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    OUT=args.out
    OUT.mkdir(parents=True, exist_ok=True)
    planes, fits, regions = dense_sources(args.high)
    bpy.ops.wm.open_mainfile(filepath=str(BASE / 'build/delivery/finalized.blend'))
    normal = read_png(args.baked/'T_Covey26_Normal.png')
    changed = np.zeros((SIZE, SIZE), bool)
    occupied = Image.new('1', (SIZE, SIZE))
    draw = ImageDraw.Draw(occupied)
    for ob in bpy.context.scene.objects:
        # The action's occupancy is the exact pixel-center raster below.
        # PIL's conservative polygon fill includes an extra fringe outside
        # its islands; blocking that fringe would retain noisy GPU values
        # inside the 2048 filter footprint. Protect other parts only here.
        if ob.name == 'Action_Body' or ob.type != 'MESH' or 'asset_set' not in ob:
            continue
        mesh = ob.data
        mesh.calc_loop_triangles()
        uv = mesh.uv_layers['BakeUV']
        for tri in mesh.loop_triangles:
            draw.polygon([(uv.data[j].uv.x*SIZE, (1-uv.data[j].uv.y)*SIZE) for j in tri.loops], fill=1)

    mesh = bpy.data.objects['Action_Body'].data
    mesh.calc_tangents(uvmap='BakeUV')
    mesh.calc_loop_triangles()
    uv = mesh.uv_layers['BakeUV']
    counts = {str(r): dict(triangles=0, texels=0, maximum_projection_distance_mm=0.) for r in range(5)}
    flat_triangles = flat_texels = 0
    for tri in mesh.loop_triangles:
        face = mesh.polygons[tri.polygon_index]
        ps = np.array([tuple(mesh.vertices[j].co) for j in tri.vertices])
        q = np.array([(uv.data[j].uv.x*SIZE-.5, (1-uv.data[j].uv.y)*SIZE-.5)
                      for j in tri.loops], dtype=np.float64)
        xmin, ymin = np.maximum(0, np.floor(q.min(axis=0)).astype(int))
        xmax, ymax = np.minimum(SIZE-1, np.ceil(q.max(axis=0)).astype(int))
        if xmax < xmin or ymax < ymin:
            continue
        yy, xx = np.mgrid[ymin:ymax+1, xmin:xmax+1]
        v0, v1 = q[1]-q[0], q[2]-q[0]
        determinant = v0[0]*v1[1]-v1[0]*v0[1]
        if abs(determinant) < 1e-10:
            continue
        dx, dy = xx-q[0, 0], yy-q[0, 1]
        b = (dx*v1[1]-v1[0]*dy)/determinant
        c = (v0[0]*dy-dx*v0[1])/determinant
        a = 1-b-c
        mask = (a >= -1e-8) & (b >= -1e-8) & (c >= -1e-8)
        if not mask.any():
            continue
        weights = np.stack((a[mask], b[mask], c[mask]), axis=1)
        n = unit(weights @ np.array([tuple(mesh.corner_normals[j].vector) for j in tri.loops]))
        t = weights @ np.array([tuple(mesh.loops[j].tangent) for j in tri.loops])
        t = unit(t - n * dot(t, n)[:, None])
        signs = weights @ np.array([mesh.loops[j].bitangent_sign for j in tri.loops])
        bitangent = np.cross(n, t) * np.sign(signs)[:, None]
        region = mesh.attributes['head_region'].data[tri.polygon_index].value
        distance = 0.
        if ground(face, ps):
            axis = np.broadcast_to(planes[int(np.sign(face.normal.x))], n.shape)
            flat_triangles += 1
            flat_texels += len(weights)
        else:
            axis, distance = source_normals(weights @ ps, regions[region])
        baked = unit(np.stack((dot(t, axis), dot(bitangent, axis), dot(n, axis)), axis=1))
        assert np.isfinite(baked).all(), (tri.index, region)
        normal[ymin:ymax+1, xmin:xmax+1][mask] = baked*.5+.5
        changed[ymin:ymax+1, xmin:xmax+1] |= mask
        count = counts[str(region)]
        count['triangles'] += 1
        count['texels'] += len(weights)
        count['maximum_projection_distance_mm'] = max(count['maximum_projection_distance_mm'], distance)

    # Pad into unoccupied gutter only, preserving all other atlas surfaces.
    ys, xs = np.nonzero(changed)
    x0, x1 = max(0, xs.min()-12), min(SIZE, xs.max()+13)
    y0, y1 = max(0, ys.min()-12), min(SIZE, ys.max()+13)
    patch = normal[y0:y1, x0:x1].copy()
    valid = changed[y0:y1, x0:x1].copy()
    block = np.asarray(occupied)[y0:y1, x0:x1] & ~valid
    for _ in range(12):
        new = valid.copy()
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            candidate = np.roll(valid, (dy, dx), axis=(0, 1)) & ~new & ~block
            patch[candidate] = np.roll(patch, (dy, dx), axis=(0, 1))[candidate]
            new |= candidate
        valid = new
    normal[y0:y1, x0:x1][valid] = patch[valid]
    write_png(OUT / 'T_Covey26_Normal.png', normal, 16)
    for channel in ('BaseColor', 'ORM'):
        shutil.copyfile(args.baked/f'T_Covey26_{channel}.png', OUT / f'T_Covey26_{channel}.png')
    report = dict(
        method='Dense original forging, ownership-constrained closest-surface normal projection through actual Mikk tangent basis',
        size=SIZE, regions=counts, source_planes=fits,
        ground_triangles=flat_triangles, ground_texels=flat_texels,
        interior_texels=int(changed.sum()), gutter_texels=int(valid.sum()-changed.sum()),
        gutter_policy='Exact action pixel-center occupancy; conservatively block every other part',
        source_sha256={'finalized.blend':digest(BASE/'build/delivery/finalized.blend'),'high.blend':digest(args.high)},
        gpu_normal_sha256=digest(args.baked/'T_Covey26_Normal.png'),
        output_normal_sha256=digest(OUT / 'T_Covey26_Normal.png'))
    (OUT / 'projection-report.json').write_text(json.dumps(report, indent=2))
    print('DENSE ACTION NORMAL PROJECTION', report)


if __name__ == '__main__':
    main()
