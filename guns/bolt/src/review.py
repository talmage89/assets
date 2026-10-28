"""Ignored checkpoint sheets and image/clip provenance, never final docs."""
import json,sys,hashlib,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(Path(__file__).parent)]
from kit.fonts import find_font
from interface import CLIPS
from shots import DEFAULT_SHOTS
font=ImageFont.truetype(find_font('Noto Sans','Regular'),22)
small=ImageFont.truetype(find_font('Noto Sans','Regular'),17)
OUT=BASE/'renders/checkpoint'
def panel(path,label,size=(600,395)):
 im=Image.open(path).convert('RGBA');im.thumbnail((size[0]-16,size[1]-48))
 canvas=Image.new('RGBA',size,(48,53,56,255));canvas.alpha_composite(im,((size[0]-im.width)//2,40+(size[1]-40-im.height)//2))
 ImageDraw.Draw(canvas).text((12,8),label,font=font,fill=(231,234,228));return canvas.convert('RGB')
def sheet(rows,path,cols=3,size=(600,395)):
 canvas=Image.new('RGB',(cols*size[0],math.ceil(len(rows)/cols)*size[1]),(48,53,56))
 for i,(p,label) in enumerate(rows):canvas.paste(panel(p,label,size),((i%cols)*size[0],(i//cols)*size[1]))
 canvas.save(path,quality=91,optimize=True)
def dimensions():
 """Project measured bounds into the actual orthographic render, in millimeters."""
 data=json.loads((BASE/'build/check.json').read_text())
 views=json.loads((OUT/'shots.json').read_text())
 lo,hi=data['bounds_m']['low'],data['bounds_m']['high']
 canvas=Image.new('RGB',(1500,1950),(48,53,56));ink=(231,234,228)
 for row,name in enumerate(('side','top','front')):
  im=Image.open(OUT/(name+'.png')).convert('RGBA');im.thumbnail((1440,530))
  ox,oy=(1500-im.width)//2,row*650+50
  canvas.paste(im,(ox,oy),im)
  draw=ImageDraw.Draw(canvas);draw.text((24,row*650+10),name+' | actual surface dimensions',font=font,fill=ink)
  target=views[name]['target'];scale=im.width/views[name]['ortho']
  def project(p):
   horizontal,vertical={'side':(p[1]-target[1],p[2]-target[2]),
     'top':(p[1]-target[1],-(p[0]-target[0])),
     'front':(-(p[0]-target[0]),p[2]-target[2])}[name]
   return ox+im.width/2+horizontal*scale,oy+im.height/2-vertical*scale
  def horizontal(a,b,y,label):
   x0,x1=sorted((project(a)[0],project(b)[0]));draw.line((x0,y,x1,y),fill=ink,width=2)
   for x in (x0,x1):draw.line((x,y-7,x,y+7),fill=ink,width=2)
   draw.text(((x0+x1)/2,y+9),label,font=small,fill=ink,anchor='mt')
  def vertical(a,b,x,label):
   y0,y1=sorted((project(a)[1],project(b)[1]));draw.line((x,y0,x,y1),fill=ink,width=2)
   for y in (y0,y1):draw.line((x-7,y,x+7,y),fill=ink,width=2)
   draw.text((x+13,(y0+y1)/2),label,font=small,fill=ink,anchor='lm')
  if name=='side':
   horizontal((0,lo[1],0),(0,hi[1],0),oy+im.height-25,f"Overall {(hi[1]-lo[1])*1000:.1f} mm | target 44-45 in")
   horizontal((0,hi[1]-data['barrel_length_m'],0),(0,hi[1],0),oy+45,f"Barrel {data['barrel_length_m']*1000:.1f} mm | target 24 in")
   horizontal((0,lo[1],0),(0,lo[1]+data['length_of_pull_m'],0),oy+im.height-83,f"Pull {data['length_of_pull_m']*1000:.1f} mm | target 13.5 in")
  elif name=='top':
   vertical((lo[0],0,0),(hi[0],0,0),ox+im.width-70,f"{(hi[0]-lo[0])*1000:.1f} mm")
   draw.text((24,row*650+610),'Width includes the oversized bolt handle; bipod folded in all orthographic views.',font=small,fill=ink)
  else:
   horizontal((lo[0],0,0),(hi[0],0,0),oy+im.height+12,f"Width {(hi[0]-lo[0])*1000:.1f} mm")
   vertical((0,0,lo[2]),(0,0,hi[2]),ox+im.width+20,f"Height {(hi[2]-lo[2])*1000:.1f} mm")
 canvas.save(OUT/'dimensions.jpg',quality=91,optimize=True)
def comparisons():
 """Historical GLB evidence stays separate from the current-source audit."""
 before=BASE/'renders/round1';out=OUT/'changes';out.mkdir(exist_ok=True)
 regions=[('bolt_rear','Bolt rear','rear_cocked.png','rear_cocked.png'),
  ('port','Port and raceway','port.png','port.png'),
  ('wrist','Wrist, inlet and comb nose','wrist.png','wrist.png'),
  ('butt','Butt taper and pad height','side.png','side.png'),
  ('bottom','Bottom metal and guard','bottom.png','bottom.png'),
  ('magazine','Five-round magazine','loaded/magazine.png','loaded/magazine.png'),
  ('bipod','Bipod tubes and molded boots','bipod_detail.png','bipod_detail.png'),
  ('barrel','Heavy barrel contour','side.png','side.png'),
  ('rings','Split caps and cross-bolt nuts','rings.png','rings.png'),
  ('reticle','Black etched reticle; coating still temporary','aimed.png','aimed.png')]
 index=[]
 for key,title,old,new in regions:
  path=out/(key+'.jpg');sheet([(before/old,'BEFORE | '+title),(OUT/new,'AFTER | '+title)],path,cols=2,size=(1000,650))
  index.append((path,title))
 # Same section station and scale treatment expose the old channel knife edge.
 old=Image.open(before/'sections/forend-sections.jpg').crop((0,0,600,600))
 new=Image.open(OUT/'sections/sections.jpg').crop((0,2400,600,3000))
 canvas=Image.new('RGB',(1200,650),(48,53,56));canvas.paste(old,(0,50));canvas.paste(new,(600,50))
 d=ImageDraw.Draw(canvas);d.text((12,8),'BEFORE | channel lips at Y=320 mm',font=small,fill='white');d.text((612,8),'AFTER | rounded channel lands',font=small,fill='white')
 path=out/'channel.jpg';canvas.save(path,quality=92,optimize=True);index.append((path,'Channel lands'))
 sheet(index,OUT/'changes.jpg',cols=2,size=(1100,420))
 sheet([(OUT/'rear_cocked.png','Our cocked tail'),(OUT/'rear_fired.png','Our fired tail'),
        (BASE/'refs/detail_032.jpg','Reference cocked | construction comparison'),
        (BASE/'refs/detail_033.jpg','Reference fired | cameras differ')],OUT/'rear-states.jpg',cols=2,size=(800,700))
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 names=DEFAULT_SHOTS.split(',')
 rows=[(OUT/(n+'.png'),n.replace('_',' ')) for n in names]
 sheet(rows,OUT/'form.jpg')
 dimensions()
 clips=[(OUT/'strips'/(n+'.jpg'),n) for n in CLIPS];sheet(clips,OUT/'clips.jpg',cols=3,size=(800,600))
 rows.extend([(OUT/'loaded/magazine.png','Loaded magazine'),(OUT/'empty/magazine.png','Empty magazine'),(OUT/'case/case.png','Fired case (400 triangles)')])
 rows.append((OUT/'case/case_mouth.png','Open fired mouth'))
 rows.append((OUT/'sections/sections.jpg','Measured sections: game/sculpt'))
 rows.extend([(OUT/'pairs'/(n+'-pair.jpg'),n.replace('_',' ')) for n in ('right_photo','profile_right','left_photo','open_photo','wrist_photo')])
 rows.extend([(OUT/'clips.jpg','All nine real-time clip strips')])
 sheet(rows,OUT/'contact-sheet.jpg',cols=3,size=(800,540))
 comparisons()
 provenance=[]
 for meta in OUT.rglob('shots.json'):
  for name,row in json.loads(meta.read_text()).items():
   source=Path(row['source']);actual=hashlib.sha256(source.read_bytes()).hexdigest()
   assert row['sha256']==actual,(meta,name,'stale render')
   assert (meta.parent/(name+'.png')).exists(),(meta,name)
   provenance.append(dict(image=str((meta.parent/(name+'.png')).relative_to(BASE)),source=str(source.relative_to(BASE)),sha256=actual))
 timing=json.loads((OUT/'strips/timing.json').read_text())
 for n,spec in CLIPS.items():assert timing[n]['encoded_duration_ms']==round(spec['frames']/60*1000)
 (BASE/'build/provenance.json').write_text(json.dumps(dict(passed=True,images=provenance,playback=timing),indent=2))
 import numpy as np
 values={}
 for name in ('right','left','grip','optic'):
  rgb=np.asarray(Image.open(OUT/(name+'.png')).convert('RGB'));luma=rgb@np.array([.2126,.7152,.0722])
  values[name]=dict(luma_percentiles=np.percentile(luma,[0,1,50,99,100]).tolist(),all_channel_clipped_pixels=int(np.all(rgb==255,axis=-1).sum()))
 (BASE/'build/tonal-range.json').write_text(json.dumps(dict(scope='render exposure only; includes studio, not recovered albedo',views=values),indent=2))
 print('Checkpoint sheets:',OUT/'contact-sheet.jpg',';',len(provenance),'current-source image records')
if __name__=='__main__':main()
