"""Town setting and weekday actors, read-only library imports.

Repeated mesh data is shared. Cars never count toward the garage's budget.
This is presentation context and a site placement manifest, not new buildings.
"""
import hashlib
import json
import math
import random
from pathlib import Path
import bpy
from mathutils import Vector,Quaternion,Matrix
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
    sx=L/2+14.2;east_sx=sx if municipal else L/2+50
    sy=W/2+12.2 if municipal else 48.8;rw=12.192
    xr=[(-230,-sx-rw/2),(-sx+rw/2,east_sx-rw/2),(east_sx+rw/2,230)]
    yr=[(-230,-sy-rw/2),(-sy+rw/2,sy-rw/2),(sy+rw/2,230)]
    for i,(x0,x1) in enumerate(xr):
        for j,(y0,y1) in enumerate(yr):
            if i==j==1:continue
            b.box(((x0+x1)/2,(y0+y1)/2,-.125),(x1-x0,y1-y0,.25),'Lawn')
    # Continuous owned parcel underneath the assembly and service courts.
    # The commercial block is deeper than the garage; it must not end at its
    # rear apron and expose the world beneath the scene.
    px0=-sx+rw/2;px1=east_sx-rw/2
    b.box(((px0+px1)/2,0,-.22605),(px1-px0,2*(sy-rw/2),.16),'Asphalt')
    if not municipal:
        y0=W/2+6.1;y1=sy-rw/2
        b.box(((px0+L/2+8.1)/2,(y0+y1)/2,-.125),(L/2+8.1-px0,y1-y0,.25),'Lawn')
    b.box((0,W/2+5.25,-.125),(L+10,1.7,.25),'Lawn')
    # Street strips stop at the two perpendicular lanes; no duplicate skins.
    def road(x0,x1,y0,y1,axis,center):
        edge=-.14605
        coords=[y0,center,y1] if axis==1 else [x0,center,x1]
        for a,c in zip(coords,coords[1:]):
            z=lambda q:edge+.02*(rw/2-abs(q-center))
            poly=[(x0,a,z(a)-.12),(x1,a,z(a)-.12),(x1,c,z(c)-.12),(x0,c,z(c)-.12)] if axis==1 else [(a,y0,z(a)-.12),(c,y0,z(c)-.12),(c,y1,z(c)-.12),(a,y1,z(a)-.12)]
            b.prism(poly,(0,0,.12),'Asphalt')
    for yy in (-sy,sy):road(-160,160,yy-rw/2,yy+rw/2,1,yy)
    for xx in (-sx,east_sx):
        for y0,y1 in ((-160,-sy-rw/2),(-sy+rw/2,sy-rw/2),(sy+rw/2,160)):
            road(xx-rw/2,xx+rw/2,y0,y1,0,xx)
    # Parking property apron and perimeter walks meet native street datums.
    # Front apron belongs to the garage export, including its accessible walk.
    b.box((0,W/2+2.2,-.08),(L+10,4.4,.16),'Deck')
    surface_stalls=[]
    if not municipal:
        # Commercial superblock: the native shop row and garage share a
        # service/arrival court. Roads surround the larger parcel rather than
        # cutting through the original center's stores.
        b.box((L/2+12.55,0,-.08),(8.9,73.2,.16),'Asphalt')
        b.box((L/2+17.0,0,-.08),(1.6,73.2,.16),'Deck')
        y0=-sy+rw/2;y1=-W/2-6.1;left=-L/2-5;right=L/2+17.8
        court_z=lambda y:-.14605+(y-y0)*.14605/(y1-y0)
        b.prism([(left,y0,court_z(y0)-.16),(right,y0,court_z(y0)-.16),(right,y1,court_z(y1)-.16),(left,y1,court_z(y1)-.16)],(0,0,.16),'Asphalt')
        rng=random.Random(p['seed']+811);cy=(y0+y1)/2
        for row in (-1,1):
            for i in range(16):
                xx=-L/2+2.5+i*2.5908;yy=cy+row*6.4008
                surface_stalls.append(dict(id=f'Surface-{row}-{i}',x=xx,y=yy,z=court_z(yy),yaw=180 if row==-1 else 0,occupied=rng.random()<.8,car=rng.randrange(6),slope_x=0,crossfall=.14605/(y1-y0)))
                for xline in (xx-1.2954,xx+1.2954):
                    b.quad([(xline-.05,yy-2.7432,court_z(yy-2.7432)+.006),(xline+.05,yy-2.7432,court_z(yy-2.7432)+.006),(xline+.05,yy+2.7432,court_z(yy+2.7432)+.006),(xline-.05,yy+2.7432,court_z(yy+2.7432)+.006)])
    for sign in (-1,1):
        b.box((sign*(L/2+6.675),0,-.08),(2.55,W+12.2,.16),'Deck')
        for x0,x1 in ((-160,-sx-rw/2),(-sx+rw/2,east_sx-rw/2),(east_sx+rw/2,160)):
            b.box(((x0+x1)/2,sign*(sy+rw/2+1.6),-.08),(x1-x0,3.2,.16),'Deck')
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
                if min(abs(xx-east_sx),abs(xx+sx))<rw/2+2.0:continue
                if sign==-1 and abs(xx-(L/2-p['end_length']/2))<4.9+1.524:continue
                rr=G.clone(curb,f'NativeCurb_{sign}_{i}',(xx,sign*(sy-rw/2),-.1524),90 if sign<0 else -90,rt)
            for i in range(-30,31):
                yy=i*3.048
                if min(abs(yy-sy),abs(yy+sy))<rw/2+2.0:continue
                G.clone(curb,f'CrossCurb_{sign}_{i}',((-sx+rw/2) if sign<0 else (east_sx-rw/2),yy,-.1524),0 if sign<0 else 180,rt)
    for o in [ground,*ground.children_recursive]:bpy.data.objects.remove(o,do_unlink=True)
    # Source-built native block faces: alternate frontage, real rear alleys and
    # returns. Their quick source palette is stated honestly at this form gate.
    block=imported('build/context/downtown.glb','Native Main Street row')
    block.parent=rt;block.location=(0,-sy-rw/2-3.2,0);block.rotation_euler.z=math.pi
    side_y=75 if municipal else 95
    for i,(pos,yaw) in enumerate([((0,sy+rw/2+3.2,0),0),((-sx-rw/2-3.2,side_y,0),math.pi/2),((east_sx+rw/2+3.2,side_y,0),-math.pi/2),((east_sx+rw/2+33.2,-sy-9.3,0),math.pi),((-sx-rw/2-33.2,-sy-9.3,0),math.pi)]):
        G.clone(block,'Continuing block '+str(i),pos,math.degrees(yaw),rt)
    if not municipal:
        commercial=imported('build/context/commercial.glb','Native commercial center');commercial.parent=rt
        # Original row has frontage about Y=-14; its lot is not used here.
        commercial.location=(L/2+17.6,0,0);commercial.rotation_euler.z=-math.pi/2
    # Delivered lights with native anchor origins and emitter sockets.
    light=imported(ROOT/'street-light/export/StreetLight.glb','Library street light');light.parent=rt
    light.location=(-L/2-4,-W/2-3.2,0)
    for i,(x,y,yaw) in enumerate([(L/2+3,-W/2-3.2,0),(-15,-sy-rw/2-1.4,180),(15,-sy-rw/2-1.4,180),(-L/2-5,26,90),(L/2+5,26,-90)]):
        G.clone(light,'Library pole '+str(i),(x,y,0),yaw,rt)
    # Two species retain their actual alpha-cut leaf cards, no opaque squares.
    for species,positions in [('PinOak',[(-L/2+5,W/2+5.2),(-L/2-25,-W/2+5),(L/2+25,3),(-45,65),(40,80),(-80,58)]),('RedMaple',[(-18,W/2+5.2),(18,W/2+5.2),(L/2-5,W/2+5.2),(-70,-60),(72,-60),(80,70)])]:
        tree=imported(ROOT/'trees/export'/(species+'.glb'),'Library '+species);tree.parent=rt;tree.location=(*positions[0],0)
        for i,(x,y) in enumerate(positions[1:]):G.clone(tree,species+str(i),(x,y,0),(i*71+p['seed'])%360,rt)
    actors=[];car_templates=[]
    if with_cars:
        for kind in ('hatchback','crossover'):
            cr=imported('build/context/'+kind+'.glb','Car template '+kind);car_templates.append(cr)
            # A procedural native shader can export an unlinked white factor.
            # Form actors get explicit stock finishes, including dark rubber
            # and glazing. Their source geometry is retained unchanged.
            mats={m for o in cr.children_recursive if o.type=='MESH' for m in o.data.materials if m}
            for m in mats:
                name=m.name.lower();color=(.025,.028,.027);rough=.55;metal=0
                if 'paint' in name:color=(.18,.24,.26);rough=.30;metal=.25
                elif 'rubber' in name or 'bumper' in name:color=(.012,.013,.014);rough=.78
                elif any(s in name for s in ('windshield','glass','lamp lens')):color=(.025,.040,.045);rough=.12
                elif 'wheel' in name or 'chrome' in name or 'metal' in name:color=(.32,.34,.33);rough=.32;metal=.8
                elif 'red' in name or 'phosphor' in name:color=(.25,.008,.005);rough=.24
                elif 'signature' in name:color=(.60,.62,.58);rough=.20
                elif 'plate' in name:color=(.42,.43,.39)
                nodes=m.node_tree.nodes;nodes.clear();bs=nodes.new('ShaderNodeBsdfPrincipled');out=nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(bs.outputs['BSDF'],out.inputs['Surface'])
                bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
        # Native sedan delivery adds an independently shaped body. Its shaders
        # are the actual baked atlas; no regeneration or decimation is performed.
        car_templates.append(imported(ROOT/'cars/export/AlderS240.glb','Car template sedan'))
        for cr in car_templates:
            for mat in {m for o in cr.children_recursive if o.type=='MESH' for m in o.data.materials if m and m.use_nodes}:
                for bs in [n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED']:
                    for key in ('Emission Color','Emission Strength'):
                        for link in list(bs.inputs[key].links):mat.node_tree.links.remove(link)
                    bs.inputs['Emission Strength'].default_value=0;bs.inputs['Emission Color'].default_value=(0,0,0,1)
            # Context-only join: retain all native vertices/materials while
            # reducing hundreds of parked assemblies to one mesh each.
            bpy.context.view_layer.update();obs=[o for o in cr.children_recursive if o.type=='MESH']
            for o in obs:
                xf=cr.matrix_world.inverted()@o.matrix_world;o.data=o.data.copy();o.data.transform(xf);o.parent=cr;o.matrix_basis=Matrix.Identity(4);o.matrix_parent_inverse=Matrix.Identity(4)
            bpy.ops.object.select_all(action='DESELECT')
            for o in obs:o.select_set(True)
            bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join()
            for o in list(cr.children_recursive):
                if o.type!='MESH':bpy.data.objects.remove(o,do_unlink=True)
        colors=[(.035,.07,.11),(.31,.018,.012),(.42,.43,.40),(.028,.032,.032),(.62,.60,.53),(.16,.22,.18)]
        paints={}
        for i,s in enumerate(p['stalls']+surface_stalls):
            if not s['occupied']:continue
            source=car_templates[s['car']%len(car_templates)]
            bias=.12 if s['yaw']==180 else -.12
            position=(s['x'],s['y']+bias,s['z']+s['crossfall']*bias)
            car=G.clone(source,'Parked '+s['id'],position,s['yaw'],rt)
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
            actors.append(dict(socket='Stall_'+s['id'],category='surface court' if s['id'].startswith('Surface') else 'garage',kind=source.name,triangles=G.triangles([source,*source.children_recursive]),position=list(position),parking_bias_m=bias))
        for i,x in enumerate((-28,-15,4,19,32)):
            # A full weekday frontage still leaves the garage access clear.
            if abs(x-(L/2-p['end_length']/2))<7.4:continue
            s=car_templates[i%3];G.clone(s,'Street parked '+str(i),(x,-sy+rw/2-1.2,-.12205),-90,rt)
            actors.append(dict(socket=None,category='street',kind=s.name,triangles=G.triangles([s,*s.children_recursive]),position=[x,-sy+rw/2-1.2,-.12205],yaw=-90))
        for source in car_templates:
            for o in [source,*source.children_recursive]:bpy.data.objects.remove(o,do_unlink=True)
    bpy.context.view_layer.update()
    return dict(root=rt,actors=actors,actor_triangles=sum(r['triangles'] for r in actors),
                garage_car_triangles=sum(r['triangles'] for r in actors if r['category']=='garage'),surface_car_triangles=sum(r['triangles'] for r in actors if r['category']=='surface court'),
                street_car_triangles=sum(r['triangles'] for r in actors if r['category']=='street'),
                context_triangles=G.triangles([rt,*rt.children_recursive]),scope='Read-only native library setting; actors remain separate from garage exports.')
