"""Original outdoor reflection stage, with photo-specific sky and sun.

All proxies are generated lighting equipment, hidden to the camera. Reference
photographs are never sampled, projected or used by the shader/world graph.
"""
import math
import bpy
from kit import model as G
from kit import studio
from mathutils import Vector


def outdoor():
    sc=bpy.context.scene;before=set(sc.objects)
    for ob in sc.objects:
        if ob.type=='LIGHT' and ob.get('studio'):ob.data.energy=0
        if ob.name.startswith('Studio black reflection flag'):ob.hide_render=True
    tree=sc.world.node_tree;tree.nodes.clear()
    sky=tree.nodes.new('ShaderNodeTexSky');sky.name='Comparison clear sky';sky.sky_type='MULTIPLE_SCATTERING'
    sky.sun_elevation=math.atan2(9,math.hypot(6,4));sky.sun_rotation=math.radians(-35);sky.sun_disc=False
    sky.air_density=1;sky.aerosol_density=.35
    bg=tree.nodes.new('ShaderNodeBackground');bg.name='Comparison environment';bg.inputs['Strength'].default_value=.12
    neutral=tree.nodes.new('ShaderNodeHueSaturation');neutral.name='Comparison sky saturation';neutral.inputs['Saturation'].default_value=1
    tree.links.new(sky.outputs['Color'],neutral.inputs['Color']);tree.links.new(neutral.outputs[0],bg.inputs['Color'])
    # A bright low sky supplies the door band; the higher sky reflected by
    # the inclined windshield is darker. Flat worlds made every pane milky.
    tc=tree.nodes.new('ShaderNodeTexCoord');sep=tree.nodes.new('ShaderNodeSeparateXYZ');tree.links.new(tc.outputs['Normal'],sep.inputs[0])
    height=tree.nodes.new('ShaderNodeMapRange');height.clamp=True
    for key,value in [('From Min',0),('From Max',.8),('To Min',1),('To Max',.12)]:height.inputs[key].default_value=value
    up=tree.nodes.new('ShaderNodeMath');up.operation='MULTIPLY';up.inputs[1].default_value=-1
    tree.links.new(sep.outputs['Z'],up.inputs[0]);tree.links.new(up.outputs[0],height.inputs['Value'])
    multiply=tree.nodes.new('ShaderNodeMixRGB');multiply.name='Comparison sky gradient';multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=1
    tree.links.new(neutral.outputs[0],multiply.inputs[1]);tree.links.new(height.outputs[0],multiply.inputs[2]);tree.links.new(multiply.outputs[0],bg.inputs['Color'])
    clear=tree.nodes.new('ShaderNodeMixRGB');clear.blend_type='MULTIPLY';clear.inputs[0].default_value=1
    clear.inputs[2].default_value=(.92,.94,1.10,1);tree.links.new(multiply.outputs[0],clear.inputs[1])
    cloud=tree.nodes.new('ShaderNodeRGB');cloud.outputs[0].default_value=(.68,.73,.80,1)
    overcast=tree.nodes.new('ShaderNodeMixRGB');overcast.name='Comparison overcast gradient';overcast.blend_type='MULTIPLY';overcast.inputs[0].default_value=1
    tree.links.new(cloud.outputs[0],overcast.inputs[1]);tree.links.new(height.outputs[0],overcast.inputs[2])
    horizon=tree.nodes.new('ShaderNodeMapRange');horizon.name='Comparison horizon elevation';horizon.clamp=True
    for key,value in [('From Min',-.012),('From Max',.025),('To Min',0),('To Max',1)]:horizon.inputs[key].default_value=value
    tree.links.new(up.outputs[0],horizon.inputs['Value'])
    for name,upper in [('Comparison clear horizon',clear),('Comparison cloud horizon',overcast)]:
        mix=tree.nodes.new('ShaderNodeMixRGB');mix.name=name;mix.blend_type='MIX';mix.inputs[1].default_value=(.07,.075,.072,1)
        tree.links.new(horizon.outputs[0],mix.inputs[0]);tree.links.new(upper.outputs[0],mix.inputs[2])
    out=tree.nodes.new('ShaderNodeOutputWorld');tree.links.new(bg.outputs[0],out.inputs[0])
    sun_data=bpy.data.lights.new('Comparison sun','SUN');sun_data.energy=3.5;sun_data.angle=math.radians(.7);sun_data.color=(1,.97,.90)
    sun=bpy.data.objects.new('Comparison sun',sun_data);sc.collection.objects.link(sun)
    sun.rotation_euler=Vector((-6,4,-9)).to_track_quat('-Z','Y').to_euler()
    ground=studio.studio_mat('Comparison asphalt',(.095,.102,.104),.88)
    G.box('Comparison ground',(0,0,-.022),(2000,2000,.04),ground,0)
    for ob in set(sc.objects)-before:
        ob['studio']=True;ob.visible_camera=False;ob.visible_shadow=False
        if ob.name=='Comparison ground':ob.visible_camera=True;ob.is_shadow_catcher=True


def conditions(name):
    """Ram: clear sun; Ford: diffuse overcast, as visible in the photos."""
    sc=bpy.context.scene;nt=sc.world.node_tree;bg=nt.nodes['Comparison environment'];sky=nt.nodes['Comparison clear sky']
    horizon=nt.nodes['Comparison horizon elevation']
    horizon.inputs['From Min'].default_value=-.012;horizon.inputs['From Max'].default_value=.025
    if name.startswith('aged_'):
        rear=name=='aged_rear'
        nt.links.new(nt.nodes['Comparison clear horizon'].outputs[0],bg.inputs['Color']);bg.inputs['Strength'].default_value=.15 if rear else .17
        # The rear photo's low horizon is obstructed by the parking-lot facade.
        # A continuous elevation band preserves that occlusion without reflected
        # box/tree silhouettes suggesting dents in the authored side surfaces.
        if rear:
            horizon.inputs['From Min'].default_value=.008;horizon.inputs['From Max'].default_value=.075
        sky.sun_rotation=math.radians(146 if rear else -35)
        sun=bpy.data.objects['Comparison sun'];sun.data.energy=3.5
        sun.rotation_euler=Vector((6,-4,-9) if rear else (-6,4,-9)).to_track_quat('-Z','Y').to_euler()
        return ('clear sky; rear/left sun' if rear else 'clear sky; front/right sun')+' at 51.3 degrees; continuous sky/asphalt horizon'
    for link in list(bg.inputs['Color'].links):nt.links.remove(link)
    nt.links.new(nt.nodes['Comparison cloud horizon'].outputs[0],bg.inputs['Color']);bg.inputs['Strength'].default_value=3.6
    bpy.data.objects['Comparison sun'].data.energy=0
    return 'overcast sky; no direct sun; continuous sky/asphalt horizon'
