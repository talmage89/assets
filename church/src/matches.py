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
    # The corner tower is on the opposite side of the reference. Mirror only
    # this comparison image, and document it; never change a model to trace it.
    im=Image.open('refs/historic-street.jpg').convert('RGB').crop((15,35,720,1009))
    ImageOps.mirror(im).save('refs/match-historic.jpg',quality=96)
    im=Image.open('refs/straight-front-28.jpg').convert('RGB').crop((160,195,1038,850))
    # Neutral: unmarked gray arrival drive, excluding curb/leaf litter.
    a=np.asarray(im).astype(float)/255;patch=a[465:477,350:450];med=np.median(patch.reshape(-1,3),axis=0);gain=med.mean()/med
    a=np.clip(a*gain,0,1);Image.fromarray(np.uint8(a*255)).save('refs/match-modern.jpg',quality=96)
    Image.open('refs/historic-entry.jpg').convert('RGB').crop((790,180,960,550)).save('refs/match-window.jpg',quality=96)
    return dict(modern_neutral_rgb=med.tolist(),modern_white_balance_gain=gain.tolist(),historic='monochrome; no chromatic balance',window='monochrome white painted siding; no chromatic balance')


def definitions():
    p=json.loads(Path('build/plan-101.json').read_text());q=json.loads(Path('build/plan-202.json').read_text())
    def point(plan,xyz):return [xyz[k]-plan['placement_offset'][k] for k in range(3)]
    def marks(plan,rows):return [dict(world=point(plan,xyz),pixel=xy) for xyz,xy in rows]
    w=p['width'];l=p['length'];tx,ty=p['tower_xy']
    classic=dict(title='Town Gothic street elevation (mirrored reference)',photo='refs/match-historic.jpg',crop=[0,0,705,974],location=point(p,(21,-64,1.72)),target=point(p,(0,-7,10)),lens=42,lens_bounds_mm=(28,85),camera_height_m=(1.72,.8),landmarks=marks(p,[
        ((-w/2,-l/2,0),(192,760)),((w/2,-l/2,0),(498,760)),
        ((-w/2,-l/2,p['eave']),(190,491)),((w/2,-l/2,p['eave']),(493,458)),
        ((0,-l/2,p['ridge']),(308,355)),
        ((tx-2.285,ty-2.285,0),(40,774)),((tx+2.285,ty-2.285,0),(180,775)),
        ((tx,ty,28.95),(112,125)),((tx-2.285,ty-2.285,17.35),(51,340)),((tx+2.285,ty-2.285,17.35),(179,348))]))
    w=q['width'];l=q['length'];e=q['eave'];h=q['ridge']
    modern=dict(title='Postwar church across its arrival drive',photo='refs/match-modern.jpg',crop=[0,0,878,655],location=point(q,(25,-58,1.72)),target=point(q,(0,0,7)),lens=42,lens_bounds_mm=(28,85),camera_height_m=(1.72,.8),landmarks=marks(q,[
        ((-w/2,-l/2,0),(51,442)),((w/2,-l/2,0),(327,448)),
        ((-w/2,-l/2,e),(76,384)),((w/2,-l/2,e),(303,388)),
        ((0,-l/2,h),(195,85)),((w/2,l/2,e),(487,402)),((w/2,l/2,0),(486,445)),((0,l/2,h),(445,268))]))
    # Compare the exported wall module: the photograph has a flat wall,
    # whereas a neighboring buttress occludes this oblique view in the nave.
    y=-.235;sill=2.30;stem=3.10;r=.70
    window=dict(title='Isolated exported wall bay: storm-protected lancet',photo='refs/match-window.jpg',crop=[0,0,170,370],location=(-12,-8,1.72),target=(0,y,4.7),lens=48,lens_bounds_mm=(28,100),camera_height_m=(1.72,1.2),landmarks=[dict(world=xyz,pixel=xy) for xyz,xy in [
        ((-r,y,sill),(86,302)),((r,y,sill),(114,303)),
        ((-r,y,sill+stem),(88,141)),((r,y,sill+stem),(117,139)),
        ((0,y,sill+stem+3**.5*r),(111,91)),
        ((-r,y,sill+1.0),(87,245)),((r,y,sill+1.0),(115,245))]])
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
