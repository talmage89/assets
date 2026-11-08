"""Export provenance, tonal measurements and ignored final contact sheets."""
from pathlib import Path
import math,hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1]
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),18)
def signature(path):
    inputs=[path]
    if path.suffix=='.gltf':
        d=json.loads(path.read_text());inputs += [path.parent/r['uri'] for k in ['buffers','images'] for r in d[k]]
        return hashlib.sha256(b''.join(hashlib.sha256(p.read_bytes()).digest() for p in inputs)).hexdigest()
    return hashlib.sha256(path.read_bytes()).hexdigest()
def sheet(paths,out,cols=3,w=520,h=370):
    im=Image.new('RGB',(cols*w,math.ceil(len(paths)/cols)*h),(231,232,226));d=ImageDraw.Draw(im)
    for i,p in enumerate(paths):
        tile=Image.open(p).convert('RGB');tile.thumbnail((w-16,h-42));x=(i%cols)*w;y=(i//cols)*h
        label='Eevee hero' if p.parent.name=='eevee' else p.stem
        im.paste(tile,(x+(w-tile.width)//2,y+29+(h-42-tile.height)//2));d.text((x+10,y+6),label,font=FONT,fill=(25,30,27))
    im.save(out,quality=92,optimize=True)
def main():
    folder=BASE/'renders/final';paths=[folder/(n+'.png') for n in ['hero','original_hero','front','side','rear','top','rear_three_quarter','front_detail','lamp_detail','hood_surface','entrance','interior','aisle','aisle_daylight','side_interior','warning','emergency','roof','wheels','scale','fleet']]
    source=BASE/'export/C75-101.gltf';digest=signature(source)
    calibration=json.loads((BASE/'build/calibration.json').read_text())
    receipts=json.loads((folder/'provenance.json').read_text())
    for p in paths:
        r=receipts[p.stem]
        if r['stage']!='export' or r['engine']!='CYCLES' or r['sha256']!=digest:raise ValueError('Stale or non-exported checkpoint view: '+p.stem)
    if set(receipts['fleet']['fleet_inputs'])!={'101','102','103'}:raise ValueError('Missing fleet exports')
    for seed in [101,102,103]:
        if receipts['fleet']['fleet_inputs'][str(seed)]!=signature(BASE/f'export/C75-{seed}.gltf'):raise ValueError('Stale fleet seed')
    poses={name:{'Entrance_front':95,'Entrance_rear':95} for name in ['entrance','interior','aisle','aisle_daylight']}
    poses.update(warning={'Stop_arm':90,'Crossing_arm':90},emergency={'Emergency_rear':100},roof={'Roof_hatch_front':65,'Roof_hatch_rear':65})
    for view,nodes in poses.items():
        for node,angle in nodes.items():
            actual=receipts[view]['posed_nodes'].get(node,{}).get('rotation_delta_degrees',0)
            if abs(actual-angle)>.01:raise ValueError(f'Incorrect evidence pose: {view}/{node}: {actual}')
    for kind,height in [('adult',1.8),('child',1.1)]:
        if abs(receipts['scale']['measured_human_heights_m'][kind]-height)>.0001:raise ValueError('Incorrect scale silhouette: '+kind)
    for folder_name,stage,path in [('matches','export',source),('source-matches','source',BASE/'build/bus-101.blend')]:
        pairs=json.loads((BASE/'renders'/folder_name/'provenance.json').read_text())
        for view in ['service_front','service_side','service_rear','vision_front']:
            r=pairs[view]
            if r['stage']!=stage or r['engine']!='CYCLES' or r['sha256']!=signature(path):raise ValueError('Stale photographic comparison: '+folder_name+'/'+view)
            expected_exposure=calibration[view]['shot']['exposure']
            if abs(r['lighting']['exposure']-expected_exposure)>1e-5:raise ValueError('Incorrect photographic exposure: '+folder_name+'/'+view)
    eevee=json.loads((BASE/'renders/eevee/provenance.json').read_text())['hero']
    if eevee['stage']!='export' or eevee['engine']!='BLENDER_EEVEE' or eevee['sha256']!=digest:raise ValueError('Stale or non-exported Eevee view')
    # Same hero camera as the direct blocker pass: measure the bus, excluding
    # the campus and sky. These statistics support visual review, not acceptance.
    hero=Image.open(folder/'hero.png').convert('RGB')
    blocker=Image.open(BASE/'renders/seethrough/front_three_quarter.png').convert('RGB').resize(hero.size,Image.Resampling.NEAREST)
    rgb=np.asarray(blocker);mask=(rgb.max(2)<30)|(rgb.min(2)>240)
    pixels=np.asarray(hero)[mask]/255;luma=pixels@np.array([.2126,.7152,.0722])
    tone=dict(scope='Display-referred bus pixels from same-camera direct blocker mask; excludes campus/sky. Not an albedo measurement or a visual acceptance test.',
        measured_pixels=int(mask.sum()),display_luma_percentiles={str(p):float(np.percentile(luma,p)) for p in [1,5,50,95,99]},
        all_channels_clipped_fraction=float(np.mean(pixels.min(1)>=254/255)),any_channel_clipped_fraction=float(np.mean(pixels.max(1)>=254/255)))
    paint=Image.open(BASE/'renders/seethrough/hero-paint.png').convert('RGBA').resize(hero.size,Image.Resampling.NEAREST)
    pp=np.asarray(paint);pm=(pp[:,:,:3].min(2)>250)&(pp[:,:,3]>250)
    pm=np.asarray(Image.fromarray(pm.astype('uint8')*255).filter(ImageFilter.MinFilter(3)))>250
    rgb=np.asarray(hero)[pm]/255;pl=rgb@np.array([.2126,.7152,.0722])
    tone['paint']=dict(measured_pixels=int(pm.sum()),display_luma_percentiles={str(p):float(np.percentile(pl,p)) for p in [1,50,99]},
                       any_channel_clipped_fraction=float(np.mean(rgb.max(1)>=254/255)))
    tone['deep_shadow_fraction_below_25_srgb']=float(np.mean(luma<25/255))
    (BASE/'build/tonal-range.json').write_text(json.dumps(tone,indent=2))
    sheet(paths+[BASE/'renders/eevee/hero.png'],folder/'contact.jpg');sheet([folder/(n+'.png') for n in ['front','side','rear','top']],folder/'turnaround.jpg',2,w=720,h=480)
    pairs=list((BASE/'renders/matches').glob('*-pair.jpg'))
    if pairs:sheet(pairs,BASE/'renders/matches/contact.jpg',1,w=1500,h=800)
    print('REVIEW_SHEETS',folder/'contact.jpg',folder/'turnaround.jpg')
if __name__=='__main__':main()
