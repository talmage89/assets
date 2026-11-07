"""Three period fits, using kit.photo_match with explicit neutral controls.

Hand-read landmarks fit the camera only; no reference becomes mesh or texture.
These are comparisons of original designs, with their residuals left visible.
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import photo_match
from kit.photo_match import calibrate

def level_calibration(match):
    """Use the kit solver with roll fixed by the photograph's vertical posts."""
    original=photo_match.project
    def project(parameters,*args):
        parameters=parameters.copy();parameters[6]=0
        return original(parameters,*args)
    photo_match.project=project
    try:return calibrate(match)
    finally:photo_match.project=original

def balanced(name,roi,neutral):
    im=Image.open(Path('refs')/(name+'.jpg')).convert('RGB');rgb=np.asarray(im,dtype=float)/255
    linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4);scale=im.width/(800 if '2005' in name else 1200)
    x0,y0,x1,y1=[round(v*scale) for v in roi];c=np.median(linear[y0:y1,x0:x1],axis=(0,1));gain=np.mean(c)/np.maximum(c,1e-6);v=np.clip(linear*gain,0,1);srgb=np.where(v<=.0031308,v*12.92,1.055*v**(1/2.4)-.055)
    path=Path('build/photo')/(name+'-balanced.jpg');path.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(np.uint8(srgb*255+.5)).save(path,quality=96)
    return str(path),scale,dict(neutral=neutral,neutral_roi_pixels=[x0,y0,x1,y1],neutral_linear_rgb=c.tolist(),rgb_gain=gain.tolist(),limitation='No gray card: an identified neutral object, not calibrated reflectance')

def main():
    specs={
      'used-deck-2009':dict(photo='roswell-2009',roi=(8,536,40,545),neutral='neutral concrete path at far left, in shade',crop=(145,365,400,720),source='Playground-202.gltf',location=(4,-7,1.6),target=(0,0,.9),lens=65,points=[((-.6096,-.6096,1.7296),(218,419)),((.6096,-.6096,1.7296),(329,417)),((-.6096,-.6096,0),(218,675)),((.6096,-.6096,0),(329,670)),((-.6096,-.6096,.6096),(218,574)),((.6096,-.6096,.6096),(329,570))]),
      'used-swings-2009':dict(photo='adair-2009',roi=(579,539,582,541),neutral='small white cap on seated child near swing, bright side',crop=(485,455,720,586),source='Playground-202.gltf',location=(6,-13,1.7),target=(0,0,1.2),lens=65,points=[((-3.35,0,2.4384),(540.5,492.0)),((0,0,2.4384),(609.2,495.3)),((3.35,0,2.4384),(673.1,498.3)),((-3.35,-.64,0),(525.3,580.2)),((-3.35,.64,0),(554,582)),((0,-.64,0),(594.6,577.5)),((0,.64,0),(623,580.6)),((3.35,-.64,0),(657.8,579.5)),((3.35,.64,0),(685.2,580.8))]),
      'used-stair-2005':dict(photo='playground-2005',roi=(312,386,316,392),neutral='gray galvanized stair cheek below rail',crop=(210,200,390,445),source='Playground-101.gltf',location=(3,-5,1.6),target=(0,-.9,1.0),lens=65,points=[((-.45,0,1.2192),(279,309)),((.45,0,1.2192),(311,315)),((-.45,-1.95,.1524),(321,411)),((.45,-1.95,.1524),(356,407)),((-.45,0,1.8792),(279,258)),((.45,0,1.8792),(308,268))])}
    out={}
    for name,d in specs.items():
        photo,scale,white=balanced(d.pop('photo'),d.pop('roi'),d.pop('neutral'));pts=d.pop('points');source=d.pop('source');crop=[round(v*scale) for v in d.pop('crop')]
        full_width=Image.open(photo).width;factor=full_width/(crop[2]-crop[0])
        if name=='used-stair-2005':d['lens']=20;d['location']=(-4,-4,1.65)
        d['lens']*=factor
        match=dict(**d,photo=photo,crop=crop,title=name.replace('-',' '),landmarks=[dict(world=w,pixel=(p[0]*scale,p[1]*scale)) for w,p in pts],lens_bounds_mm=((12 if name=='used-stair-2005' else 35)*factor,120*factor),camera_height_m=(1.65,3.),exposure=-.25)
        if name=='used-deck-2009':
            # Canon's 5.8mm / 35mm diagonal-equivalent specification on a
            # 4:3 sensor becomes 36.4mm horizontal-equivalent on our 36mm sensor.
            match['lens']=36.4*factor;match['lens_bounds_mm']=(36.0*factor,36.8*factor);match['location']=(6,-5,1.65)
        if name=='used-swings-2009':
            match['lens']=70*factor;match['lens_bounds_mm']=(69*factor,71*factor);match['location']=(45,-50,1.65);match['target']=(0,0,1.2)
            offset=(-11.1,1,0)
            for lm in match['landmarks']:lm['world']=[lm['world'][i]+offset[i] for i in range(3)]
            for k in ('location','target'):match[k]=[match[k][i]+offset[i] for i in range(3)]
        if name=='used-stair-2005':
            match['lens_bounds_mm']=(12*factor,40*factor)
            def turn(p):return [-.6096+p[1],-p[0],p[2]]
            for lm in match['landmarks']:lm['world']=turn(lm['world'])
            for k in ('location','target'):match[k]=turn(match[k])
        row=(level_calibration if name=='used-stair-2005' else calibrate)(match);row.update(source=source,white_balance=white,ground_z=-.01,full_photo_equivalent_lens_mm=row['shot']['lens']/factor,lens_note='Fitted lens uses a 36mm sensor width covering the tight crop. Full-photo value is horizontal-equivalent, rescaled by crop/full width; a 4:3 sensor differs from diagonal 35mm-film equivalence.');out[name]=row;print(name,'lens',round(row['shot']['lens'],2),'RMS',round(row['residual_rms_pixels'],2),'pixels','height',round(row['shot']['location'][2],2))
        row['rms_fraction_of_crop_width']=row['residual_rms_pixels']/(crop[2]-crop[0])
        row['maximum_landmark_error_pixels']=float(np.asarray(row['residuals_pixels']).max())
    out['used-swings-2009']['lens_status']='Original EXIF: Canon EOS 5D, 70mm; full-frame equivalent fit constrained to 69–71mm. Original compatible frame, not a surveyed replica.'
    out['used-deck-2009']['lens_status']='EXIF 5.8mm on PowerShot SD1000. Canon specifies 35mm diagonal-equivalent; its 4:3 frame corresponds to 36.4mm horizontal-equivalent. Fit constrained to 36.0–36.8mm; original equipment dimensions still differ.'
    out['used-stair-2005']['lens_status']='EXIF absent in downloaded image. Wide full-image horizontal lens bounded to 12–40mm; camera roll fixed at zero from the vertical posts. Head/foot/grip correspondences re-read on the native photograph; original construction still differs.'
    Path('build/cameras.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
