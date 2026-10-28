"""Original hammer comparisons: fixed visual camera estimates, no tracing.

The high-resolution open-cylinder photo supplies the rest profile; the target
photo supplies the cocked oblique cheek and roof. Their different viewpoints
remain explicit. Reference pixels never enter modeling or material code.
"""
import argparse,json,sys,math
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
ROWS={
 'hammer_rest_photo':dict(photo='open',crop=[2420,320,2980,730],
  shot=dict(location=(-.13,-.036,.078),target=(0,-.002,.067),ortho=.038,aspect=560/410),
  pose=dict(action='Idle',frame=0)),
 'hammer_cocked_photo':dict(photo='target',crop=[1650,720,2370,1350],
  shot=dict(location=(-.13,-.026,.080),target=(0,-.006,.064),ortho=.044,aspect=720/630,roll=.23),
  pose=dict(action='IdleCocked',frame=0)),
}
def compose(out):
 from PIL import Image,ImageDraw,ImageFont
 from kit.fonts import find_font
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),20)
 out.mkdir(parents=True,exist_ok=True)
 for name,row in ROWS.items():
  photo=Image.open(BASE/'build/references'/(row['photo']+'.png')).convert('RGBA').crop(row['crop'])
  render=Image.open(BASE/'renders/checkpoint/hammer'/(name+'.png')).convert('RGBA')
  w=900;h=round(w*photo.height/photo.width)
  pair=Image.new('RGB',(2*w,h+110),(235,237,233));draw=ImageDraw.Draw(pair)
  for i,im in enumerate((render,photo)):
   im=im.resize((w,h),Image.Resampling.LANCZOS);bg=Image.new('RGBA',im.size,(235,237,233,255));bg.alpha_composite(im)
   pair.paste(bg.convert('RGB'),(i*w,48))
  draw.text((15,12),name.replace('_photo','').replace('_',' ')+' / imported GLB',font=font,fill=(25,35,30))
  draw.text((w+15,12),'Reference photograph / estimated matching angle',font=font,fill=(25,35,30))
  draw.text((15,h+62),'Curved cheek, rising spur and fine pitch / original geometry / photograph for comparison only',font=font,fill=(25,35,30))
  pair.save(out/(name+'-pair.jpg'),quality=94,optimize=True)
def main():
 if '--compose' in sys.argv:
  compose(BASE/'renders/checkpoint/hammer-pairs');return
 import shots,interface
 from guns.common.render import main as render
 cameras={}
 for name,row in ROWS.items():
  cameras[name]=dict(title=name,shot=row['shot'],crop=row['crop'])
  shots.PHOTO_POSES[name]=row['pose']
 path=BASE/'build/hammer-cameras.json';path.write_text(json.dumps(cameras,indent=2))
 sys.argv+=['--camera-file',str(path)]
 render(shots,interface)
if __name__=='__main__':main()
