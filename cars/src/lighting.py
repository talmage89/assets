"""Original outdoor reflection stage, with photo-specific sky and sun.

All proxies are generated lighting equipment, hidden to the camera. Reference
photographs are never sampled, projected or used by the shader/world graph.
"""
import math,random
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
    sky.air_density=1.1;sky.aerosol_density=1.1
    bg=tree.nodes.new('ShaderNodeBackground');bg.name='Comparison environment';bg.inputs['Strength'].default_value=.12
    neutral=tree.nodes.new('ShaderNodeHueSaturation');neutral.name='Comparison sky saturation';neutral.inputs['Saturation'].default_value=.25
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
    cloud=tree.nodes.new('ShaderNodeRGB');cloud.outputs[0].default_value=(.68,.73,.80,1)
    overcast=tree.nodes.new('ShaderNodeMixRGB');overcast.name='Comparison overcast gradient';overcast.blend_type='MULTIPLY';overcast.inputs[0].default_value=1
    tree.links.new(cloud.outputs[0],overcast.inputs[1]);tree.links.new(height.outputs[0],overcast.inputs[2])
    out=tree.nodes.new('ShaderNodeOutputWorld');tree.links.new(bg.outputs[0],out.inputs[0])
    sun_data=bpy.data.lights.new('Comparison sun','SUN');sun_data.energy=3.5;sun_data.angle=math.radians(.7);sun_data.color=(1,.97,.90)
    sun=bpy.data.objects.new('Comparison sun',sun_data);sc.collection.objects.link(sun)
    sun.rotation_euler=Vector((-6,4,-9)).to_track_quat('-Z','Y').to_euler()
    ground=studio.studio_mat('Comparison asphalt',(.095,.102,.104),.88)
    G.box('Comparison ground',(0,0,-.022),(120,120,.04),ground,0)
    # Low parked forms leave the sky visible above the belt reflection; the
    # former continuous 5.3 m walls erased that critical horizon structure.
    colors=[(.34,.36,.36),(.015,.020,.026),(.53,.52,.48),(.08,.10,.13)]
    for sign in [-1,1]:
        for k in range(6):
            mat=studio.studio_mat('Comparison parked finish '+str(sign)+str(k),colors[k%4],.25)
            x=sign*(6.5+.4*math.sin(k*3));y=-12+k*4.5
            G.box('Comparison parked body',(x,y,.77),(1.8,3.4,.85),mat,.16,3)
            G.box('Comparison parked cabin',(x,y+.2,1.35),(1.55,1.8,.50),mat,.17,3)
    foliage=studio.studio_mat('Comparison foliage',(.025,.042,.012),.95)
    # Many irregular small leaf clusters replace solid, identical tree blobs.
    # These are reflected silhouettes only, independent of the reference pixels.
    rng=random.Random(150);verts=[];faces=[]
    centers=[(sign*(8.5+2*math.sin(k*3)),-17+k*6.3,5.0) for sign in [-1,1] for k in range(6)]
    centers += [(-5.5,-.5,8.5),(5.5,-.5,8.5)]
    for cx,cy,cz in centers:
        for k in range(480):
            t=rng.uniform(0,math.tau);v=rng.uniform(-1,1);r=rng.random()**.33
            x=cx+2.3*r*math.sqrt(1-v*v)*math.cos(t);y=cy+2.1*r*math.sqrt(1-v*v)*math.sin(t);z=cz+2.4*r*v
            size=rng.uniform(.16,.36);start=len(verts)
            verts.extend([(x+size,y,z),(x-size,y,z),(x,y+size,z),(x,y-size,z),(x,y,z+size*.75),(x,y,z-size*.75)])
            faces.extend(tuple(start+i for i in f) for f in [(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)])
    G.smooth(G.mesh('Comparison irregular foliage',verts,faces,foliage))
    for ob in set(sc.objects)-before:
        ob['studio']=True;ob.visible_camera=False;ob.visible_shadow=False
        if ob.name=='Comparison ground':ob.visible_camera=True;ob.is_shadow_catcher=True


def conditions(name):
    """Ram: clear sun; Ford: diffuse overcast, as visible in the photos."""
    sc=bpy.context.scene;nt=sc.world.node_tree;bg=nt.nodes['Comparison environment'];sky=nt.nodes['Comparison clear sky']
    if name.startswith('aged_'):
        nt.links.new(nt.nodes['Comparison sky gradient'].outputs[0],bg.inputs['Color']);bg.inputs['Strength'].default_value=.12
        bpy.data.objects['Comparison sun'].data.energy=3.5
        return 'clear sky; sun from front/right at 51.3 degrees; parking-lot reflections'
    for link in list(bg.inputs['Color'].links):nt.links.remove(link)
    nt.links.new(nt.nodes['Comparison overcast gradient'].outputs[0],bg.inputs['Color']);bg.inputs['Strength'].default_value=3.6
    bpy.data.objects['Comparison sun'].data.energy=0
    return 'overcast sky; no direct sun; trees and parked forms in reflections'
