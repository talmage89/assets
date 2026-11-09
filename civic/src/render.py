"""Cycles evidence from fresh exports; no high scene or material substitution."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(HERE),str(ROOT)]
from kit import gpu


def light():
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable()
    sc.cycles.use_denoising=True;sc.cycles.max_bounces=8;sc.cycles.transparent_max_bounces=12
    world=bpy.data.worlds.new('Procedural clear civic sky');world.use_nodes=True;sc.world=world
    nodes=world.node_tree.nodes;sky=nodes.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(22);sky.sun_rotation=math.radians(230);sky.sun_disc=False;sky.air_density=1.1;sky.dust_density=.4
    world.node_tree.links.new(sky.outputs[0],nodes['Background'].inputs['Color']);nodes['Background'].inputs['Strength'].default_value=.18
    d=bpy.data.lights.new('Low front raking sun','SUN');d.energy=3.0;d.angle=math.radians(1.0)
    ob=bpy.data.objects.new(d.name,d);sc.collection.objects.link(ob);ob.rotation_euler=Vector((.72,.55,-.36)).to_track_quat('-Z','Y').to_euler()
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.35


SHOTS={
    '101':dict(hero=((29,-57,1.72),(-6,-4,4.0),42),above=((77,-101,77),(-1,0,0),48),entry=((-1,-21,1.72),(-6,-9,2.7),45),cornice=((-4,-17,1.72),(-6,-11.5,8.3),50),police=((-36,34,1.72),(-14,14,2.2),42),scale=((-2,-23,1.72),(-6,-10,2.0),40)),
    '202':dict(hero=((28,-63,1.72),(-6,-2,2.8),42),above=((84,-94,72),(0,0,1),48),bays=((-18,-33,1.72),(-12,-5,2.5),45),interior=((-15,-9,1.72),(-15,2,2),35),tower=((-37,32,1.72),(-17,14,7),40),scale=((15,-21,1.72),(-6,-5,2),38))}


def camera(spec,width):
    loc,target,lens=spec;sc=bpy.context.scene
    cam=bpy.data.objects.new('Evidence camera',bpy.data.cameras.new('Evidence camera'));sc.collection.objects.link(cam)
    cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens;cam.data.clip_end=2500;sc.camera=cam
    sc.render.resolution_x=width;sc.render.resolution_y=round(width*.68);sc.render.resolution_percentage=100
    return cam


def open_bay():
    for ob in bpy.context.scene.objects:
        if ob.get('overhead_door')!='Bay_1':continue
        j=ob['section_index'];ph=ob['panel_pitch_m'];h=ob['door_height_m']
        ob.location.y+=.6+(7-j)*ph;ob.location.z+=h+.17-j*ph;ob.rotation_euler.x=-math.pi/2


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('renders/checkpoint'));ap.add_argument('--width',type=int,default=1400);ap.add_argument('--samples',type=int,default=40);ap.add_argument('--shots',default='all');ap.add_argument('--seeds',default='101,202');ap.add_argument('--buildings-only',action='store_true');ap.add_argument('--matches',action='store_true');ap.add_argument('--engine',default='CYCLES');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.matches:
        recipes=json.loads(Path('build/matched-cameras.json').read_text())
        jobs=[(name,str(row['seed']),(row['shot']['location'],row['shot']['target'],row['shot']['lens']),row) for name,row in recipes.items()]
    else:jobs=[(name,seed,spec,None) for seed in args.seeds.split(',') for name,spec in SHOTS[seed].items() if args.shots=='all' or name in args.shots.split(',')]
    rows=[]
    for name,seed,spec,match in jobs:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        source=Path('build/review')/(('Civic-' if args.buildings_only else 'Site-')+seed+'.glb')
        bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
        if not args.buildings_only:
            from town import context
            context(int(seed))
        light();sc=bpy.context.scene;sc.render.engine=args.engine;sc.cycles.samples=args.samples;cam=camera(spec,args.width)
        if match:
            sc.render.resolution_y=round(args.width/match['shot']['aspect']);cam.rotation_euler.rotate_axis('Z',match['shot']['roll'])
        if name=='interior':open_bay()
        if name=='scale':
            from kit.studio import human
            for ob in human():ob.location+=Vector((-6,-13,.15))
        out=args.out/(name+'.png') if args.matches else args.out/seed/(name+'.png');out.parent.mkdir(parents=True,exist_ok=True)
        sc.render.image_settings.file_format='PNG';sc.render.filepath=str(out.resolve());bpy.ops.render.render(write_still=True)
        row=dict(image=str(out),source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),camera=spec,width=args.width,samples=args.samples,engine=args.engine,exposure=sc.view_settings.exposure)
        out.with_suffix('.json').write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'render-receipts.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':main()
