"""Coarse photographic rulers and arrows, with explicit scale uncertainty.

Only comparison code reads photographs. Neither model nor shaders import this.
The side view is calibrated by its 1040-mm class envelope and barrel direction.
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1]

def main():
 out=BASE/'renders/checkpoint';out.mkdir(parents=True,exist_ok=True)
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),24)
 small=ImageFont.truetype(find_font('Noto Sans','Regular'),19)
 def arrow(d,p,label,offset=(40,-35)):
  p=np.array(p,float);q=p+offset;d.line([tuple(q),tuple(p)],fill=(40,165,145),width=3)
  d.ellipse((p[0]-5,p[1]-5,p[0]+5,p[1]+5),outline=(40,165,145),width=3)
  d.text(tuple(q),label,font=font,fill=(20,45,35),stroke_fill=(238,241,233),stroke_width=2)
 # Bore direction, as opposed to the tilted stock's butt edge.
 muzzle=np.array((2080.,154.));barrel=np.array((1620.,215.));pad=np.array((95.,550.))
 u=(muzzle-barrel);u/=np.linalg.norm(u);down=np.array((-u[1],u[0]));ppm=np.dot(muzzle-pad,u)/1040
 marks={'comb rear':(185,418),'comb front':(477,361),'butt upper':(81,420),'butt toe':(103,665),'lower edge at grip':(557,490)}
 offsets={'comb rear':(-20,-125),'comb front':(-10,-115),'butt upper':(-65,-65),'butt toe':(10,65),'lower edge at grip':(25,50)}
 readings={}
 im=Image.open(BASE/'build/white-balanced/right.jpg').convert('RGB');d=ImageDraw.Draw(im)
 for i,(name,p) in enumerate(marks.items()):
  delta=np.array(p)-muzzle
  readings[name]=dict(pixel=p,station_y_mm=710+float(delta@u)/ppm,height_z_mm=105-float(delta@down)/ppm,uncertainty_mm=8)
  arrow(d,p,str(i+1)+' '+name,offsets[name])
 for p,t in [(barrel,'bore ruler'),(muzzle,'muzzle')]:arrow(d,p,t,(-150,55))
 panel=Image.new('RGB',(2126,1140),(238,240,234));panel.paste(im,(0,0));d=ImageDraw.Draw(panel)
 d.text((25,930),f'Side ruler: {ppm:.3f} px/mm | 1040-mm envelope | barrel direction | no texture transfer',font=font,fill=(25,45,35))
 for i,(name,r) in enumerate(readings.items()):
  d.text((25,974+i*29),f"{i+1}. {name}: station Y {r['station_y_mm']:.1f}, Z {r['height_z_mm']:.1f} mm; ±8 mm including perspective/scale.",font=small,fill=(25,45,35))
 panel.save(out/'photo-measurements.jpg',quality=94)
 # The aiming eye is behind the lens beside the sight, not the far lens.
 eye=np.array((1800.,748.));aperture=np.array((1719.,811.));post=np.array((1140.,1030.))
 axis=aperture-post;ratio=float((eye-aperture)@axis/(axis@axis));relief=ratio*558.5
 im=Image.open(BASE/'refs/weld_civilian.jpg').convert('RGB');d=ImageDraw.Draw(im)
 for p,t,off in [(eye,'estimated aiming-eye plane',(-330,-110)),(aperture,'rear aperture',(-300,95)),(post,'front post',(-200,90)),((1910,1000),'supported cheek contact',(70,80))]:arrow(d,p,t,off)
 crop=im.crop((900,500,2350,1250));panel=Image.new('RGB',(1450,910),(238,240,234));panel.paste(crop,(0,0));d=ImageDraw.Draw(panel)
 d.text((20,770),f'Projected eye/aperture ratio {ratio:.3f} × 558.5-mm authored sight radius gives {relief:.1f} mm.',font=font,fill=(25,45,35))
 d.text((20,813),'Use 85 mm. ±25 mm: eyewear hides the pupil; axial foreshortening is an affine approximation.',font=small,fill=(25,45,35))
 d.text((20,851),'This is a supported cheek weld; the hand contributes to cheek height. Not an anatomical fit certification.',font=small,fill=(25,45,35))
 panel.save(out/'eye-weld.jpg',quality=94)
 result=dict(side_pixels_per_mm=ppm,bore_unit_image=u.tolist(),stock=readings,
  butt_height_photo_mm=readings['butt upper']['height_z_mm']-readings['butt toe']['height_z_mm'],
  eye=dict(eye_pixel=eye.tolist(),aperture_pixel=aperture.tolist(),post_pixel=post.tolist(),projected_ratio=ratio,inferred_relief_mm=relief,authored_relief_mm=85,uncertainty_mm=25,scope='Photographic supported cheek station; hidden pupil and perspective limit precision.'),
  handguard=dict(section_width_mm=[62,68],section_height_mm=[57,66],corner_radius_mm=[3,7],rib_spacing_mm=[12,17],scope='Coarse exterior comparison across the ribbed-handguard photograph, not a manufacturer subpart specification.'),
  rear_sight=dict(aperture_outer_mm=[8,11],aperture_hole_mm=[2.3,3.4],ear_height_mm=[29,35],ear_thickness_mm=[1.3,2.2],knob_diameter_mm=[11,15],scope='Ratios in sight.jpg transferred at the approximately 38-mm exterior housing width; ±10% scale uncertainty.'),
  bipod=dict(retracted_photo_estimate_mm=[235,260],scope='Near leg in right.jpg, hinge-to-pad with the same side ruler. Published class manuals specify telescoping legs but do not publish individual leg lengths.'))
 (BASE/'build/reference-measurements.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
