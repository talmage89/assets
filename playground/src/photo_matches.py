"""Three period fits, using kit.photo_match with explicit neutral controls.

Hand-read landmarks fit the camera only; no reference becomes mesh or texture.
These are comparisons of original designs, with their residuals left visible.
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.photo_match import calibrate

def balanced(name,roi,neutral):
    im=Image.open(Path('refs')/(name+'.jpg')).convert('RGB');rgb=np.asarray(im,dtype=float)/255
    linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4);scale=im.width/(800 if '2005' in name else 1200)
    x0,y0,x1,y1=[round(v*scale) for v in roi];c=np.median(linear[y0:y1,x0:x1],axis=(0,1));gain=np.mean(c)/np.maximum(c,1e-6);v=np.clip(linear*gain,0,1);srgb=np.where(v<=.0031308,v*12.92,1.055*v**(1/2.4)-.055)
    path=Path('build/photo')/(name+'-balanced.jpg');path.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(np.uint8(srgb*255+.5)).save(path,quality=96)
    return str(path),scale,dict(neutral=neutral,neutral_roi_pixels=[x0,y0,x1,y1],neutral_linear_rgb=c.tolist(),rgb_gain=gain.tolist(),limitation='No gray card: an identified neutral object, not calibrated reflectance')

def main():
    specs={
      'used-deck-2009':dict(photo='roswell-2009',roi=(8,536,40,545),neutral='neutral concrete path at far left, in shade',crop=(180,390,355,690),source='ComparisonDeck.gltf',location=(4,-7,1.6),target=(0,0,.9),lens=65,points=[((-.6096,-.6096,1.7296),(218,419)),((.6096,-.6096,1.7296),(329,417)),((-.6096,-.6096,0),(218,675)),((.6096,-.6096,0),(329,670)),((-.6096,-.6096,.6096),(218,574)),((.6096,-.6096,.6096),(329,570))]),
      'used-swings-2009':dict(photo='adair-2009',roi=(579,539,582,541),neutral='small white cap on seated child near swing, bright side',crop=(505,470,705,600),source='ComparisonSwings.gltf',location=(6,-13,1.7),target=(0,0,1.2),lens=65,points=[((-3.35,0,2.4384),(539,496)),((0,0,2.4384),(608,500)),((3.35,0,2.4384),(672,502)),((-3.35,-1.16,0),(524,580)),((-3.35,1.16,0),(553,581)),((0,-1.16,0),(591,580)),((3.35,-1.16,0),(658,579)),((3.35,1.16,0),(685,581))]),
      'used-stair-2005':dict(photo='playground-2005',roi=(312,386,316,392),neutral='gray galvanized stair cheek below rail',crop=(235,220,370,425),source='Stairs48.gltf',location=(3,-5,1.6),target=(0,-.9,1.0),lens=65,points=[((-.45,0,1.2192),(257,279)),((.45,0,1.2192),(280,288)),((-.45,-1.95,.1524),(316,408)),((.45,-1.95,.1524),(354,404)),((-.45,0,2.0992),(263,232)),((.45,0,2.0992),(287,239))])}
    out={}
    for name,d in specs.items():
        photo,scale,white=balanced(d.pop('photo'),d.pop('roi'),d.pop('neutral'));pts=d.pop('points');source=d.pop('source');crop=[round(v*scale) for v in d.pop('crop')]
        full_width=Image.open(photo).width;factor=full_width/(crop[2]-crop[0])
        if name=='used-stair-2005':d['lens']=20;d['location']=(-4,-4,1.65)
        d['lens']*=factor
        match=dict(**d,photo=photo,crop=crop,title=name.replace('-',' '),landmarks=[dict(world=w,pixel=(p[0]*scale,p[1]*scale)) for w,p in pts],lens_bounds_mm=((12 if name=='used-stair-2005' else 35)*factor,120*factor),camera_height_m=(1.65,.3),exposure=-.25)
        row=calibrate(match);row.update(source=source,white_balance=white,ground_z=-.01,full_photo_equivalent_lens_mm=row['shot']['lens']/factor,lens_note='Fitted lens is for a 36mm sensor covering the tight crop. Full-photo equivalent rescales by crop/full width.');out[name]=row;print(name,'lens',round(row['shot']['lens'],2),'RMS',round(row['residual_rms_pixels'],2),'pixels','height',round(row['shot']['location'][2],2))
    Path('build/cameras.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
