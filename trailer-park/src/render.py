"""Batched Cycles review from fresh external glTF imports, never source blends."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from geometry import Library,ROOT
from kit import gpu,model as G
from kit.tiling import world_uv


def setup(width,samples):
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True
    sc.cycles.transparent_max_bounces=24;sc.cycles.max_bounces=7
    sc.world=bpy.data.worlds.new('Clear afternoon');sc.world.use_nodes=True
    ns,ls=sc.world.node_tree.nodes,sc.world.node_tree.links
    sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(18);sky.sun_rotation=math.radians(235);sky.sun_disc=False;sky.aerosol_density=.45
    bg=ns.get('Background');bg.inputs['Strength'].default_value=.24;ls.new(sky.outputs[0],bg.inputs[0])
    ld=bpy.data.lights.new('Low raking sun','SUN');ld.energy=3.3;ld.angle=math.radians(.65);ld.color=(1,.94,.83)
    sun=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(sun);sun.rotation_euler=Vector((.75,.61,-.316)).to_track_quat('-Z','Y').to_euler()
    cam=bpy.data.objects.new('CheckpointCamera',bpy.data.cameras.new('CheckpointCamera'));sc.collection.objects.link(cam);sc.camera=cam
    cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL';cam.data.clip_start=.03;cam.data.clip_end=2000
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.25
    sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB'
    return cam


def context(plan):
    from town_context import context as town
    return town(plan)


def image_resources():
    """Content-deduplicated images bound by the visible presentation meshes."""
    materials={slot.material for ob in bpy.context.scene.objects if ob.type=='MESH' and not ob.hide_render
               for slot in ob.material_slots if slot.material};images=set();seen=set()
    def visit(tree):
        if tree in seen:return
        seen.add(tree)
        for node in tree.nodes:
            if node.type=='TEX_IMAGE' and node.image:images.add(node.image)
            elif node.type=='GROUP' and node.node_tree:visit(node.node_tree)
    for mat in materials:
        if mat.use_nodes:visit(mat.node_tree)
    result={}
    for im in images:
        data=im.packed_file.data if im.packed_file else Path(bpy.path.abspath(im.filepath)).read_bytes()
        sha=hashlib.sha256(data).hexdigest();w,h=im.size[:]
        result[sha]=dict(name=im.name,sha256=sha,size=[w,h],png_bytes=len(data),mipped_8bpp_mib=w*h*4/3/1048576)
    return sorted(result.values(),key=lambda row:row['sha256'])


def shot_views(stem,meta):
    p=meta['plan'];wide=stem.startswith('Double');L=p.get('length',10) if p else 10;W=p.get('width',5) if p else 5
    if stem.startswith('Park'):
        span=p['span'];sx,sy=p['size'];old=p['kind']=='old'
        xx=p['loop_x']
        return dict(hero=dict(location=(-xx-1.50,-span/2+2,1.68),target=(-xx-.3,-span/2+31,1.83),lens=40),
                    above=dict(location=(sx*1.02,-sy*1.05,max(sx,sy)*.95),target=(0,0,0),lens=43,aspect=1.45,light=dict(exposure=0,sky_strength=.28)),
                    entrance=dict(location=(-xx+11,-span/2-19,1.68),target=(-xx+6,-span/2-7,1.4),lens=48,aspect=1.5),
                    row=dict(location=(-xx+2.3,-span/2+15,1.68),target=(-xx-12,-span/2+23,1.8),lens=40))
    if stem.startswith(('Single','Double')):
        return dict(hero=dict(location=(L*.92,-L*1.14,3.6),target=(0,0,1.7),lens=42),
                    front=dict(location=(0,-40,1.8),target=(0,0,1.8),ortho=L+2.7,aspect=2.1),
                    side=dict(location=(40,0,1.9),target=(0,0,1.9),ortho=W+2.0,aspect=1.25),
                    back=dict(location=(0,40,1.8),target=(0,0,1.8),ortho=L+2.7,aspect=2.1),
                    top=dict(location=(0,0,45),target=(0,0,0),ortho=L+2.7,aspect=1.6),
                    skirt=dict(location=(2.7,-W/2-2.4,.78),target=(1.8,-W/2,.50),lens=48,aspect=1.5),
                    entry=dict(location=(-L*.035+1.7,-W/2-3.5,1.8),target=(-L*.035,-W/2,1.8),lens=48,aspect=1.3,door_angles=dict(FrontDoor=48,StormDoor=-67)),
                    scale=dict(location=(L*.76,-L*.92,2.5),target=(0,-1.0,1.35),lens=42))
    presets={
      'Deck':((4,-6,2.5),(0,-.1,.80),48),
      'Carport':((7,-7,3.3),(0,0,1.4),45),
      'UtilityService':((1.8,-2.8,1.55),(.2,0,.75),52),
      'SupportFrame':((12,-8,2.3),(0,0,.43),45),
      'EntranceSign':((3.2,-5.7,2.0),(0,0,1.1),50),
      'Modules':((24,-42,37),(0,4,0),45),
      'HomeForms':((45,-78,76),(0,10,1),45)}
    loc,target,lens=presets.get(stem,((3,-5,2),(0,0,.6),45))
    out=dict(detail=dict(location=loc,target=target,lens=lens,aspect=1.6))
    if stem=='SupportFrame':out['piers']=dict(location=(1.5,-2.6,1.05),target=(0,-.94,.35),lens=55,aspect=1.5)
    return out


def render(stem,path,meta,views,out,width,samples,dress=True):
    from inspection import mirror
    delivery=path;packed=mirror(path);archive=(out.parent if out.name=='matches' else out)/'sources'/(stem+'.glb')
    archive.parent.mkdir(parents=True,exist_ok=True)
    if not archive.exists() or archive.read_bytes()!=packed.read_bytes():archive.write_bytes(packed.read_bytes())
    path=archive
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    bpy.context.view_layer.update()
    # Imported custom bone-display helpers never appear in product evidence.
    for o in list(bpy.context.scene.objects):
        if o.type=='MESH' and not o.data.materials and 'Icosphere' in o.name:bpy.data.objects.remove(o,do_unlink=True)
    ctx=context(meta['plan']) if stem.startswith('Park') and dress else {}
    if ctx:
        ctx['image_resources']=image_resources()
        ctx['image_gpu_mib']=sum(im['mipped_8bpp_mib'] for im in ctx['image_resources'])
    cam=setup(width,samples);sc=bpy.context.scene
    if not stem.startswith('Park'):
        from kit.studio import studio_mat
        G.box('Review ground',(0,0,-.10),(1000,1000,.20),studio_mat('Ground',(.13,.14,.11),.95),0)
    provenance=[]
    for name,v in views.items():
        temporary=[];posed={}
        for suffix,angle in v.get('door_angles',{}).items():
            pivot=next(o for o in bpy.context.scene.objects if o.name.endswith('__'+suffix));posed[pivot]=pivot.matrix_basis.copy();pivot.matrix_basis=posed[pivot]@Matrix.Rotation(math.radians(angle),4,'Z')
        light=v.get('light',{})
        sun=bpy.data.objects['Low raking sun'];sun.data.energy=light.get('sun_energy',3.3);sun.data.angle=math.radians(light.get('angle_degrees',.65))
        sun.rotation_euler=Vector(light.get('direction',(.75,.61,-.316))).to_track_quat('-Z','Y').to_euler()
        sc.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=light.get('sky_strength',.24)
        sc.view_settings.exposure=light.get('exposure',-.25)
        if name=='scale':
            from kit.studio import human
            humans=human()
            for hh in humans:hh.location+=Vector((-meta['plan']['length']*.17,-meta['plan']['width']/2-1.1,0));temporary.append(hh)
            lib=Library();car=lib.place(ROOT/'cars/export/AlderH120.glb','Scale car',(meta['plan']['length']*.22,-meta['plan']['width']/2-2.7,0),90);lib.factory(car,1);lib.clear();temporary.append(car)
        cam.location=v['location'];cam.rotation_euler=(Vector(v['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.data.type='ORTHO' if 'ortho' in v else 'PERSP';cam.data.lens=v.get('lens',45);cam.data.ortho_scale=v.get('ortho',20)
        if v.get('roll'):cam.rotation_euler.rotate_axis('Z',v['roll'])
        sc.render.resolution_x=width;sc.render.resolution_y=round(width/v.get('aspect',1.78));sc.render.filepath=str((out/stem/(name+'.png')).resolve());Path(sc.render.filepath).parent.mkdir(parents=True,exist_ok=True)
        if not v.get('fixed_camera') and not stem.startswith('Park') and name in ('hero','detail','front','back','side','top','scale'):
            from bpy_extras.object_utils import world_to_camera_view
            lo,hi=meta['bounds_min'],meta['bounds_max'];corners=[Vector((x,y,z)) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])]
            bpy.context.view_layer.update()
            for rt in temporary:
                for ob in [rt,*rt.children_recursive]:
                    if ob.type=='MESH':corners.extend(ob.matrix_world@Vector(c) for c in ob.bound_box)
            center=Vector(v['target'])
            for _ in range(30):
                bpy.context.view_layer.update();projections=[world_to_camera_view(sc,cam,p) for p in corners]
                if all(.035<q.x<.965 and .035<q.y<.965 and q.z>0 for q in projections):break
                if cam.data.type=='ORTHO':cam.data.ortho_scale*=1.06
                else:cam.location=center+(cam.location-center)*1.06
            v=dict(v,location=list(cam.location),ortho=cam.data.ortho_scale) if cam.data.type=='ORTHO' else dict(v,location=list(cam.location))
        bpy.ops.render.render(write_still=True)
        provenance.append(dict(stem=stem,shot=name,camera=v,source=str(path),delivery=str(delivery),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),images=meta['images'],context=ctx,
                               light={**dict(sky_sun_elevation_degrees=18,sun_elevation_degrees=math.degrees(math.asin(-Vector(light.get('direction',(.75,.61,-.316))).normalized().z)),sun_energy=3.3,sky_strength=.24,exposure=-.25),**light},engine='CYCLES',width=width,samples=samples))
        for root in temporary:
            for o in [*root.children_recursive,root]:bpy.data.objects.remove(o,do_unlink=True)
        for pivot,rest in posed.items():pivot.matrix_basis=rest
    return provenance


def main():
    a=argparse.ArgumentParser();a.add_argument('--source');a.add_argument('--out',type=Path,default=Path('renders/checkpoint/pass1'));a.add_argument('--width',type=int,default=1200);a.add_argument('--samples',type=int,default=24);a.add_argument('--only',default='all');a.add_argument('--shots',default='all');a.add_argument('--cameras',type=Path);a.add_argument('--before-cameras',type=Path);a.add_argument('--no-context',action='store_true');a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    stems=[*[k for k in json.loads(Path('build/family.json').read_text()) if k.startswith('Park-')],'SingleWide-120','DoubleWide-228','Deck','Carport','UtilityService','EntranceSign','Modules','HomeForms','SupportFrame'] if a.only=='all' else a.only.split(',')
    receipts=[]
    for stem in stems:
        path=Path('export')/(stem+'.gltf');meta=json.loads(path.with_suffix('.json').read_text());views=shot_views(stem,meta)
        if a.shots!='all':views={k:v for k,v in views.items() if k in a.shots.split(',')}
        if a.before_cameras and a.before_cameras.exists():
            for row in json.loads(a.before_cameras.read_text()):
                if row['stem']==stem and row['shot'] in ('hero','above'):
                    oldlight={k:v for k,v in row['light'].items() if k in ('sun_energy','sky_strength','exposure','direction','angle_degrees')}
                    views['before_'+row['shot']]=dict(row['camera'],fixed_camera=True,light=oldlight)
                if stem=='Park-101' and row['shot'] in ('single-2009','addition-2007','carport-2015'):
                    from park_matches import transform
                    number={'single-2009':3,'addition-2007':5,'carport-2015':2}[row['shot']]
                    lot=next(q for q in meta['plan']['lots'] if q['number']==number);h=lot['home']
                    offset=(0,0,0) if row['shot']=='single-2009' else (-h['length']*.32,-h['width']/2-1.2,0) if row['shot']=='addition-2007' else (h['length']/2-2.9,-h['width']/2-1.82,0)
                    camera=dict(row['camera']);camera.update(location=transform(lot,camera['location'],offset),target=transform(lot,camera['target'],offset),
                        fixed_camera=True,light=row['camera'].get('light',{}),baseline_reference=dict(stem=row['stem'],shot=row['shot'],camera=row['camera'],module_frame=True))
                    views['before_'+row['shot']]=camera
        if views:receipts+=render(stem,path,meta,views,a.out,a.width,a.samples,not a.no_context)
    if a.cameras and a.cameras.exists():
        from kit.photo_match import verify
        verify(a.cameras)
        for name,row in json.loads(a.cameras.read_text()).items():
            stem=row['asset'];meta=json.loads(Path('export',stem+'.json').read_text())
            v=row['shot'];v['aspect']=(row['crop'][2]-row['crop'][0])/(row['crop'][3]-row['crop'][1])
            v['light']=(dict(sun_energy=.55,sky_strength=.36,angle_degrees=12,direction=(.3,.3,-1),exposure=-.40) if name=='single-2009' else
                        dict(sun_energy=1.5,sky_strength=.26,angle_degrees=5,direction=(.6,.6,-1),exposure=-.5) if name=='street-2007' else
                        dict(sun_energy=3.3,sky_strength=.16,angle_degrees=.65,direction=(.5,.5,-1),exposure=-.5))
            receipts+=render(stem,Path('export',stem+'.gltf'),meta,{name:v},a.out/'matches',a.width,a.samples,True)
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'provenance.json').write_text(json.dumps(receipts,indent=2));print('RENDERED',len(receipts),flush=True)

if __name__=='__main__':main()
