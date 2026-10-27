"""Body landmark comparisons held out of the chassis camera calibration.

Photo pixels are hand measurements with +/- 10 px uncertainty in the 1500 px
inspection frame. Original styling differences remain visible, never fitted.
"""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
FONT=find_font('Noto Sans', 'Regular')
ROOT=Path(__file__).resolve().parents[1]
PICKS={
 'match_front_stripes':[
   ('H','hood_leading_center',(350,522)),('C','hood_rear_center',(662,415)),
   ('R','roof_rear_corner',(1198,224)),('F','f_arch_crown',(884,600)),
   ('D','f_draw_top',(884,521)),('B','r_arch_crown',(1379,520)),
   ('E','r_draw_top',(1379,452))],
 'match_rear_stripes':[
   ('R','roof_rear_corner',(975,224)),('C','roof_rear_center',(757,211)),
   ('F','f_arch_crown',(1418,532)),('D','f_draw_top',(1418,480)),
   ('B','r_arch_crown',(915,547)),('E','r_draw_top',(915,467))],
}


def main():
 p=argparse.ArgumentParser();p.add_argument('--renders',required=True);a=p.parse_args();out=Path(a.renders)
 shots=json.loads((out/'shots.json').read_text());cameras=json.loads((out/'matched-cameras.json').read_text())
 font=ImageFont.truetype(FONT,23);small=ImageFont.truetype(FONT,18);report={}
 for name,rows in PICKS.items():
  im=Image.open(out/(name+'-pair.jpg')).convert('RGB');d=ImageDraw.Draw(im)
  data=cameras[name];shot=shots[name];crop=data['crop'];full=crop[2]-crop[0];factor=1100/full
  records=[]
  for label,key,pixel in rows:
   photo=[q*1.4 for q in pixel];projected=[q*full/shot['width'] for q in shot['points'][key]]
   expected=[q-c for q,c in zip(photo,crop[:2])]
   for x,y,col in [(projected[0]*factor,projected[1]*factor+70,(230,95,15)),
                   (1100+expected[0]*factor,expected[1]*factor+70,(0,110,155))]:
    d.ellipse((x-6,y-6,x+6,y+6),outline=col,width=3);d.text((x+9,y-17),label,font=font,fill=col)
   delta=[p-q for p,q in zip(projected,expected)]
   records.append(dict(label=label,feature=key,photo_pixel_original=photo,
       render_pixel_original=[q+c for q,c in zip(projected,crop[:2])],render_minus_photo_pixels=delta,
       photographic_pick_uncertainty_pixels=14))
  # A dedicated footer clearly separates body differences from chassis RMS.
  canvas=Image.new('RGB',(im.width,im.height+125),(238,239,236));canvas.paste(im,(0,0));d=ImageDraw.Draw(canvas)
  d.text((18,im.height+10),'Held-out body landmarks: orange render / blue photo. These never enter camera calibration; picks +/- 14 source pixels.',font=small,fill=(45,55,60))
  labels='   '.join(f"{r['label']}: dx {r['render_minus_photo_pixels'][0]:+.0f}, dy {r['render_minus_photo_pixels'][1]:+.0f} px" for r in records)
  d.text((18,im.height+45),labels,font=small,fill=(45,55,60))
  d.text((18,im.height+80),'H hood front; C cowl / rear roof center; R rear roof corner; F/B front/rear opening crown; D/E broad draw top. Styling correspondence is approximate.',font=small,fill=(45,55,60))
  canvas.save(out/(name+'-measurements.jpg'),quality=94)
  report[name]=dict(chassis_rms_pixels=data['residual_rms_pixels'],body_landmarks=records,
                   caveat='Different original styling; hand-picked semantic correspondence, not a dimensional or all-body registration certificate.')
 (out/'form-comparisons.json').write_text(json.dumps(report,indent=2))
 # The second make supplies an independent design-language cross-check. This
 # sheet is explicitly not an extra calibrated pair.
 files=[ROOT/'refs/stock-rear.jpg',out/'rear_three_quarter.png',ROOT/'refs/ram-rear.jpg']
 labels=['Ford class reference / stock crew short bed','Alder C150 / original clay form','Ram class reference / rounded draw and cab']
 canvas=Image.new('RGB',(2400,780),(230,232,231));d=ImageDraw.Draw(canvas)
 d.text((20,16),'TWO CLASS REFERENCES / original grille, lamps and sculpting / views are not camera registered',font=font,fill=(35,45,50))
 for i,(path,label) in enumerate(zip(files,labels)):
  im=ImageOps.exif_transpose(Image.open(path)).convert('RGBA');im=ImageOps.contain(im,(780,650),Image.Resampling.LANCZOS)
  canvas.paste(im,(i*800+(800-im.width)//2,65+(650-im.height)//2),im)
  d.text((i*800+15,735),label,font=small,fill=(35,45,50))
 canvas.save(out/'class-crosscheck.jpg',quality=93)
 print('FORM COMPARISONS',out/'form-comparisons.json')


if __name__=='__main__':main()
