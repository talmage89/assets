"""White-balanced view-value distributions, independent photo and surface patches."""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font
p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,default=BASE/'renders/final/photos');p.add_argument('--loci',type=Path,default=BASE/'build/value-loci.json');a=p.parse_args()
photo=Image.open(BASE/'build/references/used-rubber.png').convert('RGB');render=Image.open(a.renders/'used_photo.png').convert('RGB')
patches={'frame':(544,277,573,307),'barrel':(197,292,228,309),'rubber_texture':(733,325,784,365),'rubber_hand':(619,257,642,280),'sight':(480,126,486,133)}
loci=json.loads(a.loci.read_text())['patches'];rows={};font=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
annotated=[photo.copy(),render.copy()]
def stats(im,poly):
 mask=Image.new('L',im.size,0);ImageDraw.Draw(mask).polygon(poly,fill=255)
 rgb=np.asarray(im)[np.asarray(mask)>0].astype(float);luma=rgb@np.array([.2126,.7152,.0722]);med=np.median(rgb,axis=0)
 return dict(pixels=len(rgb),rgb_median=med.tolist(),rgb_ratio_G1=(med/max(med[1],1)).tolist(),luma_median=float(np.median(luma)),luma_p5_p95=np.percentile(luma,[5,95]).tolist())
for i,(name,rect) in enumerate(patches.items()):
 x0,y0,x1,y1=rect;pp=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
 rp=[(x*render.width,y*render.height) for x,y in loci[name]['normalized_polygon']]
 rows[name]=dict(photo_native_patch=rect,render_surface_polygon=rp,photo=stats(photo,pp),render=stats(render,rp))
 for im,poly in zip(annotated,(pp,rp)):
  d=ImageDraw.Draw(im);d.line(poly+[poly[0]],fill=(245,160,30),width=2);d.text(poly[0],str(i+1),fill=(250,60,10),font=font)
out=a.renders;out.mkdir(parents=True,exist_ok=True)
neutral=json.loads((BASE/'build/references/whitebalance.json').read_text())['used-rubber']
(out/'values.json').write_text(json.dumps(dict(neutral=neutral,patches=rows,note='Independent native-photo and actual ray-hit projected render patches. View/light values, not recovered albedo or measured roughness.'),indent=2))
canvas=Image.new('RGB',(2000,820),(229,230,226));d=ImageDraw.Draw(canvas)
for i,im in enumerate(annotated):
 im.thumbnail((990,650),Image.Resampling.LANCZOS);canvas.paste(im,(i*1000,40))
d.text((15,10),'Gray-paper-balanced used photograph / actual-surface render patches',font=font,fill=(20,30,25))
for i,(name,r) in enumerate(rows.items()):d.text((20,690+i*24),f'{i+1}. {name}: photo / render median {r["photo"]["luma_median"]:.2f} / {r["render"]["luma_median"]:.2f}',font=font,fill=(20,30,25))
canvas.save(out/'value-patches.jpg',quality=92,optimize=True)
print('VALUES',[(n,round(r['photo']['luma_median'],2),round(r['render']['luma_median'],2)) for n,r in rows.items()])
