"""Original causal arterial wearing course; canonical Ground images stay intact.

Stock glTF vertex tint carries absorbed oil, not a floating transparent film.
Only approach surfaces receive a sparse station grid; no extra image allocation.
"""
import math

def lanes(spec,turn):
 L=3.3528;n=spec['ns'] if turn%2==0 else spec['ew'];median=spec['median'] if turn%2==0 else 0
 h=n*L/2+median/2
 centers=[-h+L*(i+.5) for i in range(n//2)]
 if n==5:centers.append(0)
 if median:centers.append(-L/2)
 return centers

def value(x,y,spec):
 L=3.3528;hx=spec['ns']*L/2+spec['median']/2;hy=spec['ew']*L/2
 factor=.95
 for t in spec['approaches']:
  a=t*math.pi/2;u=x*math.cos(a)+y*math.sin(a);v=-x*math.sin(a)+y*math.cos(a)
  stop=(hy if t%2==0 else hx)+.4572+spec['radius']+3.9624
  if v<stop-5:continue
  hold=math.exp(-((v-stop-4)/11)**4)
  for c in lanes(spec,t):
   # Drips accumulate under engines in queues; uneven intensity along lane.
   drip=.68+.18*math.sin(v*2.3+c*11)+.14*math.sin(v*5.9-c*8)
   oil=math.exp(-((u-c)/.44)**2)*hold*drip
   wheels=sum(math.exp(-((u-c-d)/.30)**2) for d in (-.78,.78))
   factor*=1-.45*oil
   factor*=1-.15*wheels*math.exp(-max(0,v-stop)/85)
 return max(.19,factor)

def road_grid(h,near,stop,extent,centers):
 xs={-h,h,0}
 for c in centers:
  for d in (-1.18,-.82,-.50,0,.50,.82,1.18):
   if -h<c+d<h:xs.add(c+d)
 ys={near,extent}
 for d in (-5,-3,0,2,4,6,9,13,20,32,52):
  if near<stop+d<extent:ys.add(stop+d)
 return sorted(xs),sorted(ys)
