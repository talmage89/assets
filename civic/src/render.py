"""Cycles evidence from fresh exports; no high scene or material substitution."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(HERE),str(ROOT)]
from kit import gpu


def context_signature():
    return hashlib.sha256(b''.join((HERE/n).read_bytes() for n in ('town.py','neighborhood.py','actors.py','library.py','sites.py','geo.py','turf.py'))).hexdigest()


def light(seed=101):
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable()
    sc.cycles.use_denoising=True;sc.cycles.max_bounces=8;sc.cycles.transparent_max_bounces=12
    world=bpy.data.worlds.new('Procedural clear civic sky');world.use_nodes=True;sc.world=world
    nodes=world.node_tree.nodes;sky=nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(18);sky.sun_rotation=math.radians(210 if seed==101 else 145);sky.sun_disc=False;sky.air_density=1;sky.aerosol_density=.015
    world.node_tree.links.new(sky.outputs[0],nodes['Background'].inputs['Color']);nodes['Background'].inputs['Strength'].default_value=.045
    d=bpy.data.lights.new('Low front raking sun','SUN');d.energy=5.3;d.color=(1,.95,.86);d.angle=math.radians(.45)
    direction=(.866,.50,-.325) if seed==101 else (-.82,.572,-.325)
    ob=bpy.data.objects.new(d.name,d);sc.collection.objects.link(ob);ob.rotation_euler=Vector(direction).to_track_quat('-Z','Y').to_euler()
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.05


SHOTS={
    '101':dict(hero=((24,-46,1.72),(-6,-4,4.0),38),above=((77,-101,77),(-1,0,0),48),entry=((-1,-21,1.72),(-6,-9,2.7),45),cornice=((-4,-17,1.72),(-6,-11.5,8.3),50),police=((-36,34,1.72),(-14,18,2.2),42),scale=((-2,-23,1.72),(-6,-10,2.0),40)),
    '202':dict(hero=((23,-53,1.72),(-6,-2,2.8),42),above=((84,-94,72),(0,0,1),48),bays=((-18,-33,1.72),(-12,-5,2.5),45),interior=((-16,-7,1.72),(-13,5,2.9),28),tower=((-3,34,1.72),(-17,14,7),40),scale=((15,-21,1.72),(-6,-5,2),38))}
SHOTS['101']['flag']=((-18,-25,7.7),(-20.6,-19,8.5),60)
SHOTS['202']['scupper']=((10,17,3.8),(-1.8,9.3,4.7),50)
for seed in ('101','202'):SHOTS[seed]['hero-fixed']=SHOTS[seed]['hero']
SHOTS['101']['hero']=((20,-48,1.72),(-6,-4,4.0),38)
SHOTS['202']['hero']=((14,-49,1.72),(-6,-2,3.1),45)
for seed in ('101','202'):
    SHOTS[seed].update(front=((-6,-57,7),(-6,0,5),45),
        side=((60,0,9),(-6,0,5),45),back=((-6,65,9),(-6,0,5),45),
        top=((-6,0,100),(-6,0,0),46))


def camera(spec,width):
    loc,target,lens=spec;sc=bpy.context.scene
    cam=bpy.data.objects.new('Evidence camera',bpy.data.cameras.new('Evidence camera'));sc.collection.objects.link(cam)
    cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens;cam.data.clip_end=2500;sc.camera=cam
    sc.render.resolution_x=width;sc.render.resolution_y=round(width*.68);sc.render.resolution_percentage=100
    return cam


def open_bay():
    from door_motion import pose
    pose([o for o in bpy.context.scene.objects if o.get('overhead_door')=='Bay_1'],1)
    bpy.context.view_layer.update()
    for node in list(bpy.context.scene.objects):
        if node.get('socket_kind')!='interior_light':continue
        data=bpy.data.lights.new('Practical bay light','AREA');data.energy=node.get('power_w',240);data.shape='RECTANGLE';data.size=1.6;data.size_y=.25;data.color=(1,.89,.72)
        ob=bpy.data.objects.new(data.name,data);bpy.context.collection.objects.link(ob);ob.location=node.matrix_world.translation


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('renders/final'));ap.add_argument('--width',type=int,default=1400);ap.add_argument('--samples',type=int,default=40);ap.add_argument('--shots',default='all');ap.add_argument('--seeds',default='101,202');ap.add_argument('--buildings-only',action='store_true');ap.add_argument('--matches',action='store_true');ap.add_argument('--sheets',action='store_true');ap.add_argument('--sheets-only',action='store_true');ap.add_argument('--engine',default='CYCLES');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.sheets_only:
        from sheets import render
        args.out.mkdir(parents=True,exist_ok=True);render(args.out,args.width,args.samples);return
    if args.matches:
        recipes=json.loads(Path('build/matched-cameras.json').read_text())
        jobs=[(name,str(row['seed']),(row['shot']['location'],row['shot']['target'],row['shot']['lens']),row) for name,row in recipes.items() if args.shots=='all' or name in args.shots.split(',')]
    else:jobs=[(name,seed,spec,None) for seed in args.seeds.split(',') for name,spec in SHOTS[seed].items() if args.shots=='all' or name in args.shots.split(',')]
    if args.sheets:jobs.append(('eevee','202',SHOTS['202']['hero'],None))
    rows=[]
    for name,seed,spec,match in jobs:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        building_only=args.buildings_only or name in ('front','side','back','top') or (match and match.get('building_only'))
        source=Path('build/review')/(('Civic-' if building_only else 'Site-')+seed+'.glb')
        bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
        if not building_only:
            offset=json.loads(Path('build/family.json').read_text())['Site-'+seed]['plan'].get('origin_offset_m',(0,0,0))
            for ob in list(bpy.context.scene.objects):
                if ob.parent is None:ob.location+=Vector(offset)
        if match and match.get('building_only'):
            data=json.loads(Path('build/family.json').read_text())['Civic-'+seed]
            off=Vector(data['plan']['origin_offset_m'])+Vector((-6,0,0))
            for ob in list(bpy.context.scene.objects):
                if ob.parent is None:ob.location+=off
        if not building_only or (match and match.get('building_only')):
            from town import context
            context(101 if building_only else int(seed))
        elif not match:
            from sites import ground
            from geo import Assembly
            ground(Assembly('InspectionGround'),'InspectionConcrete',(-120,120,-120,120),'Concrete',-.035)
        light(int(seed));sc=bpy.context.scene;sc.render.engine=args.engine if name!='eevee' else 'BLENDER_EEVEE'
        sc.cycles.samples=args.samples;cam=camera(spec,args.width)
        if name in ('tower','scupper'):sc.view_settings.exposure+=.55
        if match:
            sc.render.resolution_y=round(args.width/match['shot']['aspect']);cam.rotation_euler.rotate_axis('Z',match['shot']['roll'])
            estimates={'hall-street':((-.45,.60,-.72),3.4,.23),'station-bay':((.72,.50,-.50),3.0,.22),'entry-order':((.55,.40,-.65),2.6,.24)}
            direction,power,sky=estimates[name];sun=bpy.data.objects['Low front raking sun'];sun.rotation_euler=Vector(direction).to_track_quat('-Z','Y').to_euler();sun.data.energy=power;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=sky
        if name=='interior':open_bay()
        if name=='scale':
            from kit.studio import human
            desired=Vector((-6,-15.4,.145) if seed=='101' else (3.7,-9,.145))
            for ob in human():ob.location+=desired-Vector((-1.03,.24,0))
        out=Path('renders/eevee')/seed/'hero.png' if name=='eevee' else args.out/(name+'.png') if args.matches else args.out/seed/(name+'.png');out.parent.mkdir(parents=True,exist_ok=True)
        sc.render.image_settings.file_format='PNG';sc.render.filepath=str(out.resolve());bpy.ops.render.render(write_still=True)
        row=dict(image=str(out),source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),camera=spec,width=args.width,samples=args.samples,engine=sc.render.engine,exposure=sc.view_settings.exposure)
        sun=bpy.data.objects['Low front raking sun'];sky=next(n for n in sc.world.node_tree.nodes if n.type=='TEX_SKY')
        row['lighting']=dict(sun_rotation=list(sun.rotation_euler),sun_energy=sun.data.energy,sun_angle=sun.data.angle,sky_strength=sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value,air=sky.air_density,aerosol=sky.aerosol_density)
        row['camera_matrix_world']=[list(v) for v in cam.matrix_world];row['render_recipe_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        if not building_only or match:row['context_recipe_sha256']=context_signature()
        out.with_suffix('.json').write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'render-receipts.json').write_text(json.dumps(rows,indent=2)+'\n')
    if args.sheets:
        from sheets import render
        render(args.out,args.width,args.samples)


if __name__=='__main__':main()
