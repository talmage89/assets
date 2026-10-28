"""Photo/render display medians; comparison pixels never reach the asset."""
from pathlib import Path
import json,math,sys,hashlib
import numpy as np
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parents[1]))
from kit.photo_match import project

def stats(im,polygon):
 mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(polygon,fill=255)
 return masked_stats(im,mask)
def masked_stats(im,mask):
 a=np.asarray(im.convert('RGB'),dtype=float)[np.asarray(mask)>0]
 assert len(a)>0
 rgb=np.median(a,axis=0);luma=a@np.array((.2126,.7152,.0722))
 return dict(pixels=len(a),median_rgb_255=rgb.tolist(),median_luma_255=round(float(np.median(luma)),2),
  luma_p20_p80_255=np.percentile(luma,[20,80]).round(2).tolist(),rgb_ratios_g1=(rgb/max(rgb[1],1)).round(4).tolist())
def measure(folder):
 folder=Path(folder);cal=json.loads((BASE/'build/cameras.json').read_text())['used_open']
 photo=Image.open(BASE/'build/white-balanced/open.png').convert('RGB');render=Image.open(folder/'used_open.png').convert('RGBA')
 # Manually picked native photographic polygons, without automatic material
 # classification. Stock samples the upper olive-gray paint; scope samples
 # an exposed black anodized strip; steel samples the unpainted rear bridge.
 patches={'stock':[(2110,1080),(2260,1060),(2260,1120),(2110,1140)],
          'steel':[(1140,985),(1310,965),(1310,1010),(1140,1030)],
          'scope':[(638,550),(677,550),(677,660),(638,665)]}
 loci={k:v['points_m'] for k,v in json.loads((BASE/'build/value-loci.json').read_text()).items()}
 shot=cal['shot'];loc=np.array(shot['location']);direction=np.array(shot['target'])-loc
 params=[math.atan2(direction[1],direction[0]),math.atan2(direction[2],np.linalg.norm(direction[:2])),*loc,math.log(shot['lens']),shot['roll']]
 rows={};marked=render.convert('RGB');annotated=photo.copy()
 for (name,points),color in zip(patches.items(),[(80,200,90),(240,100,60),(70,140,255)]):
  projected=project(params,np.array(loci[name]),render.width,render.height)[0].tolist()
  rows[name]=dict(photo=stats(photo,points),render=stats(render,projected),photo_polygon=points,render_polygon=projected)
  ImageDraw.Draw(annotated).line(points+[points[0]],fill=color,width=6)
  ImageDraw.Draw(marked).line(projected+[projected[0]],fill=color,width=3)
 canvas=Image.new('RGB',(1600,850),(225,226,222))
 for i,im in enumerate((marked,annotated.crop(cal['crop']))):
  im.thumbnail((1580,390),Image.Resampling.LANCZOS);canvas.paste(im,((1600-im.width)//2,35+i*400))
 ImageDraw.Draw(canvas).text((12,10),'Used daylight / green stock, orange steel, blue anodizing / display values, not recovered albedo',fill=(20,30,25))
 canvas.save(folder/'value-patches-used.jpg',quality=92,optimize=True)
 tonal={}
 for name in ('hero','hero_left','optic','wrist','bolt_open','grip','aimed'):
  path=folder.parent/'beauty'/(name+'.png')
  if not path.exists():continue
  a=np.asarray(Image.open(path).convert('RGBA'));rgb=a[:,:,:3][a[:,:,3]>128].astype(float);lum=rgb@np.array((.2126,.7152,.0722))
  tonal[name]=dict(luma_p1_p50_p99=np.percentile(lum,[1,50,99]).round(2).tolist(),deep_shadow_fraction=float(np.mean(lum<24)),clipped_fraction=float(np.mean(np.all(rgb>=254,axis=1))))
 result=dict(scope='daylight photographic versus neutral daylight-style rendered display patches; not recovered albedos',reference='open.jpg / USMC used field rifle, upper stock coat, exposed steel and black scope strip',patches=rows,tonal_ranges=tonal)
 # A separate diffuse-daylight field rifle verifies the blacks' range without
 # treating the reference's camouflage and our web paint as the same finish.
 ref=Image.open(BASE/'build/white-balanced/daylight.png').convert('RGB');scale=ref.width/2048
 secondary={'steel':[(455,507),(530,466),(539,487),(464,526)],'scope':[(635,338),(709,299),(719,317),(644,358)],'stock':[(876,262),(969,209),(972,238),(879,287)]}
 result['secondary_daylight']={name:stats(ref,[(x*scale,y*scale) for x,y in points]) for name,points in secondary.items()}
 result['surface_loci']=json.loads((BASE/'build/value-loci.json').read_text())
 result['measurement_source_sha256']={n:hashlib.sha256((BASE/'src'/n).read_bytes()).hexdigest() for n in ('value_review.py','value_loci.py')}
 result['glb_sha256']=json.loads((folder/'shots.json').read_text())['used_open']['sha256']
 result['white_balance']=json.loads((BASE/'build/white-balanced/corrections.json').read_text())
 from reference_measurements import measure as measure_references
 result['all_corrected_references']=measure_references()
 # The neutralized right-side rifle is the black-steel value target. Shade
 # camouflage remains an auxiliary stock/wear comparison, never a black target.
 right=Image.open(BASE/'build/white-balanced/left.png').convert('RGB')
 target_patches={'steel_barrel':[(920,130),(1040,130),(1040,140),(920,140)],
 'steel_barrel_full':[(920,128),(1040,128),(1040,144),(920,144)],
 'steel_receiver_full':[(450,119),(480,119),(480,129),(450,129)],
 'steel_barrel_lit':[(920,130),(1040,130),(1040,140),(920,140)],
 'steel_receiver':[(446,123),(480,123),(480,129),(446,129)],
 'scope':[(630,84),(680,84),(680,94),(630,94)],
 'scope_dark':[(430,91),(455,91),(455,98),(430,98)],
 'stock':[(600,145),(710,145),(710,160),(600,160)]}
 rc=json.loads((BASE/'build/cameras.json').read_text())['right_photo'];ri=Image.open(folder/'right_photo.png').convert('RGB')
 rs=rc['shot'];rl=np.array(rs['location']);rd=np.array(rs['target'])-rl
 rp=[math.atan2(rd[1],rd[0]),math.atan2(rd[2],np.linalg.norm(rd[:2])),*rl,math.log(rs['lens']),rs['roll']]
 result['right_photo_target']={}
 for name,polygon in target_patches.items():
  role='steel' if name=='steel_receiver' else name
  points=project(rp,np.array(loci[role]),ri.width,ri.height)[0].tolist()
  result['right_photo_target'][name]=dict(photo=stats(right,polygon),render=stats(ri,points),photo_polygon=polygon,render_polygon=points)
 combined={}
 for kind,im in [('photo',right),('render',ri)]:
  mask=Image.new('L',im.size);d=ImageDraw.Draw(mask)
  for role in ('steel_barrel_full','steel_receiver_full'):
   d.polygon(result['right_photo_target'][role][kind+'_polygon'],fill=255)
  combined[kind]=masked_stats(im,mask)
 result['right_photo_target']['steel_combined_visible']=combined
 result['right_photo_target']['scope_bell_visible']=dict(photo=stats(right,[(630,64),(680,64),(680,114),(630,114)]),render=result['right_photo_target']['scope_dark']['render'],note='Photo median across visible objective bell versus rendered diffuse tube; different surface normals. Highlight and dark-strip distributions are retained separately.')
 # Mark the actual primary masks, including both full visible steel patches.
 marked=ri.copy();annotated=right.copy()
 for name,color in [('steel_barrel_full',(240,100,60)),('steel_receiver_full',(240,100,60)),('scope_dark',(70,140,255))]:
  row=result['right_photo_target'][name]
  for im,kind in [(marked,'render'),(annotated,'photo')]:
   polygon=row[kind+'_polygon'];ImageDraw.Draw(im).line(polygon+[polygon[0]],fill=color,width=3)
 canvas=Image.new('RGB',(1600,890),(225,226,222))
 for i,im in enumerate((marked,annotated.crop(rc['crop']))):
  im.thumbnail((1580,390),Image.Resampling.LANCZOS);canvas.paste(im,((1600-im.width)//2,45+i*420))
 ImageDraw.Draw(canvas).text((12,12),'White-balanced right reference / full visible receiver + barrel masks, not just highlight strips',fill=(20,30,25))
 canvas.save(folder/'value-patches.jpg',quality=92,optimize=True)
 result['scope']='White-balanced photographs versus neutral-lit exported GLB display patches; no albedo recovery claimed. Right photo constrains black steel; shade photo is auxiliary.'
 (folder/'values.json').write_text(json.dumps(result,indent=2));return result
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--renders',type=Path,required=True);a=p.parse_args();print(json.dumps(measure(a.renders),indent=2))
