"""All checkpoint views import external glTF. Procedural clear sky and sun."""
import argparse
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from kit import gpu,studio
import geometry as G
from plan import FLOOR,SPAN,FT,deck_z


def lighting(elevation=18,azimuth=-135,interior=False):
    sc=bpy.context.scene
    world=bpy.data.worlds.new('Original procedural clear sky');world.use_nodes=True;sc.world=world
    n=world.node_tree.nodes;l=world.node_tree.links;sky=n.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(elevation);sky.sun_rotation=math.radians(azimuth);sky.sun_disc=False
    sky.altitude=100;sky.air_density=1;sky.aerosol_density=.35
    l.new(sky.outputs[0],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.10
    light=bpy.data.lights.new('Raking sun','SUN');light.energy=5.0;light.color=(1,.87,.72);light.angle=math.radians(.55)
    ob=bpy.data.objects.new('Raking sun',light);sc.collection.objects.link(ob)
    v=Vector((math.cos(math.radians(elevation))*math.cos(math.radians(azimuth)),math.cos(math.radians(elevation))*math.sin(math.radians(azimuth)),math.sin(math.radians(elevation))))
    ob.rotation_euler=(-v).to_track_quat('-Z','Y').to_euler()
    # Actual imported fixture sockets create bounded pools. Emissive lenses
    # remain in the glTF; the area sources are presentation lighting.
    for socket in list(sc.objects):
        if socket.get('socket_kind')!='light_emitter':continue
        ld=bpy.data.lights.new(socket.name+' pool','AREA');ld.energy=38;ld.shape='RECTANGLE';ld.size=1.0;ld.size_y=.14;ld.color=(1,.86,.63)
        ld.color=(1,.96,.84)
        oo=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(oo);oo.location=socket.matrix_world.translation;oo.rotation_euler=(0,0,0)
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.7 if not interior else .0


def shots(p):
    L,W=p['length'],p['width'];fy=p['flat_y'];ry=p['ramp_y'];top=(p['levels']-1)*FLOOR;ex=L/2-p['end_length']/2
    scale_car=max((s for s in p['stalls'] if s['level']==0 and not s['ramp'] and s['yaw']==180 and s['occupied']),key=lambda s:s['x'])
    # Street-side eye stays in front of the opposing frontage. Frame actual
    # exported module bounds, including the rear return and roof luminaires.
    garage=next(o for o in bpy.context.scene.objects if o.get('system')==p['system'] and o.name.startswith('Garage_'))
    points=[o.matrix_world@Vector(c) for o in garage.children_recursive if o.type=='MESH' for c in o.bound_box]
    eye=Vector((-L/2-(40 if p['system']=='precast' else 23),-W/2-(19.896 if p['system']=='precast' else 35),1.65))
    half_fov=math.atan(36/(2*35))
    for _ in range(40):
        azimuths=[math.atan2(v.y-eye.y,v.x-eye.x) for v in points]
        low,high=min(azimuths),max(azimuths)
        if high-low<1.80*half_fov:break
        eye.x-=1
    az=(low+high)/2;forward=Vector((math.cos(az),math.sin(az),0))
    elevations=[math.atan2(v.z-eye.z,(v-eye).dot(forward)) for v in points]
    el=(min(elevations)+max(elevations))/2
    direction=Vector((math.cos(el)*math.cos(az),math.cos(el)*math.sin(az),math.sin(el)))
    hero=dict(location=list(eye),target=list(eye+direction),lens=35,aspect=2.0)
    radius=min(22*FT,(ry-fy)/2)
    turn=min(p['paths'][0]['points'],key=lambda v:(v[0]-p['ramp_limits'][1]-radius)**2+(v[1]-ry+radius)**2)
    turn_eye=[turn[0],turn[1],turn[2]+1.65]
    ramp_target_x=p['ramp_limits'][1]-(8 if p['system']=='precast' else 4)
    return dict(hero=hero,
        above=dict(location=(-L*.88,-W*1.7,top+57),target=(0,0,top/2),lens=43,paths=True),
        aisle=dict(location=(-L/2+9,fy,1.65),target=(L/2-8,fy,1.70),lens=38,interior=True),
        ramp_turn=dict(location=turn_eye,target=(ramp_target_x,ry,deck_z(p,0,ramp_target_x,ry,True)+1.1),lens=28,interior=True),
        top_deck=dict(location=(-L/2+6,fy-3,top+1.65),target=(L/3,fy,top+1.70),lens=35),
        entry=dict(location=(ex-6,-W/2-20,1.65),target=(ex,-W/2-1,1.8),lens=35),
        tower=dict(location=(-L/2-20,-W/2-16,1.65),target=(p['towers'][0][0],p['towers'][0][1],p['levels']*FLOOR/2),lens=35),
        scale=dict(location=(scale_car['x']+5,fy+3,1.65),target=(scale_car['x']+.6,scale_car['y'],1.0),lens=42,interior=True,human=True,human_at=[scale_car['x']+1.45,scale_car['y'],scale_car['z']]))


def overlays(p):
    m=G.material('Drive path diagram cyan',(.025,.55,.80),.6,emission=.4);G.M['Diagram']=m
    b=G.Mesh('Drive and pedestrian path overlay')
    # Draw the upper circuit, where the actual slab does not hide the route.
    row=next(r for r in reversed(p['paths']) if r['name'].startswith('Drive_Up_'))
    b.tube([(x,y,z+.09) for x,y,z in row['points']],.095,'Diagram',8)
    b.finish()


@lru_cache(maxsize=64)
def source_identity(path):
    path=Path(path);doc=json.loads(path.read_text())
    return dict(source=str(path),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        source_buffer_sha256={b['uri']:hashlib.sha256((path.parent/b['uri']).read_bytes()).hexdigest() for b in doc['buffers']})


def render_shot(out,shot,width,samples,engine='CYCLES',source=None):
    sc=bpy.context.scene
    cam=bpy.data.objects.new('Export review camera',bpy.data.cameras.new('Export review camera'));sc.collection.objects.link(cam);sc.camera=cam
    cam.location=shot['location'];cam.rotation_euler=(Vector(shot['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=shot['lens'];cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL'
    if 'roll' in shot:cam.rotation_euler.rotate_axis('Z',shot['roll'])
    aspect=shot.get('aspect',1.6);sc.render.resolution_x=width;sc.render.resolution_y=round(width/aspect);sc.render.resolution_percentage=100
    sc.render.engine=engine
    if engine=='CYCLES':gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=shot.get('max_bounces',7);sc.cycles.transparent_max_bounces=32
    sc.render.image_settings.file_format='PNG';out.parent.mkdir(parents=True,exist_ok=True);sc.render.filepath=str(out.resolve());bpy.ops.render.render(write_still=True)
    receipt=dict(camera=list(cam.location),camera_world_z_m=float(cam.location.z),lens_mm=float(cam.data.lens),engine=engine,samples=samples,
        exposure=sc.view_settings.exposure,width=width,height=sc.render.resolution_y,output=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest())
    receipt.update(target=list(shot['target']),rotation_quaternion=list(cam.rotation_euler.to_quaternion()),sensor_width_mm=float(cam.data.sensor_width),roll=shot.get('roll',0))
    if source is not None:receipt.update(source_identity(source))
    return receipt


def module_sheet(args):
    """Each exported module receives its own scale-fitted construction view."""
    from PIL import Image,ImageDraw,ImageFont
    from kit.fonts import find_font
    inventory=json.loads(Path('build/modules.json').read_text());receipts=[];panels=[]
    outward=Vector((-1.3,-1.8,1.0)).normalized()
    rotation=(-outward).to_track_quat('-Z','Y');right=rotation@Vector((1,0,0));up=rotation@Vector((0,1,0))
    lens=48;aspect=1.25;tan_h=36/(2*lens);tan_v=tan_h/aspect
    for name,row in inventory.items():
        bpy.ops.wm.read_factory_settings(use_empty=True)
        path=Path('export/modules')/(name+'.gltf');bpy.ops.import_scene.gltf(filepath=str(path.resolve()));bpy.context.view_layer.update()
        points=[o.matrix_world@Vector(c) for o in bpy.context.scene.objects if o.type=='MESH' for c in o.bound_box]
        low=Vector([min(v[k] for v in points) for k in range(3)]);high=Vector([max(v[k] for v in points) for k in range(3)]);center=(low+high)/2
        distance=max(max((v-center).dot(outward)+abs((v-center).dot(right))/(tan_h*.84),(v-center).dot(outward)+abs((v-center).dot(up))/(tan_v*.84)) for v in points)
        G.palette();extent=max(high-low)*5+2
        plane=G.Mesh('Inspection floor');plane.box((center.x,center.y,low.z-.04),(extent,extent,.06),'Deck');plane.finish();lighting()
        shot=dict(location=list(center+outward*max(distance,.3)),target=list(center),lens=lens,aspect=aspect)
        png=args.out/'modules'/(name+'.png');r=render_shot(png,shot,600,args.samples,args.engine,source=path)
        r.update(name=name,triangles=row['triangles']);receipts.append(r)
        panel=Image.new('RGB',(400,356),(30,34,34));panel.paste(Image.open(png).convert('RGB').resize((400,320),Image.Resampling.LANCZOS),(0,0))
        d=ImageDraw.Draw(panel);font=ImageFont.truetype(find_font('DejaVu Sans','Book'),16)
        d.text((12,329),f"{name} / {row['triangles']:,} tris",font=font,fill=(235,232,218));panels.append(panel)
    sheet=Image.new('RGB',(2000,356*math.ceil(len(panels)/5)),(30,34,34))
    for i,panel in enumerate(panels):sheet.paste(panel,((i%5)*400,(i//5)*356))
    sheet.save(args.out/'modules.png');return receipts


def main():
    a=argparse.ArgumentParser();a.add_argument('--source');a.add_argument('--out',type=Path,default=Path('renders/checkpoint'));a.add_argument('--width',type=int,default=1200);a.add_argument('--samples',type=int,default=32);a.add_argument('--engine',default='CYCLES');a.add_argument('--shots',default='all');a.add_argument('--seeds',default='101,202');a.add_argument('--matches',action='store_true');args=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.matches:
        from matches import render_matches
        render_matches(args,render_shot,lighting);return
    receipts=[]
    for seed in map(int,args.seeds.split(',')):
        p=json.loads(Path(f'build/garage-{seed}.json').read_text())
        bpy.ops.wm.read_factory_settings(use_empty=True)
        path=Path(f'export/sites/ParkingGarageSite-{seed}.gltf');bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
        context=json.loads(Path(f'build/actors-{seed}.json').read_text());bpy.context.view_layer.update()
        cache=Path(f'build/render-context-{seed}.blend').resolve()
        bpy.ops.wm.save_as_mainfile(filepath=str(cache))
        print('TOWN READY',seed,len(context['actors']),context['context_triangles'],flush=True)
        for name,shot in shots(p).items():
            if args.shots!='all' and name not in args.shots.split(','):continue
            bpy.ops.wm.open_mainfile(filepath=str(cache))
            if shot.get('paths'):overlays(p)
            if shot.get('human'):
                at=Vector(shot['human_at'])
                for o in studio.human():
                    o.location+=at+Vector((1.03,-.24,0))
                    for mat in o.data.materials:mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.20,.22,.22,1)
            lighting(interior=shot.get('interior',False));receipt=render_shot(args.out/str(seed)/(name+'.png'),shot,args.width,args.samples,args.engine,source=path)
            receipt.update(seed=seed,name=name,cars=len(context['actors']),car_triangles=context['actor_triangles'],context_triangles=context['context_triangles'])
            receipts.append(receipt);(args.out/'views.json').write_text(json.dumps(receipts,indent=2)+'\n')
    if args.shots=='all' or args.shots=='modules':
        receipts.extend(module_sheet(args));(args.out/'views.json').write_text(json.dumps(receipts,indent=2)+'\n')
    if args.shots=='all':(args.out/'.stamp').touch()


if __name__=='__main__':main()
