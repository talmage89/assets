"""Audit the complete exported checkpoint, same-camera pairs and tonal range."""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def package(path):
    h=hashlib.sha256(path.read_bytes())
    if path.suffix=='.gltf':
        d=json.loads(path.read_text())
        for key in ('buffers','images'):
            for row in d.get(key,[]):h.update((path.parent/row['uri']).read_bytes())
    return h.hexdigest()


def main(require_before=True):
    recipe=sha(Path('src/render.py'));paths=[]
    shots='hero,above,doors,window,window_dusk,tower,wing,sign,scale,age,north_roof'.split(',')
    for seed in (101,202):paths += [Path(f'renders/checkpoint/{seed}/{s}.png') for s in shots]
    paths.append(Path('renders/checkpoint/range.png'))
    paths += [Path('renders/modules')/(p.stem+'.png') for p in Path('export/modules').glob('*.gltf')]
    paths += [Path(f'renders/{folder}/{name}.png') for folder in ('matches','source-matches') for name in ('gothic','modern','window')]
    paths += [Path(f'renders/eevee/{seed}/hero.png') for seed in (101,202)]
    receipts=[];hashes={}
    for p in paths:
        assert p.exists(),p
        data=json.loads(p.with_suffix('.json').read_text());source=Path(data['source'])
        assert data['sha256']==sha(source),(p,'stale geometry')
        if source not in hashes:hashes[source]=package(source)
        assert data['package_sha256']==hashes[source],(p,'stale texture package')
        assert data['render_recipe_sha256']==recipe,(p,'stale renderer')
        im=Image.open(p);assert im.size==tuple(data['resolution'])
        assert im.width>=(720 if 'modules' in p.parts else 800)
        samples=int(im.info.get('cycles.ViewLayer.samples',data.get('capture_samples',0)))
        assert samples>0,(p,'missing actual sample receipt')
        receipts.append(dict(path=str(p),source=str(source),package_sha256=hashes[source],size=im.size,samples=samples))
    tones={}
    for seed in (101,202):
        p=Path(f'renders/checkpoint/{seed}/hero.png');rgb=np.asarray(Image.open(p).convert('RGB')).astype(float)
        lum=rgb@np.array([.2126,.7152,.0722]);clipped=float(np.mean(np.any(rgb>=254,axis=2)))
        assert clipped<.001,(p,clipped)
        tones[str(seed)]=dict(display_luma_p1_p50_p99=np.percentile(lum,[1,50,99]).tolist(),clipped_pixel_fraction=clipped,scope='Display-domain frame statistics include sky; not physical surface albedos')
    differences={}
    for name in ('gothic','modern','window'):
        a=np.asarray(Image.open(f'renders/matches/{name}.png').convert('RGB')).astype(float)
        b=np.asarray(Image.open(f'renders/source-matches/{name}.png').convert('RGB')).astype(float)
        delta=np.abs(a-b);mean=float(delta.mean())
        assert mean<1.0,(name,mean)
        differences[name]=dict(mean_absolute_rgb_byte_delta=mean,p99=float(np.percentile(delta,99)))
    path=Path('renders/before-after/receipts.json')
    before=json.loads(path.read_text()) if path.exists() else []
    if require_before:assert len(before)==8,'The local revision review requires all eight before/after pairs'
    assert all(r['camera_equal'] and min(r['panel_widths'])>=800 for r in before)
    Path('build/presentation-check.json').write_text(json.dumps(dict(passed=True,images=receipts,tonal_range=tones,source_export_pairs=differences,before_after=before),indent=2))
    print('PASS',len(receipts),'current geometry/map/recipe receipts; source/export pairs, native before/after and hero tonal range')
    print(json.dumps(tones,indent=2))


if __name__=='__main__':main()
