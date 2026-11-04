"""Current source evidence, fixed ROI tolerances and unchanged delivery maps."""
import hashlib,json,sys
from pathlib import Path


def recipe_sha(extra=()):
    here=Path(__file__).resolve().parent
    paths=[here/name for name in ('cape_render.py','cape_reflections.py','render.py','ranch_render.py')]+list(extra)
    return hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in paths)).hexdigest()


def check():
    from delivery_io import bundle_hash
    root=Path('renders/cape/lookdev/checkpoint');records=[]
    paths=[root/'provenance.json',root/'comparison/provenance.json',root/'painted_cedar/provenance.json',Path('renders/cape/matches/provenance.json')]+[root/'seeds'/str(s)/'provenance.json' for s in range(31,37)]
    for path in paths:
        for name,row in json.loads(path.read_text()).items():
            assert row['engine']=='CYCLES' and 'no bake' in row['stage']
            assert row['render_recipe_sha256']==recipe_sha(),(path,name,'stale render recipe')
            assert hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['source_sha256'],(path,name,'stale source')
            for image,digest in row['material_sha256'].items():assert hashlib.sha256(Path(image).read_bytes()).hexdigest()==digest,(path,name,'stale map')
            for context in row.get('context',[]):
                p=Path(context['path']);digest=bundle_hash(p) if p.suffix=='.gltf' else hashlib.sha256(p.read_bytes()).hexdigest()
                assert digest==context['sha256'],(path,name,'stale neighboring export')
            assert (path.parent/(name+'.png')).exists();records.append(dict(view=name,seed=row['seed'],path=str(path.parent/(name+'.png'))))
    assert len(records)==36,len(records)
    folder=Path('renders/cape/lookdev/values');values=json.loads((folder/'values.json').read_text());assert values['passed'],{k:v['passed'] for k,v in values['rows'].items()}
    references=json.loads(Path('build/cape/material-photos.json').read_text())
    for name,row in values['rows'].items():
        ref=row['reference'];assert ref==references[name],(name,'stale reference measurement')
        assert hashlib.sha256((Path('refs')/(ref['file']+'.jpg')).read_bytes()).hexdigest()==ref['original_sha256']
        s=row['render'];assert s['render_recipe_sha256']==recipe_sha((Path(__file__).resolve().parent/'cape_value_render.py',))
        assert hashlib.sha256(Path(s['source']).read_bytes()).hexdigest()==s['source_sha256']
    tonal=json.loads((root/'tonal.json').read_text());assert tonal['clipped_white_fraction']==0
    result=dict(passed=True,views=records,tonal=tonal,values=str(folder/'values.json'),scope='Source/map freshness, numerical display tolerances and Cycles evidence. Before bake; no final UV/export certification.')
    Path('build/cape/lookdev-check.json').write_text(json.dumps(result,indent=2));print('CAPE_LOOKDEV',len(records),'views; material median/tails/hue passed; no white clipping')


if __name__=='__main__':check()
