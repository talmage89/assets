"""Full-resolution before/after pairs; no image alters an asset texture."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw

def main():
    root=Path('renders/before-after');out=root/'pairs';out.mkdir(parents=True,exist_ok=True)
    receipts=[]
    for before in sorted((root/'before').glob('*/*.png')):
        rel=before.relative_to(root/'before');after=root/'after'/rel
        assert after.exists(),after
        old=json.loads(before.with_suffix('.json').read_text());new=json.loads(after.with_suffix('.json').read_text())
        projection=lambda row:{k:v for k,v in row['camera'].items() if k!='isolate'}
        assert projection(old)==projection(new),(rel,'camera')
        for key in ('effective_lighting','engine','samples','width'):
            assert old[key]==new[key],(rel,key,old[key],new[key])
        for row in (old,new):
            source=Path(row['source']);assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256'],source
        a=Image.open(before).convert('RGB');b=Image.open(after).convert('RGB');assert a.size==b.size and a.width>=800
        im=Image.new('RGB',(a.width*2,a.height+30),(28,30,28));im.paste(a,(0,30));im.paste(b,(a.width,30));d=ImageDraw.Draw(im)
        d.text((12,8),f'{rel.parent}: archived checkpoint / BEFORE',fill='white');d.text((a.width+12,8),f'{rel.parent}: exported baked GLB / AFTER',fill='white')
        im.save(out/(rel.parent.name+'-'+rel.stem+'.jpg'),quality=94,optimize=True)
        receipts.append(dict(view=str(rel),panel_size=list(a.size),camera=projection(old),lighting=old['effective_lighting'],feature_isolation=dict(before=old['camera'].get('isolate'),after=new['camera'].get('isolate')),before_sha256=old['sha256'],after_sha256=new['sha256']))
    Path('build/before-after-check.json').write_text(json.dumps(dict(passed=True,pairs=len(receipts),views=receipts),indent=2))
    print('BEFORE/AFTER PASS',len(receipts),'identical cameras and lighting; source hashes verified')

if __name__=='__main__':main()
