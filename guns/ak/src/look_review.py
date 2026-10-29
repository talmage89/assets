"""Whole visible parts, HSV distributions, highlight colors and 2D wear.

Masks come from actual imported triangle IDs and UVs. Photo polygons select
whole exterior parts, independently of their RGB. White balance precedes all
measurements. Differences in light, age and finish stay explicit in the charts.
"""
from pathlib import Path
import argparse,json,sys,math,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit.fonts import find_font
from image_masks import raster,bilinear,projection
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),20);SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),16)
# Whole-part regions, in native upright photo coordinates. No photo pixels
# are used by the source materials or mesh generation.
REGIONS={
 'enamel':('museum.jpg',[[(580,162),(1136,153),(1137,229),(581,243)]],'hero',('Receiver_Sheet','Receiver_Rivet','Selector_','TriggerGuard_')),
 'cover':('museum.jpg',[[(590,158),(625,128),(1076,128),(1078,157)]],'hero',('TopCover_','Cover_Return')),
 'bluing':('front-sharp.jpg',[[(1040,640),(1255,630),(1310,800),(1375,995),(1450,1180),(1330,1220),(1220,1220),(1150,1030)],[(1265,1260),(1460,1310),(1440,1530),(1390,1710),(1215,1710),(1240,1480)]],'gas_muzzle',('Barrel','GasBlock_','Sight_Front','Sight_Windage','Sight_Rod','Muzzle_')),
 'wood':('early.jpg',[[(55,268),(397,268),(451,284),(592,259),(597,345),(55,480)],[(1281,235),(1638,239),(1640,297),(1300,327)],[(1414,165),(1644,169),(1643,210),(1414,208)]] ,'hero',('Stock_Sculpt','LowerHandguard_Sculpt','UpperHandguard_Sculpt')),
 'grip':('grip-sharp.jpg',[[(404,245),(1120,263),(1170,325),(1130,470),(1100,575),(1150,800),(1455,1520),(1410,1620),(1180,1710),(1000,1740),(935,1680),(860,1430),(780,1180),(665,900),(545,695),(460,620),(412,490)]],'grip_detail',('PistolGrip_Sculpt',)),
 'magazine':('early.jpg',[[(996,356),(1122,346),(1179,483),(1249,572),(1329,639),(1262,740),(1175,686),(1093,590),(1043,490)]] ,'magazine',('Magazine_Sheet','Magazine_FoldSpine','Magazine_Floorplate','Magazine_FeedLip')),
 'case':('ammunition.jpg',[[(1235,1300),(1640,1300),(1700,3500),(1195,3500)]],'cartridge',('Cartridge_Case',)),
 'jacket':('ammunition-copper.jpg',[[(1610,631),(1700,637),(1800,654),(1900,677),(2000,708),(2100,745),(2190,774),(2213,788),(2213,807),(2190,823),(2100,851),(2000,878),(1900,897),(1800,911),(1700,919),(1610,922)]],'cartridge',('Cartridge_Jacket',)),
}
# Also expose each furniture part separately: the large stock must not hide
# the smaller upper handguard's reflection/value differences in an aggregate.
for key,index,prefix in [('stock',0,'Stock_Sculpt'),('lower_handguard',1,'LowerHandguard_Sculpt'),('upper_handguard',2,'UpperHandguard_Sculpt')]:
 photo,polygons,shot,_=REGIONS['wood'];REGIONS[key]=(photo,[polygons[index]],shot,(prefix,))
LUMA=np.array([.2126,.7152,.0722])
def hsv(a):return np.asarray(Image.fromarray(np.uint8(np.clip(a,0,255))).convert('HSV')).astype(float)/255

def metrics(a):
 a=np.asarray(a).reshape(-1,3);lum=a@LUMA;mx=a.max(axis=1);mi=a.min(axis=1);sat=(mx-mi)/np.maximum(mx,1)
 value_percentiles=np.percentile(mx,[10,25,50,75,90])
 bright=a[lum>=np.percentile(lum,90)]
 color=bright.mean(axis=0);s=(color.max()-color.min())/max(color.max(),1)
 return dict(luma_p75=float(np.percentile(lum,75)),value_percentiles=value_percentiles.tolist(),value_p90_p10_over_median=float((value_percentiles[4]-value_percentiles[0])/max(value_percentiles[2],1)),pixels=len(a),median_rgb=np.median(a,axis=0).tolist(),luma_percentiles=np.percentile(lum,[1,5,50,95,99]).tolist(),median_saturation=float(np.median(sat)),brightest_decile_rgb=color.tolist(),brightest_decile_saturation=float(s))
def polygon_mask(size,polygons):
 m=Image.new('L',size,0);d=ImageDraw.Draw(m)
 for p in polygons:d.polygon(p,fill=255)
 return np.asarray(m)>0

def hist(d,xy,a,b):
 x,y=xy;colors=[(138,60,32),(30,95,130)]
 for j,title in enumerate(('Hue','Saturation','Value')):
  d.text((x+j*330,y),title,font=FONT,fill='black')
  vals=[]
  for q in (a,b):
   im=Image.fromarray(np.asarray(q,dtype=np.uint8).reshape(-1,1,3)).convert('HSV');values=np.asarray(im).reshape(-1,3)
   v=values[values[:,1]>=13,j] if j==0 else values[:,j]
   hh=np.histogram(v,bins=32,range=(0,256))[0].astype(float);hh/=max(hh.sum(),1);vals.append(hh)
  peak=max(np.max(q) for q in vals)
  d.line((x+j*330,y+180,x+j*330+295,y+180),fill='#888888',width=1)
  for q,color in zip(vals,colors):d.line([(x+j*330+k*295/31,y+180-v/max(peak,.001)*135) for k,v in enumerate(q)],fill=color,width=3)
  d.text((x+j*330,y+185),'0                         1',font=SMALL,fill='#555555')

def masked(a,mask,box=(780,380)):
 im=Image.fromarray(a.astype('uint8')).convert('RGBA');im.putalpha(Image.fromarray(np.uint8(mask)*255))
 bounds=im.getbbox();im=im.crop(bounds) if bounds else im
 bg=Image.new('RGBA',im.size,(108,111,114,255));bg.alpha_composite(im)
 return ImageOps.contain(bg.convert('RGB'),box,Image.Resampling.LANCZOS)

def main():
 p=argparse.ArgumentParser();p.add_argument('--renders',default='renders/final/beauty');p.add_argument('--out',default='renders/final/look-review');a=p.parse_args()
 folder=BASE/a.renders;out=BASE/a.out;out.mkdir(parents=True,exist_ok=True)
 geometry=np.load(BASE/'build/value-geometry.npz');meta=json.loads((folder/'shots.json').read_text());corrections=json.loads((BASE/'build/white-balanced/corrections.json').read_text());data={};cache={}
 ammo_folder=BASE/'renders/final/cartridge'
 if (ammo_folder/'shots.json').exists():meta.update(json.loads((ammo_folder/'shots.json').read_text()))
 for role,(photo,polygons,shot,prefixes) in REGIONS.items():
  if shot not in meta:continue
  geo=np.load(BASE/'build/value-cartridge.npz') if shot=='cartridge' else geometry
  shotfolder=ammo_folder if shot=='cartridge' else folder
  im=np.asarray(Image.open(shotfolder/(shot+'.png')).convert('RGB'));h,w=im.shape[:2]
  if shot not in cache:cache[shot]=raster(geo,meta[shot],w,h)
  ids,uv=cache[shot];selected=[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(prefixes)];mask=np.isin(ids,selected)
  ref=np.asarray(Image.open(BASE/'build/white-balanced'/photo).convert('RGB'));rm=polygon_mask((ref.shape[1],ref.shape[0]),polygons)
  rgb=im[mask];reference=ref[rm];assert len(rgb)>20,(role,len(rgb))
  values=dict(render=metrics(rgb),photo=metrics(reference),photo_source=photo,photo_polygons=polygons,neutral=corrections[photo],parts=[str(geo['names'][i-1]) for i in selected],render_sha256=meta[shot]['sha256'])
  data[role]=values
  sheet=Image.new('RGB',(1800,950),'#ebede9');d=ImageDraw.Draw(sheet)
  d.text((24,12),role+' / whole visible parts: exported GLB (brown) and white-balanced photo (blue)',font=FONT,fill='black')
  left=masked(im,mask);right=masked(ref,rm);sheet.paste(left,(25,65));sheet.paste(right,(925,65))
  hist(d,(30,465),rgb,reference)
  for k,(label,row) in enumerate([('GLB',values['render']),('Photo',values['photo'])]):
   x=30+k*880
   text=f"{label}: median RGB {np.round(row['median_rgb'],1).tolist()} | luma p1/50/99 {np.round(np.array(row['luma_percentiles'])[[0,2,4]],1).tolist()}"
   d.text((x,720),text,font=SMALL,fill='black')
   d.text((x,754),f"Brightest decile RGB {np.round(row['brightest_decile_rgb'],1).tolist()} | saturation {row['brightest_decile_saturation']:.3f}",font=SMALL,fill='black')
   color=tuple(int(v) for v in row['brightest_decile_rgb']);d.rectangle((x,793,x+125,855),fill=color)
  d.text((30,885),'Neutral: '+corrections[photo]['neutral'],font=SMALL,fill='black')
  d.text((30,916),'Whole-part image distributions; hue omits saturation <.05. Light/exposure differ; these are not inverse albedo measurements.',font=SMALL,fill='#444444')
  sheet.save(out/(role+'-histograms.jpg'),quality=94)
 # Receiver wear: resample actual hero UV/ORM and the photo to the same
 # approximate physical grid. Both binary masks retain their 2D topology.
 if 'hero' in cache:
  wear2d(folder,out,geometry,meta,cache)
 (out/'finish-values.json').write_text(json.dumps(data,indent=2))
 from final_review import sheet
 sheet(out/'finish-overview.jpg',[(k,out/(k+'-histograms.jpg')) for k in data],2,(900,530))
 print('WHOLE-PART FINISH REVIEW',list(data),flush=True)


def component_sizes(mask):
 seen=np.zeros(mask.shape,bool);areas=[];h,w=mask.shape
 for j,i in zip(*np.where(mask)):
  if seen[j,i]:continue
  stack=[(j,i)];seen[j,i]=True;count=0
  while stack:
   y,x=stack.pop();count+=1
   for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
    if 0<=yy<h and 0<=xx<w and mask[yy,xx] and not seen[yy,xx]:seen[yy,xx]=True;stack.append((yy,xx))
  areas.append(count*.25)
 return sorted(areas,reverse=True)

def wear2d(folder,out,geometry,meta,cache):
 im=np.asarray(Image.open(folder/'hero.png').convert('RGB')).astype(float);h,w=im.shape[:2];ids,uv=cache['hero']
 # Left flat at 0.5 mm sampling, Y -25..212 / Z52..85. Museum left view.
 ys=np.arange(-.025,.212,.0005);zs=np.arange(.052,.085,.0005)
 yy,zz=np.meshgrid(ys,zs);points=np.stack([np.full_like(yy,-.0175),yy,zz],axis=2).reshape(-1,3)
 xy,_=projection(points,meta['hero'],w,h);observed=bilinear(im,xy).reshape(len(zs),len(ys),3)
 coords=bilinear(uv,xy);orm=np.asarray(Image.open(BASE/'textures/T_Rill39_ORM.png').convert('RGB')).astype(float)
 pixels=bilinear(orm,np.stack([coords[:,0]*(orm.shape[1]-1),(1-coords[:,1])*(orm.shape[0]-1)],axis=1)).reshape(len(zs),len(ys),3)
 ii=np.clip(xy[:,0].astype(int),0,w-1);jj=np.clip(xy[:,1].astype(int),0,h-1)
 labels=ids[jj,ii].reshape(len(zs),len(ys));valid=np.isin(labels,[i+1 for i,n in enumerate(geometry['names']) if str(n).startswith(('Receiver_Sheet','Receiver_Rivet'))])
 worn=((pixels[:,:,1]>160)&(pixels[:,:,2]<100)| (pixels[:,:,2]>180))&valid
 # Independently specified museum left flank corners (Y increasing leftward).
 photo=np.asarray(Image.open(BASE/'build/white-balanced/museum.jpg').convert('RGB')).astype(float)
 src=np.array([[1466,798],[908,793],[910,881],[1468,888]],float);dst=np.array([[-.035,.086],[.220,.086],[.220,.050],[-.035,.050]])
 matrix=[];rhs=[]
 for (x,y),(u,v) in zip(dst,src):matrix.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);rhs.extend([u,v])
 a=np.linalg.solve(np.array(matrix),np.array(rhs));H=np.r_[a,1].reshape(3,3)
 q=np.stack([yy.ravel(),zz.ravel(),np.ones(yy.size)],axis=1)@H.T;q=q[:,:2]/q[:,2:]
 ref=bilinear(photo,q).reshape(observed.shape);refmask=(ref@LUMA)>95
 # Classifications are intentionally distinct: actual substrate in the GLB,
 # bright worn gray in the photo. Photo light can hide wear or mimic it.
 report=dict(grid_pitch_mm=.5,size_mm=[len(ys)*.5,len(zs)*.5],render_worn_share=float(worn[valid].mean()),photo_bright_worn_share=float(refmask.mean()),visible_render_share=float(valid.mean()),render_components_mm2=component_sizes(worn),photo_components_mm2=component_sizes(refmask),render_profile_length=worn.mean(axis=0).tolist(),photo_profile_length=refmask.mean(axis=0).tolist(),render_profile_height=worn.mean(axis=1).tolist(),photo_profile_height=refmask.mean(axis=1).tolist(),scope='2D whole receiver strip; GLB actual substrate from ORM versus photo luma >95; no morphology filter. Gray framing and scale are estimates; thresholds are not equivalent BRDF measurements.')
 (out/'wear-2d-values.json').write_text(json.dumps(report,indent=2))
 sheet=Image.new('RGB',(1800,980),'#ebede9');d=ImageDraw.Draw(sheet);d.text((25,12),'Receiver / actual full 2D masks at the same 0.5 mm grid / no morphology filtering',font=FONT,fill='black')
 for k,(rgb,mask,title) in enumerate([(observed,worn,'GLB: actual substrate, from shipping ORM'),(ref,refmask,'Photo: bright worn gray, luma >95')]):
  x=25+k*900;pic=Image.fromarray(np.uint8(np.clip(np.flipud(rgb),0,255))).resize((850,119));binary=Image.fromarray(np.uint8(np.flipud(mask))*255).resize((850,119),Image.Resampling.NEAREST)
  d.text((x,55),title,font=SMALL,fill='black');sheet.paste(pic,(x,90));sheet.paste(binary.convert('RGB'),(x,245))
  d.text((x,385),f"Worn area {report['render_worn_share' if k==0 else 'photo_bright_worn_share']:.1%}",font=FONT,fill='black')
  sizes=report['render_components_mm2' if k==0 else 'photo_components_mm2']
  d.text((x,430),'Largest connected areas (mm²): '+str(np.round(sizes[:7],1).tolist()),font=SMALL,fill='black')
 for j,(key,label) in enumerate([('length','Along the receiver'),('height','Across its height')]):
  x=30+j*900;y=530;d.text((x,y),label,font=FONT,fill='black')
  for prefix,color in [('render',(138,60,32)),('photo',(30,95,130))]:
   profile=report[prefix+'_profile_'+key];d.line([(x+i*800/(len(profile)-1),y+240-v*200) for i,v in enumerate(profile)],fill=color,width=3)
 d.text((25,820),'Brown: GLB. Blue: photo. Components retain boundary clipping; original scratch histories are intentionally different.',font=SMALL,fill='black')
 d.text((25,855),'GLB masks are measured on actual baked materials, not lighting highlights. Photo masks use an explicit image-value threshold.',font=SMALL,fill='black')
 d.text((25,890),'The visible-mask fraction excludes occlusion by controls and other parts. Photo homography uses four independent flank anchors.',font=SMALL,fill='black')
 sheet.save(out/'receiver-wear-2d.jpg',quality=94)

if __name__=='__main__':main()
