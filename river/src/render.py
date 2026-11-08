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
from package import bundle
from views import views
from plan import Plan


def setup(width,samples):
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable()
    sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=8
    sc.cycles.transmission_bounces=6;sc.cycles.volume_bounces=2;sc.render.resolution_x=width;sc.render.resolution_y=round(width*2/3);sc.render.resolution_percentage=100
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.4
    sc.world=bpy.data.worlds.new('Procedural clear late-afternoon sky');sc.world.use_nodes=True
    nodes=sc.world.node_tree.nodes;links=sc.world.node_tree.links
    sky=nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(18);sky.sun_rotation=math.radians(224);sky.sun_disc=False
    sky.altitude=100;sky.air_density=.8
    # Neutral diffuse sky fill preserves gray concrete in shade. A separate
    # camera-ray strength retains the clear sky's deeper photographic value.
    sat=nodes.new('ShaderNodeHueSaturation');sat.inputs['Saturation'].default_value=.55
    grade=nodes.new('ShaderNodeMixRGB');grade.blend_type='MULTIPLY';grade.inputs[0].default_value=1;grade.inputs[2].default_value=(1.18,1.04,.80,1)
    links.new(sky.outputs[0],sat.inputs['Color']);links.new(sat.outputs[0],grade.inputs[1])
    bg=nodes.get('Background');links.new(grade.outputs[0],bg.inputs[0]);bg.inputs[1].default_value=.30
    visible=nodes.new('ShaderNodeBackground');links.new(sky.outputs[0],visible.inputs[0]);visible.inputs[1].default_value=.035
    lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader')
    ray=nodes.new('ShaderNodeMath');ray.operation='MAXIMUM'
    links.new(lp.outputs['Is Camera Ray'],ray.inputs[0]);links.new(lp.outputs['Is Glossy Ray'],ray.inputs[1])
    links.new(ray.outputs[0],mix.inputs[0]);links.new(bg.outputs[0],mix.inputs[1]);links.new(visible.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes.get('World Output').inputs[0])
    light=bpy.data.lights.new('Low raking sun','SUN');light.energy=3.7;light.color=(1,.88,.73);light.angle=math.radians(.65)
    sun=bpy.data.objects.new(light.name,light);sc.collection.objects.link(sun)
    direction=Vector((-.69,-.66,.31));sun.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler()
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


def shot(sc,cam,definition,path,source,width,samples):
    sc.view_settings.exposure=definition.get('exposure',-.4)
    cam.location=definition['location'];cam.rotation_euler=(Vector(definition['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
    if definition.get('roll'):cam.rotation_euler.rotate_axis('Z',definition['roll'])
    cam.data.lens=definition['lens'];sc.render.resolution_x=width;sc.render.resolution_y=round(width/definition.get('aspect',1.5))
    sc.render.filepath=str(path.resolve());sc.render.image_settings.file_format='PNG';path.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.render.render(write_still=True)
    path.with_suffix('.json').write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),
        stage='fresh external glTF import / quick PBR form checkpoint',camera=definition,
        engine='CYCLES',samples=samples,width=width,water='imported normal, interpolated _FLOW response and uniform absorption extras',
        sun_elevation_degrees=18,exposure=sc.view_settings.exposure),indent=2)+'\n')


def render(seed,out,width,samples,names):
    bpy.ops.wm.read_factory_settings(use_empty=True);source=Path('export')/f'RiverCrossing-{seed}.gltf'
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()));restore_water();restore_native_leaves();sc,cam=setup(width,samples)
    exported=next(o['plan'] for o in bpy.context.scene.objects if o.name==f'Crossing_{seed}')
    plan=Plan(**dict(exported));definitions=views(seed,plan)
    for name in names:shot(sc,cam,definitions[name],out/str(seed)/(name+'.png'),source,width,samples)


def baseline(seed,width,samples):
    import importlib.util
    folder=Path('build/accepted-rebuild/river')
    spec=importlib.util.spec_from_file_location('_river_accepted_renderer',folder/'src/render.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    bpy.ops.wm.read_factory_settings(use_empty=True);source=folder/'export'/f'RiverCrossing-{seed}.gltf'
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()));restore_water();sc,cam=old.setup(width,samples)
    definitions=views(seed);source_hash=bundle(source)
    for name in definitions:
        path=Path('renders/fixes/before')/str(seed)/(name+'.png')
        if path.exists() and path.with_suffix('.json').exists():
            cached=json.loads(path.with_suffix('.json').read_text())
            if (cached.get('accepted_revision')=='9b1c8bc' and cached['source']==str(source)
                and cached['bundle_sha256']==source_hash and cached['camera']==json.loads(json.dumps(definitions[name]))
                and cached['width']==width and cached['samples']==samples):continue
        original=Path('build/round2-before/renders/checkpoint')/str(seed)/(name+'.png')
        if original.exists():
            meta=json.loads(original.with_suffix('.json').read_text())
            if meta['camera']==json.loads(json.dumps(definitions[name])) and meta['width']==width and meta['samples']==samples:
                import shutil
                path.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,path)
                meta.update(accepted_revision='9b1c8bc',comparison='original handoff frame, identical revised camera')
                path.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n');continue
        old.shot(sc,cam,definitions[name],path,source,width,samples)
        meta=json.loads(path.with_suffix('.json').read_text());meta.update(accepted_revision='9b1c8bc',comparison='accepted exported asset and light, regenerated with revised camera')
        path.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source');ap.add_argument('--out',type=Path,default=Path('renders/checkpoint'));ap.add_argument('--seeds',nargs='+',type=int,default=[101,202]);ap.add_argument('--width',type=int,default=1280);ap.add_argument('--samples',type=int,default=32);ap.add_argument('--shots',nargs='+',default=list(views(101)));ap.add_argument('--matches',action='store_true');ap.add_argument('--modules',action='store_true');ap.add_argument('--comparison-cameras',action='store_true');ap.add_argument('--with-baseline',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    if not a.comparison_cameras:
        for seed in a.seeds:render(seed,a.out,a.width,a.samples,a.shots)
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
            bpy.ops.wm.read_factory_settings(use_empty=True);source=Path('export')/f'RiverCrossing-{row["seed"]}.gltf'
            bpy.ops.import_scene.gltf(filepath=str(source.resolve()));restore_water();restore_native_leaves();sc,cam=setup(a.width,a.samples)
            # Match view direction/shape; daylight differs by photographic view.
            # The FHWA concrete underside is exposed for its deep shade.
            definition=row['shot'];definition['aspect']=(row['crop'][2]-row['crop'][0])/(row['crop'][3]-row['crop'][1])
            shot(sc,cam,definition,Path('renders/checkpoint-matches')/(name+'.png'),source,a.width,a.samples)
    if a.comparison_cameras:
        for seed in a.seeds:
            bpy.ops.wm.read_factory_settings(use_empty=True);source=Path('export')/f'RiverCrossing-{seed}.gltf'
            bpy.ops.import_scene.gltf(filepath=str(source.resolve()));restore_water();sc,cam=setup(a.width,a.samples)
            for name in a.shots:
                receipt=Path('build/round2-before/renders/checkpoint')/str(seed)/(name+'.json')
                definition=json.loads(receipt.read_text())['camera']
                shot(sc,cam,definition,Path('renders/fixes/after')/str(seed)/(name+'.png'),source,a.width,a.samples)
    if a.with_baseline:
        for seed in a.seeds:baseline(seed,a.width,a.samples)


if __name__=='__main__':main()
