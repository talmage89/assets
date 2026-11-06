"""Cycles form evidence from freshly imported external glTF, never the blend.

Stock Ground, Houses and Cars appear only as presentation context. Every
input bundle is hashed in each render receipt and is never saved or exported.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).resolve().parent))
from kit import model as G,gpu
from kit.studio import human
from kit.fonts import find_font

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def bundle(path):
    path=Path(path);files=[path]
    if path.suffix=='.gltf':
        doc=json.loads(path.read_text());files += [path.parent/v['uri'] for key in ('buffers','images') for v in doc.get(key,[]) if 'uri' in v]
    return dict(source=str(path.relative_to(ROOT)),files={str(p.relative_to(ROOT)):sha(p) for p in files})

def load(path):
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));added=set(bpy.context.scene.objects)-before
    return {o.name:o for o in added if o.parent not in added},added

def material(n,c,rough=.8):
    m=bpy.data.materials.new(n);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough;return m

def camera(loc,target,lens=45,ortho=None,roll=0):
    c=bpy.data.objects.new('CheckpointCamera',bpy.data.cameras.new('CheckpointCamera'));bpy.context.collection.objects.link(c);c.location=loc;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.rotation_euler.rotate_axis('Z',roll);c.data.lens=lens;c.data.sensor_width=36;c.data.sensor_fit='HORIZONTAL'
    if ortho:c.data.type='ORTHO';c.data.ortho_scale=ortho
    bpy.context.scene.camera=c;return c

def label(text,pos,size=.12):
    font=bpy.data.curves.new(text,'FONT');font.body=text;font.size=size;font.align_x='CENTER';font.font=bpy.data.fonts.load(find_font('DejaVu Sans','Condensed Bold'))
    ob=bpy.data.objects.new('Caption '+text,font);bpy.context.collection.objects.link(ob);ob.location=pos;ob.rotation_euler=(math.pi/2,0,0);font.materials.append(material('Caption',(.12,.15,.13)));return ob

def silhouette(pos):
    for o in human():o.location+=Vector((pos[0]+1.03,pos[1]-.24,pos[2]))

def setlight(outdoors=False,shade=False):
    sc=bpy.context.scene;sc.world=bpy.data.worlds.new('Procedural daylight');sc.world.use_nodes=True
    ns=sc.world.node_tree.nodes;ln=sc.world.node_tree.links
    sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False;sky.sun_elevation=math.radians(22);sky.sun_rotation=math.radians(135);sky.air_density=1.05
    sky.aerosol_density=.3
    ln.new(sky.outputs[0],ns.get('Background').inputs[0]);ns.get('Background').inputs[1].default_value=.035 if outdoors else .025
    sun=bpy.data.objects.new('Raking sun',bpy.data.lights.new('Raking sun','SUN'));bpy.context.collection.objects.link(sun);sun.rotation_euler=Vector((.55,.85,-.65)).to_track_quat('-Z','Y').to_euler();sun.data.energy=4.0 if outdoors else 3.2;sun.data.angle=math.radians(1.2);sun.data.color=(1,.97,.93)
    if shade:sun.data.energy=.05;ns.get('Background').inputs[1].default_value=.13
    if not outdoors:
        light=bpy.data.objects.new('Large overhead fill',bpy.data.lights.new('Large overhead fill','AREA'));bpy.context.collection.objects.link(light);light.location=(-3,-5,7);light.rotation_euler=(Vector((0,0,1))-light.location).to_track_quat('-Z','Y').to_euler();light.data.energy=450;light.data.shape='DISK';light.data.size=6
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.25;sc.view_settings.use_white_balance=True;sc.view_settings.white_balance_temperature=6500

def place(lib,key,loc=(0,0,0),yaw=0,copy=False):
    rt=lib[key]
    if copy:
        copies={o:o.copy() for o in [rt,*rt.children_recursive]}
        for o,cp in copies.items():bpy.context.collection.objects.link(cp);cp.parent=copies.get(o.parent);cp.matrix_basis=o.matrix_basis.copy()
        rt=copies[rt]
    rt.location=loc;rt.rotation_mode='XYZ';rt.rotation_euler=(0,0,math.radians(yaw));return rt

def visible(roots,keys):
    for key,rt in roots.items():
        for ob in [rt,*rt.children_recursive]:ob.hide_render=key not in keys

def context(receipts):
    # Standard ground modules are placed at their native construction datums.
    path=ROOT/'ground/export/Ground.glb';lib,obs=load(path);receipts.append(bundle(path))
    def tile(kind,loc,yaw=0,scale=(1,1,1)):
        rt=place(lib,kind,loc,yaw,True);rt.scale=scale;return rt
    tile('Road_Intersection',(-13.2588,-4.1148,-.1524))
    tile('Curb_Corner',(-4.572,4.572,-.1524))
    tile('Sidewalk_Corner',(-4.572,4.572,-.1524))
    for j in range(-1,25):
        x=j*3.048
        tile('Road_Straight_A',(x,-4.1148,-.1524),90,scale=(1,.5,1))
        tile('Curb_Straight',(x,0,-.1524),90)
        tile('Curb_Straight',(x,-8.2296,-.1524),270)
        for k in range(3):
            # Three native sidewalk panels make a broad transit furnishing zone
            # and leave an uninterrupted 1.524m route behind the shelter.
            tile('Sidewalk_A',(x, .1524+k*1.524,-.1524),90,scale=(1,2,1))
        tile('Lawn_Strip',(x,-8.382,-.1524),270)
        tile('Sidewalk_A',(x,-10.2108,-.1524),270,scale=(1,2,1))
    for ob in obs:bpy.data.objects.remove(ob,do_unlink=True)
    for rel,positions in [('houses/export/HearthfieldCape-31.gltf',[(-12,-22,0),(21,-22,0),(49,-22,0),(18,16,0)]),('houses/export/HearthfieldRanch-11.gltf',[(7,-23,0),(37,-23,0),(42,17,0)])]:
        path=ROOT/rel;receipt=bundle(path);lib,objs=load(path);receipts.append(receipt)
        for i,p in enumerate(positions):
            carrier=G.pivot('Presentation house',p);carrier.rotation_euler.z=math.pi if p[1]<0 else 0
            for r in lib.values():
                placed=place(lib,r.name,tuple(r.location),0,True);placed.parent=carrier
        for o in objs:bpy.data.objects.remove(o,do_unlink=True)
    for rel,positions in [('cars/export/AlderC150.glb',[(10,-1.3,-.11),(24,-1.3,-.11),(-12,-6.7,-.11)]),('cars/export/AlderH120.glb',[(0,-6.7,-.11),(16,-6.7,-.11)])]:
        path=ROOT/rel;lib,objs=load(path);receipts.append(bundle(path))
        for p in positions:
            carrier=G.pivot('Presentation parked car',p);carrier.rotation_euler.z=math.pi/2
            for r in lib.values():place(lib,r.name,(0,0,0),0,True).parent=carrier
        for o in objs:bpy.data.objects.remove(o,do_unlink=True)
    # Continuous outlying lawn belongs to presentation, never furniture export.
    G.box('Context lawn',(0,-36,-.08),(160,40,.05),material('Distant lawn',(.07,.11,.035)),0)

SHOTS={
    'hero':dict(location=(-10,-5.2,1.65),target=(5.8,1.2,1.48),lens=40,aspect=1.65),
    'lineup':dict(location=(12,-23,13),target=(10,3,1.1),lens=47,aspect=2.6,ortho=25),
    'signs-regulatory':dict(location=(8,-20,18),target=(8,4,1.7),ortho=20.5,aspect=1.8),
    'signs-warning':dict(location=(4,-12,6.5),target=(4,0,1.9),ortho=12,aspect=1.65),
    'sign-face':dict(keys=['RoadSign_speed30large'],location=(.50,-1.7,2.8),target=(0,-.03,2.59),lens=58,aspect=1),
    'sign-back':dict(keys=['RoadSign_speed30large'],location=(.7,1.4,2.7),target=(0,0,2.57),lens=60,aspect=1),
    'post-base':dict(keys=['RoadSign_schoolSpeed'],location=(.24,-.37,.23),target=(0,0,.07),lens=48,aspect=1),
    'shelter-frame':dict(keys=['Shelter'],location=(-4.4,-5.5,2.8),target=(0,0,1.45),lens=49,aspect=1.5),
    'bench':dict(keys=['Bench'],location=(2.1,-2.8,1.27),target=(0,0,.40),lens=58,aspect=1.5),
    'meter':dict(keys=['MeterSingle','MeterTwin'],location=(.8,-2.35,1.6),target=(.30,0,1.32),lens=62,aspect=1.3),
    'boxes':dict(keys=['NewsDaily','NewsPedestal','NewsWeekly'],location=(2.3,-3.6,1.64),target=(.65,0,.67),lens=54,aspect=1.5),
    'collection':dict(keys=['CollectionBox'],location=(1.8,-2.6,1.5),target=(0,0,.66),lens=60,aspect=1.2),
    'receptacles':dict(keys=['Litter','Recycling'],location=(1.9,-2.8,1.6),target=(.42,0,.48),lens=60,aspect=1.5),
    'rack':dict(keys=['BikeRack','BikeRackRow'],location=(2.3,-3.4,1.8),target=(.6,.3,.4),lens=48,aspect=1.5)
}

def build_shot(name,shot,match=False,source=Path('export/StreetFurniture.gltf')):
    bpy.ops.wm.read_factory_settings(use_empty=True);receipts=[]
    furniture=source.resolve();signs=ROOT/'street-signs/export/set/RoadSigns.gltf'
    lib,_=load(furniture);sg,_=load(signs);receipts += [bundle(furniture),bundle(signs)];lib.update(sg)
    if name=='hero':
        keep=['Shelter','BusStop','MeterSingle','MeterTwin','NewsDaily','NewsPedestal','NewsWeekly','BikeRackRow','Litter','Recycling','CollectionBox','RoadSign_noParkingL','RoadSign_speed30','RoadSign_pedestrian']
        visible(lib,keep)
        placements=[('Shelter',(3,1.60,0),0),('BusStop',(.4,.75,0),0),('MeterSingle',(10,.65,0),180),('MeterTwin',(16,.65,0),180),('NewsDaily',(-.9,.55,0),-12),('NewsPedestal',(-1.55,.60,0),3),('NewsWeekly',(-2.2,.63,0),6),('BikeRackRow',(7,1.35,0),90),('Litter',(5.65,.65,0),0),('Recycling',(6.5,.65,0),0),('CollectionBox',(21,.75,0),0),('RoadSign_noParkingL',(12,.65,0),0),('RoadSign_speed30',(24,.65,0),270),('RoadSign_pedestrian',(31,.65,0),278)]
        for k,p,y in placements:place(lib,k,p,y)
        place(lib,'MeterSingle',(22,.65,0),180,True);place(lib,'MeterTwin',(28,.65,0),180,True)
        context(receipts);setlight(True)
    elif name=='lineup':
        names=['Shelter','ShelterMissingPanel','BusStop','Bench','BikeRack','BikeRackRow','NewsDaily','NewsPedestal','NewsWeekly','CollectionBox','MeterSingle','MeterTwin','Litter','Recycling','NewsRow'];visible(lib,names)
        places=[(0,5,0),(5,5,0),(9,5,0),(12,5,0),(15,5,0),(18,5,0),(0,0,0),(2,0,0),(4,0,0),(6,0,0),(8,0,0),(10,0,0),(12,0,0),(14,0,0),(17,0,0)]
        for k,p in zip(names,places):place(lib,k,p);label(k,(p[0],p[1]-.7,.025),.16)
        for p in ((-2,0,0),(21,5,0)):silhouette(p)
        setlight()
    elif name.startswith('signs-'):
        names=[k for k in sg if k!='RoadSign_PoleBandBracket'];warning=[k for k in names if any(s in k for s in ('curve','stopAhead','pedestrian','schoolCrossing'))]
        names=warning if name=='signs-warning' else [k for k in names if k not in warning]
        visible(lib,names)
        cols=10 if name=='signs-regulatory' else 8
        for j,k in enumerate(names):
            p=((j%cols)*1.8,(j//cols)*8,0);place(lib,k,p);label(k.replace('RoadSign_',''),(p[0],p[1]-.8,.05),.14)
        silhouette((-1.5,0,0));setlight()
    else:
        keys=shot['keys'];visible(lib,keys)
        for j,k in enumerate(keys):place(lib,k,(j*(.65 if name=='meter' else .75 if name=='boxes' else .90),0,0))
        setlight(shade=match)
    if name!='hero':G.box('Neutral review ground',(8,2,-.016),(140,140,.03),material('Review ground',(.25,.26,.235)),0)
    camera(shot['location'],shot['target'],shot.get('lens',45),shot.get('ortho'),shot.get('roll',0));bpy.context.view_layer.update()
    return receipts

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=Path('export/StreetFurniture.gltf'));p.add_argument('--out',type=Path,default=Path('renders/checkpoint'));p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);p.add_argument('--shots');p.add_argument('--match',type=Path);p.add_argument('--engine',choices=['CYCLES','BLENDER_WORKBENCH'],default='CYCLES');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
    shots=SHOTS
    if a.match:
        data=json.loads(a.match.read_text());shots={k:dict(v['shot'],keys=v['keys']) for k,v in data.items()}
    names=a.shots.split(',') if a.shots else list(shots)
    for name in names:
        shot=shots[name];receipts=build_shot(name,shot,bool(a.match),a.source);sc=bpy.context.scene;sc.render.engine=a.engine
        if a.engine=='CYCLES':gpu.enable()
        else:
            sc.display.shading.light='STUDIO';sc.display.shading.color_type='TEXTURE';sc.display.shading.show_cavity=True;sc.display.shading.cavity_type='BOTH';sc.display.shading.show_shadows=True
        sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=8;sc.cycles.transparent_max_bounces=8
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.5));sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.filepath=str((a.out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        (a.out/(name+'.json')).write_text(json.dumps(dict(stage='form checkpoint from imported external glTF / quick materials',engine=a.engine,recipe_sha256=sha(Path(__file__)),photo_calibration_sha256=sha(a.match) if a.match else None,shot=shot,inputs=receipts,width=sc.render.resolution_x,height=sc.render.resolution_y,samples=a.samples,image_sha256=sha(a.out/(name+'.png'))),indent=2))
        print('RENDERED',name,flush=True)
if __name__=='__main__':main()
