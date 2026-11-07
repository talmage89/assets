"""Final sheets and measured budgets, strictly from hash-checked GLB renders."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet
OUT=Path('renders/final');STATES=('new','season','beat')
SHOTS=('hero','hero_bottom','tail_plies','truck','truck_inner','wheel_bearing','grip_edge','grip_macro')
values={};budgets={};provenance={}
for state in STATES:
    digest=hashlib.sha256(Path(f'export/{state}.glb').read_bytes()).hexdigest()
    meta=json.loads((OUT/state/'shots.json').read_text())
    names=SHOTS+('top','bottom','side','front','scale') if state=='season' else SHOTS+('wheel_profile',) if state=='beat' else SHOTS
    for name in names:
        assert meta[name]['sha256']==digest and meta[name]['stage']=='exported GLB / baked atlas',(state,name,'stale/nonexport')
        assert meta[name]['engine']=='CYCLES'
        provenance[f'{state}/{name}']={k:meta[name][k] for k in ('sha256','stage','engine','samples')}
    contact([OUT/state/(k+'.png') for k in names],OUT/state/'contact.jpg',width=2400,title=state+' / baked exported GLB / Cycles')
    for name in ('hero','hero_bottom'):
        pixels=np.asarray(Image.open(OUT/state/(name+'.png')).convert('RGB'),dtype=float);v=pixels@np.array([.2126,.7152,.0722])
        values[state+'/'+name]=dict(luma_percentiles=dict(zip(('p1','p5','p50','p95','p99'),np.percentile(v,[1,5,50,95,99]).tolist())),white_clipped_pixels=int(np.all(pixels==255,axis=2).sum()),scope='Display-referred full frame including concrete, not recovered albedo')
    model=json.loads(Path(f'build/{state}/model.json').read_text());export=json.loads(Path(f'build/{state}/export.json').read_text());uv=json.loads(Path(f'build/{state}/uv.json').read_text());bake=json.loads(Path(f'build/{state}/bake/bake-report.json').read_text())
    textures=json.loads(Path(f'textures/{state}/texture-report.json').read_text())
    budgets[state]=dict(triangles=model['triangles'],parts=model['parts'],glb_bytes=Path(f'export/{state}.glb').stat().st_size,materials=export['materials'],uv={k:uv[k] for k in ('coverage','overlap_fraction','outside_triangles','degenerate_uv_triangles','density_px_m')},textures=textures,texture_file_bytes={p.name:p.stat().st_size for p in Path(f'textures/{state}').glob('*.png')},estimated_compressed_mipped_texture_mib=sum(row['size'][0]*row['size'][1]*4/3 for row in textures.values())/1024**2,bake={k:bake[k] for k in ('size','samples','device','BaseColor','Normal')},sha256=digest)
    assert model['triangles']==(13928 if state=='beat' else 13888)
eev=json.loads((OUT/'eevee/shots.json').read_text())['hero'];assert eev['sha256']==budgets['season']['sha256'] and eev['engine']=='BLENDER_EEVEE'
provenance['eevee/hero']={k:eev[k] for k in ('sha256','stage','engine','samples')}
contact([OUT/'season'/(k+'.png') for k in ('top','bottom','side','front')],OUT/'turnaround.jpg',width=2400,title='Top / bottom / side / front — season, baked exported GLB')
rows=[[OUT/s/(k+'.png') for s in STATES] for k in SHOTS]
rows += [[OUT/'beat/wheel_profile.png'],[OUT/'season'/(k+'.png') for k in ('top','bottom')],[OUT/'season'/(k+'.png') for k in ('side','front')],[OUT/'season/scale.png',OUT/'eevee/hero.png']]
review_sheet(rows,OUT/'contact.jpg',width=3600,title='New / season / beat — all final Cycles and Eevee views from baked exported GLBs')
pairs=[OUT/'pairs'/(name+'-pair.jpg') for name in ('period_horizontal','period_truck','period_used')]
meta=json.loads((OUT/'pairs/shots.json').read_text());assert all(q['sha256']==budgets['season']['sha256'] for q in meta.values())
review_sheet([[p] for p in pairs],OUT/'matched-pairs.jpg',width=2400,title='Neutral-balanced photos / same cameras and matched illumination estimates')
render=Image.open(OUT/'pairs/period_used.png');photo=Image.open('renders/reference-neutral/period_used.jpg')
assert render.width==3072
render.crop((1450,160,2590,1240)).save(OUT/'pairs/fullsize-wheel-render.png')
photo.crop((1450,480,2590,1560)).save(OUT/'pairs/fullsize-wheel-photo.png')
review_sheet([[OUT/'pairs/fullsize-wheel-render.png',OUT/'pairs/fullsize-wheel-photo.png']],OUT/'pairs/fullsize-wheel-pair.jpg',width=2336,title='Used wheel/truck / exact native crops of the full-board calibrated camera / render left')
art=Image.open('build/art/graphics-sheet.png');art.thumbnail((1536,2048));art.save(OUT/'graphics-sheet.jpg',quality=95)
for name,data in [('values',values),('budgets',budgets),('provenance',provenance)]:
    (OUT/(name+'.json')).write_text(json.dumps(data,indent=2))
print(json.dumps({s:{k:v[k] for k in ('triangles','glb_bytes','materials','estimated_compressed_mipped_texture_mib')} for s,v in budgets.items()},indent=2))
