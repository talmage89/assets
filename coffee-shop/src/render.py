"""Cycles checkpoint images from the actual external glTF exports only."""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from kit import gpu,model,tiling,studio
from plan import PROOFS
from package import bundle


def camera(loc,target,lens=40,ortho=None):
    sc=bpy.context.scene
    if sc.camera is None:
        o=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'));sc.collection.objects.link(o);sc.camera=o
    o=sc.camera;o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.type='ORTHO' if ortho else 'PERSP';o.data.lens=lens;o.data.sensor_width=36;o.data.clip_end=500
    if ortho:o.data.ortho_scale=ortho
    return o


def lighting(elevation=18,azimuth=-155,exposure=-.35):
    # Photo comparisons change the sun while reusing the imported scene.
    # Replace it so each fitted view has exactly one directional light.
    for ob in list(bpy.context.scene.objects):
        if ob.type=='LIGHT' and ob.data.type=='SUN':bpy.data.objects.remove(ob,do_unlink=True)
    sc=bpy.context.scene;world=bpy.data.worlds.new('ProceduralDaylight');world.use_nodes=True;sc.world=world
    n=world.node_tree.nodes;l=world.node_tree.links;sky=n.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(elevation);sky.sun_rotation=math.radians(azimuth);sky.sun_disc=False;sky.altitude=.12
    hue=n.new('ShaderNodeHueSaturation');hue.inputs['Saturation'].default_value=.50;l.new(sky.outputs['Color'],hue.inputs['Color']);l.new(hue.outputs['Color'],n['Background'].inputs['Color']);n['Background'].inputs['Strength'].default_value=.10
    d=bpy.data.lights.new('RakingSun','SUN');o=bpy.data.objects.new('RakingSun',d);sc.collection.objects.link(o);a=math.radians(azimuth);e=math.radians(elevation);v=Vector((math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)));o.rotation_euler=(-v).to_track_quat('-Z','Y').to_euler();d.energy=5;d.angle=math.radians(.55)
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=exposure


def area(name,pos,power,size=1,target=None,color=(1,.81,.61)):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color;o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=pos
    if target:o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    o.visible_camera=False;o.visible_glossy=False;o.visible_transmission=False;return o


def imported(path):
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(Path(path).resolve()));return list(set(bpy.context.scene.objects)-before)


def context(p):
    # Presentation only: the roadway, original library trees and nearby hosts.
    sc=bpy.context.scene;z=p['grade'];walk=p['walk'];a=tiling.material('Asphalt',REPO/'ground/textures/ship')
    # The lowest sidewalk pour ends at grade-.14. Raise only the parcel's
    # subgrade, ending at the curb face, so the road remains above its base.
    lm=tiling.material('Lawn',REPO/'ground/textures/ship')
    land=model.box('Context distant ground',(0,15,z-.25),(220,190,.15),lm,0);tiling.world_uv(land,3.048)
    land=model.box('Context continuous ground',(0,95-walk/2-.075,z-.201),(220,190+walk+.15,.15),lm,0);tiling.world_uv(land,3.048)
    ob=model.box('Context road',(0,-walk-6,z-.23),(110,12,.15),a,0);tiling.world_uv(ob,6.096)
    con=tiling.material('Concrete',REPO/'ground/textures/ship')
    ob=model.box('Context opposite walk',(0,-walk-13.1,z-.10),(110,2.2,.18),con,0);tiling.world_uv(ob,3.048)
    for x in (-p['width']/2-7.5,p['width']/2+8):
        obs=imported(REPO/'trees/export/RedMaple.glb')
        roots=[o for o in obs if o.parent not in obs]
        for o in roots:o.location=(x,4.5,z)
    # The room must reflect a street, rather than only unoccluded sky.
    for x in ((-p['width'],p['width']) if p['kind']=='downtown' else (p['width'],) if p['kind']=='strip' else (-27,28)):
        obs=imported(Path('build/hosts')/(p['kind']+'.glb'))
        for o in obs:
            if o.parent not in obs:o.location.x+=x;o.location.y+=8 if p['kind']=='pad' else 0


def setup(seed,with_context=True):
    bpy.ops.wm.read_factory_settings(use_empty=True);p=json.loads(Path(f'build/shops/{seed}.json').read_text());path=Path(f'export/sites/CoffeeSite-{seed}.gltf') if with_context else Path(f'export/CoffeeShop-{seed}.gltf')
    obs=imported(path)
    for o in obs:
        if o.parent not in obs and not with_context:o.location.y+=p['depth']/2
    bpy.context.view_layer.update()
    for o in obs:
        if o.get('socket_kind')=='light' and o.name.startswith('Room_Pendant'):
            area(o.name+' illumination',o.matrix_world.translation,o.get('power_w',90),.32)
    # Ambient interior bounce supplement at the actual ceiling, included in
    # presentation only. No unexported room geometry is loaded.
    for x,y in ((p['counter_x'],p['counter_y']),(0,5.5)):
        area('Room ceiling practical',(x,y,p['grade']+2.88),240,1.25)
    if p['kind']=='downtown':
        for x in (-8.23,8.84,-15.55,17.37):area('Neighbor tenant practical',(x,2.2,2.8),190,1.6)
    elif p['kind']=='strip':
        for x in (9.60,16,22.4,28.8):area('Other tenant practical',(x,2.8,2.8),180,1.4)
    lighting(azimuth={'downtown':-155,'strip':-145,'pad':-55}[p['kind']]);return p,path


def source_finish():
    """Compare original charts/height with their baked shipping response."""
    for mat in bpy.data.materials:
        if not mat.use_nodes:continue
        nodes=mat.node_tree.nodes;links=mat.node_tree.links;bs=nodes.get('Principled BSDF')
        if not bs:continue
        own=False
        for node in nodes:
            if node.type!='TEX_IMAGE' or not node.image:continue
            stem=Path(node.image.filepath).name
            if stem=='T_CoffeeShop_BaseColor.png':node.image=bpy.data.images.load(str(Path('build/atlas/T_CoffeeShop_BaseColor.png').resolve()),check_existing=True);own=True
            elif stem=='T_CoffeeShop_ORM.png':node.image=bpy.data.images.load(str(Path('build/procedural/T_CoffeeShop_ORM.png').resolve()),check_existing=True);node.image.colorspace_settings.name='Non-Color'
        if own:
            h=nodes.new('ShaderNodeTexImage');h.image=bpy.data.images.load(str(Path('build/procedural/T_CoffeeShop_Height.png').resolve()),check_existing=True);h.image.colorspace_settings.name='Non-Color'
            bump=nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.004;links.new(h.outputs['Color'],bump.inputs['Height']);links.new(bump.outputs['Normal'],bs.inputs['Normal'])


def shots(p):
    z=p['grade'];t=p['tables'][1];kind=p['kind'];w=p['width']
    a=math.radians(t['rotation']);radial=Vector((math.cos(a),math.sin(a),0));tangent=Vector((-math.sin(a),math.cos(a),0));chair=Vector((t['x'],t['y'],z))+.58*radial
    cc=chair+.8*radial-1.6*tangent+Vector((0,0,.98))
    hero= dict(location=(7,-21.0,1.65+z),target=(0,0,3.58),lens=40) if kind=='downtown' else dict(location=(-10,-23.8,1.65+z),target=(0,-.3,2.18),lens=45) if kind=='strip' else dict(location=(16,-18.5,1.65+z),target=(2.0,.0,1.56),lens=42)
    ctr=(2.25,-1.8,1.72+z) if kind=='downtown' else (.80,-1.7,1.72+z) if kind=='strip' else (3,-1.7,1.72+z)
    return dict(hero=hero,above=dict(location=(12,-17,30),target=(1,-.4,0),lens=45,ortho=25 if kind!='pad' else 29),
        site=dict(location=(44,-51,62),target=(6,-2,0),lens=45,ortho=70 if kind!='downtown' else 85),
        table=dict(location=(t['x']+1.25,t['y']-1.65,1.48+z),target=(t['x'],t['y'],.73+z),lens=50),
        counter=dict(location=(-.65,-1.0,1.72+z),target=(p['counter_x']-1.65,p['counter_y'],1.37+z),lens=34) if kind=='strip' else dict(location=ctr,target=(p['counter_x'],p['counter_y'],1.37+z),lens=34),
        awning=dict(location=(.5,-8.2,4.85+z),target=(.4,-.45,3.62),lens=46) if kind=='strip' else dict(location=(3.3,-6.3,2.20+z),target=(.7,-.25,3.50 if kind=='downtown' else 3.20),lens=48),
        chair=dict(location=tuple(cc),target=tuple(chair+Vector((0,0,.43))),lens=45),
        scale=dict(location=(-7,-12,1.65+z),target=(-1,-1.8,1.3+z),lens=42),
        walkup=dict(location=(11,1.4,1.65+z),target=(5.49,2.8,1.35+z),lens=45))


def projection(points,cam):
    sc=bpy.context.scene;bpy.context.view_layer.update()
    return [(v.x,1-v.y) for p in points for v in [world_to_camera_view(sc,cam,Vector(p))]]


def render(path,recipe,source,metadata=None):
    sc=bpy.context.scene;cam=camera(recipe['location'],recipe['target'],recipe.get('lens',40),recipe.get('ortho'));path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if recipe.get('roll'):cam.rotation_euler.rotate_axis('Z',recipe['roll'])
    sc.render.filepath=str(path.resolve());bpy.ops.render.render(write_still=True)
    doc=dict(source=str(source),bundle_sha256=bundle(source),image_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),engine=sc.render.engine,recipe=recipe,width=sc.render.resolution_x,height=sc.render.resolution_y)
    doc.update(metadata or {});path.with_suffix('.json').write_text(json.dumps(doc,indent=2)+'\n')


def main():
    a=argparse.ArgumentParser();a.add_argument('--source');a.add_argument('--out',type=Path,default=Path('renders/checkpoint'));a.add_argument('--pass',dest='pass_name',default='checkpoint');a.add_argument('--width',type=int,default=1440);a.add_argument('--samples',type=int,default=32);a.add_argument('--seeds',default='117,228,339');a.add_argument('--shots',default='hero,above,table,counter,awning,chair,scale');a.add_argument('--matches',type=Path);a.add_argument('--source-finish',action='store_true');a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    jobs=[]
    if a.matches:
        for key,row in json.loads(a.matches.read_text()).items():jobs.append((row['seed'],key,row))
    else:
        for seed in map(int,a.seeds.split(',')):
            p=json.loads(Path(f'build/shops/{seed}.json').read_text())
            for key in a.shots.split(',')+(['walkup'] if p['kind']=='pad' else []):jobs.append((seed,key,None))
    previous=None
    for seed,key,match in jobs:
        # Keep the same procedural street around fitted photographic views;
        # the finite exported paving must not float against a black horizon.
        if seed!=previous:
            p,source=setup(seed);previous=seed
            if a.source_finish:source_finish()
        sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=10;sc.cycles.transmission_bounces=8;sc.cycles.transparent_max_bounces=12;gpu.enable()
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width*(.70 if key=='above' else 2/3));sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG'
        human=[];hidden=[];isolation_floor=None
        if key=='chair':
            keep=bpy.data.objects.get('Table_02_Chair_1');assert keep
            allowed=set([keep]+list(keep.children_recursive))
            for ob in sc.objects:
                if ob.type=='MESH' and ob not in allowed and not ob.hide_render:ob.hide_render=True;hidden.append(ob)
            isolation_floor=model.box('Isolated chair floor',(p['tables'][1]['x'],p['tables'][1]['y'],p['grade']-.04),(18,18,.08),studio.studio_mat('Chair neutral floor',(.22,.22,.21),.9),0)
        if key=='scale':
            human=studio.human()
            for o in human:o.location+=Vector((-1.2,-2.0,p['grade']))
        rec=match['shot'] if match else shots(p)[key]
        if match:
            lighting(match.get('sun_elevation',34),match.get('sun_azimuth',-117),match['shot'].get('exposure',-1))
            sc.render.resolution_y=round(a.width/rec['aspect'])
        camera(rec['location'],rec['target'],rec.get('lens',40),rec.get('ortho'))
        if match and rec.get('roll'):sc.camera.rotation_euler.rotate_axis('Z',rec['roll'])
        meta={'isolated_export_node':'Table_02_Chair_1'} if key=='chair' else {}
        meta['finish_stage']='original charts + meter-valued height' if a.source_finish else 'exported baked PBR'
        if key=='above':
            meta['routes']=[dict(**route,screen=projection([(x,y,p['grade']+.02) for x,y in [(route['rect'][0],route['rect'][2]),(route['rect'][1],route['rect'][2]),(route['rect'][1],route['rect'][3]),(route['rect'][0],route['rect'][3])]],sc.camera)) for route in p['routes']]
            meta['tables']=[dict(id=t['id'],accessible=t['accessible'],screen=projection([(t['x'],t['y'],p['grade']+.80)],sc.camera)[0]) for t in p['tables']]
        dest=a.out/(key+'.png') if match else a.out/str(seed)/(key+'.png')
        # Fit roll is applied after camera() in render() below.
        if match:rec=dict(rec,roll=rec.get('roll',0))
        render(dest,rec,source,meta)
        for o in human:bpy.data.objects.remove(o,do_unlink=True)
        for o in hidden:o.hide_render=False
        if isolation_floor:bpy.data.objects.remove(isolation_floor,do_unlink=True)
    if not a.matches and 'scale' in a.shots.split(','):
        bpy.ops.wm.read_factory_settings(use_empty=True);imported('export/CoffeeShopPieces.gltf');lighting();sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width*.72);sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG'
        model.box('Piece sheet floor',(4.3,4.5,-.04),(17,18,.08),studio.studio_mat('Sheet neutral floor',(.22,.22,.21),.9),0)
        rec=dict(location=(14,-19,17),target=(4.3,4.8,.9),lens=44,ortho=18);cam=camera(rec['location'],rec['target'],44,18)
        labels=[dict(name=o.get('piece'),screen=projection([tuple(o.matrix_world.translation+Vector((0,-.55,.03)))],cam)[0]) for o in sc.objects if o.get('piece')]
        render(a.out/'pieces.png',rec,'export/CoffeeShopPieces.gltf',dict(labels=labels))


if __name__=='__main__':main()
