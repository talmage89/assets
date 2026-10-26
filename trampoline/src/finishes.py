"""Cause-located weather: zinc welds/hooks, exposed PVC and molded foam."""
from kit.materials import Nodes
import math
from dimensions import *

def zinc(wear):
 n=Nodes('Galvanized steel / welded joint corrosion');tc=n.node('ShaderNodeTexCoord');p=tc.outputs['Object'];x,y,z=n.split(p)
 cell=n.voronoi(p,480);grain=n.noise(p,1400,2);patch=n.noise(p,85,3)
 base=n.mix(cell,(.27,.31,.32),(.46,.49,.49),color=True)
 radius=n.math('SQRT',n.add(n.mul(x,x),n.mul(y,y)));angle=n.math('ARCTAN2',y,x)
 joints=n.ramp(n.math('COSINE',n.mul(n.add(angle,-A0),12)),.93,.995)
 weld=n.mul(joints,n.band(z,MAT_Z,.030,.012))
 ground=n.mul(n.ramp(z,.20,.025),n.ramp(patch,.32,.68))
 rust=n.mul(n.maximum(weld,ground),n.ramp(patch,.30,.69),wear)
 base=n.mix(rust,base,(.16,.057,.014),color=True)
 # Damp soil and mower splash, concentrated on the feet and lower uprights.
 soil=n.mul(ground,wear,.75)
 base=n.mix(soil,base,(.068,.059,.034),color=True)
 return n.finish(base,n.add(.49,n.mul(grain,.17),n.mul(rust,.23),n.mul(soil,.26)),n.mix(n.maximum(rust,soil),.88,.05),n.add(n.mul(grain,.00002),n.mul(rust,.0002),n.mul(soil,.00012)))

def pad(wear):
 n=Nodes('Sewn PVC pad / exposed top fading');tc=n.node('ShaderNodeTexCoord');p=tc.outputs['Object'];x,y,z=n.split(p)
 geom=n.node('ShaderNodeNewGeometry');normal=n.split(geom.outputs['Normal'])[2]
 top=n.ramp(normal,.25,.85);cloud=n.noise(p,5,3);micro=n.noise(p,600,2)
 # UV oxidation bleaches upward-facing PVC. The narrow sides/underside stay blue.
 fade=n.mul(top,wear,n.add(.72,n.mul(cloud,.55)))
 base=n.mix(fade,(.007,.039,.067),(.090,.188,.245),color=True)
 angle=n.math('ARCTAN2',y,x);sector=n.math('PINGPONG',n.mul(angle,6/math.pi),1)
 seam=n.ramp(sector,.028,.002)
 # Stitch tension produces shallow radial pleats, with darker protected folds.
 radius=n.math('SQRT',n.add(n.mul(x,x),n.mul(y,y)))
 pleat=n.mul(top,n.ramp(sector,.28,.035),n.math('SINE',n.add(n.mul(radius,150),n.mul(cloud,7))))
 base=n.mix(n.mul(n.ramp(pleat,.1,.8),.10),base,(.012,.046,.071),color=True)
 # Radial seam puckering comes from stitched compression; shallow cracks are on top.
 wrinkle=n.mul(n.ramp(sector,.18,.02),n.math('SINE',n.add(n.mul(z,1700),n.mul(cloud,9))),.0009)
 cracks=n.mul(top,n.ramp(micro,.70,.80),n.ramp(cloud,.51,.67),wear)
 base=n.mix(n.mul(cracks,.45),base,(.17,.21,.21),color=True)
 # Shoes/knees cross the pad only at the front zipper. Broken directional
 # scuffs follow that travel, with soil caught alongside seam compression.
 entry=n.mul(n.band(x,0,.32,.13),n.ramp(y,-1.75,-1.94),top,wear)
 rub=n.noise(n.combine(n.mul(x,38),n.mul(y,8),n.mul(z,70)),1,3)
 shoes=n.maximum(n.ellipse(p,(-.15,-2.025),(.095,.17),axes=(0,1)),n.ellipse(p,(.13,-2.04),(.085,.145),axes=(0,1)))
 scuff=n.mul(entry,n.ramp(rub,.53,.72))
 grime=n.mul(entry,n.maximum(n.mul(shoes,n.ramp(rub,.28,.61)),n.mul(seam,.75)))
 base=n.mix(n.mul(scuff,.40),base,(.16,.21,.22),color=True)
 base=n.mix(n.mul(grime,.90),base,(.027,.033,.021),color=True)
 base=n.mix(n.mul(seam,.65),base,(.006,.022,.031),color=True)
 for key,val in [('fading',fade),('entry_scuff',scuff),('entry_grime',grime)]:n.channel(key,val)
 return n.finish(base,n.add(.56,n.mul(fade,.24),n.mul(micro,.08),n.mul(grime,.13)),0,n.add(wrinkle,n.mul(pleat,.0013),n.mul(micro,.00003),n.mul(cracks,-.0002),n.mul(scuff,-.00012)))

def foam(wear):
 n=Nodes('Closed cell foam / sun and handling');tc=n.node('ShaderNodeTexCoord');p=tc.outputs['Object'];x,y,z=n.split(p)
 pore=n.noise(p,800,2);cloud=n.noise(p,9,3);sun=n.mul(n.ramp(z,.8,2.6),wear)
 base=n.mix(sun,(.008,.033,.052),(.046,.087,.112),color=True)
 base=n.mix(n.mul(n.ramp(pore,.65,.79),.2),base,(.005,.010,.013),color=True)
 return n.finish(base,n.add(.85,n.mul(cloud,.1)),0,n.mul(pore,.00015))
