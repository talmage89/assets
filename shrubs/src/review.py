"""Local evidence contact, value populations and current-source provenance."""
import argparse,json,sys,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
import colorsys
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.contact import contact,review_sheet
from settings import SHOTS,HYDRANGEA_SHOTS
from photo_matches import MATCHES


def population(im):
    arr=np.asarray(im.convert('RGBA'),float)/255;r,g,b,a=np.moveaxis(arr,-1,0)
    mask=(g>r*1.18)&(g>b*1.25)&(a>.5)
    rgb=arr[:,:,:3][mask];value=rgb@np.array([.2126,.7152,.0722])
    hsv=np.array([colorsys.rgb_to_hsv(*c) for c in rgb]);hue=float(np.median(hsv[:,0])*360)
    return dict(pixels=len(value),hue_degrees_median=hue,median_rgb=np.median(rgb,axis=0).tolist(),display_luminance_p5_median_p95=np.percentile(value,[5,50,95]).tolist(),below_02_fraction=float(np.mean(value<.02)),clipped_rgb_fraction=float(np.mean(np.any(rgb>=1,axis=1))))


def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,required=True);p.add_argument('--species',choices=['boxwood','hydrangea'],default='boxwood');a=p.parse_args();r=a.renders
    matches=MATCHES
    if a.species=='hydrangea':
        from hydrangea_matches import MATCHES as matches
    shots=HYDRANGEA_SHOTS if a.species=='hydrangea' else SHOTS
    label=a.species.title()
    paths=[r/(s+'.png') for s in shots];pairs=[r/(s+'-pair.jpg') for s in matches]
    contact(paths+pairs,r/'contact.jpg',title=label+' / SOURCE look-dev checkpoint / procedural daylight')
    review_sheet([paths[:2],paths[2:4],[paths[4],paths[5]],[paths[6]]]+[[x] for x in pairs],r/'review-sheet.jpg',width=1800,title=label+' / source critique evidence; no final GLB yet')
    from values import measure,BOX_PATCHES
    if a.species=='hydrangea':
        from hydrangea_matches import PATCHES
        calibration=ROOT/'shrubs/build/hydrangea/framed-cameras.json'
    else:
        PATCHES={k:dict(crop=matches[k]['crop'],**v) for k,v in BOX_PATCHES.items()}
        calibration=ROOT/'shrubs/build/framed-cameras.json'
    evidence=measure(r,calibration,PATCHES)
    digest=hashlib.sha256((ROOT/('shrubs/build/hydrangea/lookdev.blend' if a.species=='hydrangea' else 'shrubs/build/lookdev.blend')).read_bytes()).hexdigest();meta=json.loads((r/'shots.json').read_text());assert all(x['source_sha256']==digest for x in meta.values()),'stale source renders'
    (r/'tonal-check.json').write_text(json.dumps(evidence,indent=2));(r/'render-check.json').write_text(json.dumps(dict(passed=True,source_sha256=digest,render_count=len(meta),scope='source checkpoint provenance only, no export proof'),indent=2))
    print(json.dumps(evidence,indent=2))

if __name__=='__main__':main()
