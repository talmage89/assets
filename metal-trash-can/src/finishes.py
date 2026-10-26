"""Original zinc crystallization and cause-located outdoor weathering."""
from kit.materials import Nodes,common

def zinc(name,wear=.35,lid=False):
 n=Nodes(name);c=common(n);p=c['position'];z=c['z']
 # Zinc crystals: angular Voronoi cells with random crystal orientation/color.
 v=n.node('ShaderNodeTexVoronoi',distance='EUCLIDEAN');n.feed(v.inputs['Vector'],p);v.inputs['Scale'].default_value=420
 color=v.outputs['Color'];r=n.split(color)[0]
 crystal=n.mix(r,(.19,.215,.23),(.27,.29,.31),True)
 edge=n.ramp(n.voronoi(p,420,'DISTANCE_TO_EDGE'),.015,.045)
 base=n.mix(n.mul(n.math('SUBTRACT',1,edge),.10),crystal,(.17,.19,.20),True)
 rough=n.add(.31,n.mul(r,.12))
 # Wet edges and folded seam retain water; broad exposed sheet only dulls.
 low=n.ramp(z,.10,.015) if not lid else n.band(z,-.022,.009,.009)
 seam=n.mul(n.band(c['x'],0,.002,.006),n.ramp(c['y'],.19,.23)) if not lid else c['edge']
 origin=n.maximum(n.mul(low,.8),n.mul(seam,.85),n.mul(c['cavity'],.55))
 white=n.mul(origin,wear*1.7,n.ramp(n.noise(p,170,4),.39,.66))
 base=n.mix(white,base,(.60,.61,.58),True);rough=n.mix(white,rough,.91);metal=n.mix(white,1,.05)
 # Fine oxide haze from exposure, local drip streaks below the mouth.
 haze=n.mul( wear*.28,n.ramp(n.noise(p,38,3),.25,.7))
 base=n.mix(haze,base,(.24,.26,.25),True);rough=n.mix(haze,rough,.59)
 grain=n.noise(p,3500,2)
 h=n.add(n.mul(n.math('SUBTRACT',grain,.5),3e-6),n.mul(white,25e-6))
 # Small pressed beads are normal detail, not intersecting source shells.
 if lid:
  radial=n.math('SQRT',n.add(n.mul(c['x'],c['x']),n.mul(c['y'],c['y'])))
  bead=n.maximum(*[n.band(radial,r,.0006,.0014) for r in (.065,.117,.164,.209)])
  bead=n.mul(bead,n.ramp(c['z'],.001,.006))
 else:
  bead=n.maximum(n.band(z,.040,.0007,.002),n.band(z,.073,.0007,.002))
 h=n.add(h,n.mul(bead,.0008))
 mat=n.finish(base,rough,metal,h);mat.diffuse_color=(.47,.49,.5,1);return mat
