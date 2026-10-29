"""Reference-only linear RGB adaptation; never used by the asset generator."""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageDraw
BASE=Path(__file__).resolve().parents[1]
# Native upright rectangles, independently selected in each photograph.
# Silver highlights can carry reflected color; that uncertainty is explicit.
NEUTRALS={
 'ammo':('exposed gray lead cap on center cartridge, estimated neutral',(374,149,410,161)),
 'right':('unclipped white paper below the lower carbine',(1450,485,1730,545)),
 'profile':('bright bare screw-slot facet, upper left receiver screw',(692,103,697,108)),
 'receiver':('polished pivot screw facet on the left plate',(363,100,369,105)),
 'open':('polished cross-pin highlight, estimated silver neutral',(158,243,163,248)),
 'open2':('broad exposed bolt flat, estimated silver neutral',(470,166,570,177)),
 'rear-blade':('plain gray photo backdrop beside the steel blade',(20,20,95,85)),
 'rear-sheet':('plain gray backdrop above the leaf',(320,35,480,90)),
}


def linear(a):return np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
def srgb(a):return np.where(a<=.0031308,a*12.92,1.055*np.maximum(a,0)**(1/2.4)-.055)


def main():
    out=BASE/'build/white-balanced';out.mkdir(parents=True,exist_ok=True);report={}
    for name,(neutral,rect) in NEUTRALS.items():
        im=ImageOps.exif_transpose(Image.open(BASE/'refs'/(name+'.jpg'))).convert('RGB')
        data=np.asarray(im,dtype=float)/255;patch=data[rect[1]:rect[3],rect[0]:rect[2]].reshape(-1,3)
        valid=patch[(patch.max(axis=1)<.985)&(patch.min(axis=1)>.06)]
        if not len(valid):raise ValueError((name,'neutral patch clipped or black'))
        median=np.median(linear(valid),axis=0);luma=float(median@np.array([.2126,.7152,.0722]));gains=luma/median
        corrected=np.clip(srgb(linear(data)*gains),0,1)
        Image.fromarray(np.round(corrected*255).astype('uint8')).save(out/(name+'.png'))
        marked=im.copy();d=ImageDraw.Draw(marked);d.rectangle(rect,outline='red',width=2)
        marked.thumbnail((1600,1600));marked.save(out/(name+'-neutral.jpg'),quality=92)
        report[name]=dict(neutral=neutral,rectangle_native=rect,linear_rgb_gains=gains.tolist(),
            patch_pixels=len(valid),native_linear_median=median.tolist(),
            limitation='estimated neutral; reflected light and tiny facets cannot establish calibrated albedo')
    (out/'corrections.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v['linear_rgb_gains'] for k,v in report.items()},indent=2))


if __name__=='__main__':main()
