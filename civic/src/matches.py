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
    for n,roi,d in [('hall',(800,1555,860,1567),'Sunlit concrete walk in front of the hall; approximate neutral, not a gray card'),
                    ('station-second',(1160,1290,1250,1305),'Concrete apron in front of the middle bay; approximate neutral'),
                    ('hall-close',(900,1638,980,1645),'Concrete sidewalk below the hall; approximate neutral')]:
        images[n],balances[n]=balance(n,roi,d)
    sp=site(101);p=next(p for p in cases() if p['seed']==707);x,y,_=sp['building_at'];l=x-p['width']/2;r=x+p['width']/2;f=y-p['depth']/2;top=p['floor']+p['stories']*p['story_pitch']+.63
    definitions={}
    # Full front bounding landmarks deliberately expose the original design's
    # different bay count, order and roof rather than tracing those features.
    rows=[((l,f,top),(161*2.5,454*2.5)),((r,f,top),(1091*2.5,355*2.5)),
          ((l,f,0),(164*2.5,611*2.5)),((r,f,0),(1093*2.5,621*2.5))]
    definitions['hall-street']=dict(seed=707,building_only=True,title='1938 town hall / larger generator envelope',photo=images['hall'],crop=(250,800,2850,1650),
        location=(24,-49,1.72),target=(-6,-8,4.8),lens=42,lens_bounds_mm=(25,65),camera_height_m=(1.72,.6),landmarks=landmarks(rows))
    # Clear native-resolution color photo of three brick apparatus bays. Fit
    # all twelve opening corners, rather than four corners in a blurred crop.
    sp=site(202);p=sp['building'];x,y,_=sp['building_at'];cx=x-p['width']/2+.4572+p['bay_width']/2;f=y-p['depth']/2;z=p['floor'];w=h=4.2672
    rows=[]
    for j,box in enumerate([(704,934,1026,1262),(1103,940,1428,1267),(1503,947,1828,1270)]):
        xx=cx+j*p['bay_width'];l,t,r,b=box
        rows += [((xx-w/2,f,z+h),(l,t)),((xx+w/2,f,z+h),(r,t)),((xx-w/2,f,z),(l,b)),((xx+w/2,f,z),(r,b))]
    definitions['station-bay']=dict(seed=202,title='Brick station / three sectional bays and apron from the street',photo=images['station-second'],crop=(600,830,1940,1380),
        location=(cx+p['bay_width']-1,f-30,1.72),target=(cx+p['bay_width'],f,2.25),lens=42,lens_bounds_mm=(25,90),camera_height_m=(1.72,.5),landmarks=landmarks(rows))
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
