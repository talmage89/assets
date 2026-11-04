"""Photo-specific procedural autumn sun/sky; no studio reflection rectangles.

Directions are estimates from visible ground/mirror shadows, not EXIF: front
27 +/- 6 degrees, rear 30 +/- 6. The wheel-only camera calibration stays fixed.
"""
import math
import bpy
from mathutils import Vector
from kit import studio,model as G

CONDITIONS={
 'front':dict(elevation=27,azimuth=-155,energy=8.0,sky=.025),
 'rear':dict(elevation=30,azimuth=155,energy=8.0,sky=.025),
}

def setup():
    sc=bpy.context.scene
    for ob in sc.objects:
        if ob.get('studio') and ob.type=='LIGHT':ob.data.energy=0
        if ob.name.startswith('Studio black reflection flag'):ob.hide_render=True
    nt=sc.world.node_tree;nt.nodes.clear()
    sky=nt.nodes.new('ShaderNodeTexSky');sky.name='S240 autumn sky';sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False;sky.air_density=1;sky.aerosol_density=.3
    bg=nt.nodes.new('ShaderNodeBackground');bg.name='S240 sky strength';nt.links.new(sky.outputs['Color'],bg.inputs['Color'])
    out=nt.nodes.new('ShaderNodeOutputWorld');nt.links.new(bg.outputs[0],out.inputs[0])
    data=bpy.data.lights.new('S240 matched sun','SUN');data.angle=math.radians(.53);data.color=(1,.98,.95) # photo pairs are already white-balanced on stated neutrals
    sun=bpy.data.objects.new('S240 matched sun',data);sc.collection.objects.link(sun);sun['studio']=True
    ground=studio.studio_mat('S240 asphalt gray',(.085,.083,.078),.88)
    ob=G.box('S240 comparison asphalt',(0,0,-.025),(200,200,.05),ground,0);ob['studio']=True


    plaster=studio.studio_mat('S240 reflected ochre plaster',(.38,.28,.18),.86)
    masonry=studio.studio_mat('S240 reflected terra cotta',(.27,.14,.085),.87)
    stone=studio.studio_mat('S240 reflected gray render',(.25,.27,.25),.87)
    glazing=studio.studio_mat('S240 reflected facade glazing',(.035,.060,.072),.28)
    for key,yaw in [('front',-45),('rear',35)]:
        rotation=math.radians(yaw)
        center=Vector((14,3,9)) if key=='front' else Vector((14,-12,1.4))
        along=Vector((math.cos(rotation),math.sin(rotation),0))
        normal=Vector((-along.y,along.x,0))
        if normal.dot(center)>0:normal.negate()
        height=18 if key=='front' else 2.8
        wall=G.box('S240 reflected building '+key,center,(32,.12,height),plaster,0);wall.rotation_euler.z=rotation
        obs=[wall]
        for x,mat in [(-10,masonry),(2,stone)]:
            ob=G.box('S240 reflected original facade bay '+key,center+along*x+normal*.07,(5.5,.04,height),mat,0);ob.rotation_euler.z=rotation;obs.append(ob)
        for x in [-10,-6,-2,2,6,10]:
            for z in ([-6,-3,0,3,6] if key=='front' else [0]):
                ob=G.box('S240 facade window '+key,center+along*x+Vector((0,0,z))+normal*.08,(1.4,.04,1.65),glazing,0);ob.rotation_euler.z=rotation;obs.append(ob)
        for ob in obs:ob['studio']=True;ob['comparison_view']=key;ob.visible_camera=False;ob.visible_shadow=False

def conditions(name):
    sc=bpy.context.scene;c=CONDITIONS['rear' if 'rear' in name else 'front']
    for ob in sc.objects:
        if ob.get('comparison_view'):ob.hide_render=ob['comparison_view']!=('rear' if 'rear' in name else 'front')
    sky=sc.world.node_tree.nodes['S240 autumn sky'];sky.sun_elevation=math.radians(c['elevation']);sky.sun_rotation=math.radians(c['azimuth']);sc.world.node_tree.nodes['S240 sky strength'].inputs['Strength'].default_value=c['sky']
    e=math.radians(c['elevation']);a=math.radians(c['azimuth']);towards=Vector((math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)))
    sun=bpy.data.objects['S240 matched sun'];sun.data.energy=c['energy'];sun.rotation_euler=(-towards).to_track_quat('-Z','Y').to_euler()
    return dict(method='Procedural multiple-scattering sky, 0.53 degree sun, asphalt-gray ground',sun_elevation_degrees=c['elevation'],sun_azimuth_degrees=c['azimuth'],uncertainty_elevation_degrees=6,estimate='Ground and mirror shadow direction/length relative to known wheel and mirror height; no gray card or EXIF lighting measurement')
