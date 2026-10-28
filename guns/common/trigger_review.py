"""Gun-owned trigger photo framing and comparison-only pair composition.

A kit landmark fit can be retained as a rejected diagnostic. Visually estimated
view directions and blade-height scale are explicit; optical shifts place the
reference crop without rotating the camera. No photograph enters an asset.
"""
import argparse,json,runpy,sys
from pathlib import Path
def cameras(BASE):
 from kit.photo_match import solve
 definitions=runpy.run_path(str(BASE/'src/trigger_matches.py'))['MATCHES']
 if all('landmarks' in m for m in definitions.values()):
  full=BASE/'build/trigger-cameras-full.json';solve(BASE/'src/trigger_matches.py',full)
  if 'bpy' in sys.modules:
   from kit.photo_match import verify
   verify(full)
  rows=json.loads(full.read_text())
 else:
  rows={name:dict(title=m['title'],photo=m['photo'],crop=m['crop'],shot={}) for name,m in definitions.items()}
 for name,row in rows.items():
  x,y,X,Y=definitions[name]['trigger_crop'];w,h=X-x,Y-y
  W,H=row['crop'][2:];shot=row['shot']
  if 'matched_view' in definitions[name]:
   import math,numpy as np
   m=definitions[name]['matched_view'];direction=np.array(m['direction'],float);direction/=np.linalg.norm(direction)
   # Match the observed upper-to-lower blade span. Only framing uses these
   # anchors; no silhouette pixels are sampled and no geometry is altered.
   target=np.array(m['target']);lens=70.;roll=m.get('roll',0)
   distance=(w*lens/36)*m['span_m']*math.sqrt(1-direction[2]**2)*math.cos(roll)/m['span_pixels']
   shot.update(location=(target+direction*distance).tolist(),target=target.tolist(),lens=lens,aspect=w/h,roll=roll,
    shift_x=.5-(m['anchor_pixel'][0]-x)/w,
    shift_y=((m['anchor_pixel'][1]-y)-h/2)/w)
   if 'residual_rms_pixels' in row:row['rejected_fit_rms_pixels']=row.pop('residual_rms_pixels')
   row['framing_method']='visual fixed-angle estimate; blade vertical span sets scale; surrounding guard remains independent'
  else:
   shot['shift_x']=((x+X)/2-W/2)/w
   shot['shift_y']=(H/2-(y+Y)/2)/w
   shot['lens']*=W/w;shot['aspect']=w/h
  shot.setdefault('exposure',-.15)
  row['crop']=[x,y,X,Y]
  for key in ('projected_pixels','measured_pixels'):
   if key in row:row[key]=[[a-x,b-y] for a,b in row[key]]
 out=BASE/'build/trigger-cameras.json';out.write_text(json.dumps(rows,indent=2));return out

def render(BASE,shots,interface):
 import bpy
 from guns.common.render import main
 path=cameras(BASE)
 original=shots.prepare_shot
 def prepare(scene,shot):
  original(scene,shot)
  scene.camera.data.shift_x=shot.get('shift_x',0)
  scene.camera.data.shift_y=shot.get('shift_y',0)
 shots.prepare_shot=prepare
 # Common camera loader keeps all shot fields, including the optical shifts.
 shots.PHOTO_POSES.update({name:dict(action='Idle',frame=0,trigger_light=True,daylight=1 if 'right' in name else -1)
  for name in json.loads(path.read_text())})
 if '--source-preview' in sys.argv:
  shots.FINAL_STAGE=False;shots.RENDER_STAGE='source procedural inspection';sys.argv.remove('--source-preview')
 sys.argv+=['--camera-file',str(path)]
 main(shots,interface)

def run(BASE,shots,interface):
 if '--compose' in sys.argv:
  p=argparse.ArgumentParser();p.add_argument('--compose',action='store_true');p.add_argument('--renders',required=True);p.add_argument('--out',required=True)
  a=p.parse_args()
  from PIL import Image,ImageOps,ImageDraw,ImageFont
  from kit.fonts import find_font
  out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
  font=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
  for name,row in json.loads((BASE/'build/trigger-cameras.json').read_text()).items():
   photo=ImageOps.exif_transpose(Image.open(row['photo'])).convert('RGBA').crop(row['crop'])
   render_image=Image.open(Path(a.renders)/(name+'.png')).convert('RGBA')
   w=1000;h=round(w*photo.height/photo.width)
   pair=Image.new('RGB',(2*w,h+100),(238,239,236));draw=ImageDraw.Draw(pair)
   for i,im in enumerate((render_image,photo)):
    im=im.resize((w,h),Image.Resampling.LANCZOS);panel=Image.new('RGBA',im.size,(238,239,236,255));panel.alpha_composite(im)
    pair.paste(panel.convert('RGB'),(i*w,50))
   draw.text((15,12),row['title']+' / original asset',font=font,fill=(22,38,29))
   draw.text((w+15,12),'Reference photograph / matched angle and blade scale',font=font,fill=(22,38,29))
   draw.text((15,h+65),'View angle estimated visually; original guard differs. Photo pixels are comparison only.',font=font,fill=(49,64,52))
   pair.save(out/(name+'-pair.jpg'),quality=94,optimize=True)
   print('TRIGGER PAIR',out/(name+'-pair.jpg'))
 else:render(BASE,shots,interface)
