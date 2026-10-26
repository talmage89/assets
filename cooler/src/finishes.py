"""Molded polyethylene, physically located scuffs, rim dirt and original emboss."""
from pathlib import Path
from kit import materials as M
import bpy

def polyethylene(name,wear,lid=False,brand=None):
 n=M.Nodes(name);c=M.common(n);p=c['position'];x,y,z=c['x'],c['y'],c['z']
 fine=n.noise(p,2200,2);sun=n.mul(c['up'],wear*1.7)
 fresh=(.46,.45,.36) if lid else (.032,.145,.135)
 aged=(.64,.62,.48) if lid else (.115,.245,.215)
 base=n.mix(sun,fresh,aged,True)
 # Sliding abrasion is concentrated on the exposed lower corners, not the whole shell.
 low=n.ramp(z,.075,.020) if not lid else 0
 streak=n.ramp(n.noise(n.vec('MULTIPLY',p,(18,60,950)),1,2),.42,.68)
 abrasion=n.mul(wear*1.2,low,streak,n.maximum(c['edge'],.15))
 # Corner impacts and dragging stress-whiten the raised, unprotected HDPE.
 corner=n.mul(n.ramp(n.math('ABSOLUTE',x),.24,.29),n.ramp(n.math('ABSOLUTE',y),.12,.17),n.ramp(z,.30,.18),n.ramp(z,.020,.045)) if not lid else 0
 scrapes=M.abrasion_mask(n,c,wear*3.0,n.maximum(corner,low))
 impact=n.mul(corner,n.ramp(n.noise(n.vec('MULTIPLY',p,(30,30,300)),1,2),.61,.73),n.ramp(n.noise(p,22,2),.46,.65),wear*2.5)
 abrasion=n.maximum(abrasion,impact,scrapes)
 base=n.mix(abrasion,base,(.22,.30,.25),True)
 dirt=n.mul(wear*1.0,n.maximum(n.mul(low,n.ramp(n.noise(p,80),.36,.65)),c['cavity']))
 base=n.mix(dirt,base,(.055,.039,.019),True)
 touch=M.handling_mask(n,c,[dict(center=(0,.29 if not lid else .015),radii=(.12,.045),axes=(1,2))])
 height=n.add(n.mul(n.math('SUBTRACT',fine,.5),38e-6),n.mul(scrapes,-.00012))
 cups=0
 if lid:
  # Two standing drinks leave broken mineral rims on the upward crown only.
  # Lid coordinates are rebased at its rear hinge: world Y = local Y + .225.
  cy=n.add(y,.225);rings=[]
  for cx,yy,rr in [(.11,-.03,.034),(-.17,.08,.032)]:
   radius=n.math('SQRT',n.add(n.mul(n.math('SUBTRACT',x,cx),n.math('SUBTRACT',x,cx)),n.mul(n.math('SUBTRACT',cy,yy),n.math('SUBTRACT',cy,yy))))
   rings.append(n.band(radius,rr,.0013,.0011))
  cups=n.mul(n.maximum(*rings),c['up'],n.ramp(n.noise(p,150,2),.30,.58),wear*1.9)
  base=n.mix(cups,base,(.22,.20,.115),True)
  height=n.add(height,n.mul(cups,.00002))
 if brand:
  u=n.add(n.math('DIVIDE',x,.28),.5);v=n.math('DIVIDE',n.math('SUBTRACT',z,.195),.070)
  img=n.node('ShaderNodeTexImage');img.image=bpy.data.images.load(str(Path(brand).resolve()));img.image.colorspace_settings.name='Non-Color';img.extension='CLIP'
  n.feed(img.inputs['Vector'],n.combine(u,v,0));front=n.ramp(n.vec('DOT_PRODUCT',c['normal'],(0,-1,0)),.8,.99)
  emboss=n.mul(img.outputs['Color'],front,n.ramp(y,-.175,-.190))
  height=n.add(height,n.mul(emboss,.00085));base=n.mix(n.mul(emboss,.07),base,aged,True)
 drip=M.drip_mask(n,{**c,'x':c['y']},[dict(x=.10,z=.090,width=.018,length=.065,direction=(1,0,0))]) if not lid else 0
 base=n.mix(n.mul(drip,wear*.7),base,(.26,.25,.14),True)
 return n.finish(base,n.add(.54,n.mul(sun,.15),n.mul(dirt,.18),n.mul(touch,-.07),n.mul(abrasion,.10),n.mul(cups,.12)),0,n.add(height,n.mul(dirt,.00004)))
