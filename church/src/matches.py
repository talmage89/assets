"""Explicit photographic correspondences; residuals remain visible."""
import json,sys,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.photo_match import calibrate


def prepared():
    if not Path('refs/straight-front-28.jpg').exists():
        subprocess.run(['pdftoppm','-f','28','-l','28','-scale-to','1800','-jpeg','refs/straight-aframe-nomination.pdf','refs/straight-front'],check=True)
    def balanced(file,box,out,size=None,crop=None):
        im=ImageOps.exif_transpose(Image.open(file)).convert('RGB')
        if size:im=im.resize(size,Image.Resampling.LANCZOS)
        a=np.asarray(im).astype(float)/255;x0,y0,x1,y1=box
        med=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0);gain=med.mean()/med
        im=Image.fromarray(np.uint8(np.clip(a*gain,0,1)*255+.5))
        if crop:im=im.crop(crop)
        im.save(out,quality=97)
        return dict(neutral_patch=box,neutral_rgb=med.tolist(),gain=gain.tolist(),crop=crop,prepared_size=im.size)
    # Period color photograph, not mirrored. Neutral: the concrete sidewalk
    # at lower right, away from grass, asphalt, red brick and cast shadows.
    historic=balanced('refs/color-columbus.jpg',(360,925,420,934),'refs/match-historic.jpg',(1000,960))
    im=Image.open('refs/straight-front-28.jpg').convert('RGB').crop((160,195,1038,850))
    # Neutral: unmarked gray arrival drive, excluding curb/leaf litter.
    a=np.asarray(im).astype(float)/255;patch=a[465:477,350:450];med=np.median(patch.reshape(-1,3),axis=0);gain=med.mean()/med
    a=np.clip(a*gain,0,1);Image.fromarray(np.uint8(a*255)).save('refs/match-modern.jpg',quality=96)
    # Brick tower lancet, with exterior protective sheet/bar and deep reflection.
    # Keep native photo pixels in this close comparison; concrete is in the
    # whole frame and supplies the balance before the window crop is taken.
    window=balanced('refs/color-dayton.jpg',(1371,3468,1589,3494),'refs/match-window.jpg',crop=(806,2218,1109,2822))
    return dict(modern_neutral_rgb=med.tolist(),modern_white_balance_gain=gain.tolist(),historic=historic,window=window)


def definitions():
    p=json.loads(Path('build/plan-101.json').read_text());q=json.loads(Path('build/plan-202.json').read_text())
    def point(plan,xyz):return [xyz[k]-plan['placement_offset'][k] for k in range(3)]
    def marks(plan,rows):return [dict(world=point(plan,xyz),pixel=xy) for xyz,xy in rows]
    w=p['width'];l=p['length'];tx,ty=p['tower_xy']
    classic=dict(title='Period brick Gothic church across its street',photo='refs/match-historic.jpg',crop=[0,0,1000,960],location=point(p,(-20,-65,1.72)),target=point(p,(0,-9,12)),lens=42,lens_bounds_mm=(20,85),camera_height_m=(1.72,.8),landmarks=marks(p,[
        ((-w/2,-l/2,0),(500,888)),((w/2,-l/2,0),(790,899)),
        ((-w/2,-l/2,p['eave']),(503,659)),((w/2,-l/2,p['eave']),(790,676)),
        ((0,-l/2,p['ridge']),(650,479)),
        ((tx-2.285,ty-2.285,0),(372,892)),((tx+2.285,ty-2.285,0),(500,895)),
        ((tx,ty,28.95),(418,23))]))
    w=q['width'];l=q['length'];e=q['eave'];h=q['ridge']
    modern=dict(title='Postwar church across its arrival drive',photo='refs/match-modern.jpg',crop=[0,0,878,655],location=point(q,(25,-58,1.72)),target=point(q,(0,0,7)),lens=42,lens_bounds_mm=(28,85),camera_height_m=(1.72,.8),landmarks=marks(q,[
        ((-w/2,-l/2,0),(51,442)),((w/2,-l/2,0),(327,448)),
        ((-w/2,-l/2,e),(76,384)),((w/2,-l/2,e),(303,388)),
        ((0,-l/2,h),(195,85)),((w/2,l/2,e),(487,402)),((w/2,l/2,0),(486,445)),((0,l/2,h),(445,268))]))
    # Compare the exported wall module: the photograph has a flat wall,
    # whereas a neighboring buttress occludes this oblique view in the nave.
    y=-.235;sill=2.30;stem=3.10;r=.70
    window=dict(title='Brick lancet and protective glazing',photo='refs/match-window.jpg',crop=[0,0,303,604],location=(4,-9,1.72),target=(0,y,4.6),lens=48,lens_bounds_mm=(20,160),camera_height_m=(1.72,1),landmarks=[dict(world=xyz,pixel=(xy[0]*3.36-806,xy[1]*3.36-2218)) for xyz,xy in [
        ((-r,y,sill),(267,813)),((r,y,sill),(297,806)),
        ((-r,y,sill+stem),(268,714)),((r,y,sill+stem),(301,707)),
        ((0,y,sill+stem+3**.5*r),(285,688))]])
    return dict(gothic=classic,modern=modern,window=window)


def main():
    balance=prepared();defs=definitions();out={}
    for name,row in defs.items():
        fit=calibrate(row);fit['source']=f'export/ChurchSite-{202 if name=="modern" else 101}.gltf';fit['seed']=202 if name=='modern' else 101
        if name=='window':
            fit['source']='export/modules/WallBay.gltf';fit['shot']['source_module']='WallBay'
        # Sites restore the nave datum to its town position. Apply that same
        # translation to camera and landmarks, preserving the fitted pixels.
        offset=[0,0,0] if name=='window' else json.loads(Path(f'build/plan-{fit["seed"]}.json').read_text())['placement_offset']
        for key in ('location','target'):fit['shot'][key]=[a+b for a,b in zip(fit['shot'][key],offset)]
        fit['landmarks_world_m']=[[a+b for a,b in zip(p,offset)] for p in fit['landmarks_world_m']]
        fit['shot']['exposure']=.15;fit['shot']['aspect']=(row['crop'][2]-row['crop'][0])/(row['crop'][3]-row['crop'][1])
        fit['limitations']='Different original building; landmark fit is a framing comparison, not a survey or style identity.'
        out[name]=fit;print(name,'RMS',round(fit['residual_rms_pixels'],2),'px; lens',round(fit['shot']['lens'],2),'mm')
    Path('build/matched-cameras.json').write_text(json.dumps(out,indent=2));Path('build/photo-balance.json').write_text(json.dumps(balance,indent=2))


if __name__=='__main__':main()
