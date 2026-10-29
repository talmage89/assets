"""Check imported geometric solids across duplicated glTF attribute seams."""
import json
import sys
from pathlib import Path
import bmesh
import bpy

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from kit import weapon_verify


def inspect():
    rows = {}
    for ob in bpy.context.scene.objects:
        if ob.type != 'MESH' or 'bone' not in ob:
            continue
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        before = len(bm.verts)
        raw_edges = sum(not edge.is_manifold for edge in bm.edges)
        # Check-only welding; the delivered normals and mesh stay untouched.
        bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-8)
        bad = sum(not edge.is_manifold for edge in bm.edges)
        rows[ob.name] = dict(raw_attribute_vertices=before,
                            geometric_vertices=len(bm.verts),
                            raw_attribute_seam_edges=raw_edges,
                            nonmanifold_geometric_edges=bad)
        bm.free()
    assert rows and all(row['nonmanifold_geometric_edges'] == 0 for row in rows.values()), rows
    return dict(passed=True, check_only_weld_tolerance_m=1e-8, parts=rows)


if __name__ == '__main__':
    weapon_verify.import_glb(Path('build/lever.glb').resolve())
    result = inspect()
    Path('build/topology.json').write_text(json.dumps(result, indent=2))
    print('IMPORTED TOPOLOGY:', len(result['parts']), 'closed geometric solids')
