"""Display-value comparisons on stated photo patches and matching world planes.

These diagnose render exposure and material value, never infer photographic
reflectance from uncalibrated files. Reference RGB is never used in asset maps.
"""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from kit.photo_match import project
from plan import generate

def stats(rgb,mask):
 p=rgb[mask]/255.;y=p@np.array((.2126,.7152,.0722))
 return dict(pixels=len(y),median_rgb=np.median(p,axis=0).tolist(),display_luma_median=float(np.median(y)),display_luma_p10_p90=np.percentile(y,[10,90]).tolist())

def run(folder="renders/matches",hero_path="renders/checkpoint/midwest/hero.png"):
 folder=Path(folder)
 cameras=json.loads(Path('build/cameras.json').read_text());rows=[];out=Path('renders/values');out.mkdir(parents=True,exist_ok=True)
 # Stop above the wall anchor: the earlier taller rectangle crossed hardware.
 definitions=[('louisiana_upper',(1006,1490,1050,1590),'Painted brick pier / overcast',3)]
 for name,box,label,index in definitions:
  c=cameras[name];im=Image.open(c['photo']).convert('RGB');mask=Image.new('1',im.size);ImageDraw.Draw(mask).rectangle(box,fill=1);photo=stats(np.asarray(im),np.asarray(mask).astype(bool));d=ImageDraw.Draw(im);d.rectangle(box,outline='magenta',width=2);im.save(out/(name+'-photo.jpg'),quality=94)
  path=folder/'raw'/(name+'.png')
  if not path.exists():continue
  render=Image.open(path).convert('RGB');s=c['shot'];loc=np.array(s['location']);direction=np.array(s['target'])-loc
  params=[math.atan2(direction[1],direction[0]),math.atan2(direction[2],np.linalg.norm(direction[:2])),*loc,math.log(s['lens']),s.get('roll',0)]
  p=generate(613 if c['region']=='northeast' else 411,c['region']);b=p['lots'][index];L=b['width']-b['chamfer'];left=b['x']-b['width']/2+(b['chamfer'] if b['corner']=='left' else 0)
  n=max(2,round((L-.6)/1.95));x=left+L/n*.5+.70;z=b['floor_first']+(b['stories']-2)*b['upper']+1.8
  if name=='auburn_store':x=b['x']-b['width']/2+1.95;z=.25
  points=[(x+dx,0,z+dz) for dx,dz in ((-.06,-.13),(.06,-.13),(.06,.13),(-.06,.13))]
  uv,depth,_=project(np.array(params),np.array(points),render.width,render.height);mask=Image.new('1',render.size);ImageDraw.Draw(mask).polygon([tuple(v) for v in uv],fill=1);measure=stats(np.asarray(render),np.asarray(mask).astype(bool));d=ImageDraw.Draw(render);d.polygon([tuple(v) for v in uv],outline='magenta',width=2);render.save(out/(name+'-render.jpg'),quality=94)
  rows.append(dict(pair=name,surface=label,photo_patch_pixels=box,render_world_patch=points,white_balance=c['white_balance'],photo=photo,render=measure))
 hero=Image.open(hero_path).convert('RGB');a=np.asarray(hero);y=a@np.array((.2126,.7152,.0722));report=dict(pairs=rows,hero_luma_percentiles=dict(zip(('p01','p05','p50','p95','p99'),np.percentile(y,[1,5,50,95,99]).tolist())),clipped_pixels=int(np.any(a==255,axis=2).sum()),scope='Exposed display RGB, not real-world albedo. Manual neutral assumptions and original differing facades limit the comparison.')
 Path('build/value-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--folder',default='renders/matches');p.add_argument('--hero',default='renders/checkpoint/midwest/hero.png');a=p.parse_args();run(a.folder,a.hero)
