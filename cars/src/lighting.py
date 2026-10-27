"""Procedural outdoor comparison rig. No photograph or downloaded environment.

Proxy ground and distant architecture exist only to supply exterior reflections;
like studio flags they are hidden to the camera and excluded from asset counts.
"""
import math
import bpy
from kit import model as G
from kit import studio
from mathutils import Vector


def outdoor():
    sc=bpy.context.scene;before=set(sc.objects)
    tree=sc.world.node_tree;sky=tree.nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING'
    sky.sun_elevation=math.radians(32);sky.sun_rotation=math.radians(-125);sky.sun_disc=False
    sky.air_density=1.2;sky.aerosol_density=2.0
    bg=tree.nodes.get('Background');tree.links.new(sky.outputs['Color'],bg.inputs['Color']);bg.inputs['Strength'].default_value=.22
    for ob in sc.objects:
        if ob.type=='LIGHT' and ob.get('studio'):ob.data.energy*=.12
        if ob.name.startswith('Studio black reflection flag'):ob.hide_render=True
    sunlight=bpy.data.lights.new('Comparison sun','SUN');sunlight.energy=6.0;sunlight.angle=math.radians(2.5);sunlight.color=(1,.94,.84)
    sun=bpy.data.objects.new('Comparison sun',sunlight);sc.collection.objects.link(sun);sun.rotation_euler=Vector((-6,4,-9)).to_track_quat('-Z','Y').to_euler()
    ground=studio.studio_mat('Comparison asphalt',(.12,.13,.125),.85)
    G.box('Comparison ground',(0,0,-.022),(80,80,.04),ground,0)
    wall=studio.studio_mat('Comparison distant masonry',(.20,.13,.090),.85)
    pane=studio.studio_mat('Comparison distant windows',(.012,.020,.023),.28)
    trim=studio.studio_mat('Comparison distant window trim',(.43,.44,.41),.7)
    # Original coarse buildings outside the vehicle footprint. These are lighting
    # equipment, not library assets or source mesh components.
    for sign in [-1,1]:
        x=sign*11
        G.box('Comparison facade '+str(sign),(x,0,2.65),(.12,24,5.3),wall,0)
        for row,z in enumerate([1.3,3.55]):
            for k in range(10):
                y=-10.8+2.4*k
                G.box('Comparison trim',(x-sign*.09,y,z),(.04,1.14,1.56),trim,0)
                G.box('Comparison window',(x-sign*.12,y,z),(.025,1.00,1.42),pane,0)
    foliage=studio.studio_mat('Comparison foliage',(.020,.035,.012),.95)
    for sign in [-1,1]:
        for k in range(6):
            x=sign*(7.6+.7*math.sin(k*3));y=-9+k*3.7
            loops=[]
            for z,r in [(1.8,0),(2.2,1.1),(3.0,1.7),(4.1,1.3),(4.7,0)]:
                loops.append([(x+r*(1+.15*math.sin(i*5+k))*math.cos(i*math.tau/12),y+r*math.sin(i*math.tau/12),z+.12*math.sin(i*3+k)) for i in range(12)])
            G.smooth(G.loft('Comparison canopy',loops,foliage))
    for ob in set(sc.objects)-before:
        ob['studio']=True;ob.visible_camera=False
        ob.visible_shadow=False
