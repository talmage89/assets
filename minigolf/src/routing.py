"""Measured planning areas; lane points are sampled, never claimed as mesh tests."""
import json,math
from pathlib import Path
from plan import generate,center,halfwidth,local,level
from plan_check import hull

def area(poly):return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))/2

def measure(p,construction=None):
 outlines=[];green_area=0
 for h in p['holes']:
  outline=[]
  for side,sequence in ((-1,range(101)),(1,reversed(range(101)))):
   for j in sequence:
    t=j/100;cx,cy=center(h,t);outline.append(local(h,cx+side*halfwidth(h,t),cy)[:2])
  outlines.append(outline);green_area+=area(outline)
 envelope=hull([q for ring in outlines for q in ring]);x0,x1,y0,y1=p['play_bounds'];landscape_area=(x1-x0)*(y1-y0)
 if p['kind']=='classic':
  from paths import court
  landscape_area=area(court(p))
 values=[level(h,center(h,t)[0],t) for h in p['holes'] for t in (0,.5,1)]
 row=dict(kind=p['kind'],greens_m2=green_area,green_hull_m2=area(envelope),routing_area_m2=landscape_area,routing_area_basis='Sampled common-bed polygon around greens/walks, excluding perimeter beds' if p['kind']=='classic' else 'Authored 46 x 40 m routing window, including landscape',greens_fraction_of_routing_area=green_area/landscape_area,routing_holes_per_1000m2=18000/landscape_area,playing_z_minmax_m=[min(values),max(values)],water_crossings=[h['number'] for h in p['holes'] if h.get('crossing')],parcel_including_parking_m2=math.prod(p['lot']))
 if construction:
  bounds=[h['carpet_bounds_m'] for h in construction['holes'].values()]
  row['measured_source_carpet_z_minmax_m']=[min(b[0][2] for b in bounds),max(b[1][2] for b in bounds)]
  row['height_scope']='Actual source playing-face vertices; hole roots have zero Z translation. Separate from the three-station grammar samples above.'
  row['measured_fenced_play_enclosure_m2']=construction['fenced_play_enclosure_m2'];row['holes_per_1000m2_of_fenced_play']=18000/construction['fenced_play_enclosure_m2'];row['fence_area_scope']=construction['fence_measure_scope']
 return row

if __name__=='__main__':
 source=json.loads(Path('build/source-construction.json').read_text());rows=[measure(generate(seed,kind),source[str(seed)]) for seed,kind in ((71,'classic'),(92,'adventure'))]
 print(json.dumps(rows,indent=2));Path('build/routing.json').write_text(json.dumps(rows,indent=2))
