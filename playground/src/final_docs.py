"""Five bounded JPGs made only from verified exported-scene final renders."""
import argparse,hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,default=Path('renders/final'));a=p.parse_args();out=a.renders
    for filename in ('build/check.json','build/lookdev-check.json'):
        assert json.loads(Path(filename).read_text())['passed'],filename
    sites=('hero','above','front','side','back','eevee')
    details=('clamp-deck','stairs','transfer','slide-entrance','slide-exit','swing-hanger','swing-hollow','arch-swing','swing-seat','bucket-seat','climber','tube-junction','rubber-wear','rubber-seams','fiber-carryout','scale','pieces')
    views=[out/str(seed)/(shot+'.png') for seed in (101,202,303) for shot in sites]+[out/(shot+'.png') for shot in details]
    views += [out/'matches'/(name+'.png') for name in json.loads(Path('build/cameras.json').read_text())]
    cache={};receipts={}
    for path in views:
        meta=json.loads(path.with_suffix('.json').read_text());source=Path(meta['source'])
        assert source.resolve().is_relative_to(Path('export').resolve()),(path,source)
        assert 'exported glTF' in meta['stage'] and 'baked maps' in meta['stage'],path
        if source not in cache:
            doc=json.loads(source.read_text());files=[source]+[source.parent/r['uri'] for k in ('buffers','images') for r in doc.get(k,[]) if r.get('uri')]
            cache[source]=hashlib.sha256(b''.join(bytes.fromhex(digest(p)) for p in files)).hexdigest()
        assert meta['source_sha256']==digest(source) and meta['resource_bundle_sha256']==cache[source],('Stale render',path)
        im=Image.open(path);assert im.width==meta['width'] and im.width>=1200,(path,im.size)
        assert meta['engine']==('BLENDER_EEVEE' if path.stem=='eevee' else 'CYCLES'),path
        if path.stem=='hero':
            assert abs(meta['camera_location'][2]-1.65)<1e-5 and 35<=meta['lens_mm']<=50,path
            assert meta['sun_visibility']['elevation_degrees']==18,path
        receipts[str(path)]=dict(source=str(source),bundle=cache[source],engine=meta['engine'],pixels=list(im.size),image_sha256=digest(path))
    Path('build/final-provenance.json').write_text(json.dumps(dict(passed=True,views=len(views),renders=receipts,scope='Fresh exported-scene resource hashes, cameras, engines and native image dimensions. Appearance is judged in REVIEW.md.'),indent=2))
    folder=Path('docs');folder.mkdir(exist_ok=True);font=ImageFont.truetype(find_font('Noto Sans'),21)
    written={}
    def save(im,name):
        im=im.convert('RGB')
        if im.width>1600 or im.height>5000:im=ImageOps.contain(im,(1600,5000),Image.Resampling.LANCZOS)
        path=folder/name
        for quality in range(92,39,-4):
            im.save(path,quality=quality,optimize=True,progressive=True)
            if path.stat().st_size<=198000:break
        assert im.width<=1600 and path.stat().st_size<=200000,(path,path.stat().st_size)
        written[str(path)]=dict(size=list(im.size),bytes=path.stat().st_size,quality=quality,sha256=digest(path))
    def panel(canvas,path,box,label):
        x,y,w,h=box;im=ImageOps.contain(Image.open(path).convert('RGB'),(w,h-34),Image.Resampling.LANCZOS)
        canvas.paste(im,(x+(w-im.width)//2,y));ImageDraw.Draw(canvas).text((x+9,y+h-29),label,font=font,fill=(31,40,35))
    save(Image.open(out/'101/hero.png'),'hero.jpg')
    im=Image.new('RGB',(1600,1060),(232,233,229))
    panel(im,out/'202/hero.png',(0,0,800,570),'2005 / neighborhood park')
    panel(im,out/'303/hero.png',(800,0,800,570),'2013 / inclusive play')
    for j,(seed,label) in enumerate(((101,'1996 / Eastview relationships'),(202,'2005 / Lively relationships'),(303,'2013 / Simon relationships'))):
        panel(im,out/str(seed)/'above.png',(j*533,570,533,490),label)
    save(im,'sites.jpg')
    im=Image.new('RGB',(1600,1230),(232,233,229))
    for j,(shot,label) in enumerate((('clamp-deck','Split collar / punched plastisol'),('slide-exit','Faded bed / dug landing'),('swing-hollow','Belts / displaced fiber / wear mats'),('rubber-seams','Granules / pours / landing repair'))):
        panel(im,out/(shot+'.png'),((j%2)*800,(j//2)*615,800,615),label)
    save(im,'details.jpg')
    save(Image.open(out/'pieces-labeled.jpg'),'modules.jpg')
    im=Image.new('RGB',(1600,590),(232,233,229))
    panel(im,out/'scale.png',(0,0,800,590),'1.8 m adult / 1.1 m child scale markers')
    panel(im,out/'303/eevee.png',(800,0,800,590),'Exported inclusive site / Eevee')
    save(im,'scale-eevee.jpg')
    assert len(list(folder.glob('*.jpg')))==5
    Path('build/docs.json').write_text(json.dumps(dict(passed=True,images=written),indent=2));print('DOCS PASS',len(written),'JPGs;',len(views),'exported views')

if __name__=='__main__':main()
