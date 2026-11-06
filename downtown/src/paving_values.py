"""Stated dry-pavement image-value controls under the Auburn matched light.

The neutral is the existing sunlit unpainted apron, not the yellow curb.
Rendered patches are projected ground quads, inspected in the outlined image.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit.photo_match import project
from values import stats
QUADS={'sunlit concrete':[(-5,-2,0),(-4.3,-2,0),(-4.3,-1.78,0),(-5,-1.78,0)],'sunlit asphalt':[(-27,-10,-.1524),(-26.3,-10,-.1524),(-26.3,-9.78,-.1524),(-27,-9.78,-.1524)]}

def run():
 c=json.loads(Path('build/cameras.json').read_text())['auburn_block'];photo=Image.open(c['photo']).convert('RGB');render=Image.open('renders/matches/raw/auburn_block.png').convert('RGB')
 s=c['shot'];loc=np.array(s['location']);direction=np.array(s['target'])-loc
 params=[math.atan2(direction[1],direction[0]),math.atan2(direction[2],np.linalg.norm(direction[:2])),*loc,math.log(s['lens']),s.get('roll',0)]
 photo_boxes={'sunlit concrete':[(1050,1982,1130,2005)],'sunlit asphalt':[(800,2250,1000,2320),(1600,2220,1790,2280),(2050,2140,2210,2200)]}
 quads=QUADS
 rays=json.loads(Path('renders/matches/midwest/provenance.json').read_text())['auburn_block'].get('paving_geometric_rays',{})
 rows=[];pd=ImageDraw.Draw(photo);rd=ImageDraw.Draw(render)
 for label,boxes in photo_boxes.items():
  measurements=[]
  for box in boxes:
   mask=Image.new('1',photo.size);ImageDraw.Draw(mask).rectangle(box,fill=1);measurements.append(stats(np.asarray(photo),np.asarray(mask).astype(bool)));pd.rectangle(box,outline='magenta',width=3)
  uv,depth,_=project(np.array(params),np.array(quads[label]),render.width,render.height)
  mask=Image.new('1',render.size);ImageDraw.Draw(mask).polygon([tuple(v) for v in uv],fill=1)
  if not np.asarray(mask).any():continue
  measured=stats(np.asarray(render),np.asarray(mask).astype(bool));rd.polygon([tuple(v) for v in uv],outline='magenta',width=2)
  checks=rays.get(label,{})
  assert checks and checks['camera']['blocker'] is None and checks['sun']['blocker'] is None,(label,'occluded measurement patch',checks)
  rows.append(dict(geometric_rays=checks,surface=label,photo_boxes=boxes,photo=measurements,render_world_quad=quads[label],render=measured))
 out=Path('renders/values');out.mkdir(exist_ok=True,parents=True);photo.save(out/'paving-photo.jpg',quality=95);render.save(out/'paving-render.jpg',quality=95)
 report=dict(white_balance=c['white_balance'],measurements=rows,scope='Exposed display image values, not measured reflectance. Dry Auburn pavement only; wet Louisiana paving is excluded. Outlined projected patches require visual surface/shadow review.')
 Path('build/paving-values.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PAVING VALUES',[(r['surface'],[round(v['display_luma_median'],3) for v in r['photo']],round(r['render']['display_luma_median'],3)) for r in rows])
if __name__=='__main__':run()
