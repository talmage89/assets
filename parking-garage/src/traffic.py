"""Seeded four-model weekday traffic with reusable factory paint uniforms.

Context finishes are explicitly stock PBR uniforms on the native car meshes.
No car-family delivery is rewritten and paint choices cost no new images.
"""
import json,math,random,runpy
from pathlib import Path
import bpy
from mathutils import Vector,Quaternion,Matrix
import geometry as G
from traffic_fit import vertices,lateral as fit_lateral
from setting import imported
from plan import deck_z
ROOT=Path(__file__).resolve().parents[2]
FAMILY=runpy.run_path(str(ROOT/'cars/src/pickup_spec.py'))
COLORS=dict(FAMILY['COLORS'],Burgundy=(.25,.019,.012),Forest=(.038,.085,.057),Sand=(.36,.29,.18))
# 2010 DuPont North America: white 21, black 18, silver 17, red 11.
# Remaining 33 is an authored gray/blue/green/natural mix, not fleet census.
WEIGHTS=[21,18,17,15,9,11,3,6]


def pickup():
    cr=imported(ROOT/'cars/export/AlderC150.glb','Traffic pickup template');cr['native_model']='AlderC150';finishes={}
    # Stock context finishes avoid baking duplicate color textures. Imported
    # native mesh normals/parts remain; no source model is approximated.
    for ob in cr.children_recursive:
        if ob.type!='MESH':continue
        for slot in ob.material_slots:
            old=slot.material
            if old is None:continue
            key=old.name.lower()
            col,rough,metal=(.018,.020,.021),.65,0
            if 'paint' in key:col,rough,metal=COLORS['Porcelain'],.26,.1
            elif 'glass' in key:col,rough,metal=(.025,.043,.052),.10,.1
            elif 'lamp' in key:col,rough,metal=(.32,.33,.30),.24,.2
            elif 'metal' in key:col,rough,metal=(.22,.24,.24),.35,.7
            if key not in finishes:finishes[key]=G.material('Traffic pickup '+key,col,rough,metal)
            slot.link='OBJECT';slot.material=finishes[key]
    # Collapse only context hierarchy. Preserve applied native transform.
    bpy.context.view_layer.update();obs=[o for o in cr.children_recursive if o.type=='MESH']
    for ob in obs:
        xf=cr.matrix_world.inverted()@ob.matrix_world;ob.data=ob.data.copy();ob.data.transform(xf)
        ob.parent=cr;ob.matrix_basis=Matrix.Identity(4);ob.matrix_parent_inverse=Matrix.Identity(4)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in obs:ob.select_set(True)
    bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join()
    for ob in list(cr.children_recursive):
        if ob.type!='MESH':bpy.data.objects.remove(ob,do_unlink=True)
    return cr


def revise(rt,p):
    old=json.loads(Path(f"build/lookdev/actors-{p['seed']}.json").read_text());templates={}
    for row in old['actors']:
        if row['category']!='garage' or row['kind'] in templates:continue
        source=bpy.data.objects['Parked '+row['socket'].removeprefix('Stall_')]
        templates[row['kind']]=G.clone(source,'Traffic template '+str(len(templates)))
        templates[row['kind']]['native_model']={'Car template hatchback':'AlderH120','Car template crossover':'AlderX220','Car template sedan':'AlderS240'}[row['kind']]
    templates['pickup']=pickup();models=[templates[k] for k in ('Car template hatchback','Car template crossover','Car template sedan','pickup')];paints={};actors=[]
    bpy.context.view_layer.update();envelopes=[vertices(source) for source in models]
    for ob in list(rt.children):
        if ob.name.startswith(('Parked ','Street parked ','Entry queue vehicle')):
            for child in reversed([ob,*ob.children_recursive]):bpy.data.objects.remove(child,do_unlink=True)
    rng=random.Random(p['seed']+5160)
    def spawn(name,position,yaw,category,index=None,normal=None):
        source=models[rng.choices(range(4),[36,24,32,8])[0] if index is None else index]
        car=G.clone(source,name,position,yaw,rt)
        if normal is not None:
            car.rotation_mode='QUATERNION';car.rotation_quaternion=Vector((0,0,1)).rotation_difference(normal)@Quaternion((0,0,1),math.radians(yaw))
        paint=rng.choices(list(COLORS),WEIGHTS)[0]
        for ob in car.children_recursive:
            if ob.type!='MESH':continue
            for slot in ob.material_slots:
                ma=slot.material
                if ma is None or not ('paint' in ma.name.lower() or ma.get('paint_decode')):continue
                if paint not in paints:
                    m=G.material('Weekday factory '+paint,COLORS[paint],.28,FAMILY['PAINT_METAL'].get(paint,.16))
                    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Coat Weight'].default_value=.7;bs.inputs['Coat Roughness'].default_value=.12
                    paints[paint]=m
                slot.link='OBJECT';slot.material=paints[paint]
        actors.append(dict(name=name,category=category,kind=source['native_model'],paint=paint,position=list(position),yaw=yaw,triangles=G.triangles([car,*car.children_recursive])))
        return car
    for s in p['stalls']:
        if not s['occupied']:continue
        # Pickups fit standard 18ft stalls only; compact reservations use the
        # two shorter families. Offsets stay inside each accepted envelope.
        index=0 if s['compact'] else rng.choices(range(4),[34,24,32,10])[0]
        bias=.35 if index==3 else .12
        lateral=.045 if index==3 else .12
        dx=rng.uniform(-lateral,lateral);dy=(bias if s['yaw']==180 else -bias)+rng.uniform(-.10,.10)
        normal=Vector((-s['slope_x'],-s['crossfall'],1)).normalized()
        angle=.45 if index==3 else 1.25
        dx,angle=fit_lateral(envelopes[index],s,normal,rng.uniform(-angle,angle),dx)
        x,y=s['x']+dx,s['y']+dy;z=deck_z(p,s['level'],x,y,s['ramp'])
        spawn('Parked '+s['id'],(x,y,z),s['yaw']+angle,'garage',index,normal)
    street(rt,p,rng,spawn)
    for row in actors:
        car=bpy.data.objects[row['name']];row['position']=list(car.location)
        if car.get('wheel_support'):row['wheel_support']=json.loads(car['wheel_support'])
    for source in models:
        for ob in reversed([source,*source.children_recursive]):bpy.data.objects.remove(ob,do_unlink=True)
    bpy.context.view_layer.update()
    return dict(actors=actors,actor_triangles=sum(r['triangles'] for r in actors),context_triangles=G.triangles([rt,*rt.children_recursive]))


def street(rt,p,rng,spawn):
    L,W=p['length'],p['width'];municipal=p['system']=='precast';sy=W/2+12.2 if municipal else 48.8
    ex=L/2-p['end_length']/2;sx=L/2+14.2
    eye=Vector((-L/2-(41 if municipal else 36),-W/2-(19.896 if municipal else 22)))
    target=Vector((ex-1.65,-W/2-3.3));direction=target-eye
    def visible_entry(x,y):
        delta=Vector((x,y))-eye;t=delta.dot(direction)/direction.length_squared
        return not (0<t<1 and abs(delta.x*direction.y-delta.y*direction.x)/direction.length<3.1)
    # Metered cars occupy the visible garage-side curb as well as the far
    # curb. Leave the driveway, crossings and sight triangles open.
    meters=G.Mesh('Garage curb parking meters',rt)
    for i,x in enumerate((-33,-24,-13,-3,8,18,46,57)):
        if x>L/2+8 or abs(x-ex)<8:continue
        if visible_entry(x,-sy+4.85):spawn('Meter parked '+str(i),(x,-sy+4.85,-.14605+.02*(6.096-4.85)),-90,'street',normal=Vector((0,.02,1)).normalized())
        yy=-sy+6.75
        meters.tube([(x,yy,0),(x,yy,1.17)],.026,'Steel')
        meters.box((x,yy,1.29),(.20,.15,.25),'Steel')
        meters.box((x,yy-.079,1.33),(.13,.008,.075),'Seal')
        meters.box((x+.06,yy-.083,1.23),(.045,.012,.016),'Steel')
    meters.finish()
    for i,yy in enumerate((-W/2+1,-W/2+9,8,17)):
        spawn('Cross street parked '+str(i),(-sx+4.85,yy,-.14605+.02*(6.096-4.85)),180,'street',normal=Vector((.02,0,1)).normalized())
    for i,(x,y,yaw) in enumerate([(-20,-sy-2.0,90),(13,-sy+2.0,-90),(-sx-2.0,12,0)]):
        # Street crown is .02 away from either gutter, sampled analytically
        # from the same native 40ft road profile used by setting.town.
        normal=Vector((-.02,0,1)) if i==2 else Vector((0,-.02 if i==0 else .02,1))
        spawn('Street traffic '+str(i),(x,y,-.14605+.02*(6.096-2)),yaw,'traffic',normal=normal.normalized())
    if not municipal:
        y0=-sy+6.096;y1=-W/2-6.1;cy=(y0+y1)/2
        for row in (-1,1):
            for i in range(16):
                xx=-L/2+2.5+i*2.5908;yy=cy+row*6.4008
                # A broad driveway/sight corridor makes the entry and queue
                # legible in the unchanged 35mm public hero.
                if xx>ex-13 or rng.random()>.70:continue
                if not visible_entry(xx,yy):continue
                z=-.14605+(yy-y0)*.14605/(y1-y0)
                spawn(f'Court parked {row} {i}',(xx,yy,z),180 if row==-1 else 0,'surface court',normal=Vector((0,-.14605/(y1-y0),1)).normalized())
    from town_detail import fit_queue
    queued=spawn('Entry queue vehicle',(ex-1.65,-W/2-3.3,0),180,'entry queue',0)
    support=fit_queue(queued)
    # Write true contact-adjusted root coordinates back into the actor row.
    queued['wheel_support']=json.dumps(support)
    block=next(o for o in rt.children if o.name.startswith('Native Main Street row'))
    if municipal:
        # Extend the west street with two actual buildings, leaving the
        # photographer's crossing clear and avoiding an overlapping full row.
        buildings=[o for o in block.children if any(c.type=='MESH' for c in o.children_recursive)]
        for i,yy in enumerate((0,15)):
            G.clone(buildings[i%len(buildings)],'West frontage building '+str(i),(-sx-6.096-3.2,yy,0),90,rt)
