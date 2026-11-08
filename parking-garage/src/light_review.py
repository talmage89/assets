"""Outdoor daylight and fluorescent practicals for exported open structures.

Sky/sun are procedural. Fixture powers are presentation area lights at export
sockets; diffuse bounce, rather than emissive appearance, lights the soffit.
"""
import math
import json
from pathlib import Path
import bpy
from mathutils import Vector


def lighting(elevation=18,azimuth=-135,interior=False):
    sc=bpy.context.scene;world=bpy.data.worlds.new('Clear sky with daylight bounce');world.use_nodes=True;sc.world=world
    nodes=world.node_tree.nodes;links=world.node_tree.links
    sky=nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(elevation);sky.sun_rotation=math.radians(azimuth);sky.sun_disc=False
    sky.altitude=100;sky.air_density=1;sky.aerosol_density=.35
    links.new(sky.outputs[0],nodes.get('Background').inputs['Color']);nodes.get('Background').inputs['Strength'].default_value=.50 if interior else .22
    light=bpy.data.lights.new('Low raking daylight','SUN');light.energy=4.5;light.color=(1,.91,.79);light.angle=math.radians(.65)
    ob=bpy.data.objects.new(light.name,light);sc.collection.objects.link(ob)
    sun=Vector((math.cos(math.radians(elevation))*math.cos(math.radians(azimuth)),math.cos(math.radians(elevation))*math.sin(math.radians(azimuth)),math.sin(math.radians(elevation))))
    ob.rotation_euler=(-sun).to_track_quat('-Z','Y').to_euler()
    for socket in list(sc.objects):
        if socket.get('socket_kind')!='light_emitter':continue
        for upward,power in ((False,socket.get('emitter_down_watts',55)),(True,socket.get('emitter_up_watts',25))):
            if power<=0:continue
            ld=bpy.data.lights.new(socket.name+(' uplight' if upward else ' downlight'),'AREA');ld.energy=power;ld.shape='RECTANGLE';ld.size=.11;ld.size_y=1.15;ld.color=(1,1,1)
            ld.size=socket.get('uplight_size_x',.11) if upward else socket.get('emitter_size_x',.11);ld.size_y=socket.get('emitter_size_y',1.15)
            oo=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(oo)
            oo.location=socket.matrix_world@Vector((socket.get('uplight_x',.15),0,socket.get('uplight_z',.065)) if upward else (0,0,-socket.get('downlight_offset',.015)))
            oo.rotation_euler=socket.matrix_world.to_euler()
            if upward:oo.rotation_euler.rotate_axis('X',math.pi)
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.65 if interior else -.75
    sc.cycles.diffuse_bounces=7;sc.cycles.glossy_bounces=5;sc.cycles.transmission_bounces=10;sc.cycles.max_bounces=12


def views(p,original):
    s=original(p);L,W=p['length'],p['width'];municipal=p['system']=='precast'
    baseline=Path('build/lookdev/baseline-cameras.json')
    if baseline.exists():s.update(json.loads(baseline.read_text())[str(p['seed'])])
    s['retained_hero']=dict(s['hero']);s['above'].pop('paths',None)
    s['retained_aisle']=dict(s['aisle'])
    s['plan_path']=dict(s['above'],paths=True)
    # Across the public street: 35mm at a measured 1.65m, foreground reduced
    # to the walk/curb, meters, trees and intersecting traffic lanes.
    s['hero']['aspect']=2.35
    if not municipal:
        s['hero']=dict(s['retained_hero'],aspect=2.35)
    s['aisle']=dict(location=(-L/2+10,p['flat_y']-1.6,1.65),target=(L/2-8,p['flat_y']+5,1.9),lens=32,interior=True)
    # Additional construction view angles across the tee stems; the retained
    # aisle itself is unchanged for the required before/after evidence.
    s['tee_detail']=dict(location=(-L/2+10,p['flat_y']-2,1.65),target=(-L/2+19,p['flat_y']+4,2.50),lens=35,interior=True)
    tower=p['towers'][0]
    s['tower_landing']=dict(location=(-L/2+6,tower[1]+.3,1.65),target=(tower[0]+2.78,tower[1],1.45),lens=35,interior=True)
    s['tower_open']=dict(s['tower_landing'],open_lift=True)
    s['eevee']=dict(s['hero'],engine='BLENDER_EEVEE')
    for shot in s.values():shot['max_bounces']=12
    return s
