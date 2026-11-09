"""Flat precast assembly for the interior photograph, using our stock kit.

The town garage has a ramp at its middle line; the photo has a flat inverted-T
seat. This calibration specimen keeps the actual sections and 11ft spacing.
Visible central members are measured. Roof continuation outside that crop
supplies surrounding shade, not a claim about the photographed full footprint.
This is an assembly comparator, not a third town garage delivery.
"""
import json,math
from pathlib import Path
import bpy
import geometry as G
import pieces
from plan import garage,TEE,SPAN,FLOOR,DEPTH,STALL
from form import remove_paint
from tee_detail import source
from build import members


def build(layout,tee_count=6,rear_spans=1):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(Path('export/sites/ParkingGarageSite-101.gltf').resolve()));bpy.context.view_layer.update()
    old=bpy.data.objects['Garage_101'];town=bpy.data.objects['TownContext']
    parked=[o for o in town.children if o.name.startswith('Parked ')]
    actor_root=G.root('Comparison parked cars');actors=[]
    for i,x in enumerate((-7.0,-2.7,4.2,8.4)):
        cr=G.clone(parked[(i*41)%len(parked)],'Comparison car '+str(i),(x,12.0,0),180,actor_root)
        actors.append(dict(name=cr.name,triangles=G.triangles(members(cr))))
    for rr in [old,*parked]:
        for ob in reversed(members(rr)):bpy.data.objects.remove(ob,do_unlink=True)
    # The reference looks into a landscaped open lot. Opposing town blocks
    # belong to the delivered garage, not this daylight calibration specimen.
    for rr in list(town.children):
        if rr.name.startswith(('Native Main Street row','Continuing block','Native commercial center')):
            for ob in reversed(members(rr)):bpy.data.objects.remove(ob,do_unlink=True)
    G.palette(Path('textures/lookdev'));rt=G.root('Garage_101',system='precast',stage='Flat assembly calibration specimen')
    assert tee_count>=6 and tee_count%6==0
    assert rear_spans in (1,2)
    L=tee_count*TEE;ymin,ymax=-rear_spans*SPAN,SPAN;W=ymax-ymin;p=garage(101)
    transverse=[-SPAN,0,SPAN,*[-(i+2)*SPAN for i in range(rear_spans-1)]]
    stations=[(i-tee_count//6)*3*TEE for i in range(tee_count//3+1)]
    centers=[(a+c)/2 for a,c in zip(stations,stations[1:])]
    p.update(length=L,width=W,levels=2,tee_count=tee_count,flat_y=-SPAN/2,ramp_y=SPAN/2,ramp_width=SPAN,
        structural_stations=stations,ramp_limits=[-7.5,7.5],joint_y=0,towers=[],stalls=[],pieces=[],drains=[],
        comparison_y_bounds_m=[ymin,ymax],comparison_facade_levels=[0],comparison_origin='Measured central column')
    p['comparison_actors']=actors
    b=G.Mesh('Grade slab comparison',rt);b.box((0,(ymin+ymax)/2,-.08),(L,W,.16),'Deck');b.finish()
    for ix,x in enumerate(stations):
        for iy,y in enumerate(transverse):
            core_index=ix-(len(stations)-3)//2
            rr=G.root(f'ColumnShaft_{core_index}_{iy}',(x,y,0),rt,module_kind='ColumnCorbel');pieces.column(rr)
            for ob in rr.children:
                remove_paint(ob)
                if ob.type=='MESH':
                    for v in ob.data.vertices:
                        if abs(v.co.z-(FLOOR-1.60))<1e-6:v.co.z-=(FLOOR-1.60)*.15
                    ob.data.update()
    for x in centers:
        for y in transverse:
            edge=y in (ymin,ymax)
            rr=G.root(f'Girder_{x}_{y}',(x,y,FLOOR),rt,module_kind='LBeam' if edge else 'InvertedT')
            pieces.beam(rr,edge=edge)
            if y<0:rr.rotation_euler.z=math.pi
    for row,cy in enumerate((-SPAN/2,SPAN/2,*[-(i+1.5)*SPAN for i in range(rear_spans-1)])):
        for i in range(tee_count):
            x=-L/2+(i+.5)*TEE
            core_index=i-(tee_count-6)//2
            rr=G.root(f'Flat_L2_R{row}_T{core_index}',(x,cy,FLOOR),rt,module_kind='DoubleTee');source(rr)
            if i%2==0:
                for yy in (cy-2.5,cy+2.5):
                    fr=G.root(f'Fixture_{row}_{i}_{yy}',(x,yy,FLOOR-.7024),rt,module_kind='Fixture');pieces.fixture(fr,refined=True,strap=.5524)
    closure=G.Mesh('Inner closure pour comparison',rt)
    for y in transverse:
        if y not in (ymin,ymax):closure.box((0,y,FLOOR-.025),(L,.08,.05),'Deck')
    closure.finish()
    marks=G.Mesh('Parking markings comparison',rt)
    for i,x in enumerate((-7.0,-2.7,4.2,8.4)):
        s=dict(x=x,y=12.,z=0,yaw=180,depth=DEPTH,width=STALL,level=0,ramp=False);p['stalls'].append(s)
        for xx in (x-STALL/2,x+STALL/2):marks.quad([(xx-.045,9.25,.006),(xx+.045,9.25,.006),(xx+.045,14.75,.006),(xx-.045,14.75,.006)])
    marks.finish()
    for side in (-1,1):
        for x in centers:
            rr=G.root(f'Facade_0_{side}_{x}',(x,ymin if side<0 else ymax,0),rt,module_kind='Spandrel');pieces.spandrel(rr,refined=True)
    notice=G.Mesh('Column level and payment notice',rt)
    notice.box((.12,-.386,.80),(.45,.01,.86),'White')
    for z,h,key in ((1.08,.22,'LEVEL 2'),(.78,.10,'PAY BEFORE RETURNING'),(.57,.10,'PAY HERE')):
        notice.quad([(-.09,-.392,z-h/2),(.33,-.392,z-h/2),(.33,-.392,z+h/2),(-.09,-.392,z+h/2)],layout[key],'Graphics')
    notice.finish()
    pts=[]
    for i in range(65):
        a=i*math.tau/64;pts.append([6.3*math.cos(a)+3.5*math.copysign(1,math.cos(a)),4.2*math.sin(a),0])
    p['paths']=[dict(name='Drive_Up_Comparison',points=pts,width=7.3152)];p['pedestrian_paths']=[]
    p['bounds_m']=G.bounds(members(rt));p['garage_triangles']=G.triangles(members(rt))
    Path('build/lookdev/comparison-precast.json').write_text(json.dumps(p,indent=2)+'\n')
    return rt,p
