"""Measure permitted rest LODs and the interaction hold, with bounded bearings."""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Matrix

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from kit.lod import configuration
from kit.lod_io import Document, digest
from kit.motion import inside, owned, surface

NAMES = ('Lid', 'Wheel_Left', 'Wheel_Right')
TOLERANCE = .0002


def selected_level(requested, angles):
    """Restore the original before changing a mechanism from its rest pose."""
    return 0 if any(abs(angles[name]) > 1e-9 for name in NAMES) else requested


def bearing(point, name):
    # Finite source pin/axle envelopes, plus 0.5 mm. These are intended solid
    # bearing interfaces, not exemptions for a whole lid/body or wheel/body pair.
    if name == 'Lid':
        return any(abs(point.x-sign*.263) <= .0425 and
                   math.hypot(point.y-.391075, point.z-1.032) <= .0085
                   for sign in (-1, 1))
    return abs(point.x) <= .3315 and math.hypot(
        point.y-.314925, point.z-.127) <= .0084375


def contact(a, b, name):
    if any(min(a['hi'][k], b['hi'][k])-max(a['lo'][k], b['lo'][k]) <= TOLERANCE
           for k in range(3)):
        return dict(depth_m=0, bearing_samples=0, bearing_depth_m=0)
    pairs = a['tree'].overlap(b['tree'])
    result = dict(depth_m=0, bearing_samples=0, bearing_depth_m=0)

    def measure(point, other):
        if any(point[k] < other['lo'][k] or point[k] > other['hi'][k] for k in range(3)):
            return
        hit = other['tree'].find_nearest(point)
        if hit[0] is None or hit[3] <= TOLERANCE:
            return
        if (point-hit[0]).dot(hit[1]) >= 0 or not inside(other['tree'], point):
            return
        if bearing(point, name):
            result['bearing_samples'] += 1
            result['bearing_depth_m'] = max(result['bearing_depth_m'], hit[3])
        else:
            if hit[3] > result['depth_m']:
                result['depth_m'] = hit[3]
                result['point_m'] = list(point)

    for current, other, indices in (
            (a, b, {x for x, _ in pairs}), (b, a, {y for _, y in pairs})):
        if not pairs:
            for point in current['points'][::max(1, len(current['points'])//12)]:
                measure(point, other)
            continue
        edges, vertices = set(), set()
        for index in indices:
            triangle = current['faces'][index]
            vertices.update(triangle)
            edges.update(tuple(sorted((triangle[i], triangle[(i+1)%3]))) for i in range(3))
        for index in vertices:
            measure(current['points'][index], other)
        for u, v in edges:
            p, q = current['points'][u], current['points'][v]
            length = (q-p).length
            if length < 1e-9:
                continue
            direction = (q-p)/length
            distances, cursor = [0., length], 0.
            for _ in range(64):
                hit = other['tree'].ray_cast(p+direction*(cursor+1e-7), direction, length-cursor)
                if hit[0] is None:
                    break
                cursor = (hit[0]-p).dot(direction)
                if cursor >= length:
                    break
                distances.append(cursor)
            distances.sort()
            for left, right in zip(distances, distances[1:]):
                if right-left > 2*TOLERANCE:
                    measure(p+direction*((left+right)*.5), other)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    cfg, family, source, output = configuration(Path(args.config))
    baseline = Document(source).dependencies()
    manifest = json.loads((output/'manifest.json').read_text())
    assert baseline == manifest['baseline']
    paths = [source]+[output/r['path'] for r in manifest['levels'][1:]]
    rows = []
    for level, path in enumerate(paths):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(path))
        meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
        assert len(meshes) == 4, 'Body, lid and two wheel meshes must remain separate'
        motions = []
        for name in NAMES:
            pivot = bpy.data.objects[name]
            moving = [o for o in meshes if owned(o, pivot)]
            fixed = [o for o in meshes if o not in moving]
            assert len(moving) == 1 and len(fixed) == 3
            assert pivot.get('pivot_axis') == 'X'
            rest = pivot.matrix_basis.copy()
            stationary = {o.name: surface(o) for o in fixed}
            if level:
                values = [0]
            elif name == 'Lid':
                values = list(range(0, -111, -1))
            else:
                values = list(range(0, 361, 5))
            maximum, allowed, worst, bearing_depth = 0., 0, None, 0.
            for angle in values:
                angles = dict.fromkeys(NAMES, 0.)
                angles[name] = angle
                assert selected_level(level, angles) == (0 if angle else level)
                pivot.matrix_basis = rest@Matrix.Rotation(math.radians(angle), 4, 'X')
                bpy.context.view_layer.update()
                current = surface(moving[0])
                for ob in fixed:
                    result = contact(current, stationary[ob.name], name)
                    allowed += result['bearing_samples']
                    bearing_depth = max(bearing_depth, result['bearing_depth_m'])
                    if result['depth_m'] > maximum:
                        maximum = result['depth_m']
                        worst = dict(angle=angle, fixed=ob.name, point_m=result['point_m'])
            pivot.matrix_basis = rest
            bpy.context.view_layer.update()
            motions.append(dict(node=name, samples=len(values), range=[min(values), max(values)],
                max_penetration_m=maximum, worst=worst, bearing_samples=allowed,
                max_intended_bearing_depth_m=bearing_depth, passed=maximum <= TOLERANCE))
            print('CART MOTION', level, name, maximum, allowed, flush=True)
        rows.append(dict(level=level, path=str(path.relative_to(ROOT)), sha256=digest(path),
            motions=motions, passed=all(m['passed'] for m in motions)))
    assert Document(source).dependencies() == baseline
    result = dict(passed=all(r['passed'] for r in rows), levels=rows,
        tolerance_m=TOLERANCE, config_sha256=digest(Path(args.config)),
        scope='Original full sampled sweep; reduced levels at rest only; finite source bearing volumes')
    dest = family/'build'/('lod-'+cfg['readme_key']+'-motion.json')
    dest.write_text(json.dumps(result, indent=2)+'\n')
    assert result['passed'], str(dest)


if __name__ == '__main__':
    main()
