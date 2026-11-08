"""Current export provenance, requested view coverage, traffic and hero range."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image


def check(folder):
    from inspection import mirror
    rows=json.loads((folder/'provenance.json').read_text());seen={(r['stem'],r['shot']) for r in rows};results=[];packages={}
    expected=[*(('Park-'+str(s),v) for s in (101,202) for v in ('hero','above','entrance','row')),
              *((s,v) for s in ('SingleWide-120','DoubleWide-228') for v in ('hero','front','side','back','top','skirt','entry','scale')),
              *((s,'detail') for s in ('Deck','Carport','UtilityService','EntranceSign','Modules','HomeForms','SupportFrame')),
              ('SupportFrame','piers'),('Park-202','eevee'),('Park-101','single-2009'),('Park-101','street-2007'),
              ('Park-101','aerial-2015'),('Park-202','newer-row-2024')]
    assert set(expected)<=seen,('Missing final views',set(expected)-seen)
    for row in rows:
        source=Path(row['source']);assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256']
        delivery=Path(row['delivery']);meta=json.loads(delivery.with_suffix('.json').read_text())
        if str(delivery) not in packages:packages[str(delivery)]=hashlib.sha256(mirror(delivery).read_bytes()).hexdigest()
        assert packages[str(delivery)]==row['sha256'],('Changed game geometry after render',row['stem'])
        assert meta['images']==row['images'],('Stale render metadata',row['stem'],row['shot'])
        for im in row['images']:assert hashlib.sha256((delivery.parent/im['uri']).read_bytes()).hexdigest()==im['sha256']
        p=folder/row['stem']/(row['shot']+'.png')
        if not p.exists():p=folder/'matches'/row['stem']/(row['shot']+'.png')
        assert p.is_file();image=Image.open(p);assert image.width>=800
        results.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source_sha256=row['sha256']))
        if row['stem'].startswith('Park') and row['shot']=='hero':
            cp=row['camera_parameters'];assert 35<=cp['lens']<=50 and abs(row['camera']['location'][2]-1.68)<1e-6
            assert abs(row['light']['sun_elevation_degrees']-18)<.01
            rgb=np.asarray(image.convert('RGB'),float)/255;value=rgb.max(2);assert (value>.985).mean()<.01
            fleet=row['context']['fleet'];colors=[r['color'] for r in fleet if 'lot' in r]
            assert len(set(colors))>=6 and sum(c in ('Porcelain','Aluminum') for c in colors)/len(colors)<.55
            results[-1].update(near_clip_fraction=float((value>.985).mean()),p5_p95=np.percentile(value,[5,95]).tolist(),fleet_colors={c:colors.count(c) for c in sorted(set(colors))})
        if row.get('landmark_visibility'):
            v=row['landmark_visibility'];assert v['clear_count']==v['anchor_count']
    cams=json.loads(Path('build/cameras.json').read_text());assert all(c['residual_rms_pixels']<=20 for c in cams.values())
    assert abs(cams['street-2007']['shot']['roll'])<1e-9, 'Older street camera must remain level'
    report=dict(passed=True,views=len(rows),frames=results,scope='Current GLB/images, camera/lens/light, traffic metadata and display range; photographic judgment remains manual in REVIEW.md')
    Path('build/final-provenance.json').write_text(json.dumps(report,indent=2));print('FINAL PRESENTATION PASS',len(rows),'views')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,default=Path('renders/final'));a=p.parse_args();check(a.renders)
