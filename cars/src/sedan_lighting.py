"""Procedural lighting for the sedan; leaves the pickup's calibrated stage intact."""
import math
import bpy
from mathutils import Vector
from kit import studio,model as G
from lighting import outdoor


def setup():
    outdoor()
    # Broad neutral parking-lot facades, camera invisible, provide the warm
    # low-elevation reflections that a sky-only parking lot cannot supply.
    before=set(bpy.context.scene.objects)
    wall=studio.studio_mat('S240 lighting facade',(.35,.32,.27),.83)
    window=studio.studio_mat('S240 lighting window',(.018,.028,.045),.30)
    for sign in [-1,1]:
        G.box('S240 procedural reflection facade '+str(sign),(sign*9,-1,6),( .05,24,12),wall,0)
        for y in range(-8,9,3):
            for z in [1.8,4.3,6.8,9.3]:G.box('S240 procedural reflection window',(sign*8.96,y,z),(.02,1.2,1.8),window,0)
    for ob in set(bpy.context.scene.objects)-before:
        ob['studio']=True;ob.visible_camera=False;ob.visible_shadow=False


def conditions(name):
    sc=bpy.context.scene;nt=sc.world.node_tree;bg=nt.nodes['Comparison environment']
    # Explicit radiance keeps the sky's zenith dark blue. A bright atmospheric
    # background at photographic exposure made the glass and roof milky.
    up=nt.nodes['Comparison horizon elevation'].inputs['Value'].links[0].from_socket
    ramp=nt.nodes.get('S240 calibrated sky') or nt.nodes.new('ShaderNodeValToRGB');ramp.name='S240 calibrated sky'
    ramp.color_ramp.elements[0].position=0;ramp.color_ramp.elements[0].color=(.32,.44,.65,1)
    ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=(.030,.10,.24,1)
    nt.links.new(up,ramp.inputs[0]);nt.links.new(ramp.outputs['Color'],bg.inputs['Color'])
    nt.nodes['Comparison sky saturation'].inputs['Saturation'].default_value=.65
    bg.inputs['Strength'].default_value=3.8
    sky=nt.nodes['Comparison clear sky'];sky.sun_rotation=math.radians(145 if 'rear' in name else 35)
    sun=bpy.data.objects['Comparison sun'];sun.data.energy=4.0;sun.data.angle=math.radians(.8)
    sun.rotation_euler=Vector((6,-4,-9) if 'rear' in name else (6,4,-9)).to_track_quat('-Z','Y').to_euler()
    return 'Procedural clear sky, 51-degree sun, warm neutral facades; no photographic lighting input'
