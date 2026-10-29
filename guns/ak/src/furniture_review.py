"""Independent full-part and flat-side wood measurements from rendered images.

Comparison-only. Photo pixels never enter a material, mesh or baking stage.
Value spread is explicitly (HSV-value p90 - p10) / median, not an albedo claim.
"""
from pathlib import Path
import argparse,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.fonts import find_font
from image_masks import raster,projection
from look_review import REGIONS,polygon_mask,metrics,masked
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),16)
# Interior flat side excludes the silhouette, comb highlight, worn bottom and
# wrist. Independent photo polygon follows the corresponding broad side land.
FLAT_WORLD=[(.0175,-.260,.014),(.0175,-.260,.074),(.0175,-.120,.074),(.0175,-.120,.046)]
FLAT_PHOTO=[(120,300),(352,300),(484,316),(484,345),(120,436)]

def main():
 p=argparse.ArgumentParser();p.add_argument('--renders',default='renders/final/photos');p.add_argument('--source',default='renders/final/source-photos');p.add_argument('--out',default='renders/final/look-review');args=p.parse_args()
 folder=BASE/args.renders;out=BASE/args.out;out.mkdir(parents=True,exist_ok=True)
 geo=np.load(BASE/'build/value-geometry.npz');meta=json.loads((folder/'shots.json').read_text())['used_photo']
 image=np.asarray(Image.open(folder/'used_photo.png').convert('RGB'));height,width=image.shape[:2]
 ids,_=raster(geo,meta,width,height)
 photo=np.asarray(Image.open(BASE/'build/white-balanced/early.jpg').convert('RGB'))
 correction=json.loads((BASE/'build/white-balanced/corrections.json').read_text())['early.jpg']
 rows={};tiles=[];stage='Dense source' if Path(meta['source']).suffix=='.blend' else 'Shipped GLB'
 source_folder=BASE/args.source
 source=np.asarray(Image.open(source_folder/'used_photo.png').convert('RGB')) if (source_folder/'used_photo.png').exists() else None
 if source is not None and source.shape!=image.shape:source=np.asarray(Image.fromarray(source).resize((width,height),Image.Resampling.LANCZOS))
 for name in ('stock','lower_handguard','upper_handguard','stock_flat_side'):
  role='stock' if name=='stock_flat_side' else name
  _,polygons,_,prefixes=REGIONS[role]
  selected=[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(prefixes)]
  mask=np.isin(ids,selected)
  if name=='stock_flat_side':
   pixels,_=projection(np.array(FLAT_WORLD),meta,width,height)
   mask &= polygon_mask((width,height),[pixels.tolist()]);polygons=[FLAT_PHOTO]
  pm=polygon_mask((photo.shape[1],photo.shape[0]),polygons)
  assert mask.sum()>30 and pm.sum()>30
  row=dict(render=metrics(image[mask]),photo=metrics(photo[pm]),neutral=correction,
           render_source=meta['source'],render_sha256=meta['sha256'],
           photo_polygons=polygons,scope='Same fitted side view; image value includes light/finish. Interior flat side excludes silhouette and edge wear.')
  if source is not None:row['dense_source']=metrics(source[mask])
  rows[name]=row
  tile=Image.new('RGB',(1800,440),'#ebede9');d=ImageDraw.Draw(tile)
  d.text((24,8),name+' / '+stage+' and locally balanced photo',font=FONT,fill='black')
  for k,(a,m,label,key) in enumerate(((image,mask,'GLB','render'),(photo,pm,'Photo','photo'))):
   x=24+900*k;pic=masked(a,m,(840,270));tile.paste(pic,(x,45))
   r=row[key];d.text((x,333),f"{label}: RGB {r['median_rgb']} | saturation {r['median_saturation']:.3f}",font=SMALL,fill='black')
   d.text((x,365),f"Value p10/50/90 {np.round(np.array(r['value_percentiles'])[[0,2,4]],1).tolist()} | spread / median {r['value_p90_p10_over_median']:.3f}",font=SMALL,fill='black')
  d.text((24,407),'Spread = (value p90 - p10) / median. Photo white balance: unprinted cloth immediately below receiver.',font=SMALL,fill='black')
  tiles.append(tile)
 sheet=Image.new('RGB',(1800,440*len(tiles)),'#ebede9')
 for i,tile in enumerate(tiles):sheet.paste(tile,(0,440*i))
 sheet.save(out/'wood-grain-and-color.jpg',quality=95)
 (out/'wood-grain-values.json').write_text(json.dumps(rows,indent=2))
 for name,row in rows.items():
  print(name,[(key,tuple(row[key]['median_rgb']),round(row[key]['median_saturation'],3),round(row[key]['value_p90_p10_over_median'],3)) for key in ('render','photo')],flush=True)
if __name__=='__main__':main()
