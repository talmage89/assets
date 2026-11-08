"""Measured-landmark type comparisons via kit.photo_match, never photo textures.

Different original buildings retain architectural differences; residuals and
neutral gains remain visible. These fits do not claim surveyed reconstruction.
"""
import argparse
import json
from pathlib import Path
import sys
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT))
from kit import photo_match
from kit.image_io import srgb_to_linear,linear_to_srgb
from plan import FLOOR,TEE


def definitions():
    p=json.loads(Path('build/garage-101.json').read_text());L,W=p['length'],p['width'];x=p['ramp_limits'][0];y=0
    def lm(world,pixel):return dict(world=world,pixel=pixel)
    return dict(
      precast=dict(seed=101,title='Precast corbel and tee underside / 2014 photograph',photo='refs/precast-interior.jpg',crop=[0,0,3264,2448],
        neutral=[1395,1504,1445,1509],neutral_description='Narrow unprinted top border of the column sign, clear of the red field and fixing; neutral paper in shade',
        location=[x-1.5,y-2.5,1.45],target=[x,y,1.7],lens=33,lens_bounds_mm=[30,36],camera_height_m=[1.5,.4],
        landmarks=[lm([x-.361,y-.381,0],[1175,2417]),lm([x+.361,y-.381,0],[1735,2352]),
          lm([x-.361,y-.381,FLOOR-1.60],[1180,1255]),lm([x+.361,y-.381,FLOOR-1.60],[1735,1210])]),
      pleasant=dict(seed=101,title='Open precast facade / 2007 photograph',photo='refs/pleasant-hill.jpg',crop=[0,0,1600,814],
        neutral=[1276,599,1332,621],neutral_description='Pale temporary site enclosure panel, shaded, used as approximate neutral',
        location=[-48,-68,1.65],target=[0,-W/2,5],lens=38,lens_bounds_mm=[18,90],camera_height_m=[1.65,.10],
        landmarks=[lm([-L/2,-W/2,1.08],[466,631]),lm([L/2,-W/2,1.08],[1467,643]),
          lm([-L/2,-W/2,3*FLOOR+1.08],[466,208]),lm([L/2,-W/2,3*FLOOR+1.08],[1467,532]),
          lm([-L/2,-W/2,2*FLOOR+1.08],[466,346]),lm([L/2,-W/2,2*FLOOR+1.08],[1467,566])]),
      harmon=dict(seed=202,title='Flat-deck opening rhythm / 2005 garage photographed 2012',photo='refs/harmon.jpg',crop=[1450,450,3420,2170],
        neutral=[2110,1730,2175,1760],neutral_description='Broad sunlit concrete spandrel face below the rail, approximate neutral mineral surface',
        location=[-35,-32,1.65],target=[0,-12.8,4],lens=40,lens_bounds_mm=[18,120],camera_height_m=[1.65,.10],
        landmarks=[lm([-14.63,-12.8016,1.09],[1565,2040]),lm([14.63,-12.8016,1.09],[3280,2010]),
          lm([-14.63,-12.8016,2*FLOOR+1.09],[1565,735]),lm([14.63,-12.8016,2*FLOOR+1.09],[3280,1650]),
          lm([-14.63,-12.8016,FLOOR+1.09],[1565,1380]),lm([14.63,-12.8016,FLOOR+1.09],[3280,1830])]))


def solve():
    folder=Path('build/matches');folder.mkdir(parents=True,exist_ok=True);results={};balance={}
    for name,row in definitions().items():
        im=ImageOps.exif_transpose(Image.open(row['photo'])).convert('RGB');array=np.asarray(im,dtype=float)/255
        x0,y0,x1,y1=row['neutral'];linear=srgb_to_linear(array);median=np.median(linear[y0:y1,x0:x1],axis=(0,1));gain=np.mean(median)/np.maximum(median,1e-5)
        assert np.all((gain>.5)&(gain<2)),('Inspect the neutral ROI for colored contamination',name,gain.tolist())
        # Photo balance is a local analysis product, not part of the asset.
        balanced=np.clip(linear_to_srgb(np.clip(linear*gain,0,1)),0,1)
        photo=folder/(name+'-balanced.jpg');Image.fromarray(np.rint(balanced*255).astype('uint8')).save(photo,quality=96)
        match={**row,'photo':str(photo)};fit=photo_match.calibrate(match);fit['seed']=row['seed'];fit['neutral']=row['neutral'];fit['gains_linear_rgb']=gain.tolist();results[name]=fit
        balance[name]=dict(photo=row['photo'],roi=row['neutral'],basis=row['neutral_description'],gain=gain.tolist(),limitation='No gray card, exposure or light spectrum was measured; this is an approximate white balance, not an inverse albedo solution.')
    (folder/'calibration.json').write_text(json.dumps(results,indent=2)+'\n');(folder/'balance.json').write_text(json.dumps(balance,indent=2)+'\n')
    for name,r in results.items():print('FIT',name,r['shot']['lens'],r['residual_rms_pixels'])


def render_matches(args,render_shot,lighting):
    import bpy
    photo_match.verify('build/matches/calibration.json')
    receipts=[]
    for name,fit in json.loads(Path('build/matches/calibration.json').read_text()).items():
        bpy.ops.wm.read_factory_settings(use_empty=True);seed=fit['seed'];path=Path(f'export/sites/ParkingGarageSite-{seed}.gltf')
        bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
        # Photographer stands in a clear reservation. Preserve the garage;
        # locally hide only context cars overlapping this calibrated viewpoint.
        from mathutils import Vector
        eye=Vector(fit['shot']['location']);hidden=[]
        for root in list(bpy.context.scene.objects):
            if not root.name.startswith(('Parked ','Street parked ')):continue
            if root.parent and root.parent.name.startswith(('Parked ','Street parked ')):continue
            if (root.matrix_world.translation-eye).xy.length<3.5:
                hidden.append(root.name)
                for ob in [root,*root.children_recursive]:ob.hide_render=True
        lighting(elevation=36 if name!='precast' else 20,azimuth=-120 if name!='pleasant' else 145,interior=name=='precast')
        if name=='precast':bpy.context.scene.view_settings.exposure=1.3
        shot=fit['shot'];shot['aspect']=(fit['crop'][2]-fit['crop'][0])/(fit['crop'][3]-fit['crop'][1])
        receipt=render_shot(args.out/(name+'.png'),shot,args.width,args.samples,args.engine,source=path);receipt['camera_clearance_hidden_context_cars']=hidden;receipts.append(receipt)
    (args.out/'views.json').write_text(json.dumps(receipts,indent=2)+'\n')


def main():
    a=argparse.ArgumentParser();a.add_argument('--compose',action='store_true');a=a.parse_args()
    if a.compose:
        photo_match.compose('build/matches/calibration.json','renders/matches','renders/matches')
        from kit.contact import review_sheet
        review_sheet([[p] for p in sorted(Path('renders/matches').glob('*-pair.jpg'))],Path('renders/matches/contact.jpg'),width=2200,title='Three exported-glTF photographic type comparisons')
    else:solve()


if __name__=='__main__':main()
