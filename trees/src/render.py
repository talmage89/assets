"""Outdoor Cycles/Eevee presentation with procedural daylight and baked GLB maps."""
import argparse,sys,math,json,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import gpu
from kit.studio import human,studio_mat
from views import SHOTS
from leaf_material import material as leaf_material


def setup(engine,samples):
    sc=bpy.context.scene;sc.render.engine=engine
    if engine=='CYCLES':
        gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True
        sc.cycles.transparent_max_bounces=64;sc.cycles.max_bounces=12
    world=bpy.data.worlds.new('Scripted daylight sky');world.use_nodes=True;sc.world=world
    ns=world.node_tree.nodes;ns.clear();sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING'
    sky.sun_elevation=math.radians(38);sky.sun_rotation=math.radians(225);sky.sun_disc=False
    sky.altitude=.1;sky.air_density=1;sky.aerosol_density=.35
    bg=ns.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.40
    out=ns.new('ShaderNodeOutputWorld');world.node_tree.links.new(sky.outputs[0],bg.inputs[0]);world.node_tree.links.new(bg.outputs[0],out.inputs[0])
    v=Vector((math.cos(math.radians(225))*math.cos(math.radians(38)),math.sin(math.radians(225))*math.cos(math.radians(38)),math.sin(math.radians(38))))
    ld=bpy.data.lights.new('Procedural sun','SUN');sun=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(sun)
    ld.energy=7;ld.angle=math.radians(.65);sun.rotation_euler=(-v).to_track_quat('-Z','Y').to_euler()
    bpy.ops.mesh.primitive_plane_add(size=2000,location=(0,0,-.001));floor=bpy.context.object;floor.name='Review ground only'
    floor.data.materials.append(studio_mat('Neutral outdoor grade',(.12,.13,.10),.95))
    cam=bpy.data.objects.new('Review camera',bpy.data.cameras.new('Review camera'));sc.collection.objects.link(cam);sc.camera=cam
    cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL';cam.data.clip_end=3000
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.5
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
    return cam,floor


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=40);p.add_argument('--engine',default='CYCLES')
    p.add_argument('--shots');p.add_argument('--camera-file',type=Path)
    p.add_argument('--stage');p.add_argument('--config');p.add_argument('--fit-reference')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source_sha=hashlib.sha256(a.source.read_bytes()).hexdigest()
    final=a.source.suffix.lower()=='.glb'
    if a.stage=='final' and not final:raise ValueError('Final presentation requires the exported GLB')
    if a.fit_reference:raise ValueError('No external fit asset is authorized for trees')
    if final:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(a.source.resolve()))
        # Implement the documented thin-leaf engine response using ONLY the
        # imported embedded maps. No procedural look-dev material is loaded.
        leaf=bpy.data.objects['Summer leaf cards'];images={}
        for node in leaf.data.materials[0].node_tree.nodes:
            if node.type=='TEX_IMAGE' and node.image:
                for channel in ('BaseColor','Normal','ORM'):
                    if channel in node.image.name:images[channel]=node.image
        if set(images)!=set(('BaseColor','Normal','ORM')):raise RuntimeError('Missing embedded leaf PBR maps')
        leaf.data.materials[0]=leaf_material(images['BaseColor'],images['Normal'],images['ORM'])
    else:bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
    cam,floor=setup(a.engine,a.samples);sc=bpy.context.scene
    shots={k:v['shot'] for k,v in json.loads(a.camera_file.read_text()).items()} if a.camera_file else SHOTS
    names=a.shots.split(',') if a.shots else list(shots)
    a.out.mkdir(parents=True,exist_ok=True);meta_path=a.out/'shots.json';meta=json.loads(meta_path.read_text()) if meta_path.exists() else {}
    foliage=bpy.data.objects['Summer leaf cards'];leaf_mat=foliage.data.materials[0]
    links=leaf_mat.node_tree.links;coverage=leaf_mat.node_tree.nodes['Branchlet coverage']
    leaf_surface=coverage.inputs[2].links[0].from_socket
    black=leaf_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse');black.inputs['Color'].default_value=(0,0,0,1)
    for name in names:
        shot=shots[name];cam.location=shot['location'];cam.rotation_euler=(Vector(shot['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.rotation_euler.rotate_axis('Z',shot.get('roll',0));cam.data.lens=shot.get('lens',47)
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1));sc.render.resolution_percentage=100
        foliage.hide_render=shot.get('hide_leaves',False);floor.hide_render=shot.get('silhouette',False) or shot.get('background')=='transparent'
        sc.render.film_transparent=shot.get('background')=='transparent'
        hs=human() if shot.get('human') else []
        for ob in hs:ob.location.x-=1.15;ob.location.y-=.4
        if shot.get('silhouette'):
            links.new(black.outputs[0],coverage.inputs[2])
            bark=next(n for n in bpy.data.objects['Trunk and branches'].data.materials[0].node_tree.nodes if n.type=='BSDF_PRINCIPLED')
            old=tuple(bark.inputs['Base Color'].default_value);old_link=bark.inputs['Base Color'].links[0].from_socket if bark.inputs['Base Color'].links else None
            for link in list(bark.inputs['Base Color'].links):bark.id_data.links.remove(link)
            bark.inputs['Base Color'].default_value=(0,0,0,1)
            old_spec=bark.inputs['Specular IOR Level'].default_value
            bark.inputs['Specular IOR Level'].default_value=0
        sc.render.filepath=str((a.out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        if shot.get('silhouette'):
            links.new(leaf_surface,coverage.inputs[2])
            bark.inputs['Base Color'].default_value=old
            if old_link:bark.id_data.links.new(old_link,bark.inputs['Base Color'])
            bark.inputs['Specular IOR Level'].default_value=old_spec
        for ob in hs:bpy.data.objects.remove(ob,do_unlink=True)
        meta[name]=dict(stage='EXPORTED GLB / baked maps / documented thin-leaf response' if final else 'SOURCE / procedural bark and analytic branchlets',source=a.source.name,
                        source_sha256=source_sha,engine=a.engine,samples=a.samples,shot=shot,
                        lighting=dict(sky='procedural multiple scattering',sun_elevation=38,sun_azimuth=225,sun_energy=7,sky_strength=.40,exposure=.5))
        meta_path.write_text(json.dumps(meta,indent=2))

if __name__=='__main__':main()
