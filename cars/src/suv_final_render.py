"""X220 gallery and matched-light inspection of source or exported GLB.

Final mode accepts only a GLB. Gallery construction is exactly the pickup's
render_final.py recipe: same scale, cove, broadening, energies and AgX look.
Only framing, poses and photographic exposure belong to this SUV module.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import studio,gpu
from suv_final_views import VIEWS
from suv_finishes import COLORS,PAINT_METAL
from suv_mechanics import update_supports


def gallery():
    camera=studio.add_studio(scale=3,backdrop_color=(.20,.21,.22))
    for name in ['Right rim strip','Left rim strip']:bpy.data.objects[name].data.size*=4.5
    bpy.data.objects['Key softbox'].data.size*=1.6
    bpy.data.objects['Key softbox'].data.size_y*=1.2
    bpy.data.objects['Overhead reflection card'].data.size*=1.5
    bpy.context.view_layer.update()
    return camera


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    p.add_argument('--stage',choices=['source','final'],default='final');p.add_argument('--shots',default='hero,rear,front,side,back,top,face,wheel,cargo,scale,lamps_lit')
    p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=64)
    p.add_argument('--paint',default='Atlantic');p.add_argument('--camera-file');p.add_argument('--colors',action='store_true')
    p.add_argument('--engine',choices=['CYCLES','BLENDER_EEVEE'],default='CYCLES');p.add_argument('--gate-frames',type=int,default=0)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();final=source.suffix.lower()=='.glb'
    if a.stage=='final' and not final:raise ValueError('Finals require the exported GLB')
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    recipe_files=[Path(__file__),Path(__file__).with_name('suv_final_views.py'),Path(__file__).with_name('suv_lighting.py'),Path(__file__).with_name('suv_delivery_materials.py'),Path(__file__).with_name('delivery_materials.py'),ROOT/'kit/studio.py']
    recipe=hashlib.sha256(b''.join(f.read_bytes() for f in recipe_files)).hexdigest()
    shots={n:dict(VIEWS[n]) for n in a.shots.split(',')}
    if a.colors:shots={c+'_'+v:dict(VIEWS[v],paint=c) for c in COLORS for v in ['hero','rear']}
    if a.camera_file:shots={n:r['shot'] for n,r in json.loads(Path(a.camera_file).read_text()).items()}
    if a.gate_frames:
        shots={f'gate_{i:03}':dict(VIEWS['rear'],parts={'Liftgate':75*math.sin(math.pi*i/(a.gate_frames-1))**2}) for i in range(a.gate_frames)}
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    meta=json.loads((out/'shots.json').read_text()) if (out/'shots.json').exists() else {}
    for name,shot in shots.items():
        if hashlib.sha256(source.read_bytes()).hexdigest()!=digest:raise ValueError('Source changed during rendering')
        if hashlib.sha256(b''.join(f.read_bytes() for f in recipe_files)).hexdigest()!=recipe:raise ValueError('Render recipe changed during rendering')
        if final:
            bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source))
            import suv_delivery_materials as D
            D.install()
        else:bpy.ops.wm.open_mainfile(filepath=str(source))
        sc=bpy.context.scene;camera=gallery();paint=shot.get('paint',a.paint)
        if final:D.apply(paint,shot.get('lights',False))
        else:
            for m in bpy.data.materials:
                if m.get('vehicle_paint'):
                    m.node_tree.nodes['Paint tint'].outputs[0].default_value=(*COLORS[paint],1)
                    m.node_tree.nodes['Paint metallic'].outputs[0].default_value=PAINT_METAL[paint]
                    m.node_tree.nodes['Paint flakes'].outputs[0].default_value=.55 if PAINT_METAL[paint]>0 else 0
                if m.get('lamp_lit_strength',0):m.node_tree.nodes['SURFACE'].inputs['Emission Strength'].default_value=m['lamp_lit_strength'] if shot.get('lights') else 0
        xf=Matrix.Rotation(math.radians(shot.get('studio_yaw',0)),4,'Z')
        for ob in sc.objects:
            if ob.get('studio') and ob!=camera:ob.matrix_world=xf@ob.matrix_world
        human_height=None
        if shot.get('human'):
            people=studio.human();bpy.context.view_layer.update()
            points=[o.matrix_world@v.co for o in people if o.type=='MESH' for v in o.data.vertices]
            human_height=max(p.z for p in points)-min(p.z for p in points)
            for ob in people:ob.location+=Vector(shot['human_offset'])
        for node,angle in shot.get('parts',{}).items():
            ob=bpy.data.objects[node];ob.matrix_basis=ob.matrix_basis@Matrix.Rotation(math.radians(angle),4,ob['pivot_axis'])
        update_supports()
        lighting=dict(type='C150 gallery',recipe='render_final.py gallery, unchanged lights and cove',scale=3)
        if a.camera_file:
            from suv_lighting import matched_daylight
            lighting=matched_daylight(name)
        camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0))
        camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.ortho_scale=shot.get('ortho',5.25);camera.data.lens=shot.get('lens',65)
        camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36;camera.data.clip_start=.01;camera.data.clip_end=200
        sc.render.engine=a.engine
        if a.engine=='CYCLES':
            gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=12;sc.cycles.transmission_bounces=8;sc.cycles.transparent_max_bounces=8
            sc.cycles.use_adaptive_sampling=True;sc.cycles.adaptive_threshold=.025
        else:
            sc.eevee.taa_render_samples=max(192,a.samples);sc.eevee.use_raytracing=True
            sc.eevee.ray_tracing_options.resolution_scale='1';sc.eevee.ray_tracing_options.screen_trace_quality=1;sc.eevee.ray_tracing_options.screen_trace_thickness=.003
            if final:D.eevee_glass()
        sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast'
        exposure=shot.get('exposure',-2.0)
        if paint=='Aluminum' and not a.camera_file:exposure-=.80
        if a.camera_file:exposure=-.95 if name=='used_rear' else .2
        sc.view_settings.exposure=exposure
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.6));sc.render.resolution_percentage=100
        sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
        sc.render.film_transparent=bool(a.camera_file) or camera.data.type=='ORTHO'
        bpy.data.objects['Studio seamless'].hide_render=sc.render.film_transparent
        sc.render.filepath=str((out/(name+'.png')).resolve());bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
        meta[name]=dict(shot,stage='final exported GLB' if final else 'source control',source_sha256=digest,render_recipe_sha256=recipe,paint=paint,engine=a.engine,samples=a.samples,width=a.width,height=sc.render.resolution_y,exposure=exposure,lighting=lighting,human_measured_height_m=human_height)
        for ob in sc.objects:
            if ob.get('studio') and ob.type=='MESH':ob.hide_render=True
        for mat in bpy.data.materials:mat.diffuse_color=(1,1,1,1) if mat.get('vehicle_paint') or mat.get('paint_decode') else (0,0,0,1)
        sc.render.engine='BLENDER_WORKBENCH';sh=sc.display.shading;sh.light='FLAT';sh.color_type='MATERIAL';sh.show_shadows=False;sh.show_cavity=False;sh.show_specular_highlight=False;sh.show_object_outline=False;sc.display.render_aa='16'
        sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.render.film_transparent=True
        sc.render.filepath=str((out/(name+'-mask.png')).resolve());bpy.ops.render.render(write_still=True)
        meta[name]['tonal_mask']=name+'-mask.png';(out/'shots.json').write_text(json.dumps(meta,indent=2));print('X220_DELIVERY_RENDER',name,flush=True)


if __name__=='__main__':main()
