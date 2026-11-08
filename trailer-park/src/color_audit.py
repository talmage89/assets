"""Concrete-balanced reference values; comparison evidence, never textures."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import srgb_to_linear,linear_to_srgb


def main():
    out=Path('build/color-audit');out.mkdir(parents=True,exist_ok=True);rows={}
    definitions={'home-2009':dict(neutral=[1420,2330,1540,2410],lawn=[3500,2320,3650,2400],
                                  description='weathered foreground concrete apron / sparse dry grass at its edge'),
                 'park-2015':dict(neutral=[890,1160,948,1180],lawn=[130,1010,170,1040],
                                  description='sunlit concrete pad in southwest crop / turf between neighboring homes')}
    for name,row in definitions.items():
        rgb=np.asarray(Image.open('refs/'+name+'.jpg').convert('RGB'),float)/255;linear=srgb_to_linear(rgb)
        x0,y0,x1,y1=row['neutral'];neutral=linear[y0:y1,x0:x1].mean((0,1));gain=neutral.mean()/neutral
        balanced=linear*gain;x0,y0,x1,y1=row['lawn'];grass=balanced[y0:y1,x0:x1].mean((0,1))
        row.update(linear_wb_gain=gain.tolist(),linear_grass_mean=grass.tolist(),grass_to_concrete_luminance=float(grass@np.array([.2126,.7152,.0722])/neutral.mean()))
        image=np.uint8(np.clip(linear_to_srgb(balanced),0,1)*255+.5);Image.fromarray(image).save(out/(name+'-concrete-balanced.jpg'),quality=95)
        rows[name]=row
    (out/'values.json').write_text(json.dumps(dict(scope='Assumed neutral concrete, display-reference luminance only; different exposure/sun/shade is not measured albedo',photos=rows),indent=2))
    print(json.dumps(rows,indent=2))


if __name__=='__main__':main()
