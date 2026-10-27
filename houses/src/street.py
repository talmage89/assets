"""Eye-height street staging from immutable imported deliveries only.

Ground modules are instanced and transformed for the lot. House, maple and
pickup retain their delivered geometry/materials. This file never exports.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from render import setup
from kit.tiling import world_uv
from delivery_io import bundle_hash
from check_mesh import surface

GRADE=.16764
BAY=3.048
LENGTH=6.096


def imported(source):
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
    return set(bpy.data.objects)-before


def main(a):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    source=Path(f'export/Hearthfield-{a.seed}.gltf');meta=json.loads(source.with_suffix('.json').read_text())
    house=imported(source);mh=surface([o for o in house if o.type=='MESH'])
    context=json.loads(Path('build/context.json').read_text())
    for row in context:assert hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['sha256']
    ground_path=Path(context[0]['source']);ground=imported(ground_path)
    library={o.name:o for o in ground if o.parent is None};placed=[]
    def place(kind,name,loc,yaw=0,scale=(1,1,1)):
        root=library[kind];copies={}
        for ob in [root]+list(root.children_recursive):
            cp=ob.copy();bpy.context.collection.objects.link(cp);copies[ob]=cp
        for ob,cp in copies.items():
            cp.parent=copies.get(ob.parent);cp.matrix_basis=ob.matrix_basis.copy();cp.name=name if ob==root else name+'__'+ob.name
        rt=copies[root];rt.location=loc;rt.rotation_mode='XYZ';rt.rotation_euler=(0,0,math.radians(yaw));rt.scale=scale
        placed.extend(copies.values());return rt
    apron=meta['sockets']['GarageApron'];walk=meta['sockets']['Walk'];main,garage=meta['blocks']
    # Six 10-ft driveway pours, 20-ft wide, ending on the garage's actual sill.
    street_y=apron[1]-6*BAY;drive_left=apron[0]-BAY;drive_right=apron[0]+BAY
    drive=[]
    for i in range(6):
        y=street_y+i*BAY;z=apron[2]-GRADE-.004*(apron[1]-y)+.005
        root=place('Driveway_Slab',f'Drive_{i}',(apron[0],y,z),90,(1,2,1));drive.extend(root.children_recursive)
    # A separate walk terminates at Socket_Walk, the bottom stair connection.
    walk_width=1.2192;walk_left=walk[0]-walk_width/2;walk_right=walk[0]+walk_width/2
    length=walk[1]-street_y;count=math.ceil(length/1.524);pitch=length/count
    walk_obs=[]
    for i in range(count):
        y=street_y+(i+.5)*pitch
        # Native sidewalk panels run along local Y. Keep their transverse saw
        # joints, crossfall, and add the slight longitudinal grade by rotation.
        street_z=apron[2]-.004*6*BAY
        slope=-street_z/length;angle=math.atan(slope);base=.1524+.01*.762
        center_z=street_z+slope*(y-street_y)
        rt=place('Sidewalk_A',f'Walk_{i}',(walk_left,y+math.sin(angle)*base,center_z-math.cos(angle)*base),0,
            (walk_width/1.524,pitch/(1.524*math.cos(angle)),1))
        rt.rotation_euler.x=angle
        walk_obs.extend(rt.children_recursive)
    # Fit only whole lawn modules around the pavement; no covered lawn cards.
    # Imported modules are never edited. Local height variation is retained.
    def lawn_rect(x0,x1,y0,y1,label):
        nx=math.ceil((x1-x0)/LENGTH);ny=math.ceil((y1-y0)/LENGTH)
        if nx<=0 or ny<=0:return
        dx=(x1-x0)/nx;dy=(y1-y0)/ny
        for ix in range(nx):
            for iy in range(ny):
                x=x0+ix*dx;y=y0+(iy+.5)*dy
                sx=dx/LENGTH;angle=math.atan(.004/sx);base=.16264
                rt=place('Lawn_Field',f'{label}_{ix}_{iy}',(x-math.sin(angle)*base,y,-math.cos(angle)*base),0,(sx,dy/LENGTH,1))
                rt.rotation_euler.y=angle
    lawn_rect(-23,walk_left,street_y,main['y0'],'Lawn_left')
    lawn_rect(walk_right,drive_left,street_y,main['y0'],'Lawn_middle')
    lawn_rect(drive_right,23,street_y,garage['y1']+8,'Lawn_right')
    lawn_rect(-23,main['x0'],main['y0'],main['y1']+8,'Lawn_side')
    lawn_rect(main['x0'],drive_left,main['y1'],main['y1']+8,'Lawn_rear')
    # Asphalt runs across the street, its near edge at the driveway end.
    for i in range(-7,8):place('Road_Straight_A',f'Street_{i}',(i*LENGTH,street_y-3.6576,.0221),90)
    for ob in ground:bpy.data.objects.remove(ob,do_unlink=True)
    tree=imported(Path(context[1]['source']));tree_root=next(o for o in tree if o.parent is None)
    tree_root.location=(-11.5,main['y0']-7,0)
    pickup=imported(Path(context[2]['source']));pickup_root=next(o for o in pickup if o.parent is None)
    # Stock truck -Y forward, parked facing the garage; original tire form retained.
    pickup_root.location=(apron[0]+.12,apron[1]-4.4,apron[2]+.005-.004*4.4)
    pickup_root.rotation_mode='XYZ';pickup_root.rotation_euler=(-math.atan(.004),0,math.pi)
    camera=setup('CYCLES',a.samples)
    # setup's gray presentation grade is removed: the lawn and road are imports.
    bpy.data.objects.remove(bpy.data.objects['Presentation grade, excluded from asset'],do_unlink=True)
    # Far presentation grade shares the imported lawn maps and fills the horizon.
    # It lies below all detailed lawn modules; no other asset is edited.
    lawn=next(m for o in placed if o.type=='MESH' for m in o.data.materials if m.name=='Lawn')
    bpy.ops.mesh.primitive_plane_add(size=2000,location=(0,0,-.06));far=bpy.context.object
    far.name='Distant presentation lawn';far.data.materials.append(lawn);world_uv(far,3.048)
    tint=far.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
    for c in tint.data:c.color=(.95,.95,.95,1)
    camera.location=(12,street_y-13,1.68);target=Vector((-2,-1,4.2))
    camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=35
    sc=bpy.context.scene;sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/1.6);sc.render.resolution_percentage=100
    out=Path('renders/street');out.mkdir(parents=True,exist_ok=True);sc.render.filepath=str((out/'street.png').resolve())
    # Measure actual imported pavement near each declared socket, not constants.
    bpy.context.view_layer.update();drive_surface=surface([o for o in drive if o.type=='MESH'])
    walk_surface=surface([o for o in walk_obs if o.type=='MESH'])
    contacts={}
    for name,p,mesh in [('GarageApron',apron,drive_surface),('Walk',walk,walk_surface)]:
        hit=mesh.find_nearest(Vector(p));assert hit[0] is not None
        contacts[name]=dict(socket=p,nearest_surface=list(hit[0]),gap_m=hit[3])
        assert hit[3]<.0015,(name,hit[3])
    assert not (tree & house) and not (pickup & house)
    bpy.ops.render.render(write_still=True)
    provenance=dict(house=str(source),house_bundle_sha256=bundle_hash(source),context=context,
        camera_height_m=camera.location.z,contacts=contacts,engine='CYCLES',render_only=True,
        scope='Other assets imported, instanced/transformed for presentation only; no joins, texture changes or exports')
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2));print('STREET_CONTACTS',contacts)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=27);p.add_argument('--width',type=int,default=1440)
    p.add_argument('--samples',type=int,default=64);main(p.parse_args(sys.argv[sys.argv.index('--')+1:]))
