"""Review sheets and display-value measurements; no source photograph is a texture."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
FONT=find_font('Noto Sans','Regular')

def rgb(path):
    im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(230,232,230,255));bg.alpha_composite(im);return bg.convert('RGB')

def sheet(paths,out,columns=3,width=1800):
    cell=width//columns;height=round(cell*.67);canvas=Image.new('RGB',(width,math.ceil(len(paths)/columns)*height),(230,232,230));d=ImageDraw.Draw(canvas)
    font=ImageFont.truetype(FONT,max(16,round(cell*.032)))
    for i,path in enumerate(paths):
        im=rgb(path);im.thumbnail((cell-16,height-42),Image.Resampling.LANCZOS);x=(i%columns)*cell;y=(i//columns)*height
        canvas.paste(im,(x+(cell-im.width)//2,y+34+(height-42-im.height)//2));d.text((x+10,y+8),Path(path).stem.replace('_',' '),font=font,fill=(32,42,45))
    canvas.save(out,quality=93,optimize=True)

def tone(folder):
    meta=json.loads((folder/'shots.json').read_text());results={}
    for name,row in meta.items():
        im=rgb(folder/(name+'.png'));arr=np.asarray(im)/255.;mask=np.asarray(Image.open(folder/row['tonal_mask']).convert('RGBA'))
        geometry=mask[...,3]>250;paint=geometry&(mask[...,:3].min(axis=2)>240)
        result={}
        for label,region in [('geometry',geometry),('paint',paint)]:
            colors=arr[region]
            if not len(colors):
                result[label]=dict(samples=0);continue
            luma=colors@np.array([.2126,.7152,.0722])
            result[label]=dict(display_luma_p1_p50_p99=np.percentile(luma,[1,50,99]).tolist(),deep_shadow_below_25=float(np.mean(luma<25/255)),channel_clipped_fraction=float(np.mean(colors.max(axis=1)>=254.5/255)))
        results[name]=result
        im.thumbnail((1600,1600),Image.Resampling.LANCZOS);im.save(folder/(name+'.jpg'),quality=92,optimize=True)
    (folder/'tonal-range.json').write_text(json.dumps(dict(scope='Display values inside independent geometry/paint masks; not albedo estimates',views=results),indent=2))
    return meta,results

def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--pairs',required=True);p.add_argument('--form',required=True);a=p.parse_args()
    out=Path(a.renders);pairs=Path(a.pairs);meta,tones=tone(out);pair_meta,pair_tones=tone(pairs)
    motion=out.parent/'sedan-motion';motion_meta,_=tone(motion)
    eevee=out.parent/'sedan-eevee';eevee_meta,_=tone(eevee)
    combined=list(meta.values())+list(pair_meta.values())+list(motion_meta.values())+list(eevee_meta.values())
    if len({r['source_sha256'] for r in combined})!=1:raise ValueError('Mixed delivery revisions')
    if len({r['render_recipe_sha256'] for r in combined})!=1:raise ValueError('Mixed render recipes')
    if any(r['stage']!='final exported GLB' for r in combined):raise ValueError('Checkpoint must judge the exported GLB')
    standard=[out/(n+'.png') for n in meta if not any(n.startswith(c+'_') for c in ['Porcelain','Carbon','Graphite','Aluminum','Atlantic'])]
    colors=[out/(c+'_'+view+'.png') for c in ['Porcelain','Carbon','Graphite','Aluminum','Atlantic'] for view in ['front','rear']]
    sheet(colors,out/'factory-colors.jpg',2,1600);sheet(standard,out/'contact.jpg',3,1800)
    sheet([motion/(n+'.png') for n in motion_meta],motion/'contact.jpg',5,2400)
    for group in ['doors','hood','trunk','steering','wheels']:
        sheet([motion/(group+'_'+str(i)+'.png') for i in range(5)],motion/(group+'-sweep.jpg'),5,2400)
    sheet([out/'factory-colors.jpg',out/'contact.jpg',pairs/'used_front-pair.jpg',pairs/'used_rear-pair.jpg',motion/'contact.jpg',eevee/'front_three_quarter.jpg',Path(a.form)/'contact.jpg'],out/'checkpoint.jpg',2,2400)
    print('SEDAN CHECKPOINT',out/'checkpoint.jpg','source',combined[0]['source_sha256'])
if __name__=='__main__':main()
