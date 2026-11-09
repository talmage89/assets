"""Neutral-balanced photographic type fits with visible measured residuals."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from kit.photo_match import calibrate
from plans import site,cases


def linear(a):return np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
def srgb(a):return np.where(a<=.0031308,a*12.92,1.055*np.maximum(a,0)**(1/2.4)-.055)


def balance(name,roi,description):
    im=ImageOps.exif_transpose(Image.open('refs/'+name+'.jpg')).convert('RGB');arr=np.array(im)/255
    patch=linear(np.array(im.crop(roi))/255);rgb=np.median(patch.reshape(-1,3),axis=0);gain=rgb.mean()/np.maximum(rgb,.001)
    out=Path('build/balanced')/(name+'.png');out.parent.mkdir(parents=True,exist_ok=True)
    Image.fromarray(np.uint8(np.clip(srgb(linear(arr)*gain),0,1)*255+.5)).save(out)
    return str(out),dict(source='refs/'+name+'.jpg',neutral_roi=roi,assumed_neutral=description,median_linear=rgb.tolist(),gains=gain.tolist(),exposure='neutral mean retained; no exposure normalization')


def landmarks(rows):return [dict(world=w,pixel=p) for w,p in rows]


def main():
    images={};balances={}
    for n,roi,d in [('hall',(2660,1450,2720,1490),'Sunlit pale foundation stone; approximate neutral, not a gray-card calibration'),
                    ('station-period',(600,510,660,550),'White-painted masonry adjacent to the apparatus door; approximate neutral'),
                    ('hall-close',(1630,1180,1680,1270),'White-painted column shaft, diffuse shade; approximate neutral')]:
        images[n],balances[n]=balance(n,roi,d)
    sp=site(101);p=next(p for p in cases() if p['seed']==707);x,y,_=sp['building_at'];l=x-p['width']/2;r=x+p['width']/2;f=y-p['depth']/2;top=p['floor']+p['stories']*p['story_pitch']+.63
    definitions={}
    # Full front bounding landmarks deliberately expose the original design's
    # different bay count, order and roof rather than tracing those features.
    rows=[((l,f,top),(161*2.5,454*2.5)),((r,f,top),(1091*2.5,355*2.5)),
          ((l,f,0),(164*2.5,611*2.5)),((r,f,0),(1093*2.5,621*2.5))]
    definitions['hall-street']=dict(seed=707,building_only=True,title='1938 town hall / larger generator envelope',photo=images['hall'],crop=(250,800,2850,1650),
        location=(24,-49,1.72),target=(-6,-8,4.8),lens=42,lens_bounds_mm=(25,65),camera_height_m=(1.72,.6),landmarks=landmarks(rows))
    # One genuinely visible 1967 opening; no whole-station reconstruction claim.
    sp=site(202);p=sp['building'];x,y,_=sp['building_at'];cx=x-p['width']/2+.4572+p['bay_width']/2;f=y-p['depth']/2;z=p['floor'];w=h=4.2672
    rows=[((cx-w/2,f,z+h),(800,581)),((cx+w/2,f,z+h),(953,608)),((cx-w/2,f,z),(800,757)),((cx+w/2,f,z),(954,751))]
    definitions['station-bay']=dict(seed=202,title='1967 station / overhead opening from street',photo=images['station-period'],crop=(725,530,1020,820),
        location=(cx-5,f-13,1.72),target=(cx,f,2.25),lens=42,lens_bounds_mm=(25,70),camera_height_m=(1.72,.5),landmarks=landmarks(rows))
    # This second photo is tight on the real entablature and the two outer
    # column axes. Six versus four columns remains an explicit style difference.
    p=site(101)['building'];top=p['floor']+p['stories']*p['story_pitch'];f=-p['depth']/2-2.7;x=-6
    # Pixel measurements are in the original 3000px photograph, not the study JPEG.
    rows=[((x-3.9,f,p['floor']),(1751,1516)),((x+3.9,f,p['floor']),(1989,1517)),
          ((x-3.9,f,top-.55),(1751,1141)),((x+3.9,f,top-.55),(1989,1204))]
    definitions['entry-order']=dict(seed=101,title='1938 entry / order and bearing construction',photo=images['hall-close'],crop=(1500,1000,2080,1550),
        location=(-19,-23,1.72),target=(-6,-11.5,4.8),lens=45,lens_bounds_mm=(25,90),camera_height_m=(1.72,.6),landmarks=landmarks(rows))
    result={}
    for name,d in definitions.items():
        row=calibrate(d);row['seed']=d['seed'];row['building_only']=d.get('building_only',False);row['lens_status']='Estimated type/feature fit; different original building, not EXIF recovery or a dimensional survey.'
        result[name]=row;print(name,'lens',round(row['shot']['lens'],2),'RMS original px',round(row['residual_rms_pixels'],2))
    Path('build/reference-balance.json').write_text(json.dumps(balances,indent=2)+'\n')
    Path('build/matched-cameras.json').write_text(json.dumps(result,indent=2)+'\n')
    Path('build/photo-definitions.json').write_text(json.dumps(definitions,indent=2)+'\n')


if __name__=='__main__':main()
