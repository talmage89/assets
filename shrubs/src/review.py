"""Local evidence contact, value populations and current-source provenance."""
import argparse,json,sys,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.contact import contact,review_sheet
from settings import SHOTS
from photo_matches import MATCHES


def population(im):
    arr=np.asarray(im.convert('RGBA'),float)/255;r,g,b,a=np.moveaxis(arr,-1,0)
    mask=(g>r*1.18)&(g>b*1.25)&(a>.5)
    rgb=arr[:,:,:3][mask];value=rgb@np.array([.2126,.7152,.0722])
    return dict(pixels=len(value),display_luminance_p5_median_p95=np.percentile(value,[5,50,95]).tolist(),below_02_fraction=float(np.mean(value<.02)),clipped_rgb_fraction=float(np.mean(np.any(rgb>=1,axis=1))))


def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,required=True);a=p.parse_args();r=a.renders
    paths=[r/(s+'.png') for s in SHOTS];contact(paths,r/'contact.jpg',title='Boxwood / SOURCE look-dev checkpoint / procedural daylight')
    pairs=[r/(s+'-pair.jpg') for s in MATCHES];review_sheet([paths[:2],paths[2:4],[paths[4],paths[5]],[paths[6]]]+[[x] for x in pairs],r/'review-sheet.jpg',width=1800,title='Boxwood / source critique evidence; no final GLB yet')
    evidence={}
    for name,m in MATCHES.items():
        im=ImageOps.exif_transpose(Image.open(m['photo'])).crop(m['crop'])
        # Tight interior patches exclude the surrounding lawn/ivy and labels.
        rect=(125,155,510,430) if name=='match_green_velvet' else (90,120,460,320)
        evidence[name]=dict(model=population(Image.open(r/(name+'.png'))),photo_interior=population(im.crop(rect)),photo_patch_in_crop_px=rect,scope='display-image populations; differing lighting/specimens, not calibrated albedo')
    digest=hashlib.sha256((ROOT/'shrubs/build/lookdev.blend').read_bytes()).hexdigest();meta=json.loads((r/'shots.json').read_text());assert all(x['source_sha256']==digest for x in meta.values()),'stale source renders'
    (r/'tonal-check.json').write_text(json.dumps(evidence,indent=2));(r/'render-check.json').write_text(json.dumps(dict(passed=True,source_sha256=digest,render_count=len(meta),scope='source checkpoint provenance only, no export proof'),indent=2))
    print(json.dumps(evidence,indent=2))

if __name__=='__main__':main()
