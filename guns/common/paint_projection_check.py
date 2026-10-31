"""Check the accepted enamel partition and non-enamel shipping texels.

The member-owned baseline records the accepted round-two projection control:
73 non-enamel named regions per gun, eroded one shipping texel from UV edges.
This checks the actual delivered pixels, not source shader constants. It does
not replace the causal enamel-perturbation experiment recorded in REVIEW.md.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import bpy
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def measure(base):
    baseline = json.loads((base / 'src/accepted_projection.json').read_text())
    projection = json.loads((base / 'build/baked/4k/paint-projection.json').read_text())
    assert projection['aliases'] == baseline['enamel_aliases'], 'Enamel projection owners changed'
    bpy.ops.wm.open_mainfile(filepath=str(base / 'build/delivery/finalized.blend'))
    image = np.asarray(Image.open(base / 'textures' / baseline['image']).convert('RGBA'))
    assert image.shape == (2048, 2048, 4)
    rows = {}
    for ob in bpy.context.scene.objects:
        if ob.type != 'MESH' or not ob.get('asset_set') or ob.get('bake_only'):
            continue
        if ob.name in projection['aliases']:
            continue
        mask = Image.new('L', (2048, 2048))
        draw = ImageDraw.Draw(mask)
        mesh = ob.data
        mesh.calc_loop_triangles()
        uv = mesh.uv_layers.active
        for tri in mesh.loop_triangles:
            draw.polygon([(uv.data[i].uv.x * 2048, (1 - uv.data[i].uv.y) * 2048)
                          for i in tri.loops], fill=255)
        interior = np.asarray(mask.filter(ImageFilter.MinFilter(3))) > 0
        if not interior.any():
            continue
        rows[ob.name] = dict(interior_texels=int(interior.sum()),
                            mask_sha256=hashlib.sha256(interior.tobytes()).hexdigest(),
                            rgba_sha256=hashlib.sha256(image[interior].tobytes()).hexdigest())
    assert rows == baseline['regions'], 'Non-enamel UV masks or delivered BaseColor/specular pixels changed'
    report = dict(passed=True, non_enamel_regions=len(rows), exact=True,
                  scope=__doc__, regions=rows)
    (base / 'build/delivery/paint-projection-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PROJECTION: exact enamel partition and', len(rows), 'non-enamel shipping regions')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--asset', type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    measure(args.asset.resolve())
