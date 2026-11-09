"""Checkpoint presentation imports the exported glTF, never a source blend."""
import argparse,hashlib,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import bpy
from mathutils import Vector
from kit.gpu import enable


def digest(source):
    h=hashlib.sha256(source.read_bytes())
    if source.suffix=='.gltf':
        d=json.loads(source.read_text())
        for key in ('buffers','images'):
            for row in d.get(key,[]):h.update((source.parent/row['uri']).read_bytes())
    return h.hexdigest()


def camera(loc,target,lens=42,aspect=1.5,ortho=None):
    data=bpy.data.cameras.new('Review camera');ob=bpy.data.objects.new('Review camera',data);bpy.context.collection.objects.link(ob)
    ob.location=loc;ob.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler();data.lens=lens;data.clip_end=3000;data.sensor_fit='HORIZONTAL';data.sensor_width=36
    if ortho:data.type='ORTHO';data.ortho_scale=ortho
    bpy.context.scene.camera=ob;return ob


def light(dusk=False,sun_direction=None):
    scene=bpy.context.scene;world=bpy.data.worlds.new('Procedural clear sky');world.use_nodes=True;scene.world=world
    ns=world.node_tree.nodes;ls=world.node_tree.links;sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=.37;sky.sun_rotation=4.1;sky.sun_disc=False
    bg=ns.get('Background');ls.new(sky.outputs['Color'],bg.inputs['Color']);bg.inputs['Strength'].default_value=.06 if not dusk else .025
    data=bpy.data.lights.new('Low raking morning sun','SUN');data.energy=4.5 if not dusk else .08;data.angle=math.radians(.65);data.color=(1,.90,.78)
    ob=bpy.data.objects.new(data.name,data);bpy.context.collection.objects.link(ob);ob.rotation_euler=Vector(sun_direction or (.55,.85,-.45)).to_track_quat('-Z','Y').to_euler()
    if dusk:
        for ma in bpy.data.materials:
            if 'stained' in ma.name:
                bs=ma.node_tree.nodes.get('Principled BSDF');bs.inputs['Emission Strength'].default_value=4.5
    scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.15 if not dusk else .4


def shots(seed):
    modern=seed==202
    return dict(hero=dict(location=(40,-56,1.72) if modern else (34,-40,1.72),target=(9,0,6.9) if modern else (0,0,11.8),lens=38 if modern else 35),
        above=dict(location=(100,-112,92) if modern else (61,-69,56),target=(21,1,0) if modern else (0,8,0),lens=42 if modern else 45),
        doors=dict(location=(4,-23,1.72),target=(0,-14 if modern else -12.8,1.75),lens=48),
        window=dict(location=(4,-23,5.0) if modern else (13,-1,4.0),target=(1,-14.95,6.4) if modern else (6.65,-2.13,4.8),lens=48),
        window_dusk=dict(location=(4,-23,5.0) if modern else (13,-1,4.0),target=(1,-14.95,6.4) if modern else (6.65,-2.13,4.8),lens=48,dusk=True),
        tower=dict(location=(-10,-22,1.72) if modern else (-11,-21.5,1.72),target=(-13.84,-12.94,10.8) if modern else (-8.35,-11,16.0),lens=40),
        wing=dict(location=(54,-34,4.8) if modern else (29,35,7),target=(28,4,2.2) if modern else (9,17,2.4),lens=42 if modern else 38,sun_direction=(.55,.85,-.45) if modern else (-.55,-.85,-.45)),
        sign=dict(location=(11,-47.5,1.72) if modern else (19,-26.5,1.72),target=(7,-37.5,1.9) if modern else (17,-22,1.9),lens=48 if modern else 35),
        scale=dict(location=(14,-35,2.1),target=(0,-13,3.0),lens=45,scale_ground_z=.1524 if modern else 0))


def human(point):
    from kit.studio import human as silhouette
    # The stock studio helper returns a collection of real-scale objects.
    before=set(bpy.context.scene.objects);silhouette()
    obs=set(bpy.context.scene.objects)-before
    for ob in obs:
        if ob.parent not in obs:ob.location+=Vector(point)


def render_file(source,out,name,spec,width,samples,engine):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if source.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
    else:bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    if source.suffix=='.blend' and spec.get('source_module'):
        part=next(o for o in bpy.context.scene.objects if o.get('module_kind')==spec['source_module'])
        shown=set(part.children_recursive);part.parent=None;part.location=(0,0,0);part.rotation_euler=(0,0,0)
        for ob in bpy.context.scene.objects:
            if ob.type=='MESH' and ob not in shown:ob.hide_render=True
    light(spec.get('dusk',False),spec.get('sun_direction'));scene=bpy.context.scene;scene.render.engine=engine
    if spec.get('module_studio'):
        ns=scene.world.node_tree.nodes;ls=scene.world.node_tree.links;bg=ns.get('Background')
        for link in list(bg.inputs['Color'].links):ls.remove(link)
        bg.inputs['Color'].default_value=(.22,.22,.22,1);bg.inputs['Strength'].default_value=.7
    if engine=='CYCLES':enable();scene.cycles.samples=samples;scene.cycles.use_denoising=True;scene.cycles.max_bounces=8;scene.cycles.transparent_max_bounces=12
    else:
        scene.eevee.use_raytracing=True;scene.eevee.ray_tracing_options.resolution_scale='1';scene.eevee.taa_render_samples=samples
        for ma in bpy.data.materials:
            bs=ma.node_tree.nodes.get('Principled BSDF') if ma.use_nodes else None
            if bs and bs.inputs['Transmission Weight'].default_value>0:
                ma.use_raytrace_refraction=True;ma.thickness_mode='SLAB'
                value=ma.node_tree.nodes.new('ShaderNodeValue');value.outputs[0].default_value=.006
                output=next(n for n in ma.node_tree.nodes if n.type=='OUTPUT_MATERIAL');ma.node_tree.links.new(value.outputs[0],output.inputs['Thickness'])
    cam=camera(spec['location'],spec['target'],spec.get('lens',42),ortho=spec.get('ortho'));cam.rotation_euler.rotate_axis('Z',spec.get('roll',0))
    if name=='scale':
        height=spec.get('scale_ground_z',0);human((4.03,-18.4,height))
        before=set(bpy.context.scene.objects)
        bpy.ops.import_scene.gltf(filepath=str((HERE.parents[1]/'cars/export/AlderH120.glb').resolve()))
        obs=set(bpy.context.scene.objects)-before
        for ob in obs:
            if ob.parent not in obs:ob.location+=Vector((-3,-18.5,height))
    scene.render.resolution_x=width;scene.render.resolution_y=round(width/spec.get('aspect',1.5));scene.render.resolution_percentage=100
    if 'landmarks_world_m' in spec:
        from bpy_extras.object_utils import world_to_camera_view
        bpy.context.view_layer.update();px=[]
        sw,sh=spec['photo_size'];factor=max(1,round(width/sw))
        scene.render.resolution_x=sw*factor;scene.render.resolution_y=sh*factor
        for p in spec['landmarks_world_m']:
            v=world_to_camera_view(scene,cam,Vector(p));px.append((v.x*sw,(1-v.y)*sh))
        error=max(math.dist(a,b) for a,b in zip(px,spec['expected_pixels']))
        assert error<.05,('Renderer camera differs from calibration',error)
        spec['independent_projection_error_source_px']=error
    scene.render.image_settings.file_format='PNG';out.mkdir(parents=True,exist_ok=True);scene.render.filepath=str((out/(name+'.png')).resolve())
    bpy.ops.render.render(write_still=True)
    (out/(name+'.json')).write_text(json.dumps(dict(source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),package_sha256=digest(source),render_recipe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),resolution=[scene.render.resolution_x,scene.render.resolution_y],engine=engine,**spec),indent=2))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source');ap.add_argument('--out',type=Path,default=Path('renders/checkpoint'));ap.add_argument('--width',type=int,default=1200);ap.add_argument('--samples',type=int,default=32);ap.add_argument('--seeds',default='101,202');ap.add_argument('--shots',default='hero,above,doors,window,window_dusk,tower,wing,sign,scale');ap.add_argument('--engine',default='CYCLES');ap.add_argument('--building-only',action='store_true');ap.add_argument('--range',action='store_true');ap.add_argument('--modules',action='store_true');ap.add_argument('--matches',action='store_true');ap.add_argument('--source-scene',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.modules:
        for source in sorted(Path('export/modules').glob('*.gltf')):
            meta=json.loads(source.with_suffix('.json').read_text());lo,hi=map(Vector,(meta['bounds_min'],meta['bounds_max']));center=(lo+hi)/2;span=max(hi-lo)
            if source.stem=='BentShoe':
                # Inspect one of the paired shoes at its actual scale.
                bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
                pts=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices if (o.matrix_world@v.co).x<center.x]
                lo=Vector(tuple(min(p[k] for p in pts) for k in range(3)));hi=Vector(tuple(max(p[k] for p in pts) for k in range(3)));center=(lo+hi)/2;span=max(hi-lo)
            spec=dict(location=list(center+Vector((span*.85,span*1.9*(1 if source.stem=='RearSteps' else -1),span*.70))),target=list(center),lens=48,ortho=span*1.48,module_studio=True)
            render_file(source,a.out,source.stem,spec,a.width,a.samples,a.engine)
        return
    if a.matches:
        for name,data in json.loads(Path('build/matched-cameras.json').read_text()).items():
            source=Path(f'build/site-{data["seed"]}.blend') if a.source_scene else Path(data['source'])
            spec=dict(data['shot']);spec.update(landmarks_world_m=data['landmarks_world_m'],expected_pixels=data['projected_pixels'],photo_size=[data['crop'][2]-data['crop'][0],data['crop'][3]-data['crop'][1]])
            render_file(source,a.out,name,spec,a.width,a.samples,a.engine)
        return
    if a.range:
        render_file(Path('export/Range.gltf'),a.out,'range',dict(location=(60,-170,90),target=(16,0,6),lens=42,ortho=166,module_studio=True),a.width,a.samples,a.engine);return
    for seed in map(int,a.seeds.split(',')):
        source=Path(f'export/Church-{seed}.gltf' if a.building_only else f'export/ChurchSite-{seed}.gltf')
        for name in a.shots.split(','):
            render_file(source,a.out/str(seed),name,shots(seed)[name],a.width,a.samples,a.engine)


if __name__=='__main__':main()
