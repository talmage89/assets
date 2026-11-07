"""Fit kit cameras, verify projections, render exported geometry, pair photos."""
import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit import photo_match
from photo_matches import MATCHES,LIGHT,NEUTRALS,LENS_EVIDENCE,calibrated_match

def main():
    import bpy
    from render import render
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('renders/matches'));p.add_argument('--folder',default='export/lookdev');p.add_argument('--width',type=int,default=1000);p.add_argument('--samples',type=int,default=32);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
    import numpy as np
    from PIL import Image
    calibrated={name:calibrated_match(name) for name in MATCHES};balances={}
    for name,data in calibrated.items():
        data['lens_evidence']=LENS_EVIDENCE[name]
        data['native_horizontal_equivalent_mm']=data['shot']['lens']*LENS_EVIDENCE[name]['crop_width']/LENS_EVIDENCE[name]['full_width']
        data['lens_status']='EXIF informed; crop-equivalent rendering lens; see lens_evidence' if name!='memorial_coping' else 'bounded estimate; no EXIF'
        image=Image.open(data['photo']).convert('RGB');a0=np.asarray(image,dtype=float)/255
        lin=np.where(a0<=.04045,a0/12.92,((a0+.055)/1.055)**2.4)
        x0,y0,x1,y1=NEUTRALS[name];med=np.median(lin[y0:y1,x0:x1],axis=(0,1));gains=float(med.mean())/np.maximum(med,1e-6)
        lin=np.clip(lin*gains,0,1);col=np.where(lin<=.0031308,lin*12.92,1.055*lin**(1/2.4)-.055)
        target=Path('build')/(name+'-balanced.jpg');Image.fromarray(np.rint(col*255).astype('uint8')).save(target,quality=97)
        balances[name]=dict(neutral_roi=NEUTRALS[name],neutral='unpainted gray concrete',linear_gains=gains.tolist(),scope='Review copy only; exposure unchanged; no asset inputs')
        data['photo']=str(target)
    Path('build/reference-balance.json').write_text(json.dumps(balances,indent=2))
    path=Path('build/calibration.json');path.write_text(json.dumps(calibrated,indent=2));photo_match.verify(path)
    for name,data in calibrated.items():
        shot=data['shot'];shot.update(LIGHT[name]);shot.pop('background',None)
        render(101,a.folder,a.out,a.width,a.samples,names=[name],custom={name:shot},with_context=True)
    photo_match.compose(path,a.out,a.out)
    # The kit labels its projection lens. State the full-photo equivalent as
    # well, so a tight crop is never mistaken for a 373mm telephoto capture.
    from PIL import ImageDraw,ImageFont
    from kit.fonts import find_font
    font=ImageFont.truetype(find_font('DejaVu Sans','Book'),18)
    for name,data in calibrated.items():
        target=a.out/(name+'-pair.jpg');pair=Image.open(target).convert('RGB');d=ImageDraw.Draw(pair)
        d.rectangle((0,pair.height-56,pair.width,pair.height),fill=(238,239,236))
        kind='six identified concrete corners' if name=='burnham_street' else 'inferred lip/contour correspondences'
        caption=f"{data['native_horizontal_equivalent_mm']:.1f}mm full-photo equivalent / {data['shot']['lens']:.1f}mm crop camera; RMS {data['residual_rms_pixels']:.2f}px at {data['crop'][2]-data['crop'][0]}px photo width; {kind}"
        d.text((18,pair.height-42),caption,font=font,fill=(49,64,52));pair.save(target,quality=94,optimize=True)
    print('PHOTO FITS',json.dumps({n:d['residual_rms_pixels'] for n,d in calibrated.items()}))

if __name__=='__main__':main()
