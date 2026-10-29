"""Exact player-camera panels alongside the calibrated photographic pairs.

All gun panels are reimports of the delivered baked GLB. The elevated rear
photograph is never represented as an eye-fit calibration or used to move Eye.
"""
import json,hashlib,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1];OUT=BASE/'renders/checkpoint'
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),23)
SMALL=ImageFont.truetype(find_font('Noto Sans','Regular'),18)

def main():
 digest=hashlib.sha256((BASE/'export/sxs.glb').read_bytes()).hexdigest()
 meta=json.loads((OUT/'beauty/shots.json').read_text());photos=json.loads((OUT/'photos/shots.json').read_text())
 calibration=json.loads((BASE/'build/cameras.json').read_text());records=[]
 for filename,player,reference,label in [
  ('aimed-pair','aimed','aimed_reference','Exact Socket_Eye / accepted 45 mm camera'),
  ('open-player-pair','open','open','Exact open player view / accepted camera'),
  ('open-breech-pair','open','breech_reference','Exact open player view / Commons comparison')]:
  assert meta[player]['sha256']==digest and photos[reference]['sha256']==digest
  raw=Image.open(OUT/'beauty'/(player+'.png')).convert('RGBA')
  row=calibration[reference];photo=Image.open(row['photo']).convert('RGB').crop(row['crop'])
  matched=Image.open(OUT/'pairs'/(reference+'-pair.jpg')).convert('RGB')
  width=matched.width;panel_w=width//2;panel_h=round(panel_w*.625)
  sheet=Image.new('RGB',(width,panel_h+matched.height+155),(238,239,236));draw=ImageDraw.Draw(sheet)
  draw.text((18,12),label,font=FONT,fill=(22,38,29))
  for image,x in [(raw,0),(photo,panel_w)]:
   background=Image.new('RGBA',(panel_w,panel_h),(88,91,95,255))
   image=ImageOps.contain(image,(panel_w,panel_h),Image.Resampling.LANCZOS).convert('RGBA')
   background.alpha_composite(image,((panel_w-image.width)//2,(panel_h-image.height)//2))
   sheet.paste(background.convert('RGB'),(x,55))
  draw.text((18,panel_h+68),'Upper row: player camera and photograph; different viewpoints. Lower rows: calibrated photographic view and residual arrows.',font=SMALL,fill=(35,49,41))
  if reference=='aimed_reference':
   draw.text((18,panel_h+96),'Rear photograph is above the rib and to one side; it supplies head/rib context, not an anatomical or exact eye-height claim.',font=SMALL,fill=(35,49,41))
  sheet.paste(matched,(0,panel_h+145));sheet.save(OUT/'pairs'/(filename+'.jpg'),quality=94,optimize=True)
  records.append(dict(pair=filename,player_shot=player,photo_shot=reference,source_sha256=digest))
 (OUT/'pairs/player-provenance.json').write_text(json.dumps(records,indent=2))
if __name__=='__main__':main()
