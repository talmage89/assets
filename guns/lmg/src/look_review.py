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
 'paint_receiver':('used_receiver', [[(414,446),(469,450),(485,509),(807,512),(814,448),(1452,448),(1456,414),(1604,414),(1611,637),(1550,681),(1510,710),(1448,709),(1457,647),(1374,645),(1360,710),(910,723),(841,721),(835,646),(809,646),(797,670),(552,676),(518,645),(514,551),(451,551),(440,656),(423,683),(416,624),(400,541),(359,506)]], 'used_photo', ('Receiver_Sheet','Receiver_Rivet','Receiver_RearDoubler','SideWell_Housing')),
 'paint_cover':('used_receiver', [[(788,327),(1456,319),(1514,390),(797,401)],[(488,321),(777,318),(800,349),(798,392),(520,392),(475,375),(457,349)]], 'used_photo', ('FeedCover_Shell','FeedCover_PressedBead','FeedCover_SidePress')),
 'barrel_phosphate':('used_right', [[(129,150),(370,204),(377,214),(370,228),(124,173)]], 'used_right_photo', ('Barrel_Exterior','BarrelSeat','BarrelCollar')),
 'bipod_phosphate':('used_right', [[(422,367),(441,373),(321,699),(333,705),(334,718),(326,730),(302,734),(280,726),(261,715),(254,702),(258,696),(273,698),(302,708),(301,692)],[(443,373),(452,374),(439,527),(428,607),(437,604),(439,614),(435,621),(429,621),(427,630),(438,637),(439,647),(435,654),(429,656),(430,647),(413,643),(392,635),(386,630),(385,624),(389,619),(409,623),(413,535),(422,444)]], 'used_right_photo', ('Bipod_Channel','Bipod_Extension','Bipod_Foot','Bipod_Yoke')),
 'molded_handguard':('used_right', [[(543,255),(568,253),(790,300),(824,318),(850,339),(876,353),(866,430),(616,390),(614,345),(592,329),(547,318)]], 'used_right_photo', ('Handguard_Sculpt','Handguard_MoldRib')),
 'molded_stock':('used_stock', [[(176,1066),(374,1026),(558,929),(814,748),(843,694),(830,626),(826,546),(868,469),(978,329),(1084,205),(1602,529),(1638,593),(1580,674),(1455,802),(1326,962),(1248,1037),(1212,1035),(1150,978),(1095,945),(1029,944),(906,992),(782,1079),(604,1230),(410,1450)]], 'right_photo', ('Stock_Sculpt',)),
 'molded_grip':('used_receiver', [[(1228,737),(1255,733),(1234,752),(1225,778),(1231,809),(1251,840),(1287,884),(1336,953),(1388,1023),(1424,1062),(1425,1077),(1397,1091),(1322,1112),(1247,1126),(1221,1119),(1205,1109),(1202,1090),(1208,1065),(1195,1025),(1168,975),(1134,912),(1114,865),(1103,822),(1120,827),(1154,818),(1195,791),(1214,769)]], 'used_photo', ('PistolGrip_Sculpt','Grip_MoldRib')),
 'molded_box':('used_box', [[(363,871),(419,734),(540,595),(652,470),(721,411),(801,376),(900,370),(900,560),(1182,548),(1195,589),(1586,575),(1582,1249),(1576,1281),(515,1283),(472,1264),(442,1215)]], 'box_detail_photo', ('Box_Shell','Box_EndRib','Box_MoldRib')),
 'handle_polymer':('used_receiver', [[(426,70),(765,63),(767,145),(430,148)]], 'used_photo', ('CarryHandle_Grip',)),
 'brass':('belt', [[(945,963),(1093,934),(1113,1084),(1180,1205),(1225,1460),(1005,1502),(985,1200),(966,1095)],[(1115,2135),(1310,2100),(1320,2160),(1150,2200)],[(1625,904),(1775,860),(1815,1020),(1900,1150),(1985,1375),(1740,1420),(1680,1140),(1655,1005)]], 'ammo_photo', ('Belt_Round',)),
 'steel_links':('belt', [[(1005,1510),(1225,1470),(1255,1540),(1080,1605)],[(1100,1710),(1265,1660),(1330,2050),(1150,2100)],[(1740,1428),(1985,1385),(2020,1460),(1790,1545)],[(1805,1640),(2010,1580),(2120,1940),(1890,2020)]], 'ammo_photo', ('Belt_Link',)),
 'copper_green_tip':('belt', [[(914,535),(943,576),(985,710),(1093,934),(945,963),(880,730)],[(1575,440),(1615,480),(1680,645),(1780,860),(1625,904),(1540,630)]], 'ammo_photo', ('Belt_Round',)),
}
SITES={
 'receiver':('Receiver_','SideWell_Housing'),
 'cover':('FeedCover_','RearSight_Base'),
 'handle':('CarryHandle_Grip',),'flash':('FlashHider',),
 'regulator':('GasRegulator','Regulator_Grip','GasBlock_Web'),
 'ports':('Receiver_','LinkPort_Rim','ChargingGuide'),
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
 out=BASE/(sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else 'renders/final/look-review');out.mkdir(parents=True,exist_ok=True)
 atlas=np.asarray(Image.open(BASE/'textures/T_Harrow56_BaseColor.png'));orm=np.asarray(Image.open(BASE/'textures/T_Harrow56_ORM.png'));corrections=json.loads((BASE/'build/white-balanced/corrections.json').read_text());meta=json.loads((BASE/'renders/final/beauty/shots.json').read_text());photo_meta=json.loads((BASE/'renders/final/photos/shots.json').read_text());meta.update(photo_meta);cache={};values={};observations=[]
 for role,(photo,polygons,shot,prefixes) in ({} if '--wear-only' in sys.argv else REGIONS).items():
  im=np.asarray(rgb(BASE/'renders/final'/('photos' if shot in photo_meta else 'beauty')/(shot+'.png')));h,w=im.shape[:2]
  geo=np.load(BASE/'build/image-geometry'/(shot+'.npz'))
  assert str(geo['sha256'])==meta[shot]['sha256'],('Stale imported image geometry',shot)
  assert str(geo['pose_key'])==json.dumps({k:meta[shot].get(k) for k in ('action','frame','layers','hide_box','inspection_parts','diagnostic_isolate')},sort_keys=True)
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
  overlay=Image.fromarray(ref.copy());draw=ImageDraw.Draw(overlay)
  for polygon in polygons:draw.line(polygon+[polygon[0]],fill=(245,55,25),width=max(2,overlay.width//500))
  overlay_path=out/(role+'-photo-region.png');overlay.save(overlay_path);observations.append((role+' / native whole-part observation',overlay_path))
  row=dict(render_shot=shot,camera_matched_to_this_photo=role not in ('molded_stock','molded_box'),render=metrics(im[m]),photo=metrics(ref[pm]),neutral=corrections[photo],photo_source=photo,photo_polygons=polygons,parts=[str(geo['names'][i-1]) for i in selected],sha256=meta[shot]['sha256'])
  # Preserve the metric dictionary separately from its reference filename.
  row['photo_source']=photo;row['photo']=metrics(ref[pm])
  row['shipped_basecolor_srgb_median']=np.median(sampled[m,:3],axis=0).tolist()
  row['shipped_roughness_median']=float(np.median(sampled_orm[m,1])/255)
  row['shipped_metallic_median']=float(np.median(sampled_orm[m,2])/255)
  row['shipped_specular_factor_median']=float(np.median(sampled[m,3])/255)
  values[role]=row;chart(role,im,m,ref,pm,row,out/(role+'-histograms.jpg'))
 if values:
  (out/'finish-values.json').write_text(json.dumps(values,indent=2))
  sheet(observations,out/'photographic-regions.jpg',columns=3,cell=(600,480))
 if '--finishes-only' in sys.argv:
  print('WHOLE-PART FINISHES',len(values),flush=True);return
 wear={};entries=[]
 selected_sites=sys.argv[sys.argv.index('--sites')+1].split(',') if '--sites' in sys.argv else list(SITES)
 assert set(selected_sites)<=set(SITES)
 for site in selected_sites:
  prefixes=SITES[site]
  wear[site]={}
  for shot in ('hero','hero_right'):
   off=BASE/'renders/final/wear'/site/(shot+'.png')
   if not off.exists():continue
   on=BASE/'renders/final/beauty'/(shot+'.png');a=np.asarray(rgb(on),float);b=np.asarray(rgb(off),float);h,w=a.shape[:2]
   geo=np.load(BASE/'build/image-geometry'/(shot+'.npz'))
   assert str(geo['sha256'])==meta[shot]['sha256']
   if shot not in cache:cache[shot]=raster(geo,meta[shot],w,h)
   ids,coordinates=cache[shot];selected=[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(prefixes)];region=np.isin(ids,selected)
   diff=np.max(abs(a-b),axis=2);m=region&(diff>=4)
   # Every changed pixel stays at this site's actual visible surfaces.
   comp=components(m);ys,xs=np.nonzero(m);signed=(a-b)@LUMA
   record=dict(pixel_threshold=4,changed_area_px=int(m.sum()),visible_part_area_px=int(region.sum()),bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)] if len(xs) else None,median_signed_luma_change=float(np.median(signed[m])) if m.any() else 0,mean_absolute_luma_change=float(np.mean(abs(signed[m]))) if m.any() else 0,max_rgb_change=float(diff[region].max()) if region.any() else 0,connected_regions=comp,source_on=meta[shot]['sha256'],source_off=json.loads((off.parent/'shots.json').read_text())[shot]['sha256'])
   if m.any():
    uv=coordinates[m];points=np.stack((uv[:,0]*2048,(1-uv[:,1])*2048),axis=1)
    other=BASE/'build/controls'/site/'textures'
    onbase=bilinear(atlas,points);offbase=bilinear(np.asarray(Image.open(other/'T_Harrow56_BaseColor.png')),points)
    onorm=bilinear(orm,points);ofform=bilinear(np.asarray(Image.open(other/'T_Harrow56_ORM.png')),points)
    record['shipped_maps_at_changed_pixels']=dict(basecolor_on_median_rgb=np.median(onbase[:,:3],axis=0).tolist(),basecolor_off_median_rgb=np.median(offbase[:,:3],axis=0).tolist(),roughness_on_off=[float(np.median(q[:,1])/255) for q in (onorm,ofform)],metallic_on_off=[float(np.median(q[:,2])/255) for q in (onorm,ofform)],specular_on_off=[float(np.median(q[:,3])/255) for q in (onbase,offbase)])
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
