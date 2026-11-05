"""Final-only five strip JPGs; run after the native-size review is logged."""
from pathlib import Path
from PIL import Image
import json,hashlib


def run():
    audit=json.loads(Path('build/strip-look/view-check.json').read_text());assert audit['passed']
    src=Path('renders/strip/checkpoint');dest=Path('docs');dest.mkdir(exist_ok=True)
    for name,source in (('hero','hero.png'),('sites','sites.jpg'),('streets','streets.jpg'),('details','details.jpg'),('dusk','dusk.png')):
        im=Image.open(src/source).convert('RGB');im.thumbnail((1600,10000),Image.Resampling.LANCZOS);path=dest/('strip-'+name+'.jpg')
        for q in range(92,29,-2):
            im.save(path,quality=q,optimize=True,progressive=True)
            if path.stat().st_size<=200000:break
        assert path.stat().st_size<=200000 and im.width<=1600,(path,im.size)
        print(path,im.size,path.stat().st_size)

if __name__=='__main__':run()
