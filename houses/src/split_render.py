"""Cycles source look views and calibrated pairs, with cut grade for the drive."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from render import setup,human,simple
from cape_render import load_context,tonal
from plan import subtract
from cape_reflections import scenery as reflection_scenery


def recipe_sha():
    paths=[HERE/name for name in ('split_render.py','render.py','cape_reflections.py','ranch_render.py')]
    return hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in paths)).hexdigest()


def grade(meta):
    old=bpy.data.objects.get('Presentation grade, excluded from asset')
    if old:bpy.data.objects.remove(old,do_unlink=True)
    # Lawn is presentation only. Cut a real slot so the sloped drive remains
    # visible below grade; it is never painted over a flat ground plane.
    d=meta['driveway'];w=d['width']/2+.27
    back=d['back']+6.20 if meta['spec']['garage']['kind']=='integral' else d['back']+.12
    parts=subtract([(-1000,-1000),(1000,-1000),(1000,1000),(-1000,1000)],[(1,0,-d['x']+w),(-1,0,d['x']+w),(0,1,-d['front']),(0,-1,back)])
    for o in meta['openings']:
        if not o.get('well'):continue
        b=next(v for v in meta['blocks'] if v['name']==o['block'])
        if o['face']=='back':
            x=b['x0']+o['u'];rect=(x-o['w']/2-.22,x+o['w']/2+.22,b['y1']-.02,b['y1']+.59)
        else:
            y=b['y0']+o['u'];xx=b['x0'] if o['face']=='left' else b['x1'];sign=-1 if o['face']=='left' else 1
            rect=(min(xx,xx+sign*.59),max(xx,xx+sign*.59),y-o['w']/2-.22,y+o['w']/2+.22)
        a,c,e,f=rect;cuts=[(1,0,-a),(-1,0,c),(0,1,-e),(0,-1,f)]
        parts=[p for q in parts for p in subtract(q,cuts)]
    vs=[];fs=[]
    for p in parts:
        off=len(vs);vs.extend((x,y,meta['spec'].get('site_grade_m',0)-.006) for x,y in p);fs.append(tuple(range(off,off+len(p))))
    me=bpy.data.meshes.new('ReviewGrade');me.from_pydata(vs,[],fs);ob=bpy.data.objects.new('ReviewGrade',me);bpy.context.collection.objects.link(ob);me.materials.append(simple('Review grade',(.14,.16,.105)))


def views(meta):
    m=meta['blocks'][0];wing=next((b for b in meta['blocks'] if b['name']=='Wing'),m)
    structural=[b for b in meta['blocks']];x0=min(b['x0'] for b in structural);x1=max(b['x1'] for b in structural)
    width=x1-x0+2;cx=(x0+x1)/2;y=m['y0'];lv=meta['levels'];door=meta['door_x']
    gx=meta['driveway']['x'];gy=meta['driveway']['back'];side=-1 if meta['spec']['wing']['side']=='left' else 1
    picture=next(o for o in meta['openings'] if o['role']=='living picture');px=m['x0']+picture['u'];pz=picture['z']+picture['h']/2
    if meta['spec']['kind']=='foyer':vx=m['x0']+(m['x1']-m['x0'])*.34;vy=m['y0'];vz=.55
    elif meta['spec']['cladding']['Main']['front']=='veneer':vx=m['x0']+.80;vy=m['y0'];vz=m['floor']+.40
    else:vx=(wing['x0']+wing['x1'])/2;vy=wing['y0'];vz=.50
    sx=(wing['x0']+wing['x1'])/2
    if meta['spec']['kind']=='foyer':sx=m['x0']+(m['x1']-m['x0'])*.35
    old_sash=next(o for o in meta['openings'] if o['kind']=='window' and o['face']=='front' and o['block']==wing['name'] and o['z']>=lv['upper']+.4)
    sill_x=wing['x0']+old_sash['u'];sill_z=old_sash['z']
    top_y=(meta['bounds'][0][1]+meta['bounds'][1][1])/2
    top_width=max(width+2,(meta['bounds'][1][1]-meta['bounds'][0][1]+2)*1.2)
    return dict(
        hero=dict(location=(cx+side*width*.74,y-width*1.30,6.2),target=(cx,0,2.1),lens=43,aspect=1.65),
        front=dict(location=(cx,-70,6.2),target=(cx,0,2.7),ortho=width,aspect=max(1.7,width/9)),
        rear=dict(location=(cx,70,6.2),target=(cx,0,2.7),ortho=width,aspect=max(1.7,width/9)),
        back=dict(location=(cx-width*.8,28,9),target=(cx,0,2.1),lens=42,aspect=1.65),
        side=dict(location=(x1+60,0,5.8),target=(cx,0,2.8),ortho=16,aspect=1.6),
        levels=dict(location=(cx+side*width*.65,y-width*1.2,3.7),target=(cx,y+1.2,2.1),lens=48,aspect=1.8),
        entry=dict(location=(door+2.3,y-5.2,2.5),target=(door,y-.3,lv['living']+1.05),lens=48,aspect=1.3),
        eave=dict(location=(wing['x1']+1.8,wing['y0']-3.0,2.4),target=(wing['x1']-.15,wing['y0']-.02,wing['eave']-.06),lens=46,aspect=1.3),
        veneer=dict(location=(wing['x0']+1.1,wing['y0']-3.4,lv['upper']+.5),target=(wing['x0']+1.5,wing['y0'],lv['upper']-.16),lens=60,aspect=1.3),
        garage=dict(location=(gx+2.7,gy-6.5,2.0),target=(gx,gy,meta['driveway']['back_z']+1.2),lens=44,aspect=1.5),
        garage_half=dict(location=(gx+2.7,gy-6.5,2.0),target=(gx,gy,meta['driveway']['back_z']+1.2),lens=44,aspect=1.5,garage_progress=.5),
        garage_open=dict(location=(gx+2.7,gy-6.5,2.0),target=(gx,gy,meta['driveway']['back_z']+1.2),lens=44,aspect=1.5,garage_progress=1),
        roof=dict(location=(cx+12,-15,26),target=(cx,0,2.5),lens=42,aspect=1.5),
        top=dict(location=(cx,top_y,65),target=(cx+.001,top_y,0),ortho=top_width,aspect=1.2),
        scale=dict(location=(door+3,y-11,2.8),target=(door,y-.3,lv['living']+1.0),lens=43,aspect=1.5,human=True),
        siding=dict(location=(sx+1.1,wing['y0']-3.2,lv['upper']+.80),target=(sx,wing['y0'],lv['upper']+.55),lens=60,aspect=1.3),
        veneer_face=dict(location=(vx+1.2,vy-3.5,vz+.6),target=(vx,vy,vz),lens=60,aspect=1.4),
        tired=dict(location=(wing['x1']+2.5,wing['y1']+6.0,wing['eave']+4.0),target=((wing['x0']+wing['x1'])/2,wing['y1']-1.3,wing['eave']+wing['pitch']*1.3),lens=52,aspect=1.4),
        driveway=dict(location=(gx+3.7,gy-7,6),target=(gx,gy-3.1,meta['driveway']['back_z']),lens=52,aspect=1.4),
        bay=dict(location=(px+2.8,y-4.4,pz+.7),target=(px,y-.15,pz),lens=52,aspect=1.4),
        peeling=dict(location=(sill_x+.35,wing['y0']-1.8,sill_z+.65),target=(sill_x,wing['y0']-.12,sill_z+.05),lens=65,aspect=1.6),
        lower=dict(location=(m['x0']+(m['x1']-m['x0'])*.19,y-5.4,.8),target=(m['x0']+(m['x1']-m['x0'])*.19,y,.35),lens=48,aspect=1.5))


def render(source,out,names='hero',width=1200,samples=32,camera_file=None,types=False,engine='CYCLES',clay=False):
    context_paths=None
    if types:
        from split_context import ensure
        context_paths=ensure()
    if source.suffix=='.gltf':
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
        from delivery_io import bundle_hash
        digest=bundle_hash(source)
    else:
        bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));digest=hashlib.sha256(source.read_bytes()).hexdigest()
    meta=json.loads(source.with_suffix('.json').read_text())
    maps={str(Path(bpy.path.abspath(i.filepath)).resolve()):hashlib.sha256(Path(bpy.path.abspath(i.filepath)).read_bytes()).hexdigest() for i in bpy.data.images if i.filepath and Path(bpy.path.abspath(i.filepath)).is_file()}
    if clay:
        finish=simple('Neutral construction clay',(.36,.36,.34));dark=simple('Clay opening depth',(.012,.014,.014))
        for ob in bpy.context.scene.objects:
            if ob.type=='MESH' and ob.get('asset_set'):
                for i,mat in enumerate(ob.data.materials):ob.data.materials[i]=dark if 'Glass' in mat.name else finish
    camera=setup(engine,samples);grade(meta);shots=views(meta);context=[]
    if not clay:reflection_scenery(meta)
    if types:
        for kind,offset in [('cape',-46),('ranch',-22),('builder_colonial',25)]:context.append(load_context(context_paths[kind],offset))
        shots=dict(types=dict(location=(-9,-100,18),target=(-9,0,3),ortho=102,aspect=4.6))
    if camera_file:shots={n:d['shot'] for n,d in json.loads(camera_file.read_text()).items()}
    figures=human((door:=meta['door_x']-1.5,meta['blocks'][0]['y0']-1.6,0))
    sc=bpy.context.scene;out.mkdir(parents=True,exist_ok=True)
    reports=json.loads((out/'provenance.json').read_text()) if (out/'provenance.json').exists() else {}
    for name in names.split(','):
        shot=shots[name];camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0))
        if 'garage_progress' in shot:
            from split_motion import pose
            pose(shot['garage_progress'])
        camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.lens=shot.get('lens',45)
        if 'ortho' in shot:camera.data.ortho_scale=shot['ortho']
        for ob in figures:ob.hide_render=not shot.get('human',False)
        sc.render.resolution_x=width;sc.render.resolution_y=round(width/shot.get('aspect',1.5));sc.render.resolution_percentage=100
        sc.render.film_transparent=shot.get('background')=='transparent';sc.view_settings.exposure=shot.get('exposure',-.35)
        sc.view_settings.use_white_balance=True;sc.view_settings.white_balance_temperature=6500
        bpy.data.objects['Afternoon sun'].rotation_euler=Vector((.5,.8,-1)).to_track_quat('-Z','Y').to_euler()
        next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=.12
        sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        reports[name]=dict(source=str(source),source_sha256=digest,metadata_sha256=hashlib.sha256(source.with_suffix('.json').read_bytes()).hexdigest(),map_sha256=maps,recipe_sha256=recipe_sha(),image_sha256=hashlib.sha256((out/(name+'.png')).read_bytes()).hexdigest(),width=width,samples=samples,camera=shot,context=context,stage=meta['stage'],engine=engine,clay=clay)
        if name=='hero':tonal(out/'hero.png',camera)
    (out/'provenance.json').write_text(json.dumps(reports,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=51);p.add_argument('--out',type=Path,default=Path('renders/split/checkpoint'));p.add_argument('--source',type=Path);p.add_argument('--shots',default='hero,back,levels,side,entry,eave,veneer,garage,roof,scale');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=48);p.add_argument('--camera-file',type=Path);p.add_argument('--types',action='store_true');p.add_argument('--family',action='store_true')
    p.add_argument('--clay',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    render(a.source or Path(f'build/split/house-{a.seed}.blend'),a.out,a.shots,a.width,a.samples,a.camera_file,a.types,clay=a.clay)
    if a.family:
        for seed in range(51,57):render(Path(f'build/split/house-{seed}.blend'),a.out/'seeds'/str(seed),'front,rear',min(a.width,1200),a.samples)
