"""Cycles construction review from reimported glTF, with source pair witnesses."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from kit import gpu
from kit import model as G


def material(name,color):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.9
    return m


def setup(samples,width,light=None):
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True
    sc.cycles.transparent_max_bounces=32;sc.cycles.max_bounces=6
    sc.world=bpy.data.worlds.new('Procedural daylight');sc.world.use_nodes=True
    ns,ls=sc.world.node_tree.nodes,sc.world.node_tree.links
    sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(34);sky.sun_rotation=math.radians(225);sky.sun_disc=False;sky.aerosol_density=.4
    bg=ns.get('Background');bg.inputs['Strength'].default_value=.075;ls.new(sky.outputs[0],bg.inputs[0])
    ld=bpy.data.lights.new('Raking afternoon sun','SUN');sun=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(sun)
    ld.energy=3.7;ld.color=(1,.965,.91);ld.angle=math.radians(1.8);sun.rotation_euler=Vector((.65,.80,-.75)).to_track_quat('-Z','Y').to_euler()
    G.box('Presentation ground',(0,0,-.23),(1800,1800,.10),material('Presentation ground',(.10,.125,.065)),0)
    cam=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'));sc.collection.objects.link(cam);sc.camera=cam
    cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.data.clip_end=2000;cam.data.clip_start=.05
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.45
    sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
    if light:
        sky.sun_elevation=math.radians(light.get('elevation',26));sky.sun_rotation=math.radians(light.get('azimuth',225))
        bg.inputs['Strength'].default_value=light.get('sky',.12);ld.energy=light.get('energy',3.2);ld.angle=math.radians(light.get('softness',1.8))
        sun.rotation_euler=Vector(light.get('direction',(.65,.80,-.75))).to_track_quat('-Z','Y').to_euler()
        sc.view_settings.exposure=light.get('exposure',-.45)
        if light.get('overcast',0):
            mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.inputs[0].default_value=light['overcast']
            mix.inputs[2].default_value=(1.2,1.2,1.2,1);ls.new(sky.outputs[0],mix.inputs[1]);ls.new(mix.outputs[0],bg.inputs[0])
    return cam


def views(stem,meta):
    p=meta['plan'];lo,hi=Vector(meta['bounds_min']),Vector(meta['bounds_max']);center=(lo+hi)/2;size=hi-lo
    if stem.startswith('Complex'):
        W,D=p['lot'];b=p['building'];w,d=b['width'],b['depth'];origin=p['buildings'][0]['origin'];origin=Vector(origin)+Vector(b['modules'][0]['origin']);x,y,_=origin
        v=dict(hero=dict(location=(x-21,-12,1.68),target=(x+2,y,4.1),lens=40,aspect=1.78),
               above=dict(location=(W*1.02,-D*1.20,max(W,D)*1.12),target=(0,0,1.8),lens=43,aspect=1.55),
               ground=dict(location=(x-28,y-36,1.68),target=(x+5,y,3.6),lens=35,aspect=1.65),
               rear=dict(location=(W*.45,D*.42,12),target=(0,18,3.5),lens=35,aspect=1.65))
        v['dusk']=dict(v['hero'])
    elif stem.startswith('Row'):
        w,d=p['width'],p['depth'];total=p['count']*w
        v=dict(hero=dict(location=(-total*.72,-d/2-14,1.68),target=(-total*.06,-d/2,3.1),lens=40,aspect=1.78),
               above=dict(location=(total*.64,-total*.90,total*.78),target=(0,0,2),lens=43,aspect=1.55),
               ground=dict(location=(-total*.59,-d/2-24,1.68),target=(0,-d/2,2.8),lens=40,aspect=1.65),
               rear=dict(location=(total*.53,d/2+27,7.5),target=(0,d/2,2.3),lens=42,aspect=1.65),
               entry=dict(location=(p['units'][1]['x']+(w*.29 if p['garage'] else -w*.29)+1.6,-d/2-4.5,1.68),target=(p['units'][1]['x']+(w*.29 if p['garage'] else -w*.29),-d/2+.4,1.4),lens=45,aspect=1.35),
               patios=dict(location=(-total*.42,d/2+10,3.3),target=(-total*.16,d/2+1.0,1.2),lens=42,aspect=1.6))
        if p['garage']:
            u=p['units'][1];gx=u['x']-w*.16;gy=-d/2+u['y']-1
            v['garage']=dict(location=(gx+2.5,gy-7,1.68),target=(gx,gy,1.5),lens=45,aspect=1.4)
        v['dusk']=dict(v['hero'])
    else:
        w,d=p['width'],p['depth'];fh=p['floor_height'];base=p['base']
        cx=(lo.x+hi.x)/2
        v=dict(hero=dict(location=(cx-size.x*.82,-d/2-25,1.68),target=(cx,0,4),lens=40,aspect=1.65),
               above=dict(location=(cx+size.x*.78,-size.x*.95,size.x*.80),target=(cx,0,3),lens=44,aspect=1.55),
               rear=dict(location=(cx+size.x*.75,d/2+26,11),target=(cx,0,3),lens=40,aspect=1.65),
               meters=dict(location=(w/2+4,-3.4,1.8),target=(w/2,0,1.35),lens=48,aspect=1.35))
        if p['access']=='breezeway':
            v['stairs']=dict(location=(-w/2-3,-d/2-9,2.0),target=(-w/2+1.5,-d/2-3.2,2.25),lens=42,aspect=1.25)
            bx=-w/2+p['unit_width']*.5-p['unit_width']*.22;sy=1
            v['balcony']=dict(location=(bx+3,d/2+7,base+fh+1.5),target=(bx,d/2+.5,base+fh+.9),lens=48,aspect=1.35)
        else:
            v['stairs']=dict(location=(1.20,-3.4,base+1.6),target=(-.3,.4,base+2.2),lens=28,aspect=1.25)
            bx=-(p['core_width']/2+p['unit_width']/2)-p['unit_width']*.22
            v['balcony']=dict(location=(bx-2,-d/2-7,base+fh+1.5),target=(bx,-d/2-.8,base+fh+.95),lens=48,aspect=1.35)
    if stem.startswith('Building'):
        if len(p['modules'])>1:
            v['meters']=dict(location=(w/2+.85,-2.7,1.75),target=(w/2,0,1.25),lens=36,aspect=1.3)
        offset=Vector(p['modules'][0]['origin'])
        for key in ('stairs','balcony','meters'):
            for field in ('location','target'):v[key][field]=list(Vector(v[key][field])+offset)
        if p['roof']=='mansard':v['mansard']=dict(location=(-w*.55+offset.x,-d/2-9+offset.y,7.2),target=(offset.x,-d/2+offset.y,4.0),lens=45,aspect=1.5)
        if p['access']=='breezeway':
            v['gallery']=dict(location=(-w/2+3+offset.x,-d/2-8+offset.y,4.4),target=(offset.x,-d/2-.8+offset.y,3.9),lens=42,aspect=1.5)
            v['gallery_dusk']=dict(v['gallery'],dusk=True)
        v['scale']=dict(location=(-9,-d/2-20,2.6),target=(0,-d/2,4.7),lens=40,aspect=1.4,human_offset=(0,-d/2-1.2,.13))
        for name,loc in (('front',(center.x,-size.y*3,center.z)),('side',(hi.x+size.x*2,center.y,center.z)),('back',(center.x,hi.y+size.y*3,center.z)),('top',(center.x,center.y-.001,hi.z+size.x*2))):
            v[name]=dict(location=loc,target=tuple(center),ortho=max(size.x,size.y)*1.15,aspect=1.4)
        v['dusk']=dict(v['hero'])
    return v


def package_hash(path):
    paths=[path]
    if path.suffix=='.gltf':
        doc=json.loads(path.read_text());paths += [path.parent/q['uri'] for q in doc.get('buffers',[])+doc.get('images',[])]
    return hashlib.sha256(b''.join(hashlib.sha256(p.read_bytes()).digest() for p in sorted(set(paths)))).hexdigest()


def recipe_hash():
    return hashlib.sha256(b''.join((HERE/f).read_bytes() for f in ('render.py','presentation.py','landscaping.py','context.py'))).hexdigest()


def paving_probes(sc,cam):
    """Actual camera/ground and unobstructed-sun rays, independent of luma."""
    from bpy_extras.object_utils import world_to_camera_view
    frame=cam.data.view_frame(scene=sc);lo=[min(v[k] for v in frame) for k in (0,1)];hi=[max(v[k] for v in frame) for k in (0,1)]
    sun=next(o for o in sc.objects if o.type=='LIGHT' and o.data.type=='SUN')
    toward_sun=-(sun.matrix_world.to_3x3()@Vector((0,0,-1)));rows=[];dg=bpy.context.evaluated_depsgraph_get()
    for x,y in ((.27,.92),(.35,.95),(.48,.91),(.78,.92),(.88,.96)):
        local=Vector((lo[0]+x*(hi[0]-lo[0]),hi[1]-y*(hi[1]-lo[1]),frame[0].z))
        direction=(cam.matrix_world.to_3x3()@local).normalized()
        hit,p,n,face,ob,xf=sc.ray_cast(dg,cam.location,direction,distance=500)
        if not hit:continue
        poly=ob.data.polygons[face];ma=ob.data.materials[poly.material_index]
        shadow,sp,sn,sf,so,sx=sc.ray_cast(dg,p+n*.012,toward_sun,distance=200)
        rows.append(dict(pixel_fraction=(x,y),object=ob.name,material=ma.name,surface_m=list(p),normal=list(n),sun_unoccluded=not shadow,sun_blocker=so.name if shadow else None))
    return rows


def render_file(path,out,width,samples,names=None,cameras=None,engine='CYCLES'):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if path.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
    else:bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    asset_objects=set(bpy.context.scene.objects)
    meta=json.loads(path.with_suffix('.json').read_text())
    light=next(iter(cameras.values())).get('light') if cameras else None
    cam=setup(samples,width,light)
    bpy.context.scene.render.engine=engine
    from presentation import dress,match_context
    dependencies=dress(meta,path.stem) if not cameras else match_context(meta,path.stem)
    if engine=='BLENDER_EEVEE':
        sc=bpy.context.scene;sc.eevee.use_raytracing=True
        sc.eevee.ray_tracing_options.resolution_scale='1';sc.eevee.ray_tracing_options.screen_trace_quality=.75
        for ma in bpy.data.materials:
            pp=next((n for n in ma.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None) if ma.use_nodes else None
            ma.use_raytrace_refraction=bool(pp and pp.inputs['Transmission Weight'].default_value>0);ma.thickness_mode='SLAB'
            if ma.use_raytrace_refraction:
                # Use the modeled 12 mm glazing pocket, rather than deriving
                # thickness from the entire joined building's bounds.
                gauge=ma.node_tree.nodes.new('ShaderNodeValue');gauge.outputs[0].default_value=.012
                output=next(n for n in ma.node_tree.nodes if n.type=='OUTPUT_MATERIAL')
                ma.node_tree.links.new(gauge.outputs[0],output.inputs['Thickness'])
    shots=cameras or views(path.stem,meta);out.mkdir(parents=True,exist_ok=True)
    # Photo comparisons share a folder; retain the other fitted views when
    # this call renders one asset, and when a detail-only rerender is requested.
    provenance=out/'provenance.json'
    records=json.loads(provenance.read_text()) if provenance.exists() else {}
    for name,shot in shots.items():
        if names and name not in names:continue
        sc=bpy.context.scene;shot=dict(shot)
        if not cameras:
            sun_direction=(-.65,-.80,-.75) if name in ('rear','patios','back') else (-.65,.80,-.75) if name=='side' else (.65,.80,-.75)
            for ob in sc.objects:
                if ob.type=='LIGHT' and ob.data.type=='SUN':ob.rotation_euler=Vector(sun_direction).to_track_quat('-Z','Y').to_euler()
            if name in ('rear','patios','back','side'):shot['inspection_sun_direction']=sun_direction
        hidden=[]
        if not cameras:
            for rt in sc.objects:
                if rt.get('presentation_family')!='trees':continue
                if math.hypot(rt.location.x-shot['location'][0],rt.location.y-shot['location'][1])>=10:continue
                for ob in rt.children_recursive:
                    if not ob.hide_render:ob.hide_render=True;hidden.append(ob)
            shot['camera_clearance_hidden_tree_objects']=[o.name for o in hidden]
        if name=='dusk' or shot.get('dusk'):
            from presentation import dusk_lights
            dusk_lights()
            sky=next(n for n in sc.world.node_tree.nodes if n.type=='TEX_SKY');sky.sun_elevation=math.radians(-3)
            sc.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.65
            for ob in sc.objects:
                if ob.type=='LIGHT' and ob.data.type=='SUN':ob.data.energy=0
            for ma in bpy.data.materials:
                if ma.name.startswith('Apartments_Trim') and ma.use_nodes:
                    next(n for n in ma.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Emission Strength'].default_value*=18
            sc.view_settings.exposure=1.25
        if name in ('hero','ground') and not cameras:
            # Measure the ground under the clear camera station, then put the
            # eye 1.68 m above that actual surface rather than nominal grade.
            xy=shot['location'];bpy.context.view_layer.update()
            station=Vector((xy[0],xy[1],100));ground=None
            for attempt in range(512):
                hit,point,normal,face,obj,matrix=sc.ray_cast(bpy.context.evaluated_depsgraph_get(),station,Vector((0,0,-1)))
                if not hit:break
                if point.z<.5 and normal.z>.8:ground=point.copy();break
                station=point-Vector((0,0,.004))
            assert ground is not None,(path,name,'No walking surface under camera')
            point=ground
            shot['location']=(xy[0],xy[1],point.z+1.68);shot['measured_ground_z_m']=point.z;shot['eye_height_m']=1.68
        cam.location=shot['location'];cam.rotation_euler=(Vector(shot['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
        if shot.get('roll'):cam.rotation_euler.rotate_axis('Z',shot['roll'])
        cam.data.lens=shot.get('lens',40);sc.render.resolution_x=width;sc.render.resolution_y=round(width/shot.get('aspect',1.6))
        cam.data.type='ORTHO' if shot.get('ortho') else 'PERSP'
        if shot.get('ortho'):cam.data.ortho_scale=shot['ortho']
        humans=[]
        inspection_floor=None
        if shot.get('ortho'):
            for ob in sc.objects:
                if ob not in asset_objects and ob.type in ('MESH','CURVE','FONT') and not ob.hide_render:
                    ob.hide_render=True;hidden.append(ob)
            inspection_floor=G.box('Turnaround floor',(0,0,-.06),(1000,1000,.12),material('Turnaround neutral ground',(.12,.125,.115)),0)
            shot['inspection_context']='Exported asset only, procedural neutral floor; surrounding presentation geometry hidden'
            shot['context_objects_hidden']=len(hidden)
        if shot.get('human_offset'):
            from kit.studio import human
            hpos=Vector(shot['human_offset']);bpy.context.view_layer.update()
            hit,ground,normal,face,obj,xf=sc.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((hpos.x,hpos.y,.45)),Vector((0,0,-1)),distance=1.)
            assert hit and normal.z>.8,('No human standing surface',path,name)
            hpos.z=ground.z;shot['human_base_ground_z_m']=ground.z;shot['human_height_m']=1.8
            humans=human()
            for ob in humans:ob.location+=hpos-Vector((-1.03,.24,0))
        audit_light=None
        if name=='meters' or name=='stairs' and meta['plan'].get('access') in ('enclosed','open'):
            # Temporary studio inspection fill makes dark covered construction
            # readable. It is not part of the asset, hero or photographic pairs.
            ld=bpy.data.lights.new('Inspection softbox','AREA');ld.energy=400 if name=='stairs' else 120;ld.shape='DISK';ld.size=1.5
            audit_light=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(audit_light)
            audit_light.location=cam.location+Vector((0,0,.45))
            audit_light.rotation_euler=(Vector(shot['target'])-audit_light.location).to_track_quat('-Z','Y').to_euler()
            shot['inspection_fill_w']=ld.energy
        sc.render.filepath=str((out/(name+'.png')).resolve());bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
        if name=='hero' and path.stem=='Complex-301':shot['paving_surface_probes']=paving_probes(sc,cam)
        if inspection_floor:bpy.data.objects.remove(inspection_floor,do_unlink=True)
        for ob in humans:bpy.data.objects.remove(ob,do_unlink=True)
        if audit_light:bpy.data.objects.remove(audit_light,do_unlink=True)
        for ob in hidden:ob.hide_render=False
        records[name]=dict(source=str(path),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),package_sha256=package_hash(path),recipe_sha256=recipe_hash(),camera=shot,light=light,context_dependencies=dependencies,engine=engine,samples=samples)
        provenance.write_text(json.dumps(records,indent=2))
    return records


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path);p.add_argument('--out',type=Path,default=Path('renders/checkpoint'));p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=32);p.add_argument('--only',default='all');p.add_argument('--shots');p.add_argument('--camera-file',type=Path);p.add_argument('--source-pairs',action='store_true');p.add_argument('--engine',default='CYCLES',choices=('CYCLES','BLENDER_EEVEE'));a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    names=a.shots.split(',') if a.shots else None
    if a.camera_file:
        data=json.loads(a.camera_file.read_text())
        for key,row in data.items():
            src=Path('build' if a.source_pairs else 'export')/(row['asset']+('.blend' if a.source_pairs else '.gltf'))
            render_file(src,a.out,a.width,a.samples,cameras={key:row['shot']})
        return
    paths=sorted(Path('export').glob('*.gltf'))
    for path in paths:
        if a.only!='all' and path.stem!=a.only:continue
        allshots=views(path.stem,json.loads(path.with_suffix('.json').read_text()))
        selected=names or ((['hero','above','ground','rear','entry','patios'] if path.stem.startswith('Row') else ['hero','above','ground','rear','dusk'] if path.stem in ('Complex-301','Complex-304') else ['hero','above','ground','rear']) if not path.stem.startswith('Building') else ['stairs','balcony','meters','mansard'])
        if not names:
            selected += {'Building-301':['scale','front','side','back','top'],
                         'Building-304':['gallery','gallery_dusk'],
                         'Building-305':['hero','above','front','side','back','top','dusk'],
                         'Row-403':['garage','dusk']}.get(path.stem,[])
        render_file(path,a.out/path.stem,a.width,a.samples,selected,engine=a.engine)

if __name__=='__main__':main()
