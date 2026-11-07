"""Every form view imports the external glTF; no source-scene render shortcut."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(HERE),str(ROOT)]
from kit.gpu import enable
from plans import school,world


def views(p):
    ex,ey=p['entry'];b=next(b for b in p['blocks'] if b['id']==('Finger_A' if p['type']=='finger' else 'Cluster_B' if p['type']=='courtyard' else 'South_Classrooms'))
    face='west' if p['type']=='finger' else 'north' if p['type']=='courtyard' else 'south'
    o=next(o for o in b['openings'] if o['type']=='window' and o['face']==face);pt=world((o['u'],0,0),o['origin'],o['yaw']);nx,ny,_=world((0,-1,0),(0,0),o['yaw']);tx,ty,_=world((1,0,0),(0,0),o['yaw'])
    gym=next(b for b in p['blocks'] if b['kind']=='gym');l,r,f,k=gym['rect']
    door=next(o for o in gym['openings'] if o['type'] in ('double','door'));dp=world((door['u'],0,0),door['origin'],door['yaw'])
    dnx,dny,_=world((0,-1,0),(0,0),door['yaw'])
    result=dict(
      hero=dict(location=(ex-45,ey-57,1.68),target=(ex+6,ey+12,2.50),lens=40,aspect=1.80),
      above=dict(location=(225,-245,210),target=(0,0,0),lens=48,aspect=1.55),
      plan=dict(location=(92,-114,106),target=(0,0,0),lens=45,aspect=1.5),
      rear=dict(location=(68,87,10),target=(8,20,2.0),lens=42,aspect=1.8),
      windows=dict(location=(pt[0]+nx*11+tx*7,pt[1]+ny*11+ty*7,1.68),target=(pt[0]+tx*1.5,pt[1]+ty*1.5,1.95),lens=45,aspect=1.55),
      entry=dict(location=(ex-10,ey-17,1.68),target=(ex,ey,2.0),lens=42,aspect=1.55),
      gym=dict(location=(l-6,f-16,1.68),target=((l+r)/2,f,3.3),lens=40,aspect=1.5),
      door=dict(location=(dp[0]+dnx*4.4-1.4,dp[1]+dny*4.4,1.60),target=(dp[0],dp[1],1.25),lens=48,aspect=1.25),
      roof=dict(location=(r+10,k+13,13),target=((l+r)/2,(f+k)/2,5.5),lens=45,aspect=1.5))
    if p['type']=='finger':result['windows']=dict(location=(pt[0]+nx*6+tx*5,pt[1]+ny*6+ty*5,1.68),target=(pt[0]+tx*1.5,pt[1]+ty*1.5,1.95),lens=35,aspect=1.55)
    if p['type']=='courtyard':
        result['hero']=dict(location=(ex-57,ey-44,1.68),target=(ex+2,ey+9,2.55),lens=40,aspect=1.80)
        result['gym']=dict(location=(l-4,f-10,1.68),target=((l+r)/2,f,3.3),lens=35,aspect=1.5)
    return result


def setup(width,samples,light=None):
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=8;sc.cycles.transparent_max_bounces=16;enable()
    worldmat=bpy.data.worlds.new('Procedural school daylight');sc.world=worldmat;worldmat.use_nodes=True
    ns,ls=worldmat.node_tree.nodes,worldmat.node_tree.links;bg=ns.get('Background');sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False;sky.sun_elevation=math.radians(24);sky.sun_rotation=math.radians(215);sky.altitude=100;sky.air_density=1.1
    ls.new(sky.outputs[0],bg.inputs[0]);bg.inputs[1].default_value=.20
    ld=bpy.data.lights.new('Raking school sun','SUN');sun=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(sun);ld.energy=3.1;ld.angle=math.radians(1.4);ld.color=(1,.96,.89)
    sun.rotation_euler=Vector((.62,.78,-.52)).to_track_quat('-Z','Y').to_euler()
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.45
    if light:
        ld.energy=light.get('energy',3.1);bg.inputs[1].default_value=light.get('sky',.20);ld.angle=math.radians(light.get('softness',1.4))
        sun.rotation_euler=Vector(light.get('direction',(.62,.78,-.52))).to_track_quat('-Z','Y').to_euler()
        sc.view_settings.exposure=light.get('exposure',-.45)
    # Procedural distant ground only; the entire visible school/site ships in
    # the glTF, including its library cars, plants, fences and ground modules.
    ma=bpy.data.materials.new('Distant ground');ma.use_nodes=True;bs=ma.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.045,.066,.021,1);bs.inputs['Roughness'].default_value=1
    from kit.model import box
    box('Distant ground',(0,0,-.12),(2400,2400,.10),ma,0)
    cam=bpy.data.objects.new('School review camera',bpy.data.cameras.new('School review camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL';cam.data.clip_end=3000;cam.data.clip_start=.03
    sc.render.resolution_x=width;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
    return cam,sun


def digest(path):
    d=json.loads(path.read_text());files=[path]+[path.parent/r['uri'] for k in ('buffers','images') for r in d.get(k,[])];return hashlib.sha256(b''.join(hashlib.sha256(p.read_bytes()).digest() for p in files)).hexdigest()


def render(path,out,width,samples,shots,light=None,engine='CYCLES'):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));cam,sun=setup(width,samples,light);sc=bpy.context.scene;sc.render.engine=engine
    out.mkdir(parents=True,exist_ok=True);receipt={}
    for name,s in shots.items():
        cam.location=s['location'];cam.rotation_euler=(Vector(s['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',s.get('roll',0));cam.data.lens=s['lens']
        if name=='rear' and not light:sun.rotation_euler=Vector((-.6,-.7,-.6)).to_track_quat('-Z','Y').to_euler()
        else:
            direction=(light or {}).get('direction',(.62,.78,-.52));sun.rotation_euler=Vector(direction).to_track_quat('-Z','Y').to_euler()
        sc.render.resolution_y=round(width/s['aspect']);sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        receipt[name]=dict(source=path.as_posix(),package_sha256=digest(path),camera=s,engine=engine,width=width,samples=samples,eye_height_m=s['location'][2],stage='exported checkpoint glTF; quick school materials',light=dict(sun_energy=sun.data.energy,sky_strength=sc.world.node_tree.nodes.get('Background').inputs[1].default_value,sun_direction=list(sun.rotation_euler),exposure=sc.view_settings.exposure))
    target=out/'provenance.json';existing=json.loads(target.read_text()) if target.exists() else {};existing.update(receipt);target.write_text(json.dumps(existing,indent=2))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source');ap.add_argument('--seeds',default='101,102,103');ap.add_argument('--out',type=Path,default=Path('renders/checkpoint'));ap.add_argument('--width',type=int,default=1400);ap.add_argument('--samples',type=int,default=32);ap.add_argument('--shots');ap.add_argument('--matches',action='store_true');ap.add_argument('--engine',default='CYCLES');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.matches:
        for name,row in json.loads(Path('build/matched-cameras.json').read_text()).items():
            render(Path('export')/('Campus-'+str(row['seed'])+'.gltf'),a.out,a.width,a.samples,{name:row['shot']},row.get('light'))
    else:
        for seed in map(int,a.seeds.split(',')):
            shots=views(school(seed))
            if a.shots:shots={k:v for k,v in shots.items() if k in a.shots.split(',')}
            render(Path('export')/('Campus-'+str(seed)+'.gltf'),a.out/str(seed),a.width,a.samples,shots,engine=a.engine)

if __name__=='__main__':main()
