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
    bg=ns.get('Background');bg.inputs['Strength'].default_value=.12;ls.new(sky.outputs[0],bg.inputs[0])
    ld=bpy.data.lights.new('Low raking sun','SUN');ld.energy=3.3;ld.angle=math.radians(.65);ld.color=(1,.94,.83)
    sun=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(sun);sun.rotation_euler=Vector((.75,.61,-.316)).to_track_quat('-Z','Y').to_euler()
    cam=bpy.data.objects.new('CheckpointCamera',bpy.data.cameras.new('CheckpointCamera'));sc.collection.objects.link(cam);sc.camera=cam
    cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL';cam.data.clip_start=.03;cam.data.clip_end=2000
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.5
    sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB'
    return cam


def context(plan):
    from site import getsitepackages # startup site remains untouched
    import importlib.util
    spec=importlib.util.spec_from_file_location('_render_terrain',HERE/'site.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
    lib=Library();W,D=plan['size'];ground=ROOT/'ground/export/Ground.glb'
    counts=dict(cars=0,vegetation=0,town_architecture=0,street=0);placements=[]
    def triangle_count(root):
        result=0
        for ob in [root,*root.children_recursive]:
            if ob.type=='MESH':ob.data.calc_loop_triangles();result+=len(ob.data.loop_triangles)
        return result
    turf=S.library_material(lib,'Lawn');asphalt=S.library_material(lib,'Asphalt')
    parent=bpy.data.objects.new('TownContext',None);bpy.context.collection.objects.link(parent)
    # Ground continues into the town, below the native park surface. There is
    # no plinth; the public street crosses both actual park connections.
    for x0,x1,y0,y1 in ((-600,-W/2,-600,600),(W/2,600,-600,600),(-W/2,W/2,-600,-D/2),(-W/2,W/2,D/2,600)):
        S.ground_box(parent,'Continuing town lawn',((x0+x1)/2,(y0+y1)/2,-.05),(x1-x0,y1-y0,.10),turf,3.048,(.78,.80,.64))
    for sy in (-1,1):
        y=sy*(D/2+3.65)
        for j in range(-23,24):
            r=lib.place(ground,'Public street',(j*6.096,y,-.00635),90,'Road_Straight_'+('ABC'[j%3]));counts['street']+=triangle_count(r)
        for j in range(-4,5):
            hp=ROOT/'houses/export'/('Hearthfield-2.gltf' if j%2 else 'Hearthfield-27.gltf')
            r=lib.place(hp,'Neighbor',(j*27+7,sy*(D/2+25),0),180 if sy<0 else 0);counts['town_architecture']+=triangle_count(r)
    for side in (-1,1):
        # Side neighbors have a public approach too; the neighborhood continues
        # around the park rather than ending in houses staged on a lawn.
        for j in range(-30,31):
            r=lib.place(ground,'Continuing side street',(side*(W/2+39),j*6.096,-.00635),0,'Road_Straight_'+('BCA'[j%3]));counts['street']+=triangle_count(r)
        for j in range(-2,3):
            hp=ROOT/'houses/export'/('Hearthfield-2.gltf' if j%2 else 'Hearthfield-27.gltf')
            r=lib.place(hp,'Beyond park boundary',(side*(W/2+21),j*27,0),-90 if side<0 else 90);counts['town_architecture']+=triangle_count(r)
    cars=[ROOT/'cars/export'/s for s in ('AlderC150.glb','AlderX220.glb','AlderH120.glb')]
    markers=[o for o in bpy.context.scene.objects if o.get('socket_kind') in ('car','tree','shrub')]
    for j,o in enumerate(markers):
        xf=o.matrix_world.copy();kind=o['socket_kind'];pos=xf.translation;yaw=math.degrees(xf.to_euler().z)
        if kind=='car':
            # Some driveways hold two vehicles, some one. Every occupied street
            # includes three native body types with varied factory paint.
            if 'CarportCar' in o.name and j%3==0:continue
            path=cars[int(o.get('vehicle_index',j%3))];r=lib.place(path,'Resident car '+str(j),pos,yaw)
            # Distribute colors independently of vehicle/lot seed modulo.
            # The leading pair deliberately uses Atlantic and Graphite.
            paint=(3,4,0,1,3,0,4,1,2)[len(placements)%9];lib.factory(r,paint)
        elif kind=='tree':
            species=o.get('species','maple');path=ROOT/'trees/export'/('PinOak.glb' if species=='oak' else 'RedMaple.glb')
            s=float(o.get('plant_scale',1));r=lib.place(path,'Yard tree '+str(j),pos,j*47,scale=(s,s,s))
        else:
            path=ROOT/'shrubs/export/Shrubs.glb';r=lib.place(path,'Yard planting '+str(j),pos,j*33,select='Hydrangea' if j%4==0 else 'Boxwood',scale=(.84,.84,.84))
        category='cars' if kind=='car' else 'vegetation'
        n=triangle_count(r)
        paint_names=sorted({slot.material.name for ob in r.children_recursive if ob.type=='MESH' for slot in ob.material_slots if slot.material and slot.material.name.startswith('Presentation factory')})
        counts[category]+=n;placements.append(dict(kind=kind,triangles=n,source=str(path.relative_to(ROOT)),position=list(pos),paint_materials=paint_names))
    for sy in (-1,1):
        for j in range(-6,7):
            r=lib.place(ROOT/'trees/export/RedMaple.glb','Town canopy',(j*23+10,sy*(D/2+12),0),j*61,scale=(1.03,1.03,1.03))
            counts['vegetation']+=triangle_count(r)
        for j in range(-3,4):
            r=lib.place(cars[(j+1)%3],'Street resident',(j*31,sy*(D/2+17),0),90 if sy<0 else -90);lib.factory(r,j);counts['cars']+=triangle_count(r)
    lib.clear();return dict(triangles=counts,placements=placements,dependencies=lib.dependencies)


def shot_views(stem,meta):
    p=meta['plan'];wide=stem.startswith('Double');L=p.get('length',10) if p else 10;W=p.get('width',5) if p else 5
    if stem.startswith('Park'):
        span=p['span'];sx,sy=p['size'];old=p['kind']=='old'
        return dict(hero=dict(location=(-1.50,-span/2-13,1.68) if old else (-17.5,-span/2-3,1.68),target=(-.4,-span/2+16,1.83) if old else (-24,-span/2+25,1.92),lens=40),
                    above=dict(location=(sx*1.02,-sy*1.05,max(sx,sy)*.95),target=(0,0,0),lens=43,aspect=1.45),
                    entrance=dict(location=(12,-span/2-23,1.68),target=(7,-span/2-16,1.4),lens=48,aspect=1.5))
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
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    bpy.context.view_layer.update()
    # Imported custom bone-display helpers never appear in product evidence.
    for o in list(bpy.context.scene.objects):
        if o.type=='MESH' and not o.data.materials and 'Icosphere' in o.name:bpy.data.objects.remove(o,do_unlink=True)
    ctx=context(meta['plan']) if stem.startswith('Park') and dress else {}
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
        sc.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=light.get('sky_strength',.12)
        sc.view_settings.exposure=light.get('exposure',-.5)
        if name=='scale':
            from kit.studio import human
            humans=human()
            for hh in humans:hh.location+=Vector((-meta['plan']['length']*.17,-meta['plan']['width']/2-1.1,0));temporary.append(hh)
            lib=Library();car=lib.place(ROOT/'cars/export/AlderH120.glb','Scale car',(meta['plan']['length']*.22,-meta['plan']['width']/2-2.7,0),90);lib.factory(car,1);lib.clear();temporary.append(car)
        cam.location=v['location'];cam.rotation_euler=(Vector(v['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.data.type='ORTHO' if 'ortho' in v else 'PERSP';cam.data.lens=v.get('lens',45);cam.data.ortho_scale=v.get('ortho',20)
        if v.get('roll'):cam.rotation_euler.rotate_axis('Z',v['roll'])
        sc.render.resolution_x=width;sc.render.resolution_y=round(width/v.get('aspect',1.78));sc.render.filepath=str((out/stem/(name+'.png')).resolve());Path(sc.render.filepath).parent.mkdir(parents=True,exist_ok=True)
        if not stem.startswith('Park') and name in ('hero','detail','front','back','side','top','scale'):
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
        provenance.append(dict(stem=stem,shot=name,camera=v,source=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),images=meta['images'],context=ctx,
                               light={**dict(sun_elevation_degrees=18,sun_energy=3.3,sky_strength=.12,exposure=-.5),**light},engine='CYCLES',width=width,samples=samples))
        for root in temporary:
            for o in [*root.children_recursive,root]:bpy.data.objects.remove(o,do_unlink=True)
        for pivot,rest in posed.items():pivot.matrix_basis=rest
    return provenance


def main():
    a=argparse.ArgumentParser();a.add_argument('--source');a.add_argument('--out',type=Path,default=Path('renders/checkpoint/pass1'));a.add_argument('--width',type=int,default=1200);a.add_argument('--samples',type=int,default=24);a.add_argument('--only',default='all');a.add_argument('--shots',default='all');a.add_argument('--cameras',type=Path);a.add_argument('--no-context',action='store_true');a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    stems=[*[k for k in json.loads(Path('build/family.json').read_text()) if k.startswith('Park-')],'SingleWide-120','DoubleWide-228','Deck','Carport','UtilityService','EntranceSign','Modules','HomeForms','SupportFrame'] if a.only=='all' else a.only.split(',')
    receipts=[]
    for stem in stems:
        path=Path('export')/(stem+'.gltf');meta=json.loads(path.with_suffix('.json').read_text());views=shot_views(stem,meta)
        if a.shots!='all':views={k:v for k,v in views.items() if k in a.shots.split(',')}
        if views:receipts+=render(stem,path,meta,views,a.out,a.width,a.samples,not a.no_context)
    if a.cameras and a.cameras.exists():
        from kit.photo_match import verify
        verify(a.cameras)
        for name,row in json.loads(a.cameras.read_text()).items():
            stem=row['asset'];meta=json.loads(Path('export',stem+'.json').read_text())
            v=row['shot'];v['aspect']=(row['crop'][2]-row['crop'][0])/(row['crop'][3]-row['crop'][1])
            v['light']=(dict(sun_energy=.55,sky_strength=.36,angle_degrees=12,direction=(.3,.3,-1),exposure=-.40) if name=='single-2009' else
                        dict(sun_energy=1.5,sky_strength=.26,angle_degrees=5,direction=(.6,.6,-1),exposure=-.5) if name=='addition-2007' else
                        dict(sun_energy=3.3,sky_strength=.16,angle_degrees=.65,direction=(.5,.5,-1),exposure=-.5))
            receipts+=render(stem,Path('export',stem+'.gltf'),meta,{name:v},a.out/'matches',a.width,a.samples,False)
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'provenance.json').write_text(json.dumps(receipts,indent=2));print('RENDERED',len(receipts),flush=True)

if __name__=='__main__':main()
