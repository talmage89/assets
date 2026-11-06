"""Ignored contact sheet only: checkpoint images never enter docs/history."""
import argparse,sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.contact import review_sheet
p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,default=Path('renders/checkpoint'));a=p.parse_args()
names=['hero','lineup','signs-regulatory','signs-warning','sign-face','sign-back','post-base','pole-band','shelter-frame','bench','meter','boxes','collection','receptacles','rack']
paths=[a.folder/(n+'.png') for n in names]
matches=[Path('renders/match')/(n+'.png') for n in ('used-shelter','used-meter','used-news')]
for path in paths+matches:assert path.is_file(),path
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
checks=[]
for path in paths+matches:
    m=json.loads(path.with_suffix('.json').read_text());assert m['engine']=='CYCLES',path
    assert m['recipe_sha256']==sha(Path(__file__).with_name('render.py')),path
    assert m['image_sha256']==sha(path),path
    for bundle in m['inputs']:
        for file,h in bundle['files'].items():assert sha(Path('..')/file)==h,(path,file)
    if m.get('photo_calibration_sha256'):assert m['photo_calibration_sha256']==sha('build/photo-calibration.json'),path
    checks.append(str(path))
rows=[[p] for p in paths[:4]]+[paths[i:i+2] for i in range(4,len(paths),2)]
rows += [[p] for p in Path('renders/match').glob('*-pair.jpg')]
review_sheet(rows,a.folder/'contact.jpg',width=1800,title='Street furniture + 2009 signs / FORM checkpoint / exported quick materials')
Path('build/view-check.json').write_text(json.dumps(dict(passed=True,views=checks,scope='Current exported bundles, current render recipe, camera fit and actual Cycles image bytes; aesthetic review remains separate'),indent=2))
