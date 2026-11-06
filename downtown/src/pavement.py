"""Original sidewalk deposits and utility repairs at their physical causes.

Uses the accepted mineral/roof maps and COLOR_0; no extra allocation or state.
"""
import math,random

CONCRETE=(.245,.238,.215)
ASPHALT=(.14,.143,.14)

def tint(point,role,color,p):
 x,y,z=point
 if role=='Mineral' and max(color)>.18 and z>-.16:
  # Dirt follows the curb/building lines, rather than a uniform dark overlay.
  curb=-p['walk'];far=curb-p['road_width']
  edge=min(abs(y),abs(y-curb),abs(y-far),abs(y-far+p['walk']))
  deposit=math.exp(-edge/.19)*(.13+.20*(.5+.5*math.sin(x*2.7+y*5)))
  slab=.5+.5*math.sin(math.floor(x/1.524)*7.31+math.floor(y/1.524)*4.15)
  stain=.09*max(0,math.sin(x*2.1+y*3.4))**6
  return tuple(v*(.88+.19*slab)*(1-deposit-stain) for v in color)
 return color


def dress(b,p):
 rng=random.Random(p['seed']+9281);W=p['width'];curb=-p['walk'];far=curb-p['road_width']
 # Worn gum is flattened into the walk; the irregular perimeter is authored.
 for i in range(round(W*1.5)):
  x=rng.uniform(-W/2,W/2);y=rng.uniform(curb+.18,-.1);r=rng.uniform(.012,.045)
  pts=[(x+r*math.cos(j*math.tau/7)*(1+.24*math.sin(j*3+i)),y+r*.65*math.sin(j*math.tau/7),.0004) for j in range(7)]
  b.geom(pts,[tuple(range(7))],'Mineral',(.075,.070,.058))
 # Saw-cut utility patches with visible edge seal. Different maintenance dates.
 for i in range(5):
  x=-W*.37+i*W*.17;y=curb-2.4-(i%2)*3.3;w=1.3+.6*(i%3);h=1.1+.3*(i%2)
  col=(.031+.007*i,.033+.007*i,.032+.006*i)
  b.geom([(x-w/2,y-h/2,-.1518),(x+w/2,y-h/2,-.1518),(x+w/2,y+h/2,-.1518),(x-w/2,y+h/2,-.1518)],[(0,1,2,3)],'Roof',col)
  path=[(x-w/2,y-h/2,-.1514),(x+w/2,y-h/2,-.1514),(x+w/2,y+h/2,-.1514),(x-w/2,y+h/2,-.1514),(x-w/2,y-h/2,-.1514)]
  for a,c in zip(path,path[1:]):b.beam(a,c,.04,.001,role='Roof',color=(.018,.019,.018))
 # Routed crack seal meanders down the wearing course, away from marks.
 for lane in (curb-3.1,far+3.3):
  pts=[(-W/2+j*W/18,lane+.22*math.sin(j*1.4)+.07*math.sin(j*4.8),-.1513) for j in range(19)]
  for a,c in zip(pts,pts[1:]):b.beam(a,c,.035,.001,role='Roof',color=(.022,.023,.022))
