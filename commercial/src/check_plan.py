"""Grammar bounds and continuous sampled vehicle paths; no Blender dependency."""
import json,math,sys
from pathlib import Path
from plan import generate,rotate,PROOF_SEEDS,FT


def rect(center,width,length,yaw):
 return [(center[0]+u,center[1]+v) for u,v in [rotate((x,y),yaw) for x,y in ((-width/2,-length/2),(width/2,-length/2),(width/2,length/2),(-width/2,length/2))]]


def separation(a,b):
 """Signed separating-axis gap. Negative implies polygon penetration."""
 gaps=[]
 for poly in (a,b):
  for p,q in zip(poly,poly[1:]+poly[:1]):
   nx,ny=-(q[1]-p[1]),q[0]-p[0];le=math.hypot(nx,ny);nx/=le;ny/=le
   aa=[x*nx+y*ny for x,y in a];bb=[x*nx+y*ny for x,y in b]
   gaps.append(max(min(aa)-max(bb),min(bb)-max(aa)))
 return max(gaps)


def path(p):
 """Forward-only pickup route through the outer lane, on true 4.8m-radius arcs.

Body yaw 0 faces +Y, +90 faces -X. Every quarter/partial arc is sampled at
one degree; straight segments at <=.12m. Entrance crossings are also checked.
 """
 c=p['canopy'];R=4.8;W,D=p['lot'];cy=c['center'][1];pts=[]
 entrance=p['driveways'][0]['center'][0]
 def line(a,b,yaw):
  n=max(1,math.ceil(math.dist(a,b)/.12))
  pts.extend((a[0]+(b[0]-a[0])*i/n,a[1]+(b[1]-a[1])*i/n,yaw) for i in range(n+1))
 def arc(a,low,high):
  sign=1 if high>low else -1;n=abs(high-low)
  for i in range(n+1):
   theta=math.radians(low+(high-low)*i/n);t0=math.radians(low)
   x=a[0]+sign*R*(math.cos(theta)-math.cos(t0))
   y=a[1]+sign*R*(math.sin(theta)-math.sin(t0))
   pts.append((x,y,math.degrees(theta)))
  return pts[-1][:2]
 if c['angle']==0:
  end_y=p['parking_front']-1.95;start=(entrance,end_y-R)
  line((entrance,-D/2-6),start,0);end=arc(start,0,90)
  line(end,(-W/2-6,end[1]),90)
 elif c['angle']==90:
  end_y=cy+c['pitch']/2+2.0;start=(entrance,end_y-R)
  line((entrance,-D/2-6),start,0);end=arc(start,0,90)
  line(end,(-W/2-6,end_y),90)
 else:
  fx,fy=rotate((-(c['count']-1)/2*c['pitch']-3.35,0),30);fy+=cy
  west_y=fy-R*.5
  start=(entrance,west_y-R);line((entrance,-D/2-6),start,0)
  end=arc(start,0,90)
  second=(fx+R*math.cos(math.radians(30)),west_y)
  line(end,second,90);end=arc(second,90,30)
  third=(end[0]-6,end[1]+12*math.cos(math.radians(30)))
  line(end,third,30);end=arc(third,30,90)
  line(end,(-W/2-6,end[1]),90)
 return pts


def entrance_clear(p,polygon):
 W,D=p['lot'];front,side=p['driveways'];margin=.02
 for x,y in polygon:
  if x>W/2 or y>D/2:return False
  if y<-D/2 and abs(x-front['center'][0])>front['width']/2-margin:return False
  if x<-W/2 and abs(y-side['center'][1])>side['width']/2-margin:return False
 return True


def traffic(p):
 c=p['canopy'];b=p['building'];obstacles=[]
 for isl in p['islands']:obstacles.append(('island_'+str(isl['index']),rect(isl['center'],c['island'][0]+.02,c['island'][1]+.02,c['angle'])))
 # Occupied parking row is an obstruction, not empty painted bays in this proof.
 obstacles.append(('occupied_parking',rect((b['center_x'],(p['parking_front']+b['front']-p['walk'])/2),b['width'],p['parking_depth'],0)))
 obstacles.append(('store',rect((b['center_x'],b['front']+b['depth']/2),b['width'],b['depth'],0)))
 obstacles.append(('price_sign',rect(p['sign_center'],(2.9 if p['sign']=='pylon' else 3.6)+.34,.80,p['sign_yaw'])))
 gaps=[];fail=[];entrance_fail=[]
 for i,(x,y,angle) in enumerate(path(p)):
  car=rect((x,y),2.14,5.70,angle)
  if not entrance_clear(p,car):entrance_fail.append(i)
  values=[(separation(car,ob),name) for name,ob in obstacles];v,name=min(values)
  gaps.append(v)
  if v<-.001:fail.append(dict(sample=i,obstacle=name,penetration_sat_m=-v))
 return dict(scope='5.70 x 2.14m rectangular body envelope, geometry in plan; not tire dynamics or opposing traffic',route='south street through outer fueling lane to west street; forward only; 4.8m center-radius arcs',samples=len(gaps),minimum_separating_gap_m=min(gaps),violations=fail,entrance_violations=entrance_fail,passed=not fail and not entrance_fail)


def main():
 for i in range(1000):generate(i)
 invalid=[dict(brand='shell'),dict(count=5),dict(store=(90,80,20)),dict(angle=44),dict(lot=(50,50)),dict(yaw=45),dict(wall='vinyl'),dict(sign_placement='roof')]
 for bad in invalid:
  try:generate(101,bad)
  except (AssertionError,ValueError):pass
  else:raise AssertionError('Accepted unsupported plan '+repr(bad))
 result=dict(plan_count=1000,rejected_controls=len(invalid),traffic={str(s):traffic(generate(s)) for s in PROOF_SEEDS})
 Path('build').mkdir(exist_ok=True);Path('build/plan-check.json').write_text(json.dumps(result,indent=2))
 print('PLAN 1000 passed,',len(invalid),'negative controls rejected')
 for s,r in result['traffic'].items():print('TRAFFIC',s,r['passed'],r['minimum_separating_gap_m'],len(r['violations']))
 if any(not v['passed'] for v in result['traffic'].values()):raise AssertionError('Circulation collision')

if __name__=='__main__':main()
