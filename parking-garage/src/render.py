"""All checkpoint views import external glTF. Procedural clear sky and sun."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from kit import gpu,studio
import geometry as G
from plan import FLOOR,SPAN,deck_z
from setting import town


def lighting(elevation=18,azimuth=-135,interior=False):
    sc=bpy.context.scene
    world=bpy.data.worlds.new('Original procedural clear sky');world.use_nodes=True;sc.world=world
    n=world.node_tree.nodes;l=world.node_tree.links;sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(elevation);sky.sun_rotation=math.radians(azimuth);sky.sun_disc=False
    sky.altitude=.1;sky.air_density=1;sky.dust_density=.35
    l.new(sky.outputs[0],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.32
    light=bpy.data.lights.new('Raking sun','SUN');light.energy=2.8;light.angle=math.radians(.55)
    ob=bpy.data.objects.new('Raking sun',light);sc.collection.objects.link(ob)
    v=Vector((math.cos(math.radians(elevation))*math.cos(math.radians(azimuth)),math.cos(math.radians(elevation))*math.sin(math.radians(azimuth)),math.sin(math.radians(elevation))))
    ob.rotation_euler=(-v).to_track_quat('-Z','Y').to_euler()
    # Actual imported fixture sockets create bounded pools. Emissive lenses
    # remain in the glTF; the area sources are presentation lighting.
    for socket in list(sc.objects):
        if socket.get('socket_kind')!='light_emitter':continue
        ld=bpy.data.lights.new(socket.name+' pool','AREA');ld.energy=38;ld.shape='RECTANGLE';ld.size=1.0;ld.size_y=.14;ld.color=(1,.86,.63)
        oo=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(oo);oo.location=socket.matrix_world.translation;oo.rotation_euler=(0,0,0)
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.7 if not interior else .0


def shots(p):
    L,W=p['length'],p['width'];fy=p['flat_y'];ry=p['ramp_y'];top=(p['levels']-1)*FLOOR;ex=L/2-p['end_length']/2
    return dict(hero=dict(location=(-L/2-23,-W/2-25,1.65),target=(0,0,4.0 if p['levels']==4 else 3.0),lens=35),
        above=dict(location=(-L*.88,-W*1.7,top+57),target=(0,0,top/2),lens=43,paths=True),
        aisle=dict(location=(-L/2+9,fy,1.65),target=(L/2-8,fy,1.70),lens=38,interior=True),
        ramp_turn=dict(location=(L/2-2,fy-1,1.65+FLOOR),target=(L/2-10,ry,1.0+FLOOR),lens=28,interior=True),
        top_deck=dict(location=(-L/2+6,fy-3,top+1.65),target=(L/3,fy,top+1.70),lens=35),
        entry=dict(location=(ex-8,-W/2-15,1.65),target=(ex,-W/2+2,1.8),lens=40),
        tower=dict(location=(-L/2-15,-W/2-12,1.65),target=(-L/2-2.5,-W/2+2.8,4),lens=35),
        scale=dict(location=(L/2-14,-W/2-12,1.65),target=(L/2-3,-W/2+1.5,1.1),lens=45,human=True))


def overlays(p):
    m=G.material('Drive path diagram cyan',(.025,.55,.80),.6,emission=.4);G.M['Diagram']=m
    b=G.Mesh('Drive and pedestrian path overlay')
    # Draw the upper circuit, where the actual slab does not hide the route.
    row=p['paths'][-2]
    b.tube([(x,y,z+.09) for x,y,z in row['points']],.095,'Diagram',8)
    b.finish()


def render_shot(out,shot,width,samples,engine='CYCLES'):
    sc=bpy.context.scene
    cam=bpy.data.objects.new('Export review camera',bpy.data.cameras.new('Export review camera'));sc.collection.objects.link(cam);sc.camera=cam
    cam.location=shot['location'];cam.rotation_euler=(Vector(shot['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=shot['lens'];cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL'
    if 'roll' in shot:cam.rotation_euler.rotate_axis('Z',shot['roll'])
    aspect=shot.get('aspect',1.6);sc.render.resolution_x=width;sc.render.resolution_y=round(width/aspect);sc.render.resolution_percentage=100
    sc.render.engine=engine
    if engine=='CYCLES':gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=7;sc.cycles.transparent_max_bounces=12
    sc.render.image_settings.file_format='PNG';out.parent.mkdir(parents=True,exist_ok=True);sc.render.filepath=str(out.resolve());bpy.ops.render.render(write_still=True)
    return dict(camera=list(cam.location),eye_height_m=float(cam.location.z),lens_mm=float(cam.data.lens),engine=engine,
        exposure=sc.view_settings.exposure,width=width,height=sc.render.resolution_y,output=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest())


def main():
    a=argparse.ArgumentParser();a.add_argument('--source');a.add_argument('--out',type=Path,default=Path('renders/checkpoint'));a.add_argument('--width',type=int,default=1200);a.add_argument('--samples',type=int,default=32);a.add_argument('--engine',default='CYCLES');a.add_argument('--shots',default='all');a.add_argument('--seeds',default='101,202');a.add_argument('--matches',action='store_true');args=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.matches:
        from matches import render_matches
        render_matches(args,render_shot,lighting);return
    receipts=[]
    for seed in map(int,args.seeds.split(',')):
        p=json.loads(Path(f'build/garage-{seed}.json').read_text())
        for name,shot in shots(p).items():
            if args.shots!='all' and name not in args.shots.split(','):continue
            bpy.ops.wm.read_factory_settings(use_empty=True)
            path=Path(f'export/ParkingGarage-{seed}.gltf');bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
            rt=next(o for o in bpy.context.scene.objects if o.parent is None)
            context=town(p,rt);bpy.context.view_layer.update()
            if shot.get('paths'):overlays(p)
            if shot.get('human'):
                for o in studio.human():o.location+=Vector((p['length']/2-2,-p['width']/2+1.6,0))
            lighting(interior=shot.get('interior',False));receipt=render_shot(args.out/str(seed)/(name+'.png'),shot,args.width,args.samples,args.engine)
            receipt.update(seed=seed,name=name,source=str(path),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),cars=len(context['actors']),car_triangles=context['actor_triangles'],context_triangles=context['context_triangles'])
            receipts.append(receipt);(args.out/'views.json').write_text(json.dumps(receipts,indent=2)+'\n')
            (Path('build')/f'actors-{seed}.json').write_text(json.dumps({k:v for k,v in context.items() if k!='root'},indent=2)+'\n')
    if args.shots=='all' or args.shots=='modules':
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path('export/ParkingGaragePieces.gltf').resolve()));G.palette()
        plane=G.Mesh('Module inspection ground');plane.box((50,30,-.22),(160,150,.22),'Deck');plane.finish();lighting()
        shot=dict(location=(135,-115,105),target=(48,30,3),lens=44,aspect=1.4)
        receipts.append(render_shot(args.out/'modules.png',shot,max(args.width,1800),args.samples,args.engine));(args.out/'views.json').write_text(json.dumps(receipts,indent=2)+'\n')


if __name__=='__main__':main()
