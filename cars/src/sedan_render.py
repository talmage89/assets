"""Form-only source views. No final-delivery claim, no photographic shaders."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import studio,gpu
import sedan_spec as S

SHOTS={
 'front_three_quarter':dict(location=(7,-9,2.9),target=(0,-.1,.72),lens=58,aspect=1.65),
 'rear_three_quarter':dict(location=(-7,9,2.9),target=(0,.15,.73),lens=58,aspect=1.65),
 'side':dict(location=(10,0,.74),target=(0,0,.74),ortho=5.7,aspect=2),
 'front':dict(location=(0,-10,.76),target=(0,0,.76),ortho=2.55,aspect=1.25),
 'rear':dict(location=(0,10,.76),target=(0,0,.76),ortho=2.55,aspect=1.25),
 'side_raking':dict(location=(10,-.25,1.20),target=(0,0,.75),ortho=5.7,aspect=2,raking=True),
 'top':dict(location=(0,0,10),target=(0,0,0),ortho=5.7,aspect=1.8,roll=math.pi/2),
 'stripes_horizontal':dict(location=(7,-8,2.7),target=(0,0,.76),lens=58,aspect=1.65,direction='horizontal'),
 'stripes_rear_horizontal':dict(location=(-7,8,2.7),target=(0,.15,.76),lens=58,aspect=1.65,direction='horizontal'),
 'stripes_rear_vertical':dict(location=(-7,8,2.7),target=(0,.15,.76),lens=58,aspect=1.65,direction='vertical'),
 'stripes_vertical':dict(location=(7,-8,2.7),target=(0,0,.76),lens=58,aspect=1.65,direction='vertical'),
 'stripes_side_horizontal':dict(location=(10,0,1.0),target=(0,0,.74),ortho=5.7,aspect=2,direction='horizontal'),
 'stripes_side_vertical':dict(location=(10,0,1.0),target=(0,0,.74),ortho=5.7,aspect=2,direction='vertical'),
 'stripes_hood_driver':dict(location=(.34,-.60,1.24),target=(.06,-1.70,.85),lens=38,aspect=1.6,direction='vertical',only=['Hood outer']),
}


def stripes(sc,direction):
    world=bpy.data.worlds.new('Original procedural reflection bands');world.use_nodes=True;sc.world=world
    n=world.node_tree.nodes;l=world.node_tree.links;n.clear()
    tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Normal'],sep.inputs[0])
    angle=n.new('ShaderNodeMath')
    if direction=='horizontal':
        # Latitude bands have no azimuthal pole in either end-on view. Using
        # atan2(Z,X) here made radial fans even on a fair front/rear surface.
        angle.operation='ARCSINE';l.new(sep.outputs['Z'],angle.inputs[0])
    else:
        angle.operation='ARCTAN2';l.new(sep.outputs['X'],angle.inputs[0]);l.new(sep.outputs['Y'],angle.inputs[1])
    mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=36 if direction=='horizontal' else 24;l.new(angle.outputs[0],mul.inputs[0])
    sine=n.new('ShaderNodeMath');sine.operation='SINE';l.new(mul.outputs[0],sine.inputs[0])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='LINEAR'
    ramp.color_ramp.elements[0].position=.42;ramp.color_ramp.elements[0].color=(.015,.015,.015,1)
    ramp.color_ramp.elements[1].position=.55;ramp.color_ramp.elements[1].color=(1,1,1,1)
    l.new(sine.outputs[0],ramp.inputs[0]);bg=n.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.8
    l.new(ramp.outputs[0],bg.inputs[0]);out=n.new('ShaderNodeOutputWorld');l.new(bg.outputs[0],out.inputs[0])
    for mat in bpy.data.materials:
        if mat.name=='Clay body':
            bs=mat.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(.28,.29,.30,1)
            bs.inputs['Metallic'].default_value=.75;bs.inputs['Roughness'].default_value=.065


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    p.add_argument('--width',type=int,default=1400);p.add_argument('--samples',type=int,default=32)
    p.add_argument('--workbench',action='store_true',help='Fast clay inspection; reflection diagnostics still use Cycles')
    p.add_argument('--mode',choices=['clay','stripes','pairs','comparisons'],default='clay');p.add_argument('--cameras',default='build/sedan/cameras.json');p.add_argument('--shots',default='')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    shots={n:s for n,s in SHOTS.items() if n.startswith('stripes')==(a.mode=='stripes')}
    if a.mode=='clay':
        profile=source.parent/'profile-camera.json'
        if profile.exists():
            for name,row in json.loads(profile.read_text()).items():shots[name]=row['shot']
    if a.mode in ['pairs','comparisons']:shots={n+('_clay' if a.mode=='comparisons' else ''):r['shot'] for n,r in json.loads(Path(a.cameras).read_text()).items()}
    if a.shots:shots={n:s for n,s in shots.items() if n in a.shots.split(',')}
    metadata={}
    if (out/'shots.json').exists():metadata=json.loads((out/'shots.json').read_text())
    for name,shot in shots.items():
        bpy.ops.wm.open_mainfile(filepath=str(source));sc=bpy.context.scene
        camera=studio.add_studio(scale=2.5,backdrop_color=(.2,.21,.22))
        stripe=a.mode in ['stripes','pairs']
        if stripe:
            stripes(sc,shot.get('direction','horizontal'));sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=4
            for ob in sc.objects:
                if ob.get('studio') and ob.type in ['MESH','LIGHT']:ob.hide_render=True
        elif not a.workbench and (shot.get('raking') or name in ['front_three_quarter','rear_three_quarter']):
            sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=5
            for mat in bpy.data.materials:
                bs=mat.node_tree.nodes.get('Principled BSDF') if mat.use_nodes else None
                if bs:
                    value={'Clay body':.24,'Clay rubber':.009,'Clay glass':.018,'Clay bumper':.035}.get(mat.name)
                    if value is not None:bs.inputs['Base Color'].default_value=(value,value,value,1)
                    bs.inputs['Roughness'].default_value=.31 if mat.name=='Clay body' else .36
                    if mat.name=='Clay glass':bs.inputs['Specular IOR Level'].default_value=.06
            if shot.get('raking'):
                for ob in sc.objects:
                    if ob.type=='LIGHT':ob.hide_render=True
                sun=bpy.data.lights.new('Low sun along stamped side','SUN');sun.energy=5.0;sun.angle=.035
                ob=bpy.data.objects.new('Low sun along stamped side',sun);sc.collection.objects.link(ob)
                direction=Vector((-.25,1,-.18));ob.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
                sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
                sc.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.15,.15,.15,1)
        else:
            sc.render.engine='BLENDER_WORKBENCH';sh=sc.display.shading
            sh.light='STUDIO';sh.studio_light='studio.sl';sh.studiolight_rotate_z=0;sh.color_type='MATERIAL';sh.show_shadows=True
            sh.show_cavity=True;sh.cavity_type='BOTH';sh.curvature_ridge_factor=1.0;sh.curvature_valley_factor=1.0
            sh.show_specular_highlight=True;sh.background_type='VIEWPORT';sh.background_color=(.22,.23,.24);sh.show_object_outline=False
            sc.display.render_aa='32'
            for ob in sc.objects:
                if ob.name.startswith('Studio black reflection flag'):ob.hide_render=True
        for hidden in shot.get('hide',[]):bpy.data.objects[hidden].hide_render=True
        if shot.get('only'):
            for ob in sc.objects:
                if ob.type=='MESH' and ob.name not in shot['only']:ob.hide_render=True
        camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0))
        camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.sensor_width=36;camera.data.sensor_fit='HORIZONTAL'
        camera.data.lens=shot.get('lens',58);camera.data.ortho_scale=shot.get('ortho',5.7);camera.data.clip_start=.02;camera.data.clip_end=100
        sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.25 if shot.get('raking') else -.2 if stripe else -.85 if sc.render.engine=='CYCLES' else .25
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.65));sc.render.resolution_percentage=100
        sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=True
        bpy.data.objects['Studio seamless'].hide_render=True
        sc.render.filepath=str((out/(name+'.png')).resolve());bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
        landmarks=dict(front=(0,-S.LENGTH/2,0),rear=(0,S.LENGTH/2,0),front_axle=(S.FRONT_TRACK/2,S.FRONT_AXLE,S.HUB_HEIGHT),rear_axle=(S.REAR_TRACK/2,S.REAR_AXLE,S.HUB_HEIGHT),left=(-S.WIDTH/2,0,0),right=(S.WIDTH/2,0,0),ground=(0,0,0),roof=(0,.35,S.HEIGHT))
        if name.startswith('side_matched'):
            landmarks.update(front_axle=(.895,S.FRONT_AXLE,S.HUB_HEIGHT),rear_axle=(.900,S.REAR_AXLE,S.HUB_HEIGHT))
        measured=source.parent/'form-check.json'
        if measured.exists():
            data=json.loads(measured.read_text())
            if data['source_sha256']!=hashlib.sha256(source.read_bytes()).hexdigest():raise ValueError('Form measurements predate source')
            landmarks.update(front=(0,data['bounds_m']['min'][1],0),rear=(0,data['bounds_m']['max'][1],0),
                left=(data['bounds_m']['min'][0],0,0),right=(data['bounds_m']['max'][0],0,0),
                hood_front=data['hood_leading_center_m'],roof_peak=data['roof_peak_m'],deck=data['deck_trailing_peak_m'])
        pixels={}
        for key,point in landmarks.items():
            q=world_to_camera_view(sc,camera,Vector(point));pixels[key]=[q.x*a.width,(1-q.y)*sc.render.resolution_y]
        metadata[name]=dict(shot,source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),stage='sedan source form checkpoint',engine=sc.render.engine,width=a.width,height=sc.render.resolution_y,points=pixels)
        (out/'shots.json').write_text(json.dumps(metadata,indent=2));print('SEDAN_RENDERED',name,flush=True)
if __name__=='__main__':main()
