"""Five final JPGs from current export renders; run after native inspection."""
import io,json,hashlib,sys,shutil
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.contact import review_sheet


def run():
    audit=json.loads(Path('renders/review/evidence-audit.json').read_text());assert len(audit)==83
    for key,row in audit.items():
        source=Path(row['source']);assert row['source_sha256']==hashlib.sha256(source.read_bytes()).hexdigest(),key
    base=Path('renders/final');temp=Path('build/docs');temp.mkdir(parents=True,exist_ok=True)
    layouts={
      'court':[[base/'Complex-301/hero.png'],[base/'Complex-301/dusk.png']],
      'garden-types':[[base/'Complex-302/hero.png',base/'Complex-303/hero.png'],[base/'Complex-304/hero.png',base/'Building-305/hero.png']],
      'townhouses':[[base/'Row-401/hero.png',base/'Row-402/hero.png'],[base/'Row-403/hero.png',base/'Row-404/hero.png']],
      'construction':[[base/'Building-304/stairs.png',base/'Building-304/gallery_dusk.png'],[base/'Building-305/balcony.png',base/'Row-403/garage.png'],[base/'Row-402/entry.png',base/'Building-301/scale.png']],
      'plans':[[Path('renders/plans/floor-plans.jpg'),Path('renders/plans/complex-plans.jpg')],[base/'Complex-301/above.png',base/'Complex-302/above.png'],[base/'Complex-303/above.png',base/'Complex-304/above.png']]}
    receipt={};out=Path('docs');out.mkdir(exist_ok=True)
    for name,layout in layouts.items():
        contact=temp/(name+'.jpg')
        labeled=[]
        for row in layout:
            current=[]
            for p in row:
                copy=temp/(p.parent.name+'_'+p.stem+p.suffix);shutil.copy2(p,copy);current.append(copy)
            labeled.append(current)
        review_sheet(labeled,contact,width=1600,title='Rill Court / '+name.replace('-',' '))
        im=Image.open(contact).convert('RGB');im.thumbnail((1600,10000),Image.Resampling.LANCZOS)
        for quality in range(94,25,-2):
            encoded=io.BytesIO();im.save(encoded,format='JPEG',quality=quality,optimize=True,progressive=True)
            if len(encoded.getvalue())<=200000:break
        data=encoded.getvalue();assert len(data)<=200000
        path=out/(name+'.jpg');path.write_bytes(data)
        receipt[str(path)]=dict(size=list(im.size),bytes=len(data),quality=quality,sha256=hashlib.sha256(data).hexdigest(),sources=[str(p) for row in layout for p in row])
        print(path,im.size,len(data),'quality',quality)
    assert len(list(out.glob('*.jpg')))==5
    Path('build/docs.json').write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':run()
