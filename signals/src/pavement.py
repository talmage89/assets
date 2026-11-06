"""Dedicated used-road material comparison; no borrowed installation residual.

Nominal 42 mm, 1.6 m eye beside the approach curb. The seven fitted equipment
pairs remain separate. Actual ray probes certify what the color ROIs sample.
"""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font

def camera():
 source=json.loads(Path('build/cameras.json').read_text())['span']
 shot=dict(source['shot']);shot.pop('equipment_roots',None);shot.pop('phase',None)
 shot.update(location=[9.1,-40,1.7524],target=[1.6,-8,.2],lens=42,aspect=4/3,exposure=0,surface_pixels=[[1265,1350],[1130,1580],[1330,1660]])
 data=dict(title='Used intersection asphalt / nominal curbside viewpoint',seed=201,photo='refs/maryland-2006-balanced.jpg',crop=[0,0,2592,1944],presentation_crop=[300,1100,2200,1900],shot=shot,landmarks_world_m=[[6.7,-30,.012],[7.1,-33,.012],[7.7,-34,.012]],exposure_calibration=dict(inherited_exposure=-.5,exposure=0,reason='Half-stop field-exposure correction: unoccluded near white paint was Yprime .670 versus .889 in the balanced photograph; asphalt is measured separately. Different paint ages and camera response limit the inference.',photo_white_roi=[280,1480,300,1490],trial_render_white_roi=[246,239,254,244]),scope='Estimated ground-view camera, with sun/sky inherited from the Maryland shadow study and an explicit half-stop exposure correction. No equipment-fit RMS is claimed. Original lane/curb layouts differ; material rectangles require actual asphalt hits and sun-path probes.')
 Path('build/pavement-camera.json').write_text(json.dumps(dict(pavement=data),indent=2))

def compose(folder):
 folder=Path(folder);meta=json.loads((folder/'pavement.json').read_text());data=json.loads(Path('build/pavement-camera.json').read_text())['pavement']
 a=Image.open(folder/'pavement.png').convert('RGB');b=Image.open(data['photo']).convert('RGB').crop(data['presentation_crop']);width=1600;height=round(width*a.height/a.width)
 canvas=Image.new('RGB',(width*2,height+80),'#e5e7e2');draw=ImageDraw.Draw(canvas);font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),22)
 for i,(im,label) in enumerate(((a,'Exported road / actual surface probes'),(b,'Neutral-balanced used intersection photograph'))):
  canvas.paste(im.resize((width,height),Image.Resampling.LANCZOS),(i*width,40));draw.text((i*width+12,12),label,fill='#18302b',font=font)
 draw.text((12,height+54),'Nominal 42 mm / 1.6 m curbside viewpoint; estimated ground framing, no equipment-fit RMS. Different street layouts.',fill='#18302b',font=font)
 canvas.save(folder/'pavement-pair.jpg',quality=95,optimize=True)
 print('PAVEMENT PAIR',folder,meta.get('surface_probes'))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['camera','compose']);p.add_argument('--folder',default='renders/matches');a=p.parse_args();camera() if a.stage=='camera' else compose(a.folder)
