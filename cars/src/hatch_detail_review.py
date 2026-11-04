"""Reproducible checkpoint sheets; no committed final-doc images at this gate."""
import argparse,hashlib,json,math,shutil,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
from hatch_pair_measure import measure
FONT=find_font('Noto Sans','Regular')
VIEWS='front_three_quarter rear_three_quarter face lamp_unlit lamp_lit wheel grille plate_detail mirror interior_glass cargo underbody underbody_layout opened_front opened_rear scale side front rear top'.split()
COLORS=['Porcelain','Carbon','Graphite','Aluminum','Atlantic']
GROUPS=['doors','hood','liftgate','steering','wheels']

def sheet(folder,names,path,columns=2,cell=(700,470)):
    canvas=Image.new('RGB',(columns*cell[0],math.ceil(len(names)/columns)*cell[1]),(228,231,234));d=ImageDraw.Draw(canvas)
    font=ImageFont.truetype(FONT,max(14,round(cell[0]/35)))
    for k,name in enumerate(names):
        image=Image.open(folder/(name+'.png')).convert('RGBA');image.thumbnail((cell[0],cell[1]-34),Image.Resampling.LANCZOS)
        x=(k%columns)*cell[0];y=(k//columns)*cell[1];d.text((x+12,y+5),name.replace('_',' '),font=font,fill=(20,30,35));canvas.paste(image,(x+(cell[0]-image.width)//2,y+34),image)
    canvas.save(path,quality=91,optimize=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--source',required=True);a=p.parse_args();folder=Path(a.renders)
    colors=[color+'_'+view for color in COLORS for view in ['front','rear']]
    motions=[group+'_'+str(i) for group in GROUPS for i in range(5)]
    names=VIEWS+colors+motions+['used_front','used_rear'];meta=json.loads((folder/'shots.json').read_text())
    missing=[n for n in names if not (folder/(n+'.png')).exists() or n not in meta]
    if missing:raise ValueError('Incomplete checkpoint: '+str(missing))
    hashes={meta[n]['source_sha256'] for n in names}
    current=hashlib.sha256(Path(a.source).read_bytes()).hexdigest()
    if hashes!={current}:raise ValueError('Mixed or stale source hashes: rebuild all checkpoint views')
    if Path(a.source).suffix=='.glb':
        extra=folder.parent/'hatch-eevee';record=json.loads((extra/'shots.json').read_text())['front_three_quarter']
        if record['source_sha256']!=current:raise ValueError('Stale Eevee source hash')
        for suffix in ['.png','-mask.png']:shutil.copyfile(extra/('front_three_quarter'+suffix),folder/('eevee'+suffix))
        meta['eevee']=record;meta['eevee']['tonal_mask']='eevee-mask.png';names.append('eevee')
    meta={name:meta[name] for name in names}
    (folder/'shots.json').write_text(json.dumps(meta,indent=2))
    sheet(folder,colors,folder/'five-colors.jpg',2,(700,470))
    sheet(folder,VIEWS,folder/'details-contact.jpg',3,(700,485))
    sheet(folder,motions,folder/'motion-sweeps.jpg',5,(480,340))
    sheet(folder,names,folder/'contact-sheet.jpg',4,(600,420))
    for start in range(0,len(names),9):
        sheet(folder,names[start:start+9],folder/('review-page-'+str(start//9)+'.jpg'),3,(600,420))
    tones={}
    for n in names:
        rgb=np.asarray(Image.open(folder/(n+'.png')).convert('RGB'),dtype=float)
        mask=np.asarray(Image.open(folder/(n+'-mask.png')).convert('RGBA'))
        body=(mask[:,:,:3].mean(axis=2)>128)&(mask[:,:,3]>128);asset=mask[:,:,3]>128
        vals=rgb[asset]@np.array([.2126,.7152,.0722])
        tones[n]=dict(asset_luma_p1_p50_p99=np.percentile(vals,[1,50,99]).tolist(),below_25_fraction=float((vals<25).mean()),
            clipped_channel_fraction=float((rgb[asset]>=254).mean()),paint_luma_median=float(np.median(rgb[body]@np.array([.2126,.7152,.0722]))))
    (folder/'tonal-range.json').write_text(json.dumps(tones,indent=2));measure(folder)
    print('H120_CHECKPOINT',len(names),'native views',current)
if __name__=='__main__':main()
