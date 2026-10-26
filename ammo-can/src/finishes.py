"""Olive paint, fold abrasion and handling wear with original procedural masks."""
from pathlib import Path
import bpy
from kit.materials import Nodes,common

def olive(name,wear=.35,role='body',stamp=None):
 n=Nodes(name);c=common(n);p=c['position'];z=c['z']
 touch=n.ellipse(p,(0,.12),(.050,.045),(0,2)) if role=='body' else n.mul(n.maximum(n.band(z,0,.003,.005),n.band(z,-.11,.012,.010)),n.ramp(n.math('ABSOLUTE',c['y']),.010,.004))
 low=n.ramp(z,.027,.004) if role=='body' else 0
 exposure=n.maximum(c['edge'],n.mul(touch,.12),n.mul(low,.40))
 chips=n.mul(exposure,wear*1.65,n.ramp(n.noise(p,330,4),.53,.70))
 fine=n.noise(p,2100,2);fade=n.mul(wear,.28,n.maximum(n.mul(c['up'],.5),n.ramp(z,.10,.18) if role=='body' else .25))
 base=n.mix(fade,(.029,.037,.012),(.065,.069,.028),True)
 base=n.mix(chips,base,(.14,.15,.12),True);rough=n.mix(chips,.57,.40);metal=n.mix(chips,0,.85)
 scuff=n.mul(exposure,wear,n.ramp(n.noise(n.vec('MULTIPLY',p,(35,150,2200)),1,3),.56,.71))
 base=n.mix(n.mul(scuff,.30),base,(.082,.085,.052),True);rough=n.mix(n.mul(touch,wear*.25),rough,.40)
 dirt=n.mul(n.maximum(n.mul(c['cavity'],.7),n.mul(low,.6)),wear,n.ramp(n.noise(p,110,3),.31,.72))
 base=n.mix(dirt,base,(.019,.017,.009),True);rough=n.mix(dirt,rough,.80)
 rust=n.mul(chips,low,wear,n.ramp(n.noise(p,220,3),.57,.73))
 base=n.mix(rust,base,(.10,.039,.010),True);metal=n.mix(rust,metal,0);rough=n.mix(rust,rough,.83)
 height=n.add(n.mul(n.math('SUBTRACT',fine,.5),6e-6),n.mul(chips,-30e-6),n.mul(rust,20e-6))
 if stamp:
  tex=n.node('ShaderNodeTexImage',extension='CLIP');tex.image=bpy.data.images.load(str(stamp));tex.image.colorspace_settings.name='sRGB'
  u=n.math('DIVIDE',n.add(c['y'],.115),.230);v=n.math('DIVIDE',n.math('SUBTRACT',z,.043),.084)
  n.feed(tex.inputs['Vector'],n.combine(u,v,0));mask=n.mul(tex.outputs['Alpha'],n.ramp(c['x'],.069,.070),n.ramp(n.split(c['normal'])[0],.75,.95))
  mask=n.mul(mask,n.math('SUBTRACT',1,n.mul(chips,.65)))
  base=n.mix(mask,base,tex.outputs['Color'],True);rough=n.mix(mask,rough,.67);metal=n.mix(mask,metal,0);height=n.add(height,n.mul(mask,8e-6))
 mat=n.finish(base,n.add(rough,n.mul(n.math('SUBTRACT',fine,.5),.045)),metal,height);mat.diffuse_color=(.08,.10,.035,1);return mat
