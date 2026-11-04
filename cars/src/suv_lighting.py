"""X220 procedural daylight and gloss-clay inspection environment."""
import bpy
from lighting import outdoor,conditions


def daylight(overcast=False,reflections=False):
    outdoor()
    description=conditions('used_front' if overcast else 'aged_front')
    bpy.data.objects['Studio seamless'].hide_render=True
    # A dark real plane supplies the lower reflected hemisphere. It remains
    # visible to glossy rays and receives shadows; no photographic environment.
    ground=bpy.data.objects['Comparison ground'];ground.visible_shadow=True
    if overcast:
        node=bpy.context.scene.world.node_tree.nodes['Comparison overcast gradient'].inputs[1].links[0].from_node
        node.outputs[0].default_value=(.74,.74,.74,1)
    if reflections:roadside_reflections()
    return description


def gloss_clay():
    daylight()
    nt=bpy.context.scene.world.node_tree
    nt.nodes['Comparison sky saturation'].inputs['Saturation'].default_value=.15
    nt.nodes['Comparison environment'].inputs['Strength'].default_value=.35
    bpy.data.objects['Comparison sun'].data.energy=2.0
    bpy.data.objects['Comparison sun'].data.angle=.08
    for m in bpy.data.materials:
        if m.name=='Clay body':
            bs=m.node_tree.nodes['Principled BSDF']
            bs.inputs['Base Color'].default_value=(.18,.18,.18,1)
            bs.inputs['Roughness'].default_value=.22
            bs.inputs['Metallic'].default_value=.18
            bs.inputs['Coat Weight'].default_value=1
            bs.inputs['Coat Roughness'].default_value=.08


def inspection_fill(name):
    """A photographer's area bounce for enclosed construction inspection."""
    from mathutils import Vector
    if name=='underbody':location,target,power,size=(1.5,-1.0,.10),(0,0,.45),20,1.8
    elif name=='cargo_open':location,target,power,size=(-.8,3,1.9),(0,1.4,.8),75,1.5
    else:
        location,target,power,size=(0,-.1,1.40),(.2,-.4,.8),12,.5
        from kit import model as G
        from kit.studio import studio_mat
        # A photographer's black flag cuts the reflected sky without altering
        # the actual glass shader. The cabin bounce reveals the construction.
        flag=G.box('Interior reflection flag',(2.2,-.3,1.6),(.02,3.5,2.4),studio_mat('Interior black flag',(.006,.007,.008),1),0)
        flag['studio']=True;flag.visible_camera=False;flag.visible_shadow=False
    data=bpy.data.lights.new('Inspection bounce','AREA');data.energy=power;data.shape='DISK';data.size=size
    ob=bpy.data.objects.new('Inspection bounce',data);bpy.context.scene.collection.objects.link(ob)
    ob.location=location;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    if name.startswith('interior_'):
        ob.visible_camera=False;ob.visible_glossy=False;ob.visible_transmission=False


def roadside_reflections():
    """Original camera-hidden roadside canopies supply reflected structure.

    Procedural sky/ground remain the light sources. These coarse irregular
    silhouettes are inspection equipment, not vehicle textures or asset meshes.
    No photographed environment is sampled or reconstructed.
    """
    import math
    from kit import model as G
    from kit.studio import studio_mat
    canopy=studio_mat('Procedural roadside canopy',(.025,.032,.022),.93)
    trunk=studio_mat('Procedural roadside trunk',(.06,.05,.036),.88)
    for side in [-1,1]:
        for j,y in enumerate([-12,-7,-2,3,8,13]):
            z=3.5+.35*math.sin(j*2.3+side);points=[]
            for i in range(80):
                a=math.tau*i/80;r=1+.12*math.sin(5*a+j)+.07*math.sin(11*a+.4*j)+.035*math.cos(17*a)
                points.append((side*(9+.3*math.sin(j)),y+2.7*r*math.cos(a),z+2.1*r*math.sin(a)))
            ob=G.mesh('Roadside reflection canopy '+str(side)+str(j),points,[tuple(range(80))],canopy)
            stem=G.box('Roadside reflection trunk '+str(side)+str(j),(side*9,y,1.6),(.18,.18,3.2),trunk,0)
            for part in [ob,stem]:
                part['studio']=True;part.visible_camera=False;part.visible_shadow=False
