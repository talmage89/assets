"""Rebuild the last form fixes and their measured photographic evidence."""
import os,sys,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path[:0]=[str(ROOT),str(BASE/'src')]
from kit.fonts import find_font
from kit.photo_match import compose
from final_review import sheet

def main():
 out=BASE/'renders/form3';out.mkdir(parents=True,exist_ok=True)
 env=os.environ.copy();env.pop('PD_LEVER_FINAL',None)
 def render(folder,shots,cameras=None):
  cmd=[str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python','src/render.py','--','--source','build/lever.glb','--out',str(folder),'--shots',shots,'--width','1440','--samples','32']
  if cameras:cmd+=['--camera-file',str(cameras)]
  subprocess.run(cmd,cwd=BASE,env=env,check=True)
 render(out,'sights,sight_blade,wrist_raking,hammer,lever_rest_ortho,lever_mid_ortho,lever_open_ortho,aimed')
 names=('lever_rest_photo','hammer_photo','sight_photo');cal=json.loads((BASE/'build/cameras.json').read_text());subset={n:cal[n] for n in names}
 path=BASE/'build/form3-cameras.json';path.write_text(json.dumps(subset,indent=2))
 render(out/'pairs',','.join(names),path);compose(path,out/'pairs',out/'pairs')
 sheet([(n,out/'pairs'/(n+'-pair.jpg')) for n in names]+[('Wrist / raking inspection',out/'wrist_raking.png')],out/'form-fixes.jpg',columns=1,width=1800,height=540)
 sheet([(n,out/(n+'.png')) for n in ('lever_rest_ortho','lever_mid_ortho','lever_open_ortho')],out/'lever-stroke.jpg',columns=3,width=1800,height=620)
 # The ruler is not coplanar with the photographed blade. Keep both the
 # ruler estimate and the independent seller's actual blade measurement.
 scale=251/25.4
 native=dict(ruler_one_inch=((112,295),(363,298)),blade_height=((151,110),(151,210)),
             ear_rise=((152,110),(152,126)),notch_width=((201,126),(221,126)),notch_depth=((211,123),(211,135)))
 report=dict(photo='rear-blade.jpg',author='Homestead Parts',license='copyrighted comparison photograph',ruler_pixels_per_mm=scale,
  native_endpoints=native,ruler_estimates_mm={k:((a[0]-b[0])**2+(a[1]-b[1])**2)**.5/scale for k,(a,b) in native.items() if k!='ruler_one_inch'},
  published_blade_height_mm=.355*25.4,published_notch_height_mm=.270*25.4,
  adopted_design_mm=dict(height=9,ear_rise=2.2,notch_width=2.02,notch_depth=1.25,sheet_thickness=1.1),
  limits='Ruler/blade perspective differs; photographed insert has different two-screw mounting and rounded ears. Coin gauge is an authored visible construction estimate. The exact Eye frame and notch shoulders remain unchanged.')
 (BASE/'build/final-form-measurements.json').write_text(json.dumps(report,indent=2))
 im=Image.open(BASE/'build/white-balanced/rear-blade.png').convert('RGB');draw=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('Noto Sans','Regular'),12)
 for i,(name,(a,b)) in enumerate(native.items()):
  color=('red','lime','yellow','cyan','magenta')[i];draw.line((*a,*b),fill=color,width=2);draw.text((8,8+i*16),name,font=font,fill=color,stroke_width=1,stroke_fill='black')
 im.save(out/'sight-measurements.jpg',quality=95,optimize=True)
 print('FORM FIXES',out/'form-fixes.jpg',flush=True)
if __name__=='__main__':main()
