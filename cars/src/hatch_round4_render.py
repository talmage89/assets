"""H120-only gloss environment and whole-game-skin curvature diagnostics."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import gpu
from hatch_render import SHOTS,stripes
import hatch_curvature_map


def gloss(scene):
    """Neutral clearcoated clay over an original sky/ground environment."""
    world=bpy.data.worlds.new('H120 procedural sky');world.use_nodes=True;scene.world=world
    n=world.node_tree.nodes;l=world.node_tree.links;n.clear()
    sky=n.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(32)
    sky.sun_rotation=math.radians(125);sky.sun_disc=False;sky.altitude=.2;sky.air_density=1.0
    # Desaturate the procedural daylight for neutral form inspection.
    hue=n.new('ShaderNodeHueSaturation');hue.inputs['Saturation'].default_value=.15;l.new(sky.outputs[0],hue.inputs['Color'])
    bg=n.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.35;l.new(hue.outputs[0],bg.inputs[0])
    out=n.new('ShaderNodeOutputWorld');l.new(bg.outputs[0],out.inputs[0])
    for mat in bpy.data.materials:
        if not mat.use_nodes:continue
        bs=mat.node_tree.nodes.get('Principled BSDF')
        if not bs:continue
        if mat.name=='Clay body':
            bs.inputs['Base Color'].default_value=(.18,.18,.18,1)
            bs.inputs['Metallic'].default_value=0
            bs.inputs['Roughness'].default_value=.22
            bs.inputs['Coat Weight'].default_value=1
            bs.inputs['Coat Roughness'].default_value=.075
            bs.inputs['Coat IOR'].default_value=1.5
        elif mat.name=='Clay rubber':
            bs.inputs['Base Color'].default_value=(.012,.012,.012,1);bs.inputs['Roughness'].default_value=.48
        elif mat.name=='Clay glass':
            bs.inputs['Base Color'].default_value=(.018,.021,.023,1);bs.inputs['Roughness'].default_value=.17
    ground=bpy.data.materials.new('H120 dark ground');ground.use_nodes=True
    bs=ground.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.045,.045,.045,1);bs.inputs['Roughness'].default_value=.82
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.006));ob=bpy.context.object;ob.name='H120 procedural ground';ob.data.materials.append(ground)
    # Present the same cutout framing as existing pairs; the ground still
    # receives light and supplies the lower hemisphere in paint reflections.
    ob.visible_camera=False;ob['studio']=True


def camera(scene,shot,width):
    data=bpy.data.cameras.new('H120 diagnostic camera');ob=bpy.data.objects.new('H120 diagnostic camera',data)
    scene.collection.objects.link(ob);scene.camera=ob
    ob.location=shot['location'];ob.rotation_euler=(Vector(shot['target'])-ob.location).to_track_quat('-Z','Y').to_euler();ob.rotation_euler.rotate_axis('Z',shot.get('roll',0))
    data.type='ORTHO' if 'ortho' in shot else 'PERSP';data.sensor_width=36;data.sensor_fit='HORIZONTAL'
    data.lens=shot.get('lens',58);data.ortho_scale=shot.get('ortho',5.1);data.clip_start=.02;data.clip_end=500
    scene.render.resolution_x=width;scene.render.resolution_y=round(width/shot.get('aspect',1.65));scene.render.resolution_percentage=100


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    p.add_argument('--mode',choices=['curvature','gloss','map-stripes'],required=True)
    p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=40)
    p.add_argument('--cameras',default='cars/build/hatch/cameras.json');p.add_argument('--shots',default='')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    if a.mode=='gloss':
        shots={n:SHOTS[n] for n in ['side','front_three_quarter','rear_three_quarter','rear']}
        shots.update({n:r['shot'] for n,r in json.loads(Path(a.cameras).read_text()).items()})
    else:shots={n:SHOTS[n] for n in ['front_three_quarter','rear_three_quarter','side','front','rear']}
    if a.shots:shots={n:s for n,s in shots.items() if n in a.shots.split(',')}
    bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene
    if a.mode=='curvature':
        report=hatch_curvature_map.apply();report['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
        (out/'mean-curvature.json').write_text(json.dumps(report,indent=2));scene.render.engine='BLENDER_WORKBENCH'
        sh=scene.display.shading;sh.light='FLAT';sh.color_type='VERTEX';sh.show_shadows=False;sh.show_cavity=False;sh.show_specular_highlight=False;sh.show_object_outline=False
        scene.display.render_aa='32'
        scene.world=bpy.data.worlds.new('Curvature backdrop');scene.world.color=(.05,.05,.05)
        scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0
    else:
        if a.mode=='gloss':gloss(scene)
        else:stripes(scene,'horizontal')
        scene.render.engine='CYCLES';gpu.enable();scene.cycles.samples=a.samples;scene.cycles.use_denoising=True;scene.cycles.max_bounces=5
        scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-1.3 if a.mode=='gloss' else -.2
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    meta_path=out/'round4-shots.json';metadata=json.loads(meta_path.read_text()) if meta_path.exists() else {}
    for name,shot in shots.items():
        key=a.mode.replace('-','_')+'_'+name
        camera(scene,shot,a.width);scene.render.filepath=str((out/(key+'.png')).resolve())
        bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
        metadata[key]=dict(shot,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),mode=a.mode,width=a.width,height=scene.render.resolution_y)
        meta_path.write_text(json.dumps(metadata,indent=2));print('HATCH_R4_RENDERED',key,flush=True)

if __name__=='__main__':main()
