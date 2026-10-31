"""Optional native-docs grain crops against a local accepted snapshot.

The snapshot is review input only, never a rebuild or texture dependency.
Crop coordinates are identical before/after in the unchanged details layout.
"""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parents[1]
CROPS = {'butt': (824, 235, 1290, 574), 'wrist': (1008, 790, 1475, 1176)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--before', type=Path, required=True)
    p.add_argument('--out', type=Path, default=BASE / 'renders/grain/comparison')
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    images = [Image.open(root / 'docs/details.jpg').convert('RGB')
              for root in (a.before, BASE)]
    assert images[0].size == images[1].size == (1600, 1200)
    paths = {}
    for name, box in CROPS.items():
        tiles = [im.crop(box) for im in images]
        for label, tile in zip(('before', 'after'), tiles):
            tile.save(a.out / f'{name}-{label}.jpg', quality=98, optimize=True)
        pair = Image.new('RGB', (tiles[0].width * 2, tiles[0].height))
        for i, tile in enumerate(tiles):
            pair.paste(tile, (i * tile.width, 0))
        path = a.out / f'{name}-before-after.jpg'
        pair.save(path, quality=98, optimize=True)
        paths[name] = dict(box=box, before_left_after_right=str(path.relative_to(BASE)))
    old = json.loads((a.before / 'renders/final/look-review/values.json').read_text())['finishes']
    new = json.loads((BASE / 'renders/final/look-review/values.json').read_text())['finishes']
    digest = hashlib.sha256((BASE / 'export/sxs.glb').read_bytes()).hexdigest()
    values = {}
    for name in ('walnut_stock', 'walnut_forend'):
        assert new[name]['model_sha256'] == digest and new[name]['passed'], name
        values[name] = dict(before=old[name]['ours'], after=new[name]['ours'],
                            photo=new[name]['photo'], passed=new[name]['passed'],
                            relative_errors=new[name]['relative_errors'],
                            highlight_rgb_relative_errors=new[name]['highlight_rgb_relative_errors'])
    (a.out / 'values.json').write_text(json.dumps(dict(
        export_sha256=digest, crops=paths, finishes=values), indent=2) + '\n')
    print('Native details crops and whole-part walnut gates:', a.out)


if __name__ == '__main__':
    main()
