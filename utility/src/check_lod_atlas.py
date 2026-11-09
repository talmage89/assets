"""Retain the family's guarded stock charts and actual marking supports."""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT), str(HERE)]
from atlas import RECTS, rect
from kit.lod import configuration
from kit.lod_io import Document, digest

parser = argparse.ArgumentParser()
parser.add_argument('--config', required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
cfg, family, source, output = configuration(Path(args.config))
manifest = json.loads((output/'manifest.json').read_text())
assert Document(source).dependencies() == manifest['baseline']
paths = [source] + [output/row['path'] for row in manifest['levels'][1:]]
rows = []
for path in paths:
    doc = Document(path)
    if path == source:
        doc.select(cfg.get('include_nodes'))
    crossed = 0
    checked = 0
    contacts = []
    examples = []
    for mesh in doc.data['meshes']:
        chart_geometry = {}
        for primitive in mesh['primitives']:
            mat = doc.data['materials'][primitive.get('material', 0)]
            if mat['name'] != 'Utility':
                continue
            attrs, faces = doc.arrays(primitive)
            uv = attrs['TEXCOORD_0'].copy()
            uv[:,1] = 1-uv[:,1]
            triangles = uv[faces]
            xyz = attrs['POSITION'][faces]
            low, high = triangles.min(axis=1), triangles.max(axis=1)
            classified = np.zeros(len(faces), bool)
            for role in RECTS:
                a,b,c,d = rect(role)
                selected = ((low[:,0]>=a-1e-6)&(low[:,1]>=b-1e-6)&
                            (high[:,0]<=c+1e-6)&(high[:,1]<=d+1e-6))
                assert not np.any(classified&selected)
                classified |= selected
                chart_geometry.setdefault(role, []).extend(xyz[selected].tolist())
            checked += len(faces)
            crossed += int((~classified).sum())
            examples.extend(triangles[~classified][:3].tolist())
        for marking, supports in (('Brand',('PoleA','PoleB')),('Rating',('Tank',))):
            marks = chart_geometry.get(marking, [])
            if not marks:
                continue
            target = [t for role in supports for t in chart_geometry.get(role, [])]
            assert target, (mesh.get('name'), marking, 'missing support')
            vertices = [p for triangle in target for p in triangle]
            faces = [(3*i,3*i+1,3*i+2) for i in range(len(target))]
            tree = BVHTree.FromPolygons(vertices, faces, all_triangles=True)
            gaps = []
            for triangle in marks:
                points = [Vector(p) for p in triangle]
                points.append(sum(points,Vector())/3)
                gaps.extend(tree.find_nearest(p)[3] for p in points)
            contacts.append(dict(marking=marking, samples=len(gaps),
                min_gap_m=min(gaps), max_gap_m=max(gaps),
                passed=min(gaps)>1e-5 and max(gaps)<.001))
    rows.append(dict(file=str(path.relative_to(ROOT)), sha256=digest(path),
        checked_triangles=checked, crossed_chart_triangles=crossed,
        examples=examples[:3], marking_supports=contacts,
        passed=crossed==0 and all(c['passed'] for c in contacts)))
report = dict(passed=all(row['passed'] for row in rows), levels=rows,
    scope='Same guarded-chart and measured marking-gap limits as original delivery')
dest = family/'build'/('lod-'+cfg.get('readme_key','default')+'-atlas.json')
dest.write_text(json.dumps(report,indent=2)+'\n')
print('LOD ATLAS',report['passed'],[(r['crossed_chart_triangles'],r['marking_supports']) for r in rows])
assert report['passed'], str(dest)
