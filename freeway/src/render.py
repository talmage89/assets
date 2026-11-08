"""Cycles inspection of freshly imported external glTF; no source render path."""
import argparse,sys,json,math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit import gpu
from external import bundle
from render_recipe import digest as render_recipe

def setup(samples,engine):
    sc=bpy.context.scene;sc.render.engine=engine
    if engine=='CYCLES':
        gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True
        # Native pin oak's nested alpha cards require the same depth as its
        # family renderer; eight transparent hits falsely blacken the canopy.
        sc.cycles.transparent_max_bounces=128
    sc.world=bpy.data.worlds.new('Procedural raking daylight');sc.world.use_nodes=True
    ns=sc.world.node_tree.nodes;ls=sc.world.node_tree.links
    sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False;sky.sun_elevation=math.radians(17);sky.sun_rotation=math.atan2(-.65,.72);sky.air_density=.8;sky.aerosol_density=.12;sky.altitude=1200
    sat=ns.new('ShaderNodeHueSaturation');sat.inputs['Saturation'].default_value=1.0;ls.new(sky.outputs[0],sat.inputs['Color'])
    bg=ns.get('Background');ls.new(sat.outputs[0],bg.inputs[0]);bg.inputs['Strength'].default_value=.08
    sun=bpy.data.objects.new('Raking sun',bpy.data.lights.new('Raking sun','SUN'));sc.collection.objects.link(sun);sun.data.energy=7.0;sun.data.angle=math.radians(.53);sun.rotation_euler=Vector((-.72,.65,-.28)).to_track_quat('-Z','Y').to_euler()
    fill=bpy.data.objects.new('Photographic environment bounce',bpy.data.lights.new('Photographic environment bounce','AREA'));sc.collection.objects.link(fill);fill.data.energy=0
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.45
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB'
    cam=bpy.data.objects.new('Inspection camera',bpy.data.cameras.new('Inspection camera'));sc.collection.objects.link(cam);sc.camera=cam
    cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.data.clip_start=.025;cam.data.clip_end=10000
    return cam

def shots(seed):
    if seed==101:return {
        'hero':dict(location=(67.894475458,-69.253495475,8.086790339),target=(-125,25,-6.5),lens=50,aspect=1.78),
        'hero_cut':dict(location=(12.15,-42,1.43),target=(-1,1,3.8),lens=40,aspect=1.78),
        'above':dict(location=(-275,-430,365),target=(0,0,0),lens=35,aspect=1.5,overlay=True,sky_strength=.13,sky_saturation=.75),
        'alignment':dict(location=(-850,-1300,1000),target=(0,0,0),lens=40,aspect=1.5,overlay=True),
        'barrier':dict(location=(3.3,-53,1.23),target=(0,-49,.40),lens=50,aspect=1.5),
        'guardrail_end':dict(location=(10,-291,1.25),target=(16.6,-275,.35),lens=48,aspect=1.5),
        'sign_structure':dict(location=(6,-405,2.8),target=(6,-360,7.6),lens=40,aspect=1.5),
        'south_sign':dict(location=(-6,405,2.8),target=(-6,360,7.6),lens=40,aspect=1.5),
        'pier_girders':dict(location=(8,-15,1.65),target=(0,1.5,5.65),lens=36,aspect=1.5),
        'bearings':dict(location=(4,-11.8,5.6),target=(.5,-6.096,5.6),lens=36,aspect=1.5,sky_strength=.55,sky_saturation=.12,sun_direction=(-.5,2,-1),sun_energy=4.5,exposure=-.15),
        'gore':dict(location=(22,-251,1.65),target=(14.2,-221,.38),lens=45,aspect=1.5),
        'terminal_controls':dict(location=(112,-58,17),target=(79,0,7.5),lens=40,aspect=1.5),
        'rail_repair':dict(location=(29,-249,2.3),target=(22.5,-234,.3),lens=48,aspect=1.5),
        'terminal':dict(location=(55,-34,9.0),target=(78,0,9.5),lens=40,aspect=1.5)}
    return {
        'hero':dict(location=(5.2,-75,2.90),target=(9,65,3.55),lens=40,aspect=1.78),
        'hero_old':dict(location=(15.,-75,2.45),target=(4,65,3.35),lens=40,aspect=1.78),
        'above':dict(location=(-230,-335,280),target=(25,0,1),lens=35,aspect=1.5,overlay=True,sky_strength=.13,sky_saturation=.75),
        'alignment':dict(location=(-650,-780,630),target=(35,0,1),lens=40,aspect=1.5,overlay=True),
        'sound_wall':dict(location=(24,-5,2.2),target=(31,9,2.4),lens=45,aspect=1.5),
        'cable_median':dict(location=(3,-26,2.2),target=(0,-17,1.52),lens=45,aspect=1.5)}

def overlay(path,cam,width,height):
    from PIL import Image,ImageDraw,ImageFont
    from kit.fonts import find_font
    im=Image.open(path);d=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),max(12,width//72))
    for ob in bpy.context.scene.objects:
        if ob.get('socket_kind')!='drive_path':continue
        pts=json.loads(ob['points_blender_json']);pixels=[]
        for p in pts:
            v=world_to_camera_view(bpy.context.scene,cam,Vector(p));pixels.append((v.x*width,(1-v.y)*height))
        color=(251,133,45) if 'Ramp' in ob.name else (30,204,240)
        d.line(pixels,fill=color,width=max(1,width//500))
        for j in range(15,len(pixels)-2,45):
            a=Vector(pixels[j-2]);b=Vector(pixels[j]);u=(b-a).normalized();n=Vector((-u.y,u.x));scale=max(4,width/200)
            d.polygon([tuple(b),tuple(b-u*scale+n*scale*.4),tuple(b-u*scale-n*scale*.4)],fill=color)
    d.rectangle((10,10,width-10,43),fill=(22,28,26));d.text((20,16),'CYAN: lane paths   /   ORANGE: ramp paths   /   exported driving sockets',font=font,fill=(230,236,225))
    im.save(path)

def render(source,out,width,samples,engine,names=None,custom=None,seed=101,source_fields=False):
    source=Path(source);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    context_sources=[]
    if source.stem.startswith('Freeway-'):
        sid=source.stem.split('-')[-1]
        for category in ('Town','Traffic'):
            path=source.parent/(category+'-'+sid+'.gltf')
            bpy.ops.import_scene.gltf(filepath=str(path.resolve()));context_sources.append(dict(source=str(path),bundle_sha256=bundle(path)))
    field_changes=[]
    if source_fields:
        from source_compare import install
        field_changes=install()
    from foliage_adapter import install as install_foliage
    foliage=install_foliage()
    cam=setup(samples,engine);sc=bpy.context.scene;views=custom or shots(seed);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    if 'above' in views:
        # Preserve the accepted annotated camera, and show the same place
        # unobstructed so traffic, paving age and parcels can be judged.
        views=dict(views);views['above_clean']=dict(views['above'],overlay=False)
    result={}
    for name,v in views.items():
        if names and name not in names:continue
        if v.get('stage_floor'):
            bpy.ops.mesh.primitive_plane_add(size=v['stage_floor']['size'],location=v['stage_floor']['location'])
            floor=bpy.context.object;ma=bpy.data.materials.new('Temporary inspection stage');ma.diffuse_color=(.14,.15,.14,1);floor.data.materials.append(ma)
        cam.location=v['location'];cam.rotation_euler=(Vector(v['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=v.get('lens',40)
        if v.get('roll'):cam.rotation_euler.rotate_axis('Z',v['roll'])
        sc.render.resolution_x=width;sc.render.resolution_y=round(width/v.get('aspect',1.5));sc.render.resolution_percentage=100
        sc.view_settings.exposure=v.get('exposure',-.45)
        sun=bpy.data.objects['Raking sun'];sun.rotation_euler=Vector(v.get('sun_direction',(-.72,.65,-.28))).to_track_quat('-Z','Y').to_euler();sun.data.energy=v.get('sun_energy',7.)
        direction=v.get('sun_direction',(-.72,.65,-.28));sun.data.angle=math.radians(v.get('sun_angle_degrees',.53))
        fill=bpy.data.objects['Photographic environment bounce'];bounce=v.get('diffuse_bounce')
        fill.data.energy=bounce['energy'] if bounce else 0
        if bounce:
            fill.location=bounce['location'];fill.rotation_euler=(Vector(bounce['target'])-fill.location).to_track_quat('-Z','Y').to_euler()
            fill.data.size=bounce['size'];fill.data.color=bounce.get('color',(1,1,1))
        sky=next(n for n in sc.world.node_tree.nodes if n.type=='TEX_SKY')
        sky.sun_rotation=math.atan2(-direction[1],-direction[0]);sky.sun_elevation=math.atan2(-direction[2],math.hypot(direction[0],direction[1]))
        sc.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=v.get('sky_strength',.08)
        next(n for n in sc.world.node_tree.nodes if n.type=='HUE_SAT').inputs['Saturation'].default_value=v.get('sky_saturation',1.0)
        bpy.context.view_layer.update();path=out/(name+'.png');sc.render.filepath=str(path.resolve());bpy.ops.render.render(write_still=True)
        if v.get('overlay'):overlay(path,cam,width,sc.render.resolution_y)
        result[name]=dict(frame_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),recipe_sha256=render_recipe(),lighting=dict(sun_direction=list(direction),sun_energy=sun.data.energy,sky_strength=sc.world.node_tree.nodes.get('Background').inputs['Strength'].default_value,sun_angle_degrees=v.get('sun_angle_degrees',.53)),foliage_profiles=foliage,material_stage='4096 source-field inspection' if source_fields else 'exported shipped PBR',source_field_changes=field_changes,source_field_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path('textures/source').glob('*.png'))} if source_fields else {},context=context_sources,source=str(source),bundle_sha256=bundle(source),engine=engine,samples=samples,width=width,camera=v)
        path.with_suffix('.json').write_text(json.dumps(result[name],indent=2))
    return result

def inspection(source,out,width,samples,engine):
    if Path(source).stem=='FreewayModules':
        return render(source,out,width,samples,engine,custom={'modules':dict(location=(-245,-350,345),target=(95,115,0),lens=42,aspect=1.5)})
    return render(source,out,width,samples,engine)

def scale(out,width,samples,engine):
    from kit.studio import human
    import geom as Q
    import importlib.util
    spec=importlib.util.spec_from_file_location('freeway_site',HERE/'site.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
    bpy.ops.wm.read_factory_settings(use_empty=True);source=Path('export/modules/GuardrailEnd.gltf');bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    c=s.load('build/context/HeroHatch.glb');c.location=(-3.6,.6,0)
    figures=human()
    for ob in figures:ob.location+=Vector((1.8,-1.2,0))
    bpy.context.view_layer.update()
    points=[ob.matrix_world@v.co for ob in figures if ob.type=='MESH' for v in ob.data.vertices]
    measured_height=max(v.z for v in points)-min(v.z for v in points)
    ma=Q.constant('Scale stage',(.16,.17,.16),.9);Q.M['Stage']=ma
    b=Q.Batch('Scale floor');b.face([(-200,-200,-.005),(200,-200,-.005),(200,200,-.005),(-200,200,-.005)],'Stage');b.finish()
    cam=setup(samples,engine);sc=bpy.context.scene;cam.location=(10,-13,5.8);cam.rotation_euler=(Vector((-1,0,.7))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=45
    sc.render.resolution_x=width;sc.render.resolution_y=round(width/1.5);out=Path(out);out.mkdir(parents=True,exist_ok=True);sc.render.filepath=str((out/'scale.png').resolve());bpy.ops.render.render(write_still=True)
    (out/'scale.json').write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),measured_human_height_m=measured_height,car_glb='build/context/HeroHatch.glb',car_glb_sha256=hashlib.sha256(Path('build/context/HeroHatch.glb').read_bytes()).hexdigest(),frame_sha256=hashlib.sha256((out/'scale.png').read_bytes()).hexdigest(),recipe_sha256=render_recipe(),car='Original full-resolution Alder H120, unchanged geometry',engine=engine),indent=2))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',default='export/Freeway-101.gltf');ap.add_argument('--out',default='renders/checkpoint/101');ap.add_argument('--width',type=int,default=1200);ap.add_argument('--samples',type=int,default=32);ap.add_argument('--engine',default='CYCLES');ap.add_argument('--shots',nargs='+');ap.add_argument('--seeds',nargs='+',type=int,default=[101,202]);ap.add_argument('--scale',action='store_true');ap.add_argument('--camera-file');ap.add_argument('--source-fields',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.scale:scale(a.out,a.width,a.samples,a.engine);return
    if a.camera_file:
        data=json.loads(Path(a.camera_file).read_text())
        for name,row in data.items():
            if a.shots and name not in a.shots:continue
            render(row.get('source',a.source),a.out,a.width,a.samples,a.engine,custom={name:row['shot']},source_fields=a.source_fields)
        return
    if Path(a.source).stem=='FreewayModules':inspection(a.source,a.out,a.width,a.samples,a.engine);return
    for seed in a.seeds:
        render('export/Freeway-'+str(seed)+'.gltf',Path(a.out)/str(seed),a.width,a.samples,a.engine,a.shots,seed=seed)
if __name__=='__main__':main()
