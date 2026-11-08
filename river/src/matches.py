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
    p=generate(202);l=p.length/2;y=-p.deck_width/2
    bank=definition('CO_SH_8_bridge_over_Bear_Creek,_Morrison,_CO.jpg','Bank bridge / abutment, planted slope and trail',[
        ((-l,y,5.348),.255,.310),((l,y,5.348),.772,.280),
        ((-l,y,4.13),.255,.369),((l,y,4.13),.772,.335)],
        (-1,-86,3.3),(0,0,3.1),42,height=[3.3,.8])
    # Native construction differs. Restrict anchors to the cap/column frame;
    # the photographed steel cross-bracing remains an explicit mismatch.
    p=generate(101);x=-p.span/2;half=p.deck_width/2-.3
    under=definition('under-huron.jpg','Under bridge / support frame; steel reference differs',[
        ((x-.86,half,2.687),.170,.660),((x-.86,-half,2.687),.849,.679),
        ((x-.86,half,1.887),.170,.711),((x-.86,-half,1.887),.849,.730)],
        (-24,-.4,1.65),(x,0,3.7),24,height=[1.65,1.2])
    return dict(urban=(101,urban),bank=(202,bank),under=(101,under))


def prepare():
    result={}
    neutral=dict(urban=(260,466,350,477),bank=(1140,1070,1220,1150),under=(380,582,460,610))
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
        result[name]['white_balance']=dict(original=original,neutral_patch_xyxy=neutral[name],
            assumed_neutral=['bridge concrete','trail wall concrete','pier cap concrete'][['urban','bank','under'].index(name)],
            photo_patch_rgb=med.tolist(),gains=gain.tolist())
    Path('build/photo-calibration.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PHOTO_FITS',[(k,round(v['residual_rms_pixels'],2),round(v['shot']['lens'],2)) for k,v in result.items()])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare',action='store_true');ap.add_argument('--compose',action='store_true');a=ap.parse_args()
    if a.prepare:prepare()
    if a.compose:compose('build/photo-calibration.json','renders/checkpoint-matches','renders/checkpoint-matches')


if __name__=='__main__':main()
