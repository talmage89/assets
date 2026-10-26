"""Original zinc crystallization and cause-located outdoor weathering."""
from kit.materials import Nodes,common

def zinc(name,wear=.35,lid=False,handle=False):
 n=Nodes(name);c=common(n);p=c['position'];z=c['z']
 # Zinc crystals: angular Voronoi cells with random crystal orientation/color.
 v=n.node('ShaderNodeTexVoronoi',distance='EUCLIDEAN');n.feed(v.inputs['Vector'],p);v.inputs['Scale'].default_value=420
 color=v.outputs['Color'];r=n.split(color)[0]
 crystal=n.mix(r,(.19,.215,.23),(.27,.29,.31),True)
 edge=n.ramp(n.voronoi(p,420,'DISTANCE_TO_EDGE'),.015,.045)
 base=n.mix(n.mul(n.math('SUBTRACT',1,edge),.10),crystal,(.17,.19,.20),True)
 rough=n.add(.39,n.mul(r,.12),wear*.30)
 # Wet edges and folded seam retain water; broad exposed sheet only dulls.
 low=n.ramp(z,.10,.015) if not lid else n.band(z,-.022,.009,.009)
 seam=n.mul(n.band(c['x'],0,.002,.006),n.ramp(c['y'],.19,.23)) if not lid else c['edge']
 rim=n.band(z,-.033,.009,.008) if lid else n.band(z,.687,.013,.012)
 handling=1 if handle else n.mul(n.band(z,.632,.030,.026),n.ramp(n.math('ABSOLUTE',c['x']),.22,.25),n.ramp(n.math('ABSOLUTE',c['y']),.085,.045))
 # Wet folded joints, splashed skirt and hand-contact areas carry visible deposits.
 rain=n.mul(n.ramp(z,.70,.60),n.ramp(z,.035,.14),n.ramp(n.noise(n.vec('MULTIPLY',p,(24,24,2)),2,3),.29,.64)) if not lid else c['up']
 origin=n.maximum(n.mul(rain,.45),n.mul(low,1.1),seam,n.mul(c['cavity'],rain,.5),n.mul(rim,.65),n.mul(handling,.7))
 white=n.mul(origin,wear*2.0,n.ramp(n.noise(p,85,4),.43,.65))
 base=n.mix(white,base,(.60,.61,.58),True);rough=n.mix(white,rough,.91);metal=n.mix(white,1,.05)
 # Fine oxide haze from exposure, local drip streaks below the mouth.
 haze=n.mul(wear*1.2,n.maximum(.35,n.mul(c['up'],.8)),n.ramp(n.noise(p,38,3),.25,.7))
 base=n.mix(haze,base,(.24,.26,.25),True);rough=n.mix(haze,rough,.59)
 # Dirt settles in the bottom skirt and around folded handle brackets.
 grime=n.mul(wear*2.1,n.maximum(low,n.mul(handling,.8),n.mul(c['cavity'],.7)),n.ramp(n.noise(n.vec('MULTIPLY',p,(30,30,3)),3,3),.26,.64))
 base=n.mix(grime,base,(.035,.029,.020),True);rough=n.mix(grime,rough,.90);metal=n.mix(grime,metal,.05)
 rust=n.mul(wear*2.2,n.maximum(n.mul(rim,.85),seam,n.mul(low,.50)),n.ramp(n.noise(p,135,3),.51,.68))
 base=n.mix(rust,base,(.19,.063,.018),True);rough=n.mix(rust,rough,.86);metal=n.mix(rust,metal,0)
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
