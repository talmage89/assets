"""Source checkpoint outdoors; every image records source hash and lighting."""
import argparse,sys,math,json,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import gpu
from kit.studio import human,studio_mat
from settings import SHOTS,HYDRANGEA_SHOTS


def setup(engine,samples):
    sc=bpy.context.scene;sc.render.engine=engine
    if engine=='CYCLES':
        gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.transparent_max_bounces=64;sc.cycles.max_bounces=12
    else:
        sc.eevee.taa_render_samples=samples;sc.eevee.use_raytracing=True
        sc.eevee.fast_gi_method='AMBIENT_OCCLUSION_ONLY';sc.eevee.fast_gi_distance=1.5
        sc.eevee.fast_gi_thickness_near=.012;sc.eevee.fast_gi_bias=.005
        sc.eevee.fast_gi_quality=1;sc.eevee.fast_gi_ray_count=8;sc.eevee.fast_gi_step_count=16
        sc.eevee.ray_tracing_options.screen_trace_thickness=.015
        sc.eevee.ray_tracing_options.screen_trace_quality=1
    world=bpy.data.worlds.new('Procedural summer daylight');world.use_nodes=True;sc.world=world;n=world.node_tree.nodes;n.clear();l=world.node_tree.links
    sky=n.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(48);sky.sun_rotation=math.radians(225);sky.sun_disc=False;sky.altitude=.1;sky.aerosol_density=.5
    hue=n.new('ShaderNodeHueSaturation');hue.inputs['Saturation'].default_value=.22;l.new(sky.outputs[0],hue.inputs['Color'])
    bg=n.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.45;out=n.new('ShaderNodeOutputWorld');l.new(hue.outputs[0],bg.inputs[0]);l.new(bg.outputs[0],out.inputs[0])
    v=Vector((-.473,-.473,.743));ld=bpy.data.lights.new('Summer sun','SUN');sun=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(sun);ld.energy=3.5;ld.color=(1,.94,.85);ld.angle=math.radians(1);sun.rotation_euler=(-v).to_track_quat('-Z','Y').to_euler()
    bpy.ops.mesh.primitive_plane_add(size=2000,location=(0,0,-.001));floor=bpy.context.object;floor.name='Review grade';floor.data.materials.append(studio_mat('Outdoor neutral ground',(.083,.087,.063),.96))
    cam=bpy.data.objects.new('Checkpoint camera',bpy.data.cameras.new('Checkpoint camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL'
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.1
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
    return cam,floor,sun,bg


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--species',choices=['boxwood','hydrangea'],default='boxwood');p.add_argument('--out',type=Path,required=True);p.add_argument('--stage');p.add_argument('--config');p.add_argument('--fit-reference');p.add_argument('--shots');p.add_argument('--camera-file',type=Path);p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=40);p.add_argument('--engine',default='CYCLES');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    final=a.source.suffix.lower()=='.glb'
    if a.stage=='final' and not final:raise ValueError('Final images require GLB')
    if final:
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(a.source.resolve()))
        selected=a.species.title()
        for ob in list(bpy.context.scene.objects):
            if ob.name.startswith('Hydrangea' if selected=='Boxwood' else 'Boxwood'):bpy.data.objects.remove(ob,do_unlink=True)
        leaves=bpy.data.objects['Hydrangea leaf and flower cards' if a.species=='hydrangea' else 'Boxwood leaf cards']
        images={}
        for node in leaves.data.materials[0].node_tree.nodes:
            if node.type=='TEX_IMAGE' and node.image:
                for channel in ('BaseColor','Normal','ORM'):
                    if channel in node.image.name:images[channel]=node.image
        assert len(images)==3
        from materials import foliage_material
        leaves.data.materials[0]=foliage_material(images)
    else:bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
    cam,floor,sun,bg=setup(a.engine,a.samples);sc=bpy.context.scene
    shots={k:v['shot'] for k,v in json.loads(a.camera_file.read_text()).items()} if a.camera_file else (HYDRANGEA_SHOTS if a.species=='hydrangea' else SHOTS)
    names=a.shots.split(',') if a.shots else (list(shots) if a.camera_file else ['three_quarter','side','close_1m','scale','base','shaded_side','structure']);a.out.mkdir(parents=True,exist_ok=True);path=a.out/'shots.json';meta=json.loads(path.read_text()) if path.exists() else {}
    digest=hashlib.sha256(a.source.read_bytes()).hexdigest()
    for name in names:
        s=shots[name];cam.location=s['location'];cam.rotation_euler=(Vector(s['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',s.get('roll',0));cam.data.lens=s.get('lens',55)
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/s.get('aspect',1.25));sc.render.resolution_percentage=100
        bpy.data.objects['Hydrangea leaf and flower cards' if a.species=='hydrangea' else 'Boxwood leaf cards'].hide_render=s.get('hide_leaves',False)
        sc.render.film_transparent=s.get('background')=='transparent';floor.hide_render=sc.render.film_transparent
        hs=human() if s.get('human') else []
        for ob in hs:ob.location.x+=.18;ob.location.y+=.1
        sc.render.filepath=str((a.out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        for ob in hs:bpy.data.objects.remove(ob,do_unlink=True)
        meta[name]=dict(stage='EXPORTED GLB / baked maps / documented thin-leaf response' if final else 'SOURCE LOOKDEV / analytic tiles',source_sha256=digest,engine=a.engine,samples=a.samples,shot=s,camera_target_distance_m=(Vector(s['target'])-cam.location).length,lighting=dict(sky='procedural',sun_elevation_deg=48,sun_energy=3.5,sky_strength=.45,sky_saturation=.22,exposure=.1))
        if a.species=='hydrangea':
            graph=json.loads((ROOT/'shrubs/build/hydrangea/growth.json').read_text());windows=[]
            for head in graph['heads']:
                c=Vector(head['center_m']);r=head['radius_m']*.72
                corners=[world_to_camera_view(sc,cam,c+Vector((x,y,z))*r) for x in (-1,1) for y in (-1,1) for z in (-1,1)]
                windows.append([min(p.x for p in corners),1-max(p.y for p in corners),max(p.x for p in corners),1-min(p.y for p in corners)])
            meta[name]['head_windows_normalized']=windows
        path.write_text(json.dumps(meta,indent=2))

if __name__=='__main__':main()
