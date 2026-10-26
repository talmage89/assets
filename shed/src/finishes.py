"""Original plywood and asphalt; weather masks follow exposure and construction."""
from kit.materials import Nodes
from dimensions import *


def wood(name,wear,axis='Z',paint=None,trim=False,floor=False,origin=(0,0,0)):
 n=Nodes(name);tc=n.node('ShaderNodeTexCoord')
 # Moving leaves use their rest-pivot offset, retained through bake isolation.
 p=n.vec('ADD',tc.outputs['Object'],origin);x,y,z=n.split(p)
 a,b,c={'Z':(x,y,z),'X':(y,z,x),'Y':(x,z,y)}[axis]
 broad=n.noise(n.combine(n.mul(a,75),n.mul(b,75),n.mul(c,2.2)),1,3)
 fine=n.noise(n.combine(n.mul(a,950),n.mul(b,950),n.mul(c,9)),1,2)
 rings=n.ramp(n.math('SINE',n.add(n.mul(a,780),n.mul(broad,8))),.25,.9)
 base=n.mix(n.add(n.mul(broad,.7),n.mul(rings,.22)),(.39,.26,.125),(.17,.108,.048),color=True)
 h=n.add(n.mul(rings,-.00012),n.mul(fine,.00016));rough=n.add(.68,n.mul(fine,.18))
 if paint:
  geom=n.node('ShaderNodeNewGeometry');nx,ny,nz=n.split(geom.outputs['Normal'])
  side=n.ramp(n.math('ABSOLUTE',nx),.45,.85)
  across=n.mix(side,x,y)
  groove=n.ramp(n.math('PINGPONG',across,.1016),.004,.001) if not trim else 0
  patch=n.noise(n.combine(n.mul(x,8),n.mul(y,8),n.mul(z,13)),1,3)
  flecks=n.noise(n.combine(n.mul(x,43),n.mul(y,43),n.mul(z,25)),1,2)
  # -X/-Y receive sun; +X/+Y retain moisture. A roof/eave shelters the top.
  shade=n.ramp(n.add(nx,ny),-.5,.7)
  sun=n.mul(n.math('SUBTRACT',1,shade),n.ramp(z,.2,.65),n.ramp(z,EAVE,EAVE-.20))
  chalk=n.mul(sun,wear,n.add(.16,n.mul(patch,.20)))
  tint=n.mix(n.mul(broad,.09),paint,tuple(v*.81 for v in paint),color=True)
  base=n.mix(chalk,tint,tuple(v*.77+.12 for v in paint),color=True)
  # Soil splash only reaches the bottom 90 mm of siding; noise breaks droplets.
  splash=n.mul(n.ramp(z,.23,.12),n.ramp(flecks,.35,.67),wear)
  # Water held in T1-11 channels, behind corner boards and below horizontal trim.
  corners=n.mix(side,n.band(n.math('ABSOLUTE',x),W/2-.047,.035,.05),n.band(n.math('ABSOLUTE',y),D/2-.047,.035,.05))
  roofline=n.mix(side,n.add(RIDGE,n.mul(n.math('ABSOLUTE',x),-PITCH)),EAVE)
  below_roof=n.math('SUBTRACT',roofline,z)
  eave=n.mul(n.ramp(below_roof,.24,.035),n.ramp(below_roof,0,.02))
  lintel=n.mul(n.ramp(y,-D/2+.02,-D/2-.02),n.band(x,0,DOOR_W/2,.03),n.ramp(z,DOOR_TOP-.18,DOOR_TOP-.02),n.ramp(z,DOOR_TOP,DOOR_TOP-.015))
  sill_z=WIN_Z-WIN_H/2-.065
  sill=n.mul(n.ramp(x,W/2-.02,W/2),n.band(y,WIN_Y,WIN_W/2+.065,.045),n.ramp(z,sill_z-.28,sill_z-.025),n.ramp(z,sill_z+.015,sill_z-.01))
  retained=n.maximum(n.mul(groove,.32),n.mul(corners,.45),n.mul(eave,.48),lintel,sill)
  mildew=n.mul(retained,n.add(.15,n.mul(shade,.85)),n.ramp(patch,.31,.68),wear)
  base=n.mix(n.mul(mildew,.65),base,(.037,.067,.026),color=True)
  base=n.mix(n.mul(splash,.60),base,(.078,.062,.036),color=True)
  # Hand pressure near each door pull; palm smear and narrow finger drag.
  hand=n.mul(n.ramp(y,-D/2-.015,-D/2-.03),n.maximum(*[n.ellipse(p,(xx,DECK+1.03),(.11,.16)) for xx in (-.075,.075)]),n.ramp(flecks,.28,.68),wear)
  base=n.mix(n.mul(hand,.47),base,(.062,.073,.040),color=True)
  if not trim:
   base=n.mix(n.mul(groove,.25),base,tuple(v*.53 for v in paint),color=True)
   h=n.add(h,n.mul(groove,-.0035))
  # Sparse paint loss confined to damp joinery and handling, not a height wash.
  chips=n.mul(n.maximum(n.mul(retained,.4),n.mul(hand,.3)),n.ramp(fine,.68,.79),wear)
  base=n.mix(chips,base,(.15,.125,.078),color=True)
  h=n.add(h,n.mul(chips,-.00035));rough=n.add(.73,n.mul(fine,.10),n.mul(chalk,.10),n.mul(mildew,.08),n.mul(hand,-.14))
  for key,val in [('splash',splash),('mildew',mildew),('chalk',chalk),('handling',hand)]:n.channel(key,val)
 if floor:
  traffic=n.mul(n.ramp(n.math('ABSOLUTE',x),.65,.22),n.ramp(y,.35,-1.55),wear)
  base=n.mix(n.mul(traffic,.55),base,(.36,.29,.18),color=True)
  dirt=n.mul(n.ramp(n.math('ABSOLUTE',x),.6,1.1),wear*.55)
  base=n.mix(dirt,base,(.12,.105,.075),color=True)
 return n.finish(base,rough,0,h)


def shingles(wear,cap=False):
 n=Nodes('Granular asphalt / '+('ridge caps' if cap else 'three-tab strips'));tc=n.node('ShaderNodeTexCoord');p=tc.outputs['Object'];x,y,z=n.split(p)
 # Twelve courses: 127.8 mm exposure along the 6:12 slope. Half-tab stagger.
 q=n.mul(n.math('SUBTRACT',RX,n.math('ABSOLUTE',x)),12/RX)
 row=n.math('FLOOR',n.add(q,.0001));phase=n.math('FRACT',q)
 station=n.add(y,RY,n.mul(n.math('MODULO',row,2),-.1524))
 tab=n.math('FLOOR',n.mul(station,1/.3048))
 strip=n.math('FLOOR',n.mul(station,1/.9144))
 batch=n.noise(n.combine(strip,row,2.17),3,1)
 # The blend belongs to the whole 914 mm strip, rather than independent slates.
 base=n.mix(n.ramp(batch,.30,.70),(.006,.009,.011),(.050,.044,.032),color=True)
 aggregate=n.noise(p,90,2);gran=n.noise(p,680,2)
 # Mineral clusters must survive the 123 px/m delivery footprint. Fine grit
 # sits on a coarser, high-contrast mix of light stone and dark asphalt grains.
 grit=n.ramp(aggregate,.37,.63)
 base=n.mix(n.mul(grit,.56),base,(.085,.076,.055),color=True)
 base=n.mix(n.mul(n.ramp(gran,.40,.60),.48),base,(.004,.007,.009),color=True)
 shadow=0 if cap else n.ramp(phase,.88,.985)
 slot=0 if cap else n.ramp(n.math('PINGPONG',station,.1524),.008,.002)
 base=n.mix(n.mul(shadow,.78),base,(.003,.004,.004),color=True)
 base=n.mix(n.mul(slot,.83),base,(.004,.005,.004),color=True)
 # Soft moss colonies where shaded retained moisture permits growth; no long runs.
 cloud=n.noise(n.combine(n.mul(x,3.8),n.mul(y,3.8),n.mul(z,3.8)),1,4)
 damp=n.mul(n.ramp(x,-.05,.4),n.ramp(cloud,.43,.62),wear)
 moss=n.mul(damp,n.add(.72,n.mul(slot,.28)))
 base=n.mix(n.mul(moss,.78),base,(.025,.067,.009),color=True)
 stain=n.mul(n.ramp(x,-.05,.4),n.ramp(cloud,.37,.58),wear*.30)
 base=n.mix(stain,base,(.012,.018,.013),color=True)
 height=n.add(n.mul(grit,.0018),n.mul(gran,.0008),n.mul(slot,-.0014),n.mul(moss,.001))
 for key,val in [('strip',batch),('course_shadow',shadow),('moss',moss)]:n.channel(key,val)
 return n.finish(base,n.add(.85,n.mul(gran,.10)),0,height)
