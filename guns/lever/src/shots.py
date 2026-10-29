"""Checkpoint cameras. Exact socket aim, gray surround, procedural studio."""
from pathlib import Path
import os
import bpy
from mathutils import Vector
from kit import studio


def shot(location,target,lens=70,aspect=1.7,**kw):
    return dict(location=location,target=target,lens=lens,aspect=aspect,**kw)


SHOTS={
 'hero_right':shot((1.05,-.55,.58),(0,.20,.015),65,2.4,action='Idle',frame=0),
 'hero_left':shot((-1.05,-.50,.58),(0,.20,.015),65,2.4,action='Idle',frame=0),
 'right':shot((1.8,.225,.025),(0,.225,.025),ortho=1.04,aspect=3.6,action='Idle',frame=0),
 'left':shot((-1.8,.225,.025),(0,.225,.025),ortho=1.04,aspect=3.6,action='Idle',frame=0),
 'top':shot((0,.225,1.8),(0,.225,0),ortho=1.04,aspect=3.6,action='Idle',frame=0,roll=1.57079632679),
 'front':shot((0,1.5,.02),(0,0,.02),ortho=.22,aspect=1.3,action='Idle',frame=0),
 'receiver':shot((.31,.30,.215),(0,.111,.029),65,1.5,action='Idle',frame=0),
 'receiver_left':shot((-.31,.28,.22),(0,.111,.029),65,1.5,action='Idle',frame=0),
 'raking_right':shot((.60,-.35,.23),(0,.10,.01),62,2.1,action='Idle',frame=0,raking=True),
 'raking_left':shot((-.60,-.35,.23),(0,.10,.01),62,2.1,action='Idle',frame=0,raking=True),
 'open':shot((.29,.31,.25),(0,.116,.018),65,1.5,action='Cycle',frame=36),
 'open_left':shot((-.32,.27,.20),(0,.118,.004),65,1.5,action='Cycle',frame=36),
 'lever_open':shot((.64,.18,.22),(0,.105,-.075),60,1.15,action='Cycle',frame=36),
 'lever_rest_ortho':shot((1.8,.065,-.072),(0,.065,-.072),ortho=.36,aspect=1.1,action='Cycle',frame=0),
 'lever_mid_ortho':shot((1.8,.065,-.072),(0,.065,-.072),ortho=.36,aspect=1.1,action='Cycle',frame=13.2258064516),
 'lever_open_ortho':shot((1.8,.065,-.072),(0,.065,-.072),ortho=.36,aspect=1.1,action='Cycle',frame=36),
 'hammer':shot((.18,-.10,.16),(0,.060,.038),78,1.45,action='Idle',frame=0),
 'trigger':shot((.21,.074,-.013),(0,.076,-.012),78,1.5,action='Idle',frame=0),
 'trigger_quarter_view':shot((.18,.0,.07),(0,.079,-.012),78,1.5,action='Idle',frame=0),
 'sights':shot((.14,.19,.19),(0,.297,.064),75,1.7,action='Idle',frame=0),
 'sight_blade':shot((0,.09,.065),(0,.283,.065),ortho=.033,aspect=1.7,action='Idle',frame=0),
 'wrist_raking':shot((.19,-.10,.125),(0,.035,.030),78,1.5,action='Idle',frame=0,raking=True),
 'front_sight':shot((.12,.59,.12),(0,.686,.060),85,1.5,action='Idle',frame=0),
 'stock':shot((.40,-.40,.18),(0,-.12,-.02),72,1.7,action='Idle',frame=0),
 'butt_plate':shot((-.16,-.44,.045),(0,-.254,-.050),75,1.4,action='Idle',frame=0),
 'butt_plate_profile':shot((.8,-.245,-.050),(0,-.245,-.050),ortho=.145,aspect=1.1,action='Idle',frame=0),
 'wrist_under':shot((.14,-.04,-.17),(0,.006,.003),78,1.5,action='Idle',frame=0),
 'receiver_raking_right':shot((.34,-.08,.12),(0,.121,.028),70,1.8,action='Idle',frame=0,raking=True),
 'receiver_raking_left':shot((-.34,-.08,.12),(0,.121,.028),70,1.8,action='Idle',frame=0,raking=True),
 'forend':shot((.32,.46,.17),(0,.31,.021),70,1.8,action='Idle',frame=0),
 'gate_open':shot((.28,.16,.10),(0,.143,.02),68,1.7,action='Reload',frame=42),
 'aimed':shot((0,-.085,.066),(0,.69,.066),36/(2*__import__('math').tan(__import__('math').radians(35))),1.6,
              action='Idle',frame=0,aimed=True,opaque=True),
 'cartridge':shot((.100,-.03,.085),(0,.032,0),75,1.7,exposure=-1.8,background='transparent'),
 'case':shot((.090,.09,.075),(0,.026,0),78,1.7,exposure=-1.8,background='transparent'),
 'mouth':shot((.034,.13,.031),(0,.048,0),85,1.4,exposure=-1.8,background='transparent'),
 'headstamp':shot((.008,-.07,.004),(0,0,0),85,1.4,exposure=-1.8,background='transparent'),
}
DEFAULT_SHOTS=','.join(n for n in SHOTS if n not in ('cartridge','case','mouth','headstamp'))
PHOTO_POSES={n:dict(action='Idle',frame=0) for n in ('right_photo','left_photo','trigger_right','trigger_quarter','hammer_photo')}
PHOTO_POSES['open_photo']=dict(action='Cycle',frame=36)
STRIP_SHOT=shot((1.50,-.30,.58),(0,.22,-.03),55,1.6,exposure=.8)
if os.environ.get('PD_LEVER_DETAIL_STRIP')=='1':
    STRIP_SHOT=shot((.86,-.005,.28),(0,.14,-.02),48,1.4,exposure=.8)


def floor_height(source):return -.014 if Path(source).stem in ('case','cartridge') else -.22


def configure_scene(sc,source):
    # Held-weapon photography uses reflection cards against a surrounding
    # neutral gray world, with no downloaded environment or visible floor.
    world=bpy.data.worlds.new('Procedural gray studio') if not sc.world else sc.world
    sc.world=world;world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.16,.16,.16,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.6
    for ob in sc.objects:
        if ob.name.startswith('Studio seamless'):ob.hide_render=True
    def area(name,location,target,size,power):
        data=bpy.data.lights.new(name,'AREA');data.shape='RECTANGLE'
        data.energy=power;data.size,data.size_y=size
        ob=bpy.data.objects.new(name,data);sc.collection.objects.link(ob)
        ob.location=location;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    area('Lever top strip',(.05,.20,.8),(0,.2,0),(.6,.15),38)
    area('Lever action fill',(.32,.12,.26),(0,.12,.025),(.3,.3),10)
    area('Lever rear edge',(-.24,-.35,.25),(0,-.10,0),(.3,.5),20)
    # All card colors remain neutral. No blue calibration tint is introduced.
    for ob in sc.objects:
        if ob.type=='LIGHT':ob.data.color=(1,1,1)
    nt=world.node_tree;old=nt.nodes['Background']
    bg=nt.nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=(.16,.16,.16,1)
    path=nt.nodes.new('ShaderNodeLightPath');mix=nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(path.outputs['Is Camera Ray'],mix.inputs[0]);nt.links.new(old.outputs[0],mix.inputs[1])
    nt.links.new(bg.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],nt.nodes['World Output'].inputs['Surface'])
    def exact_camera(scene,*_):
        if scene.get('opaque_socket'):
            scene.render.film_transparent=False
            cam=scene.camera;eye=scene.objects['Socket_Eye'].matrix_world
            assert (cam.matrix_world.translation-eye.translation).length<1e-7
            for ca,sa in [((0,0,-1),(0,1,0)),((0,1,0),(0,0,1))]:
                assert ((cam.matrix_world.to_3x3()@Vector(ca))-(eye.to_3x3()@Vector(sa))).length<1e-7
    bpy.app.handlers.render_pre.append(exact_camera)


def prepare_shot(sc,s):
    sc['opaque_socket']=bool(s.get('opaque'))
    for name in ('Key softbox','Camera fill'):
        ob=bpy.data.objects.get(name)
        if ob:ob.hide_render=bool(s.get('raking'))
