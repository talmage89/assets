"""Look-dev review evidence from the exported GLBs; no final docs images."""
import json,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import numpy as np
from PIL import Image
from kit.contact import contact,review_sheet
out=Path('renders/lookdev');states=('new','season','beat');shots=('hero','hero_bottom','tail_plies','truck','truck_inner','wheel_bearing','grip_edge','grip_macro')
values={};budgets={}
for state in states:
    digest=hashlib.sha256(Path(f'export/{state}.glb').read_bytes()).hexdigest()
    meta=json.loads((out/state/'shots.json').read_text())
    assert all(meta[k]['sha256']==digest for k in shots),'Stale '+state+' render'
    contact([out/state/(k+'.png') for k in shots],out/state/'contact.jpg',width=2400,title=state+' / baked GLB / Cycles')
    for k in ('hero','hero_bottom'):
        p=np.asarray(Image.open(out/state/(k+'.png')).convert('RGB'),dtype=float);v=p@np.array([.2126,.7152,.0722])
        values[state+'/'+k]=dict(luma_percentiles=dict(zip(('p1','p5','p50','p95','p99'),np.percentile(v,[1,5,50,95,99]).tolist())),clipped_all_channels_fraction=float(np.all(p>=250,axis=2).mean()),scope='Display-referred full frame, concrete included; not recovered albedo')
    model=json.loads(Path(f'build/{state}/model.json').read_text());export=json.loads(Path(f'build/{state}/export.json').read_text());uv=json.loads(Path(f'build/{state}/uv.json').read_text());bake=json.loads(Path(f'build/{state}/bake/bake-report.json').read_text())
    budgets[state]=dict(parts=model['parts'],triangles=model['triangles'],glb_bytes=Path(f'export/{state}.glb').stat().st_size,materials=export['materials'],uv={k:uv[k] for k in ('coverage','overlap_fraction','outside_triangles','degenerate_uv_triangles','density_px_m')},textures=json.loads(Path(f'textures/{state}/texture-report.json').read_text()),bake={k:bake[k] for k in ('size','samples','device','BaseColor','Normal')},sha256=digest)
review_sheet([[out/s/(k+'.png') for s in states] for k in ('hero','hero_bottom','tail_plies','truck_inner','wheel_bearing','grip_macro')],out/'contact.jpg',width=3600,title='New / season / beat — exported baked GLBs, Cycles, procedural raking sun')
pairs=sorted((out/'pairs').glob('*-pair.jpg'))
review_sheet([[p] for p in pairs],out/'matched-pairs.jpg',width=2200,title='Neutral-balanced photographs / matched framing and estimated illumination')
# A true crop of the constrained full-board pair, preserving its fitted camera.
# The renderer has the exact 3072 px horizontal span of the source crop.
if (out/'pairs/period_used.png').exists():
    render=Image.open(out/'pairs/period_used.png');photo=Image.open('renders/reference-neutral/period_used.jpg')
    assert render.width==3072
    render.crop((1450,160,2590,1240)).save(out/'pairs/fullsize-wheel-render.png')
    photo.crop((1450,480,2590,1560)).save(out/'pairs/fullsize-wheel-photo.png')
    review_sheet([[out/'pairs/fullsize-wheel-render.png',out/'pairs/fullsize-wheel-photo.png']],out/'pairs/fullsize-wheel-pair.jpg',width=2280,title='Full-size used truck/wheel / exact crops of the full-board calibration / render left')
art=Image.open('build/art/graphics-sheet.png');art.thumbnail((1536,2048));art.save(out/'graphics-sheet.jpg',quality=95)
(out/'values.json').write_text(json.dumps(values,indent=2));(out/'budgets.json').write_text(json.dumps(budgets,indent=2))
print(json.dumps({'values':values,'budgets':{k:{q:v[q] for q in ('triangles','glb_bytes','materials')} for k,v in budgets.items()}},indent=2))
