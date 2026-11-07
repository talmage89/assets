"""Inspect imported GLBs or source look-dev under procedural daylight."""
import argparse,json,sys,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
import bpy,bmesh
from mathutils import Vector,Matrix
from kit import gpu,model as G
from kit.studio import human
from kit.photo_match import verify
from kit.motion import surface
from spec import spec

def mat(name,col,rough=.8):
    m=bpy.data.materials.new(name);m.use_nodes=True;b=m.node_tree.nodes['Principled BSDF'];b.inputs['Base Color'].default_value=(*col,1);b.inputs['Roughness'].default_value=rough;return m

def setup(engine):
    sc=bpy.context.scene;sc.render.engine=engine;
    if engine=='CYCLES':gpu.enable()
    sc.cycles.use_denoising=True;sc.cycles.max_bounces=7
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.85
    world=bpy.data.worlds.new('Procedural daylight');world.use_nodes=True;sc.world=world
    sky=world.node_tree.nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False;sky.sun_elevation=math.radians(27);sky.sun_rotation=math.radians(135)
    world.node_tree.links.new(sky.outputs['Color'],world.node_tree.nodes['Background'].inputs['Color']);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.035
    sun=bpy.data.objects.new('Raking sun',bpy.data.lights.new('Raking sun','SUN'));sc.collection.objects.link(sun);sun.data.energy=2.6;sun.data.angle=math.radians(3)
    sun.rotation_euler=Vector((.7,.2,-.48)).to_track_quat('-Z','Y').to_euler()
    ground=G.mesh('Presentation concrete',[(-100,-100,0),(100,-100,0),(100,100,0),(-100,100,0)],[(0,1,2,3)],mat('Quick concrete',(.25,.26,.25)))
    nt=ground.data.materials[0].node_tree;n=nt.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=280
    tex=nt.nodes.new('ShaderNodeTexCoord');nt.links.new(tex.outputs['Object'],n.inputs['Vector']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.35;bump.inputs['Distance'].default_value=.0004;nt.links.new(n.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs['Normal'],nt.nodes['Principled BSDF'].inputs['Normal'])
    camera=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(camera);sc.camera=camera;camera.data.clip_start=.001
    silhouettes=human()
    for o in silhouettes:o.hide_render=True
    return camera,ground,silhouettes,sun,sky

def shots(s):
    return {
      'hero':dict(location=(.90,-.95,.70),target=(0,0,.075),lens=54,aspect=1.45),
      'top':dict(location=(0,-.001,1.6),target=(0,0,.08),ortho=.94,aspect=1.0),
      'bottom':dict(location=(0,-.001,1.6),target=(0,0,.10),ortho=.94,aspect=1.0,invert=True),
      'side':dict(location=(1.5,0,.11),target=(0,0,.11),ortho=.95,aspect=2.6),
      'front':dict(location=(0,-1.5,.095),target=(0,-s.axle_y,.08),ortho=.285,aspect=1.6),
      'concave_section':dict(location=(0,-.7,.16),target=(0,0,.089),ortho=.235,aspect=2.5,section=True),
      'truck':dict(location=(.21,-.38,.31),target=(0,-s.plate_y,.097),lens=64,aspect=1.35,invert=True),
      'truck_inner':dict(location=(.16,.015,.27),target=(0,-s.plate_y,.088),lens=62,aspect=1.35,invert=True),
      'wheel_bearing':dict(location=(-.28,-.31,.10),target=(-.087,-s.axle_y,.029),lens=70,aspect=1.3),
      'tail_plies':dict(location=(.13,.61,.125),target=(0,.374,.125),lens=65,aspect=1.5),
      'section_stance':dict(location=(0,-.7,.16),target=(0,0,.089),ortho=.235,aspect=2.5,section=True,station=0),
      'section_truck':dict(location=(0,-.90,.16),target=(0,-.20,.089),ortho=.235,aspect=2.5,section=True,station=-.20),
      'section_kick':dict(location=(0,-1.02,.17),target=(0,-.32,.105),ortho=.235,aspect=2.5,section=True,station=-.32),
      'hero_bottom':dict(location=(.80,-.9,.68),target=(0,0,.065),lens=54,aspect=1.45,invert=True),
      'grip_macro':dict(location=(.10,-.23,.21),target=(.014,-.17,.093),lens=80,aspect=1.35),
      'grip_edge':dict(location=(.23,-.10,.18),target=(.081,-.17,.096),lens=75,aspect=1.4),
      'lean_left':dict(location=(.22,-.55,.29),target=(0,-s.plate_y,.10),lens=62,aspect=1.5,invert=True,lean=-12),
      'lean_center':dict(location=(.22,-.55,.29),target=(0,-s.plate_y,.10),lens=62,aspect=1.5,invert=True,lean=0),
      'lean_right':dict(location=(.22,-.55,.29),target=(0,-s.plate_y,.10),lens=62,aspect=1.5,invert=True,lean=12),
      'rest_wall':dict(location=(1.05,1.5,.86),target=(0,.11,.40),lens=58,aspect=1.0,wall_rest=True,sun_direction=(.5,-.3,-.70)),
      'scale':dict(location=(2.6,-3.5,1.8),target=(-.43,0,.82),lens=60,aspect=.85,human=True),
    }

def main():
    p=argparse.ArgumentParser();p.add_argument('--engine',default='CYCLES');p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=40);p.add_argument('--shots');p.add_argument('--cameras');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source).resolve();digest=hashlib.sha256(src.read_bytes()).hexdigest();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if src.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(src))
    else:bpy.ops.import_scene.gltf(filepath=str(src))
    sc=bpy.context.scene
    root=bpy.data.objects['Skateboard'];s=spec(int(root.get('seed',0)),root.get('age_state','season'))
    meshes=[o for o in sc.objects if o.type=='MESH' and not o.get('source_only')];rest={o:o.matrix_basis.copy() for o in sc.objects};cam,ground,silhouettes,sun,sky=setup(a.engine)
    definitions=shots(s)
    if a.cameras:
        verify(a.cameras);definitions={k:{**v['shot'],**v.get('presentation',{})} for k,v in json.loads(Path(a.cameras).read_text()).items()}
    names=a.shots.split(',') if a.shots else list(definitions)
    metadata=json.loads((out/'shots.json').read_text()) if (out/'shots.json').exists() else {}
    sc.render.engine=a.engine;sc.cycles.samples=a.samples;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
    for name in names:
        d=definitions[name]
        for o,m in rest.items():o.matrix_basis=m
        bpy.context.view_layer.update()
        for o in meshes:o.hide_render=False
        for o in silhouettes:o.hide_render=not d.get('human',False)
        ground.hide_render=d.get('background')=='transparent';sc.render.film_transparent=ground.hide_render
        temporary=None
        if d.get('invert'):
            root.matrix_world=Matrix.Rotation(math.pi,4,'X')@root.matrix_world;bpy.context.view_layer.update()
            zmin=min((o.matrix_world@v.co).z for o in meshes for v in o.data.vertices);root.location.z-=zmin
        if d.get('wall_rest'):
            socket=bpy.data.objects['Socket_Rest_Wall'];root.matrix_world=Matrix.Translation((0,0,float(socket['wall_alignment_height_m'])))@Matrix.Rotation(-math.pi/2,4,'X')@socket.matrix_world.inverted();bpy.context.view_layer.update()
            wall=G.mesh('Temporary wall',[(-2,-.0002,0),(2,-.0002,0),(2,-.0002,3),(-2,-.0002,3)],[(0,1,2,3)],mat('Wall concrete',(.28,.29,.28)));wall['section_temp']=True
        if 'lean' in d:
            for label in ('Front','Rear'):h=bpy.data.objects['Hanger_'+label];h.matrix_basis=h.matrix_basis@Matrix.Rotation(math.radians(d['lean'] if label=='Front' else -d['lean']),4,'Z')
        ground.location.z=0
        if d.get('isolate_truck'):
            for o in meshes:
                o.hide_render='Front' not in o.name
                if o.name=='SkateboardMesh':
                    # Presentation-only face isolation from the imported GLB.
                    # The actual delivered baseplate/hardware surfaces remain;
                    # the deck and rear truck are omitted for the loose photo.
                    q=o.copy();q.data=o.data.copy();sc.collection.objects.link(q);q.hide_render=False;q['section_temp']=True
                    bm=bmesh.new();bm.from_mesh(q.data)
                    doomed=[f for f in bm.faces if all((q.matrix_world@v.co).z<root.location.z-s.underside+.0001 for v in f.verts) or any((q.matrix_world@v.co).y<.10 for v in f.verts)]
                    bmesh.ops.delete(bm,geom=doomed,context='FACES');bm.to_mesh(q.data);bm.free()
        if d.get('hide_wheels'):
            for o in meshes:
                if any(v in o.name for v in ('Urethane','Wheel_','608 ','Bearing spacer','Axle nut','Axle speed')):o.hide_render=True
        if d.get('isolate_truck'):
            visible=[o for o in sc.objects if o.type=='MESH' and o!=ground and o not in silhouettes and not o.hide_render]
            if visible:ground.location.z=min((o.matrix_world@v.co).z for o in visible for v in o.data.vertices)
        if d.get('section'):
            for o in meshes:o.hide_render=True
            deck=next(o for o in meshes if o.get('part')=='deck');temporary=deck.copy();temporary.data=deck.data.copy();sc.collection.objects.link(temporary);temporary.hide_render=False
            bm=bmesh.new();bm.from_mesh(temporary.data)
            cut=bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,d.get('station',0),0),plane_no=(0,1,0),clear_inner=True)
            edges=[e for e in cut['geom_cut'] if isinstance(e,bmesh.types.BMEdge) and e.is_boundary]
            fill=bmesh.ops.holes_fill(bm,edges=edges,sides=0)
            for f in fill['faces']:f.material_index=2
            bm.to_mesh(temporary.data);bm.free()
            # Laminate faces for the exposed section only. Heights are ray-hit
            # on the actual imported deck; these inspection caps never export.
            surf=surface(deck);xs=[-s.width/2+.0008+(s.width-.0016)*i/64 for i in range(65)];profile=[]
            for x in xs:
                top=surf['tree'].ray_cast(Vector((x,d.get('station',0),1)),Vector((0,0,-1)),2)[0]
                bot=surf['tree'].ray_cast(Vector((x,d.get('station',0),-1)),Vector((0,0,1)),2)[0]
                if bot is not None and top is not None:profile.append((x,bot.z,top.z))
            for layer in range(8):
                vertices=[]
                for x,b,t in profile:
                    lo=b+(t-b-.00055)*layer/7 if layer<7 else t-.00055
                    hi=b+(t-b-.00055)*(layer+1)/7 if layer<7 else t
                    vertices.extend([(x,d.get('station',0)-.00015,lo),(x,d.get('station',0)-.00015,hi)])
                cap=G.mesh('Section veneer '+str(layer),vertices,[(2*i,2*i+2,2*i+3,2*i+1) for i in range(len(profile)-1)],deck.data.materials[2+layer] if layer<7 else deck.data.materials[1]);cap['section_temp']=True
        bpy.context.view_layer.update();cam.location=d['location'];cam.rotation_euler=(Vector(d['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',d.get('roll',0))
        cam.data.type='ORTHO' if 'ortho' in d else 'PERSP';cam.data.ortho_scale=d.get('ortho',1);cam.data.lens=d.get('lens',55);cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36
        sc.view_settings.exposure=d.get('exposure',.85)
        if d.get('light')=='window':
            sun.data.energy=0;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.055
            light=bpy.data.objects.get('Camera flash')
            if not light:light=bpy.data.objects.new('Camera flash',bpy.data.lights.new('Camera flash','AREA'));sc.collection.objects.link(light)
            center=Vector((0,s.plate_y,.075));right=cam.rotation_euler.to_quaternion()@Vector((1,0,0))
            light.location=center-right*.28+Vector((0,0,.45));light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler();light.data.energy=65;light.data.size=.32;light.hide_render=False
        elif d.get('light')=='flash':
            sun.data.energy=0;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.08
            light=bpy.data.objects.get('Camera flash')
            if not light:light=bpy.data.objects.new('Camera flash',bpy.data.lights.new('Camera flash','AREA'));sc.collection.objects.link(light)
            light.location=cam.location;light.rotation_euler=cam.rotation_euler;light.data.energy=35;light.data.size=.04;light.hide_render=False
        else:
            sun.data.energy=d.get('sun_energy',2.6);sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=d.get('sky_strength',.035)
            sun.rotation_euler=Vector(d.get('sun_direction',(.7,.2,-.48))).to_track_quat('-Z','Y').to_euler()
            if bpy.data.objects.get('Camera flash'):bpy.data.objects['Camera flash'].hide_render=True
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/d.get('aspect',1.45));sc.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
        metadata[name]=dict(source=str(src),sha256=digest,stage='source procedural look-dev' if src.suffix=='.blend' else 'exported GLB / baked atlas' if 'export' in src.parts else 'form checkpoint exported GLB',samples=a.samples,**d)
        (out/'shots.json').write_text(json.dumps(metadata,indent=2))
        if temporary:bpy.data.objects.remove(temporary,do_unlink=True)
        for o in list(sc.objects):
            if o.get('section_temp'):bpy.data.objects.remove(o,do_unlink=True)
if __name__=='__main__':main()
