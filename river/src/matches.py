"""Measured feature cameras and honest type comparisons using kit.photo_match.

Photographs never enter Blender. Fitting small landmark sets does not survey
the real crossings. Under-Huron is steel and wider; this remains disclosed.
"""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
from kit.photo_match import calibrate,compose
from plan import generate


def definition(photo,title,landmarks,loc,target,lens=40,height=None):
    im=Image.open(Path('refs')/photo);w,h=im.size
    d=dict(photo=str(Path('refs')/photo),title=title,crop=[0,0,w,h],location=loc,target=target,
           lens=lens,lens_bounds_mm=[18,100],landmarks=[dict(world=v,pixel=[u*w,t*h]) for v,u,t in landmarks])
    if height:d['camera_height_m']=height
    return d


def definitions():
    p=generate(101);l=p.length/2;y=-p.deck_width/2;top=p.deck_z+.898144
    urban=definition('Raisinriver.jpg','Town river / brick backs and three spans',[
        ((-l,y,top),.137,.774),((l,y,top),.611,.769),
        ((-l,y,4.13),.139,.815),((l,y,4.13),.615,.807),
        ((-p.span/2,y,0),.264,.839),((p.span/2,y,0),.471,.837)],
        (3,-110,3.5),(0,0,2.4),42,height=[4.3,.6])
    urban['lens_bounds_mm']=[32,70]
    p=generate(202)
    shores=[]
    for y,left,right in ((42,(.03,.68),(.94,.70)),(76,(.20,.44),(.91,.43))):
        l,r=p.water_edges(y)
        shores += [((l,y,p.water_z(y)),*left),((r,y,p.water_z(y)),*right)]
    bank=definition('riverside-2008.jpg','Town park bank and water / autumn reference; dock differs',shores,
        (15,-45,11),(p.center(130),130,0),99)
    bank['lens_bounds_mm']=[98.5,99.5]
    # Native construction differs. Restrict anchors to the cap/column frame;
    # the photographed steel cross-bracing remains an explicit mismatch.
    p=generate(101);x=-p.span/2;half=p.deck_width/2-.3
    cap_top=p.deck_z-.32-1.143-.30
    # Native bent cap is 2.30m wide, 1.10m deep, with 50mm chamfers.
    # Use its actual upper/lower chamfer endpoints after height adaptation.
    under=definition('under-huron.jpg','Under bridge / support frame; steel reference differs',[
        ((x-1.10,half,cap_top),.170,.660),((x-1.10,-half,cap_top),.849,.679),
        ((x-1.10,half,cap_top-1.10),.170,.711),((x-1.10,-half,cap_top-1.10),.849,.730)],
        (-24,-.4,2.15),(x,0,3.7),24,height=[2.15,.25])
    return dict(urban=(101,urban),bank=(202,bank),under=(101,under))


def prepare():
    result={}
    neutral=dict(urban=(260,466,350,477),bank=(1660,857,1740,865),under=(380,582,460,610))
    Path('build/photo-balanced').mkdir(parents=True,exist_ok=True)
    for name,(seed,d) in definitions().items():
        original=d['photo'];im=ImageOps.exif_transpose(Image.open(original)).convert('RGB')
        patch=np.asarray(im.crop(neutral[name]),dtype=float)/255
        med=np.median(patch.reshape(-1,3),axis=0);gain=np.exp(np.log(np.maximum(med,.01)).mean())/med
        gain=np.clip(gain,.7,1.3)
        balanced=Path('build/photo-balanced')/(name+'.png')
        Image.fromarray(np.uint8(np.clip(np.asarray(im)*gain,0,255))).save(balanced)
        d['photo']=str(balanced)
        result[name]=calibrate(d);result[name]['seed']=seed
        # Original photographs remain untouched. The neutral gains are
        # recorded separately from the fitted geometry and not baked into art.
        result[name]['construction_status']='type comparison, not reconstruction'
        result[name]['shot']['exposure']=1.0 if name=='under' else -.4
        if name=='under':result[name]['reference_optics']='18mm EXIF on APS-C Canon Rebel T3i; fit uses a 36mm sensor and authored narrower bridge'
        if name=='bank':result[name]['reference_optics']='99mm equivalent in EXIF; fit estimates the authored channel scale, not a surveyed park replica'
        result[name]['white_balance']=dict(original=original,neutral_patch_xyxy=neutral[name],
            assumed_neutral=['bridge concrete','weathered gray dock decking','pier cap concrete'][['urban','bank','under'].index(name)],
            photo_patch_rgb=med.tolist(),gains=gain.tolist())
    Path('build/photo-calibration.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PHOTO_FITS',[(k,round(v['residual_rms_pixels'],2),round(v['shot']['lens'],2)) for k,v in result.items()])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare',action='store_true');ap.add_argument('--compose',action='store_true');a=ap.parse_args()
    if a.prepare:prepare()
    if a.compose:compose('build/photo-calibration.json','renders/checkpoint-matches','renders/checkpoint-matches')


if __name__=='__main__':main()
