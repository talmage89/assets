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
    plan=park(101,'old');lot=next(q for q in plan['lots'] if q['number']==1);p=lot['home']
    L,W,E,F=p['length'],p['width'],p['eave'],p['floor'];s=3888/1920
    # Fit the visible outer fascia, rather than the wall corner behind it.
    lx=L/2+.20;half=W/2+.216;top=E+.112
    corners=[((-lx,-half,top),(326,446)),((lx,-half,top),(1350,280)),
             ((L/2,-W/2,F),(1348,615)),((lx,half,top),(1750,317)),((L/2,W/2,F),(1744,616))]
    definitions={
      'single-2009':dict(asset='Park-101',photo='refs/home-2009.jpg',crop=[0,0,3888,2592],title='Used 1980s lot inside Alder Court',
        location=transform(lot,(L*.85,-L*.7,1.0)),target=transform(lot,(0,0,1.8)),lens=38,lens_bounds_mm=[20,90],
        neutral='White storm-door frame, shaded daylight; fit uses three outer-fascia corners and two exposed wall/skirt corners; obscured rear floor excluded',
        neutral_rect=[1804,990,1844,1100],landmarks=[dict(world=transform(lot,w),pixel=[x*s,y*s]) for w,(x,y) in corners])}
    lot=next(q for q in plan['lots'] if q['number']==36);h=lot['home'];assert h['room'];off=(-h['length']*.32,-h['width']/2-1.20,0)
    pts=[((-1.6,-1.2,2.95),(475,454)),((1.6,-1.2,2.95),(694,453)),
         ((-1.6,-1.2,.80),(488,674)),((1.6,-1.2,.80),(692,667)),
         ((1.6,1.2,3.20),(787,457)),((1.6,1.2,.80),(785,668))]
    definitions['street-2007']=dict(asset='Park-101',photo='refs/street-2007.jpg',crop=[0,0,1241,906],title='Occupied older row / additions and planted fronts',
      location=transform(lot,(7,-9,2.0),off),target=transform(lot,(0,0,1.7),off),lens=28,lens_bounds_mm=[12,80],
      neutral='White porch fascia around yellow addition; full photograph, not the earlier isolated addition crop',neutral_rect=[482,449,650,459],
      landmarks=[dict(world=transform(lot,w,off),pixel=p) for w,p in pts])
    # The previous room-only fit put the camera beyond the last row and
    # pointed away from the actual street. Keep its 26mm optics, but fit the
    # lane context explicitly. Longitudinal road stations are inferred;
    # this is a type/framing comparison, not a reconstruction of the site.
    lane=-plan['loop_x'];y=-plan['span']/2;half=plan['street_width']/2
    anchors=[((lane-half,y+7,.015),(255,900)),((lane+half,y+7,.015),(1220,900)),
             ((lane-half,y+16,.015),(338,712)),((lane+half,y+16,.015),(777,712))]
    definitions['street-2007']=dict(asset='Park-101',photo='refs/street-2007.jpg',crop=[0,0,1241,906],
      title='Older park lane / occupied neighbors, driveways and planted fronts',
      location=[lane,y+1,1.46],target=[lane+1,y+25,1.9],lens=25.93,lens_bounds_mm=[20,45],camera_height_m=[1.46,.30],
      neutral='White addition fascia; four inferred lane-edge stations fit street framing, not individual home construction; replaces the isolated room camera',
      neutral_rect=[482,449,650,459],landmarks=[dict(world=q,pixel=pix) for q,pix in anchors])
    lot=next(q for q in plan['lots'] if q['number']==6);h=lot['home'];off=(h['length']/2-2.9,-h['width']/2-1.82,0)
    pts=[((-3.3528,1.6764,2.68),(1337,1201)),((3.3528,1.6764,2.68),(1509,1223)),
         ((-3.3528,-1.6764,2.42),(1328,1270)),((3.3528,-1.6764,2.42),(1473,1291)),
         ((3.2228,-1.5964,.07),(1461,1318))]
    definitions['aerial-2015']=dict(asset='Park-101',photo='refs/park-2015.jpg',crop=[1000,800,1850,1450],title='Dense four-row park / above the occupied lots',
      location=transform(lot,(3,-10,14),off),target=transform(lot,(0,0,1.6),off),lens=42,lens_bounds_mm=[16,100],
      neutral='Sunlit bare aluminum pan assumed neutral; original lens unavailable; nine anchors on two adjacent carports, with the occluded left post foot excluded; fictional park is a density/type comparison',neutral_rect=[1350,1240,1460,1260],
      landmarks=[dict(world=transform(lot,w,off),pixel=p) for w,p in pts])
    neighbor=next(q for q in plan['lots'] if q['number']==7);h=neighbor['home'];off2=(h['length']/2-2.9,-h['width']/2-1.82,0)
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
      neutral='White PVC entrance-fence post, crop checked at pixel scale; four lane-edge anchors, longitudinal stations inferred from our fictional plan; does not fit individual houses or establish surveyed depth',
      neutral_rect=[265,683,269,717],landmarks=[dict(world=q,pixel=pix) for q,pix in anchors])
    results={}
    subjects={'single-2009':['Lot_01_Home'],'street-2007':['Lot_01_Home','Lot_10_Home'],
              'aerial-2015':['Lot_06_Carport','Lot_07_Carport'],'newer-row-2024':[]}
    for name,d in definitions.items():
        nodes={n.get('name') for n in json.loads(Path('export',d['asset']+'.gltf').read_text())['nodes']}
        assert set(subjects[name])<=nodes,(name,'Declared comparison subject absent from export',subjects[name])
        result=calibrate(d);result.update(asset=d['asset'],neutral=d['neutral'],neutral_rect=d['neutral_rect'],subject_nodes=subjects[name])
        result['shot']['require_visible_landmarks']=True
        if name=='newer-row-2024':result['lens_status']='24mm full-frame EXIF; bounded 23.5–24.5mm lane fit; inferred longitudinal stations'
        results[name]=result;print(name,round(result['residual_rms_pixels'],2),'px',round(result['shot']['lens'],1),'mm',flush=True)
        assert result['residual_rms_pixels']<=20,(name,result['residual_rms_pixels'])
    Path('build/cameras.json').write_text(json.dumps(results,indent=2))


def compose(folder):
    from PIL import Image,ImageOps,ImageDraw,ImageFont
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
    # Lane depth is inferred, unlike the two construction-corner fits.
    # Keep the shared compositor but make that weaker evidence explicit.
    from kit.fonts import find_font
    font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),23)
    small=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),18)
    for name in ('street-2007','newer-row-2024'):
        path=dest/(name+'-pair.jpg');im=Image.open(path).convert('RGB');draw=ImageDraw.Draw(im)
        draw.rectangle((im.width//2,0,im.width,68),fill=(238,239,236))
        draw.text((im.width//2+18,12),'Reference photograph / inferred lane framing',font=font,fill=(22,38,29))
        draw.rectangle((0,im.height-56,im.width,im.height),fill=(238,239,236))
        row=cams[name]
        label='Lane-anchor RMS %.1f px; longitudinal stations inferred / type comparison, not surveyed construction'%row['residual_rms_pixels']
        draw.text((18,im.height-42),label,font=small,fill=(49,64,52));im.save(path,quality=94,optimize=True)
