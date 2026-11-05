"""Form review sheets and current-export provenance audit; no committed docs."""
import hashlib
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.contact import review_sheet


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    folder=Path('renders/strip/checkpoint');pairs=Path('renders/strip/matches');records=[];images=[]
    for path in [folder,*[folder/'seeds'/str(s) for s in (201,202,203,204)],pairs]:
        provenance=json.loads((path/'provenance.json').read_text())
        for name,row in provenance.items():
            image=path/(name+'.png');assert sha(image)==row['image_sha256'],image
            assert sha(row['source'])==row['sha256'],('Stale export image',image)
            assert row['recipe_sha256']==sha(HERE/'strip_render.py'),('Stale render recipe',image)
            assert row['ground']['sha256']==sha('../ground/export/Ground.glb')
            for context in row['context']:assert sha(context['path'])==context['sha256']
            records.append(dict(image=str(image),image_sha256=sha(image),source=row['source'],source_sha256=row['sha256']));images.append(image)
    family=[folder/'seeds'/str(s)/(name+'.png') for s in (201,202,203,204) for name in ('above','street')]
    details=[folder/(name+'.png') for name in ('storefront','walk','tower','pylon','rear','services')]
    review_sheet([family[i:i+2] for i in range(0,len(family),2)],folder/'family.jpg',width=1600,title='Strip center / four form seeds')
    review_sheet([details[i:i+2] for i in range(0,len(details),2)],folder/'details.jpg',width=1600,title='Strip center / construction details')
    review_sheet([[pairs/'commerce-pair.jpg'],[pairs/'sunnyvale-pair.jpg']],pairs/'pairs.jpg',width=1600,title='Strip center / sparse fitted comparisons')
    review_sheet([[folder/'hero.png'],* [family[i:i+2] for i in range(0,len(family),2)],*[details[i:i+2] for i in range(0,len(details),2)],[folder/'scale.png'],[pairs/'commerce-pair.jpg'],[pairs/'sunnyvale-pair.jpg']],folder/'contact.jpg',width=2000,title='Strip center / exported form checkpoint')
    out=Path('build/strip/view-check.json');out.write_text(json.dumps(dict(passed=True,views=len(records),rows=records,scope='Every checkpoint image hashes its current diagnostic GLB, renderer, native ground and optional scale context. No final surface/bake acceptance.'),indent=2)+'\n')
    print('STRIP VIEW AUDIT',len(records),'current exported views; sheets ready')


if __name__=='__main__':main()
