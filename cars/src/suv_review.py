"""Dimensioned X220 source evidence. No committed docs or photographic textures."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.fonts import find_font
from kit.photo_match import compose
import suv_spec as S
ASSET=Path(__file__).resolve().parents[1];FONT=find_font('Noto Sans','Regular')
def font(n):return ImageFont.truetype(FONT,n)
def rgb(path):
 im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,(228,231,232,255));bg.alpha_composite(im);return bg.convert('RGB')
def save(im,path):im.save(path,quality=92,optimize=True)

def overlays(out,shots,perspective=False):
 records={}
 definitions={
 'rav4':dict(wb=2.690,axles=[(244,574),(938,575)],top=[('hood lead',65,417),('hood mid',205,382),('cowl',340,369),('header',525,267),('roof middle',700,239),('roof aft',900,241),('spoiler',1055,259),('D pillar',1110,320)],ends=[('front upper',45,440,True),('front bumper',33,500,True),('front chin',30,570,True),('tail upper',1157,425,False),('tail bumper',1169,500,False),('tail lower',1150,556,False)]),
 'crv':dict(wb=2.66192,axles=[(246,574),(937,574)],top=[('hood lead',80,411),('hood mid',220,382),('cowl',340,360),('header',515,268),('roof middle',700,238),('roof aft',900,242),('spoiler',1080,253),('D pillar',1128,315)],ends=[('front upper',41,465,True),('front bumper',29,510,True),('front chin',34,576,True),('tail upper',1161,425,False),('tail bumper',1170,506,False),('tail lower',1150,565,False)])}
 source=Image.open(out/'side.png').convert('RGBA');meta=shots['side'];sf=np.array(meta['points']['front_axle']);sr=np.array(meta['points']['rear_axle'])
 for make,rec in definitions.items():
  if perspective:
   source=Image.open(out/(make+'_profile.png')).convert('RGBA');meta=shots[make+'_profile'];sf=np.array(meta['points']['front_axle']);sr=np.array(meta['points']['rear_axle'])
  photo=Image.open(ASSET/('refs/suv-'+make+'-side.jpg')).convert('RGBA');pf,pr=[np.array(p)*1.75 for p in rec['axles']]
  v=sr-sf;w=pr-pf;theta=math.atan2(w[1],w[0])-math.atan2(v[1],v[0]);scale=np.linalg.norm(w)/np.linalg.norm(v);matrix=scale*np.array([[math.cos(theta),-math.sin(theta)],[math.sin(theta),math.cos(theta)]]);offset=pf-matrix@sf;inverse=np.linalg.inv(matrix);shift=-inverse@offset
  warped=source.transform(photo.size,Image.Transform.AFFINE,(*inverse[0],shift[0],*inverse[1],shift[1]),Image.Resampling.BICUBIC)
  tint=Image.new('RGBA',photo.size,(20,120,200,0));tint.putalpha(warped.getchannel('A').point(lambda v:round(v*.4)));photo.alpha_composite(tint)
  im=photo.convert('RGB');d=ImageDraw.Draw(im);ppm=np.linalg.norm(w)/rec['wb'];mask=np.array(warped.getchannel('A'))>200;measure=[]
  for name,x,y in rec['top']:
   xx,yy=round(1.75*x),round(1.75*y);ys=np.nonzero(np.any(mask[:,xx-1:xx+2],axis=1))[0]
   if not len(ys):continue
   measured=int(ys[0]);delta=(yy-measured)/ppm;measure.append(dict(feature=name,axis='height',render_minus_photo_m=delta,photo_pixel=[xx,yy],render_pixel=[xx,measured]))
   d.line((xx,yy,xx,measured),fill=(210,50,20),width=4);d.ellipse((xx-4,yy-4,xx+4,yy+4),fill=(210,50,20))
  for name,x,y,front in rec['ends']:
   xx,yy=round(1.75*x),round(1.75*y);xs=np.nonzero(np.any(mask[yy-1:yy+2,:],axis=0))[0]
   if not len(xs):continue
   measured=int(xs[0] if front else xs[-1]);delta=(xx-measured if front else measured-xx)/ppm;measure.append(dict(feature=name,axis='outward',render_minus_photo_m=delta,photo_pixel=[xx,yy],render_pixel=[measured,yy]))
   d.line((xx,yy,measured,yy),fill=(210,50,20),width=4);d.ellipse((xx-4,yy-4,xx+4,yy+4),fill=(210,50,20))
  # At a steep backlight, a vertical residual greatly exceeds actual edge
  # separation. Retain that residual and independently report nearest 2D
  # silhouette distance; neither is an all-outline/photo accuracy claim.
  interior=np.zeros_like(mask)
  interior[1:-1,1:-1]=mask[1:-1,1:-1]&mask[:-2,1:-1]&mask[2:,1:-1]&mask[1:-1,:-2]&mask[1:-1,2:]
  edge_y,edge_x=np.nonzero(mask & ~interior)
  for row in measure:
   xx,yy=row['photo_pixel'];index=np.argmin((edge_x-xx)**2+(edge_y-yy)**2);nx,ny=int(edge_x[index]),int(edge_y[index])
   row['nearest_silhouette_pixel']=[nx,ny];row['nearest_silhouette_distance_m']=math.hypot(nx-xx,ny-yy)/ppm
  worst=max(abs(r['render_minus_photo_m']) for r in measure);nearest_worst=max(r['nearest_silhouette_distance_m'] for r in measure)
  d.text((35,35),'X220 / '+make.upper()+(' / WHEELBASE-REGISTERED PERSPECTIVE OVERLAY' if perspective else ' / WHEELBASE-REGISTERED ORTHOGRAPHIC OVERLAY'),font=font(29),fill=(25,55,80))
  d.text((35,80),f'Held-out axis max {worst*1000:.0f} mm / nearest silhouette max {nearest_worst*1000:.0f} mm. Red: photo picks. No outline fit.',font=font(23),fill=(25,55,80))
  d.text((35,118),'Photo retains perspective. Picks +/-4 preview px; wheel centers alone set scale, translation and level.',font=font(21),fill=(25,55,80))
  for x,y in [pf,pr]:d.ellipse((x-6,y-6,x+6,y+6),outline=(0,90,180),width=4)
  save(im,out/(('side-perspective-overlay-' if perspective else 'side-overlay-')+make+'.jpg'))
  records[make]=dict(method='Two chassis wheel centers only, no silhouette fit or model deformation',reference_wheelbase_m=rec['wb'],reference_axles_px=[pf.tolist(),pr.tolist()],original_pixels_per_m=ppm,pick_uncertainty_m=7/ppm,worst_absolute_deviation_m=worst,worst_nearest_silhouette_distance_m=nearest_worst,measurements=measure,rotation_degrees=math.degrees(theta),scale=scale,offset_px=offset.tolist())
 (out/('side-perspective-overlays.json' if perspective else 'side-overlays.json')).write_text(json.dumps(records,indent=2))

def sections(out,report):
 for rec in report['sections']:
  im=Image.new('RGB',(1150,950),(240,242,240));d=ImageDraw.Draw(im);scale=380
  def xy(p):return 575+p[0]*scale,850-p[1]*scale
  for z in np.arange(0,1.81,.25):
   y=xy((0,z))[1];d.line((100,y,1040,y),fill=(205,214,210));d.text((20,y-12),f'{z:.2f} m',font=font(17),fill=(70,80,80))
  for a,b in rec['segments_xz_m']:d.line((*xy(a),*xy(b)),fill=(25,77,102),width=2)
  lo,hi=rec['tumblehome_samples_m'];d.line((*xy(lo),*xy(hi)),fill=(215,67,25),width=4)
  d.text((25,20),rec['name'].replace('_',' ').upper()+f" / actual mesh plane y={rec['y_m']:.3f} m",font=font(27),fill=(30,50,65))
  d.text((25,65),f"Shoulder {rec['shoulder_m'][2]*1000:.0f} mm; upper lean {rec['upper_inward_degrees'][0]:.1f} deg; glass {rec['tumblehome_degrees']:.1f} deg",font=font(22),fill=(30,60,80))
  d.text((25,102),f"Lower lean {rec['just_below_degrees']:.1f} to {rec['low_door_degrees']:.1f} deg; crease turn {rec['crease_normal_turn_80mm_degrees']:.1f} deg / 80 mm",font=font(21),fill=(30,60,80))
  d.text((25,138),f"Die hollow {rec['hollow_50mm_chord_m']*1000:.2f} mm / 50 mm chord. Actual cuts, including glazing/gauge.",font=font(20),fill=(30,60,80))
  save(im,out/('section-'+rec['name']+'.jpg'))

def rear_photos(out,report):
 records={}
 for make,body,top,base in [('rav4',[(250,360),(948,360)],[(379,180),(810,180)],[(323,298),(874,298)]),('crv',[(237,350),(960,350)],[(383,202),(824,202)],[(334,309),(874,309)])]:
  width=1.855;ppm=(body[1][0]-body[0][0])/width;record=dict(scope='Near-rear photograph ratio estimate; perspective and feature picks +/-5 preview px, not OEM section data',body_reference_m=width,top_m=(top[1][0]-top[0][0])/ppm,base_m=(base[1][0]-base[0][0])/ppm)
  record['d_pillar_per_side_m']=(width-record['base_m'])/2
  record['vertical_span_m']=(sum(p[1] for p in base)/2-sum(p[1] for p in top)/2)/ppm;records[make]=record
  im=Image.open(ASSET/('refs/suv-'+make+'-back.jpg')).convert('RGB');d=ImageDraw.Draw(im)
  for name,pair in [('body',body),('top',top),('base',base)]:
   pair=[tuple(1.75*v for v in p) for p in pair];d.line((*pair[0],*pair[1]),fill=(230,55,20),width=5)
  d.text((35,35),f"{make.upper()} / glass top {record['top_m']*1000:.0f}, base {record['base_m']*1000:.0f}, H {record['vertical_span_m']*1000:.0f} mm / pillar {record['d_pillar_per_side_m']*1000:.0f} mm",font=font(29),fill=(35,65,85))
  save(im,out/('rear-photo-measure-'+make+'.jpg'))
 (out/'rear-photo-measurements.json').write_text(json.dumps(records,indent=2))
 # Same-frame construction comparisons, deliberately not called fitted rear pairs.
 for make in records:
  left=rgb(out/'rear.png');right=Image.open(out/('rear-photo-measure-'+make+'.jpg')).convert('RGB');left.thumbnail((1000,850));right.thumbnail((1000,850));im=Image.new('RGB',(2000,950),(228,231,232));im.paste(left,((1000-left.width)//2,80));im.paste(right,(1000+(1000-right.width)//2,80));d=ImageDraw.Draw(im);d.text((25,20),'X220 / '+make.upper()+' rear / photographic widths are estimates',font=font(28),fill=(30,50,65));save(im,out/('rear-comparison-'+make+'.jpg'))

def dimensioned(out,shots,report):
 for name in ['side','front','rear','top']:
  im=rgb(out/(name+'.png'));d=ImageDraw.Draw(im);w,h=im.size;points=shots[name]['points']
  d.text((25,20),'ALDER X220 / '+name.upper()+' / SOURCE FORM',font=font(27),fill=(25,50,65))
  text=f"Measured {report['bounds_m']['size'][1]*1000:.1f} L / {report['bounds_m']['size'][0]*1000:.1f} body W / {report['bounds_m']['size'][2]*1000:.1f} H mm"
  d.text((25,60),text,font=font(20),fill=(25,65,85))
  if name=='side':
   for aa,bb,y,label in [('front','rear',h-25,'Overall length / class 4595-4625 mm'),('front_axle','rear_axle',h-75,f"{report['wheelbase_m']*1000:.0f} mm wheelbase / class 2662-2690 mm")]:
    x1,x2=sorted((points[aa][0],points[bb][0]));d.line((x1,y,x2,y),fill=(20,90,125),width=2)
    for x in [x1,x2]:d.line((x,y-6,x,y+6),fill=(20,90,125),width=2)
    d.text((x1,y-28),label,font=font(18),fill=(20,80,110))
   d.text((25,h-115),f"Actual overhangs F/R {report['overhangs_m']['front']*1000:.0f} / {report['overhangs_m']['rear']*1000:.0f} mm; 225/65R17",font=font(20),fill=(25,65,85))
  if name in ['front','rear']:d.text((25,h-45),f"Tracks {report['tracks_m']['F']*1000:.0f} / {report['tracks_m']['R']*1000:.0f} mm; mirrors {report['mirror_span_m']*1000:.0f} mm",font=font(20),fill=(25,65,85))
  save(im,out/(name+'-dimensions.jpg'))


def main():
 p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--report',required=True);p.add_argument('--cameras',required=True);a=p.parse_args();out=Path(a.renders);report=json.loads(Path(a.report).read_text());shots=json.loads((out/'shots.json').read_text());cameras=json.loads(Path(a.cameras).read_text())
 if any(v['source_sha256']!=report['source_sha256'] for v in shots.values()):raise ValueError('Mixed source revisions in review')
 tone={}
 for name in shots:
  path=out/(name+'.png');im=np.array(Image.open(path).convert('RGBA'));cols=im[...,:3][im[...,3]>250]
  if len(cols)<100:raise ValueError('Empty opaque foreground in '+str(path)+'; inspect framing and studio occlusion')
  luma=cols@np.array([.2126,.7152,.0722]);tone[name]=dict(display_luma_p1_p50_p99=np.percentile(luma,[1,50,99]).tolist(),channel_255_fraction=float(np.mean(cols.max(axis=1)==255)),shadow_below_25_fraction=float(np.mean(luma<25)))
  save(rgb(path),out/(name+'.jpg'))
 (out/'tonal-range.json').write_text(json.dumps(dict(scope='Opaque foreground source clay; lit values are not paint albedos',views=tone),indent=2))
 compose(Path(a.cameras),out,out);clay={k+'_clay':dict(v,title=v['title'].replace('clay with stripes','neutral clay')) for k,v in cameras.items()};cp=out/'clay-cameras.json';cp.write_text(json.dumps(clay,indent=2));compose(cp,out,out)
 overlays(out,shots);overlays(out,shots,True);sections(out,report);rear_photos(out,report);dimensioned(out,shots,report)
 front,rear=[rgb(out/(n+'-dimensions.jpg')) for n in ['front','rear']];pair=Image.new('RGB',(front.width+rear.width,max(front.height,rear.height)),(228,231,232));pair.paste(front,(0,0));pair.paste(rear,(front.width,0));save(pair,out/'front-rear.jpg')
 names=['front_three_quarter.jpg','rear_three_quarter.jpg','side-dimensions.jpg','front-rear.jpg','top-dimensions.jpg','side_raking.jpg','side-overlay-rav4.jpg','side-overlay-crv.jpg','side-perspective-overlay-rav4.jpg','side-perspective-overlay-crv.jpg','rav4_profile.jpg','crv_profile.jpg']
 names += [k+'.jpg' for k in shots if k.startswith('stripes')]
 names += ['curvature-body.jpg','curvature-hood-roof.jpg','parent/curvature-body.jpg','parent/curvature-hood-roof.jpg']+['section-'+r['name']+'.jpg' for r in report['sections']]
 names += ['rear-photo-measure-'+k+'.jpg' for k in ['crv','rav4']]+['rear-comparison-'+k+'.jpg' for k in ['crv','rav4']]
 names += [k+'-pair.jpg' for k in cameras]+[k+'_clay-pair.jpg' for k in cameras]+[k+'-calibration.jpg' for k in cameras]
 tw,th=800,550;canvas=Image.new('RGB',(2400,math.ceil(len(names)/3)*th),(228,231,232));d=ImageDraw.Draw(canvas)
 for i,name in enumerate(names):
  im=rgb(out/name);im.thumbnail((tw-20,th-60),Image.Resampling.LANCZOS);x=i%3*tw;y=i//3*th;canvas.paste(im,(x+(tw-im.width)//2,y+45+(th-60-im.height)//2));d.text((x+12,y+10),name,font=font(19),fill=(25,50,65))
 save(canvas,out/'contact.jpg');(out/'review-manifest.json').write_text(json.dumps(dict(source_sha256=report['source_sha256'],images=names,scope='Source form checkpoint, no baked SUV GLB'),indent=2));print('SUV REVIEW',out/'contact.jpg',len(names),'views')
if __name__=='__main__':main()
