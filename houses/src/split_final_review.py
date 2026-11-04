"""Current-export proof, honest bake loss, final-only five portfolio JPGs."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageDraw
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from ranch_review import sheet
from delivery_io import bundle_hash

ROOT=Path('renders/split');BUILD=Path('build/split/delivery')


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def recipe(value=False):
    names=('split_value_render.py','split_render.py','cape_value_render.py','cape_render.py','cape_reflections.py','ranch_render.py','render.py') if value else ('split_render.py','render.py','cape_reflections.py','ranch_render.py')
    return hashlib.sha256(b''.join((HERE/n).read_bytes() if value else n.encode()+(HERE/n).read_bytes() for n in names)).hexdigest()


def current(row,value=False):
    p=Path(row['source']);actual=bundle_hash(p) if p.suffix=='.gltf' else digest(p)
    assert actual==row['source_sha256'],(p,'stale source')
    assert digest(p.with_suffix('.json'))==row['metadata_sha256'],(p,'stale metadata')
    assert row['recipe_sha256']==recipe(value),(p,'stale render recipe')
    for path,sha in row['map_sha256'].items():assert digest(path)==sha,(p,path,'stale map')


def materials():
    folders=[ROOT/'source-values',ROOT/'final-values'];source,final=[json.loads((p/'values.json').read_text()) for p in folders]
    assert len(final['rows'])==17 and source['passed'] and final['passed'],[(n,r['relative_errors'],r['hue_relative_errors']) for n,r in final['rows'].items() if not r['passed']]
    rows={}
    for name,f in final['rows'].items():
        s=source['rows'][name]
        for folder,row in zip(folders,(s,f)):
            current(row['render'],True);assert digest(folder/(name+'.png'))==row['render']['image_sha256']
        ims=[np.asarray(Image.open(p/(name+'.png')).convert('RGB'))/255 for p in folders]
        masks=[np.asarray(Image.open(p/(name+'-mask.png')))>0 for p in folders];mask=masks[0]&masks[1]
        y=[im[mask]@np.array((.2126,.7152,.0722)) for im in ims];error=abs(y[1]-y[0])
        row=dict(source=s['source'],export=f['source'],photo=f['photo'],median_export_minus_source=f['source']['median']-s['source']['median'],mean_absolute_display_y_loss=float(error.mean()),p90_absolute_display_y_loss=float(np.quantile(error,.9)),relative_to_photo=f['relative_errors'],hue_relative_to_photo=f['hue_relative_errors'],neutral=f['reference']['why'])
        assert abs(row['median_export_minus_source'])<.03,(name,row)
        rows[name]=row
    (BUILD/'bake-loss.json').write_text(json.dumps(dict(passed=True,rows=rows,scope='Identical cameras/lights/EV and independent common material-ID masks. Display appearance, not JPEG-derived albedo.'),indent=2))
    sheet([(n,folders[1]/(n+'-pair.jpg')) for n in rows],folders[1]/'pairs.jpg',2,1200)
    sheet([(n+' / '+label,folder/(n+'.png')) for n in rows for label,folder in zip(('source','export'),folders)],folders[1]/'bake-loss.jpg',2,700)
    return rows


def whole_house():
    folders=[ROOT/'source-matches',ROOT/'final-matches'];rows={};pictures=[]
    records=json.loads((folders[0]/'provenance.json').read_text())
    for name in records:
        for folder in folders:
            row=json.loads((folder/'provenance.json').read_text())[name];current(row)
            proof=json.loads((folder/'masks.json').read_text())[name]
            assert proof['source_sha256']==row['source_sha256'] and proof['mask_sha256']==digest(folder/(name+'-mask.png'))
        ims=[np.asarray(Image.open(p/(name+'.png')).convert('RGBA'))/255 for p in folders]
        masks=[np.asarray(Image.open(p/(name+'-mask.png')))>0 for p in folders]
        mask=masks[0]&masks[1]&(ims[0][:,:,3]>.99)&(ims[1][:,:,3]>.99)
        y=[im[:,:,:3][mask]@np.array((.2126,.7152,.0722)) for im in ims];error=abs(y[1]-y[0])
        rows[name]=dict(pixels=int(mask.sum()),mean_absolute_display_y=float(error.mean()),p95_absolute_display_y=float(np.quantile(error,.95)),median_export_minus_source=float(np.median(y[1])-np.median(y[0])),scope='Common opaque projected asset silhouettes; presentation ground/context excluded')
        pictures.extend([(name+' / source',folders[0]/(name+'.png')),(name+' / export',folders[1]/(name+'.png'))])
    sheet(pictures,folders[1]/'bake-loss.jpg',2,1000);(BUILD/'whole-house-loss.json').write_text(json.dumps(rows,indent=2));return rows


def street_photo_pair():
    """Composition inspection only: a registered real street, not a camera fit."""
    source=Path('refs/split-midwest-summer.jpg');crop=(0,385,1000,690)
    views=[('Export: 35 mm / own sidewalk / 1.60 m',Image.open(ROOT/'street/street.png').convert('RGB')),
           ('Real split-level street, 1964 / elevated view / massing reference',Image.open(source).convert('RGB').crop(crop))]
    canvas=Image.new('RGB',(1600,400),(234,235,230));draw=ImageDraw.Draw(canvas)
    for i,(label,im) in enumerate(views):
        im=ImageOps.contain(im,(790,355),Image.Resampling.LANCZOS);canvas.paste(im,(i*800+(800-im.width)//2,35+(355-im.height)//2));draw.text((i*800+8,12),label,fill=(20,25,22))
    canvas.save(ROOT/'street/photo-pair.jpg',quality=93)
    return dict(source=str(source),sha256=digest(source),crop=crop,scope='Elevated 1964 monochrome street photograph: row rhythm/setbacks/massing only, not matched camera or color calibration')


def main():
    base=ROOT/'final';family=ROOT/'final-seeds';pairs=ROOT/'final-matches';seeds=list(range(51,57))
    materials();whole_house()
    sheet([(n,base/(n+'.png')) for n in ('front','side','rear','top')],base/'turnaround.jpg',2,1000)
    details=[('Entry / stoop',base/'entry.png'),('Eave / soffit',base/'eave.png'),('Veneer top',base/'veneer.png'),('Garage',base/'garage.png'),('Shallow bay',base/'bay/bay.png'),('Wet sill',base/'peeling.png')]
    sheet(details,base/'details.jpg',2,1000)
    sheet([(f'{s} / {n}',family/str(s)/(n+'.png')) for s in seeds for n in ('front','rear')],base/'family.jpg',2,1100)
    sheet([(n,pairs/(n+'-pair.jpg')) for n in records_pairs()],pairs/'pairs.jpg',1,1600)
    views=[]
    for folder in (base,base/'bay',base/'foyer',pairs,ROOT/'final-eevee',*[family/str(s) for s in seeds]):
        for name,row in json.loads((folder/'provenance.json').read_text()).items():
            current(row);assert Path(row['source']).suffix=='.gltf';p=folder/(name+'.png');assert digest(p)==row['image_sha256'];views.append((str(p.relative_to(ROOT)),p))
    street=json.loads((ROOT/'street/provenance.json').read_text())
    assert street['recipe_sha256']==hashlib.sha256(b''.join((HERE/n).read_bytes() for n in ('split_street.py','cape_street.py','street.py','render.py'))).hexdigest()
    assert digest(ROOT/'street/street.png')==street['image_sha256']
    for row in street['houses']:assert bundle_hash(Path(row['source']))==row['bundle_sha256']
    for row in street['context']:assert digest(row['source'])==row['sha256']
    assert abs(street['eye_height_above_sidewalk_m']-1.6)<1e-5 and .30<=street['houses'][0]['visible_frame_width']<=.39
    assert 35<=street['lens']<=50 and street['sensor_width_mm']==36 and street['camera_support'].startswith('House-side')
    assert street['houses'][0]['projected_frame_bounds_x'][0]<0,'Nearest living wing intentionally exits the left frame'
    rgb=np.asarray(Image.open(ROOT/'street/street.png').convert('RGB'))/255;lum=rgb@np.array((.2126,.7152,.0722))
    street_tone=dict(zip(('p1','p50','p95','p99'),map(float,np.quantile(lum,[.01,.5,.95,.99]))))
    street_tone.update(clipped_white_fraction=float(np.mean(np.min(rgb,axis=2)>.985)),scope='Entire street image including sky, ground and context; hero asset-mask check retained separately')
    assert street_tone['clipped_white_fraction']<.001
    (ROOT/'street/tonal.json').write_text(json.dumps(street_tone,indent=2))
    views.append(('Street',ROOT/'street/street.png'))
    sheet(views,base/'contact.jpg',3,850)
    tonal=json.loads((base/'tonal.json').read_text());assert tonal['clipped_white_fraction']<.001
    result=dict(passed=True,views=len(views),paths=[str(p) for n,p in views],tonal=tonal,street_tonal=street_tone,street_photo_reference=street_photo_pair(),street_eye_height_m=street['eye_height_above_sidewalk_m'],nearest_house_visible_frame_width=street['houses'][0]['visible_frame_width'],nearest_house_unclipped_frame_width=street['houses'][0]['projected_frame_width'])
    (BUILD/'view-check.json').write_text(json.dumps(result,indent=2))
    for name,path in dict(hero=base/'hero.png',turnaround=base/'turnaround.jpg',details=base/'details.jpg',family=base/'family.jpg',street=ROOT/'street/street.png').items():
        im=Image.open(path).convert('RGB');im.thumbnail((1600,3800),Image.Resampling.LANCZOS);dest=Path('docs')/('split-'+name+'.jpg')
        for quality in range(91,31,-4):
            im.save(dest,quality=quality,optimize=True)
            if dest.stat().st_size<=200000:break
        assert im.width<=1600 and dest.stat().st_size<=200000
    print('SPLIT_FINAL_VIEWS',result['views'],'current exports; tone',tonal)


def records_pairs():return ('side_pa','side_oh','foyer_pa','foyer_oh')


if __name__=='__main__':main()
