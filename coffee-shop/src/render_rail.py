"""A reproducible close-up of the strip patio's actual chair-contact rail.

The older ground-facing wear camera looks between the coating-loss groups.
This view stands farther back, showing contact chips and paving together.
"""
import argparse,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ap=argparse.ArgumentParser();ap.add_argument('--width',type=int,default=1280);ap.add_argument('--samples',type=int,default=40);ap.add_argument('--lock-held',action='store_true',help='Called inside the serial render batch GPU lock');a=ap.parse_args()
if a.lock_held:assert os.environ.get('ASSETS_GPU_HELD')=='1','The kit GPU lock must own this render batch'
p=json.loads(Path('build/shops/228.json').read_text());t=p['tables'][0];z=p['grade']
recipe=dict(location=[t['x'],-7.25,1.43+z],target=[t['x'],t['y'],.30+z],lens=46,aspect=a.width/round(a.width*2/3),exposure=.15)
job=dict(rail=dict(seed=228,shot=recipe,sun_elevation=16,sun_azimuth=-145))
path=Path('build/rail-camera.json');path.write_text(json.dumps(job,indent=2)+'\n')
command=['blender','-b','-t','1','--factory-startup','--python-exit-code','1','--python','src/render.py','--','--matches',str(path),'--out','renders/final/228','--width',str(a.width),'--samples',str(a.samples)]
subprocess.run(command if a.lock_held else [str(ROOT/'kit/with_gpu.sh')]+command,check=True)
path=Path('renders/final/228/rail.json');meta=json.loads(path.read_text())
# Keep lighting and image aspect in their standard metadata fields. The camera
# recipe agrees with the ordinary detail views, with implicit zero roll.
for key in ('aspect','exposure','roll'):meta['recipe'].pop(key,None)
meta['detail_scope']='Actual chair-contact coating losses on the strip front rail and localized paving use'
path.write_text(json.dumps(meta,indent=2)+'\n')
