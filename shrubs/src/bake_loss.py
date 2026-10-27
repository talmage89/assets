"""Measure matching source/export views and the actual delivered analytic regions."""
import sys,json,hashlib,io
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.gltf import GLB
from values import stats
raw=GLB(Path('export/Shrubs.glb'));glb_sha=hashlib.sha256(Path('export/Shrubs.glb').read_bytes()).hexdigest();rows={}
for species,source,final,scene,names in [
 ('Boxwood',Path('renders/boxwood-source-final'),Path('renders/final'),Path('build/boxwood/lookdev.blend'),('match_green_velvet','match_clipped')),
 ('Hydrangea',Path('renders/hydrangea-source-final'),Path('renders/hydrangea-final'),Path('build/hydrangea/lookdev.blend'),('hyd_match_house','hyd_match_bed'))]:
    sm=json.loads((source/'shots.json').read_text());fm=json.loads((final/'shots.json').read_text());source_sha=hashlib.sha256(scene.read_bytes()).hexdigest();rows[species]={}
    for name in names:
        assert sm[name]['source_sha256']==source_sha and fm[name]['source_sha256']==glb_sha
        a=Image.open(source/(name+'.png')).convert('RGBA');b=Image.open(final/(name+'.png')).convert('RGBA');assert a.size==b.size
        aa=np.asarray(a,float)/255;bb=np.asarray(b,float)/255;mask=(aa[:,:,3]>.9)&(bb[:,:,3]>.9)
        error=aa[:,:,:3][mask]-bb[:,:,:3][mask]
        row=dict(checked_pixels=int(mask.sum()),rgb_RMSE_display=float(np.sqrt(np.mean(error**2))),max_RGB_error_display=float(np.abs(error).max()),leaf_source=stats(a),leaf_export=stats(b))
        if species=='Hydrangea':row.update(flower_source=stats(a,'flower'),flower_export=stats(b,'flower'))
        rows[species][name]=row
textures={}
for i,entry in enumerate(raw.json['images']):
    name=entry['name'];channel=next(c for c in ('BaseColor','Normal','ORM') if c in name)
    delivered=np.asarray(Image.open(io.BytesIO(raw.image(i))));analytic=np.asarray(Image.open(Path('textures/analytic')/f'T_Shrubs_{channel}.png'))
    h,w=delivered.shape[:2];mask=np.ones((h,w),bool);mask[:h//2,:w//4]=False
    assert np.array_equal(delivered[mask],analytic[mask]),channel+' analytic foliage changed during delivery'
    textures[channel]=dict(compared_pixels=int(mask.sum()),maximum_byte_error=0)
report=dict(passed=True,glb_sha256=glb_sha,views=rows,analytic_tile_delivery=textures,scope='Actual source/export matched view differences and embedded analytic card fields; wood has real GPU projection/coverage checks, cards intentionally retain original analytic fields')
Path('build/bake-loss.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
