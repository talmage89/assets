"""Checkpoint sheets and measured resources; no committed gallery generation."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet


def receipt(path):
    data=json.loads(path.with_suffix('.json').read_text())
    sources=data.get('sources',[dict(path=data.get('source'),sha256=data.get('source_sha256'))])
    for row in sources:
        source=Path(row['path'])
        if not source.exists():source=ROOT/source
        assert source.is_file(),(path,source)
        assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256'],(path,'Stale exported subject',source)
    if data.get('context_recipe_sha256'):
        source=Path(__file__).parent
        current=hashlib.sha256(b''.join((source/n).read_bytes() for n in ('town.py','neighborhood.py','actors.py','library.py','sites.py','geo.py','turf.py'))).hexdigest()
        assert current==data['context_recipe_sha256'],(path,'Stale town/actor recipe')
    return sources


def main():
    folder=Path('renders/checkpoint');images=sorted(folder.glob('*/*.png'))+sorted(folder.glob('*.png'))
    assert images,'Render the exports first'
    rows=[]
    for path in images:
        pix=np.asarray(Image.open(path).convert('RGB'))/255;y=pix@np.array((.2126,.7152,.0722))
        row=dict(image=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),export_sources=receipt(path),display_y_percentiles=np.percentile(y,[1,10,50,90,99]).tolist(),fraction_below_01=float((y<.01).mean()),fraction_any_channel_above_995=float((pix.max(2)>.995).mean()))
        assert row['fraction_below_01']<.85,(path,'Rejected near-black frame')
        rows.append(row)
    contact(images,folder/'contact.jpg',width=2000,title='Civic / form and look checkpoint / exported glTF and shared maps',captions={str(p):str(p.relative_to(folder).with_suffix('')) for p in images})
    pairs=sorted(Path('renders/matches').glob('*-pair.jpg'))
    for pair in pairs:receipt(pair.with_name(pair.name.replace('-pair.jpg','.png')))
    if pairs:review_sheet([[p] for p in pairs],Path('renders/matches/contact.jpg'),width=2200,title='Civic / photographic type comparisons / fit residuals retained')
    source_pairs=sorted(Path('renders/source-matches').glob('*-pair.jpg'))
    for pair in source_pairs:
        path=pair.with_name(pair.name.replace('-pair.jpg','.png'));receipt(path)
        source=json.loads(path.with_suffix('.json').read_text())
        exported=json.loads(Path(source['export_pair']).with_suffix('.json').read_text())
        assert source['camera']==exported['camera'],(path,'Source/export camera differs')
        assert source['lighting']==exported['lighting'],(path,'Source/export lighting differs')
        assert source['width']==exported['width'] and source['width']>=800,(path,'Source/export width differs')
        assert Image.open(path).size==Image.open(source['export_pair']).size,(path,'Source/export dimensions differ')
    family=json.loads(Path('build/family.json').read_text());checks=json.loads(Path('build/check.json').read_text());modules=json.loads(Path('build/modules.json').read_text())
    lines=['# Measured checkpoint resources','', '| Export | Placed triangles | Materials | glTF + BIN bytes | Image MiB |', '| --- | ---: | ---: | ---: | ---: |']
    for name,r in family.items():
        memory=sum(im['gpu_mib'] for im in checks['files'][name]['images'])
        lines.append(f"| {name} | {r['placed_triangles']:,} | {r['materials']} | {r['gltf_bytes']+r['bin_bytes']:,} | {memory:.3f} |")
    lines+=['','| Module | Triangles | Materials | Shared image MiB |','| --- | ---: | ---: | ---: |']
    for m in modules['modules']:lines.append(f"| {m['name']} | {m['triangles']:,} | {m['materials']} | {m['image_gpu_mib']:.3f} |")
    pieces=[]
    for name,r in family.items():
        if name.startswith('Civic-'):pieces += [dict(building=name,**p) for p in r['source']['pieces']]
        else:
            p=r['plan'];lines += ['',f"{name}: {p['static_site']['triangles']:,} static triangles; {p['vegetation']['triangles']:,} vegetation triangles. Static image dependencies {p['static_site']['image_gpu_mib']:.3f} MiB; vegetation {p['vegetation']['image_gpu_mib']:.3f} MiB."]
    Path('build/piece-costs.json').write_text(json.dumps(dict(pieces=pieces,scope='Actual per-construction-object counts and resident shared image dependencies; never sum shared image costs across pieces'),indent=2)+'\n')
    for seed in (101,202):
        path=Path('build',f'town-costs-{seed}.json')
        if not path.exists():continue
        town=json.loads(path.read_text());lines += ['',f'Presentation actors / {seed}:','', '| Group | Placed triangles | Unique geometry triangles | Shared image MiB |','| --- | ---: | ---: | ---: |']
        for key in ('static_context','vegetation','cars'):
            q=town[key];lines.append(f"| {key} | {q['triangles']:,} | {q['unique_triangles']:,} | {q['image_gpu_mib']:.3f} |")
    lines+=['',f"Shared civic/site images: {len(checks['unique_images'])}; {checks['shared_gpu_mib']:.3f} MiB at 8bpp with full mips.",'','Cars and town context are separate presentation actors. Vegetation is included in the site glTF but excluded from its static budget. Image dependencies are shared, not additive. The garden July albedo variant reuses native lawn normal/ORM; no new civic three-map set is allocated.']
    Path('build/resource-report.md').write_text('\n'.join(lines)+'\n')
    Path('build/render-check.json').write_text(json.dumps(dict(passed=True,views=rows,source_pairs=[str(p) for p in source_pairs],photos='Pairs contain separately attributed reference photos; no photo pixels enter assets',contact=str(folder/'contact.jpg')),indent=2)+'\n')
    print('CIVIC REVIEW',len(images),'views;',len(pairs),'export pairs;',len(source_pairs),'source pairs')


if __name__=='__main__':main()
