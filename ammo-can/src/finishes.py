"""Olive paint, fold abrasion and handling wear with original procedural masks."""
from pathlib import Path
import bpy
from kit.materials import Nodes,common

def olive(name,wear=.35,role='body',stamp=None):
 n=Nodes(name);c=common(n);p=c['position'];z=c['z']
 touch=n.ellipse(p,(0,.12),(.050,.045),(0,2)) if role=='body' else n.mul(n.maximum(n.band(z,0,.003,.005),n.band(z,-.11,.012,.010)),n.ramp(n.math('ABSOLUTE',c['y']),.010,.004))
 low=n.ramp(z,.012,.002) if role=='body' else 0
 # Folding, stacking and the ground concentrate abrasion at actual sheet boundaries.
 if role=='body':
  folds=n.maximum(n.mul(n.ramp(n.math('ABSOLUTE',c['x']),.064,.070),n.ramp(n.math('ABSOLUTE',c['y']),.134,.141)),n.band(z,.174,.002,.005))
 elif role=='lid':folds=n.maximum(n.mul(n.band(z,.007,.001,.004),n.maximum(n.ramp(n.math('ABSOLUTE',c['x']),.069,.077),n.ramp(n.math('ABSOLUTE',n.add(c['y'],.1498)),.132,.146))),c['edge'])
 else:folds=n.maximum(n.mul(touch,1.15),c['edge'])
 exposure=n.maximum(c['edge'],n.mul(folds,.95),n.mul(touch,.55),n.mul(low,.65))
 chips=n.mul(exposure,wear*3.2,n.ramp(n.noise(p,240,4),.46,.67))
 fine=n.noise(p,2100,2);fade=n.mul(wear,.65,n.maximum(n.mul(c['up'],.5),n.ramp(z,.10,.18) if role=='body' else .25))
 base=n.mix(fade,(.029,.037,.012),(.092,.100,.041),True)
 base=n.mix(chips,base,(.11,.12,.11),True);rough=n.mix(chips,.57,.51);metal=n.mix(chips,0,.85)
 # Sparse rack scrapes are authored contact tracks, broken by small-scale paint.
 # Cover positions are hinge-local: its geometric center is Y=-149.8 mm.
 scuff=0
 if role=='body':
  for center,slope,along,length in [(.043,.055,-.04,.11),(.081,-.065,.040,.13),(.128,.045,-.065,.065)]:
   line=n.band(n.add(z,n.mul(c['y'],slope)),center,.00035,.00065)
   reach=n.band(c['y'],along,length/2,.012)
   scuff=n.maximum(scuff,n.mul(line,reach,n.ramp(n.math('ABSOLUTE',n.split(c['normal'])[0]),.55,.9)))
 elif role=='lid':
  ly=n.add(c['y'],.1498)
  for center,slope,along,length in [(-.031,.12,-.025,.13),(.041,-.22,.055,.075),(.015,.3,-.095,.045)]:
   scuff=n.maximum(scuff,n.mul(n.band(n.add(c['x'],n.mul(ly,slope)),center,.00035,.00065),n.band(ly,along,length/2,.012),n.band(z,.007,.001,.003)))
 else:scuff=n.mul(touch,n.ramp(n.noise(n.vec('MULTIPLY',p,(45,18,600)),1,2),.57,.68))
 scuff=n.mul(scuff,wear*1.9,n.ramp(n.noise(p,370,3),.25,.60))
 base=n.mix(n.mul(scuff,.72),base,(.082,.085,.052),True);rough=n.mix(n.mul(touch,wear*.25),rough,.40)
 dirt=n.mul(n.maximum(n.mul(c['cavity'],1.4),n.mul(low,1.8)),wear,n.ramp(n.noise(p,110,3),.31,.72))
 base=n.mix(dirt,base,(.019,.017,.009),True);rough=n.mix(dirt,rough,.80)
 rust=n.mul(chips,low,wear,n.ramp(n.noise(p,220,3),.57,.73))
 base=n.mix(rust,base,(.10,.039,.010),True);metal=n.mix(rust,metal,0);rough=n.mix(rust,rough,.83)
 height=n.add(n.mul(n.math('SUBTRACT',fine,.5),6e-6),n.mul(chips,-30e-6),n.mul(rust,20e-6))
 if stamp:
  tex=n.node('ShaderNodeTexImage',extension='CLIP');tex.image=bpy.data.images.load(str(stamp));tex.image.colorspace_settings.name='sRGB'
  u=n.math('DIVIDE',n.add(c['y'],.115),.230);v=n.math('DIVIDE',n.math('SUBTRACT',z,.043),.084)
  n.feed(tex.inputs['Vector'],n.combine(u,v,0));mask=n.mul(tex.outputs['Alpha'],n.ramp(c['x'],.069,.070),n.ramp(n.split(c['normal'])[0],.75,.95))
  # Stencil pigment fades and abrades with the same contact scratches as the paint.
  pigment=n.ramp(n.noise(n.vec('MULTIPLY',p,(35,22,450)),1,3),.32,.69)
  mask=n.mul(mask,n.math('SUBTRACT',1,n.maximum(n.mul(chips,.95),n.mul(scuff,.72),n.mul(pigment,wear*1.4))))
  base=n.mix(mask,base,tex.outputs['Color'],True);rough=n.mix(mask,rough,.67);metal=n.mix(mask,metal,0);height=n.add(height,n.mul(mask,8e-6))
 mat=n.finish(base,n.add(rough,n.mul(n.math('SUBTRACT',fine,.5),.045)),metal,height);mat.diffuse_color=(.08,.10,.035,1);return mat
