"""Daylight construction review, exclusively from reimported checkpoint GLBs."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit import gpu
from kit import model as G


def simple(name,color):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=.85
    return m


def human(p):
    """Exactly 1.8 m high neutral scale aid, never exported with the house."""
    mat=simple('Neutral 1.8 m figure',(.05,.065,.07));obs=[]
    x,y,z=p
    def part(name,a,c,r,sz=None):
        a,c=Vector(a),Vector(c)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=1,location=(a+c)/2)
        o=bpy.context.object;o.name=name;o.scale=(r,r,(c-a).length/2+r)
        o.rotation_euler=(c-a).to_track_quat('Z','Y').to_euler();o.data.materials.append(mat);obs.append(o)
    def p(a,b,c):return (x+a,y+b,z+c)
    part('Scale torso',p(0,0,1.0),p(0,0,1.38),.15)
    part('Scale head',p(0,0,1.65),p(0,0,1.68),.12)
    for s in (-1,1):
        part('Scale leg',p(s*.09,0,.075),p(s*.09,0,.89),.075)
        part('Scale arm',p(s*.22,0,.95),p(s*.22,0,1.40),.055)
    return obs


def shots(meta):
    main,garage=meta['blocks'];cx=(main['x0']+main['x1'])/2;cy=(main['y0']+main['y1'])/2
    px=meta['sockets']['FrontThreshold'][0];fy=main['y0'];front=garage['y0']
    # At 20 m from the nearest facade, camera is at true pedestrian eye height.
    side=1 if meta['spec']['garage']['side']=='right' else -1
    result=dict(
        hero=dict(location=(side*17,front-20,1.68),target=(0,-.2,3.7),lens=34,aspect=1.6),
        rear=dict(location=(0,36,4.3),target=(0,0,4.3),ortho=23,aspect=1.7),
        front=dict(location=(0,-36,4.3),target=(0,0,4.3),ortho=23,aspect=1.7),
        side=dict(location=(side*36,0,4.3),target=(0,0,4.3),ortho=15,aspect=1.1),
        back=dict(location=(-14,24,8),target=(0,0,3.9),lens=40,aspect=1.6),
        roof=dict(location=(14,-16,24),target=(0,0,4.3),lens=42,aspect=1.4),
        top=dict(location=(0,0,38),target=(0,0,0),ortho=23,aspect=1.4),
        eave=dict(location=(garage['x1']+1.9,front-2.7,5.03),target=(garage['x1']+.12,front-.10,5.55),lens=50,aspect=1.3),
        window=dict(location=(garage['x1']-2.1,front-3.0,4.8),target=(garage['x0']+garage['width']*.73 if 'width' in garage else garage['x0']+(garage['x1']-garage['x0'])*.73,front,4.65),lens=52,aspect=1.1),
        scale=dict(location=(px+2.7,fy-8.5,2.4),target=(px,fy-.6,1.8),lens=50,aspect=1.4,human=True),
        door_open=dict(location=(px+2.7,fy-6.8,2.4),target=(px,fy-.1,1.7),lens=48,aspect=1.2,door_angle=95),
    )
    valleys=[r for r in meta['roof_junctions'] if r['kind']=='valley']
    valley=max(valleys,key=lambda r:(int('Cricket' in r['blocks']),math.dist(*r['points']))) if valleys else None
    if valley:
        p=[sum(v[k] for v in valley['points'])/2 for k in range(3)]
        result['valley']=dict(location=(p[0]+3.7,p[1]-4.5,p[2]+5.5),target=p,lens=40,aspect=1.3)
    return result


def setup(engine,samples):
    sc=bpy.context.scene;sc.render.engine=engine
    if engine=='CYCLES':gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True
    if engine=='BLENDER_EEVEE':
        sc.eevee.use_raytracing=True
        sc.eevee.ray_tracing_options.resolution_scale='1'
        sc.eevee.ray_tracing_options.screen_trace_quality=.75
        for mat in bpy.data.materials:
            p=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None) if mat.use_nodes else None
            mat.use_raytrace_refraction=bool(p and p.inputs['Transmission Weight'].default_value>0)
            mat.thickness_mode='SLAB'
            if mat.use_raytrace_refraction:
                # Eevee otherwise derives thickness from the whole joined
                # house bounds, skipping the shallow rooms behind its glass.
                # Link the modeled 4 mm pane gauge instead of a building-wide
                # approximation; this is an Eevee integration setting only.
                value=mat.node_tree.nodes.new('ShaderNodeValue');value.outputs[0].default_value=.004
                output=next(n for n in mat.node_tree.nodes if n.type=='OUTPUT_MATERIAL')
                mat.node_tree.links.new(value.outputs[0],output.inputs['Thickness'])
    sc.world=bpy.data.worlds.new('Procedural daylight only');sc.world.use_nodes=True
    ns,ls=sc.world.node_tree.nodes,sc.world.node_tree.links;ns.clear()
    sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(40)
    sky.sun_rotation=math.radians(225);sky.sun_disc=False;sky.air_density=1.;sky.aerosol_density=.35
    bg=ns.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.09
    out=ns.new('ShaderNodeOutputWorld');ls.new(sky.outputs[0],bg.inputs[0]);ls.new(bg.outputs[0],out.inputs[0])
    # Clear procedural sky. The previous dark noise blend read as smoke.
    ld=bpy.data.lights.new('Afternoon sun','SUN');ob=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(ob)
    ld.energy=3.7;ld.color=(1.0,.96,.90);ld.angle=math.radians(1.4)
    ob.rotation_euler=Vector((.6,.7,-1)).to_track_quat('-Z','Y').to_euler()
    floor=G.box('Presentation grade, excluded from asset',(0,0,-.040),(2000,2000,.08),simple('Neutral warm gray grade',(.16,.17,.15)),0)
    camera=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'));sc.collection.objects.link(camera);sc.camera=camera
    camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36;camera.data.clip_start=.03;camera.data.clip_end=3000
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.35
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
    return camera


def render(a):
    if a.source.suffix=='.gltf':
        from delivery_io import bundle_hash
        source_digest=bundle_hash(a.source)
    else:source_digest=hashlib.sha256(a.source.read_bytes()).hexdigest()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if a.source.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
    else:bpy.ops.import_scene.gltf(filepath=str(a.source.resolve()))
    meta=json.loads(a.source.with_suffix('.json').read_text())
    camera=setup(a.engine,a.samples)
    figures=human((meta['sockets']['FrontThreshold'][0]+.40,meta['blocks'][0]['y0']-.9,.48))
    for o in figures:o.hide_render=True
    views=shots(meta)
    px=meta['sockets']['FrontThreshold'][0];fy=meta['blocks'][0]['y0'];g=meta['blocks'][1]
    views['entry']=dict(location=(px+2.0,fy-5.8,2.2),target=(px,fy+.1,1.65),lens=45,aspect=1.2,door_angle=85)
    views['entry_closed']={**views['entry'],'door_angle':0}
    m=meta['blocks'][0]
    views['shingles']=dict(location=(m['x0']+2,m['y0']-20,1.68),target=(m['x0']+4,m['y0']+1.4,7.0),lens=100,aspect=1.6)
    views['window']=dict(location=(m['x0']+1.55,m['y0']-3.0,1.9),target=(m['x0']+1.28,m['y0'],2.02),lens=48,aspect=1.1)
    if a.camera_file:views={name:data['shot'] for name,data in json.loads(a.camera_file.read_text()).items()}
    names=a.shots.split(',') if a.shots else list(views)
    a.out.mkdir(parents=True,exist_ok=True)
    reports={}
    for name in names:
        shot=views[name]
        if bpy.data.objects.get('FrontDoor'):
            door=bpy.data.objects['FrontDoor'];door.rotation_mode='XYZ';door.rotation_euler.z=math.radians(shot.get('door_angle',0))
        for o in figures:o.hide_render=not shot.get('human',False)
        camera.location=shot['location'];direction=Vector(shot['target'])-camera.location
        camera.rotation_euler=direction.to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0))
        camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP'
        if 'ortho' in shot:camera.data.ortho_scale=shot['ortho']
        camera.data.lens=shot.get('lens',45)
        sc=bpy.context.scene;sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.5));sc.render.resolution_percentage=100
        sc.render.film_transparent=shot.get('background')=='transparent'
        sc.render.filepath=str((a.out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        if name=='hero':
            # Triangle-union silhouette, excluding presentation grade and aids.
            # No external occluders are present in this controlled source view.
            from PIL import Image,ImageDraw
            from bpy_extras.object_utils import world_to_camera_view
            mask=Image.new('L',(sc.render.resolution_x,sc.render.resolution_y));draw=ImageDraw.Draw(mask)
            for ob in bpy.context.scene.objects:
                if ob.type!='MESH' or not ob.get('asset_set'):continue
                points=[]
                for v in ob.data.vertices:
                    uv=world_to_camera_view(sc,camera,ob.matrix_world@v.co)
                    points.append((uv.x*mask.width,(1-uv.y)*mask.height))
                ob.data.calc_loop_triangles()
                for t in ob.data.loop_triangles:draw.polygon([points[i] for i in t.vertices],fill=255)
            mask.save(a.out/'hero-mask.png')
        # Dimensions are authored wall-to-wall guides, projected through the
        # very camera used for the elevation. Actual-surface measurements live
        # in the mesh audit, separately from these drawing annotations.
        dimensions=[]
        if name in ('front','side'):
            from bpy_extras.object_utils import world_to_camera_view
            m,g=meta['blocks'];x0=min(m['x0'],g['x0']);x1=max(m['x1'],g['x1']);y0=min(m['y0'],g['y0']);y1=max(m['y1'],g['y1'])
            if name=='front':
                dim=[((x0,y0,-.4),(x1,y0,-.4),f"wall blocks: {x1-x0:.4f} m"),
                     ((m['x0'],m['y0'],9.2),(m['x1'],m['y0'],9.2),f"main: {m['x1']-m['x0']:.4f} m"),
                     ((x0-.6,m['y0'],.508),(x0-.6,m['y0'],5.9944),'9 ft + floor + 8 ft')]
            else:
                dim=[((x1,y0,-.4),(x1,y1,-.4),f"wall blocks: {y1-y0:.4f} m"),
                     ((x1,y1+.65,0),(x1,y1+.65,6.1468),'main roof bearing: 6.1468 m')]
            for a1,c1,label in dim:
                pts=[]
                for point in (a1,c1):
                    uv=world_to_camera_view(sc,camera,Vector(point));pts.append([uv.x*sc.render.resolution_x,(1-uv.y)*sc.render.resolution_y])
                dimensions.append(dict(points=pts,label=label))
        reports[name]=dict(source=str(a.source),sha256=source_digest,stage=meta['stage'],engine=a.engine,camera=shot,dimensions=dimensions)
    current=bundle_hash(a.source) if a.source.suffix=='.gltf' else hashlib.sha256(a.source.read_bytes()).hexdigest()
    assert current==source_digest, 'Source changed during rendering'
    (a.out/'provenance.json').write_text(json.dumps(reports,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=Path('build/house.glb'))
    p.add_argument('--out',type=Path,default=Path('renders/checkpoint'));p.add_argument('--width',type=int,default=1400)
    p.add_argument('--samples',type=int,default=40);p.add_argument('--engine',default='CYCLES');p.add_argument('--shots');p.add_argument('--camera-file',type=Path)
    render(p.parse_args(sys.argv[sys.argv.index('--')+1:]))
