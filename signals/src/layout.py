"""Road grammar. Equipment derives from the approach it controls, in meters."""
from dataclasses import dataclass
from plan import LANE,xy
@dataclass(frozen=True)
class Site:
 seed:int
 title:str
 ns:int
 ew:int
 radius:float
 median:float=0
 approaches:tuple=(0,1,2,3)
 diagonal:bool=False
 commercial:bool=False
 @property
 def hx(self):return self.ns*LANE/2+self.median/2
 @property
 def hy(self):return self.ew*LANE/2
 def half(self,turn):return self.hx if turn%2==0 else self.hy
 def farhalf(self,turn):return self.hy if turn%2==0 else self.hx
 def core(self,turn):return self.farhalf(turn)+.4572+self.radius
 def face(self,turn):return self.half(turn)+.4572
 def stop(self,turn):return self.core(turn)+1.524+2.4384
 def pole(self,turn):return xy(self.face(turn)+1.02,self.core(turn)-1,turn*90,.1524)
 def positions(self,turn):
  if (self.ns if turn%2==0 else self.ew)>=4:
   outer=self.median/2+LANE*1.5 if self.median else 2*LANE
   if self.seed==201:return [2*LANE,LANE+.1524,0]
   return [outer,outer-2.4384]+([self.median/2-LANE*.5] if self.median else [0])
  c=LANE/2;return [c+1.2192,c-1.2192]
 def arm(self,turn):
  if self.diagonal and turn%2:return self.core(0)-1+max(self.positions(turn))+.65
  return max(6.096,self.face(turn)+1.02-min(self.positions(turn))+.65)
 def cabinet(self):
  # Outside corner service zone, beyond pedestrian route.
  return xy(self.hx+6.3,self.hy+self.radius+6.5,(self.seed-201)*90,.171)
 def data(self):
  return dict(seed=self.seed,title=self.title,ns=self.ns,ew=self.ew,radius=self.radius,median=self.median,approaches=self.approaches,diagonal=self.diagonal,commercial=self.commercial)
SITES={201:Site(201,'Five-lane arterial / two-lane commercial street',5,2,10.668,commercial=True),
202:Site(202,'Two-lane town crossroads / two diagonal dual-arm poles',2,2,4.572,diagonal=True),
203:Site(203,'Divided boulevard / median left-turn bays',4,2,7.62,median=2*LANE),
204:Site(204,'Two-lane T junction / span wire',2,2,6.096,approaches=(0,2,3))}

if __name__=='__main__':
 import json
 from pathlib import Path
 Path('build/sites.json').write_text(json.dumps([s.data() for s in SITES.values()],indent=2))
