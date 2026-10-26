"""Procedural product studio, configured by an asset's src/config.py.

Look-dev explicitly loads a .blend. Final mode accepts ONLY an exported GLB.
No downloaded lighting. All temporary scene objects are tagged studio=True.
"""
import argparse, math, sys, runpy, json, hashlib
from pathlib import Path
import bpy
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit import model as G, gpu, rig


def studio_mat(name,col,rough):
    m=bpy.data.materials.new(name);m.use_nodes=True
    b=m.node_tree.nodes['Principled BSDF'];b.inputs['Base Color'].default_value=(*col,1);b.inputs['Roughness'].default_value=rough
    return m


def add_studio(light_scale=None, light_center=(0,0,0), backdrop_half_width=12,
               backdrop_color=(.48,.49,.47), backdrop_roughness=.78,
               scale=None, backdrop_height=None):
    # scale is canonical; light_scale is its lighting-only legacy alias. Preserve
    # legacy backdrop/flag dimensions when only light_scale was supplied.
    geometry_scale=1 if scale is None else scale
    if scale is not None and light_scale is not None and scale!=light_scale:
        raise ValueError('scale and legacy light_scale disagree')
    scale=scale if scale is not None else (1 if light_scale is None else light_scale)
    before=set(bpy.context.scene.objects)
    sc=bpy.context.scene
    prof=[(-10,-.002),(2,-.002)]+[(2+1.8*math.sin(i*math.pi/48),1.8-1.8*math.cos(i*math.pi/48)-.002) for i in range(1,25)]+[(3.8,6)]
    G.loft('Studio seamless',[[(x,y,z) for x in (-backdrop_half_width,backdrop_half_width)] for y,z in prof],studio_mat('Studio warm gray',backdrop_color,backdrop_roughness),caps=False,closed=False)
    world=bpy.data.worlds.new('Procedural studio world');world.use_nodes=True;sc.world=world
    bg=world.node_tree.nodes['Background'];bg.inputs['Color'].default_value=(.20,.22,.25,1);bg.inputs['Strength'].default_value=.12
    def light(name,loc,target,power,w,h,color):
        loc=Vector(loc)*scale+Vector(light_center);target=Vector(target)*scale+Vector(light_center)
        d=bpy.data.lights.new(name,'AREA');d.energy=power*scale**2;d.shape='RECTANGLE';d.size=w*scale;d.size_y=h*scale;d.color=color
        ob=bpy.data.objects.new(name,d);sc.collection.objects.link(ob);ob.location=loc
        ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    light('Key softbox',(-4.0,-1.8,3.2),(0,0,.72),1400,1.3,1.8,(1,.96,.90))
    light('Camera fill',(2.1,-3.5,2.1),(0,0,.72),115,2.7,2.0,(.92,.96,1))
    light('Right rim strip',(1.8,1.2,2.4),(0,0,.78),520,.28,2.2,(.91,.96,1))
    light('Left rim strip',(-1.9,.7,2.1),(0,0,.80),310,.22,1.8,(1,.98,.92))
    light('Overhead reflection card',(0,.3,3.8),(0,0,.75),70,1.0,.3,(1,1,1))
    # Negative-fill flags shape reflections on enamel and stainless.
    for sign in (-1,1):
        flag=G.box('Studio black reflection flag',(sign*1.65,-.1,1.1),(.035,2.1,2.1),studio_mat('Flag black',(.003,.003,.003),.9),0)
        flag.visible_camera=False;flag.visible_shadow=False
    cam=bpy.data.objects.new('Studio camera',bpy.data.cameras.new('Studio camera'));sc.collection.objects.link(cam);sc.camera=cam
    for ob in set(sc.objects)-before:
        ob['studio']=True
        if geometry_scale!=1 and ob.type=='MESH':
            ob.location*=geometry_scale
            for vertex in ob.data.vertices:vertex.co*=geometry_scale
            if ob.name=='Studio seamless':
                for vertex in ob.data.vertices:vertex.co.z+=.002*(geometry_scale-1)
    if backdrop_height is not None:
        for vertex in bpy.data.objects['Studio seamless'].data.vertices:
            if vertex.co.z>5.9*geometry_scale:vertex.co.z=backdrop_height
    return cam


def human():
    """Neutral 1.8 m stylized silhouette with no facial, clothing or gender detail."""
    before=set(bpy.context.scene.objects);m=studio_mat('Silhouette neutral',(.065,.074,.077),.85)
    x,y=-1.03,.24
    G.smooth(G.loft('Scale torso',[[(x+u,y+v,z) for u,v in G.rounded_rectangle(w*2,.16,.045,4)]
            for z,w in [(.84,.14),(1.03,.13),(1.33,.18),(1.44,.21),(1.50,.10)]],m))
    G.cylinder('Scale neck',(x,y,1.48),(x,y,1.57),.055,m,16)
    head=G.lathe('Scale head',[(1.55,0),(1.56,.065),(1.61,.087),(1.71,.089),(1.77,.065),(1.79,.035),(1.80,0)],m,24,center=(x,y))
    for sign in (-1,1):
        G.tube('Scale arm',[(x+sign*.18,y,1.42),(x+sign*.25,y,1.17),(x+sign*.27,y,.98)],.047,m,12)
        G.tube('Scale leg',[(x+sign*.08,y,.88),(x+sign*.105,y,.48),(x+sign*.115,y,.08)],.070,m,12)
        G.box('Scale foot',(x+sign*.115,y-.055,.04),(.14,.25,.08),m,.025,3)
    obs=list(set(bpy.context.scene.objects)-before)
    for ob in obs:ob['studio']=True
    return obs


def display_instances(definitions):
    """Clone authored modules for a shot, sharing mesh/atlas data unchanged.

    Placement is absolute in Blender meters. This is review-only instancing;
    the source GLB remains the independently verified reusable module library.
    """
    created=[]
    for row in definitions:
        source=bpy.data.objects[row['source']]
        members=[source]+list(source.children_recursive)
        copies={ob:ob.copy() for ob in members}
        for ob,copy in copies.items():
            bpy.context.scene.collection.objects.link(copy)
            copy.name=row['name']+'__'+ob.name
            copy.parent=copies.get(ob.parent)
            copy.matrix_parent_inverse=ob.matrix_parent_inverse.copy()
            copy.matrix_basis=ob.matrix_basis.copy()
            created.append(copy)
        root=copies[source];root.name=row['name']
        root.location=row.get('location',source.location)
        root.rotation_euler=tuple(math.radians(v) for v in row.get('rotation_degrees',(0,0,0)))
    return created


def main():
    p=argparse.ArgumentParser();p.add_argument('--fit-reference');p.add_argument('--camera-file');p.add_argument('--source',required=True);p.add_argument('--stage',choices=['lookdev','final'],default='lookdev');p.add_argument('--config',required=True);p.add_argument('--out',required=True);p.add_argument('--shots',default='hero_closed,hero_open,controls,front,side');p.add_argument('--engine',choices=['CYCLES','BLENDER_EEVEE','BLENDER_WORKBENCH'],default='CYCLES');p.add_argument('--width',type=int,default=1400);p.add_argument('--samples',type=int,default=64)
    p.add_argument('--lid-node',default='Lid');p.add_argument('--lid-axis',choices=['X','Y','Z'],default='X')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
    if a.stage=='final':
        if source.suffix!='.glb':raise ValueError('Final renders must load the exported GLB')
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source))
        # glTF importer makes a bone-display icosphere in a hidden collection.
        for ob in list(bpy.context.scene.objects):
            if ob.type=='MESH' and 'asset_set' not in ob:bpy.data.objects.remove(ob,do_unlink=True)
    else:bpy.ops.wm.open_mainfile(filepath=str(source))
    source_digest=hashlib.sha256(source.read_bytes()).hexdigest()
    sc=bpy.context.scene
    config=runpy.run_path(a.config)
    studio_options=dict(config.get('STUDIO',{}))
    if 'STUDIO_SCALE' in config:studio_options.setdefault('scale',config['STUDIO_SCALE'])
    # Preserve zero-argument capture wrappers when no backdrop override exists.
    if config.get('STUDIO_BACKDROP_HEIGHT') is not None:
        studio_options.setdefault('backdrop_height',config['STUDIO_BACKDROP_HEIGHT'])
    cam=add_studio(**studio_options)
    bpy.context.view_layer.update()
    studio_rest={ob:ob.matrix_world.copy() for ob in sc.objects if ob.get('studio') and ob!=cam}
    silhouette=human()
    human_rest={ob:ob.location.copy() for ob in silhouette}
    sc.render.engine=a.engine
    if a.engine=='CYCLES':
        gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True
        sc.cycles.max_bounces=8;sc.cycles.use_adaptive_sampling=True
        sc.cycles.adaptive_threshold=.025
    elif a.engine=='BLENDER_WORKBENCH':
        sh=sc.display.shading;sh.light='STUDIO';sh.color_type='SINGLE'
        sh.single_color=(.48,.51,.50);sh.show_shadows=True;sh.show_cavity=True
        # Workbench ignores Cycles ray visibility; keep reflection flags out of
        # its geometry preview and use neutral clay so dark paint remains legible.
        for ob in sc.objects:
            if ob.name.startswith('Studio black reflection flag'):ob.hide_render=True
        sc.display.render_aa='16'
    else:
        sc.eevee.taa_render_samples=a.samples;sc.eevee.use_raytracing=True
        sc.eevee.ray_tracing_options.resolution_scale='1'
        sc.eevee.ray_tracing_options.screen_trace_quality=.75
        sc.eevee.ray_tracing_options.trace_max_roughness=.7
        sc.eevee.shadow_ray_count=3
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=0
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.resolution_percentage=100
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    shots=config['SHOTS'].copy();
    if a.camera_file:
        shots.update({key:value['shot'] for key,value in json.loads(Path(a.camera_file).read_text()).items()})
    metadata=json.loads((out/'shots.json').read_text()) if (out/'shots.json').exists() else {}
    lid=bpy.data.objects.get(a.lid_node)
    if lid:lid.rotation_mode='XYZ'
    rest=lid.rotation_euler.copy() if lid else None
    part_rest={key:bpy.data.objects[key].matrix_basis.copy() for shot in shots.values() for key in shot.get('parts',{}) if key in bpy.data.objects}
    emissions={m: m.node_tree.nodes.get('SURFACE') or next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None) for m in bpy.data.materials if m.use_nodes}
    emissions={m: (n,n.inputs['Emission Strength'].default_value) for m,n in emissions.items() if n and n.inputs['Emission Strength'].default_value>0}
    for name in a.shots.split(','):
        shot=shots[name]
        for m,(node,strength) in emissions.items():node.inputs['Emission Strength'].default_value=strength*shot.get('emission_scale',1)
        # Optional per-view studio orientation keeps the seamless behind back views.
        studio_rotation=Matrix.Rotation(math.radians(shot.get('studio_yaw',0)),4,'Z')
        for ob,matrix in studio_rest.items():ob.matrix_world=studio_rotation@matrix
        for key,matrix in part_rest.items():bpy.data.objects[key].matrix_basis=matrix
        for key,pose in shot.get('parts',{}).items():
            if 'translation' in pose:bpy.data.objects[key].location+=Vector(pose['translation'])
            if 'rotation_degrees' in pose:
                part=bpy.data.objects[key];part.rotation_mode='XYZ'
                part.rotation_euler.rotate(__import__('mathutils').Euler(tuple(math.radians(v) for v in pose['rotation_degrees'])))
        instances=display_instances(shot.get('instances',[]))
        imported_reference=[]
        if shot.get('fit_reference'):
            reference=Path(a.fit_reference).expanduser() if a.fit_reference else None
            if not reference or not reference.is_file():
                message='SKIP fit-check render: optional owner tank is absent'
                print(message,flush=True);(out/(name+'.png')).unlink(missing_ok=True)
                metadata[name]={'skipped':message,'source':str(source)}
                (out/'shots.json').write_text(json.dumps(metadata,indent=2));continue
            before_reference=set(sc.objects)
            bpy.ops.import_scene.gltf(filepath=str(reference))
            imported_reference=list(set(sc.objects)-before_reference)
            socket=bpy.data.objects[shot.get('fit_socket','tank_socket')]
            for ob in imported_reference:
                original=ob.matrix_world.copy();ob.matrix_world=socket.matrix_world@original
                ob.hide_render='collision' in ob.name.lower()
        for arm in [o for o in sc.objects if o.type=='ARMATURE']:
            rig.reset(arm)
            if shot.get('hose')=='dangling':rig.dangling(arm,**config.get('RIG_POSES',{}).get(arm.name,{}))
        if lid:lid.rotation_euler=rest;lid.rotation_euler['XYZ'.index(a.lid_axis)]+=math.radians(shot.get('lid',0))
        for ob in silhouette:
            ob.hide_render=not shot.get('human',False)
            ob.location=human_rest[ob]+Vector(shot.get('human_offset',(0,0,0)))
        cam.location=shot['location'];target=Vector(shot['target'])
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.rotation_euler.rotate_axis('Z',shot.get('roll',0))
        cam.data.type='ORTHO' if 'ortho' in shot else 'PERSP'
        cam.data.ortho_scale=shot.get('ortho',1.6);cam.data.lens=shot.get('lens',70)
        cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36
        sc.view_settings.exposure=shot.get('exposure',.3 if a.engine=='BLENDER_WORKBENCH' else -.8)
        cam.data.clip_start=.01;cam.data.clip_end=100
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.25))
        sc.render.film_transparent=cam.data.type=='ORTHO' or shot.get('background')=='transparent'
        bpy.data.objects['Studio seamless'].hide_render=cam.data.type=='ORTHO'
        for ob in sc.objects:
            if ob.type=='MESH' and 'asset_set' in ob:
                ob.hide_render=ob.get('bake_only',False) or any(ob.name.startswith(prefix) for prefix in shot.get('hide',[]))
                ob.hide_render|=ob.get('asset_set') in shot.get('hide_sets',[])
                parent=ob.parent
                while parent:
                    ob.hide_render|=parent.name in shot.get('hide_assemblies',[])
                    parent=parent.parent
                if shot.get('isolate'):
                    ob.hide_render=not any(ob.name.startswith(prefix) for prefix in shot['isolate'])
        sc.render.filepath=str((out/(name+'.png')).resolve())
        bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
        metadata[name]=dict(shot,width=sc.render.resolution_x,height=sc.render.resolution_y,source=str(source),source_sha256=source_digest,stage=a.stage,engine=a.engine,samples=a.samples)
        (out/'shots.json').write_text(json.dumps(metadata,indent=2))
        print('RENDERED',sc.render.filepath,flush=True)
        for ob in imported_reference:bpy.data.objects.remove(ob,do_unlink=True)
        for ob in reversed(instances):bpy.data.objects.remove(ob,do_unlink=True)

if __name__=='__main__':main()
