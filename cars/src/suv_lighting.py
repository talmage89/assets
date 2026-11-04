"""X220 procedural daylight and gloss-clay inspection environment."""
import bpy
from lighting import outdoor,conditions


def product_studio(shot):
    """The C150's broad diffusion panels, with no serrated roadside proxies."""
    import math
    from mathutils import Matrix
    for name in ['Right rim strip','Left rim strip']:bpy.data.objects[name].data.size*=4.5
    bpy.data.objects['Key softbox'].data.size*=1.6
    bpy.data.objects['Key softbox'].data.size_y*=1.2
    bpy.data.objects['Overhead reflection card'].data.size*=1.5
    bpy.context.view_layer.update()
    if shot['location'][1]>0:
        rotation=Matrix.Rotation(math.pi,4,'Z')
        for ob in bpy.context.scene.objects:
            if ob.get('studio') and ob.type in ['MESH','LIGHT']:ob.matrix_world=rotation@ob.matrix_world
    return dict(type='Family studio',lighting='Broad key/fill/rim diffusion panels, continuous rectangular reflectors; no outdoor proxies')


def matched_daylight(name):
    """Estimated diffuse sun/sky from the used references; no studio lights.

    Neither photo contains a sharp cast-shadow edge. Directions follow the
    visible bright upper-left front panels / upper-right rear panels and soft
    ground shadows. The declared broad angular uncertainty is intentional.
    """
    import math
    from mathutils import Vector
    outdoor();sc=bpy.context.scene;nt=sc.world.node_tree
    bpy.data.objects['Studio seamless'].hide_render=True
    rear=name=='used_rear'
    elevation=math.radians(34 if rear else 48);azimuth=math.radians(145 if rear else -40)
    sky=nt.nodes['Comparison clear sky'];sky.sun_elevation=elevation;sky.sun_rotation=azimuth
    sky.aerosol_density=.8;sky.sun_disc=False
    # Overcast daylight is a low-saturation scattering sky, not a studio gradient.
    nt.nodes['Comparison sky saturation'].inputs['Saturation'].default_value=.12
    # The photos show diffuse cloud cover. Mix a procedural overcast dome with
    # the scattering sky rather than substituting a clear, dark zenith.
    cloud=nt.nodes.new('ShaderNodeMixRGB');cloud.name='Diffuse cloud cover';cloud.inputs[0].default_value=.82
    nt.links.new(nt.nodes['Comparison sky saturation'].outputs[0],cloud.inputs[1]);cloud.inputs[2].default_value=(.74,.74,.74,1)
    horizon=nt.nodes['Comparison clear horizon'];nt.links.new(cloud.outputs[0],horizon.inputs[2])
    bg=nt.nodes['Comparison environment'];nt.links.new(horizon.outputs[0],bg.inputs['Color'])
    bg.inputs['Strength'].default_value=1.6 if rear else 1.25
    vector=Vector((math.cos(azimuth)*math.cos(elevation),math.sin(azimuth)*math.cos(elevation),math.sin(elevation)))
    sun=bpy.data.objects['Comparison sun'];sun.rotation_euler=(-vector).to_track_quat('-Z','Y').to_euler()
    sun.data.energy=.35 if rear else .16;sun.data.angle=math.radians(18 if rear else 25);sun.data.color=(1,.985,.96)
    ground=bpy.data.objects['Comparison ground'];ground.visible_shadow=True
    parking_surroundings(rear)
    return dict(type='Photo-estimated diffuse sun and scattering sky',sun_elevation_degrees=math.degrees(elevation),sun_azimuth_degrees=math.degrees(azimuth),sun_angular_diameter_degrees=18 if rear else 25,sun_energy=sun.data.energy,sky_strength=bg.inputs['Strength'].default_value,ground_linear_rgb=[.095,.102,.104],direction_uncertainty_degrees=20,observation='Soft tire/contact shadows; no sharp sun-shadow measurement available')


def parking_surroundings(rear=False):
    """Original smooth tree masses obstruct the low wooded parking horizon.

    Unlike the archived serrated billboards these are closed, smoothly shaded
    volumes and cast real shade. They do not reconstruct either photograph.
    Bright sky remains above them for the sloping glazing; low door reflections
    see the shaded surroundings actually present in both reference locations.
    """
    import math
    from kit import model as G
    from kit.studio import studio_mat
    leaf=studio_mat('Diffuse distant foliage',(.014,.022,.013),.95)
    if rear:
        # The November reference has a mostly bare, porous wooded horizon.
        # Effective leaf coverage integrates small gaps without fake serrated
        # silhouettes. A closed crown crosses two or more such thin surfaces.
        nt=leaf.node_tree;surface=nt.nodes['Principled BSDF'];out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
        transparent=nt.nodes.new('ShaderNodeBsdfTransparent');mix=nt.nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.10
        nt.links.new(transparent.outputs[0],mix.inputs[1]);nt.links.new(surface.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs['Surface'])
    bark=studio_mat('Diffuse distant bark',(.025,.022,.018),.95)
    for j in range(14):
        angle=math.tau*j/14;x=12*math.cos(angle);y=12*math.sin(angle)
        height=(5.1 if rear else 3.5)+.35*math.sin(j*1.7);rings=[];count=32
        for k in range(13):
            a=-math.pi/2+.035+(math.pi-.07)*k/12;r=math.cos(a)
            rings.append([(x+(2.9+.12*math.sin(3*t+j))*r*math.cos(t),y+(2.9+.12*math.sin(3*t+j))*r*math.sin(t),height+(2.8 if rear else 2.0)*math.sin(a)) for t in [math.tau*i/count for i in range(count)]])
        crown=G.smooth(G.loft('Matched parking canopy '+str(j),rings,leaf),180)
        trunk=G.cylinder('Matched parking trunk '+str(j),(x,y,0),(x,y,height),.14,bark,12)
        for ob in [crown,trunk]:ob['studio']=True;ob.visible_camera=False


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
