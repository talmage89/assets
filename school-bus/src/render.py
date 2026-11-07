"""Checkpoint presentation always imports the delivery for exported views."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(HERE),str(ROOT),str(ROOT/'cars/src')]
from kit import gpu,model as G
from kit.studio import human
from views import SHOTS

def material(name,color,rough=.7):
    m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;return m

def setup(width,samples,engine):
    sc=bpy.context.scene;sc.render.engine=engine
    if engine=='CYCLES':gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=10;sc.cycles.transmission_bounces=8;sc.cycles.transparent_max_bounces=16
    sc.world=bpy.data.worlds.new('Procedural low school sun');sc.world.use_nodes=True;nt=sc.world.node_tree
    sky=nt.nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False;sky.sun_elevation=math.radians(18);sky.sun_rotation=math.radians(225)
    nt.links.new(sky.outputs[0],nt.nodes['Background'].inputs['Color']);nt.nodes['Background'].inputs['Strength'].default_value=.18
    ld=bpy.data.lights.new('Low raking sun','SUN');ld.energy=3.0;ld.angle=math.radians(.8);ld.color=(1,.94,.84)
    sun=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(sun);sun.rotation_euler=Vector((.60,.80,-.33)).to_track_quat('-Z','Y').to_euler()
    G.box('Checkpoint asphalt',(0,0,-.035),(1000,1000,.06),material('Asphalt',(.047,.052,.052)),0)
    cam=bpy.data.objects.new('Bus checkpoint camera',bpy.data.cameras.new('Bus checkpoint camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL';cam.data.clip_start=.025;cam.data.clip_end=10000
    sc.render.resolution_x=width;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.25
    return cam

def pose(shot):
    vals={}
    for name in ['Entrance_front','Entrance_rear','Stop_arm','Crossing_arm','Roof_hatch_front','Roof_hatch_rear']:
        ob=bpy.data.objects.get(name)
        if ob:vals[ob]=ob.rotation_euler.copy()
    if shot.get('pose')=='entrance':
        bpy.data.objects['Entrance_front'].rotation_euler.z=math.radians(95);bpy.data.objects['Entrance_rear'].rotation_euler.z=math.radians(-95)
    if shot.get('pose')=='warning':
        bpy.data.objects['Stop_arm'].rotation_euler.z=math.radians(-90);bpy.data.objects['Crossing_arm'].rotation_euler.z=math.radians(-90)
    if shot.get('pose')=='hatches':
        for name in ['Roof_hatch_front','Roof_hatch_rear']:bpy.data.objects[name].rotation_euler.x=math.radians(-65)
    for m in bpy.data.materials:
        if not m.use_nodes:continue
        bs=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if not bs:continue
        if m.get('lamp_lit_strength') or 'Lamps' in m.name or 'Warning' in m.name:
            bs.inputs['Emission Strength'].default_value=12 if shot.get('lit') else 0
    if any('Lamps' in m.name for m in bpy.data.materials):
        from lamp_states import apply
        apply(red=shot.get('lit',False),strobe=shot.get('lit',False))
    return vals

def imported(path):
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    return list(set(bpy.context.scene.objects)-before)

def digest(path):
    if path.suffix!='.gltf':return hashlib.sha256(path.read_bytes()).hexdigest()
    d=json.loads(path.read_text());fs=[path]+[path.parent/i['uri'] for k in ['buffers','images'] for i in d.get(k,[])]
    return hashlib.sha256(b''.join(hashlib.sha256(f.read_bytes()).digest() for f in fs)).hexdigest()

def render(a):
    path=Path(a.source).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if path.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(path))
    else:imported(path)
    for ob in bpy.context.scene.objects:
        if ob.get('bake_only'):ob.hide_render=True
    cam=setup(a.width,a.samples,a.engine);sc=bpy.context.scene;receipts={}
    shots=SHOTS if a.shots=='all' else {n:SHOTS[n] for n in a.shots.split(',')}
    if a.calibration:shots={n:d['shot'] for n,d in json.loads(Path(a.calibration).read_text()).items()}
    for name,s in shots.items():
        temp=[];vals=pose(s)
        if s.get('fleet'):
            for seed,dx in [(102,-4.1),(103,4.1)]:
                obs=imported(path.parent/f'C75-{seed}.gltf')
                for ob in obs:
                    if ob.parent is None:ob.location.x+=dx
                temp+=obs
        if s.get('human'):
            adults=human();temp+=adults
            for ob in adults:ob.location+=Vector((-2.5,-3.1,0))
            children=human();temp+=children
            for ob in children:
                ob.location*=1.1/1.8;ob.scale*=1.1/1.8;ob.location+=Vector((-2.5,-4.0,0))
        if name=='hero' and a.school:
            school=Path(a.school).resolve();obs=imported(school);temp+=obs
            # Place the native campus so the actual reserved socket sits at the bus origin.
            socket=next(o for o in obs if 'Bus_loading_0' in o.name)
            bpy.context.view_layer.update();xf=socket.matrix_world.inverted()
            for ob in obs:
                if ob.parent is None:ob.matrix_world=xf@ob.matrix_world
            receipts['school']=dict(source=str(school.relative_to(ROOT)),sha256=digest(school),socket=socket.name,
                fit='Original 11m reservation with a 12.192m bus; centered fit measured separately')
        cam.location=s['location'];cam.rotation_euler=(Vector(s['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',s.get('roll',0))
        cam.data.type='ORTHO' if 'ortho' in s else 'PERSP';cam.data.ortho_scale=s.get('ortho',14);cam.data.lens=s['lens']
        sc.render.resolution_y=round(a.width/s.get('aspect',1.78));sc.render.filepath=str((out/f'{name}.png').resolve())
        bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
        receipts[name]=dict(camera=s,source=str(path.relative_to(ROOT)),sha256=digest(path),stage='source' if path.suffix=='.blend' else 'export',engine=a.engine,width=a.width,samples=a.samples)
        (out/'provenance.json').write_text(json.dumps(receipts,indent=2))
        for ob,r in vals.items():ob.rotation_euler=r
        for ob in temp:bpy.data.objects.remove(ob,do_unlink=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--shots',default='all');p.add_argument('--width',type=int,default=1400);p.add_argument('--samples',type=int,default=48);p.add_argument('--engine',default='CYCLES');p.add_argument('--school');p.add_argument('--calibration');render(p.parse_args(sys.argv[sys.argv.index('--')+1:]))
if __name__=='__main__':main()
