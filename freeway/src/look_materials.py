"""Four ordinary shared PBR sets layered onto unchanged Ground tiling sets."""
from pathlib import Path
import bpy
import geom as Q
from kit.tiling import material

def install():
    folder=Path('textures/ship')
    for role,name in [('Bridge','FreewayConcrete'),('Steel','FreewayZinc'),('Signs','FreewaySigns'),('Maintenance','FreewayMaintenance')]:
        m=material(name,folder,alpha=role=='Maintenance',tint=role in ('Bridge','Steel','Maintenance'))
        m.name='Freeway_Form_'+role if role in ('Bridge','Steel') else name
        if role=='Maintenance':m.use_backface_culling=False
        Q.M[role]=m
    Q.M['Barrier']=Q.M['Bridge']
    # Native mineral grain at the bare paving edge; the previous scalar
    # brown made soil/gravel look like a strip of smooth paste.
    Q.M['Earth']=Q.M['Asphalt'].copy();Q.M['Earth'].name='Freeway_Form_Earth'
    Q.M['GrassCard']=Q.M['Maintenance'].copy();Q.M['GrassCard'].name='Freeway_TurfCards'
    normal=next(n for n in Q.M['GrassCard'].node_tree.nodes if n.type=='NORMAL_MAP')
    normal.inputs['Strength'].default_value=.10 # Leaf edges are thinner than the maintenance atlas's 8mm relief.
    from landscape import install as install_turf
    install_turf()
    Q.M['WheelPolish']=Q.M['Concrete'].copy();Q.M['WheelPolish'].name='Freeway Wheel polish / Ground Concrete'
    bs=Q.M['WheelPolish'].node_tree.nodes.get('Principled BSDF')
    # Same Ground manufacture/normal, attenuated roughness in the wheel paths.
    tree=Q.M['WheelPolish'].node_tree;src=bs.inputs['Roughness'].links[0].from_socket
    multiply=tree.nodes.new('ShaderNodeMath');multiply.operation='MULTIPLY';multiply.inputs[1].default_value=.60
    tree.links.new(src,multiply.inputs[0]);tree.links.new(multiply.outputs[0],bs.inputs['Roughness'])
    Q.M['AsphaltPolish']=Q.M['Asphalt'].copy();Q.M['AsphaltPolish'].name='Freeway Wheel polish / Ground Asphalt'
    tree=Q.M['AsphaltPolish'].node_tree;bs=tree.nodes.get('Principled BSDF');src=bs.inputs['Roughness'].links[0].from_socket
    multiply=tree.nodes.new('ShaderNodeMath');multiply.operation='MULTIPLY';multiply.inputs[1].default_value=.70
    tree.links.new(src,multiply.inputs[0]);tree.links.new(multiply.outputs[0],bs.inputs['Roughness'])
