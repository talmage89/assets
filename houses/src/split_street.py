"""Four exported split-levels on library ground, with own-export vegetation/car."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from render import setup
from street import imported
from cape_street import move
from delivery_io import bundle_hash


def main(a):
    bpy.ops.wm.read_factory_settings(use_empty=True);houses=[];groups=[]
    curb_y=-10.;grade=-.16764;walk_y=curb_y+.1524+1.8288
    for seed,x in ((51,0),(52,26),(55,52),(56,78)):
        source=Path(f'export/HearthfieldSplit-{seed}.gltf');meta=json.loads(source.with_suffix('.json').read_text())
        loc=(x,walk_y+1.524-meta['driveway']['front'],-meta['spec']['site_grade_m'])
        objects=imported(source);move(objects,loc);groups.append(objects)
        houses.append(dict(source=str(source),bundle_sha256=bundle_hash(source),location=loc,meta=meta))
    context=[]
    for folder,name in (('ground','Ground'),('trees','RedMaple'),('cars','AlderC150'),('shrubs','Shrubs'),('trees','PinOak')):
        p=Path('..')/folder/'export'/(name+'.glb');assert p.exists(),p
        context.append(dict(source=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size))
    ground=imported(Path(context[0]['source']));library={o.name:o for o in ground if o.parent is None};placed=[]
    def place(kind,name,loc,yaw=0,scale=(1,1,1)):
        root=library[kind];copies={}
        for ob in [root]+list(root.children_recursive):
            cp=ob.copy();bpy.context.collection.objects.link(cp);copies[ob]=cp
        for ob,cp in copies.items():cp.parent=copies.get(ob.parent);cp.matrix_basis=ob.matrix_basis.copy();cp.name=name+'__'+ob.name
        rt=copies[root];rt.location=loc;rt.rotation_mode='XYZ';rt.rotation_euler=(0,0,math.radians(yaw));rt.scale=scale;placed.extend(copies.values());return rt
    for i in range(-8,27):place('Road_Straight_A',f'Road_{i}',(i*6.096,curb_y-.4572-3.6576,grade),90)
    openings=[]
    for i,row in enumerate(houses):
        d=row['meta']['driveway'];dx=d['x']+row['location'][0];scale=d['width']/3.048
        openings.append((dx-d['width'],dx+d['width']))
        place('Curb_DrivewayCut',f'DriveCut_{i}',(dx,curb_y,grade),90,(1,scale,1))
        place('Driveway_Apron',f'Apron_{i}',(dx,curb_y+.1524,grade),90,(1,scale,1))
        place('Lawn_DriveWings',f'ApronSod_{i}',(dx,curb_y+.1524,grade),90,(1,scale,1))
    intervals=[];start=-48
    for lo,hi in sorted(openings):intervals.append((start,lo));start=hi
    intervals.append((start,163))
    for i,(lo,hi) in enumerate(intervals):
        count=math.ceil((hi-lo)/3.048);length=(hi-lo)/count
        for j in range(count):place('Curb_Straight',f'Curb_{i}_{j}',(lo+(j+.5)*length,curb_y,grade),90,(1,length/3.048,1))
    walks=[]
    for i in range(-32,108):
        rt=place('Sidewalk_A',f'Sidewalk_{i}',(i*1.524,walk_y,grade),90);walks.extend([rt,*rt.children_recursive])
    def lawn_rect(x0,x1,y0,y1,label):
        if x1-x0<.02 or y1-y0<.02:return
        nx=math.ceil((x1-x0)/6.096);ny=math.ceil((y1-y0)/6.096);dx=(x1-x0)/nx;dy=(y1-y0)/ny
        for ix in range(nx):
            for iy in range(ny):
                sx=dx/6.096;angle=math.atan(.004/sx);base=.16264
                rt=place('Lawn_Field',f'{label}_{ix}_{iy}',(x0+ix*dx-math.sin(angle)*base,y0+(iy+.5)*dy,-math.cos(angle)*base),scale=(sx,dy/6.096,1));rt.rotation_euler.y=angle
    for i,(lo,hi) in enumerate(intervals):lawn_rect(lo,hi,curb_y+.1524,walk_y,'PlantingStrip'+str(i))
    # Leave the exported descending drives and integral garage voids open.
    for i,row in enumerate(houses):
        m=row['meta'];d=m['driveway'];x,y,z=row['location'];lo=x-13 if i else -40;hi=x+13 if i<3 else 155
        dx=d['x']+x;w=d['width']/2+.30;back=d['back']+y+(6.20 if m['spec']['garage']['kind']=='integral' else .12)
        lawn_rect(lo,dx-w,walk_y+1.524,30,'LotLeft'+str(i));lawn_rect(dx+w,hi,walk_y+1.524,30,'LotRight'+str(i));lawn_rect(dx-w,dx+w,back,30,'LotBack'+str(i))
    south_curb=curb_y-2*(.4572+3.6576);south_walk=south_curb-.1524-1.8288
    for i in range(-16,54):place('Curb_Straight',f'SouthCurb_{i}',(i*3.048,south_curb,grade),-90)
    for i in range(-32,108):
        rt=place('Sidewalk_A',f'SouthWalk_{i}',(i*1.524,south_walk,grade),-90);walks.extend([rt,*rt.children_recursive])
    lawn_rect(-40,155,south_walk,south_curb-.1524,'SouthStrip');lawn_rect(-40,155,-32,south_walk-1.524,'SouthLawns')
    for ob in ground:bpy.data.objects.remove(ob,do_unlink=True)
    for row in houses:
        meta=row['meta'];m=meta['blocks'][0];x,y,z=row['location'];d=meta['driveway']
        for i,xx in enumerate((m['x0']+.8,m['x1']-.8)):
            if abs(xx-d['x'])<d['width']/2+1.0:continue
            shrubs=imported(Path(context[3]['source']))
            for rt in [o for o in shrubs if o.parent not in shrubs]:
                descendants={rt,*rt.children_recursive};keep=('hydrangea' if i else 'boxwood') in rt.name.lower()
                if not keep:
                    for ob in descendants:bpy.data.objects.remove(ob,do_unlink=True)
                else:move(descendants,(x+xx,y+m['y0']-.7,0))
    tree=imported(Path(context[1]['source']));move(tree,(66,17,0))
    tree=imported(Path(context[4]['source']));move(tree,(14,12,0),25)
    # Mature back-lot crowns break the empty horizon without covering the
    # staggered fronts. Each is another untouched instance of its own export.
    for index,location,yaw in ((1,(-10,17,0),70),(4,(39,20,0),115),(1,(94,19,0),150),(4,(119,22,0),210)):
        tree=imported(Path(context[index]['source']));move(tree,location,yaw)
    # The pickup rests on the second house's level carport drive, not a ramp.
    row=houses[1];d=row['meta']['driveway'];x,y,z=row['location'];cx=x+d['x'];cy=y+d['back']-3.5
    pickup=imported(Path(context[2]['source']));move(pickup,(cx,cy,0),180)
    from check_mesh import surface
    drive=surface([o for o in groups[1] if o.type=='MESH'])
    car_hit=drive.ray_cast(Vector((cx,cy,2)),Vector((0,0,-1)),4);hit_car=car_hit[0];assert hit_car is not None
    center=Vector((cx,cy,0));tilt=Matrix.Translation(center)@Matrix.Rotation(math.atan2(-car_hit[1].y,car_hit[1].z),4,'X')@Matrix.Translation(-center)
    for ob in pickup:
        if ob.parent not in pickup:ob.matrix_world=tilt@ob.matrix_world
    move(pickup,(0,0,hit_car.z))
    camera=setup('BLENDER_WORKBENCH' if a.layout_only else 'CYCLES',a.samples);bpy.data.objects.remove(bpy.data.objects['Presentation grade, excluded from asset'],do_unlink=True)
    # The finite lots must not reveal the sky's blue lower hemisphere beyond
    # their edge. Reuse the exported lawn on the distant presentation plane,
    # as in the Cape street; it never becomes house geometry.
    lawn=next(m for o in placed if o.type=='MESH' for m in o.data.materials if m.name=='Lawn')
    bpy.ops.mesh.primitive_plane_add(size=2000,location=(0,0,-.25));far=bpy.context.object;far.name='Distant presentation lawn';far.data.materials.append(lawn)
    from kit.tiling import world_uv
    world_uv(far,3.048);tint=far.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
    for c in tint.data:c.color=(.95,.95,.95,1)
    # Stand on the houses' own walk, looking along their fronts with a normal
    # full-frame lens. A panoramic vertical crop keeps the lawn in a low band;
    # the nearest living wing continues naturally beyond the left frame edge.
    camera.location=(-20,-7,1.6);target=Vector((80,11,8))
    camera.data.lens=35
    sc=bpy.context.scene;sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/2.6);sc.render.resolution_percentage=100
    walk=surface([o for o in walks if o.type=='MESH']);hit=walk.ray_cast(Vector((camera.location.x,camera.location.y,2)),Vector((0,0,-1)),3)[0];assert hit is not None
    assert walk_y<camera.location.y<walk_y+1.524,'Camera must stand on the house-side walk'
    camera.location.z=hit.z+1.6;camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
    from bpy_extras.object_utils import world_to_camera_view
    def projected(objects):
        p=[]
        for ob in objects:
            if ob.type!='MESH':continue
            # The joined static mesh also contains the drive and retaining
            # cheeks. Those are not the building's apparent frame width.
            ids={vi for poly in ob.data.polygons if ob.data.materials[poly.material_index].name.split('.')[0]!='CapeConcrete' for vi in poly.vertices}
            p.extend(world_to_camera_view(sc,camera,ob.matrix_world@ob.data.vertices[i].co) for i in ids)
        return [min(q.x for q in p),max(q.x for q in p)]
    bpy.context.view_layer.update()
    for row,objects in zip(houses,groups):
        bounds=projected(objects);visible=[max(0,bounds[0]),min(1,bounds[1])]
        row.update(projected_frame_width=bounds[1]-bounds[0],projected_frame_bounds_x=bounds,visible_frame_width=max(0,visible[1]-visible[0]),visible_frame_bounds_x=visible,framing_scope='Architecture excluding concrete drive/retaining walls; raw and frame-clipped extents reported separately')
        row.pop('meta')
    bpy.data.objects['Afternoon sun'].rotation_euler=Vector((.35,.9,-.65)).to_track_quat('-Z','Y').to_euler()
    next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=.12
    if a.layout_only:
        proof=dict(houses=houses,camera=list(camera.location),target=list(target),lens=camera.data.lens,eye_height_above_sidewalk_m=camera.location.z-hit.z)
        Path('build/split/delivery/street-layout.json').write_text(json.dumps(proof,indent=2));print('SPLIT_STREET_LAYOUT',proof);return
    out=Path('renders/split/street');out.mkdir(parents=True,exist_ok=True);sc.render.filepath=str((out/'street.png').resolve());bpy.ops.render.render(write_still=True)
    for row in houses:assert bundle_hash(Path(row['source']))==row['bundle_sha256']
    for row in context:assert hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['sha256']
    recipe=hashlib.sha256(b''.join((HERE/n).read_bytes() for n in ('split_street.py','cape_street.py','street.py','render.py'))).hexdigest()
    (out/'provenance.json').write_text(json.dumps(dict(houses=houses,context=context,camera=list(camera.location),target=list(target),lens=camera.data.lens,sensor_width_mm=camera.data.sensor_width,aspect=2.6,camera_support='House-side Sidewalk_A; measured vertical ray hit',sidewalk_surface_z_m=hit.z,eye_height_above_sidewalk_m=camera.location.z-hit.z,pickup_drive_surface_z_m=hit_car.z,engine='CYCLES',recipe_sha256=recipe,image_sha256=hashlib.sha256((out/'street.png').read_bytes()).hexdigest(),render_only=True),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=48);p.add_argument('--layout-only',action='store_true');main(p.parse_args(sys.argv[sys.argv.index('--')+1:]))
