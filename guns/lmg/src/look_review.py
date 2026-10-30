"""Whole visible parts, highlight chroma and native 2D on/off wear evidence.

Photo polygons are comparison observations only. All delivered masks and UVs
come from the actual imported GLBs; none enter a modeling/material stage.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.fonts import find_font
from image_masks import raster,bilinear
from final_review import rgb,sheet
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),19);SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),15)
LUMA=np.array([.2126,.7152,.0722])
# Native upright coordinates, whole visible part silhouettes, never tiny patches.
REGIONS={
 'paint_receiver':('used_receiver', [[(826,466),(1473,448),(1500,643),(829,688)]], 'hero', ('Receiver_Sheet','Receiver_Rivet','Receiver_RearDoubler','SideWell_Housing')),
 'paint_cover':('used_receiver', [[(788,327),(1456,319),(1514,390),(797,411)]], 'hero', ('FeedCover_Shell','FeedCover_PressedBead','FeedCover_SidePress')),
 'barrel_phosphate':('used_right', [[(40,128),(91,134),(107,146),(377,205),(390,220),(372,231),(106,164),(75,158),(43,153)]], 'hero', ('Barrel_Exterior','BarrelSeat','BarrelCollar')),
 'bipod_phosphate':('used_right', [[(390,344),(413,349),(315,699),(336,708),(335,722),(290,743),(277,734),(277,723),(294,715)]], 'hero', ('Bipod_Channel','Bipod_Extension','Bipod_Foot','Bipod_Yoke')),
 'molded_handguard':('used_right', [[(543,255),(568,253),(790,300),(824,318),(850,339),(876,353),(866,430),(616,390),(614,345),(592,329),(547,318)]], 'handguard', ('Handguard_Sculpt','Handguard_MoldRib')),
 'molded_stock':('used_receiver', [[(1210,781),(1340,901),(1440,1090),(1410,1120),(1300,1110),(1190,955),(1140,872)]], 'furniture', ('Stock_Sculpt',)),
 'molded_box':('used_right', [[(543,255),(568,253),(790,300),(824,318),(850,339),(876,353),(866,430),(616,390),(614,345),(592,329),(547,318)]], 'box', ('Box_Shell','Box_EndRib','Box_MoldRib')),
 'handle_polymer':('used_receiver', [[(426,70),(765,63),(767,145),(430,148)]], 'barrel_handle', ('CarryHandle_Grip',)),
 'brass':('belt', [[(945,963),(1093,934),(1113,1084),(1180,1205),(1225,1460),(1005,1502),(985,1200),(966,1095)],[(1115,2135),(1310,2100),(1320,2160),(1150,2200)],[(1625,904),(1775,860),(1815,1020),(1900,1150),(1985,1375),(1740,1420),(1680,1140),(1655,1005)]], 'belt', ('Belt_Round',)),
 'steel_links':('belt', [[(1005,1510),(1225,1470),(1255,1540),(1080,1605)],[(1100,1710),(1265,1660),(1330,2050),(1150,2100)],[(1740,1428),(1985,1385),(2020,1460),(1790,1545)],[(1805,1640),(2010,1580),(2120,1940),(1890,2020)]], 'belt', ('Belt_Link',)),
 'copper_green_tip':('belt', [[(914,535),(943,576),(985,710),(1093,934),(945,963),(880,730)],[(1575,440),(1615,480),(1680,645),(1780,860),(1625,904),(1540,630)]], 'belt', ('Belt_Round',)),
}
SITES={
 'receiver':('Receiver_Sheet','Receiver_RearDoubler','SideWell_Housing'),
 'cover':('FeedCover_Shell','FeedCover_PressedBead','FeedCover_SidePress'),
 'handle':('CarryHandle_Grip',),'flash':('FlashHider',),
 'regulator':('GasRegulator','Regulator_Grip'),
 'ports':('Receiver_Sheet','LinkPort_Rim','ChargingGuide'),
 'feet':('Bipod_Foot',),'box':('Box_Shell','Box_MoldRib','Box_EndRib','Box_ClipBacking'),
 'butt':('Buttpad','Stock_Sculpt'),
}
def polygon_mask(shape,polygons):
 m=Image.new('L',shape,0);d=ImageDraw.Draw(m)
 for p in polygons:d.polygon(p,fill=255)
 return np.asarray(m)>0

def metrics(a):
 a=np.asarray(a,float).reshape(-1,3);lum=a@LUMA;v=a.max(axis=1)
 hi=a[lum>=np.percentile(lum,90)];c=hi.mean(axis=0)
 return dict(pixels=len(a),median_rgb=np.median(a,axis=0).tolist(),luma_p10_p50_p90=np.percentile(lum,[10,50,90]).tolist(),value_p10_p50_p90=np.percentile(v,[10,50,90]).tolist(),brightest_decile_rgb=c.tolist(),highlight_saturation=float((c.max()-c.min())/max(c.max(),1)),value_histogram=np.histogram(v,bins=32,range=(0,256))[0].tolist())
def mask_crop(im,m):
 q=Image.fromarray(np.uint8(im)).convert('RGBA');q.putalpha(Image.fromarray(np.uint8(m)*255));box=q.getbbox();q=q.crop(box) if box else q
 bg=Image.new('RGBA',q.size,(108,111,114,255));bg.alpha_composite(q);return ImageOps.contain(bg.convert('RGB'),(840,390),Image.Resampling.LANCZOS)
def chart(name,im,m,photo,pm,record,path):
 canvas=Image.new('RGB',(1800,850),'#e7e9e6');d=ImageDraw.Draw(canvas)
 d.text((25,12),name+' / whole visible parts, exported GLB vs white-balanced photograph',font=FONT,fill='black')
 canvas.paste(mask_crop(im,m),(25,60));canvas.paste(mask_crop(photo,pm),(925,60))
 for i,(label,key,color) in enumerate([('GLB','render',(145,55,28)),('Photo','photo',(25,90,150))]):
  row=record[key];x=25+i*900
  d.text((x,470),label+' value P10/P50/P90 '+str(np.round(row['value_p10_p50_p90'],1).tolist()),font=FONT,fill='black')
  d.text((x,501),'Median RGB '+str(np.round(row['median_rgb'],1).tolist()),font=SMALL,fill='black')
  d.text((x,529),'Highlight RGB '+str(np.round(row['brightest_decile_rgb'],1).tolist())+' / saturation %.3f'%row['highlight_saturation'],font=SMALL,fill='black')
  values=np.array(row['value_histogram'],float);values/=max(values.max(),1)
  d.line([(x+10+j*25,716-t*140) for j,t in enumerate(values)],fill=color,width=3)
 d.text((25,760),'Image distributions include illumination. No claim of inverse reflectance calibration.',font=SMALL,fill='black')
 d.text((25,789),'Neutral: '+record['neutral']['limit']+'; clipped = '+str(record['neutral']['clipped_neutral']),font=SMALL,fill='black')
 canvas.save(path,quality=94)
def components(mask):
 # Eight-connected areas: two-dimensional shape evidence, not line runs.
 h,w=mask.shape;remaining=set(np.flatnonzero(mask));rows=[]
 while remaining:
  seed=remaining.pop();stack=[seed];xs=[];ys=[]
  while stack:
   j=stack.pop();y,x=divmod(j,w);xs.append(x);ys.append(y)
   for dy in (-1,0,1):
    for dx in (-1,0,1):
     xx=x+dx;yy=y+dy;k=yy*w+xx
     if 0<=xx<w and 0<=yy<h and k in remaining:remaining.remove(k);stack.append(k)
  rows.append(dict(area_px=len(xs),bounds=[int(min(xs)),int(min(ys)),int(max(xs)+1),int(max(ys)+1)]))
 return sorted(rows,key=lambda r:r['area_px'],reverse=True)
def main():
 out=BASE/'renders/final/look-review';out.mkdir(parents=True,exist_ok=True)
 atlas=np.asarray(Image.open(BASE/'textures/T_Harrow56_BaseColor.png'));orm=np.asarray(Image.open(BASE/'textures/T_Harrow56_ORM.png'));corrections=json.loads((BASE/'build/white-balanced/corrections.json').read_text());meta=json.loads((BASE/'renders/final/beauty/shots.json').read_text());cache={};values={}
 for role,(photo,polygons,shot,prefixes) in ({} if '--wear-only' in sys.argv else REGIONS).items():
  im=np.asarray(rgb(BASE/'renders/final/beauty'/(shot+'.png')));h,w=im.shape[:2]
  geo=np.load(BASE/'build/image-geometry'/(shot+'.npz'))
  assert str(geo['sha256'])==meta[shot]['sha256'],('Stale imported image geometry',shot)
  assert str(geo['pose_key'])==json.dumps({k:meta[shot].get(k) for k in ('action','frame','layers','hide_box')},sort_keys=True)
  if shot not in cache:cache[shot]=raster(geo,meta[shot],w,h)
  ids,coords=cache[shot];selected=[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(prefixes)];m=np.isin(ids,selected)
  points=np.stack((coords[:,:,0].ravel()*2048,(1-coords[:,:,1].ravel())*2048),axis=1)
  sampled=bilinear(atlas,points).reshape(h,w,-1);sampled_orm=bilinear(orm,points).reshape(h,w,-1)
  # Exterior axial station separates the case and jacket on actual triangles.
  if role in ('brass','copper_green_tip'):
   suffix='_Case' if role=='brass' else '_Jacket'
   m &= np.isin(ids,[i+1 for i,n in enumerate(geo['names']) if str(n).endswith(suffix)])
  # Guard raster/AA boundaries by one pixel; this removes subpixel hidden
  # silhouettes, rather than measuring the neighboring surface's color.
  m=np.asarray(Image.fromarray(np.uint8(m)*255).filter(ImageFilter.MinFilter(3)))>0
  ref=np.asarray(Image.open(BASE/'build/white-balanced'/(photo+'.jpg')).convert('RGB'));pm=polygon_mask((ref.shape[1],ref.shape[0]),polygons)
  pm=np.asarray(Image.fromarray(np.uint8(pm)*255).filter(ImageFilter.MinFilter(3)))>0
  assert m.sum()>10,(role,m.sum())
  row=dict(render=metrics(im[m]),photo=metrics(ref[pm]),neutral=corrections[photo],photo_source=photo,photo_polygons=polygons,parts=[str(geo['names'][i-1]) for i in selected],sha256=meta[shot]['sha256'])
  # Preserve the metric dictionary separately from its reference filename.
  row['photo_source']=photo;row['photo']=metrics(ref[pm])
  row['shipped_basecolor_srgb_median']=np.median(sampled[m,:3],axis=0).tolist()
  row['shipped_roughness_median']=float(np.median(sampled_orm[m,1])/255)
  row['shipped_metallic_median']=float(np.median(sampled_orm[m,2])/255)
  row['shipped_specular_factor_median']=float(np.median(sampled[m,3])/255)
  values[role]=row;chart(role,im,m,ref,pm,row,out/(role+'-histograms.jpg'))
 if values:(out/'finish-values.json').write_text(json.dumps(values,indent=2))
 wear={};entries=[]
 for site,prefixes in SITES.items():
  wear[site]={}
  for shot in ('hero','hero_right'):
   off=BASE/'renders/final/wear'/site/(shot+'.png')
   if not off.exists():continue
   on=BASE/'renders/final/beauty'/(shot+'.png');a=np.asarray(rgb(on),float);b=np.asarray(rgb(off),float);h,w=a.shape[:2]
   geo=np.load(BASE/'build/image-geometry'/(shot+'.npz'))
   assert str(geo['sha256'])==meta[shot]['sha256']
   if shot not in cache:cache[shot]=raster(geo,meta[shot],w,h)
   ids,_=cache[shot];selected=[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(prefixes)];region=np.isin(ids,selected)
   diff=np.max(abs(a-b),axis=2);m=region&(diff>=4)
   # Every changed pixel stays at this site's actual visible surfaces.
   comp=components(m);ys,xs=np.nonzero(m);signed=(a-b)@LUMA
   record=dict(pixel_threshold=4,changed_area_px=int(m.sum()),visible_part_area_px=int(region.sum()),bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)] if len(xs) else None,median_signed_luma_change=float(np.median(signed[m])) if m.any() else 0,mean_absolute_luma_change=float(np.mean(abs(signed[m]))) if m.any() else 0,max_rgb_change=float(diff[region].max()) if region.any() else 0,connected_regions=comp,source_on=meta[shot]['sha256'],source_off=json.loads((off.parent/'shots.json').read_text())[shot]['sha256'])
   wear[site][shot]=record
   difference=np.uint8(np.clip(abs(a-b)*6,0,255));difference[~region]=0
   dpath=out/(site+'-'+shot+'-difference.png');Image.fromarray(difference).save(dpath)
   mpath=out/(site+'-'+shot+'-mask.png');Image.fromarray(np.uint8(m)*255).save(mpath)
   pair=out/(site+'-'+shot+'-on-off.jpg');sheet([('Wear ON / native '+shot,on),('Only '+site+' OFF / same camera',off),('Absolute RGB difference ×6',dpath),('Actual 2D changed area / >=4 RGB',mpath)],pair,columns=2,cell=(800,500));entries.append((site+' / '+shot,pair))
 (out/'wear-values.json').write_text(json.dumps(wear,indent=2))
 if entries:sheet(entries,out/'wear-sites.jpg',columns=3,cell=(600,740))
 if 'hero' in cache:
  a=np.asarray(rgb(BASE/'renders/final/beauty/hero.png'));ids,_=cache['hero'];foreground=ids>0
  (out/'hero-tones.json').write_text(json.dumps(dict(luma_percentiles=np.percentile(a[foreground]@LUMA,[1,10,50,90,99]).tolist(),clipped_channel_fraction=float((a[foreground]>=255).mean())),indent=2))
 print('WHOLE-PART FINISHES',len(values),'WEAR SITES',len(wear),flush=True)
if __name__=='__main__':main()
