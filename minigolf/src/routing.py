"""Measured planning areas; lane points are sampled, never claimed as mesh tests."""
import json,math
from pathlib import Path
from plan import generate,center,halfwidth,local,level
from plan_check import hull

def area(poly):return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))/2

def measure(p):
 outlines=[];green_area=0
 for h in p['holes']:
  outline=[]
  for side,sequence in ((-1,range(101)),(1,reversed(range(101)))):
   for j in sequence:
    t=j/100;cx,cy=center(h,t);outline.append(local(h,cx+side*halfwidth(h,t),cy)[:2])
  outlines.append(outline);green_area+=area(outline)
 envelope=hull([q for ring in outlines for q in ring]);x0,x1,y0,y1=p['play_bounds'];landscape_area=(x1-x0)*(y1-y0)
 values=[level(h,center(h,t)[0],t) for h in p['holes'] for t in (0,.5,1)]
 return dict(kind=p['kind'],greens_m2=green_area,green_hull_m2=area(envelope),landscaped_play_enclosure_m2=landscape_area,greens_fraction=green_area/landscape_area,holes_per_1000m2=18000/landscape_area,playing_z_minmax_m=[min(values),max(values)],water_crossings=[h['number'] for h in p['holes'] if h.get('crossing')],parcel_including_parking_m2=math.prod(p['lot']))

if __name__=='__main__':
 rows=[measure(generate(71,'classic')),measure(generate(92,'adventure'))]
 print(json.dumps(rows,indent=2));Path('build/routing.json').write_text(json.dumps(rows,indent=2))
