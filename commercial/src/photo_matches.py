"""Two dated period photographs: canopy construction and a dispenser cabinet.

The chosen points calibrate corresponding structure, not the whole original
station plan. Farther columns, signage and active/stowed hose states are held
out and remain visible in the comparisons.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from plan import generate,rotate

def point(world,pixel,label):return dict(world=world,pixel=pixel,label=label)
p=generate(101);c=p['canopy'];coly=c['center'][1]+.92-c['column']/2
# Picked on the 1400-wide inspection grid; explicitly convert to native pixels.
scale=2132/1400
pa=[]
for x,top,base in [(-c['pitch'],(360,490),(360,771)),(c['pitch'],(786,318),(786,866))]:
 pa+=[point((x,coly,c['clear']),tuple(v*scale for v in top),'column / soffit'),point((x,coly,.20),tuple(v*scale for v in base),'column / island top')]
# M3 first unit's front (-Y) face becomes +X after the island's 90-degree yaw.
ix,iy=p['islands'][0]['center'];iy-=.96

def pump(v):
 u,w,z=rotate(v,90);return (u+ix,w+iy,z+.1624)
# Photograph is 1899x2700; grid was reduced to height 1100.
cs=2700/1100
ca=[point(pump(v),tuple(q*cs for q in xy),lab) for v,xy,lab in (
 ((-.4825,-.3015,1.01),(105,575),'cabinet access upper left'),
 ((.4825,-.3015,1.01),(280,500),'cabinet access upper right'),
 ((.4825,-.3015,.11),(255,725),'cabinet access lower right'),
 ((-.4825,-.3015,.11),(105,890),'cabinet access lower left'))]
MATCHES={
 'period_canopy':dict(title='Pennsylvania 2006 / canopy and column proportions',photo='build/pa-canopy-neutral.png',crop=(260,350,1600,1390),
  location=(26,-24,1.7),target=(0,coly,2.5),lens=40,lens_bounds_mm=(24,150),background='transparent',exposure=-.15,landmarks=pa),
 'period_dispenser':dict(title='California 2009 / cabinet and slack hose',photo='build/ca-dispenser-neutral.png',crop=(0,610,1300,2500),
  location=(ix+3.0,iy-2.0,1.7),target=(ix,iy,1.2),lens=45,lens_bounds_mm=(24,180),background='transparent',exposure=-.15,landmarks=ca)
}
PAIR_SEEDS={name:101 for name in MATCHES}
LIGHTING={'period_canopy':dict(sky_strength=.7,neutral_ambient=1,sun_direction=(-.6,.4,-1)),
          'period_dispenser':dict(sky_strength=.7,neutral_ambient=1)}
