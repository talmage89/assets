"""Count-aware cosmetic belt rig. A sampled planar hanging curve, no dynamics.

All ammunition axes remain +Y. Successive centers are solved at equal chord
lengths, rather than resampling equal arc length and silently stretching links.
"""
import math
PITCH=12.8
COUNT=19
# Artistic curve controls in x/z, selected against exterior photographs.
# Starts on tray, bows outboard, hangs below its box mouth and returns inward.
CONTROL=[(0,124),(-38,124),(-76,114),(-91,91),(-95,62),(-81,45),(-55,39),(-38,0),(-38,-140)]

def curve(t):
 # Catmull-Rom, a continuous guide; rigged chord distances are solved separately.
 t=min(len(CONTROL)-1.000001,t)
 if t<0:return (-PITCH*t,124)
 k=int(t);u=t-k
 p0=CONTROL[max(0,k-1)];p1=CONTROL[k];p2=CONTROL[min(len(CONTROL)-1,k+1)];p3=CONTROL[min(len(CONTROL)-1,k+2)]
 return tuple(.5*((2*b)+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u**3) for a,b,c,d in zip(p0,p1,p2,p3))

def solve(phase=0,count=COUNT):
 # Phase translates the train toward +X across the tray; no loop reset/pop.
 points=[(phase*PITCH,124.)];parameters=[-phase]
 for i in range(1,count+1):
  prev=points[-1];a=parameters[-1];b=a+.015
  # Find FIRST forward crossing, not a long chord across a loop.
  while b<len(CONTROL)-1 and math.dist(prev,curve(b))<PITCH:b+=.015
  for _ in range(30):
   mid=(a+b)/2
   if math.dist(prev,curve(mid))<PITCH:a=mid
   else:b=mid
  t=(a+b)/2;points.append(curve(t));parameters.append(t)
 return points

def transforms(phase=0,remaining=200,lift=0,withdraw=0,consumed=0):
 points=solve(phase);out={}
 for i in range(COUNT):
  x,z=points[i];nx,nz=points[i+1]
  angle=math.degrees(math.atan2(nz-z,-(nx-x)))
  out[f'BeltLink{i:02d}']=dict(loc=(x*.001,0,(z-124)*.001),rot_deg=(0,angle,0),scale=(1,1,1) if consumed<=i<consumed+remaining else (0,0,0))
  out[f'BeltRound{i:02d}']=dict(scale=(1,1,1) if consumed<=i<consumed+remaining else (0,0,0))
 out['BeltRoot']=dict(loc=(-withdraw*.001,0,lift*.001))
 return out

def game_pose(completed_shots,advance,remaining):
 """Consumer helper: recycle owners at the tray/box ends of the display train.

 completed_shots is monotonic; advance is [0,1]. Commit one completed shot only
 after reaching 1, then reset advance to 0. Geometrically identical instances
 retain their visible positions under the cyclic permutation. The consumed
 owner returns at the box end. Engine integration must keep that recycling
 region occluded; the finite authored clips test up to a three-round advance.
 """
 if not isinstance(completed_shots,int) or completed_shots<0:raise ValueError(completed_shots)
 if not 0<=advance<=1 or not 0<=remaining<=200:raise ValueError((advance,remaining))
 result=transforms(advance,remaining)
 shifted={'BeltRoot':result['BeltRoot']}
 for i in range(COUNT):
  slot=(completed_shots+i)%COUNT
  for kind in ('Link','Round'):shifted[f'Belt{kind}{slot:02d}']=result[f'Belt{kind}{i:02d}']
 return shifted
