"""Review freshness and source-only provenance, separate from visual acceptance."""
import hashlib
import json
from pathlib import Path
from delivery_io import bundle_hash


def check():
    root=Path('renders/cape/checkpoint');rows=[]
    paths=[root/'provenance.json',root/'comparison/provenance.json']+[root/'seeds'/str(s)/'provenance.json' for s in range(31,37)]+[Path('renders/cape/matches/provenance.json')]
    for path in paths:
        data=json.loads(path.read_text())
        for name,row in data.items():
            source=Path(row['source']);assert source.suffix=='.blend' and row['engine']=='CYCLES'
            assert hashlib.sha256(source.read_bytes()).hexdigest()==row['source_sha256'],(path,name,'stale source')
            for image,digest in row['material_sha256'].items():assert hashlib.sha256(Path(image).read_bytes()).hexdigest()==digest,(path,name,image)
            for context in row.get('context',[]):
                p=Path(context['path']);digest=bundle_hash(p) if p.suffix=='.gltf' else hashlib.sha256(p.read_bytes()).hexdigest()
                assert digest==context['sha256']
            assert (path.parent/(name+'.png')).is_file();rows.append(dict(view=name,seed=row['seed'],image=str(path.parent/(name+'.png'))))
    assert len(rows)==22,len(rows)
    tonal=json.loads((root/'tonal.json').read_text());assert tonal['clipped_white_fraction']==0
    result=dict(passed=True,views=rows,tonal=tonal,scope='Source/map/context freshness and Cycles provenance only; images require visual photographic critique, no baked delivery claim')
    Path('build/cape/view-check.json').write_text(json.dumps(result,indent=2));print('CAPE_VIEWS',len(rows),'current Cycles views; no white clipping')
    return result

if __name__=='__main__':check()
