"""Ignored form-checkpoint presentation and measured tonal ranges; no docs JPGs."""
import argparse,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet
from kit.fonts import find_font
from PIL import Image,ImageDraw,ImageFont
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--renders',required=True);a=p.parse_args();out=Path(a.renders)
font=ImageFont.truetype(find_font('Noto Sans','Regular'),21)
names=['hero','top','bottom','side','front','concave_section','truck','truck_inner','wheel_bearing','tail_plies','grip_edge','lean_left','lean_center','lean_right','rest_wall','scale']
paths=[out/(n+'.png') for n in names if (out/(n+'.png')).exists()]
if paths:contact(paths,out/'contact.jpg',width=2400,title='Skateboard / FORM CHECKPOINT / exported quick-material GLB / Cycles')
pairs=list((out/'pairs').glob('*-pair.jpg'))
if pairs:review_sheet([[x] for x in sorted(pairs)],out/'matched-pairs.jpg',width=2200,title='Period photographic comparisons / form checkpoint')
if all((out/(n+'.png')).exists() for n in ('lean_left','lean_center','lean_right')):
    review_sheet([[out/(n+'.png') for n in ('lean_left','lean_center','lean_right')]],out/'steering.jpg',width=2400,title='Coordinated steer / front +angle, rear -angle / conservative ±12° hanger travel')
section=Path('build/sections.json')
if section.exists():
    rows=json.loads(section.read_text());w,h=1600,1280;canvas=Image.new('RGB',(w,h),(237,237,232));draw=ImageDraw.Draw(canvas)
    draw.text((22,20),'Actual casting sections / dense source blue / game mesh orange / equal axes',font=font,fill=(25,35,38))
    for index,row in enumerate(rows):
        x0=(index%3)*530+28;y0=(index//3)*580+100
        allpoints=np.array([p for key in ('dense','game') for seg in row[key] for p in seg]);lo=allpoints.min(axis=0);hi=allpoints.max(axis=0);scale=min(470/max(hi[0]-lo[0],.001),430/max(hi[1]-lo[1],.001))
        draw.text((x0,y0-36),row['part'].replace('Front ','')+' / X %.0f mm'%(row['station_m']*1000),font=font,fill=(25,35,38))
        for key,color,width in [('dense',(44,93,148),3),('game',(204,107,37),2)]:
            for seg in row[key]:
                a,b=[(x0+(p[0]-lo[0])*scale,y0+450-(p[1]-lo[1])*scale) for p in seg];draw.line([a,b],fill=color,width=width)
        draw.text((x0,y0+470),'Section Y × Z: %.1f × %.1f mm'%tuple((hi-lo)*1000),font=font,fill=(70,75,75))
    canvas.save(out/'cast-sections.jpg',quality=94)
measurements={}
for name in names:
    path=out/(name+'.png')
    if not path.exists():continue
    rgb=np.asarray(Image.open(path).convert('RGB'),float);luma=rgb@np.array([.2126,.7152,.0722])
    measurements[name]=dict(scope='Display-referred full frame including concrete; not recovered albedo',luma_percentiles=dict(zip(['p1','p5','p50','p95','p99'],np.percentile(luma,[1,5,50,95,99]).tolist())),all_channels_ge250_fraction=float(np.all(rgb>=250,axis=2).mean()),all_channels_le5_fraction=float(np.all(rgb<=5,axis=2).mean()))
(out/'values.json').write_text(json.dumps(measurements,indent=2))
# Complete checkpoint sheets must refer to the current GLB; iteration folders
# may contain earlier versions, which keep their original recorded hashes.
if out.name=='checkpoint':
    digest=hashlib.sha256(Path('build/skateboard.glb').read_bytes()).hexdigest();meta=json.loads((out/'shots.json').read_text())
    assert set(names)<=set(meta),'Missing checkpoint view'
    assert all(meta[n]['sha256']==digest for n in names),'Stale checkpoint renders'
    pm=json.loads((out/'pairs/shots.json').read_text());assert len(pm)>=3 and all(v['sha256']==digest for v in pm.values()),'Stale photographic pairs'
print('Checkpoint sheets:',out,'; hero values:',measurements.get('hero'))
