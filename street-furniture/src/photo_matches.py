"""Hand-measured landmarks for three used-object form comparisons.

Photo pixels are used only in ignored comparison images. Neutral controls
remove the photograph's white balance before any color judgment. These are
different original designs, so residuals and construction differences remain
visible; a fitted camera is not a surveyed reconstruction.
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.photo_match import calibrate

def balanced(name,roi):
    src=Path('refs')/(name+'.jpg');im=Image.open(src).convert('RGB');a=np.asarray(im).astype(float)/255
    linear=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4);x0,y0,x1,y1=roi
    median=np.median(linear[y0:y1,x0:x1],axis=(0,1));gain=np.mean(median)/median;b=linear*gain
    s=np.where(b<=.0031308,b*12.92,1.055*np.maximum(b,0)**(1/2.4)-.055)
    out=Path('build/photo')/(name+'-balanced.jpg');out.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(np.uint8(np.clip(s,0,1)*255+.5)).save(out,quality=96)
    return str(out.resolve()),dict(neutral_roi_pixels=roi,neutral_median_linear_rgb=median.tolist(),linear_rgb_gains=gain.tolist(),control='bare neutral paving / no painted surface')

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/photo-calibration.json'));a=p.parse_args();results={}
    specs={
      'used-shelter':dict(photo='shelter-used',roi=(1840,1160,2020,1280),crop=(700,650,1500,1450),title='Used shelter / aluminum frame and glazing construction',keys=['Shelter'],location=(7,8,8),target=(0,0,1.3),lens=55,landmarks=[
        ((-1.8,.59,2.47),(105,123)),((1.8,.59,2.47),(357,310)),((1.8,-.59,2.47),(582,275)),((-1.8,-.59,2.47),(316,80)),((-1.8,.59,.15),(105,450)),((1.8,.59,.15),(369,677)),((1.8,-.59,.15),(584,635))]),
      'used-meter':dict(photo='meter-mechanical',roi=(2270,3300,2450,3550),crop=(0,0,2499,2500),title='Used mechanical meter / domed lens, cast bezel and coin crank',keys=['MeterSingle'],location=(.05,-1.1,1.55),target=(0,0,1.3),lens=80,landmarks=[
        ((-.084,-.078,1.373),(100,1070)),((.084,-.078,1.373),(2390,1020)),((0,-.078,1.487),(1260,35)),((-.101,-.025,1.35),(30,1340)),((.101,-.025,1.35),(2460,1210))]),
      'used-news':dict(photo='news-group',roi=(2200,3080,2800,3300),crop=(3600,950,4850,3040),title='Used standalone coin news cabinet / lower hinge and upper coin housing',keys=['NewsDaily'],location=(.7,-2.0,1.45),target=(0,0,.65),lens=70,landmarks=[
        ((-.2445,-.2175,.98),(3809,1485)),((.2445,-.2175,.98),(4666,1571)),((-.2445,-.2175,.34),(3767,2473)),((.2445,-.2175,.34),(4685,2530)),((.081,-.18,1.23825),(4064,1107)),((.231,-.18,1.23825),(4444,1123))]),
      'used-sign':dict(photo='speed-used',roi=(1660,3650,1750,3780),crop=(900,1380,2150,2870),title='Used R2-1 / white sheeting, black legend and border',keys=['RoadSign_speed30'],location=(.10,-2,1.9),target=(0,0,2.5),lens=65,landmarks=[
        ((-.3048,-.031,2.1336),(985,2795)),((.3048,-.031,2.1336),(2100,2795)),((.3048,-.031,2.8956),(2068,1445)),((-.3048,-.031,2.8956),(1012,1435))])
    }
    for name,d in specs.items():
        path,white=balanced(d.pop('photo'),d.pop('roi'));points=d.pop('landmarks');keys=d.pop('keys');crop=d['crop']
        if name=='used-shelter':
            # Rear view: photo's near end is our negative-X end. The original
            # design keeps its advertising at the opposite end; do not force
            # a mirrored, below-ground camera to conceal that difference.
            points=[((-w[0],w[1],w[2]),p) for w,p in points];d['location']=(-7,8,8);d['camera_height_m']=(8,.25)
        if name=='used-news':d['camera_height_m']=(1.5,.10)
        d.update(photo=path,landmarks=[dict(world=w,pixel=(p[0]+crop[0],p[1]+crop[1]) if name=='used-shelter' else p) for w,p in points],lens_bounds_mm=(30,140))
        result=calibrate(d);result.update(keys=keys,white_balance=white)
        lights={
          'used-shelter':dict(direction=(.6,-.45,-.9),energy=3.6,sky=.045,angle=1.5,exposure=-.15,reason='Crisp shadows fall down/right from shelter and pedestrians; bright roof, shaded rear panels'),
          'used-meter':dict(direction=(.6,.8,-1.25),energy=3.5,sky=.055,angle=2.0,exposure=-.05,reason='Direct highlights on upper-left bezel and cast shadow below crank'),
          'used-news':dict(direction=(.25,.8,-1.6),energy=.25,sky=.50,cloud=.85,angle=18,exposure=.10,reason='Soft shadows beneath cabinets; diffuse broken-cloud daylight; exposure calibrated on comparable front red stile, not side skin'),
          'used-sign':dict(direction=(.3,.8,-1.0),energy=.05,sky=.18,cloud=.80,angle=25,exposure=-1.90,reason='Shade above overcast wet paving, no directional cast shadow on sheeting; exposure calibrated on blank white ROI')
        }
        result['shot']['light']=lights[name];results[name]=result;print(name,'lens',round(result['shot']['lens'],2),'RMS',round(result['residual_rms_pixels'],2))
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(results,indent=2))
if __name__=='__main__':main()
