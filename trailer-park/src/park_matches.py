"""Photographed lots compared inside the complete exported communities.

Named visible construction landmarks fit the camera, never the mesh. RMS is
for those anchors, not a claim that the fictional park duplicates the photo.
"""
import json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from plans import park
from kit.photo_match import calibrate


def transform(row,point,offset=(0,0,0)):
    t=math.radians(row['yaw']);x,y,z=[point[i]+offset[i] for i in range(3)]
    return [row['origin'][0]+x*math.cos(t)-y*math.sin(t),row['origin'][1]+x*math.sin(t)+y*math.cos(t),z]


def solve():
    plan=park(101,'old');lot=next(q for q in plan['lots'] if q['number']==3);p=lot['home']
    L,W,E,F=p['length'],p['width'],p['eave'],p['floor'];s=3888/1920
    corners=[((-L/2,-W/2,E),(326,446)),((L/2,-W/2,E),(1350,280)),
             ((L/2,-W/2,F),(1348,615)),((L/2,W/2,E),(1750,317)),((L/2,W/2,F),(1744,616))]
    definitions={
      'single-2009':dict(asset='Park-101',photo='refs/home-2009.jpg',crop=[0,0,3888,2592],title='Used 1980s lot inside Alder Court',
        location=transform(lot,(L*.85,-L*.7,1.0)),target=transform(lot,(0,0,1.8)),lens=38,lens_bounds_mm=[20,90],
        neutral='White storm-door frame, shaded daylight; geometry fit uses five visible wall-line corners; obscured rear floor and old erroneous ridge anchor excluded',
        neutral_rect=[1804,990,1844,1100],landmarks=[dict(world=transform(lot,w),pixel=[x*s,y*s]) for w,(x,y) in corners])}
    lot=next(q for q in plan['lots'] if q['number']==5);h=lot['home'];off=(-h['length']*.32,-h['width']/2-1.20,0)
    pts=[((-1.6,-1.2,2.95),(479,454)),((1.6,-1.2,2.95),(651,456)),
         ((-1.6,-1.2,.80),(488,674)),((1.6,-1.2,.80),(651,670)),
         ((1.6,1.2,3.20),(787,457)),((1.6,1.2,.80),(785,668))]
    definitions['street-2007']=dict(asset='Park-101',photo='refs/street-2007.jpg',crop=[0,0,1241,906],title='Occupied older row / additions and planted fronts',
      location=transform(lot,(7,-9,2.0),off),target=transform(lot,(0,0,1.7),off),lens=28,lens_bounds_mm=[12,80],
      neutral='White porch fascia around yellow addition; full photograph, not the earlier isolated addition crop',neutral_rect=[482,449,650,459],
      landmarks=[dict(world=transform(lot,w,off),pixel=p) for w,p in pts])
    lot=next(q for q in plan['lots'] if q['number']==2);h=lot['home'];off=(h['length']/2-2.9,-h['width']/2-1.82,0)
    pts=[((-3.3528,1.6764,2.68),(1337,1201)),((3.3528,1.6764,2.68),(1509,1223)),
         ((-3.3528,-1.6764,2.42),(1328,1270)),((3.3528,-1.6764,2.42),(1473,1291)),
         ((-3.2228,-1.5964,.07),(1329,1292)),((3.2228,-1.5964,.07),(1461,1318))]
    definitions['aerial-2015']=dict(asset='Park-101',photo='refs/park-2015.jpg',crop=[1000,800,1850,1450],title='Dense four-row park / above the occupied lots',
      location=transform(lot,(3,-10,14),off),target=transform(lot,(0,0,1.6),off),lens=42,lens_bounds_mm=[16,100],
      neutral='Sunlit bare aluminum pan assumed neutral; original lens unavailable; ten anchors on two adjacent carports; fictional park is a density/type comparison',neutral_rect=[1350,1240,1460,1260],
      landmarks=[dict(world=transform(lot,w,off),pixel=p) for w,p in pts])
    neighbor=next(q for q in plan['lots'] if q['number']==3);h=neighbor['home'];off2=(h['length']/2-2.9,-h['width']/2-1.82,0)
    for world,pixel in [((-3.3528,1.6764,2.68),(1455,1104)),((3.3528,1.6764,2.68),(1610,1120)),
                        ((-3.3528,-1.6764,2.42),(1410,1165)),((3.3528,-1.6764,2.42),(1562,1191))]:
        definitions['aerial-2015']['landmarks'].append(dict(world=transform(neighbor,world,off2),pixel=pixel))
    newer=park(202,'new');x=-newer['loop_x'];w=newer['street_width'];y=-newer['span']/2
    # Supplement the home/addition/pan fits with the newer occupied lane.
    # Longitudinal stations are inferred from our plan, not surveyed photo
    # dimensions. Four coplanar edges constrain this perspective comparison.
    anchors=[((x-w/2,y+17,.016),(477,745)),((x+w/2,y+17,.016),(826,741)),
             ((x-w/2,-y-15,.016),(617,654)),((x+w/2,-y-15,.016),(666,654))]
    definitions['newer-row-2024']=dict(asset='Park-202',photo='refs/newer-row-2024.jpg',crop=[0,0,1280,873],
      title='Newer occupied lane / planted fronts and summer turf',location=[x,y-3,1.68],target=[x,y+45,14],
      lens=24,lens_bounds_mm=[23.5,24.5],camera_height_m=[1.68,.15],
      neutral='Sunlit white entrance fence; four lane-edge anchors, longitudinal stations inferred from our fictional plan; does not fit individual houses or establish surveyed depth',
      neutral_rect=[200,687,250,692],landmarks=[dict(world=q,pixel=pix) for q,pix in anchors])
    results={}
    for name,d in definitions.items():
        result=calibrate(d);result.update(asset=d['asset'],neutral=d['neutral'],neutral_rect=d['neutral_rect'])
        if name=='newer-row-2024':result['lens_status']='24mm full-frame EXIF; bounded 23.5–24.5mm lane fit; inferred longitudinal stations'
        results[name]=result;print(name,round(result['residual_rms_pixels'],2),'px',round(result['shot']['lens'],1),'mm',flush=True)
        assert result['residual_rms_pixels']<=20,(name,result['residual_rms_pixels'])
    Path('build/cameras.json').write_text(json.dumps(results,indent=2))


def compose(folder):
    from PIL import Image,ImageOps
    import numpy as np
    from kit.photo_match import compose as pairs
    from kit.image_io import srgb_to_linear,linear_to_srgb
    cams=json.loads(Path('build/cameras.json').read_text());folder=Path(folder);dest=folder/'matches';dest.mkdir(parents=True,exist_ok=True);balanced={}
    for name,row in cams.items():
        im=ImageOps.exif_transpose(Image.open(row['photo'])).convert('RGB');rgb=np.asarray(im).astype(float)/255
        linear=srgb_to_linear(rgb);x0,y0,x1,y1=row['neutral_rect'];neutral=linear[y0:y1,x0:x1].mean(axis=(0,1));gains=neutral.mean()/neutral
        path=dest/(name+'-balanced.jpg');Image.fromarray(np.round(np.clip(linear_to_srgb(linear*gains),0,1)*255).astype('uint8')).save(path,quality=96)
        copied=dict(row,photo=str(path),linear_neutral_gain=gains.tolist());balanced[name]=copied
        (dest/(name+'.png')).write_bytes((dest/row['asset']/(name+'.png')).read_bytes())
    calibration=dest/'comparison-cameras.json';calibration.write_text(json.dumps(balanced,indent=2));pairs(calibration,dest,dest)
