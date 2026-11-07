"""Shared planted-bed footprints for construction and native plant placement."""
import math
def beds(p):
 W,_=p['lot'];out=[]
 for side in (-1,1):
  out.append(dict(name='Entry planting bed',center=(side*10.35,-15.5 if p['water'] else -13),radii=(6.8,1.05 if p['water'] else .35)))
  out.append(dict(name='Perimeter planting bed',center=(side*(23 if p['water'] else W/2-3),4),radii=(1.05,13.2)))
 if not p['water']:
  out.extend((dict(name='Classic lower island',center=(-1.7,-5.4),radii=(1.25,3.2)),dict(name='Classic upper island',center=(-1.7,14.8),radii=(1.25,4.5))))
 return out
def outline(b,n=40):
 x,y=b['center'];rx,ry=b['radii']
 return [(x+rx*math.cos(a)*(1+.025*math.sin(a*3+x)),y+ry*math.sin(a)) for a in (j*math.tau/n for j in range(n))]
