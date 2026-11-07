"""Final gallery from exported-asset frames, with current-bundle receipts."""
import json,sys
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
sys.path[:0]=[str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parents[2])]
from external import bundle
from kit.fonts import find_font


def frame(name):
    path=Path('renders/final')/name
    meta=json.loads(path.with_suffix('.json').read_text())
    assert meta['source'].endswith('.gltf') and meta['bundle_sha256']==bundle(Path(meta['source'])),('Stale gallery source',path)
    return path,meta


def montage(items,width=1600,columns=2):
    cell=width//columns;h=round(cell*.68);out=Image.new('RGB',(width,h*((len(items)+columns-1)//columns)),(29,32,30));d=ImageDraw.Draw(out)
    font=ImageFont.truetype(find_font('DejaVu Sans','Book'),17)
    for i,(name,label) in enumerate(items):
        path,_=frame(name);im=Image.open(path).convert('RGB');im.thumbnail((cell-12,h-36),Image.Resampling.LANCZOS)
        x=i%columns*cell;y=i//columns*h;out.paste(im,(x+(cell-im.width)//2,y+30));d.text((x+10,y+7),label,font=font,fill=(230,230,222))
    return out


def main():
    docs=Path('docs');docs.mkdir(exist_ok=True);rows=[]
    hero,_=frame('101/hero.png');im=Image.open(hero).convert('RGB');im.thumbnail((1600,1600),Image.Resampling.LANCZOS)
    outputs={'hero.jpg':im,
             'parks.jpg':montage([('101/above.png','2011 / Alder Glen'),('202/above.png','2004 / Cedar Junction'),('202/hero.png','Older municipal concrete'),('303/hero.png','1999 / Mill Creek prefab')]),
             'details.jpg':montage([('101/bowl.png','Block coping and tile'),('101/ledge.png','Wax and truck contact'),('101/stairs.png','Stairs and armored hubba'),('101/deep_end.png','Deep end / grit and drain'),('303/prefab.png','Composite / placed wheel slides'),('303/plate.png','Bare steel toe plate')]),
             'modules.jpg':Image.open(frame('modules.png')[0]).convert('RGB'),
             'scale-eevee.jpg':montage([('101/scale.png','1.8 m silhouette at the bowl'),('eevee/101/hero.png','Exported park / Eevee')])}
    for name,im in outputs.items():
        im.thumbnail((1600,1600),Image.Resampling.LANCZOS);path=docs/name
        for q in (90,86,82,78,74,70,65):
            im.save(path,quality=q,optimize=True)
            if path.stat().st_size<=200000:break
        assert path.stat().st_size<=200000 and im.width<=1600,(name,im.size,path.stat().st_size)
        rows.append(dict(path=str(path),size=list(im.size),bytes=path.stat().st_size,quality=q))
    Path('build/docs.json').write_text(json.dumps(rows,indent=2));print('FINAL DOCS',json.dumps(rows))
if __name__=='__main__':main()
