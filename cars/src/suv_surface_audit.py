"""Inspect optical/paint normal continuity without changing the measured mesh.

Corner discontinuities are measured only within one manufactured face role;
an intentional gauge edge is not a smooth-surface defect. Reports are evidence,
not a substitute for same-camera softbox images.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
from collections import defaultdict
import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(Path(__file__).resolve().parent)]


def inspect(ob):
    me = ob.data
    role = me.attributes.get('skin_face_role')
    groups = defaultdict(list)
    for f in me.polygons:
        r = role.data[f.index].value if role else 0
        if role is None and not f.use_smooth:continue
        for li in f.loop_indices:
            groups[(me.loops[li].vertex_index, r)].append(me.corner_normals[li].vector.copy())
    turns = []
    worst = []
    for (vi, r), ns in groups.items():
        if r != 0 or len(ns) < 2:
            continue
        angle = max(math.degrees(a.angle(c, 0)) for a in ns for c in ns)
        turns.append(angle)
        if angle > 2:
            worst.append(dict(point_m=list(ob.matrix_world @ me.vertices[vi].co), turn_degrees=angle))
    return dict(triangles=sum(len(f.vertices)-2 for f in me.polygons),
                custom_normals=me.has_custom_normals,
                explicit_manufacturing_roles=role is not None,
                within_role_corner_turn_p50_p95_max=np.percentile(turns,[50,95,100]).tolist() if turns else [],
                discontinuities=sorted(worst,key=lambda r:-r['turn_degrees'])[:30])


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source)
    bpy.ops.wm.open_mainfile(filepath=str(src.resolve()))
    report={o.name:inspect(o) for o in bpy.context.scene.objects if o.type=='MESH' and
            (o.get('part_category') in ['body','fascia','glass','pillars','cladding','spoiler'] or
             o.name.startswith(('Headlamp','Taillamp','Projector','Grille','Upper grille','Lower intake')))}
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps(dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),parts=report),indent=2))
    print('SURFACE_NORMAL_AUDIT',json.dumps({k:r['within_role_corner_turn_p50_p95_max'] for k,r in report.items() if r['discontinuities']}))


if __name__=='__main__':main()
