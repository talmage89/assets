"""Reference-only cheek-weld estimate, including the uncertain silhouette baseline."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1]
def main():
 # Native pixel observations, approximate because the pupil is shadowed and
 # the gun recedes. Receiver span is an assumed class envelope, not a known
 # manufacturing dimension. It supplies an explicit uncertainty, not precision.
 eye=(760,852);notch=(1380,755);rear=(847,871);front=(1440,815)
 axis=(front[0]-rear[0],front[1]-rear[1]);length=math.hypot(*axis)
 scale=length/255;distance=((notch[0]-eye[0])*axis[0]+(notch[1]-eye[1])*axis[1])/length/scale
 report=dict(reference='refs/weld.jpg',eye_pixels=eye,rear_notch_pixels=notch,
  receiver_end_pixels=[rear,front],assumed_receiver_envelope_mm=255,
  estimated_eye_to_notch_mm=distance,estimated_uncertainty_mm=35,
  authored_eye_to_notch_mm=295,limits='shadowed pupil, perspective and assumed exterior scale; no ergonomic certification')
 out=BASE/'renders/checkpoint';out.mkdir(parents=True,exist_ok=True)
 im=Image.open(BASE/'build/white-balanced/weld.jpg').convert('RGB').crop((650,700,1500,1010))
 d=ImageDraw.Draw(im)
 for a,b,color in [(eye,notch,'red'),(rear,front,'cyan')]:
  d.line((a[0]-650,a[1]-700,b[0]-650,b[1]-700),fill=color,width=3)
 im.save(out/'cheek-weld.jpg',quality=94)
 (BASE/'build/cheek-weld.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
