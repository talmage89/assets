"""Gravity runoff from cap/column shoulders and splash from median level.

Meter-space fields are sampled on the existing cylindrical form. Narrow
streams start at the wet head, spread and fade down it, with no decal stamp.
"""
import math

def tint(v,station=0):
 angle=math.atan2(v.x,v.y-round(v.y/7)*7)
 h=max(0,v.z)
 # Several connected channels, uneven around each column's circumference.
 stream=0
 for a,w,strength in ((-.9,.22,.48),(.45,.26,.55),(1.9,.18,.48),(3.0,.24,.38),(-2.1,.20,.45)):
  delta=math.atan2(math.sin(angle-a-.035*math.sin(h*2.1)),math.cos(angle-a-.035*math.sin(h*2.1)))
  stream+=strength*math.exp(-(delta/w)**2)
 runoff=stream*(.32+.68*min(1,(h/4.35)**.60))
 splash=.68*math.exp(-(h/1.10)**1.4)*(.83+.12*math.sin(angle*5+station))
 damp=.055+.065*(.5+.5*math.sin(angle*8+h*.8))
 value=max(.22,1-runoff-splash-damp)
 return (value,value*(1-(1-value)*.09),value*(1-(1-value)*.24),1)
