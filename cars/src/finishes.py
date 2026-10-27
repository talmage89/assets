"""Alder source finish palette; delivery remains one neutral three-map atlas."""
from pathlib import Path
import bpy
from kit import vehicle_materials as V
from kit.materials import Nodes
import pickup_spec as S


def build(wear):
    root=Path(__file__).resolve().parents[1]/'build/markings'
    images={n:bpy.data.images.load(str(root/(n+'.png')),check_existing=True) for n in ['plate','badge','model','tire_relief','grille','display']}
    images['tire_relief'].colorspace_settings.name='Non-Color'
    axles=(S.FRONT_AXLE,S.REAR_AXLE)
    m={'body':V.paint('Alder factory paint',S.COLORS['Atlantic'],wear,axles,front=-S.LENGTH/2,rear=2.847)}
    for key,col,kind in [
      ('rubber',(.009,.010,.011),'rubber'),('plastic',(.011,.013,.014),'plastic'),
      ('wheel',(.46,.49,.51),'alloy'),('chrome',(.60,.64,.66),'chrome'),
      ('bed',(.012,.015,.016),'liner'),('bumper',(.016,.019,.021),'plastic'),
      ('frame',(.008,.009,.010),'plastic'),('brake',(.28,.30,.31),'steel'),
      ('caliper',(.11,.12,.12),'steel'),('cloth',(.065,.073,.079),'fabric'),
      ('seat_side',(.026,.031,.035),'plastic'),('interior',(.018,.022,.026),'plastic'),
      ('headliner',(.20,.21,.20),'fabric'),('interior_light',(.10,.12,.13),'plastic')]:
        m[key]=V.manufactured('Alder '+key,col,kind,wear,axles,brake_centers=[(sign*S.TRACK/2,y,S.HUB_HEIGHT) for sign in [-1,1] for y in axles] if key=='wheel' else ())
    m['tire_L']=V.tire('Alder tire left',images['tire_relief'],-1,wear=wear)
    m['tire_R']=V.tire('Alder tire right',images['tire_relief'],1,wear=wear)
    m['glass']=V.glazing('Alder clear windshield')
    m['side_glass']=V.glazing('Alder front side glass',(.88,.94,.94),axes=(1,2))
    m['privacy']=V.glazing('Alder factory privacy glass',(.13,.19,.20),True,axes=(1,2))
    m['rear_glass']=V.glazing('Alder rear privacy glass',(.16,.21,.22),True)
    m['lens']=V.glazing('Alder headlamp polycarbonate',(.96,.98,.99))
    m['lens'].node_tree.nodes['SURFACE'].inputs['IOR'].default_value=1.49
    m['red_lens']=V.lamp('Alder red prismatic lens',(.36,.009,.006),0,.40)
    m['mirror']=V.manufactured('Alder mirror silver',(.76,.78,.79),'chrome',0)
    m['mirror'].node_tree.nodes['SURFACE'].inputs['Roughness'].default_value=.035
    m['drl']=V.lamp('Alder white running signature',(.86,.94,1),16)
    m['headlight']=V.lamp('Alder projector phosphor',(1,.92,.79),45)
    m['brakelight']=V.lamp('Alder red brake emitter',(.68,.009,.005),9)
    m['amber']=V.lamp('Alder amber reflector',(.70,.18,.008),3)
    for key in ['plate','badge','model','grille','display']:
        n=Nodes('Alder original '+key);tex=n.node('ShaderNodeTexImage');tex.image=images[key]
        mat=n.finish(tex.outputs['Color'],.36 if key=='plate' else .25,.0 if key in ['plate','grille'] else .8, n.mul(tex.outputs['Color'],.0015) if key=='grille' else 0)
        if key=='display':
            bs=mat.node_tree.nodes['SURFACE'];n.feed(bs.inputs['Emission Color'],tex.outputs['Color']);bs.inputs['Emission Strength'].default_value=.35
        m[key]=mat
    return m
