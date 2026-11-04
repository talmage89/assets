"""Current-export gates, bake-loss measurements and final-only portfolio JPGs."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from ranch_review import sheet
from delivery_io import bundle_hash


def recipe_sha(extra=()):
    paths=[HERE/name for name in ('cape_render.py','cape_reflections.py','render.py','ranch_render.py',*extra)]
    return hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in paths)).hexdigest()


def bake_loss():
    folders=[Path('renders/cape')/n for n in ('source-values','final-values')]
    source,final=[json.loads((p/'values.json').read_text()) for p in folders];assert source['passed'] and final['passed'],[(k,v['relative_errors']) for k,v in final['rows'].items() if not v['passed']]
    rows={}
    for name,f in final['rows'].items():
        s=source['rows'][name];spec=f['render']
        for folder,item in zip(folders,(s,f)):
            p=item['render'];file=Path(p['source']);digest=bundle_hash(file) if file.suffix=='.gltf' else hashlib.sha256(file.read_bytes()).hexdigest()
            assert digest==p['source_sha256'],(name,folder,'stale material render')
            assert p['metadata_sha256']==hashlib.sha256(file.with_suffix('.json').read_bytes()).hexdigest()
            assert p['render_recipe_sha256']==recipe_sha(('cape_value_render.py',)),(name,folder,'stale material recipe')
        ims=[np.asarray(Image.open(p/(name+'.png')).convert('RGB'))/255 for p in folders]
        masks=[np.asarray(Image.open(p/(name+'-mask.png')))>0 for p in folders];mask=masks[0]&masks[1]
        y=[im[mask]@np.array((.2126,.7152,.0722)) for im in ims]
        rows[name]=dict(source=s['source'],export=f['source'],photo=f['photo'],relative_to_photo=f['relative_errors'],hue_relative_to_photo=f['hue_relative_errors'],median_export_minus_source=f['source']['median']-s['source']['median'],mean_absolute_display_y_loss=float(abs(y[1]-y[0]).mean()),p90_absolute_display_y_loss=float(np.quantile(abs(y[1]-y[0]),.9)))
        # A material can have registered microtexture differences after filtering;
        # this gate detects a large change to its overall rendered appearance.
        assert abs(rows[name]['median_export_minus_source'])<.03,(name,rows[name])
    rows['cedar']['per_shingle']={key:value for key,value in [('source',source['rows']['cedar']['render']['per_shingle']),('export',final['rows']['cedar']['render']['per_shingle']),('photo',final['rows']['cedar']['reference']['per_shingle'])]}
    Path('build/cape/delivery/bake-loss.json').write_text(json.dumps(dict(passed=True,rows=rows,scope='Same cameras, lights, controls and exposure; independently ray-masked material pixels. Display-space appearance, not inferred albedo.'),indent=2))
    sheet([(n,folders[1]/(n+'-pair.jpg')) for n in rows],folders[1]/'pairs.jpg',2,1200)
    sheet([(n+' / '+label,folder/(n+'.png')) for n in rows for label,folder in zip(('source','export'),folders)],folders[1]/'bake-loss.jpg',2,650)
    return rows


def whole_house_loss():
    source=Path('renders/cape/source-matches');final=Path('renders/cape/final-matches');rows={};pictures=[]
    records=json.loads((source/'provenance.json').read_text())
    for name,row in records.items():
        file=Path(row['source']);assert file.suffix=='.blend' and hashlib.sha256(file.read_bytes()).hexdigest()==row['source_sha256']
        assert row['metadata_sha256']==hashlib.sha256(file.with_suffix('.json').read_bytes()).hexdigest()
        assert row['render_recipe_sha256']==recipe_sha()
        ims=[Image.open(p/(name+'.png')).convert('RGBA') for p in (source,final)];a,b=[np.asarray(im)/255 for im in ims];mask=(a[:,:,3]>.99)&(b[:,:,3]>.99)
        for folder in (source,final):
            proof=json.loads((folder/'masks.json').read_text())[name];path=folder/(name+'-mask.png')
            assert hashlib.sha256(path.read_bytes()).hexdigest()==proof['mask_sha256']
            expected=json.loads((folder/'provenance.json').read_text())[name]
            assert proof['source_sha256']==expected['source_sha256'] and proof['render_recipe_sha256']==expected['render_recipe_sha256']
            mask&=np.asarray(Image.open(path))>0
        ya=a[:,:,:3][mask]@np.array((.2126,.7152,.0722));yb=b[:,:,:3][mask]@np.array((.2126,.7152,.0722));error=abs(yb-ya)
        rows[name]=dict(pixels=int(mask.sum()),mean_absolute_display_y=float(error.mean()),p95_absolute_display_y=float(np.quantile(error,.95)),median_export_minus_source=float(np.median(yb)-np.median(ya)),scope='Same fitted camera and light; common opaque silhouette pixels, fine texture filtering included')
        pictures.extend([(name+' / source',source/(name+'.png')),(name+' / export',final/(name+'.png'))])
    sheet(pictures,final/'bake-loss.jpg',2,1000)
    Path('build/cape/delivery/whole-house-loss.json').write_text(json.dumps(rows,indent=2));return rows


def course_shadows():
    """Fold horizontal-lap profiles at independently established course periods.

    Width is the fraction below the midpoint between profile p10 and p90.
    This is illumination-sensitive and is reported, not forced to match by EV.
    """
    values=json.loads(Path('renders/cape/final-values/values.json').read_text());rows={}
    for name,number in (('wood',2.941),('vinyl',7.944),('aluminum',6.211)):
        ref=values['rows'][name]['reference'];spec=values['rows'][name]['render'];images=[Image.open(ref['balanced']).crop(ref['box']),Image.open('renders/cape/final-values/'+name+'.png').crop(tuple(map(round,spec['box'])))];stats=[]
        for im in images:
            a=np.asarray(im.convert('RGB'))/255;profile=np.median(a@np.array((.2126,.7152,.0722)),axis=1);period=len(profile)/number
            phase=(np.arange(len(profile))%period)/period;bins=np.array([np.median(profile[(phase>=k/32)&(phase<(k+1)/32)]) if np.any((phase>=k/32)&(phase<(k+1)/32)) else np.nan for k in range(32)]);bins=bins[np.isfinite(bins)]
            lo,hi=np.quantile(bins,[.1,.9]);stats.append(dict(courses_in_crop=number,profile_p10=float(lo),profile_p90=float(hi),dark_to_lit_ratio=float(lo/hi),shadow_fraction=float(np.mean(bins<(lo+hi)/2))))
        rows[name]=dict(photo=stats[0],export=stats[1],scope='Same physical number of courses; folded median scanline profile. Width is midpoint-threshold fraction, not a geometric shadow claim.')
    Path('build/cape/delivery/course-shadows.json').write_text(json.dumps(rows,indent=2));return rows


def main():
    seeds=list(range(31,37));base=Path('renders/cape/final');family=Path('renders/cape/final-seeds');pairs=Path('renders/cape/final-matches')
    material=bake_loss();course_shadows();whole_house_loss()
    sheet([(n,base/(n+'.png')) for n in ('front','side','rear','top')],base/'turnaround.jpg',2,900)
    sheet([(n,base/(n+'.png')) for n in ('dormer','eave','entry','chimney')],base/'details.jpg',2,1000)
    sheet([(f'{s} / {n}',family/str(s)/(n+'.png')) for s in seeds for n in ('front','rear')],base/'family.jpg',2,1100)
    sheet([(f'{s} / {n}',family/str(s)/(n+'.png')) for s in seeds for n in ('siding',)],base/'siding.jpg',2,1000)
    sheet([(n,pairs/(n+'-pair.jpg')) for n in ('cape_dormers','cape_plain')],pairs/'pairs.jpg',1,1600)
    # The supplemental peel photograph illustrates water and grain; its teal
    # paint is not used as a hue/value target for the off-white asset paint.
    sheet([('Used sill photograph / water damage',Path('refs/cape-used-peeling.jpg')),('Export / nose and sash-joint peeling',base/'peeling.png')],base/'peeling-pair.jpg',2,900)
    paths=[(n,base/(n+'.png')) for n in ('hero','front','side','rear','back','top','roof','dormer','eave','entry','chimney','scale','foundation','concrete','peeling')]
    paths.extend([('Eevee',Path('renders/cape/final-eevee/hero.png')),('Street',Path('renders/cape/street/street.png'))])
    paths.extend([(f'{s} / {n}',family/str(s)/(n+'.png')) for s in seeds for n in ('front','rear','siding')]);paths.extend([(f'{s} / {n}',family/str(s)/(n+'.png')) for s in (32,35) for n in ('hero','connector')]);paths.append(('32 / roof wear',family/'32/tired.png'));paths.extend([(n+' / fitted camera',pairs/(n+'.png')) for n in ('cape_dormers','cape_plain')])
    sheet(paths,base/'contact.jpg',3,800)
    views=[]
    for folder in (base,pairs,Path('renders/cape/final-eevee'),*[family/str(s) for s in seeds]):
        for name,row in json.loads((folder/'provenance.json').read_text()).items():
            assert row['render_recipe_sha256']==recipe_sha(),(folder,name,'stale camera/lighting recipe')
            source=Path(row['source']);assert source.suffix=='.gltf' and bundle_hash(source)==row['source_sha256'],(folder,name,'stale export')
            assert row['metadata_sha256']==hashlib.sha256(source.with_suffix('.json').read_bytes()).hexdigest()
            for file,digest in row['material_sha256'].items():assert hashlib.sha256(Path(file).read_bytes()).hexdigest()==digest
            assert row['stage']=='baked Cape delivery; shared external PBR maps';assert (folder/(name+'.png')).exists();views.append(str(folder/(name+'.png')))
    street=json.loads(Path('renders/cape/street/provenance.json').read_text())
    for row in street['houses']:assert bundle_hash(Path(row['source']))==row['bundle_sha256']
    for row in street['context']:assert hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['sha256']
    tonal=json.loads((base/'tonal.json').read_text());assert tonal['clipped_white_fraction']<.001
    assert abs(street['eye_height_above_sidewalk_m']-1.68)<1e-5 and .28<=street['houses'][0]['projected_frame_width']<=.42
    result=dict(passed=True,views=len(views)+1,paths=views+['renders/cape/street/street.png'],tonal=tonal,street_eye_height_m=street['eye_height_above_sidewalk_m'],nearest_house_frame_width=street['houses'][0]['projected_frame_width'])
    Path('build/cape/delivery/view-check.json').write_text(json.dumps(result,indent=2))
    for name,path in dict(hero=base/'hero.png',turnaround=base/'turnaround.jpg',details=base/'details.jpg',family=base/'family.jpg',street=Path('renders/cape/street/street.png')).items():
        im=Image.open(path).convert('RGB');im.thumbnail((1600,3500),Image.Resampling.LANCZOS);dest=Path('docs')/('cape-'+name+'.jpg')
        for quality in range(91,35,-4):
            im.save(dest,quality=quality,optimize=True)
            if dest.stat().st_size<=200000:break
        assert im.width<=1600 and dest.stat().st_size<=200000
    print('CAPE_FINAL_VIEWS',result['views'],'current bundles; tonal',tonal)

if __name__=='__main__':main()
