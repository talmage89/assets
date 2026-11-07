"""Cycles form judgments from freshly imported external checkpoint glTF.

All lighting is procedural. Native library geometry builds the neighborhood;
it is presentation context and never enters the park exports.
"""
import argparse,json,math,hashlib,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit import gpu
import geometry as Q
from park_site import load,remove

def setup(samples,energy=4.5,direction=(-.7,.35,-.55),sky=.08):
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True
    sc.world=bpy.data.worlds.new('Procedural late summer sky');sc.world.use_nodes=True
    nt=sc.world.node_tree;nt.nodes.clear();n=nt.nodes.new('ShaderNodeTexSky');n.sky_type='MULTIPLE_SCATTERING';n.sun_disc=False;n.sun_elevation=math.radians(30);n.sun_rotation=math.radians(215);n.air_density=1;n.aerosol_density=.3
    sat=nt.nodes.new('ShaderNodeHueSaturation');sat.name='Estimated sky chroma';nt.links.new(n.outputs[0],sat.inputs['Color'])
    bg=nt.nodes.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=sky;out=nt.nodes.new('ShaderNodeOutputWorld');nt.links.new(sat.outputs[0],bg.inputs[0]);nt.links.new(bg.outputs[0],out.inputs[0])
    sun=bpy.data.objects.new('Raking sun',bpy.data.lights.new('Raking sun','SUN'));sc.collection.objects.link(sun);sun.data.energy=energy;sun.data.angle=math.radians(.6);sun.rotation_euler=Vector(direction).to_track_quat('-Z','Y').to_euler()
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.2
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB'
    cam=bpy.data.objects.new('Form camera',bpy.data.cameras.new('Form camera'));sc.collection.objects.link(cam);sc.camera=cam
    cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.data.clip_end=1500;cam.data.clip_start=.02;return cam

def context(p):
    W,D=p['skating'];Q.palette();rt=Q.root('Presentation only context','context')
    # Four disjoint lawn regions leave the park's actual bowl void uncovered.
    SW,SD=p['site']
    for x0,x1,y0,y1 in ((-700,-SW/2,-700,700),(SW/2,700,-700,700),(-SW/2,SW/2,SD/2,700),(-SW/2,SW/2,-700,-SD/2)):
        Q.mesh('Surrounding city park',[(x0,y0,-.08),(x1,y0,-.08),(x1,y1,-.08),(x0,y1,-.08)],[(0,1,2,3)],rt,'Lawn')
    f=load('ground')
    # Continuous native road/curb/walk on both front and rear park streets.
    for cy in (-D/2-20.7264,D/2+22.86):
        for i in range(-15,16):
            x=i*6.096;Q.instance(f['Road_Straight_A'],'Context road',(x,cy,-.17),90,rt)
            for side in (-1,1):
                for dx in (-1.524,1.524):Q.instance(f['Curb_Straight'],'Context curb',(x+dx,cy+side*4.1148,-.17),90 if side>0 else -90,rt)
                for dx in (-2.286,-.762,.762,2.286):Q.instance(f['Sidewalk_A'],'Context sidewalk',(x+dx,cy+side*6.096,-.17),90 if side>0 else -90,rt)
    cx=W/2+22.86
    for i in range(-12,13):
        y=i*6.096;Q.instance(f['Road_Straight_A'],'Context east street',(cx,y,-.17),0,rt)
        for side in (-1,1):
            for dy in (-1.524,1.524):Q.instance(f['Curb_Straight'],'Context east curb',(cx+side*4.1148,y+dy,-.17),0 if side>0 else 180,rt)
            for dy in (-2.286,-.762,.762,2.286):Q.instance(f['Sidewalk_A'],'Context east sidewalk',(cx+side*6.096,y+dy,-.17),0 if side>0 else 180,rt)
    remove(f)
    f=load('houses');house=next(iter(f.values()))
    for i in range(-3,4):
        Q.instance(house,'Context town house',(i*23.0,D/2+39.624,-.1),0,rt)
    for i in range(-2,3):Q.instance(house,'Context east town house',(W/2+37.0,i*24.0,-.1),-90,rt)
    if p.get('terrain_yaw'):
        for i in range(-3,4):Q.instance(house,'Context south town house',(i*23.0,-D/2-39.624,-.1),180,rt)
        for i in range(-2,3):Q.instance(house,'Context west town house',(-W/2-37.0,i*24.0,-.1),90,rt)
    remove(f)
    f=load('tree');species=sorted(f.values(),key=lambda o:o.name)
    for i in range(-6,7):
        Q.instance(species[i%len(species)],'Context street tree',(i*13.5+5,D/2+31.0,-.1),(i*43)%360,rt)
    for i in range(7):
        Q.instance(species[i%len(species)],'Context park tree',(W/2+16+(i%2)*10,-20+i*12,-.1),i*71,rt)
    remove(f)
    return rt

def views(p):
    W,D=p['skating']
    shots=dict(above=dict(location=(-W*1.10,-D*1.70,57),target=(0,-3,0),lens=40,aspect=1.5),
               ground=dict(location=(-W*.68,-D*.77,1.65),target=(1,2,1.0),lens=40,aspect=1.9))
    if p['seed']==202:shots['ground']=dict(location=(18.7,-9,1.65),target=(-8,1,.8),lens=40,aspect=1.9)
    shots['plan']=dict(location=(0,0,65),target=(0,0,0),lens=40,aspect=1.5)
    if p['bowl']:
        x,y,z=p['bowl']['location'];shots['bowl_plan']=dict(location=(x,y,25),target=(x,y,z),lens=40,aspect=1.35)
    if p['seed']==202:shots['hero']=dict(location=(-15.6,-7.5,1.65),target=(4,3,.4),lens=35,aspect=1.85)
    if p['seed']==202:shots['steel_coping']=dict(location=(-13.6,10.8,2.32),target=(-12.2,10.1,1.22),lens=65,aspect=1.5)
    if p['seed']==101:
        shots['scale']=dict(location=(-24,-14,3.4),target=(-12,-1,-.3),lens=40,aspect=1.5,human_offset=(-13,-7.5,0))
        shots['transition']=dict(location=(-14.8,4.3,1.6),target=(-10,9,1),lens=45,aspect=1.5)
        shots['tag']=dict(location=(16,-1.5,.72),target=(15.392,3.045,.35),lens=65,aspect=1.5)
        shots['walk']=dict(location=(2,-20.5,.70),target=(.6,-19.4,0),lens=45,aspect=1.5)
        shots.update(hero=dict(location=(-19.0,-7.0,1.65),target=(4,1,1.0),lens=35,aspect=1.85),
                     bowl=dict(location=(-13,-3,1.4),target=(-13,-5.1,-.03),lens=50,aspect=1.5),
                     ledge=dict(location=(12.0,-10.0,1.25),target=(9.449,-6.6,.39),lens=55,aspect=1.5),
                     stairs=dict(location=(17,-4.2,1.70),target=(12.8,2,.61),lens=45,aspect=1.5),
                     deep_end=dict(location=(-8.25,-3.5,-.5),target=(-6.668,-1.2192,-2.14),lens=45,aspect=1.5),
                     fence=dict(location=(16,-20,1.5),target=(20,-18.288,1.3),lens=45,aspect=1.5),
                     edge=dict(location=(-22.6,-17.9,1.0),target=(-21,-16.75,-.01),lens=45,aspect=1.5),
                     trees=dict(location=(-38,-19,7),target=(-27.4,-10.6,6),lens=38,aspect=.9))
    if p['seed']==303:
        shots['prefab']=dict(sun_direction=(.5,.9,-.55),sun_energy=7,location=(2.25,4.95,1.4),target=(0,7.5,.65),lens=40,aspect=1.5)
        shots['prefab_side']=dict(sun_direction=(.5,.9,-.55),sun_energy=7,location=(2.6,5.6,1.0),target=(3.66,9.5,.60),lens=50,aspect=1.5)
        shots['plate']=dict(sun_direction=(-.7,-.7,-.40),sun_energy=7,location=(-.8,7.9,.43),target=(0,8.70,.02),lens=55,aspect=1.5)
        # Turn the same low sun 12 degrees in azimuth. The previous tree-gap
        # sun patch made an isolated white highlight on the far riding sheet.
        yaw=math.radians(12)
        shots['hero']=dict(location=(-10.97,-6.7056,1.65),target=(0,4,.7),lens=40,aspect=1.9,
                           sun_direction=(-.82*math.cos(yaw)-.4*math.sin(yaw),-.82*math.sin(yaw)+.4*math.cos(yaw),-.3))
    if p.get('terrain_yaw'):
        from mathutils import Matrix
        turn=Matrix.Rotation(math.radians(p['terrain_yaw']),4,'Z')
        for name,v in shots.items():
            if name in ('above','plan'):continue
            for key in ('location','target'):v[key]=list(turn@Vector(v[key]))
    return shots

def recipe_hash():
    h=hashlib.sha256()
    for name in ('render.py','geometry.py','park_site.py'):
        h.update((HERE/name).read_bytes())
    for path in sorted(Path('build/context').glob('*.glb')):h.update(path.read_bytes())
    return h.hexdigest()

def render(seed,folder,out,width,samples,names=None,custom=None,with_context=True,engine='CYCLES',manifest=None):
    source=Path(folder)/('Park_'+str(seed)+'.gltf')
    if not source.exists():source=source.with_suffix('.glb')
    info=json.loads(Path(manifest or ('build/park-'+str(seed)+'.json')).read_text());p=info['plan']
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()));assets=list(bpy.context.scene.objects)
    if with_context:context(p)
    from kit.studio import human
    silhouettes=human();human_rest={o:o.location.copy() for o in silhouettes}
    cam=setup(samples);sc=bpy.context.scene;sc.render.engine=engine;shots=custom or views(p);records={};out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for name,v in shots.items():
        if names and name not in names:continue
        if v.get('isolate'):
            for ob in assets:
                owner=ob
                while owner.parent:owner=owner.parent
                ob.hide_render=owner.name not in v['isolate']
        for ob in silhouettes:
            ob.hide_render='human_offset' not in v
            ob.location=human_rest[ob]+Vector(v.get('human_offset',(0,0,0)))
        cam.location=v['location'];cam.rotation_euler=(Vector(v['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
        if v.get('roll'):cam.rotation_euler.rotate_axis('Z',v['roll'])
        cam.data.lens=v.get('lens',40);cam.data.shift_y=v.get('shift_y',0)
        sc.view_settings.exposure=v.get('exposure',-.25)
        sc.render.resolution_x=width;sc.render.resolution_y=round(width/v.get('aspect',1.5));sc.render.resolution_percentage=100
        sun=bpy.data.objects['Raking sun'];sun.rotation_euler=Vector(v.get('sun_direction',(-.82,.4,-.30))).to_track_quat('-Z','Y').to_euler();sun.data.energy=v.get('sun_energy',12.0)
        sc.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=v.get('sky_strength',.08)
        sc.world.node_tree.nodes['Estimated sky chroma'].inputs['Saturation'].default_value=v.get('sky_saturation',.45)
        sun.data.angle=math.radians(v.get('sun_angle_degrees',.6))
        bpy.context.view_layer.update();sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        from external import bundle
        records[name]=dict(recipe_sha256=recipe_hash(),bundle_sha256=bundle(source) if source.suffix=='.gltf' else None,seed=seed,source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),camera=v,engine=engine,samples=samples,width=width,
            effective_lighting=dict(sun_direction_world=list(Vector(v.get('sun_direction',(-.82,.4,-.30))).normalized()),sun_elevation_degrees=math.degrees(math.asin(-Vector(v.get('sun_direction',(-.82,.4,-.30))).normalized().z)),exposure=sc.view_settings.exposure,sun_energy=sun.data.energy,sky_strength=sc.world.node_tree.nodes.get('Background').inputs['Strength'].default_value,sky_saturation=sc.world.node_tree.nodes['Estimated sky chroma'].inputs['Saturation'].default_value,view_transform=sc.view_settings.view_transform,look=sc.view_settings.look))
        (out/(name+'.json')).write_text(json.dumps(records[name],indent=2))
    return records

def main():
    p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--folder',default='export/checkpoint');p.add_argument('--engine',default='CYCLES');p.add_argument('--out',type=Path,default=Path('renders/checkpoint'));p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);p.add_argument('--seed',type=int);p.add_argument('--shots',nargs='+');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    for seed in ([a.seed] if a.seed else (101,202,303)):render(seed,a.folder,a.out/str(seed),a.width,a.samples,a.shots,engine=a.engine)

if __name__=='__main__':main()
