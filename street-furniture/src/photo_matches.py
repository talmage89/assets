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
      'used-meter':dict(photo='meter-used',roi=(690,600,790,900),crop=(0,0,800,1200),title='Used meter / casting section, dome and vault',keys=['MeterSingle'],location=(.08,-1.1,1.34),target=(0,0,1.28),lens=60,landmarks=[
        ((0,0,1.52),(367,25)),((-.094,0,1.37),(55,300)),((.094,0,1.37),(668,308)),((0,-.08,1.30),(381,790)),((0,0,1.04),(391,1170))]),
      'used-news':dict(photo='news-used',roi=(1550,2220,1730,2370),crop=(2580,620,3230,2320),title='Used pedestal news rack / window, door and support proportions',keys=['NewsPedestal'],location=(.8,-2.2,1.1),target=(0,0,.6),lens=55,landmarks=[
        ((-.23,-.215,1.16),(55,77)),((.23,-.215,1.16),(458,56)),((-.23,-.215,.34),(72,831)),((.23,-.215,.34),(466,816)),((-.20,-.19,0),(80,1452)),((.20,-.19,0),(617,1450))])
    }
    for name,d in specs.items():
        path,white=balanced(d.pop('photo'),d.pop('roi'));points=d.pop('landmarks');keys=d.pop('keys');crop=d['crop']
        if name=='used-shelter':
            # Rear view: photo's near end is our negative-X end. The original
            # design keeps its advertising at the opposite end; do not force
            # a mirrored, below-ground camera to conceal that difference.
            points=[((-w[0],w[1],w[2]),p) for w,p in points];d['location']=(-7,8,8);d['camera_height_m']=(8,.25)
        if name=='used-news':d['camera_height_m']=(1.3,.05)
        d.update(photo=path,landmarks=[dict(world=w,pixel=(p[0]+crop[0],p[1]+crop[1])) for w,p in points],lens_bounds_mm=(30,140))
        result=calibrate(d);result.update(keys=keys,white_balance=white);results[name]=result;print(name,'lens',round(result['shot']['lens'],2),'RMS',round(result['residual_rms_pixels'],2))
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(results,indent=2))
if __name__=='__main__':main()
