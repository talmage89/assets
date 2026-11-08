"""Freeze supplied checkpoint packages for identical-camera comparisons.

Historical outputs are local review inputs, not new shipping assets. Geometry
and image bytes must match the accepted checkpoint; only image URIs relocate.
"""
import hashlib,json,os,subprocess
from pathlib import Path


def freeze():
    source=Path('build/repeat-before');out=Path('build/baseline/export');out.mkdir(parents=True,exist_ok=True)
    receipts=[]
    for stem in ('Park-101','Park-202','SingleWide-120','DoubleWide-228','Deck','Carport'):
        p=source/(stem+'.gltf');meta=json.loads(p.with_suffix('.json').read_text());doc=json.loads(p.read_text())
        if stem.startswith('Park'):assert len(meta['plan']['lots']) in (10,12),'Historical cache was overwritten'
        images=[]
        for im,record in zip(doc['images'],meta['images']):
            candidates=[Path('export')/im['uri'],source/im['uri']]
            q=next((q for q in candidates if q.is_file() and hashlib.sha256(q.read_bytes()).hexdigest()==record['sha256']),None)
            assert q is not None,('Historical image unavailable',im['uri'])
            uri=os.path.relpath(q.resolve(),out.resolve());im['uri']=uri;images.append(dict(record,uri=uri))
        name='Baseline_'+stem;binary=p.parent/doc['buffers'][0]['uri'];doc['buffers'][0]['uri']=name+'.bin'
        (out/(name+'.bin')).write_bytes(binary.read_bytes());(out/(name+'.gltf')).write_text(json.dumps(doc,separators=(',',':')))
        meta['images']=images;(out/(name+'.json')).write_text(json.dumps(meta,indent=2))
        receipts.append(dict(stem=stem,original_gltf_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                             geometry_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),images=images))
    legacy=subprocess.check_output(['git','show','07d9d3f:trailer-park/src/render.py'])
    Path('build/baseline/legacy_render.py').write_bytes(legacy)
    Path('build/baseline/receipt.json').write_text(json.dumps(dict(commit='07d9d3f',packages=receipts,
        scope='Supplied accepted local checkpoint cache; unchanged geometry/image bytes, relocated image URIs'),indent=2))
    print('FROZEN BASELINE',len(receipts),'accepted packages')


if __name__=='__main__':freeze()
