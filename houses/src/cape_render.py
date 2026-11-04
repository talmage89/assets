"""Cape source and delivered-file views in GPU Cycles and Eevee."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from render import setup,human
from cape_reflections import scenery as reflection_scenery


def recipe_sha(extra=()):
    paths=[HERE/name for name in ('cape_render.py','cape_reflections.py','render.py','ranch_render.py')]+list(extra)
    return hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in paths)).hexdigest()


def views(meta):
    m=meta['blocks'][0];lo,hi=map(Vector,meta['bounds']);w=hi.x-lo.x;cx=(hi.x+lo.x)/2;cy=(hi.y+lo.y)/2;z=3.0
    x=meta['door_x'];y=m['y0'];d=next((v for v in meta['blocks'] if v['name'].startswith('Dormer')),None)
    dx=(d['x0']+d['x1'])/2 if d else (m['x0']+m['x1'])/2;dy=d['y0'] if d else m['y0'];dz=d['floor']+1.4 if d else m['eave']+1.0
    wallx=m['x0']+(m['x1']-m['x0'])*.39
    sill=next(o for o in meta['openings'] if o['block']=='Main' and o['face']=='front' and o['kind']=='window')
    sx=m['x0']+sill['u'];sz=sill['z']
    bridge=next((b for b in meta['blocks'] if b['name']=='Breezeway'),None)
    bx=(bridge['x0']+bridge['x1'])/2 if bridge else x;by=bridge['y0'] if bridge else y
    shots=dict(hero=dict(location=(cx+w*.85,cy-w*1.45-9,4.4),target=(cx,cy,2.65),lens=45,aspect=1.65),
        front=dict(location=(cx,-60,3.8),target=(cx,0,3.8),ortho=max(14,w+2),aspect=max(1.65,(w+2)/8.0)),
        rear=dict(location=(cx,60,3.8),target=(cx,0,3.8),ortho=max(14,w+2),aspect=max(1.65,(w+2)/8.0)),
        back=dict(location=(cx-w*.6,cy+w*1.25+9,7.5),target=(cx,cy,2.9),lens=43,aspect=1.65),
        roof=dict(location=(cx+12,cy-17,23),target=(cx,cy,2.5),lens=40,aspect=1.5),
        dormer=dict(location=(dx+2.4,dy-5.5,dz+1.2),target=(dx,dy+.25,dz),lens=52,aspect=1.25),
        eave=dict(location=(m['x1']+1.9,y-2.9,2.0),target=(m['x1']-.12,y-.03,m['eave']+.12),lens=46,aspect=1.25),
        entry=dict(location=(x+1.7,y-5.6,2.0),target=(x,y-.3,m['floor']+1.1),lens=46,aspect=1.2),
        scale=dict(location=(x+3,y-10,2.3),target=(x,y-.5,m['floor']+1),lens=45,aspect=1.5,human=True),
        siding=dict(location=(wallx+.65,y-3.2,1.75),target=(wallx,y,1.7),lens=58,aspect=1.25),
        foundation=dict(location=(x+1.7,y-4.0,1.1),target=(x,y-.35,.55),lens=48,aspect=1.5),
        concrete=dict(location=(m['x0']+1.02,y-4,.19),target=(m['x0']+1.02,y,.19),ortho=1.22,aspect=3.6),
        peeling=dict(location=(sx+.38,y-1.28,sz+.45),target=(sx,y,sz+.03),lens=58,aspect=1.4),
        tired=dict(location=(m['x0']+2.6,m['y1']+5.2,m['eave']+4.5),target=(m['x0']+2,m['y1']-1.0,m['eave']+m['pitch']),lens=55,aspect=1.4),
        connector=dict(location=(bx+(-3.2 if bx<(m['x0']+m['x1'])/2 else 3.2),by-4.6,2.2),target=(bx,by+.7,1.35),lens=45,aspect=1.4),
        side=dict(location=(60,cy,4),target=(cx,cy,3.7),ortho=max(14,hi.y-lo.y+2),aspect=1.65),
        top=dict(location=(cx,cy,65),target=(cx+.001,cy,0),ortho=max(14,w+2,hi.y-lo.y+2),aspect=1.2))
    chimney=bpy.data.objects.get('Brick_Chimney')
    if chimney:
        pts=[chimney.matrix_world@v.co for v in chimney.data.vertices]
        target=Vector(tuple((min(p[k] for p in pts)+max(p[k] for p in pts))/2 for k in range(3)))
        target.z=max(p.z for p in pts)-.5
        shots['chimney']=dict(location=tuple(target+Vector((2,-3,1.4))),target=tuple(target),lens=52,aspect=1.25)
    elif meta.get('chimney_camera'):shots['chimney']=meta['chimney_camera']
    return shots


def load_context(path,offset):
    before=set(bpy.context.scene.objects)
    group=bpy.data.node_groups.get('glTF Material Output')
    if group:group.name='CapeSource_Occlusion'
    if path.suffix=='.gltf':bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    else:
        with bpy.data.libraries.load(str(path.resolve()),link=False) as (src,dst):dst.objects=src.objects
        for ob in dst.objects:
            if ob and ob.name not in bpy.context.scene.objects:bpy.context.scene.collection.objects.link(ob)
    imported=set(bpy.context.scene.objects)-before
    for ob in imported:
        if ob.parent not in imported:ob.location.x+=offset
    from delivery_io import bundle_hash
    return dict(path=str(path),sha256=bundle_hash(path) if path.suffix=='.gltf' else hashlib.sha256(path.read_bytes()).hexdigest(),offset_m=offset)


def render(source,out,names,width=1200,samples=32,camera_file=None,types=False,engine='CYCLES'):
    from delivery_io import bundle_hash
    if source.suffix=='.gltf':
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()));digest=bundle_hash(source)
    else:
        bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));digest=hashlib.sha256(source.read_bytes()).hexdigest()
    meta=json.loads(source.with_suffix('.json').read_text())
    mats={bpy.path.abspath(im.filepath):hashlib.sha256(Path(bpy.path.abspath(im.filepath)).read_bytes()).hexdigest() for im in bpy.data.images if im.filepath and Path(bpy.path.abspath(im.filepath)).is_file()}
    camera=setup(engine,samples);reflection_scenery(meta);shots=views(meta);context=[]
    if types:
        # Equal meters and one shared orthographic projection. Context loaded
        # read-only from accepted family exports, or source fallback on a clone.
        colonial=Path('export/Hearthfield-27.gltf');ranch=Path('export/HearthfieldRanch-12.gltf')
        context.append(load_context(ranch if ranch.exists() else Path('build/ranch/house-12.blend'),-22))
        context.append(load_context(colonial if colonial.exists() else Path('build/lookdev.blend'),22))
        shots=dict(types=dict(location=(0,-80,15),target=(0,0,3.6),ortho=68,aspect=3.3))
    if camera_file:shots={n:d['shot'] for n,d in json.loads(camera_file.read_text()).items()}
    figures=human((meta['door_x']+1.5,meta['blocks'][0]['y0']-.55,0))
    out.mkdir(parents=True,exist_ok=True);reports=json.loads((out/'provenance.json').read_text()) if (out/'provenance.json').exists() else {}
    for name in names.split(','):
        shot=shots[name];camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0))
        camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.lens=shot.get('lens',45)
        if 'ortho' in shot:camera.data.ortho_scale=shot['ortho']
        for ob in figures:ob.hide_render=not shot.get('human',False)
        sc=bpy.context.scene;sc.render.resolution_x=width;sc.render.resolution_y=round(width/shot.get('aspect',1.5));sc.render.resolution_percentage=100
        sc.view_settings.exposure=shot.get('exposure',-.35);sc.render.film_transparent=shot.get('background')=='transparent'
        # Controlled daylight: enough front sun to read roof/cheek construction,
        # restrained sky fill preserves the low eave and entry cavities.
        bpy.data.objects['Afternoon sun'].rotation_euler=Vector((.5,.8,-1)).to_track_quat('-Z','Y').to_euler()
        next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=.12
        sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        reports[name]=dict(source=str(source),source_sha256=digest,metadata_sha256=hashlib.sha256(source.with_suffix('.json').read_bytes()).hexdigest(),material_sha256=mats,render_recipe_sha256=recipe_sha(),seed=meta['seed'],engine=engine,stage=meta['stage'],camera=shot,context=context,lighting=dict(sun_direction=(.5,.8,-1),sky_strength=.12,exposure_ev=sc.view_settings.exposure))
        if name=='hero':tonal(out/'hero.png',camera)
    (out/'provenance.json').write_text(json.dumps(reports,indent=2))


def tonal(path,camera):
    from PIL import Image,ImageDraw
    from bpy_extras.object_utils import world_to_camera_view
    import numpy as np
    im=Image.open(path).convert('RGB');mask=Image.new('L',im.size);draw=ImageDraw.Draw(mask);sc=bpy.context.scene
    for ob in sc.objects:
        if ob.type!='MESH' or not ob.get('asset_set'):continue
        points=[]
        for v in ob.data.vertices:
            p=world_to_camera_view(sc,camera,ob.matrix_world@v.co);points.append((p.x*im.width,(1-p.y)*im.height))
        ob.data.calc_loop_triangles()
        for t in ob.data.loop_triangles:draw.polygon([points[i] for i in t.vertices],fill=255)
    rgb=np.asarray(im)[np.asarray(mask)>0]/255;lum=rgb@np.array([.2126,.7152,.0722]);out=dict(zip(('p1','p50','p95','p99'),map(float,np.quantile(lum,[.01,.5,.95,.99]))));out['clipped_white_fraction']=float(np.mean(np.min(rgb,axis=1)>.985));path.with_name('tonal.json').write_text(json.dumps(out,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=36);p.add_argument('--source',type=Path);p.add_argument('--out',type=Path,default=Path('renders/cape/checkpoint'));p.add_argument('--shots',default='hero,back,roof,dormer,eave,entry,scale');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=48);p.add_argument('--camera-file',type=Path);p.add_argument('--types',action='store_true');p.add_argument('--family',action='store_true');p.add_argument('--seeds',default='31,32,33,34,35,36')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);render(a.source or Path(f'build/cape/house-{a.seed}.blend'),a.out,a.shots,a.width,a.samples,a.camera_file,a.types)
    if a.family:
        for seed in map(int,a.seeds.split(',')):render(Path(f'build/cape/house-{seed}.blend'),a.out/'seeds'/str(seed),'front,rear',min(a.width,1200),a.samples)
