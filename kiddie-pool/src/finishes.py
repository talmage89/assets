"""Original molded traction pattern and cause-driven exposed/wet HDPE."""
import math
from kit import materials as M

def plastic(wear):
 n=M.Nodes('Minnow blue HDPE / petal mold / exposure / waterline');c=M.common(n);p=c['position'];x,y,z=c['x'],c['y'],c['z']
 radius=n.math('SQRT',n.add(n.mul(x,x),n.mul(y,y)));angle=n.math('ARCTAN2',y,x)
 radial=n.vec('DOT_PRODUCT',c['normal'],n.combine(x,y,0))
 inside=n.ramp(radial,-.04,-.35)
 exposed=n.maximum(c['up'],n.mul(n.ramp(z,.20,.30),.8))
 sun=n.mul(wear*1.5,exposed,n.add(.85,n.mul(n.noise(p,8),.15)))
 base=n.mix(sun,(.012,.16,.30),(.11,.36,.48),True)
 # The original raised floor design is molded relief, not painted dots or artwork.
 floor=n.mul(c['up'],n.ramp(z,.012,.004),n.ramp(radius,.625,.59))
 petals=n.add(.205,n.mul(n.math('COSINE',n.mul(angle,8)),.035))
 outline=n.band(radius,petals,.004,.003)
 rings=n.maximum(n.band(radius,.335,.003,.002),n.band(radius,.475,.003,.002))
 # Radial ribs break the rings into an original pinwheel traction layout.
 spokes=n.mul(n.ramp(n.math('ABSOLUTE',n.math('SINE',n.add(n.mul(angle,16),n.mul(radius,8)))),.055,.020),n.ramp(radius,.26,.30),n.ramp(radius,.59,.55))
 relief=n.mul(floor,n.maximum(outline,rings,spokes))
 micro=n.mul(n.math('SUBTRACT',n.noise(p,2500,2),.5),22e-6)
 level=n.add(.145,n.mul(n.math('SUBTRACT',n.noise(p,31),.5),.003))
 line=n.mul(inside,n.band(z,level,.003,.003),wear*2.1,n.ramp(n.noise(p,43),.20,.62))
 base=n.mix(line,base,(.13,.16,.065),True)
 outside=n.ramp(radial,.04,.35)
 low=n.mul(n.ramp(z,.045,.004),outside)
 dirt=n.mul(wear,n.maximum(n.mul(c['cavity'],.8),n.mul(low,n.ramp(n.noise(p,90),.40,.65))),.75)
 base=n.mix(dirt,base,(.05,.065,.028),True)
 arcs=[]
 for aa,bb in [(-1.24,-.92),(-2.22,-2.00)]:
  arcs.append(n.mul(n.ramp(angle,aa-.025,aa+.025),n.ramp(angle,bb+.025,bb-.025)))
 wet_rim=n.mul(n.maximum(*arcs),n.ramp(z,.288,.299))
 wet=n.maximum(n.mul(n.maximum(inside,floor),n.ramp(z,.146,.133)),wet_rim)
 # Contact polishes the raised traction crests; it is not a printed pattern.
 base=n.mix(n.mul(relief,.16),base,(.009,.13,.24),True)
 rim_scuff=n.mul(wear*2.1,n.ramp(z,.285,.300),n.maximum(c['edge'],n.mul(outside,.18)),n.ramp(n.noise(n.vec('MULTIPLY',p,(80,80,450)),1,2),.48,.68))
 base=n.mix(rim_scuff,base,(.32,.49,.54),True)
 rough=n.add(n.mix(wet,.48,.23),n.mul(sun,.15),n.mul(line,.15),n.mul(dirt,.12),n.mul(relief,-.12))
 return n.finish(base,rough,0,n.add(micro,n.mul(relief,.00125),n.mul(line,.00004)))

def water():
 n=M.Nodes('Clear still water / small original capillary ripples');tc=n.node('ShaderNodeTexCoord');p=tc.outputs['Object'];x,y,z=n.split(p)
 ripple=n.mul(n.math('SINE',n.add(n.mul(x,58),n.mul(n.math('SINE',n.mul(y,17)),1.2))),.00008)
 m=n.finish((.88,.95,.97),.055,0,ripple)
 m.node_tree.nodes['SURFACE'].inputs['Transmission Weight'].default_value=1
 m.node_tree.nodes['SURFACE'].inputs['IOR'].default_value=1.333
 return m
