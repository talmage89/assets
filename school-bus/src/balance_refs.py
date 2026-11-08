"""Neutral-balance comparison copies only. Originals never enter a material."""
from pathlib import Path
import json,numpy as np
from PIL import Image
BASE=Path(__file__).resolve().parents[1]
PATCHES={'front':((30,140,190,180),'background snow'),
         'side':((735,760,875,815),'unmarked dry asphalt'),
         'rear':((370,475,530,492),'pale gray concrete curb'),
         'vision':((700,905,725,920),'near white parking stripe'),
         'c2':((320,870,350,900),'white parking stripe beside entrance side'),
         'used':((60,450,105,477),'unlettered white trailer panel behind the nose')}
PAINT_PATCHES={'front':(1010,545,1050,565),'vision':(450,525,490,540),
               'used':(1075,543,1085,553)}
def main():
    out=BASE/'build/balanced';out.mkdir(parents=True,exist_ok=True);rows={}
    for name,(box,neutral) in PATCHES.items():
        filename={'vision':'vision-service.jpg','c2':'c2-77.jpg','used':'used-long-side.jpg'}.get(name,f'service-{name}.jpg')
        im=Image.open(BASE/'refs'/filename).convert('RGB');factor=im.width/1400
        rect=tuple(round(x*factor) for x in box);arr=np.asarray(im,dtype=float)/255
        x0,y0,x1,y1=rect;median=np.median(arr[y0:y1,x0:x1],axis=(0,1));gains=np.clip(np.mean(median)/median,.8,1.25)
        result=np.clip(arr*gains,0,1);Image.fromarray(np.round(result*255).astype('uint8')).save(out/filename,quality=98)
        rows[name]=dict(assumed_neutral=neutral,pixel_rect=rect,median_srgb=median.tolist(),rgb_gains=gains.tolist(),limitation='Assumed neutral in scene, not a calibrated gray card')
        if name in PAINT_PATCHES:
            r=tuple(round(v*factor) for v in PAINT_PATCHES[name]);x0,y0,x1,y1=r
            color=np.median(result[y0:y1,x0:x1],axis=(0,1))
            rows[name]['paint_appearance']=dict(pixel_rect=r,balanced_median_srgb_255=(color*255).tolist(),
                scope='Unlettered side panel below rub rail; displayed appearance under photographed light, not calibrated albedo')
    (out/'white-balance.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':main()
