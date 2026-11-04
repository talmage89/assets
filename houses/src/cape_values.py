"""Independent display-space patch comparison; photos are inspection only.

Median and 10/90 tails of encoded Rec.709 luma; median R/G and B/G retain
the hue after neutral balancing. These are rendered appearances, not a claim
that an uncalibrated JPEG reveals physical albedo.
"""
import argparse,json,sys,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import srgb_to_linear,linear_to_srgb

PHOTOS={
 'wood':dict(file='cape-used-white',neutral=(579,604,587,704),box=(446,717,550,744),why='white-painted left door casing, in the same facade light'),
 'cedar':dict(file='cape-used-brown',neutral=(630,392,636,440),box=(579,477,625,505),unit_boxes_native=[(1595,1304,1610,1310),(1623,1304,1643,1310),(1657,1304,1674,1310),(1578,1326,1595,1332),(1606,1326,1633,1332),(1645,1326,1671,1332),(1684,1326,1698,1332),(1580,1347,1640,1354),(1655,1347,1695,1354)],why='white-painted left attic window casing; clean shingle patch below-left, avoiding foreground twigs; nine exposed lower-face unit samples exclude keyways and upper overlap shadows'),
 'roof':dict(file='cape-used-white',neutral=(579,604,587,704),box=(275,355,517,478),why='white-painted left door casing; roof has diffuse open-sky light'),
 'aluminum':dict(file='cape-used-metal',neutral=(697,391,706,484),box=(250,380,305,435),why='white-painted right corner board in front-wall daylight'),
 'vinyl':dict(file='cape-used-vinyl-houses',neutral=(784,218,792,282),box=(800,550,900,626),why='white-painted upper window casing on the same gray vinyl facade'),
 'cement':dict(file='cape-used-striated',neutral=(410,10,470,65),box=(20,5,680,450),measure_box=(40,125,650,210),why='clean white-painted upper shingle face; paint statistics use the clean upper face, excluding the low biological deposit; full pair retains two courses, face nails and the stagger'),
 'concrete':dict(file='cape-northeast-spring',neutral=(706,486,714,615),box=(465,710,535,738),why='white-painted window casing; poured plinth patch excluding the foreground post/well'),
 'trim':dict(file='cape-used-white',neutral=(579,604,587,704),box=(579,604,587,704),why='white-painted door casing, same neutral used for wall paint'),
 'brick':dict(file='cape-used-white',neutral=(579,604,587,704),box=(576,194,630,220),why='white-painted door casing; upper chimney face above lettering'),
 'glass':dict(file='cape-used-white',neutral=(579,604,587,704),box=(259,642,268,665),why='white-painted door casing; lower pane interior, excluding its muntin'),
}


def summarize(rgb):
    y=rgb@np.array([.2126,.7152,.0722]);median=np.median(rgb,axis=0)
    return dict(pixels=len(rgb),p10=float(np.quantile(y,.1)),median=float(np.median(y)),p90=float(np.quantile(y,.9)),rgb=median.tolist(),ratios=[float(median[0]/median[1]),1.,float(median[2]/median[1])])


def prepare():
    rows={}
    for name,s in PHOTOS.items():
        im=ImageOps.exif_transpose(Image.open(Path('refs')/(s['file']+'.jpg'))).convert('RGB')
        preview=im.copy();preview.thumbnail((1200,1200));scale=im.width/preview.width
        neutral_box=tuple(round(v*scale) for v in s['neutral']);box=tuple(round(v*scale) for v in s['box'])
        a=srgb_to_linear(np.array(im)/255);x0,y0,x1,y1=neutral_box;neutral=np.median(a[y0:y1,x0:x1],axis=(0,1));gain=neutral.mean()/neutral
        corrected=np.clip(linear_to_srgb(a*gain),0,1);p=Path('refs')/(s['file']+'-'+name+'-balanced.jpg');Image.fromarray(np.uint8(np.rint(corrected*255))).save(p,quality=98)
        measurement_box=tuple(round(v*scale) for v in s.get('measure_box',s['box']))
        x0,y0,x1,y1=measurement_box;stats=summarize(corrected[y0:y1,x0:x1].reshape(-1,3))
        rows[name]={**s,'original_sha256':hashlib.sha256((Path('refs')/(s['file']+'.jpg')).read_bytes()).hexdigest(),'box_1200px':s['box'],'neutral_1200px':s['neutral'],'box':box,'measurement_box':measurement_box,'neutral':neutral_box,'balanced':str(p),'linear_neutral':neutral.tolist(),'gains':gain.tolist(),'photo':stats}
        if s.get('unit_boxes_native'):
            values=[]
            for x0,y0,x1,y1 in s['unit_boxes_native']:values.append(float(np.median(corrected[y0:y1,x0:x1]@np.array((.2126,.7152,.0722)))))
            rows[name]['per_shingle']=dict(values=values,count=len(values),median=float(np.median(values)),sd=float(np.std(values)),cv=float(np.std(values)/np.mean(values)),p10=float(np.quantile(values,.1)),p90=float(np.quantile(values,.9)))
    Path('build/cape/material-photos.json').write_text(json.dumps(rows,indent=2));print(json.dumps({k:v['photo'] for k,v in rows.items()},indent=2))


def measure(folder):
    refs=json.loads(Path('build/cape/material-photos.json').read_text());spec=json.loads((folder/'patches.json').read_text());rows={}
    for name,s in spec.items():
        im=Image.open(folder/(s['image']+'.png')).convert('RGB');x0,y0,x1,y1=map(round,s['box']);a=np.asarray(im)[y0:y1,x0:x1]/255
        if s.get('material_mask'):
            keep=np.asarray(Image.open(folder/s['material_mask']))[y0:y1,x0:x1]>0;a=a[keep]
            assert len(a)>1000,(name,'Insufficient actual material pixels')
        actual=summarize(a.reshape(-1,3));ref=refs[name]['photo']
        errors={key:actual[key]/ref[key]-1 for key in ('p10','median','p90')}
        hue=[actual['ratios'][i]/ref['ratios'][i]-1 for i in (0,2)]
        passed=abs(errors['median'])<=.10 and max(abs(errors['p10']),abs(errors['p90']))<=.15 and max(map(abs,hue))<=.10
        rows[name]=dict(source=actual,photo=ref,relative_errors=errors,hue_relative_errors=hue,passed=passed,render=s,reference=refs[name])
        photo=Image.open(refs[name]['balanced']).crop(refs[name]['box']);render=im.crop((x0,y0,x1,y1))
        canvas=Image.new('RGB',(1200,630),(231,232,228));d=ImageDraw.Draw(canvas)
        stage_label='Cape export / Cycles / unedited pixels' if s.get('stage')=='delivered shared PBR' else 'Cape source / Cycles / unedited pixels'
        for i,(label,patch) in enumerate((('Used-house photograph / neutral balanced',photo),(stage_label,render))):
            patch=ImageOps.fit(patch,(590,550),method=Image.Resampling.LANCZOS);canvas.paste(patch,(i*600+5,40));d.text((i*600+10,12),label,fill=(20,25,22))
        d.text((12,604),f"{name}: median {actual['median']:.3f} / {ref['median']:.3f}; R:G:B {actual['ratios'][0]:.3f}:1:{actual['ratios'][2]:.3f} / {ref['ratios'][0]:.3f}:1:{ref['ratios'][2]:.3f}",fill=(20,25,22));canvas.save(folder/(name+'-pair.jpg'),quality=94)
    result=dict(passed=all(r['passed'] for r in rows.values()),scope='Fixed photographed and rendered ROIs, display Y prime and hue; not inverse-rendered albedo',rows=rows)
    (folder/'values.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:dict(passed=v['passed'],error=v['relative_errors'],hue=v['hue_relative_errors']) for k,v in rows.items()},indent=2));return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--folder',type=Path,default=Path('renders/cape/lookdev/values'));a=p.parse_args()
    prepare() if a.prepare else measure(a.folder)
