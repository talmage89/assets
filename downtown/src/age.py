"""Cause-specific color at real rest positions; stock exported COLOR_0.

No uniform grime wash. Sill runoff, damp scuppers, splash, repointing patches,
paint wear at folds and door handling keep each substrate's own color.
"""
import math
AMOUNT=1.0


def tint(point,role,color,p,name):
 if not p or role in ('Glass','Graphics','Interior'):return color
 x,y,z=point;w=p['width'];d=p['depth'];seed=p['seed']%53
 ripple=.5+.23*math.sin(x*6.1+z*9.3+seed)+.17*math.sin(x*17.3-z*2.1)
 dirt=0.;salt=0.
 if role=='Masonry':
  # Splash rises unevenly above the pavement, concentrated beside drains.
  splash=max(0,1-z/.62)**1.8*(.25+.65*ripple)
  dirt+=.62*splash
  back=y>d/2-.50
  drain_x=-w/2+.38
  drain=math.exp(-((x-drain_x)/.22)**2) if back else 0
  dirt+=.48*drain*(.6+.4*ripple)
  # Atmospheric soot collects in sheltered upper courses; rain escapes at
  # sheet joints and brings it down in changing-width gravity tracks.
  under=max(0,p['height']-.72-z)
  if z>p['roof']-1.10:
   shelter=math.exp(-under/.75)
   drip=(.5+.5*math.sin(x*4.7+seed))**8
   dirt+=shelter*(.22+.28*drip)
  if back and p.get('fire_escape'):
   # Oxide runs from the lower fixings of the two actual escape anchor plates.
   span=min(5.60,w-.55);rust=0.
   for level in range(p['stories']-1):
    fixing=p['floor_first']+level*p['upper']+.02-1.65
    drop=fixing-z
    if 0<=drop<1.15:
     for sign in (-1,1):rust+=.38*math.exp(-((x-sign*(span/2-.35))/(.11+.035*drop))**2)*math.exp(-drop/.62)
   rust=min(.42,rust)*AMOUNT
   color=tuple(v*(1-rust)+rust*c for v,c in zip(color,(.22,.075,.027)))
  # Water passing each projecting sill drags atmospheric soot downward.
  if y<-d/2+.48:
   L=w-p['chamfer'];left=-w/2+(p['chamfer'] if p['corner']=='left' else 0);n=max(2,round((L-.6)/1.95))
   for level in range(1,p['stories']):
    sill=p['floor_first']+(level-1)*p['upper']+.65
    if sill-1.25<=z<=sill+.00001:
     for j in range(n):
      xx=left+(j+.5)*L/n
      for off in (-.46,.46):dirt+=.70*math.exp(-((x-xx-off)/.29)**2)*math.exp(-(sill-z)/.95)*(.7+.3*ripple)
   for xx in (left+.70,left+L-.70):
    fall=p['floor_first']+.15-z
    if 0<fall<1.1:dirt+=.32*math.exp(-((x-xx)/(.12+.1*fall))**2)*math.exp(-fall/.7)
   # Repointing replaces local mortar/body response over a stepped repair.
   patch=(w*.08<x<w*.36 and .5<z<2.1 and int(z/.2032)%3!=1)
   if patch:color=tuple(v*(1.04+.055*ripple) for v in color)
  salt=.25*max(0,1-abs(z-.32)/.32)*max(0,ripple-.38)* (1+drain)
  if p.get('painted') and y<-d/2+.48 and z<.9:
   peel=max(0,1-z/.9)*max(0,math.sin(x*5.7+seed)+.2)*AMOUNT
   color=tuple(v*(1-min(.78,peel))+c*min(.78,peel) for v,c in zip(color,(.40,.18,.095)))
  if p.get('corner')=='left' and x<-w/2+.02:
   L=d-p['chamfer'];u=d/2-y;gx=min(L*.50,L-14.0)
   old_top=3.2+(min(4.35,p['floor_first']-.35)-3.2)*(1-abs(u-gx)/3.85)
   if abs(u-gx)<3.8 and .45<z<old_top:
    interior=min(1,(old_top-z)/.35)
    color=tuple(v*(1-interior*loss) for v,loss in zip(color,(.03,.10,.18)))
 elif role in ('Finish','Mineral'):
  dirt+=.40*max(0,1-z/.65)*ripple
  if z>p['roof']-.1:
   # Fold seams collect moisture and develop downward, narrow paint losses.
   seam=math.exp(-((math.sin((x+.10)*3.4))/.12)**2)
   dirt+=.16*seam*(.5+.5*ripple)
  if role=='Mineral':dirt+=.14*ripple*max(0,1-abs((z-p['floor_first']-.65)%p['upper']+.10)/.23)
 if 'Door' in name:
  # Polish/grime at the latch and shoe-contact rail.
  dirt+=.15*math.exp(-((z-1.12)/.13)**2)+.19*math.exp(-((z-.10)/.12)**2)
 dirt*=AMOUNT*1.65;salt*=AMOUNT
 factor=max(.35,1-dirt)
 return tuple(min(1,v*factor*(1-salt)+salt*.50) for v in color)
