"""Eye-height raking-sun checkpoint views, always imported external glTF."""
import argparse,sys,json,math,hashlib,inspect
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];sys.path[:0]=[str(REPO),str(HERE)]
RECIPE_SHA256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
import geometry as Q
from kit import gpu,tiling
from plan import SEEDS


def bundle(path):
    p=Path(path);d=json.loads(p.read_text());files=[p]+[p.parent/r['uri'] for k in ('buffers','images') for r in d.get(k,[]) if r.get('uri')]
    return hashlib.sha256(b''.join(hashlib.sha256(f.read_bytes()).digest() for f in files)).hexdigest()


def setup(samples):
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.eevee.taa_render_samples=samples
    sc.world=bpy.data.worlds.new('Procedural midsummer sky');sc.world.use_nodes=True;nt=sc.world.node_tree
    n=nt.nodes.new('ShaderNodeTexSky');n.sky_type='MULTIPLE_SCATTERING';n.sun_disc=False;n.aerosol_density=.35;n.sun_elevation=math.radians(24);n.sun_rotation=math.radians(215)
    bg=nt.nodes.get('Background');nt.links.new(n.outputs[0],bg.inputs['Color']);bg.inputs['Strength'].default_value=.16
    sun=bpy.data.objects.new('Raking sun',bpy.data.lights.new('Raking sun','SUN'));sc.collection.objects.link(sun)
    sun.data.energy=7.5;sun.data.angle=math.radians(.75);sun.rotation_euler=Vector((-.15,.9,-.40)).to_track_quat('-Z','Y').to_euler()
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.35
    cam=bpy.data.objects.new('CheckpointCamera',bpy.data.cameras.new('CheckpointCamera'));sc.collection.objects.link(cam);sc.camera=cam
    cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.data.clip_start=.015;cam.data.clip_end=1200
    return cam


def load(path,name):
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(Path(path).resolve()))
    added=set(bpy.context.scene.objects)-before;rt=Q.root(name,'presentation context')
    for o in added:
        if o.parent not in added:o.parent=rt
    return rt


def context(p):
    """Native library beyond the fence; presentation context is separately costed."""
    Q.palette();W,D=p['size'];rt=Q.root('NeighborhoodContext','presentation context')
    for n in ('Asphalt','Concrete'):Q.M[n]=tiling.material(n,REPO/'ground/textures/ship')
    import groundcover
    Q.M['Lawn']=groundcover.material(REPO)
    o=Q.box('Neighborhood ground',(0,0,-.12),(500,500,.16),rt,'Lawn');tiling.world_uv(o,3.048)
    # Native urban/site construction swatches stay on the same shared atlas.
    Q.finishes()
    road_y=-D/2-8.6
    Q.box('Street asphalt',(0,road_y,-.052),(220,7.3152,.08),rt,'Asphalt')
    for side in (-1,1):
        Q.box('Street concrete curb',(0,road_y+side*3.9,.015),(220,.15,.16),rt,'Concrete',.012)
        Q.box('Neighborhood sidewalk',(0,road_y+side*5.0,.01),(220,1.524,.09),rt,'Concrete')
        for x in range(-90,91,3):Q.box('Sidewalk expansion joint',(x,road_y+side*5,.057),(.009,1.524,.002),rt,'Soil')
    # Continuous approach from the gate to the neighbourhood sidewalk, with
    # an authored ~1.4% rise rather than a disconnected garden on a grass pad.
    w=p.get('main_width',1.524);y0=-D/2;y1=road_y+5.0+.762
    Q.mesh('Gate sidewalk approach',[(-w/2,y0,.014),(w/2,y0,.014),(w/2,y1,.055),(-w/2,y1,.055)],[(0,1,2,3)],rt,'Gravel')
    if p['archetype']!='city':groundcover.verge(p,rt)
    if p['archetype']=='city':
        house=load(REPO/'apartments/export/Building-301.gltf','NativeApartment')
        # Measured native 23.8 x 18.388 footprint; long facade runs down lot.
        for x,yaw in ((-W/2-10.8,90),(W/2+10.8,-90)):
            Q.instance(house,'Adjacent apartment',(x,2,-.02),yaw,rt)
        Q.instance(house,'Across street apartment',(35,road_y-16,-.02),180,rt)
        # Close the urban block across the rear service alley. Leaving this
        # gap open exposed the presentation ground's featureless horizon.
        Q.instance(house,'Across alley apartment',(0,D/2+15.5,-.02),0,rt)
    else:
        house=load(REPO/'houses/export/Hearthfield-27.gltf','NativeHouse')
        for j,x in enumerate((-36,-14,14,36,58)):
            Q.instance(house,'Neighborhood house',(x,road_y-22,-.03),180,rt)
        for x in ((W/2+17,) if p['archetype']=='park' else (-W/2-11,W/2+17)):Q.instance(house,'Side street house',(x,8 if x<0 else 15,-.03),90 if x<0 else -90,rt)
    for o in [*house.children_recursive,house]:bpy.data.objects.remove(o,do_unlink=True)
    rear=load(REPO/'houses/export/Hearthfield-27.gltf','NativeRearNeighbor')
    rear_positions={'city':[(-27,D/2+18),(25,D/2+23)],'park':[(-39,D/2+25),(-18,D/2+27),(4,D/2+24),(26,D/2+29),(48,D/2+25)],'accessible':[(-23,D/2+20),(0,D/2+24),(25,D/2+24)]}[p['archetype']]
    for j,(x,y) in enumerate(rear_positions):Q.instance(rear,'Rear block neighbor',(x,y,-.03),j*90,rt)
    for o in [*rear.children_recursive,rear]:bpy.data.objects.remove(o,do_unlink=True)
    if p['archetype']=='park':
        from park_hall import build as hall
        hall(rt,-W/2-6.9,13)
        Q.box('Hall walk connection',(-W/2-6.9,4.8,-.02),(2.0,6.5,.06),rt,'Gravel')
    if p['archetype']!='park':Q.box('Rear service alley',(0,D/2+3.5,-.052),(160,4.0,.08),rt,'Asphalt')
    tree=load(REPO/'trees/export/RedMaple.glb','NativeMaple')
    for i,(x,y) in enumerate(([(-8,D/2+8),(2,D/2+12),(11,D/2+10)] if p['archetype']=='park' else [])+[(-W/2-5,D/2+2),(W/2+6,D/2+4),(-W/2-5,-2),(W/2+7,-1),(-22,road_y-5.8),(23,road_y-5.8),(-W/2-2,D/2+12)]):
        if p['archetype']=='park' and -28<x<-13.8 and 8.4<y<17.6:x=-31
        Q.instance(tree,'Neighborhood tree',(x,y,-.035),i*67,rt)
    if p['archetype']=='park':
        for i in range(12):
            tree_copy=Q.instance(tree,'Park perimeter grove',(-45+i*8.1,D/2+18+(i%3)*2,-.035),i*137,rt)
            tree_copy.scale*=.80+.045*(i%5)
    if p['archetype']=='accessible':
        for i,x in enumerate((-5,3,11)):
            Q.instance(tree,'Rear garden canopy',(x,D/2+8+(i%2)*2,-.035),i*137+23,rt)
    # Shade bench, with a native tree rooted outside the cultivated plot area.
    bx,by=p['bench'];tree_location=(-9.9,D/2+1.8,-.04) if p['archetype']=='park' else (-W/2-1.5,by+1.8,-.04)
    Q.instance(tree,'Bench shade tree',tree_location,39,rt)
    for o in [*tree.children_recursive,tree]:bpy.data.objects.remove(o,do_unlink=True)
    car=load(REPO/'cars/export/AlderH120.glb','NativeCar')
    for i,x in enumerate((-13,13,33)):Q.instance(car,'Street parked car',(x,road_y+2.3,.0),90,rt)
    for o in [*car.children_recursive,car]:bpy.data.objects.remove(o,do_unlink=True)
    # Reuse actual utility pole assemblies; authored catenaries connect their
    # socket-height conductors. Never introduce new tree/pole construction.
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str((REPO/'utility/export/UtilityParts.gltf').resolve()))
    added=set(bpy.context.scene.objects)-before
    roots=[o for o in added if o.parent not in added]
    tangent=next((o for o in roots if 'tangent' in o.name.lower()),roots[0])
    for x in (-30,20,70):Q.instance(tangent,'Street utility pole',(x,road_y+4.0,0),0,rt)
    for r in roots:
        for o in [*r.children_recursive,r]:bpy.data.objects.remove(o,do_unlink=True)
    for z in (6.62,7.94,10.0):
        for xa,xb in ((-30,20),(20,70)):
            pts=[(xa+(xb-xa)*j/24,road_y+4.0,z-.8*math.sin(math.pi*j/24)) for j in range(25)]
            Q.tube('Utility catenary',pts,.009,rt,'Steel',4)
    bpy.context.view_layer.update()
    images={}
    for ob in [rt,*rt.children_recursive]:
        if ob.type!='MESH':continue
        for ma in ob.data.materials:
            if not ma or not ma.use_nodes:continue
            for node in ma.node_tree.nodes:
                if node.type=='TEX_IMAGE' and node.image:
                    im=node.image
                    if im.packed_file:key=hashlib.sha256(im.packed_file.data).hexdigest()
                    else:
                        path=Path(bpy.path.abspath(im.filepath));key=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else im.name
                    images[key]=dict(name=im.name,width=im.size[0],height=im.size[1])
    costs=dict(triangles=Q.count(rt),unique_images=len(images),images=list(images.values()),
               compressed_texture_mib=sum(r['width']*r['height']*4/3 for r in images.values())/2**20,
               scope='presentation-only native neighborhood, excluded from garden budget; 8bpp per map plus full mips, no geometry/engine overhead')
    Path('build/context').mkdir(parents=True,exist_ok=True)
    Path(f'build/context/costs-{p.get("seed",0)}.json').write_text(json.dumps(costs,indent=2))
    return rt


CONTEXT_SHA256=hashlib.sha256((inspect.getsource(context)+inspect.getsource(load)).encode()+b''.join((HERE/name).read_bytes() for name in ('geometry.py','groundcover.py','park_hall.py'))).hexdigest()

def views(p):
    W,D=p['size'];plot=p['plots'][0];x,y=plot['center'];cx,cy=p['compost'];wx,wy=p['water']
    out=dict(hero=dict(location=(-.45,-D/2-3.6,1.65),target=(0,3,.85),lens=38,aspect=1.65),
             above=dict(location=(0,0,40),target=(0,0,0),ortho=W*1.30,aspect=W/D),
             corner=dict(location=(x-plot['width']/2-.7,y-plot['depth']/2-.9,.75),target=(x-plot['width']/2+.06,y-plot['depth']/2+.08,.20),lens=48,aspect=1.5),
             compost=dict(location=(cx-2.7,cy-3.6,1.65),target=(cx,cy,.62),lens=45,aspect=1.5),
             water=dict(location=(wx-1.7,wy-2.3,1.15),target=(wx+.3,wy-.30,.43),lens=48,aspect=1.5))
    if p['archetype']=='park':out['hero'].update(location=(-.45,-D/2-3.6,1.65),target=(0,2,.9),lens=42)
    if p['archetype']=='accessible':
        out['hero'].update(location=(-2.8,-D/2-4.4,1.65),target=(.7,1,.7),lens=38)
        out['accessible']=dict(location=(-5.1,-8.3,1.3),target=(-3.048,-7.01,.55),lens=42,aspect=1.5)
    out['before-camera']=dict(out['hero'])
    # View through the physical open gate: no near wire plane crosses the frame.
    out['hero'].update(location=(0,-D/2+.55,1.65),target=({'city':(-.3,4,1.0),'park':(-6,3,1.0),'accessible':(-.2,3,.85)}[p['archetype']]),lens=35)
    if p['archetype']=='accessible':out['hero'].update(location=(.6,-D/2+.15,1.65),target=(-3.4,-5.2,.55),lens=35)
    if p['seed']==117:
        out['scale']=dict(location=(-.30,-9.0,1.65),target=(-2.13,-4.5,.85),lens=40,aspect=1.5,human=(-1.10,-4.74,0))
        out['eevee']=dict(out['hero'],engine='BLENDER_EEVEE')
    for sp in ('tomato','bean','squash'):
        options=[b for b in p['plots'] if b['crop']==sp and b['state'] not in ('fallow','new')]
        if options:
            q=options[0];x,y=q['center']
            if sp=='tomato':
                # The front specimen is caged in every plan, including beds
                # that demonstrate stakes on their remaining plants.
                specimen=next(p for p in q['plants'] if p['species']=='tomato')
                x+=specimen['local'][0];y+=specimen['local'][1]
            out[sp]=dict(location=(x-1.6,y-2.0,1.30),target=(x,y,.9),lens=52,aspect=1.3)
            if sp=='squash':out[sp]=dict(location=(x-1.2,y-1.8,1.55),target=(x,y,.45),lens=40,aspect=1.5)
            if sp=='bean':out[sp]=dict(location=(x-2.3,y-3.5,1.55),target=(x,y,1.25),lens=45,aspect=1.2)
    sx,sy=p['service']
    out['shed']=dict(location=(sx-3.8,sy-5,2.0),target=(sx,sy,1.1),lens=48,aspect=1.5)
    out['turf']=dict(location=(-1.2,-D/2+1.8,.62),target=(-2.3,-D/2+3.1,.025),lens=48,aspect=1.5)
    out['front']=dict(location=(0,-D/2-18,6),target=(0,0,0.9),ortho=W*1.25,aspect=1.6)
    out['side']=dict(location=(W/2+23,0,7),target=(0,0,1),ortho=D*1.25,aspect=1.6)
    out['back']=dict(location=(0,D/2+20,6),target=(0,0,1),ortho=W*1.25,aspect=1.6)
    return out


def shot(cam,v,path,width):
    sc=bpy.context.scene;cam.location=v['location'];cam.rotation_euler=(Vector(v['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
    if v.get('roll'):cam.rotation_euler.rotate_axis('Z',v['roll'])
    cam.data.type='ORTHO' if 'ortho' in v else 'PERSP';cam.data.ortho_scale=v.get('ortho',20);cam.data.lens=v.get('lens',40)
    sc.render.resolution_x=width;sc.render.resolution_y=round(width/v.get('aspect',1.5));sc.render.resolution_percentage=100
    sc.render.engine=v.get('engine','CYCLES');sc.view_settings.exposure=v.get('exposure',-.35)
    sun=bpy.data.objects.get('Raking sun')
    if v.get('overcast'):
        nt=sc.world.node_tree;sky=next(n for n in nt.nodes if n.type=='TEX_SKY')
        cloud=nt.nodes.get('Overcast neutral skylight') or nt.nodes.new('ShaderNodeHueSaturation');cloud.name='Overcast neutral skylight'
        cloud.inputs['Saturation'].default_value=.20;nt.links.new(sky.outputs['Color'],cloud.inputs['Color']);nt.links.new(cloud.outputs['Color'],nt.nodes['Background'].inputs['Color'])
    if sun:
        sun.data.energy=v.get('sun_energy',7.5);sun.data.angle=math.radians(v.get('sun_angle',.40))
        sun.rotation_euler=Vector(v.get('sun_direction',(-.15,.9,-.40))).to_track_quat('-Z','Y').to_euler()
        sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=v.get('sky_strength',.12)
    sc.render.image_settings.file_format='PNG';sc.render.filepath=str(Path(path).resolve());bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)


def render(seed,out,width,samples,names=None,custom=None,with_context=True,final=False):
    source=Path(f'export/final/Garden_{seed}.gltf');p=json.loads(Path(f'build/garden-{seed}.json').read_text())['plan']
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if with_context:
        import neighborhood as package
        source,receipt=package.prepare(seed,REPO,CONTEXT_SHA256,context)
        bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    if with_context:
        measured=sum(Q.count(o) for o in bpy.context.scene.objects if not o.parent)
        assert measured==json.loads(receipt.read_text())['triangles'],'Site re-import triangle count differs'
    cam=setup(samples)
    if not with_context:
        # Neutral inspection grade lets the side/back views show the garden
        # without the neighboring buildings occluding it. Asset meshes/maps
        # remain the imported export; this is presentation floor only.
        ma=bpy.data.materials.new('Neutral inspection ground');ma.use_nodes=True
        ma.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.12,.125,.11,1)
        ma.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.95
        floor=bpy.data.meshes.new('Inspection ground');floor.from_pydata([(-250,-250,-.011),(250,-250,-.011),(250,250,-.011),(-250,250,-.011)],[],[(0,1,2,3)])
        ob=bpy.data.objects.new('Neutral inspection grade',floor);sc=bpy.context.scene;sc.collection.objects.link(ob);floor.materials.append(ma)
    from kit.studio import human
    humans=human();rest={o:o.location.copy() for o in humans};out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for n,v in (custom or views(p)).items():
        if names and n not in names:continue
        for o in humans:o.hide_render='human' not in v;o.location=rest[o]+Vector(v.get('human',(0,0,0)))
        bpy.context.scene.cycles.samples=max(samples,192) if final and n=='hero' else samples
        shot(cam,v,out/(n+'.png'),width)
        (out/(n+'.json')).write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),render_script_sha256=RECIPE_SHA256,camera=v,plan=p,engine=bpy.context.scene.render.engine,samples=bpy.context.scene.cycles.samples,width=width,context=with_context,stage='final exported PBR' if final else 'exported PBR review'),indent=2))


def sheet(out,width,samples):
    source=Path('export/final/CommunityGardenPieces.gltf');bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()));roots=[o for o in bpy.context.scene.objects if not o.parent]
    Q.palette();out=Path(out);out.mkdir(parents=True,exist_ok=True);cam=setup(samples)
    def points(rt):return [ob.matrix_world@v.co for ob in [rt,*rt.children_recursive] if ob.type=='MESH' for v in ob.data.vertices]
    for group in ('pieces','plants'):
        selected=sorted([r for r in roots if (r.get('kind')=='plant')==(group=='plants') and not r.name.endswith('_field') and (group!='plants' or r.name.rsplit('_',1)[-1] in ('0','1'))],key=lambda o:o.name)
        for r in roots:
            for ob in [r,*r.children_recursive]:ob.hide_render=r not in selected
        labels=[];x=y=depth=0
        for j,rt in enumerate(selected):
            bpy.context.view_layer.update();pp=points(rt)
            lo=Vector(tuple(min(p[a] for p in pp) for a in range(3)));hi=Vector(tuple(max(p[a] for p in pp) for a in range(3)))
            if group=='plants':rt.location=(j%4*2.8,j//4*2.8,0)
            else:
                w,d=hi.x-lo.x,hi.y-lo.y
                if x+w>14:x=0;y+=depth+1.3;depth=0
                rt.location=Vector((x-lo.x,y-lo.y,-lo.z));x+=w+.65;depth=max(depth,d)
            bpy.context.view_layer.update();pp=points(rt)
            labels.append((rt.name,Vector(((min(p.x for p in pp)+max(p.x for p in pp))/2,min(p.y for p in pp)-.34,.01))))
        pp=[p for rt in selected for p in points(rt)]+[p for _,p in labels]
        centre=Vector(tuple((min(p[a] for p in pp)+max(p[a] for p in pp))/2 for a in range(3)))
        offset=Vector((0,-20,34));rot=(-offset).to_track_quat('-Z','Y');basis=rot.to_matrix();inv=basis.transposed()
        projected=[inv@(p-centre) for p in pp];lo=Vector(tuple(min(p[a] for p in projected) for a in range(3)));hi=Vector(tuple(max(p[a] for p in projected) for a in range(3)))
        centre+=basis@Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,0));span=hi.x-lo.x+1.1;aspect=span/(hi.y-lo.y+1.4)
        floor=Q.root('Sheet floor');Q.box('Neutral sheet ground',(centre.x,centre.y,-.05),(60,90,.08),floor,'Gravel')
        v=dict(location=tuple(centre+offset),target=tuple(centre),ortho=span,aspect=aspect,exposure=0,sun_energy=4,sun_angle=3,sky_strength=.18)
        path=out/(group+'.png');shot(cam,v,path,width)
        # Screen-space labels stay legible on the complete catalogue. Geometry
        # and shadows below them are the unchanged imported glTF prototypes.
        from bpy_extras.object_utils import world_to_camera_view
        from PIL import Image,ImageDraw,ImageFont
        from kit.fonts import find_font
        im=Image.open(path).convert('RGB');draw=ImageDraw.Draw(im);font=ImageFont.truetype(find_font('Noto Sans'),max(14,width//85))
        for name,p in labels:
            q=world_to_camera_view(bpy.context.scene,cam,p);draw.text((q.x*im.width,(1-q.y)*im.height),name,font=font,anchor='mt',fill='white',stroke_width=2,stroke_fill=(20,25,20))
        im.save(path)
        (out/(group+'.json')).write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),render_script_sha256=RECIPE_SHA256,camera=v,engine='CYCLES',samples=samples,width=width,members=[r.name for r in selected]),indent=2))
        for ob in [*floor.children_recursive,floor]:bpy.data.objects.remove(ob,do_unlink=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--out',default='renders/checkpoint');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=40);p.add_argument('--seeds',type=int,nargs='+',default=list(SEEDS));p.add_argument('--shots',nargs='+');p.add_argument('--sheet',action='store_true');p.add_argument('--lookdev',action='store_true');p.add_argument('--no-context',action='store_true');p.add_argument('--final',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.sheet:sheet(a.out,a.width,a.samples);return
    for seed in a.seeds:render(seed,Path(a.out)/str(seed),a.width,a.samples,a.shots,with_context=not a.no_context,final=a.final)
    if not a.shots:
        sheet(a.out,a.width,a.samples)
        if a.lookdev:
            from look_batch import specimens
            specimens(a.out,a.width,a.samples)
            import match
            sys.argv=['match.py','--','--out',str(Path(a.out)/'matches'),'--width',str(a.width),'--samples',str(a.samples)]
            match.main()


if __name__=='__main__':main()
