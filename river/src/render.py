"""Serial Cycles batch: freshly import external glTF, never the source scene."""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import bpy
from mathutils import Vector
from kit import gpu
from package import bundle,presentation_recipe,camera_signature,sha
from views import views
from plan import Plan
RECIPE=presentation_recipe()


def current_shot(path,source,definition,width,samples,engine='CYCLES',fields=None):
    if not path.exists() or not path.with_suffix('.json').exists():return False
    try:meta=json.loads(path.with_suffix('.json').read_text())
    except (OSError,ValueError):return False
    return (meta.get('recipe_sha256')==RECIPE and meta.get('bundle_sha256')==bundle(source)
            and meta.get('camera')==json.loads(json.dumps(definition)) and meta.get('width')==width
            and meta.get('samples')==samples and meta.get('engine')==engine and meta.get('image_sha256')==sha(path)
            and meta.get('source_fields_sha256',{})==(fields or {}))


def setup(width,samples):
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable()
    sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=8
    sc.cycles.transmission_bounces=6;sc.cycles.volume_bounces=2;sc.render.resolution_x=width;sc.render.resolution_y=round(width*2/3);sc.render.resolution_percentage=100
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.15
    sc.world=bpy.data.worlds.new('Procedural clear late-afternoon sky');sc.world.use_nodes=True
    nodes=sc.world.node_tree.nodes;links=sc.world.node_tree.links
    sky=nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(16);sky.sun_rotation=math.radians(-62);sky.sun_disc=False
    sky.altitude=100;sky.air_density=.8
    # Neutral diffuse sky fill preserves gray concrete in shade. A separate
    # camera-ray strength retains the clear sky's deeper photographic value.
    sat=nodes.new('ShaderNodeHueSaturation');sat.inputs['Saturation'].default_value=.55
    grade=nodes.new('ShaderNodeMixRGB');grade.blend_type='MULTIPLY';grade.inputs[0].default_value=1;grade.inputs[2].default_value=(1.18,1.04,.80,1)
    links.new(sky.outputs[0],sat.inputs['Color']);links.new(sat.outputs[0],grade.inputs[1])
    bg=nodes.get('Background');links.new(grade.outputs[0],bg.inputs[0]);bg.inputs[1].default_value=.35
    visible=nodes.new('ShaderNodeBackground');links.new(sky.outputs[0],visible.inputs[0]);visible.inputs[1].default_value=.045
    reflection=nodes.new('ShaderNodeBackground');links.new(sky.outputs[0],reflection.inputs[0]);reflection.inputs[1].default_value=.10
    lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader')
    environment=nodes.new('ShaderNodeMixShader')
    links.new(lp.outputs['Is Glossy Ray'],environment.inputs[0]);links.new(bg.outputs[0],environment.inputs[1]);links.new(reflection.outputs[0],environment.inputs[2])
    ray=nodes.new('ShaderNodeMath');ray.operation='MAXIMUM'
    links.new(lp.outputs['Is Camera Ray'],ray.inputs[0])
    links.new(ray.outputs[0],mix.inputs[0]);links.new(environment.outputs[0],mix.inputs[1]);links.new(visible.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes.get('World Output').inputs[0])
    light=bpy.data.lights.new('Low raking sun','SUN');light.energy=5.5;light.color=(1,.94,.84);light.angle=math.radians(.53)
    sun=bpy.data.objects.new(light.name,light);sc.collection.objects.link(sun)
    direction=Vector((.45,-.849,.276));sun.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler()
    cam=bpy.data.objects.new('Review camera',bpy.data.cameras.new('Review camera'));sc.collection.objects.link(cam);sc.camera=cam
    cam.data.clip_end=2500;cam.data.clip_start=.04;cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL'
    return sc,cam


def restore_water():
    # glTF cannot carry a node volume closure. Its documented material extras
    # contain the original absorption/scattering coefficients and flow ranges.
    from materials import volume_from_extras
    for ob in bpy.context.scene.objects:
        if ob.type=='MESH' and ob.name=='WaterSurface':
            assert ob.data.attributes.get('_FLOW') is not None,'Imported water lost its flow field'
    for ma in bpy.data.materials:
        if not ma.use_nodes or 'River_water' not in ma.name:continue
        out=ma.node_tree.nodes.get('Material Output')
        if not out:out=next(n for n in ma.node_tree.nodes if n.type=='OUTPUT_MATERIAL')
        if out.inputs['Volume'].is_linked:continue
        volume_from_extras(ma)
        # Direct-light shadow rays cross the interface without the refractive
        # caustic solve, while the actual medium still attenuates/scatters them.
        # Camera and reflection rays keep the exported IOR and normal map.
        # Cycles' MNEE mode ignores volumes and is unsuitable for this medium.
        nodes=ma.node_tree.nodes;links=ma.node_tree.links
        surface=out.inputs['Surface'].links[0].from_socket
        transparent=nodes.new('ShaderNodeBsdfTransparent');lp=nodes.new('ShaderNodeLightPath')
        shadow=nodes.new('ShaderNodeMixShader');links.new(lp.outputs['Is Shadow Ray'],shadow.inputs[0])
        links.new(surface,shadow.inputs[1]);links.new(transparent.outputs[0],shadow.inputs[2])
        links.new(shadow.outputs[0],out.inputs['Surface'])
        if 'river_flow_speed_range' not in ma:continue
        nodes=ma.node_tree.nodes;links=ma.node_tree.links
        attr=nodes.new('ShaderNodeAttribute');attr.attribute_name=ma['river_flow_attribute']
        xy=nodes.new('ShaderNodeVectorMath');xy.operation='MULTIPLY';xy.inputs[1].default_value=(1,1,0)
        links.new(attr.outputs['Vector'],xy.inputs[0])
        speed=nodes.new('ShaderNodeVectorMath');speed.operation='LENGTH';links.new(xy.outputs[0],speed.inputs[0])
        normal=next(n for n in nodes if n.type=='NORMAL_MAP');bs=nodes.get('Principled BSDF')
        for socket,key in ((normal.inputs['Strength'],'river_flow_normal_range'),(bs.inputs['Roughness'],'river_flow_roughness_range')):
            value=nodes.new('ShaderNodeMapRange');value.clamp=True
            value.inputs['From Min'].default_value=ma['river_flow_speed_range'][0];value.inputs['From Max'].default_value=ma['river_flow_speed_range'][1]
            value.inputs['To Min'].default_value=ma[key][0];value.inputs['To Max'].default_value=ma[key][1]
            links.new(speed.outputs['Value'],value.inputs['Value']);links.new(value.outputs[0],socket)


def restore_native_leaves():
    # Reuse freeway's existing adapter to the native tree family's thin-leaf
    # response. It reads only the imported baked images, never source meshes.
    import importlib.util
    spec=importlib.util.spec_from_file_location('_river_native_leaf_response',REPO/'freeway/src/foliage_adapter.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.install()


def photographic_light(name):
    """Estimated sun direction from each photo's lit faces and cast shadows.

    These are visual light matches, not recovered capture metadata. Geometry,
    cameras, white-balance controls and shipped material inputs stay identical.
    """
    direction=Vector({'urban':(-.75,-.35,.56),'bank':(-.70,-.45,.55),
                      'under':(.45,-.70,.55)}[name]).normalized()
    sun=bpy.data.objects['Low raking sun'];sun.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler()
    sun.data.energy={'urban':5.5,'bank':4.6,'under':5.0}[name]
    bpy.context.scene['photo_light_estimate']=dict(direction=list(direction),
        elevation_degrees=math.degrees(math.asin(direction.z)),energy=sun.data.energy)


def restore_bank_source():
    """Original manufacture fields before normal baking and 1024 filtering."""
    folder=Path('build/bank-fields/source').resolve()
    for ma in bpy.data.materials:
        if not ma.use_nodes or 'RiverBank' not in ma.name:continue
        nodes=ma.node_tree.nodes;links=ma.node_tree.links
        for node in nodes:
            if node.type!='TEX_IMAGE' or not node.image:continue
            name=Path(node.image.filepath).name
            if name in ('T_RiverBank_BaseColor.png','T_RiverBank_ORM.png'):
                node.image=bpy.data.images.load(str(folder/name),check_existing=True)
                node.image.colorspace_settings.name='sRGB' if 'BaseColor' in name else 'Non-Color'
        normal=next(n for n in nodes if n.type=='NORMAL_MAP');bs=nodes.get('Principled BSDF')
        height=nodes.new('ShaderNodeTexImage');height.image=bpy.data.images.load(str(folder/'T_RiverBank_Height.png'),check_existing=True)
        height.image.colorspace_settings.name='Non-Color'
        bump=nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.006
        links.new(height.outputs['Color'],bump.inputs['Height']);links.new(bump.outputs['Normal'],bs.inputs['Normal'])
    bpy.context.scene['bank_source_fields']=True
    bpy.context.scene['bank_field_sha256']={p.name:sha(p) for p in folder.glob('*.png')}


def shot(sc,cam,definition,path,source,width,samples):
    fields=dict(sc.get('bank_field_sha256',{}))
    photo_light=dict(sc.get('photo_light_estimate',{}))
    if photo_light:photo_light['direction']=list(photo_light['direction'])
    if current_shot(path,source,definition,width,samples,sc.render.engine,fields):return
    sc.view_settings.exposure=definition.get('exposure',-.15)
    cam.location=definition['location'];cam.rotation_euler=(Vector(definition['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
    if definition.get('roll'):cam.rotation_euler.rotate_axis('Z',definition['roll'])
    cam.data.lens=definition['lens'];sc.render.resolution_x=width;sc.render.resolution_y=round(width/definition.get('aspect',1.5))
    sc.render.filepath=str(path.resolve());sc.render.image_settings.file_format='PNG';path.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.render.render(write_still=True)
    path.with_suffix('.json').write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),
        stage='bank manufacture source fields on imported export' if sc.get('bank_source_fields') else 'fresh external glTF import / shared shipped PBR images',recipe_sha256=RECIPE,image_sha256=sha(path),source_fields_sha256=fields,camera=definition,
        engine=sc.render.engine,samples=samples,width=width,water='imported normal, interpolated _FLOW response and uniform absorption extras',
        sun_elevation_degrees=16,sun_direction=[.45,-.849,.276],
        photographic_light_estimate=photo_light,exposure=sc.view_settings.exposure),indent=2)+'\n')


def render(seed,out,width,samples,names,eevee=False):
    bpy.ops.wm.read_factory_settings(use_empty=True);source=Path('export')/f'RiverCrossing-{seed}.gltf'
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()));restore_water();restore_native_leaves();sc,cam=setup(width,samples)
    exported=next(o['plan'] for o in bpy.context.scene.objects if o.name==f'Crossing_{seed}')
    plan=Plan(**dict(exported));definitions=views(seed,plan)
    for name in names:
        if name in definitions:shot(sc,cam,definitions[name],out/str(seed)/(name+'.png'),source,width,samples)
    if eevee:
        sc.render.engine='BLENDER_EEVEE'
        sc.eevee.use_raytracing=True
        shot(sc,cam,definitions['hero'],out/str(seed)/'eevee.png',source,width,samples)


def baseline(seed,width,samples,names=None):
    import importlib.util
    folder=Path('build/accepted-rebuild/river')
    spec=importlib.util.spec_from_file_location('_river_accepted_renderer',folder/'src/render.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    bpy.ops.wm.read_factory_settings(use_empty=True);source=folder/'export'/f'RiverCrossing-{seed}.gltf'
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()));old.restore_water();old.restore_native_leaves();sc,cam=old.setup(width,samples)
    definitions=views(seed);source_hash=bundle(source)
    from mathutils.bvhtree import BVHTree
    soil=bpy.data.objects['BedBanksFloodplain']
    tree=BVHTree.FromPolygons([soil.matrix_world@v.co for v in soil.data.vertices],
                              [list(f.vertices) for f in soil.data.polygons],all_triangles=True)
    clearances=[]
    for name in (names or definitions):
        if name not in definitions:continue
        eye=Vector(definitions[name]['location'])
        hit=tree.ray_cast(Vector((eye.x,eye.y,1000)),Vector((0,0,-1)),2000)[0]
        assert hit is None or eye.z>hit.z+.04,('Before camera inside accepted terrain',seed,name,eye,hit)
        clearances.append(dict(view=name,eye_z_m=eye.z,terrain_z_m=None if hit is None else hit.z,
                               clearance_m=None if hit is None else eye.z-hit.z))
        path=Path('renders/fixes/before')/str(seed)/(name+'.png')
        if path.exists() and path.with_suffix('.json').exists():
            cached=json.loads(path.with_suffix('.json').read_text())
            if (cached.get('accepted_revision')=='4f09582' and cached['source']==str(source)
                and cached['bundle_sha256']==source_hash and camera_signature(cached['camera'])==json.loads(json.dumps(camera_signature(definitions[name])))
                and cached['width']==width and cached['samples']==samples and cached.get('image_sha256')==sha(path)):continue
        original=Path('build/round3-before/renders/checkpoint')/str(seed)/(('hero' if name=='retained_hero' else name)+'.png')
        if not original.exists():
            original=REPO/'build/river-handoff/renders/checkpoint'/str(seed)/(('hero' if name=='retained_hero' else name)+'.png')
        if original.exists():
            meta=json.loads(original.with_suffix('.json').read_text())
            if camera_signature(meta['camera'])==json.loads(json.dumps(camera_signature(definitions[name]))) and meta['width']==width and meta['samples']==samples:
                import shutil
                path.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,path)
                meta.update(accepted_revision='4f09582',comparison='original handoff frame, identical revised camera',image_sha256=sha(path))
                path.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n');continue
        old.shot(sc,cam,definitions[name],path,source,width,samples)
        meta=json.loads(path.with_suffix('.json').read_text());meta.update(accepted_revision='4f09582',comparison='accepted exported asset and light, regenerated with revised camera',image_sha256=sha(path))
        path.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n')
    report=Path(f'build/baseline-clearance-{seed}.json');combined={}
    if report.exists():
        previous=json.loads(report.read_text())
        if previous['accepted_bundle_sha256']==source_hash:combined={r['view']:r for r in previous['views']}
    combined.update({r['view']:r for r in clearances})
    report.write_text(json.dumps(dict(passed=True,accepted_bundle_sha256=source_hash,
        views=[combined[k] for k in definitions if k in combined]),indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source');ap.add_argument('--out',type=Path,default=Path('renders/checkpoint'));ap.add_argument('--seeds',nargs='+',type=int,default=[101,202]);ap.add_argument('--width',type=int,default=1280);ap.add_argument('--samples',type=int,default=32);ap.add_argument('--shots',nargs='+',default=list(dict.fromkeys([*views(101),*views(202)])));ap.add_argument('--matches',action='store_true');ap.add_argument('--modules',action='store_true');ap.add_argument('--comparison-cameras',action='store_true');ap.add_argument('--with-baseline',action='store_true')
    ap.add_argument('--match-names',nargs='+',choices=('urban','bank','under'))
    ap.add_argument('--eevee',action='store_true')
    ap.add_argument('--auxiliary-only',action='store_true')
    ap.add_argument('--source-fields',action='store_true');ap.add_argument('--match-out',type=Path,default=Path('renders/checkpoint-matches'))
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    if not a.comparison_cameras and not a.auxiliary_only:
        for seed in a.seeds:render(seed,a.out,a.width,a.samples,a.shots,a.eevee)
    if a.modules:
        bpy.ops.wm.read_factory_settings(use_empty=True);source=Path('export/RiverModules.gltf')
        bpy.ops.import_scene.gltf(filepath=str(source.resolve()));sc,cam=setup(a.width,a.samples)
        floor_mat=bpy.data.materials.new('Module review floor');floor_mat.diffuse_color=(.09,.10,.085,1)
        floor_mat.use_nodes=True;floor_mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.09,.10,.085,1)
        bpy.ops.mesh.primitive_plane_add(size=120,location=(23,15,-1.82));bpy.context.object.data.materials.append(floor_mat)
        from kit.fonts import find_font
        labelmat=bpy.data.materials.new('Module review lettering');labelmat.diffuse_color=(.55,.56,.49,1)
        labelmat.use_nodes=True;labelmat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.55,.56,.49,1)
        for row in json.loads(Path('build/manifest.json').read_text())['modules']:
            ob=bpy.data.objects.get(row['name'])
            if ob is None:continue
            cu=bpy.data.curves.new('Review label '+row['name'],'FONT');cu.font=bpy.data.fonts.load(find_font('DejaVu Sans','Book'))
            cu.body=row['name']+'\n'+str(row['triangles'])+' tris';cu.size=.85;cu.align_x='CENTER'
            label=bpy.data.objects.new(cu.name,cu);bpy.context.collection.objects.link(label)
            label.location=(ob.location.x,ob.location.y-7,-1.80);cu.materials.append(labelmat)
        shot(sc,cam,dict(location=(39,-63,48),target=(23,15,.3),lens=43),a.out/'modules.png',source,a.width,a.samples)
    if a.matches:
        for name,row in json.loads(Path('build/photo-calibration.json').read_text()).items():
            if a.match_names and name not in a.match_names:continue
            bpy.ops.wm.read_factory_settings(use_empty=True);source=Path('export')/f'RiverCrossing-{row["seed"]}.gltf'
            bpy.ops.import_scene.gltf(filepath=str(source.resolve()));restore_water();restore_native_leaves();sc,cam=setup(a.width,a.samples)
            photographic_light(name)
            if a.source_fields:restore_bank_source()
            # Match view direction/shape; daylight differs by photographic view.
            # The FHWA concrete underside is exposed for its deep shade.
            definition=row['shot'];definition['aspect']=(row['crop'][2]-row['crop'][0])/(row['crop'][3]-row['crop'][1])
            shot(sc,cam,definition,a.match_out/(name+'.png'),source,a.width,a.samples)
    if a.comparison_cameras:
        for seed in a.seeds:
            bpy.ops.wm.read_factory_settings(use_empty=True);source=Path('export')/f'RiverCrossing-{seed}.gltf'
            bpy.ops.import_scene.gltf(filepath=str(source.resolve()));restore_water();sc,cam=setup(a.width,a.samples)
            for name in a.shots:
                receipt=Path('build/round2-before/renders/checkpoint')/str(seed)/(name+'.json')
                definition=json.loads(receipt.read_text())['camera']
                shot(sc,cam,definition,Path('renders/fixes/after')/str(seed)/(name+'.png'),source,a.width,a.samples)
    if a.with_baseline:
        for seed in a.seeds:baseline(seed,a.width,a.samples,a.shots)


if __name__=='__main__':main()
