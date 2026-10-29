"""Review-only landmark arrows on baked-export rakes; no model inputs."""
import math,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.photo_match import project
from kit.fonts import find_font
BASE=Path(__file__).resolve().parents[1]
FONT=ImageFont.truetype(find_font('Noto Sans','Regular'),21)
TITLE=ImageFont.truetype(find_font('Noto Sans','Regular'),27)

def arrow(draw,start,end,color=(80,238,226)):
 draw.line([start,end],fill=color,width=2)
 v=np.array(start)-end;length=np.linalg.norm(v)
 if length>1:
  v/=length;side=np.array([-v[1],v[0]]);q=np.array(end)
  draw.polygon([tuple(q),tuple(q+v*11+side*4),tuple(q+v*11-side*4)],fill=color)
 draw.ellipse((end[0]-3,end[1]-3,end[0]+3,end[1]+3),outline=color,width=2)

def main():
 out=BASE/'renders/checkpoint/landmarks';out.mkdir(parents=True,exist_ok=True)
 meta=json.loads((BASE/'renders/checkpoint/beauty/shots.json').read_text())
 gauges=json.loads((BASE/'build/serialization.json').read_text())['form_gauges']['action_round4']
 fence=gauges['fences'][0];radius=np.mean([r['radius_mm'] for r in gauges['bottom_edge_radius']]);slot=gauges['trigger_slots'][0]
 rows={
 'action_rake_right':[
  (f"Fence / barrel crowns: {fence['highest_mm']:.3f} / {fence['barrel_top_mm']:.3f} mm Z",(.0126,.115,.05735),(.20,.16)),
  ('One ground side plane',(.02595,.115,.022),(.36,.83)),
  ('Flush hinge end / same steel',(.02595,.170,.019),(.68,.73))],
 'action_rake_top':[
  (f"Pair: {gauges['fence_pair_width_mm']:.3f} mm / breech: {gauges['barrel_breech_width_mm']:.3f} mm",(.02595,.115,.044),(.04,.10)),
  (f"Short rear roll, about {fence['fitted_rounding_length_mm']:.3f} mm",(-.012635,.102,.0535),(.04,.84)),
  ('Valley returns between fences',(0,.111,.04924),(.57,.84))],
 'action_rake_bottom':[
  (f"Flush plate joint: largest step {gauges['maximum_bar_plate_step_mm']:.3f} mm",(0,.102,.001),(.04,.12)),
  (f'Lower arris: fitted radius {radius:.2f} mm',(.024,.135,.0055),(.50,.83)),
  (f"Blade slot: {slot['slot_width_mm']:.1f} mm / blade: {slot['blade_width_mm']:.1f} mm",(.0056,.064,.0047),(.04,.83))]}
 for name,labels in rows.items():
  raw=Image.open(BASE/'renders/checkpoint/beauty'/(name+'.png')).convert('RGBA')
  im=Image.new('RGBA',raw.size,(70,73,77,255));im.alpha_composite(raw);im=im.convert('RGB')
  draw=ImageDraw.Draw(im);draw.text((24,18),'Covey 26 / baked 2048 export / '+name.replace('action_rake_',''),font=TITLE,fill='white')
  shot=meta[name];direction=np.array(shot['target'])-shot['location'];direction/=np.linalg.norm(direction)
  parameters=np.array([math.atan2(direction[1],direction[0]),math.asin(direction[2]),*shot['location'],math.log(shot['lens']),shot.get('roll',0)])
  pixels,depth,_=project(parameters,np.array([row[1] for row in labels]),*im.size)
  for (label,point,pos),pixel in zip(labels,pixels):
   x=round(pos[0]*im.width);y=round(pos[1]*im.height)
   box=draw.textbbox((x,y),label,font=FONT);draw.rectangle((box[0]-5,box[1]-3,box[2]+5,box[3]+4),fill=(22,28,30))
   draw.text((x,y),label,font=FONT,fill=(215,255,248))
   start=(min(max(pixel[0],box[0]),box[2]),box[3]+7 if pixel[1]>y else box[1]-7)
   arrow(draw,start,tuple(pixel))
  im.save(out/(name+'-landmarks.jpg'),quality=94,optimize=True)
 (out/'provenance.json').write_text(json.dumps(dict(source_sha256=meta['action_rake_right']['sha256'],scope='Review-only arrows; measurements in serialization.json'),indent=2))
if __name__=='__main__':main()
