"""Fixed used-surface photo ROIs and independent display-value comparisons.

Statistics measure rendered appearance, not inverse albedo. White balance
preserves exposure. Any auxiliary paint control is explicitly named.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import srgb_to_linear,linear_to_srgb
from kit.fetch_refs import fetch
from cape_values import summarize,PHOTOS as CAPE

PHOTOS={
 'brick51':dict(file='split-builder-used-pa.jpg',neutral=(580,259,584,301),box=(220,350,338,377),why='white upper sash casing; living-wing brick under the picture sill'),
 'stone52':dict(file='split-pa-builder-c.jpg',neutral=(505,554,648,561),box=(982,673,1092,720),why='white upper window bottom casing; fieldstone below the right window, above the hedge'),
 'brick53':dict(file='split-pa-builder-d.jpg',neutral=(551,465,558,600),box=(125,601,510,677),why='white living-window casing; red-brown brick between picture sill and garage header'),
 'brick54':dict(file='split-foyer-used-pa.webp',neutral=(336,172,341,249),box=(75,220,124,278),why='white entry casing; mottled common brick left of the lower sash'),
 'brick55':dict(file='split-pa-split_entry_2_1.jpg',neutral=(813,493,821,549),box=(680,713,735,748),why='white upper sash casing; buff lower wall clear of the mailbox and snow'),
 'brick56':dict(file='split-pa-builder-a.jpg',neutral=(52,604,100,627),box=(175,289,426,330),why='unpainted sunlit concrete at the lower-left drive, assumed neutral gray; tan living-wall brick clear of the fixture and vehicle'),
 'battens':dict(file='split-side-fit.jpg',neutral=(700,163,704,213),box=(558,235,660,300),why='white upper sash stile; used vertical painted boards beneath the left sash; western photograph retained for material only'),
 'blue_lap':dict(file='split-pa-builder-c.jpg',neutral=(505,554,648,561),box=(704,439,789,507),why='white upper window casing; blue painted horizontal cladding, substrate not independently identified'),
 'vinyl':dict(file='split-builder-used-pa.jpg',neutral=(580,259,584,301),box=(468,312,767,340),why='white upper sash casing; updated pale upper lap face, away from window trims'),
 'garage':dict(file='split-oh-side-c.jpg',neutral=(914,300,921,405),box=(665,630,1001,747),why='white upper window casing; used white stamped door including low panel and impact creases'),
 'roof':dict(file='split-pa-builder-d.jpg',neutral=(551,465,558,600),box=(220,338,550,405),why='white living-window casing; used dark asphalt courses on the living roof'),
 'driveway':dict(file='split-pa-builder-a.jpg',neutral=(52,604,100,627),box=(116,508,404,619),why='unpainted sunlit concrete at the lower-left drive, assumed neutral gray; old concrete drive with joints, cracks and parked-car marks'),
}
for name in ('wood','aluminum','concrete','trim','glass'):
    s=CAPE[name];PHOTOS[name]=dict(file=s['file']+'.jpg',neutral=s['neutral'],box=s['box'],why=s['why']+'; accepted Cape reference/finish reused',coordinates_1200=True)


def prepare():
    local={'split-builder-used-pa.jpg','split-builder-used-oh.jpg','split-oh-side-b.jpg','split-used-bay.jpg','split-foyer-used-pa.webp','split-side-fit.jpg'}
    fetch('refs',list(dict.fromkeys(s['file'] for s in PHOTOS.values() if s['file'] not in local)))
    records={}
    for name,s in PHOTOS.items():
        path=Path('refs')/s['file'];im=ImageOps.exif_transpose(Image.open(path)).convert('RGB');scale=1
        if s.get('coordinates_1200'):
            preview=im.copy();preview.thumbnail((1200,1200));scale=im.width/preview.width
        neutral_box=tuple(round(v*scale) for v in s['neutral']);box=tuple(round(v*scale) for v in s['box'])
        a=srgb_to_linear(np.asarray(im)/255);x0,y0,x1,y1=neutral_box;white=np.median(a[y0:y1,x0:x1],axis=(0,1));gains=white.mean()/white
        corrected=np.clip(linear_to_srgb(a*gains),0,1);out=Path('refs')/('split-material-'+name+'.jpg')
        Image.fromarray(np.uint8(np.rint(corrected*255))).save(out,quality=98)
        x0,y0,x1,y1=box;stats=summarize(corrected[y0:y1,x0:x1].reshape(-1,3))
        records[name]={**s,'box':box,'neutral':neutral_box,'balanced':str(out),'linear_neutral':white.tolist(),'gains':gains.tolist(),'photo':stats,'original_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    Path('build/split/material-photos.json').write_text(json.dumps(records,indent=2))
    print(json.dumps({k:dict(Y=round(v['photo']['median'],4),tails=[round(v['photo'][p],4) for p in ('p10','p90')],ratios=[round(x,4) for x in v['photo']['ratios']]) for k,v in records.items()},indent=2))


def measure(folder):
    photos=json.loads(Path('build/split/material-photos.json').read_text());patches=json.loads((folder/'patches.json').read_text());records={}
    for name,s in patches.items():
        im=Image.open(folder/(name+'.png')).convert('RGB');x0,y0,x1,y1=map(round,s['box']);a=np.asarray(im)[y0:y1,x0:x1]/255
        mask=np.asarray(Image.open(folder/(name+'-mask.png')))[y0:y1,x0:x1]>0
        assert mask.sum()>1000,(name,int(mask.sum()))
        actual=summarize(a[mask]);ref=photos[name]['photo'];errors={k:actual[k]/ref[k]-1 for k in ('p10','median','p90')}
        hue=[actual['ratios'][i]/ref['ratios'][i]-1 for i in (0,2)]
        passed=abs(errors['median'])<=.10 and max(abs(errors['p10']),abs(errors['p90']))<=.15 and max(map(abs,hue))<=.10
        records[name]=dict(passed=passed,source=actual,photo=ref,relative_errors=errors,hue_relative_errors=hue,render=s,reference=photos[name])
        photo=Image.open(photos[name]['balanced']).crop(photos[name]['box']);render=im.crop((x0,y0,x1,y1));canvas=Image.new('RGB',(1200,650),(234,235,230));draw=ImageDraw.Draw(canvas)
        for i,(label,patch) in enumerate((('Used-surface photograph / stated neutral',photo),('Split '+('export' if s['source'].endswith('.gltf') else 'source')+' / Cycles / unedited pixels',render))):
            # Same physical sample framing is declared by each case. No color
            # normalization or pixel selection is applied to rendered images.
            patch=ImageOps.contain(patch,(590,550),Image.Resampling.LANCZOS);canvas.paste(patch,(i*600+(600-patch.width)//2,50+(550-patch.height)//2));draw.text((i*600+8,15),label,fill=(20,25,22))
        draw.text((12,606),f"{name}: Y median {actual['median']:.3f} / {ref['median']:.3f}; R:G:B {actual['ratios'][0]:.3f}:1:{actual['ratios'][2]:.3f} / {ref['ratios'][0]:.3f}:1:{ref['ratios'][2]:.3f}",fill=(20,25,22))
        canvas.save(folder/(name+'-pair.jpg'),quality=94)
    result=dict(passed=all(v['passed'] for v in records.values()),rows=records,scope='Fixed photograph/Cycles ROIs and independent material-ID ray masks; encoded Rec.709 Y prime and channel ratios. Not inverse albedo or a bake check.')
    (folder/'values.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:dict(passed=v['passed'],error={p:round(x,3) for p,x in v['relative_errors'].items()},hue=[round(x,3) for x in v['hue_relative_errors']]) for k,v in records.items()},indent=2));return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--folder',type=Path,default=Path('renders/split/lookdev/values'));a=p.parse_args()
    prepare() if a.prepare else measure(a.folder)
