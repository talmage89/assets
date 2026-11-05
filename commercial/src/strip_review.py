"""Checkpoint sheets and strict current-export/context/image provenance."""
import hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
from kit.contact import review_sheet
from strip_plan import PROOF_SEEDS


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def recipe():
    files=[HERE/n for n in ('strip_render.py','strip_presentation.py','render.py','presentation.py','paving.py','strip_photo_matches.py')]
    files += [REPO/'houses/src/render.py',REPO/'cars/src/delivery_materials.py']
    return hashlib.sha256(b''.join(p.read_bytes() for p in files)).hexdigest()


def dependency(row):
    for f in row['files']:assert sha(REPO/f['source'])==f['sha256'],('Changed presentation dependency',f['source'])


def main():
    folder=Path('renders/strip/checkpoint');pairs=Path('renders/strip/matches');eevee=Path('renders/strip/eevee');records=[]
    expected={folder:('hero','storefront','walk','tower','endcap','pylon','rear','services','stalls','dusk','scale'),pairs:('commerce','sterling','sunnyvale','period_walk','period_lot','used_rear'),eevee:('hero',)}
    expected.update({folder/'seeds'/str(s):('above','street') for s in PROOF_SEEDS})
    for path,names in expected.items():
        provenance=json.loads((path/'provenance.json').read_text())
        for name in names:
            row=provenance[name];image=path/(name+'.png');assert sha(image)==row['image_sha256'],image
            assert sha(row['source'])==row['sha256'],('Stale export image',image)
            assert row['recipe_sha256']==recipe(),('Stale render recipe',image)
            assert row['ground']['sha256']==sha('../ground/export/Ground.glb')
            assert row['ground'].get('strip_context'),'Incomplete neighborhood presentation'
            for dep in row['ground'].get('neighbor_dependencies',[]):dependency(dep)
            for car in row.get('context',[]):
                if 'bundle' in car:dependency(car['bundle'])
            if row.get('comparison'):
                assert row['comparison']['calibration_sha256']==sha('build/strip/cameras.json')
                cal=json.loads(Path('build/strip/cameras.json').read_text())[name]
                assert row['comparison']['balanced_photo_sha256']==sha(cal['photo'])
                assert row['comparison'].get('lighting_recipe_sha256')==sha(HERE/'strip_matches.py'),('Stale calibrated illumination',image)
            if row.get('eye'):assert abs(row['eye']['height_m']-1.6)<1e-5
            records.append(dict(image=str(image),image_sha256=sha(image),source=row['source'],source_sha256=row['sha256']))
    family=[folder/'seeds'/str(s)/(name+'.png') for s in PROOF_SEEDS for name in ('above','street')]
    details=[folder/(name+'.png') for name in ('storefront','walk','tower','endcap','pylon','rear','services','stalls')]
    review_sheet([family[i:i+2] for i in range(0,len(family),2)],folder/'family.jpg',width=1600,title='Strip centers / four distinct occupied sites')
    review_sheet([details[i:i+2] for i in range(0,len(details),2)],folder/'details.jpg',width=1600,title='Strip centers / exported construction and maintained age')
    pair_rows=[[pairs/(name+'-pair.jpg')] for name in expected[pairs]]
    review_sheet(pair_rows,pairs/'pairs.jpg',width=1800,title='Estimated matched sunlight / stated neutrals and held-out construction differences')
    rows=[[folder/'hero.png'],*[family[i:i+2] for i in range(0,len(family),2)],*[details[i:i+2] for i in range(0,len(details),2)],[folder/'dusk.png',folder/'scale.png',eevee/'hero.png'],*pair_rows]
    fixes=Path('renders/strip/form-fixes');fix_images=sorted(fixes.glob('*-before-after.jpg'))
    assert len(fix_images)==6,'Six before/after form comparisons are required'
    comparison=json.loads((fixes/'comparison.json').read_text())
    for entry in comparison['rows']:
        assert sha(entry['source'])==entry['sha256'],('Stale form-fix source',entry)
        path=fixes/entry['label']/str(entry['seed'])
        provenance=json.loads((path/'provenance.json').read_text())
        for name in (('above','endcap','rear') if entry['seed']==201 else ('above',)):
            record=provenance[name]
            assert record['sha256']==entry['sha256'] and record['recipe_sha256']==recipe(),('Stale form-fix render',entry,name)
            assert sha(path/(name+'.png'))==record['image_sha256']
    rows += [fix_images[i:i+2] for i in range(0,len(fix_images),2)]
    review_sheet(rows,folder/'contact.jpg',width=2200,title='Strip look checkpoint / current GLBs, baked maps, context, matched pairs and form fixes')
    out=Path('build/strip-look/view-check.json');out.write_text(json.dumps(dict(passed=True,views=len(records),rows=records,scope='Current exported GLB, source recipe, map-containing context bundles, photographic calibration and actual image bytes; appearance acceptance is the separate native-size review in REVIEW.md.'),indent=2)+'\n')
    print('STRIP VIEW AUDIT',len(records),'current exported views; sheets ready')

if __name__=='__main__':main()
