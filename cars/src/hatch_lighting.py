"""Diffuse late-summer daylight estimated from the four-year reference pair.

No hard cast shadow is visible. A broad weak sun is constrained by the shadow
under the mirror and wheel contact; the hemispherical sky dominates both views.
"""
import math
import bpy
from mathutils import Vector
from kit import studio,model as G
CONDITIONS={'front':dict(elevation=24,azimuth=-130,energy=3.25,sky=.225),
            'rear':dict(elevation=24,azimuth=140,energy=3.25,sky=.230)}

def setup():
    sc=bpy.context.scene
    for ob in sc.objects:
        if ob.get('studio') and ob.type=='LIGHT':ob.data.energy=0
        if ob.name.startswith('Studio black reflection flag'):ob.hide_render=True
    nt=sc.world.node_tree;nt.nodes.clear()
    sky=nt.nodes.new('ShaderNodeTexSky');sky.name='H120 diffuse sky';sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False;sky.air_density=1;sky.aerosol_density=2.0
    hue=nt.nodes.new('ShaderNodeHueSaturation');hue.inputs['Saturation'].default_value=.20;nt.links.new(sky.outputs[0],hue.inputs['Color'])
    bg=nt.nodes.new('ShaderNodeBackground');bg.name='H120 sky strength';nt.links.new(hue.outputs['Color'],bg.inputs['Color'])
    out=nt.nodes.new('ShaderNodeOutputWorld');nt.links.new(bg.outputs[0],out.inputs[0])
    data=bpy.data.lights.new('H120 diffuse sun','SUN');data.angle=math.radians(18)
    ob=bpy.data.objects.new('H120 diffuse sun',data);sc.collection.objects.link(ob);ob['studio']=True
    mat=studio.studio_mat('H120 asphalt gray',(.115,.112,.107),.88)
    ob=G.box('H120 comparison asphalt',(0,0,-.025),(200,200,.05),mat,0);ob['studio']=True
    # Plain procedural facade supplies the low-angle building reflection in
    # the rear reference. It is scene context, never part of the car or atlas.
    mat=studio.studio_mat('H120 gray facade',(.95,.96,.96),.90)
    ob=G.box('H120 comparison facade',(3.4,-6.3,3),(4,.20,6),mat,0)
    ob.rotation_euler.z=math.radians(28);ob['studio']=True;ob.visible_camera=False

def conditions(name):
    sc=bpy.context.scene
    bpy.data.objects['H120 comparison facade'].hide_render='rear' not in name
    c=CONDITIONS['rear' if 'rear' in name else 'front']
    sky=sc.world.node_tree.nodes['H120 diffuse sky'];sky.sun_elevation=math.radians(c['elevation']);sky.sun_rotation=math.radians(c['azimuth'])
    sc.world.node_tree.nodes['H120 sky strength'].inputs['Strength'].default_value=c['sky']
    e,a=math.radians(c['elevation']),math.radians(c['azimuth']);towards=Vector((math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)))
    ob=bpy.data.objects['H120 diffuse sun'];ob.data.energy=c['energy'];ob.rotation_euler=(-towards).to_track_quat('-Z','Y').to_euler()
    return dict(method='Procedural multiple-scattering sky, diffuse sun, asphalt-gray ground; rear view includes an estimated plain gray facade',sun_elevation_degrees=c['elevation'],sun_azimuth_degrees=c['azimuth'],sun_energy=c['energy'],sky_strength=c['sky'],uncertainty_degrees=15,facade=(dict(center_m=[3.4,-6.3,3],size_m=[4,.20,6],yaw_degrees=28,linear_albedo=[.95,.96,.96],camera_visible=False) if 'rear' in name else None),estimate='No distinct hard shadows: mirror underside and tire contact constrain weak diffuse light, not a unique solar fit')
