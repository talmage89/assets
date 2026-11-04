"""Current exported look-checkpoint sheets and provenance, never docs JPGs."""
import hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from review import sheet
from context import recipe,bundle


def digest(path):
 path=Path(path);return bundle(path.resolve())['sha256'] if path.suffix=='.gltf' else hashlib.sha256(path.read_bytes()).hexdigest()


def main():
 root=Path('renders/look-checkpoint');names=('hero','above','dispenser','canopy','column','entry','sign','rear','services','asphalt','landscape','dusk')
 details=[(name,root/(name+'.png')) for name in names];family=[(f'{seed} / {view}',root/'seeds'/str(seed)/(view+'.png')) for seed in (101,102,103,104) for view in ('above','street')]
 sheet(details,root/'details.jpg',3,(800,560));sheet(family,root/'family.jpg',2,(960,620))
 pairs=[(n,Path('renders/look-matches')/(n+'-pair.jpg')) for n in ('period_canopy','period_dispenser','used_forecourt','used_store')]
 sheet(pairs,root/'matched-pairs.jpg',1,(1800,850))
 fixes=[(p.stem,p) for p in sorted(Path('renders/form-fixes').glob('*-before-after.jpg'))]
 assert len(fixes)==7
 sheet(fixes,root/'form-fixes.jpg',2,(900,510))
 values=[(p.stem,p) for p in sorted(Path('renders/look-matches').glob('*-values.jpg'))]
 sheet(values,root/'material-values.jpg',2,(900,500))
 sheet(details+family+pairs+fixes,root/'contact.jpg',3,(750,540))
 rows=[]
 for folder in (root,Path('renders/look-matches')):
  for p in folder.rglob('provenance.json'):
   for name,r in json.loads(p.read_text()).items():
    image=p.parent/(name+'.png');assert digest(image)==r['image_sha256'];assert digest(r['source'])==r['sha256'],('Stale export',image)
    assert r['source'].endswith('.gltf') and r['recipe_sha256']==recipe(),('Stale render recipe',image)
    assert r['engine']=='CYCLES'
    if r.get('ground'):
     source=HERE.parents[1]/r['ground']['source'];assert digest(source)==r['ground']['sha256']
     for ctx in r['ground'].get('neighbor_dependencies',[]):assert bundle(HERE.parents[1]/ctx['source'])==ctx
    rows.append(str(image))
 for name in names:assert (root/(name+'.png')).exists()
 physical=json.loads(Path('build/checks.json').read_text());delivery=json.loads(Path('build/delivery-check.json').read_text())
 assert all(r['passed'] for r in physical) and delivery['passed']
 result=dict(passed=True,views=rows,cycles_views=len(rows),new_gpu_mib=delivery['new_gpu_mib'],contact=str(root/'contact.jpg'),stage='Exported surface/age checkpoint; no portfolio docs accepted yet',scope='Current image, source/buffer/map, recipe and context hashes; physical and raw delivery checks remain separate from visual critique')
 Path('build/look-view-check.json').write_text(json.dumps(result,indent=2));print('LOOK_REVIEW',len(rows),'current exported Cycles views,',delivery['new_gpu_mib'],'MiB new maps')


if __name__=='__main__':main()
