"""Compare independent clean-scene source builds, without claiming bake identity."""
import json
from pathlib import Path

folder = Path('build')
rows = []
for quality, name in [('game', 'game'), ('high', 'lookdev')]:
    original = json.loads((folder/(name+'-audit.json')).read_text())
    repeat = json.loads((folder/'repeat'/(name+'-audit.json')).read_text())
    assert original['passed'] and repeat['passed']
    a, b = original['sets']['TrashCart'], repeat['sets']['TrashCart']
    assert a['geometry_sha256'] == b['geometry_sha256'], quality
    assert original['pivots'] == repeat['pivots'], quality+' pivots'
    rows.append(dict(quality=quality, triangles=a['triangles'],
                     geometry_sha256=a['geometry_sha256']))
report = dict(passed=True, scope='Evaluated source geometry and pivot frames; no rebake',
              builds=rows)
(folder/'repeat'/'check.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
