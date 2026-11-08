"""Three independent photographed form comparisons via kit's camera solver.

Photo landmarks are manually inspected; no tracing or photographic materials.
Original forms compare a construction type, not the photographed property.
"""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from plans import home
from kit.photo_match import calibrate


def solve():
    h=home(147,'1984',14,70);L,W,E,F=h['length'],h['width'],h['eave'],h['floor']
    # Photo shown in the review at 1920; original is 3888 wide.
    s=3888/1920
    definitions={
      'single-2009':dict(asset='SingleWide-147',photo='refs/home-2009.jpg',crop=[0,0,3888,2592],title='Used single-wide / side-entry construction',
        location=[L*.85,-L*.70,2.2],target=[0,0,1.8],lens=38,lens_bounds_mm=[24,80],camera_height_m=[1.8,.5],neutral='Nominal white aluminum storm-door frame; shaded daylight, not blue siding',
        landmarks=[dict(world=w,pixel=[x*s,y*s],weight=wt) for w,(x,y),wt in [
          ((L/2,-W/2,E),(1349,278),1),((-L/2,-W/2,E),(326,439),1),
          ((L/2,-W/2,F),(1342,615),1),((-L/2,-W/2,F),(326,681),.25),
          ((L/2,W/2,E),(1787,281),1),((L/2,W/2,F),(1752,617),1),
          ((L/2,0,E+.10+(W/2+.12)*h['pitch']),(1497,155),.6)]]),
      'addition-2007':dict(asset='AddedRoom',photo='refs/street-2007.jpg',crop=[420,380,850,755],title='Older park / independently supported added room',
        location=[7,-9,2.0],target=[0,0,1.7],lens=48,lens_bounds_mm=[28,100],neutral='White porch fascia around the yellow addition; original image already color balanced by uploader',
        landmarks=[dict(world=w,pixel=p) for w,p in [
          ((-1.6,-1.2,2.95),(479,454)),((1.6,-1.2,2.95),(651,456)),
          ((-1.6,-1.2,.80),(488,674)),((1.6,-1.2,.80),(651,670)),
          ((1.6,1.2,3.20),(787,457)),((1.6,1.2,.80),(785,668))]]),
      'carport-2015':dict(asset='Carport',photo='refs/park-2015.jpg',crop=[1240,1150,1580,1370],title='Installed aluminum carport / pans and support spacing',
        location=[3,-10,14],target=[0,0,1.6],lens=48,lens_bounds_mm=[28,100],neutral='Bare aluminum sunlit pan, assumed near neutral; evaluate form separately from cool sky reflection',
        landmarks=[dict(world=w,pixel=p) for w,p in [
          ((-3.3528,1.6764,2.68),(1337,1201)),((3.3528,1.6764,2.68),(1509,1223)),
          ((-3.3528,-1.6764,2.42),(1328,1270)),((3.3528,-1.6764,2.42),(1473,1291)),
          ((-3.2228,-1.5964,.07),(1329,1292)),((3.2228,-1.5964,.07),(1461,1318))]])}
    results={}
    for name,d in definitions.items():
        result=calibrate(d);result['asset']=d['asset'];result['neutral']=d['neutral'];results[name]=result
        print(name,round(result['residual_rms_pixels'],2),'px',round(result['shot']['lens'],1),'mm',flush=True)
    Path('build/cameras.json').write_text(json.dumps(results,indent=2))


def compose(folder):
    from PIL import Image,ImageOps
    import numpy as np
    from kit.photo_match import compose as pairs
    cams=json.loads(Path('build/cameras.json').read_text());folder=Path(folder);dest=folder/'matches';dest.mkdir(parents=True,exist_ok=True)
    balanced={}
    for name,row in cams.items():
        # Images stay local. Same geometry/camera on both sides; render remains
        # an imported export. Neutral assumption is recorded for each photo.
        im=ImageOps.exif_transpose(Image.open(row['photo'])).convert('RGB');rgb=np.asarray(im).astype(float)/255
        rect={'single-2009':(1804,990,1844,1100),'addition-2007':(482,449,650,459),'carport-2015':(1350,1240,1460,1260)}[name]
        x0,y0,x1,y1=rect;neutral=rgb[y0:y1,x0:x1].mean(axis=(0,1));gains=neutral.mean()/neutral
        value=np.clip(rgb*gains,0,1)
        path=dest/(name+'-balanced.jpg');Image.fromarray(np.round(value*255).astype('uint8')).save(path,quality=96)
        copied=dict(row);copied['photo']=str(path);copied['neutral_rect_pixels']=rect;copied['rgb_neutral_gain']=gains.tolist();balanced[name]=copied
        src=dest/row['asset']/(name+'.png')
        (dest/(name+'.png')).write_bytes(src.read_bytes())
    calibration=dest/'comparison-cameras.json';calibration.write_text(json.dumps(balanced,indent=2));pairs(calibration,dest,dest)


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='compose':compose(sys.argv[2])
    else:solve()
