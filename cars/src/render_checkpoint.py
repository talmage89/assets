"""Workbench form views and Eevee procedural striped reflection diagnostics.

All views load the game-density checkpoint. No photographed pixel is loaded by
Blender. Photo pairs are composed outside Blender by kit/photo_match.py.
"""
import argparse,json,math,runpy,sys,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import studio,gpu
from kit import model as G
import pickup_spec as S


def stripe_world(sc):
    world=bpy.data.worlds.new('Procedural stripe dome');world.use_nodes=True;sc.world=world
    n=world.node_tree.nodes;l=world.node_tree.links;n.clear()
    tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Normal'],sep.inputs[0])
    angle=n.new('ShaderNodeMath');angle.operation='ARCTAN2';l.new(sep.outputs['X'],angle.inputs[0]);l.new(sep.outputs['Z'],angle.inputs[1])
    mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=16;l.new(angle.outputs[0],mul.inputs[0])
    sine=n.new('ShaderNodeMath');sine.operation='SINE';l.new(mul.outputs[0],sine.inputs[0])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='CONSTANT'
    ramp.color_ramp.elements[0].position=.47;ramp.color_ramp.elements[0].color=(.008,.008,.008,1)
    ramp.color_ramp.elements[1].position=.50;ramp.color_ramp.elements[1].color=(1,1,1,1)
    l.new(sine.outputs[0],ramp.inputs[0]);bg=n.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.8
    l.new(ramp.outputs[0],bg.inputs[0]);out=n.new('ShaderNodeOutputWorld');l.new(bg.outputs[0],out.inputs[0])
    for mat in bpy.data.materials:
        if mat.name=='Clay body':
            bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.24,.26,.28,1)
            bs.inputs['Metallic'].default_value=.85;bs.inputs['Roughness'].default_value=.12


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--width',type=int,default=1400)
    p.add_argument('--mode',choices=['clay','match','stripes'],default='clay');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    source=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(source))
    sc=bpy.context.scene;camera=studio.add_studio(scale=3,backdrop_color=(.22,.23,.24))
    config=runpy.run_path(str(Path(__file__).with_name('config.py')))
    shots=config['SHOTS']
    if a.mode=='match':
        data=json.loads(Path('build/matched-cameras.json').read_text());shots={k:v['shot'] for k,v in data.items()}
    else:shots={k:v for k,v in shots.items() if k.startswith('stripes')==(a.mode=='stripes')}
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    if a.mode=='stripes':
        sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=24;sc.cycles.use_denoising=True
        sc.cycles.max_bounces=4
        stripe_world(sc)
        for ob in sc.objects:
            if ob.get('studio') and ob.type in ['MESH','LIGHT']:ob.hide_render=True
    else:
        sc.render.engine='BLENDER_WORKBENCH';sh=sc.display.shading
        sh.light='STUDIO';sh.studiolight_rotate_z=.35;sh.color_type='MATERIAL';sh.show_shadows=True
        sh.show_cavity=True;sh.cavity_type='BOTH';sh.curvature_ridge_factor=1.1;sh.curvature_valley_factor=1.0
        sh.show_specular_highlight=True;sh.background_type='VIEWPORT';sh.background_color=(.23,.24,.25);sh.show_object_outline=False
        sc.display.render_aa='32'
        for ob in sc.objects:
            if ob.name.startswith('Studio black reflection flag'):ob.hide_render=True
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.5 if a.mode!='stripes' else -.2
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.resolution_percentage=100
    metadata=json.loads((out/'shots.json').read_text()) if (out/'shots.json').exists() else {}
    for name,shot in shots.items():
        camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler()
        camera.rotation_euler.rotate_axis('Z',shot.get('roll',0));camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP'
        camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36;camera.data.lens=shot.get('lens',57);camera.data.ortho_scale=shot.get('ortho',7)
        camera.data.clip_start=.02;camera.data.clip_end=100
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.6))
        sc.render.film_transparent=name not in ['front_three_quarter','rear_three_quarter']
        bpy.data.objects['Studio seamless'].hide_render=sc.render.film_transparent
        bpy.context.view_layer.update();sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        def project(p):
            q=world_to_camera_view(sc,camera,Vector(p));return (q.x*sc.render.resolution_x,(1-q.y)*sc.render.resolution_y)
        points=dict(front_ground=(0,-S.LENGTH/2,0),rear_ground=(0,S.LENGTH/2,0),
                    front_axle=(0,S.FRONT_AXLE,0),rear_axle=(0,S.REAR_AXLE,0),
                    roof=(0,0,S.HEIGHT),origin=(0,0,0),left=(-S.WIDTH/2,0,0),right=(S.WIDTH/2,0,0),
                    bed_front=(0,S.BED_FRONT,S.BED_TOP),bed_rear=(0,S.BED_REAR,S.BED_TOP),
                    track_left=(-S.TRACK/2,0,0),track_right=(S.TRACK/2,0,0))
        metadata[name]=dict(shot,source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),stage='body form checkpoint',
                            engine=sc.render.engine,width=sc.render.resolution_x,height=sc.render.resolution_y,points={k:project(p) for k,p in points.items()})
        (out/'shots.json').write_text(json.dumps(metadata,indent=2))
        print('RENDERED',name,flush=True)


if __name__=='__main__':main()
