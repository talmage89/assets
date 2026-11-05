"""Final-only five strip JPGs; run after the native-size review is logged."""
from pathlib import Path
from PIL import Image
import io,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.contact import review_sheet


def run():
    audit=json.loads(Path('build/strip-look/view-check.json').read_text());assert audit['passed']
    src=Path('renders/strip/checkpoint');dest=Path('docs');dest.mkdir(exist_ok=True)
    detail=Path('build/strip-look/docs-details.jpg')
    review_sheet([[src/(n+'.png') for n in ('storefront','walk','endcap')],
                  [src/(n+'.png') for n in ('pylon','rear','stalls')]],
                 detail,width=1600,title='Strip centers / storefront, walk, end cap, pylon, rear and stalls')
    for name,source in (('hero','hero.png'),('sites','sites.jpg'),('streets','streets.jpg'),('details','details.jpg'),('dusk','dusk.png')):
        im=Image.open(detail if name=='details' else src/source).convert('RGB');im.thumbnail((1600,10000),Image.Resampling.LANCZOS);path=dest/('strip-'+name+'.jpg')
        for q in range(92,29,-2):
            encoded=io.BytesIO();im.save(encoded,format='JPEG',quality=q,optimize=True,progressive=True)
            data=encoded.getvalue()
            if len(data)<=200000:break
        assert len(data)<=200000 and im.width<=1600,(path,im.size)
        path.write_bytes(data)
        print(path,im.size,len(data))

if __name__=='__main__':run()
