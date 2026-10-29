"""Local before/after/photo evidence for the four final corrections.

The optional before folder contains the preserved 27f07da GLB renders. Only
comparison images read reference pixels; geometry, shaders and exports do not.
"""
import argparse,json,hashlib,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parents[1]))
from kit.fonts import find_font

ROWS={
 'rod':('rod_detail','open',(680,600,1400,1080),'Shaft 5.80 mm; knurled head 6.40 mm; original endpoints and extraction'),
 'spur':('hammer_rest_photo','open',(2420,320,2980,730),'Near-tip thickness 5.44 mm; broad rounded end; original width and roof cuts'),
 'spur-cocked':('hammer_cocked_photo','target',(1650,720,2370,1350),'Same spur in the accepted cocked pose; crescent body and checker field retained'),
 'lug-front':('muzzle','muzzle-front',(1510,850,2010,1280),'Rounded section, continuous barrel/lug side and head within the rolled nose'),
 'lug-below':('lug_under','quarter',(0,490,1150,1250),'Rounded underside and nose; narrow opening follows the actual leftward departure'),
 'slot':('rear_slot','rear-top',(170,65,294,174),'Rear crown rounds down; 8.00 mm body cut below the wider 9.92 mm spur'),
}

def main():
 p=argparse.ArgumentParser();p.add_argument('--before',type=Path,required=True)
 p.add_argument('--after',type=Path,default=BASE/'renders/final')
 p.add_argument('--out',type=Path,default=BASE/'renders/final/fixes')
 a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),22)
 small=ImageFont.truetype(find_font('Noto Sans','Regular'),17)
 manifest={}
 expected_after=hashlib.sha256((BASE/'export/revolver.glb').read_bytes()).hexdigest()
 expected_before=hashlib.sha256((a.before/'revolver.glb').read_bytes()).hexdigest()
 for name,(shot,photo,crop,note) in ROWS.items():
  if shot.startswith('hammer_') and shot.endswith('_photo'):
   before=a.before/'final/hammer'/(shot+'.png');after=a.after/'hammer'/(shot+'.png')
  else:
   before=a.before/'matched'/(shot+'.png');after=a.after/'beauty'/(shot+'.png')
  bm=json.loads((before.parent/'shots.json').read_text())[shot]
  am=json.loads((after.parent/'shots.json').read_text())[shot]
  assert bm['sha256']==expected_before and am['sha256']==expected_after,shot
  for key in ('location','target','lens','ortho','aspect','roll','action','frame','exposure'):
   assert bm.get(key)==am.get(key),(shot,key,'different before/after camera or pose')
  balanced=BASE/'build/references'/(photo+'.png')
  reference=balanced if balanced.exists() else BASE/'refs'/(photo+'.jpg')
  images=[Image.open(before).convert('RGBA'),Image.open(after).convert('RGBA'),Image.open(reference).convert('RGBA').crop(crop)]
  w,h=700,540;canvas=Image.new('RGB',(w*3,h+140),(235,237,233));d=ImageDraw.Draw(canvas)
  for i,(im,label) in enumerate(zip(images,('Before / 27f07da baked GLB','After / current baked GLB','Reference photograph / form'))):
   im.thumbnail((w-16,h-16),Image.Resampling.LANCZOS)
   bg=Image.new('RGBA',im.size,(235,237,233,255));bg.alpha_composite(im)
   canvas.paste(bg.convert('RGB'),(i*w+(w-im.width)//2,60+(h-im.height)//2))
   d.text((i*w+12,14),label,font=font,fill=(25,35,30))
  d.text((12,h+68),note,font=font,fill=(25,35,30))
  d.text((12,h+103),'Identical before/after camera and lighting; photo angle/scale estimated. Photographs are comparison only.',font=small,fill=(45,55,48))
  canvas.save(a.out/(name+'.jpg'),quality=94,optimize=True)
  manifest[name]=dict(shot=shot,before_sha256=hashlib.sha256(before.read_bytes()).hexdigest(),after_sha256=hashlib.sha256(after.read_bytes()).hexdigest(),reference=reference.name,crop=crop,note=note)
 (a.out/'evidence.json').write_text(json.dumps(manifest,indent=2))
 # Each requested region can be opened as one image, including both poses
 # for the hammer and both directions for the lug.
 for name,parts in [('hammer',('spur','spur-cocked')),('lug',('lug-front','lug-below'))]:
  panels=[Image.open(a.out/(n+'.jpg')) for n in parts]
  sheet=Image.new('RGB',(panels[0].width,sum(im.height for im in panels)),(235,237,233));y=0
  for im in panels:sheet.paste(im,(0,y));y+=im.height
  sheet.save(a.out/(name+'.jpg'),quality=94,optimize=True)
 print('FOUR-REGION BEFORE / AFTER / PHOTO',a.out)

if __name__=='__main__':main()
