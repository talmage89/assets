"""S240 source and freshly imported GLB review, with shared factory factors."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import studio,gpu
import sedan_colors as FAMILY
from sedan_views import SHOTS


def supports():
    """Re-aim telescoping members from their exported endpoint nodes."""
    bpy.context.view_layer.update()
    for o in bpy.context.scene.objects:
        if 'support_target' not in o or o.constraints:continue
        target=bpy.data.objects[o['support_target']].matrix_world.translation
        p=o.matrix_world.translation.copy();rotation=(target-p).to_track_quat('Z','Y').to_matrix().to_4x4()
        o.matrix_world=Matrix.Translation(p)@rotation
    bpy.context.view_layer.update()


def appearance_points(camera,width,height):
    """Find the actual delivered paint skin before choosing a review patch."""
    from mathutils.bvhtree import BVHTree
    from bpy_extras.object_utils import world_to_camera_view
    vertices=[];faces=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('asset_set')!='Sedan':continue
        start=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        faces.extend(tuple(start+i for i in face.vertices) for face in ob.data.polygons
                     if ob.data.materials[face.material_index].get('vehicle_paint') or ob.data.materials[face.material_index].get('paint_decode'))
    tree=BVHTree.FromPolygons(vertices,faces);result={}
    for label,(y,z) in {'upper front door':(-.48,.70),'front road film':(-.70,.37),'rear door':(.62,.70),'rear road film':(.58,.36),'quarter':(1.65,.84)}.items():
        p=tree.ray_cast(Vector((-2,y,z)),Vector((1,0,0)),4)[0]
        if p is None:raise ValueError('Appearance patch misses actual paint: '+label)
        uv=world_to_camera_view(bpy.context.scene,camera,p)
        result[label]=dict(world_m=list(p),render_pixel=[uv.x*width,(1-uv.y)*height])
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    p.add_argument('--shots',default='front_three_quarter,rear_three_quarter,face,lamp_unlit,lamp_lit,wheel,interior_glass,underbody,opened_front,opened_rear')
    p.add_argument('--studio-exposure',type=float,default=-2.8);p.add_argument('--width',type=int,default=1400);p.add_argument('--samples',type=int,default=40)
    p.add_argument('--motions',action='store_true');p.add_argument('--colors',action='store_true');p.add_argument('--camera-file');p.add_argument('--paint',default='Atlantic')
    p.add_argument('--engine',default='CYCLES',choices=['CYCLES','BLENDER_EEVEE']);p.add_argument('--workbench',action='store_true')
    p.add_argument('--zebra',action='store_true',help='Gallery cameras with evenly spaced reflection lights and neutral polished surfaces')
    p.add_argument('--crop',type=float,nargs=4,metavar=('X0','Y0','X1','Y1'),help='Native pixel bounds, measured from the upper left')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();source_hash=hashlib.sha256(source.read_bytes()).hexdigest();final=source.suffix.lower()=='.glb'
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if final:
        bpy.ops.import_scene.gltf(filepath=str(source));import delivery_materials as D;D.install()
    else:bpy.ops.wm.open_mainfile(filepath=str(source))
    sc=bpy.context.scene;camera=studio.add_studio(scale=2.5,backdrop_color=(.20,.21,.22))
    for name in ['Right rim strip','Left rim strip']:bpy.data.objects[name].data.size*=4.5
    bpy.data.objects['Key softbox'].data.size*=1.6;bpy.data.objects['Key softbox'].data.size_y*=1.2
    bpy.data.objects['Overhead reflection card'].data.size*=1.5
    # Car-width panels sit below the tall equipment studio. Their continuous
    # reflected strips reveal compound panel curvature and the smooth coat.
    panels={
      'Key softbox':((-4,-3,3.5),2200,4.0,2.2),
      'Camera fill':((4,-2,2.3),700,5.0,1.5),
      'Right rim strip':((3.6,2.7,2.1),1000,5.0,1.0),
      'Left rim strip':((-3.5,1.5,2.4),900,5.0,1.2),
      'Overhead reflection card':((0,.3,5),900,4.0,2.0),
    }
    for name,(position,power,width,height) in panels.items():
        ob=bpy.data.objects[name];ob.location=position
        ob.rotation_euler=(Vector((0,0,.75))-ob.location).to_track_quat('-Z','Y').to_euler()
        ob.data.energy=power;ob.data.size=width;ob.data.size_y=height
    light_data=bpy.data.lights.new('S240 underside inspection fill','AREA');light_data.energy=0;light_data.size=4
    bottom_fill=bpy.data.objects.new('S240 underside inspection fill',light_data);sc.collection.objects.link(bottom_fill);bottom_fill.location=(0,0,-3);bottom_fill.rotation_euler=(Vector((0,0,.25))-bottom_fill.location).to_track_quat('-Z','Y').to_euler();bottom_fill['studio']=True
    people=studio.human()
    if a.zebra:
        from sedan_reflection_review import setup
        setup()
    if a.camera_file:
        from sedan_lighting import setup
        setup()
    shots={n:dict(s) for n,s in SHOTS.items()}
    if a.motions:
        from sedan_views import motion_shots
        shots=motion_shots()
    if a.colors:shots={color+'_'+view:dict(SHOTS[view+'_three_quarter'],paint=color) for color in FAMILY.COLORS for view in ['front','rear']}
    if a.camera_file:shots={n:r['shot'] for n,r in json.loads(Path(a.camera_file).read_text()).items()}
    names=list(shots) if a.colors or a.motions or a.camera_file else a.shots.split(',')
    bpy.context.view_layer.update();poses={o.name:o.matrix_basis.copy() for o in sc.objects if o.type=='EMPTY'}
    rest={o:o.matrix_world.copy() for o in sc.objects if o.get('studio') and o!=camera};visibility={o:o.hide_render for o in rest}
    colors={m:m.diffuse_color[:] for m in bpy.data.materials}
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);meta=json.loads((out/'shots.json').read_text()) if (out/'shots.json').exists() else {}
    recipe=hashlib.sha256(b''.join(Path(__file__).with_name(n).read_bytes() for n in ['sedan_lookdev.py','sedan_views.py','sedan_colors.py','delivery_materials.py','sedan_lighting.py','lighting.py'])).hexdigest()
    for name in names:
        shot=shots[name];paint=shot.get('paint','Graphite' if a.camera_file else a.paint);lights=shot.get('lights',False)
        if final:D.apply(paint,lights)
        else:
            for m in bpy.data.materials:
                if m.get('vehicle_paint'):
                    m.node_tree.nodes['Paint tint'].outputs[0].default_value=(*FAMILY.COLORS[paint],1)
                    m.node_tree.nodes['Paint metallic'].outputs[0].default_value=FAMILY.PAINT_METAL[paint]
                if m.get('lamp_lit_strength',0)>0:m.node_tree.nodes['SURFACE'].inputs['Emission Strength'].default_value=m['lamp_lit_strength'] if lights else 0
        if a.zebra:
            from sedan_reflection_review import material
            material()
        xf=Matrix.Rotation(math.radians(shot.get('studio_yaw',0)),4,'Z')
        for o,m in rest.items():o.matrix_world=xf@m;o.hide_render=visibility[o]
        for o in people:
            o.hide_render=not shot.get('human',False)
            if shot.get('human'):
                o.matrix_world=rest[o].copy();o.matrix_world.translation+=Vector((2.75,-.35,0))
        for node,m in poses.items():bpy.data.objects[node].matrix_basis=m
        for node,(axis,angle) in shot.get('parts',{}).items():bpy.data.objects[node].matrix_basis=poses[node]@Matrix.Rotation(math.radians(angle),4,axis)
        bottom_fill.data.energy=750 if shot.get('underside') else 0
        supports();lighting='procedural studio with broad reflection panels'
        if a.camera_file:
            from sedan_lighting import conditions
            lighting=conditions('aged_front' if 'front' in name else 'aged_rear')
        camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0))
        camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36;camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.ortho_scale=shot.get('ortho',5.7);camera.data.lens=shot.get('lens',58);camera.data.clip_start=.01;camera.data.clip_end=200
        sc.render.engine='BLENDER_WORKBENCH' if a.workbench else a.engine
        if sc.render.engine=='CYCLES':
            gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=12;sc.cycles.transmission_bounces=8;sc.cycles.transparent_max_bounces=8;sc.cycles.use_adaptive_sampling=True;sc.cycles.adaptive_threshold=.008
        elif sc.render.engine=='BLENDER_EEVEE':
            sc.eevee.taa_render_samples=max(128,a.samples);sc.eevee.use_raytracing=True
            if final:D.eevee_glass()
        else:
            sh=sc.display.shading;sh.light='STUDIO';sh.studio_light='studio.sl';sh.color_type='MATERIAL';sh.show_cavity=True;sh.cavity_type='BOTH';sh.show_shadows=True;sh.show_specular_highlight=True
            for o in sc.objects:
                if o.get('studio') and o.type in ['MESH','LIGHT']:o.hide_render=True
        sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=shot.get('exposure',a.studio_exposure) if not a.workbench else .3
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.65));sc.render.resolution_percentage=100
        if a.crop:
            x0,y0,x1,y1=a.crop;sc.render.use_border=True;sc.render.use_crop_to_border=True
            sc.render.border_min_x=x0/sc.render.resolution_x;sc.render.border_max_x=x1/sc.render.resolution_x
            sc.render.border_min_y=1-y1/sc.render.resolution_y;sc.render.border_max_y=1-y0/sc.render.resolution_y
        sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=bool(a.camera_file) or a.workbench or camera.data.type=='ORTHO' or shot.get('underside',False);bpy.data.objects['Studio seamless'].hide_render=sc.render.film_transparent
        sc.render.filepath=str((out/(name+'.png')).resolve());bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
        meta[name]=dict(shot,source=str(source),source_sha256=source_hash,render_recipe_sha256=recipe,stage='final exported GLB' if final else 'source detail and look-dev',paint=paint,lighting=lighting,engine=sc.render.engine,width=sc.render.resolution_x,height=sc.render.resolution_y,samples=a.samples,exposure=sc.view_settings.exposure)
        if a.zebra:meta[name]['reflection_lines']=dict(spacing_m=.60,width_m=.13,count_per_rack=15,racks=['ceiling','wall'],mesh_normals=True,normal_map=False)
        if a.crop:meta[name]['native_crop_pixels']=a.crop
        if a.camera_file:meta[name]['appearance_points']=appearance_points(camera,sc.render.resolution_x,sc.render.resolution_y)
        # Same-framing paint/geometry mask, independent of backdrop and floor.
        for o in rest:
            if o.type=='MESH':o.hide_render=True
        for m in bpy.data.materials:m.diffuse_color=(1,1,1,1) if m.get('vehicle_paint') or m.get('paint_decode') else (0,0,0,1)
        sc.render.engine='BLENDER_WORKBENCH';sh=sc.display.shading;sh.light='FLAT';sh.color_type='MATERIAL';sh.show_cavity=False;sh.show_shadows=False;sh.show_specular_highlight=False
        sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.render.film_transparent=True
        sc.render.filepath=str((out/(name+'-mask.png')).resolve());bpy.ops.render.render(write_still=True)
        for m,c in colors.items():m.diffuse_color=c
        meta[name]['tonal_mask']=name+'-mask.png';(out/'shots.json').write_text(json.dumps(meta,indent=2));print('S240_RENDERED',name,flush=True)
if __name__=='__main__':main()
