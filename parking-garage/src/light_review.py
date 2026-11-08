"""Outdoor daylight and fluorescent practicals for exported open structures.

Sky/sun are procedural. Fixture powers are presentation area lights at export
sockets; diffuse bounce, rather than emissive appearance, lights the soffit.
"""
import math
import bpy
from mathutils import Vector


def lighting(elevation=18,azimuth=-135,interior=False):
    sc=bpy.context.scene;world=bpy.data.worlds.new('Clear sky with daylight bounce');world.use_nodes=True;sc.world=world
    nodes=world.node_tree.nodes;links=world.node_tree.links
    sky=nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(elevation);sky.sun_rotation=math.radians(azimuth);sky.sun_disc=False
    sky.altitude=100;sky.air_density=1;sky.aerosol_density=.35
    links.new(sky.outputs[0],nodes.get('Background').inputs['Color']);nodes.get('Background').inputs['Strength'].default_value=.65
    light=bpy.data.lights.new('Low raking daylight','SUN');light.energy=3.0;light.color=(1,.91,.79);light.angle=math.radians(.65)
    ob=bpy.data.objects.new(light.name,light);sc.collection.objects.link(ob)
    sun=Vector((math.cos(math.radians(elevation))*math.cos(math.radians(azimuth)),math.cos(math.radians(elevation))*math.sin(math.radians(azimuth)),math.sin(math.radians(elevation))))
    ob.rotation_euler=(-sun).to_track_quat('-Z','Y').to_euler()
    for socket in list(sc.objects):
        if socket.get('socket_kind')!='light_emitter':continue
        for upward,power in ((False,115),(True,45)):
            ld=bpy.data.lights.new(socket.name+(' uplight' if upward else ' downlight'),'AREA');ld.energy=power;ld.shape='RECTANGLE';ld.size=.11;ld.size_y=1.15;ld.color=(.94,1,.90)
            oo=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(oo);oo.location=socket.matrix_world@Vector((.15,0,.065) if upward else (0,0,-.015))
            oo.rotation_euler=socket.matrix_world.to_euler()
            if upward:oo.rotation_euler.rotate_axis('X',math.pi)
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.15 if interior else -1.35
    sc.cycles.diffuse_bounces=7;sc.cycles.glossy_bounces=5;sc.cycles.transmission_bounces=10;sc.cycles.max_bounces=12


def views(p,original):
    s=original(p);L,W=p['length'],p['width'];municipal=p['system']=='precast'
    s['retained_hero']=dict(s['hero']);s['above'].pop('paths',None)
    s['plan_path']=dict(s['above'],paths=True)
    # Across the public street: 35mm at a measured 1.65m, foreground reduced
    # to the walk/curb, meters, trees and intersecting traffic lanes.
    s['hero']['aspect']=1.85
    if not municipal:
        s['hero']=dict(location=(-L/2-32,-58,1.65),target=(-1,-W/2,4.4),lens=35,aspect=1.85)
    # Additional construction view angles across the tee stems; the retained
    # aisle itself is unchanged for the required before/after evidence.
    s['tee_detail']=dict(location=(-L/2+10,p['flat_y']-2,1.65),target=(-L/2+19,p['flat_y']+4,2.50),lens=35,interior=True)
    s['eevee']=dict(s['hero'],engine='BLENDER_EEVEE_NEXT')
    return s
