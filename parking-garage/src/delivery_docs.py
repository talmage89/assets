"""Five bounded JPEGs from an explicitly inspected exported render recipe."""
import hashlib,io,json,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import review_sheet
from lookdev_review import verify_receipt


def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def recipe():
    return {str(p):digest(p) for p in sorted(Path('src').glob('*'))
            if p.suffix in ('.py','.mk','.sh') or p.name.endswith('-surface.json')}


def encode(source,dest):
    im=Image.open(source).convert('RGB')
    if im.width>1600:im=im.resize((1600,round(im.height*1600/im.width)),Image.Resampling.LANCZOS)
    for quality in range(94,35,-1):
        payload=io.BytesIO();im.save(payload,format='JPEG',quality=quality,optimize=True,subsampling=0)
        if len(payload.getvalue())<=200000:break
    assert len(payload.getvalue())<=200000
    dest.write_bytes(payload.getvalue())
    return dict(source=str(source),source_sha256=digest(source),output=str(dest),sha256=digest(dest),bytes=dest.stat().st_size,size=list(im.size),quality=quality)


def main():
    acceptance=Path('src/delivery-acceptance.json')
    assert acceptance.exists(),'Open and critique every final at full size before recording acceptance'
    approved=json.loads(acceptance.read_text());assert approved['recipe']==recipe(),'Recipe changed since visual review'
    assert approved['parameters']==json.loads(Path('build/delivery-render-parameters.json').read_text()),'Render parameters changed since review'
    folder=Path('renders/final');receipts=json.loads((folder/'views.json').read_text())
    assert len(receipts)==33
    for r in receipts:verify_receipt(r)
    module_receipts=json.loads((folder/'module-views.json').read_text())
    assert len(module_receipts)==25
    for r in module_receipts:verify_receipt(r)
    for suffix in ('-matches','-source-matches'):
        pairs=json.loads(Path('renders/final'+suffix+'/views.json').read_text())
        assert {r['name'] for r in pairs}=={'precast','pleasant','harmon'}
        assert all('pair_sha256' in r for r in pairs)
        for r in pairs:verify_receipt(r)
    work=Path('build/docs');work.mkdir(parents=True,exist_ok=True)
    review_sheet([[folder/'101/above.png',folder/'202/above.png'],[folder/'101/plan_path.png']],work/'family.jpg',width=1600,title='Two systems / bays, parking and drive paths')
    names=['101/aisle','101/ramp_turn','101/tower_open','202/entry','202/top_deck','101/scale','202/eevee']
    paths=[folder/(n+'.png') for n in names]
    review_sheet([paths[:3],paths[3:5],paths[5:]],work/'details.jpg',width=1600,title='Construction, maintained use, scale and Eevee')
    docs=Path('docs');docs.mkdir(exist_ok=True);report=[]
    for source,name in ((folder/'101/hero.png','hero-101'),(folder/'202/hero.png','hero-202'),(work/'family.jpg','family'),(work/'details.jpg','details'),(folder/'modules.png','modules')):
        report.append(encode(source,docs/(name+'.jpg')))
    Path('build/docs.json').write_text(json.dumps(dict(images=report,visual_review=approved['review']),indent=2)+'\n')
    print('FINAL DOCS',[(r['output'],r['bytes']) for r in report],flush=True)


if __name__=='__main__':main()
