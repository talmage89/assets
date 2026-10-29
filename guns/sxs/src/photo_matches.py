"""Manual photographic landmarks calibrate only cameras, never geometry.

Coordinates are observations on native upright originals. The sharp underside
macro is rotated 25 degrees for a comparable camera roll. Calibration residuals
remain visible; these are different original field guns, not replica targets.
"""
import sys,math,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from guns.common.photo_matches import L
BASE=Path(__file__).resolve().parents[1];REF=BASE/'refs';OUT=BASE/'build/references'

def opened(p):
 from parameters import HINGE,OPEN
 p=np.array(p,float);c=np.array(HINGE);t=math.radians(OPEN)
 return tuple(c+np.array([[1,0,0],[0,math.cos(t),-math.sin(t)],[0,math.sin(t),math.cos(t)]])@(p-c))
def prep():
 OUT.mkdir(parents=True,exist_ok=True);rows={}
 for name,patch in [('class-side',None),('side-b',(80,40,540,260)),
  ('breech',(120,70,175,270)),('side-a',(1450,80,1950,300)),('open-empty',(112,405,159,453)),('open-candidate-5',(100,3500,550,3900))]:
  im=ImageOps.exif_transpose(Image.open(REF/(name+'.jpg'))).convert('RGB');a=np.array(im)/255
  if patch:
   x0,y0,x1,y1=patch;v=np.median(a[y0:y1,x0:x1],axis=(0,1));lin=np.where(v<=.04045,v/12.92,((v+.055)/1.055)**2.4)
   gains=np.dot(lin,[.2126,.7152,.0722])/lin
   linear=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)*gains
   a=np.where(linear<=.0031308,linear*12.92,1.055*np.maximum(linear,0)**(1/2.4)-.055)
   im=Image.fromarray(np.clip(a*255,0,255).astype('uint8'))
  else:gains=np.ones(3)
  im.save(OUT/(name+'.png'));rows[name]=dict(neutral_patch=patch,linear_gains=gains.tolist(),
   scope='form only; no finish accepted',neutral='colored wooden floor: no reliable neutral' if patch is None else 'white sheet' if name in ('side-a','side-b','open-candidate-5') else 'uncolored action flat, neutral assumption; form only' if name=='open-empty' else 'pale shirt stripe; mixed outdoor light')
 (OUT/'whitebalance.json').write_text(json.dumps(rows,indent=2))

# Left uses the original straight-hand field silhouette. Fences, butt endpoints
# and muzzle locate the camera; independent wrist/forend differences stay visible.
MATCHES={
 'left':dict(photo=str(OUT/'class-side.png'),crop=(0,0,4608,906),title='Left / straight-hand class',
  location=(-2,.20,.6),target=(0,.23,.01),lens=85,lens_bounds_mm=(45,135),
  landmarks=[L((0,775.4,44),(116,366)),L((-12.6,115,57.35),(2855,230)),
   L((-16.6,36,25),(3107,316)),L((0,-304.6,-5),(4470,345)),L((0,-296.2,-117),(4476,794))]),
 'right':dict(photo=str(OUT/'side-b.png'),crop=(0,100,3840,1500),title='Right / open field class',
  location=(2,-.3,1.1),target=(0,.22,0),lens=75,lens_bounds_mm=(35,135),
  landmarks=[L(opened((10.9,775.4,44)),(3794,915)),L(opened((12.6,115,44)),(1596,373)),
   L((23,170,19),(1725,466)),L((17,36,23),(1502,549)),
   L((0,-304.6,-5),(185,974),.2),L((0,-296.2,-117),(276,1354),.2)]),
 'action':dict(photo=str(OUT/'class-side.png'),crop=(2460,150,3310,650),title='Action / independent left close-up',
  location=(-.50,.08,.15),target=(0,.095,.026),lens=85,lens_bounds_mm=(45,130),
  landmarks=[L((-12.6,115,57.35),(2855,230)),L((-26,115,10),(2813,386)),
   L((-16.6,36,25),(3107,316)),L((0,52,-31),(3015,520))]),
 'open_loaded':dict(photo=str(OUT/'breech.png'),crop=(180,210,1910,1490),title='Open assembled side-by-side / different sidelock',
  location=(.30,-.15,.23),target=(0,.13,.06),lens=75,lens_bounds_mm=(35,120),
  landmarks=[L(opened((-12.6,105,44)),(1617,724)),L(opened((12.6,105,44)),(1441,906)),
   L((0,63,57.5),(620,453)),L((0,94,55.5),(995,650))]),
 'open':dict(photo=str(OUT/'open-candidate-5.png'),crop=(1100,1500,2136,2900),title='Chambers and extractor / reference barrels detached',
  location=(.15,-.25,.25),target=(0,.135,.055),lens=70,lens_bounds_mm=(30,135),camera_height_m=(.12,.04),
  landmarks=[L(opened((12.6,115,44)),(1550,1980)),L(opened((-12.6,115,44)),(1570,2630)),
   L(opened((12.6,115,55.3)),(1235,1965)),L(opened((0,116.4,32.2)),(1870,2350))]),
 'trigger':dict(photo=str(OUT/'side-a.png'),crop=(480,750,1580,1600),title='Double triggers / sharp underside macro',
  location=(.25,.10,-.20),target=(0,.055,-.008),lens=85,lens_bounds_mm=(40,135),
  landmarks=[L((4.7,14,-1),(625,1214)),L((4.7,82,4),(1428,969)),
   L((4.7,75,-29),(1269,1320)),L((4.7,35,-31),(887,1405)),
   L((2.6,64,-23),(1190,1275),.3),L((-2.6,43,-23),(902,1317),.3)])}
if __name__=='__main__':prep()
