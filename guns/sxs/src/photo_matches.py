"""Round-two cameras observed on plain field boxlocks; images are review only.

The observation grid is the aspect-preserving preview used during inspection;
all fits and residuals use the original delivered pixels. No measurement here
is consumed by the geometry generator. White-balance patches stay explicit.
"""
import sys,json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from guns.common.photo_matches import L
BASE=Path(__file__).resolve().parents[1];REF=BASE/'refs';OUT=BASE/'build/references'
# Native size / inspected preview size. Preview coordinates are observations,
# never traced outlines or generator inputs.
GRIDS={**{f'plain-{i}':(1900,round(h*1900/w)) if w>=h else (round(w*1300/h),1300) for i,(w,h) in enumerate([(4767,1549),(4623,1866),(1876,4679),(4252,2615),(4359,2390),(2027,4234),(1899,3454),(4047,1858)])},
 'field-alt-0':(900,600),'field-alt-11':(900,600),'field-alt-21':(900,600)}
def px(photo,p):
 w,h=Image.open(REF/(photo+'.jpg')).size;gw,gh=GRIDS[photo]
 return tuple(v*f for v,f in zip(p,(w/gw,h/gh)))
def spec(photo,crop,title,location,target,landmarks,**kw):
 return dict(locked_view=title.startswith(('Right action','Left action','Top /','Bottom /','Triggers /','Open /','Splinter / right','Barrel flats')),photo=str(OUT/(photo+'.png')),crop=tuple(round(v) for v in (*px(photo,crop[:2]),*px(photo,crop[2:]))),
  title=title,location=location,target=target,lens=85,lens_bounds_mm=(45,160),
  landmarks=[L(world,px(photo,p),weight) for world,p,weight in landmarks],**kw)
def opened(p,angle=-30):
 from parameters import HINGE
 p=np.array(p,float);c=np.array(HINGE);t=math.radians(angle)
 return tuple(c+np.array([[1,0,0],[0,math.cos(t),-math.sin(t)],[0,math.sin(t),math.cos(t)]])@(p-c))
def prep():
 OUT.mkdir(parents=True,exist_ok=True);rows={}
 for name in GRIDS:
  im=ImageOps.exif_transpose(Image.open(REF/(name+'.jpg'))).convert('RGB');a=np.array(im)/255
  # Dealer black-background photographs have no defensible neutral. A neutral
  # must not be invented by assuming case colors or bluing are gray.
  patch=(40,30,180,130) if name.startswith('field-alt') else None
  if patch:
   x0,y0,x1,y1=patch;v=np.median(a[y0:y1,x0:x1],axis=(0,1));lin=np.where(v<=.04045,v/12.92,((v+.055)/1.055)**2.4)
   gains=np.dot(lin,[.2126,.7152,.0722])/lin
   linear=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)*gains
   a=np.where(linear<=.0031308,linear*12.92,1.055*np.maximum(linear,0)**(1/2.4)-.055)
   im=Image.fromarray(np.clip(a*255,0,255).astype('uint8'))
  else:gains=np.ones(3)
  im.save(OUT/(name+'.png'));rows[name]=dict(neutral_patch=patch,linear_gains=gains.tolist(),
   scope='form only, inspection constants; no color or wear acceptance',
   neutral='white dealer backdrop' if patch else 'none in frame; no quantitative hue comparison')
 (OUT/'whitebalance.json').write_text(json.dumps(rows,indent=2))
MATCHES={
 'left':spec('field-alt-0',(0,245,900,455),'Whole left / plain field boxlock (smaller gauge)',(-2,.2,.3),(0,.24,.02),[
  ((0,775.4,44),(31,300),1),((-12.6,115,57.4),(560,289),1),
  ((0,-304.6,-5),(868,352),.4),((0,-296.2,-117),(850,435),.4)]),
 'right':spec('field-alt-11',(0,240,900,450),'Whole right / plain field boxlock (smaller gauge)',(2,.2,.3),(0,.24,.02),[
  ((0,775.4,44),(875,295),1),((12.6,115,57.4),(333,286),1),
  ((0,-304.6,-5),(39,350),.4),((0,-296.2,-117),(52,435),.4)]),
 'action':spec('plain-3',(690,270,1580,780),'Right action / plain 12-gauge boxlock',(.7,.10,.15),(0,.10,.03),[
  ((26.1,115,44),(1040,485),1),((22,70,42),(850,400),1),
  ((19,70,7),(850,730),1),((25.95,170,19),(1470,630),1),
]),
 'action_left':spec('plain-4',(300,220,1100,735),'Left action / plain 12-gauge boxlock',(-.7,.10,.15),(0,.10,.03),[
  ((-26.1,115,44),(805,430),1),((-22,70,42),(995,350),1),
  ((-19,70,7),(1010,680),1),((-25.95,170,19),(400,590),1)]),
 'action_top':spec('plain-2',(110,660,380,1235),'Top / fences and forged lever',(.03,-.07,.7),(0,.075,.045),[
  ((26,115,44),(350,700),1),((-26,115,44),(140,700),1),
  ((0,94,55.5),(240,790),.7),((8,54,50),(240,1020),.7),
  ((0,5,24),(240,1145),.4)]),
 'action_bottom':spec('plain-5',(125,280,465,1110),'Bottom / rounded bar and trigger plate',(.15,.10,-.60),(0,.10,.015),[
  ((-24,140,8),(393,450),1),((24,140,8),(200,450),1),
  ((0,170,8),(298,330),1),((0,70,5),(290,715),1),
  ((4.1,46,-32),(240,900),.3)]),
 'forend':spec('plain-6',(180,20,505,1290),'Splinter / bottom and rear iron',(.09,.28,-.6),(0,.27,.025),[
  ((0,355,30),(338,55),1),((0,185,14),(345,1230),1),
  ((-17.3,211,15),(465,1050),.7),((17.3,211,15),(220,1050),.7)]),
 'forend_side':spec('plain-1',(1030,235,1490,325),'Splinter / right side',(.7,.27,.10),(0,.27,.025),[
  ((17,188,20),(1100,287),1),((0,355,30),(1458,272),1),
  ((16,250,14),(1230,300),.5),((12,320,19),(1380,288),.5)]),
 'trigger':spec('plain-3',(290,730,910,1050),'Triggers / front-right, rear-left',(.5,.055,-.09),(0,.055,-.01),[
  ((4.1,10,-9),(350,840),1),((4.1,94,7),(800,760),1),
  ((4.1,72,-32),(600,1010),1),((4.1,100,-14),(855,860),1),
  ((2.6,71,-23),(602,980),.3),((-2.6,38,-23),(411,980),.3)]),
 'open':spec('plain-7',(670,130,1090,520),'Open / empty plain boxlock, pose matched',(-.5,.5,.14),(0,.13,.045),[
  (opened((-12.6,115,57.35)),(940,295),1),
  (opened((12.6,115,57.35)),(905,235),1),
  ((-26,115,44),(962,370),.8),((-22,70,30),(1060,435),.7)]),
 'barrel_flats':spec('field-alt-21',(0,0,900,600),'Barrel flats and lump / reference detached',(-.03,0,-.45),(0,.14,.03),[
  (opened((12.6,115,31)),(665,440),1),(opened((-12.6,115,31)),(670,150),1),
  (opened((0,170,19)),(218,290),1),(opened((0,119,29.5)),(639,295),.7)])}
# Round-three observations. Only shared class features calibrate cameras;
# outlines below are generated separately for review and never fit geometry.
def observed(name,points,location=None,target=None,crop=None):
 row=MATCHES[name];photo=Path(row['photo']).stem
 row['landmarks']=[dict(L(world,px(photo,pixel),weight),name=label) for label,world,pixel,weight in points]
 if location:row['location']=location
 if target:row['target']=target
 if crop:row['crop']=tuple(round(v) for v in (*px(photo,crop[:2]),*px(photo,crop[2:])))
 row['lens']=150;row['lens_bounds_mm']=(150,150)
observed('action',[
 ('breech crown',(12.6,115,57.35),(1043,311),1),
 ('breech lower corner',(24.0,115,31),(1045,531),1),
 ('hinge pin center',(25.95,170,19),(1421,625),1),
 ('front trigger root',(2.6,71,7),(700,755),.7)],
 location=(.9,.1,.13),target=(0,.1,.03),crop=(600,260,1530,820))
observed('action_left',[
 ('breech crown',(-12.6,115,57.35),(805,270),1),
 ('breech lower corner',(-24,115,31),(803,480),1),
 ('hinge pin center',(-25.95,170,19),(402,580),1)],
 location=(-.9,.1,.13),target=(0,.1,.03))
observed('action_top',[
 ('breech right corner',(25.95,115,44),(350,700),1),
 ('breech left corner',(-25.95,115,44),(141,703),1),
 ('lever boss center',(0,94,49),(231,800),1),
 ('lever tail',(.6,21,29),(263,1071),.35),
 ('safety center',(0,5,24),(260,1120),.4)],
 location=(.02,-.03,.8),target=(0,.075,.045))
observed('action_bottom',[
 ('hinge pin center',(-25.95,170,19),(382,337),1),
 ('front guard seat',(0,74,7),(268,699),1),
 ('rear guard seat',(0,10,-9),(252,1081),1)],
 location=(-.32,.1,-.70),target=(0,.1,.015))
observed('trigger',[
 ('front guard seat',(0,74,7),(725,760),1),
 ('rear guard seat',(0,10,-9),(318,840),1),
 ('front trigger root',(2.6,71,7),(700,755),1),
 ('front guard arc',(0,100,-14),(855,860),.6)],
 location=(.8,.055,-.09),target=(0,.055,-.01))
# An open-camera fit uses the barrel's actual outer rim and fixed hinge.
# The photo's top extension is not a landmark: our under-lug class differs.
observed('open',[
 ('far breech crown',opened((12.6,115,57.35)),(866,169),1),
 ('near breech crown',opened((-12.6,115,57.35)),(864,209),1),
 ('near breech heel',opened((-12.6,115,30.65)),(906,342),1),
 ('hinge pin center',(-25.95,170,19),(723,460),1)],
 location=(-.5,.5,.14),target=(0,.13,.045),crop=(660,130,1070,500))
for name,row in MATCHES.items():
 if name not in ('left','right'):
  row.update(lens=150,lens_bounds_mm=(150,150),locked_view=True)
if __name__=='__main__':prep()
