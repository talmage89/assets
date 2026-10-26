"""Causal polyethylene weather: sun, ground splash, lip runoff and contact scuffs."""
from kit.materials import Nodes,common,drip_mask

def polyethylene(name,wear=.35,color=(.026,.030,.031),lid=False,wheel=False,stamp=None):
 n=Nodes(name);c=common(n);p=c['position']
 grain=n.noise(p,1450,2)
 exposure=n.maximum(n.mul(c['up'],.7),n.mul(n.ramp(c['z'],.15,1.02),.55)) if not lid else n.maximum(c['up'],.2)
 fade=n.mul(wear,exposure,n.ramp(n.noise(p,8,3),.18,.83))
 base=n.mix(fade,color,tuple(v*1.7+.004 for v in color),True)
 speckle=n.ramp(n.noise(p,290,2),.32,.68)
 base=n.mix(n.mul(speckle,.28),base,tuple(v*1.45 for v in color),True)
 rough=n.add(.46 if lid else .58,n.mul(n.math('SUBTRACT',grain,.5),.12),n.mul(fade,.17))
 # Road grit accumulates below the splash line and in the rim recess.
 low=n.ramp(c['z'],.30,.015) if not lid else 0
 lip=n.band(c['z'],1.012,.014,.018) if not lid else n.band(c['z'],-.010,.009,.01)
 dirt=n.mul(wear,n.maximum(n.mul(low,.9),n.mul(lip,.8),n.mul(c['cavity'],.55)),n.ramp(n.noise(p,62,4),.30,.72))
 base=n.mix(dirt,base,(.057,.047,.033),True);rough=n.mix(dirt,rough,.88)
 # Downward water tracks below the front lifting shoulder, irregular only within source zones.
 drips=drip_mask(n,c,[dict(x=x,z=.80,width=w,length=l,direction=(0,-1,0)) for x,w,l in [(-.23,.006,.24),(.19,.004,.18),(.09,.003,.13)]]) if not lid else 0
 base=n.mix(n.mul(drips,wear*.48),base,(.015,.014,.010),True)
 # Scraping follows truck contact shoulders, ground drag edge and the lid's hand grip.
 touch=n.maximum(n.mul(c['edge'],.5),n.mul(n.band(c['z'],.58,.14,.04),.15),n.mul(low,.65)) if not lid else n.maximum(c['edge'],n.mul(n.ramp(c['y'],-.72,-.78),n.ramp(n.math('ABSOLUTE',c['x']),.14,.07),.8))
 direction=n.vec('MULTIPLY',p,(12,180,900))
 scratches=n.mul(touch,wear*2.5,n.ramp(n.noise(direction,1,2),.53,.69))
 base=n.mix(scratches,base,(.11,.115,.111) if not wheel else (.045,.042,.034),True)
 rough=n.mix(scratches,rough,.72)
 height=n.add(n.mul(n.math('SUBTRACT',grain,.5),65e-6),n.mul(scratches,-70e-6))
 if stamp:
  import bpy
  tex=n.node('ShaderNodeTexImage',extension='CLIP');tex.image=bpy.data.images.load(str(stamp),check_existing=True)
  uv=n.combine(n.add(n.mul(n.math('SUBTRACT',c['y'],.036075),1/.33),.5),n.add(n.mul(n.math('SUBTRACT',c['z'],.885),1/.13),.5),0)
  n.feed(tex.inputs['Vector'],uv)
  alpha=n.mul(tex.outputs['Alpha'],n.ramp(n.split(c['normal'])[0],.75,.99),n.ramp(c['x'],.30,.34))
  base=n.mix(alpha,base,tex.outputs['Color'],True);rough=n.mix(alpha,rough,.73)
 n.channel('dust',dirt);n.channel('grease',drips)
 return n.finish(base,rough,0,height)
