"""Checkpoint review sheets; no documentation images before final approval.

Reference photographs are only displayed beside renders. Never used as UV,
projection, tracing, normal, albedo or other asset input. Derived reference
plates remain in ignored renders/ alongside the full-size checkpoints.
"""
import argparse,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from kit.contact import contact,review_sheet
FONT=find_font('Noto Sans', 'Regular')


def background(im,color=(231,233,229)):
    im=im.convert('RGBA');bg=Image.new('RGBA',im.size,(*color,255));bg.alpha_composite(im)
    return bg.convert('RGB')


def comparisons(folder):
    folder=Path(folder);meta=json.loads((folder/'shots.json').read_text())
    audit=json.loads((ROOT/'gas-grill/build/game-audit.json').read_text())
    size=audit['sets']['Grill']['bounds_m']['size']
    font=ImageFont.truetype(FONT,23);small=ImageFont.truetype(FONT,18)
    # Manufacturer front image: crop is measured from alpha, no tracing/adaptation.
    ref=Image.open(ROOT/'gas-grill/refs/grill-B.png').convert('RGBA')
    crop=ref.getchannel('A').point(lambda v:255 if v>180 else 0).getbbox();ref=ref.crop(crop)
    # Photo width corresponds to catalog's extended 52 inch table width.
    for name,axis,spec in [('front',0,1.3208),('side',1,.6858)]:
        raw=Image.open(folder/(name+'.png')).convert('RGBA')
        # Use identical px/m for model and reference, horizontal ortho camera scale.
        ppm=raw.width/meta[name]['ortho'];scale=800/raw.width;ppm*=scale
        render=background(raw.resize((800,round(raw.height*scale)),Image.Resampling.LANCZOS))
        plate=Image.new('RGB',(1600,850),(231,233,229));d=ImageDraw.Draw(plate)
        d.text((20,20),f'{name.upper()}  /  PHYSICAL SCALE REVIEW',font=font,fill=(26,43,35))
        plate.paste(render,(0,90));d.text((20,60),'Original asset • orthographic Cycles',font=small,fill=(32,51,42))
        if name=='front':
            r=ref.resize((round(1.3208*ppm),round(ref.height*(1.3208*ppm)/ref.width)),Image.Resampling.LANCZOS)
            # Ground and width both matched; reference photo includes a small perspective elevation.
            yground=90+round((.56515+meta[name]['ortho']/meta[name]['aspect']/2)*ppm)
            plate.paste(background(r),(800+(800-r.width)//2-round(.0495*ppm),yground-r.height))
            d.text((820,60),'Weber product photo • width calibrated to 1320.8 mm',font=small,fill=(32,51,42))
            d.text((820,735),'Photo perspective is retained; this is not a silhouette identity test.',font=small,fill=(70,77,70))
        else:
            # A dimension gate is useful even where no exact side orthophoto exists.
            x0,y0=890,180;w,h=spec*ppm,1.1303*ppm
            d.rectangle((x0,y0,x0+w,y0+h),outline=(43,91,70),width=3)
            d.line((x0,y0+h+22,x0+w,y0+h+22),fill=(43,91,70),width=2)
            d.text((x0+w/2,y0+h+36),'685.8 mm • US catalog p12',font=small,fill=(26,58,40),anchor='mt')
            d.text((x0+w+15,y0+30),'1130.3 mm',font=small,fill=(26,58,40))
            d.text((820,60),'Catalog dimension envelope • same pixels per meter',font=small,fill=(32,51,42))
            inset=ImageOps.contain(Image.open(ROOT/'gas-grill/refs/grill-metric-dimensions.jpg').convert('RGB'),(340,230))
            plate.paste(inset,(1250,310))
            d.text((1250,280),'Manufacturer dimension callouts',font=ImageFont.truetype(FONT,15),fill=(70,77,70))
            d.text((1250,550),'Inset not to scale; envelope at left is.',font=ImageFont.truetype(FONT,14),fill=(70,77,70))
            d.text((820,735),'Side orthophoto unavailable; depth compared to the published envelope.',font=small,fill=(70,77,70))
        d.text((20,782),f'Generated grill: {size[axis]*1000:.1f} mm vs {spec*1000:.1f} mm; height {size[2]*1000:.1f} mm vs 1130.3 mm',font=small,fill=(26,58,40))
        d.text((20,813),'Sources: refs/SOURCES.md • manufacturer US catalog, p12 and original front product image',font=small,fill=(70,77,70))
        plate.save(folder/(name+'_comparison.jpg'),quality=89,optimize=True)


def doc_jpg(source,target):
    im=background(Image.open(source));im.thumbnail((1600,16000),Image.Resampling.LANCZOS)
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    while True:
        for quality in range(88,49,-3):
            im.save(target,quality=quality,optimize=True)
            if target.stat().st_size<=200000:return
        im.thumbnail((round(im.width*.9),round(im.height*.9)),Image.Resampling.LANCZOS)


def final_sheets(folder):
    metadata=json.loads((folder/'shots.json').read_text())
    for name,shot in metadata.items():
        if not shot.get('skipped') and (shot.get('stage')!='final' or not shot.get('source','').endswith('.glb')):
            raise RuntimeError('Final sheets require exported-GLB renders')
    # Measurement overlay on an unaltered orthographic render, not on a photo.
    proof=json.loads((ROOT/'gas-grill/build/construction-check.json').read_text())
    raw=background(Image.open(folder/'front.png'))
    front=Image.new('RGB',(raw.width,raw.height+100),(231,233,229));front.paste(raw,(0,0));d=ImageDraw.Draw(front)
    shot=metadata['front'];ppm=front.width/shot['ortho']
    x=round(front.width/2+(proof['lid_center_x_m']-shot['target'][0])*ppm)
    d.line((x,20,x,300),fill=(193,76,43),width=2)
    font=ImageFont.truetype(FONT,20)
    d.text((40,front.height-81),'Lid centerline / badge and thermometer X error <0.001 mm',font=font,fill=(26,58,40))
    d.text((40,front.height-48),f"Projected vertical gap: {proof['header']['vertical_gap_m']*1000:.2f} mm",font=font,fill=(26,58,40))
    front.save(folder/'front-centering.jpg',quality=90,optimize=True)
    names=['hero_closed','hero_open','front','side','back','top','controls','interior',
           'construction','combustion','regulator','scale','hose_pose','fit_check','drawer_open','grease_support']
    paths=[folder/(name+'.png') for name in names if (folder/(name+'.png')).exists()]
    eevee=folder.parent/'final-eevee/hero_closed.png'
    if eevee.exists():paths.append(eevee)
    contact(paths,folder/'contact.jpg',width=2400,title='Cinder Works / Field 3 • exported GLB • Cycles + Eevee last',
            captions={str(folder/'combustion.png'):'combustion / all five tents removed',str(eevee):'Eevee / exported GLB'})
    review_sheet([[folder/'controls.png',folder/'interior.png'],[folder/'drawer_open.png',folder/'grease_support.png']],
                 folder/'details-contact.jpg',width=2400,title='Baked atlas / controls / cookbox / withdrawn drawer / cup supports')
    rig_row=[folder/'hose_pose.png']
    if (folder/'fit_check.png').exists():rig_row.append(folder/'fit_check.png')
    review_sheet([rig_row],folder/'rig-contact.jpg',width=2400,title='Six-bone free hose / optional canonical tank fit')
    review_sheet([[folder/'front-centering.jpg',folder/'side.png'],[folder/'back.png',folder/'top.png']],
                 folder/'turnaround-contact.jpg',width=2400,title='Exported geometry / orthographic turnaround')
    for source,name in [('hero_closed.png','hero-closed'),('hero_open.png','hero-open'),
                         ('details-contact.jpg','details'),('rig-contact.jpg','rig-fit'),('turnaround-contact.jpg','turnaround')]:
        doc_jpg(folder/source,ROOT/'gas-grill/docs'/(name+'.jpg'))
    print('Final GLB contact sheet and five bounded docs JPGs:',folder)


def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--final',action='store_true')
    a=p.parse_args();folder=Path(a.renders)
    if a.final:
        final_sheets(folder);return
    comparisons(folder)
    rows=[['hero_closed.png','hero_open.png'],['match_closed-pair.jpg'],
          ['match_interior-pair.jpg']]
    review_sheet([[folder/name for name in row] for row in rows],folder/'contact.jpg',
                 title='Cinder Works / Field 3 • checkpoint 2 • high-detail Cycles source')
    rows=[['construction.png','combustion.png'],['controls.png','hose_pose.png']]
    review_sheet([[folder/name for name in row] for row in rows],folder/'construction-contact.jpg',
                 title='Construction / combustion / controls / free hose')
    contact([folder/'front_comparison.jpg',folder/'side_comparison.jpg'],
            folder/'dimensions-contact.jpg',width=2400,title='Published dimension envelope / source mesh')

if __name__=='__main__':main()
