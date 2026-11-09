"""Checkpoint sheets and measured resources; no committed gallery generation."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet


def main():
    folder=Path('renders/checkpoint');images=sorted(folder.glob('*/*.png'))+sorted(folder.glob('*.png'))
    assert images,'Render the exports first'
    rows=[]
    for path in images:
        pix=np.asarray(Image.open(path).convert('RGB'))/255;y=pix@np.array((.2126,.7152,.0722))
        row=dict(image=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),display_y_percentiles=np.percentile(y,[1,10,50,90,99]).tolist(),fraction_below_01=float((y<.01).mean()),fraction_any_channel_above_995=float((pix.max(2)>.995).mean()))
        assert row['fraction_below_01']<.85,(path,'Rejected near-black frame')
        rows.append(row)
    contact(images,folder/'contact.jpg',width=2000,title='Civic / form and construction checkpoint / exported glTF and shared maps',captions={str(p):str(p.relative_to(folder).with_suffix('')) for p in images})
    pairs=sorted(Path('renders/matches').glob('*-pair.jpg'))
    if pairs:review_sheet([[p] for p in pairs],Path('renders/matches/contact.jpg'),width=2200,title='Civic / photographic type comparisons / fit residuals retained')
    family=json.loads(Path('build/family.json').read_text());checks=json.loads(Path('build/check.json').read_text());modules=json.loads(Path('build/modules.json').read_text())
    lines=['# Measured checkpoint resources','', '| Export | Placed triangles | Materials | glTF + BIN bytes |', '| --- | ---: | ---: | ---: |']
    for name,r in family.items():lines.append(f"| {name} | {r['placed_triangles']:,} | {r['materials']} | {r['gltf_bytes']+r['bin_bytes']:,} |")
    lines+=['','| Module | Triangles |','| --- | ---: |']
    for m in modules['modules']:lines.append(f"| {m['name']} | {m['triangles']:,} |")
    lines+=['',f"Shared civic/site images: {len(checks['unique_images'])}; {checks['shared_gpu_mib']:.3f} MiB at 8bpp with full mips.",'','Cars and town context are separate presentation actors. Vegetation is included in the site glTF but excluded from its static budget. No new civic image set is allocated.']
    Path('build/resource-report.md').write_text('\n'.join(lines)+'\n')
    Path('build/render-check.json').write_text(json.dumps(dict(passed=True,views=rows,photos='Pairs contain separately attributed reference photos; no photo pixels enter assets',contact=str(folder/'contact.jpg')),indent=2)+'\n')
    print('CIVIC REVIEW',len(images),'views;',len(pairs),'pairs')


if __name__=='__main__':main()
