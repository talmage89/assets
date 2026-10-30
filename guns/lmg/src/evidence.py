"""Audit presentation provenance, playback durations and inspection tonal range."""
import hashlib, json, sys
from pathlib import Path
import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))
from interface import CLIPS

out = BASE / 'renders/checkpoint'
hashes = {p.resolve(): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in (BASE / 'build').glob('*.glb')}
groups = {'main': out / 'shots.json', 'photo_pairs': out / 'photos/shots.json',
          'belt_advance': out / 'belt-advance/shots.json'}
groups.update({f'detachable_{n}': out / f'detachables/{n}/shots.json'
               for n in ('box_loaded', 'box_empty', 'cartridge', 'case', 'link')})
groups.update({f'clip_{n}': out / f'strips/{n}/shots.json' for n in CLIPS})
counts = {}
for group, path in groups.items():
    records = json.loads(path.read_text())
    for name, record in records.items():
        source = Path(record['source']).resolve()
        assert record['sha256'] == hashes[source], (group, name, 'stale GLB')
        assert (path.parent / (name + '.png')).exists(), (group, name, 'missing image')
    counts[group] = len(records)
assert counts['main'] == 22 and counts['photo_pairs'] == 10 and counts['belt_advance'] == 7
timing = json.loads((out / 'strips/timing.json').read_text())
assert set(timing) == set(CLIPS)
for name, record in timing.items():
    assert record['encoded_duration_ms'] == record['duration_ms']
    assert record['duration_ms'] == round(CLIPS[name]['frames'] / 60 * 1000)

rgb = np.asarray(Image.open(out / 'hero.png').convert('RGB'))
neutral = rgb[0, 0].astype(float)
foreground = rgb[np.max(abs(rgb.astype(float) - neutral), axis=2) > 8]
luma = foreground @ np.array((.2126, .7152, .0722))
result = dict(passed=True, image_counts=counts, clips_with_verified_duration=len(timing),
    hero_display_luma_p01_p50_p99=np.percentile(luma, (1, 50, 99)).tolist(),
    hero_foreground_any_channel_255_fraction=float(np.mean(np.max(foreground, axis=1) == 255)),
    tone_scope='Approximate foreground from deviation from gray backdrop. Display RGB only; quick constants, no albedo or wear acceptance.')
(BASE / 'build/presentation.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
