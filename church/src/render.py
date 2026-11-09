"""Checkpoint presentation imports the exported glTF, never a source blend."""
import argparse,hashlib,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import bpy
from mathutils import Vector
from kit.gpu import enable


def camera(loc,target,lens=42,aspect=1.5,ortho=None):
    data=bpy.data.cameras.new('Review camera');ob=bpy.data.objects.new('Review camera',data);bpy.context.collection.objects.link(ob)
    ob.location=loc;ob.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler();data.lens=lens;data.clip_end=3000
    if ortho:data.type='ORTHO';data.ortho_scale=ortho
    bpy.context.scene.camera=ob;return ob


def light(dusk=False):
    scene=bpy.context.scene;world=bpy.data.worlds.new('Procedural clear sky');world.use_nodes=True;scene.world=world
    ns=world.node_tree.nodes;ls=world.node_tree.links;sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=.37;sky.sun_rotation=4.1;sky.sun_disc=False
    bg=ns.get('Background');ls.new(sky.outputs['Color'],bg.inputs['Color']);bg.inputs['Strength'].default_value=.06 if not dusk else .025
    data=bpy.data.lights.new('Low raking morning sun','SUN');data.energy=3.5 if not dusk else .08;data.angle=math.radians(.65)
    ob=bpy.data.objects.new(data.name,data);bpy.context.collection.objects.link(ob);ob.rotation_euler=Vector((.55,.85,-.45)).to_track_quat('-Z','Y').to_euler()
    if dusk:
        for ma in bpy.data.materials:
            if 'stained' in ma.name:
                bs=ma.node_tree.nodes.get('Principled BSDF');bs.inputs['Emission Strength'].default_value=4.5
    scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.35 if not dusk else .4


def shots(seed):
    modern=seed==202
    return dict(hero=dict(location=(38,-67,1.72) if modern else (36,-60,1.72),target=(0,0,8.6),lens=42),
        above=dict(location=(73,-85,70) if modern else (61,-69,56),target=(11,0,0) if modern else (0,8,0),lens=45),
        doors=dict(location=(4,-23,1.72),target=(0,-14 if modern else -12.8,1.75),lens=48),
        window=dict(location=(13,-1,4.0),target=(6.65,-2.13,4.8),lens=48),
        window_dusk=dict(location=(13,-1,4.0),target=(6.65,-2.13,4.8),lens=48,dusk=True),
        tower=dict(location=(-17,-22,1.72),target=(-8.35,-11,17.0),lens=40),
        wing=dict(location=(49,-17,5.5) if modern else (31,37,3.5),target=(22,9,2.3) if modern else (10,10,2.4),lens=42),
        sign=dict(location=(21,-33,1.72),target=(17,-22,1.9),lens=48),
        scale=dict(location=(12,-26,2.1),target=(0,-13,2.0),lens=40))


def human(point):
    from kit.studio import human as silhouette
    # The stock studio helper returns a collection of real-scale objects.
    before=set(bpy.context.scene.objects);silhouette()
    obs=set(bpy.context.scene.objects)-before
    for ob in obs:
        if ob.parent not in obs:ob.location+=Vector(point)


def render_file(source,out,name,spec,width,samples,engine):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    light(spec.get('dusk',False));scene=bpy.context.scene;scene.render.engine=engine
    if engine=='CYCLES':enable();scene.cycles.samples=samples;scene.cycles.use_denoising=True;scene.cycles.max_bounces=8;scene.cycles.transparent_max_bounces=12
    camera(spec['location'],spec['target'],spec.get('lens',42),ortho=spec.get('ortho'))
    if name=='scale':human((2,-15,0))
    scene.render.resolution_x=width;scene.render.resolution_y=round(width/spec.get('aspect',1.5));scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';out.mkdir(parents=True,exist_ok=True);scene.render.filepath=str((out/(name+'.png')).resolve())
    bpy.ops.render.render(write_still=True)
    (out/(name+'.json')).write_text(json.dumps(dict(source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),engine=engine,**spec),indent=2))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source');ap.add_argument('--out',type=Path,default=Path('renders/checkpoint'));ap.add_argument('--width',type=int,default=1200);ap.add_argument('--samples',type=int,default=32);ap.add_argument('--seeds',default='101,202');ap.add_argument('--shots',default='hero,above,doors,window,window_dusk,tower,wing,sign,scale');ap.add_argument('--engine',default='CYCLES');ap.add_argument('--building-only',action='store_true');ap.add_argument('--range',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.range:
        render_file(Path('export/Range.gltf'),a.out,'range',dict(location=(55,-105,50),target=(5,0,5),lens=42),a.width,a.samples,a.engine);return
    for seed in map(int,a.seeds.split(',')):
        source=Path(f'export/Church-{seed}.gltf' if a.building_only else f'export/ChurchSite-{seed}.gltf')
        for name in a.shots.split(','):
            render_file(source,a.out/str(seed),name,shots(seed)[name],a.width,a.samples,a.engine)


if __name__=='__main__':main()
