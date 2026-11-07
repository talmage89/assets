"""Town setting and weekday actors, read-only library imports.

Repeated mesh data is shared. Cars never count toward the garage's budget.
This is presentation context and a site placement manifest, not new buildings.
"""
import hashlib
import json
import math
from pathlib import Path
import bpy
from mathutils import Vector,Quaternion
import geometry as G
from plan import FLOOR,SPAN,TEE,deck_z
ROOT=Path(__file__).resolve().parents[2]


def imported(path,name):
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(Path(path).resolve()));obs=set(bpy.context.scene.objects)-before
    r=G.root(name)
    for o in obs:
        if o.parent not in obs:o.parent=r
    return r


def town(p,garage_root,with_cars=True):
    rt=G.root('TownContext');L,W=p['length'],p['width'];municipal=p['system']=='precast'
    G.palette()
    b=G.Mesh('Continuing library streets and paving',rt)
    # Native Ground tiling PBR remains byte-identical. Road widths here match
    # Downtown's 40ft two-way / parallel parking street envelope.
    sx=L/2+12.2;sy=W/2+12.2;rw=12.192
    b.box((0,0,-.24),(460,460,.25),'Lawn')
    # Street strips stop at the two perpendicular lanes; no duplicate skins.
    for yy in (-sy,sy):b.box((0,yy,-.0924),(320,rw,.12),'Asphalt')
    for xx in (-sx,sx):
        for y0,y1 in ((-160,-sy-rw/2),(-sy+rw/2,sy-rw/2),(sy+rw/2,160)):
            b.box((xx,(y0+y1)/2,-.0924),(rw,y1-y0,.12),'Asphalt')
    # Parking property apron and perimeter walks meet native street datums.
    b.box((0,-W/2-2.1,-.08),(L+10,4.2,.16),'Deck')
    b.box((0,W/2+2.2,-.08),(L+10,4.4,.16),'Deck')
    for sign in (-1,1):b.box((sign*(L/2+5.1),0,-.08),(4.2,W+8.4,.16),'Deck')
    b.finish()
    # Native curb and sidewalk pieces, extracted from the delivered library.
    ground=imported(ROOT/'ground/export/Ground.glb','Ground templates')
    templates={o.name.split('.')[0]:o for o in ground.children}
    curb=templates.get('Curb_Straight');walk=templates.get('Sidewalk_A')
    # Imports carry inspection-layout positions; replace root transforms.
    if curb:
        for sign in (-1,1):
            for i in range(-38,39):
                xx=i*3.048
                # Crossing gaps around the connecting streets and actual entry.
                if min(abs(xx-sx),abs(xx+sx))<rw/2+2.0:continue
                if sign==-1 and abs(xx-(L/2-p['end_length']/2))<4.0:continue
                rr=G.clone(curb,f'NativeCurb_{sign}_{i}',(xx,sign*(sy-rw/2),-.1524),90 if sign<0 else -90,rt)
            for i in range(-30,31):
                yy=i*3.048
                if min(abs(yy-sy),abs(yy+sy))<rw/2+2.0:continue
                G.clone(curb,f'CrossCurb_{sign}_{i}',(sign*(sx-rw/2),yy,-.1524),0 if sign<0 else 180,rt)
    for o in [ground,*ground.children_recursive]:bpy.data.objects.remove(o,do_unlink=True)
    # Source-built native block faces: alternate frontage, real rear alleys and
    # returns. Their quick source palette is stated honestly at this form gate.
    block=imported('build/context/downtown.glb','Native Main Street row')
    block.parent=rt;block.location=(0,-sy-rw/2-3.2,0);block.rotation_euler.z=math.pi
    for i,(pos,yaw) in enumerate([((0,W/2+15,0),0),((-L/2-18,38,0),math.pi/2),((L/2+18,38,0),-math.pi/2),((75,-sy-9.3,0),math.pi),((-75,-sy-9.3,0),math.pi)]):
        G.clone(block,'Continuing block '+str(i),pos,math.degrees(yaw),rt)
    if not municipal:
        commercial=imported('build/context/commercial.glb','Native commercial center');commercial.parent=rt
        # Original row has frontage about Y=-14; its lot is not used here.
        commercial.location=(0,58,0);commercial.rotation_euler.z=math.pi
    # Delivered lights with native anchor origins and emitter sockets.
    light=imported(ROOT/'street-light/export/StreetLight.glb','Library street light');light.parent=rt
    light.location=(-L/2-4,-W/2-3.2,0)
    for i,(x,y,yaw) in enumerate([(L/2+3,-W/2-3.2,0),(-15,-sy-rw/2-1.4,180),(15,-sy-rw/2-1.4,180),(-L/2-5,26,90),(L/2+5,26,-90)]):
        G.clone(light,'Library pole '+str(i),(x,y,0),yaw,rt)
    # Two species retain their actual alpha-cut leaf cards, no opaque squares.
    for species,positions in [('PinOak',[(-L/2-7,W/2+7),(-L/2-19,-W/2+5),(L/2+18,3),(-45,65),(40,80),(-80,58)]),('RedMaple',[(-18,W/2+7),(18,W/2+7),(L/2+6,W/2+7),(-70,-60),(72,-60),(80,70)])]:
        tree=imported(ROOT/'trees/export'/(species+'.glb'),'Library '+species);tree.parent=rt;tree.location=(*positions[0],0)
        for i,(x,y) in enumerate(positions[1:]):G.clone(tree,species+str(i),(x,y,0),(i*71+p['seed'])%360,rt)
    actors=[];car_templates=[]
    if with_cars:
        for kind in ('hatchback','crossover'):
            cr=imported('build/context/'+kind+'.glb','Car template '+kind);car_templates.append(cr)
        # Native sedan delivery adds an independently shaped body. Its shaders
        # are the actual baked atlas; no regeneration or decimation is performed.
        car_templates.append(imported(ROOT/'cars/export/AlderS240.glb','Car template sedan'))
        for cr in car_templates:
            # Context-only join: retain all native vertices/materials while
            # reducing hundreds of parked assemblies to one mesh each.
            bpy.context.view_layer.update();obs=[o for o in cr.children_recursive if o.type=='MESH']
            for o in obs:
                xf=cr.matrix_world.inverted()@o.matrix_world;o.data=o.data.copy();o.data.transform(xf);o.parent=cr;o.matrix_basis.identity();o.matrix_parent_inverse.identity()
            bpy.ops.object.select_all(action='DESELECT')
            for o in obs:o.select_set(True)
            bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join()
            for o in list(cr.children_recursive):
                if o.type!='MESH':bpy.data.objects.remove(o,do_unlink=True)
        colors=[(.035,.07,.11),(.31,.018,.012),(.42,.43,.40),(.028,.032,.032),(.62,.60,.53),(.16,.22,.18)]
        paints={}
        for i,s in enumerate(p['stalls']):
            if not s['occupied']:continue
            source=car_templates[s['car']%len(car_templates)]
            car=G.clone(source,'Parked '+s['id'],(s['x'],s['y'],s['z']),s['yaw'],rt)
            normal=Vector((-s['slope_x'],-s['crossfall'],1)).normalized()
            car.rotation_mode='QUATERNION';car.rotation_quaternion=Vector((0,0,1)).rotation_difference(normal)@Quaternion((0,0,1),math.radians(s['yaw']))
            # Shared car geometry, six reusable form paint references.
            for o in car.children_recursive:
                if o.type!='MESH':continue
                for slot in o.material_slots:
                    m=slot.material
                    if m is None or 'paint' not in m.name.lower() or 'Context' not in m.name:continue
                    key=(m.name,s['car'])
                    if key not in paints:
                        ma=m.copy();ma.name='Parked form paint '+str(key)
                        ma.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*colors[s['car']],1);paints[key]=ma
                    slot.link='OBJECT';slot.material=paints[key]
            actors.append(dict(socket='Stall_'+s['id'],kind=source.name,triangles=G.triangles([source,*source.children_recursive]),position=[s['x'],s['y'],s['z']]))
        for i,x in enumerate((-28,-15,4,19,32)):
            s=car_templates[i%3];G.clone(s,'Street parked '+str(i),(x,-sy+rw/2-1.2,-.03),90,rt)
        for source in car_templates:
            for o in [source,*source.children_recursive]:bpy.data.objects.remove(o,do_unlink=True)
    bpy.context.view_layer.update()
    return dict(root=rt,actors=actors,actor_triangles=sum(r['triangles'] for r in actors),
                context_triangles=G.triangles([rt,*rt.children_recursive]),scope='Read-only native library setting; actors remain separate from garage exports.')
